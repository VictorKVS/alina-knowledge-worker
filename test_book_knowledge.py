import json
import sqlite3
import unittest
from pathlib import Path

import book_knowledge

BASE = Path(__file__).resolve().parent


class BookKnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        book_knowledge.init(self.db)

    def tearDown(self):
        self.db.close()

    def test_book0001_ch01_package_validates(self):
        path = BASE / "docs" / "books" / "BOOK-0001" / "ch01" / "package.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(book_knowledge.validate_package(payload), [])

    def test_book0001_ch01_can_be_stored(self):
        path = BASE / "docs" / "books" / "BOOK-0001" / "ch01" / "package.json"
        payload = book_knowledge.load_package(path)
        result = book_knowledge.store_package(self.db, payload, str(path))
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        summary = book_knowledge.summary(self.db)
        self.assertEqual(summary["packages"], 1)
        self.assertEqual(summary["by_status"]["REVIEW_REQUIRED"], 1)

    def test_missing_translation_locator_fails(self):
        path = BASE / "docs" / "books" / "BOOK-0001" / "ch01" / "package.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["translation"][0].pop("locator")
        errors = book_knowledge.validate_package(payload)
        self.assertTrue(any("translation[0] missing locator" in e for e in errors))

    def test_alina_conclusion_requires_traceability(self):
        path = BASE / "docs" / "books" / "BOOK-0001" / "ch01" / "package.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["conclusions"].append({
            "conclusion_id": "BAD",
            "owner": "ALINA",
            "statement": "unsupported"
        })
        errors = book_knowledge.validate_package(payload)
        self.assertTrue(any("lacks traceability" in e for e in errors))

    def test_checklist_requires_source_knowledge(self):
        path = BASE / "docs" / "books" / "BOOK-0001" / "ch01" / "package.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["checklists"][0]["source_knowledge_ids"] = []
        errors = book_knowledge.validate_package(payload)
        self.assertTrue(any("missing source_knowledge_ids" in e for e in errors))

    def test_bundled_import_discovers_book0001(self):
        imported = book_knowledge.import_bundled_packages(self.db, BASE)
        self.assertTrue(any(item.get("status") == "REVIEW_REQUIRED" for item in imported))
        self.assertEqual(book_knowledge.summary(self.db)["packages"], 1)


if __name__ == "__main__":
    unittest.main()
