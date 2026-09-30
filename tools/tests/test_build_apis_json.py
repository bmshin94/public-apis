# -*- coding: utf-8 -*-

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_apis_json import (  # noqa: E402
    UNRESOLVED_KINDS,
    deduplicate,
    normalize_url,
    parse,
    split_cells,
)

SAMPLE = """## Index
* [Test](#test)

### Test
API | Description | Auth | HTTPS | CORS |
|:---|:---|:---|:---|:---|
| [Good](https://good.example.com) | Fine entry | No | Yes | Yes |
| [Backticked](https://bt.example.com) | Backticks everywhere | `apiKey` | `Yes` | `Unknown` |
| [DupeA](https://dupe.example.com) | First | No | Yes | Yes |
| [DupeB](https://dupe.example.com/) | Second, trailing slash | No | Yes | Yes |
| [TrailingPipes](https://tp.example.com) | Extra empty cells | No | Yes | Yes | | |
| [Padded](https://padded.example.com)     | Alignment padding    | No     | Yes  | No  |
| [BadAuth](https://bad.example.com) | Invalid values | `token` | Yes | Maybe |
| [Junk](https://junk.example.com) | Leftover data in 6th cell | No | Yes | Yes | oops |
""".split('\n')


class TestSplitCells(unittest.TestCase):

    def test_strips_padding(self):
        cells = split_cells('|  [A](https://a.example.com)   |  Desc  | No | Yes | No |')
        self.assertEqual(cells[0], '[A](https://a.example.com)')
        self.assertEqual(cells[1], 'Desc')

    def test_trailing_pipes_become_empty_cells(self):
        cells = split_cells('| [A](https://a.example.com) | Desc | No | Yes | Yes | | |')
        self.assertEqual(len(cells), 7)
        self.assertEqual(cells[5:], ['', ''])


class TestNormalizeUrl(unittest.TestCase):

    def test_trailing_slash_is_not_a_difference(self):
        self.assertEqual(
            normalize_url('https://dupe.example.com/'),
            normalize_url('https://dupe.example.com'),
        )


class TestParse(unittest.TestCase):

    def setUp(self):
        self.entries, self.anomalies = parse(SAMPLE)
        self.by_name = {entry['name']: entry for entry in self.entries}

    def test_header_and_separator_rows_are_not_entries(self):
        names = set(self.by_name)
        self.assertNotIn('API', names)
        self.assertFalse(any(':---' in name for name in names))
        self.assertEqual(len(self.entries), 8)

    def test_every_entry_keeps_its_category(self):
        self.assertTrue(all(entry['category'] == 'Test' for entry in self.entries))

    def test_backticks_are_stripped_from_all_flag_columns(self):
        entry = self.by_name['Backticked']
        self.assertEqual(entry['auth'], 'apiKey')
        self.assertEqual(entry['https'], 'Yes')
        self.assertEqual(entry['cors'], 'Unknown')

    def test_backticked_values_are_not_reported_as_anomalies(self):
        kinds = {kind for _, kind, detail in self.anomalies if 'Backticked' in detail}
        self.assertEqual(kinds, set())

    def test_row_with_extra_empty_cells_is_parsed(self):
        entry = self.by_name['TrailingPipes']
        self.assertEqual((entry['auth'], entry['https'], entry['cors']), ('No', 'Yes', 'Yes'))

    def test_extra_empty_cells_are_reported_but_resolved(self):
        kinds = [kind for _, kind, detail in self.anomalies if 'TrailingPipes' in detail]
        self.assertEqual(kinds, ['extra_column_empty'])
        self.assertNotIn('extra_column_empty', UNRESOLVED_KINDS)

    def test_alignment_padding_is_not_part_of_the_value(self):
        entry = self.by_name['Padded']
        self.assertEqual(entry['description'], 'Alignment padding')
        self.assertEqual((entry['auth'], entry['https'], entry['cors']), ('No', 'Yes', 'No'))

    def test_invalid_values_are_reported(self):
        kinds = {kind for _, kind, detail in self.anomalies if 'BadAuth' in detail}
        self.assertEqual(kinds, {'bad_auth', 'bad_cors'})

    def test_invalid_cors_falls_back_to_unknown(self):
        self.assertEqual(self.by_name['BadAuth']['cors'], 'Unknown')

    def test_non_empty_extra_cell_is_unresolved(self):
        kinds = [kind for _, kind, detail in self.anomalies if 'Junk' in detail]
        self.assertEqual(kinds, ['extra_column_filled'])
        self.assertIn('extra_column_filled', UNRESOLVED_KINDS)


class TestDeduplicate(unittest.TestCase):

    def setUp(self):
        entries, _ = parse(SAMPLE)
        self.unique, self.anomalies = deduplicate(entries)

    def test_first_entry_wins(self):
        names = [entry['name'] for entry in self.unique]
        self.assertIn('DupeA', names)
        self.assertNotIn('DupeB', names)

    def test_duplicate_is_reported(self):
        kinds = [kind for _, kind, _ in self.anomalies]
        self.assertEqual(kinds, ['duplicate_url'])

    def test_no_duplicate_urls_remain(self):
        keys = [normalize_url(entry['url']) for entry in self.unique]
        self.assertEqual(len(keys), len(set(keys)))


class TestRealReadme(unittest.TestCase):
    """The defenses exist because of defects in the real README.md."""

    @classmethod
    def setUpClass(cls):
        readme = Path(__file__).resolve().parents[2] / 'README.md'
        if not readme.is_file():
            raise unittest.SkipTest('README.md not found')
        lines = readme.read_text(encoding='utf-8').split('\n')
        start = next(i for i, line in enumerate(lines) if line.startswith('## Index'))
        entries, cls.anomalies = parse(lines[start:])
        cls.entries, dup = deduplicate(entries)
        cls.anomalies += dup

    def test_all_values_are_valid(self):
        for entry in self.entries:
            self.assertIn(entry['auth'], ('apiKey', 'OAuth', 'X-Mashape-Key', 'User-Agent', 'No'))
            self.assertIn(entry['https'], ('Yes', 'No'))
            self.assertIn(entry['cors'], ('Yes', 'No', 'Unknown'))
            self.assertTrue(entry['category'])
            self.assertTrue(entry['url'].startswith('http'))

    def test_no_duplicate_urls_remain(self):
        keys = [normalize_url(entry['url']) for entry in self.entries]
        self.assertEqual(len(keys), len(set(keys)))

    def test_no_unresolved_anomalies(self):
        blocking = [a for a in self.anomalies if a[1] in UNRESOLVED_KINDS]
        self.assertEqual(blocking, [])


if __name__ == '__main__':
    unittest.main()
