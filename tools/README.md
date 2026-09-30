# tools

Helpers for consuming `README.md` as data. Nothing here modifies `README.md`,
so this fork stays mergeable with upstream.

## `build_apis_json.py`

Turns the curated Markdown table into `apis.json`.

```bash
python3 tools/build_apis_json.py                 # -> tools/dist/apis.json
python3 tools/build_apis_json.py --report        # also list the anomalies found
python3 tools/build_apis_json.py -o public/apis.json --indent 0   # compact, for a web app
python3 tools/build_apis_json.py --check         # exit 1 on an unresolved anomaly
```

No dependencies beyond the standard library.

`--check` passes on the current `README.md`. It only fails on anomalies the
builder cannot repair (an unknown `auth`/`https`/`cors` value, or a 6th cell
carrying data), which makes it usable as a signal that a *new* kind of defect
has appeared upstream. Resolved ones — duplicate URLs, empty trailing cells —
are reported but do not fail it.

## Tests

```bash
cd tools && python3 -m unittest discover tests/ --verbose
```

19 tests: each defense is covered by a synthetic case, plus three assertions
against the real `README.md` (all values valid, no duplicate URLs, no
unresolved anomalies).

### Output shape

```json
{
  "source": "README.md",
  "stats": { "total": 1829, "categories": 51, "auth": {...}, "no_auth_and_cors": 372 },
  "anomalies": [ { "line": 641, "kind": "duplicate_url", "detail": "..." } ],
  "apis": [
    {
      "name": "Open-Meteo",
      "url": "https://open-meteo.com/",
      "description": "Free weather API for non-commercial use",
      "auth": "No",
      "https": "Yes",
      "cors": "Yes",
      "category": "Environment"
    }
  ]
}
```

`--keep-source-line` adds a `source_line` field to each entry, which is handy
when reporting a data problem back upstream.

## Why the defenses exist

`README.md` is hand-curated, so a naive parser trips over real quirks in the
file. Each defense below was added against a defect measured in the current
`README.md`, not a hypothetical one.

| Defect in `README.md` | Count | What the builder does |
|:---|--:|:---|
| Backticked HTTPS/CORS values (`` `Yes` ``, `` `Unknown` ``) | 1 row | Strips backticks from `auth`, `https` and `cors` alike, so the value passes validation instead of failing every filter |
| Duplicate documentation URLs (some differ only by a trailing slash) | 4 | Normalizes the URL, keeps the first entry, reports the rest as `duplicate_url` |
| Rows with extra trailing pipes (6 or 7 cells instead of 5) | 92 | Reads the first 5 cells, ignores trailing empty ones, reports them as `extra_column_empty` |
| Rows padded with multiple spaces around cells | 1 | Cells are stripped, so alignment padding is not part of the value |
| `|:---|` separator rows and `| API | Description | ... |` header rows | 47 | Only rows whose first cell is `[title](link)` are read, so neither can leak in as an entry |
| 3-column sponsor table above the catalogue | 11 rows | Parsing starts at `## Index`, and rows with fewer than 5 cells are skipped |

Verified on the current `README.md`: 1,829 unique entries, 51 categories, zero
invalid `auth`/`https`/`cors` values, zero entries without a category.

## Note on `scripts/validate/format.py`

Upstream's own validator reports 567 errors on this `README.md`, but 496 of
them are phantoms: `format.py` skips separator rows with
`line_content.startswith('|---')`, while 46 of the 47 separator rows are
written as `|:---|`, so each one is parsed as a broken API entry. Matching
`^\|\s*:?-{3,}` instead brings the count to 71 real findings.

That is an upstream fix, not something this fork applies — editing `README.md`
or `scripts/` here would only make future merges from upstream conflict.
