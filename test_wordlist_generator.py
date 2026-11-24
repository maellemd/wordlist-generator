import tempfile
import unittest
from pathlib import Path
from wordlist_generator import export_words, date_to_formats, passes_filter

class ExportTests(unittest.TestCase):
    def test_distinct_exports(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sample'
            export_words(['Demo'], path, True)
            self.assertEqual(path.read_text(), 'Demo\n')
            self.assertIn('1,Demo,4', path.with_suffix('.csv').read_text())

    def test_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sample.txt'
            path.write_text('original')
            with self.assertRaises(FileExistsError):
                export_words(['Demo'], path, False)
            self.assertEqual(path.read_text(), 'original')

    def test_collision(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sample.csv'
            with self.assertRaises(ValueError):
                export_words(['Demo'], path, True)
            self.assertFalse(path.exists())

    def test_existing_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sample.txt'
            path.with_suffix('.csv').write_text('original')
            with self.assertRaises(FileExistsError):
                export_words(['Demo'], path, True)
            self.assertFalse(path.exists())

    def test_missing_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                export_words(['Demo'], Path(directory) / 'missing' / 'sample.txt', False)

    def test_invalid_date(self):
        self.assertEqual(date_to_formats('invalid'), [])

    def test_filter(self):
        self.assertFalse(passes_filter('ab', 4, False, False))
        self.assertTrue(passes_filter('Demo1', 4, True, True))

if __name__ == '__main__':
    unittest.main()
