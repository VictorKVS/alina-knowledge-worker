import tempfile
import unittest
from pathlib import Path

import book_source


class BookSourceTests(unittest.TestCase):
    def test_invalid_page_range_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(book_source.BookSourceError):
                book_source.chapter_source_bundle(Path(td)/"missing.pdf", 5, 4, Path(td)/"out")


if __name__ == "__main__":
    unittest.main()
