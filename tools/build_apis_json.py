#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a clean apis.json from README.md.

README.md is a hand-curated Markdown table, so it carries a few data quality
quirks that break naive parsers. This builder defends against the ones that
actually exist in the file today:

1. Backticked values in the HTTPS/CORS columns (e.g. ``| `Yes` | `Unknown` |``)
   -- backticks are stripped from auth, https and cors alike.
2. Duplicate documentation URLs (the same link listed twice, sometimes only
   differing by a trailing slash) -- the first entry wins, the rest are
   reported.
3. Rows carrying extra trailing pipes, so the row has 6 or 7 cells instead of
   5 -- the extra cells are ignored when empty, reported when not.
4. Category header rows and ``|:---|`` separator rows that a looser regex would
   pick up as entries -- only rows whose first cell is a ``[title](link)`` are
   read.

Usage:
    python tools/build_apis_json.py                      # README.md -> tools/dist/apis.json
    python tools/build_apis_json.py -o public/apis.json  # custom output path
    python tools/build_apis_json.py --report             # print anomalies found
    python tools/build_apis_json.py --check              # exit 1 if anomalies remain
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CATEGORY_ANCHOR = '### '
INDEX_HEADING = '## Index'

# The first cell of an entry is always "[title](documentation link)".
LINK_RE = re.compile(r'^\[(?P<name>.+)\]\((?P<url>.+)\)$')
# "|---|", "|:---|", "| :--- |" ... all forms of a table separator row.
SEPARATOR_RE = re.compile(r'^\|\s*:?-{3,}')

AUTH_VALUES = ('apiKey', 'OAuth', 'X-Mashape-Key', 'User-Agent', 'No')
HTTPS_VALUES = ('Yes', 'No')
CORS_VALUES = ('Yes', 'No', 'Unknown')

NUM_COLUMNS = 5

# Anomalies the builder cannot repair on its own; everything else it resolves
# (duplicates are dropped, empty trailing cells are ignored).
UNRESOLVED_KINDS = ('bad_auth', 'bad_https', 'bad_cors', 'extra_column_filled')


class Anomaly(Tuple[int, str, str]):
    """(line number, kind, detail)"""


def normalize_url(url: str) -> str:
    """Key used for duplicate detection: trailing slash is not a difference."""
    return url.rstrip('/')


def split_cells(line: str) -> List[str]:
    """Split a Markdown table row into its cells.

    Rows in README.md always start with a pipe; some also carry one or two
    extra trailing pipes, which show up as empty cells at the end.
    """
    return [cell.strip() for cell in line.split('|')[1:-1]]


def parse(lines: List[str]) -> Tuple[List[Dict[str, str]], List[Tuple[int, str, str]]]:
    """Parse README lines into entries plus a list of anomalies."""

    entries: List[Dict[str, str]] = []
    anomalies: List[Tuple[int, str, str]] = []
    category: Optional[str] = None

    for line_num, raw in enumerate(lines, start=1):
        line = raw.rstrip()

        if line.startswith(CATEGORY_ANCHOR):
            category = line[len(CATEGORY_ANCHOR):].strip()
            continue

        if not line.startswith('|') or SEPARATOR_RE.match(line):
            continue

        cells = split_cells(line)
        if len(cells) < NUM_COLUMNS:
            # The sponsor table near the top of the README has 3 columns.
            continue

        link_match = LINK_RE.match(cells[0])
        if not link_match:
            # Category header rows ("| API | Description | Auth | ... |").
            continue

        # Defense 3: tolerate extra trailing cells, but report non-empty ones.
        extra = cells[NUM_COLUMNS:]
        if extra:
            filled = [cell for cell in extra if cell]
            kind = 'extra_column_filled' if filled else 'extra_column_empty'
            anomalies.append((line_num, kind, f'{len(cells)} cells: {cells[0][:60]}'))

        # Defense 1: strip backticks from every flag column, not just auth.
        auth = cells[2].strip('`').strip()
        https = cells[3].strip('`').strip()
        cors = cells[4].strip('`').strip()

        if auth not in AUTH_VALUES:
            anomalies.append((line_num, 'bad_auth', f'{auth!r} in {cells[0][:60]}'))
        if https not in HTTPS_VALUES:
            anomalies.append((line_num, 'bad_https', f'{https!r} in {cells[0][:60]}'))
        if cors not in CORS_VALUES:
            anomalies.append((line_num, 'bad_cors', f'{cors!r} in {cells[0][:60]}'))
            cors = 'Unknown'

        entries.append({
            'name': link_match.group('name').strip(),
            'url': link_match.group('url').strip(),
            'description': cells[1],
            'auth': auth,
            'https': https,
            'cors': cors,
            'category': category or '',
            'source_line': line_num,
        })

    return entries, anomalies


def deduplicate(
    entries: List[Dict[str, str]]
) -> Tuple[List[Dict[str, str]], List[Tuple[int, str, str]]]:
    """Defense 2: drop entries whose documentation URL was already seen."""

    seen: Dict[str, Dict[str, str]] = {}
    unique: List[Dict[str, str]] = []
    anomalies: List[Tuple[int, str, str]] = []

    for entry in entries:
        key = normalize_url(entry['url'])
        first = seen.get(key)
        if first is not None:
            anomalies.append((
                entry['source_line'],
                'duplicate_url',
                f"{entry['url']} ({entry['category']}/{entry['name']}) "
                f"first seen L{first['source_line']} ({first['category']}/{first['name']})",
            ))
            continue
        seen[key] = entry
        unique.append(entry)

    return unique, anomalies


def build_stats(entries: List[Dict[str, str]]) -> Dict[str, Any]:
    auth = Counter(entry['auth'] for entry in entries)
    https = Counter(entry['https'] for entry in entries)
    cors = Counter(entry['cors'] for entry in entries)
    categories = Counter(entry['category'] for entry in entries)
    no_auth_cors = sum(
        1 for entry in entries if entry['auth'] == 'No' and entry['cors'] == 'Yes'
    )

    return {
        'total': len(entries),
        'categories': len(categories),
        'auth': dict(sorted(auth.items(), key=lambda kv: -kv[1])),
        'https': dict(sorted(https.items(), key=lambda kv: -kv[1])),
        'cors': dict(sorted(cors.items(), key=lambda kv: -kv[1])),
        'no_auth_and_cors': no_auth_cors,
        'per_category': dict(sorted(categories.items(), key=lambda kv: -kv[1])),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('readme', nargs='?', default='README.md', help='source Markdown file')
    parser.add_argument('-o', '--output', default='tools/dist/apis.json', help='output JSON path')
    parser.add_argument('--report', action='store_true', help='print the anomalies found')
    parser.add_argument('--check', action='store_true', help='exit 1 if anomalies were found')
    parser.add_argument('--indent', type=int, default=2, help='JSON indent (0 for compact)')
    parser.add_argument(
        '--keep-source-line',
        action='store_true',
        help='keep the source_line field in the output',
    )
    args = parser.parse_args()

    readme = Path(args.readme)
    if not readme.is_file():
        print(f'error: {readme} not found', file=sys.stderr)
        return 1

    lines = readme.read_text(encoding='utf-8').split('\n')

    # Only the catalogue below "## Index" holds API entries; the header above it
    # is sponsor content.
    try:
        start = next(i for i, line in enumerate(lines) if line.startswith(INDEX_HEADING))
    except StopIteration:
        start = 0
    offset_lines = lines[start:]

    entries, parse_anomalies = parse(offset_lines)
    for entry in entries:
        entry['source_line'] += start

    fixed_anomalies = []
    for line_num, kind, detail in parse_anomalies:
        fixed_anomalies.append((line_num + start, kind, detail))

    entries, dup_anomalies = deduplicate(entries)
    anomalies = sorted(fixed_anomalies + dup_anomalies)

    if not args.keep_source_line:
        for entry in entries:
            entry.pop('source_line', None)

    stats = build_stats(entries)
    payload = {
        'source': str(readme),
        'stats': stats,
        'anomalies': [
            {'line': line_num, 'kind': kind, 'detail': detail}
            for line_num, kind, detail in anomalies
        ],
        'apis': entries,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=args.indent or None) + '\n',
        encoding='utf-8',
    )

    print(f'{output}: {stats["total"]} APIs across {stats["categories"]} categories')
    print(f'  auth      : {stats["auth"]}')
    print(f'  https     : {stats["https"]}')
    print(f'  cors      : {stats["cors"]}')
    print(f'  no auth + cors: {stats["no_auth_and_cors"]}')

    kinds = Counter(kind for _, kind, _ in anomalies)
    print(f'  anomalies : {len(anomalies)} {dict(kinds)}')

    if args.report and anomalies:
        print('\n--- anomalies ---')
        for line_num, kind, detail in anomalies:
            print(f'(L{line_num:04d}) {kind}: {detail}')

    if args.check:
        # Only anomalies the builder could not resolve are blocking. Duplicate
        # URLs and empty trailing cells are handled, so they are reported but
        # do not fail the check -- that keeps --check usable as a CI signal for
        # *new* defects appearing upstream.
        blocking = [a for a in anomalies if a[1] in UNRESOLVED_KINDS]
        if blocking:
            print(f'\ncheck failed: {len(blocking)} unresolved anomalies', file=sys.stderr)
            for line_num, kind, detail in blocking:
                print(f'(L{line_num:04d}) {kind}: {detail}', file=sys.stderr)
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
