import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from process_engine import init, get_process


class BookKnowledgeProcessTests(unittest.TestCase):
    def test_book_process_registers_and_has_full_pipeline(self):
        repo = Path(__file__).resolve().parent
        payload = json.loads((repo / "processes" / "alina_book_knowledge_factory.v1.json").read_text(encoding="utf-8"))
        required = {"TRANSLATE","SEMANTIC_ANALYSIS","KNOWLEDGE","APPLICATION","EXAMPLES","ALGORITHM","SYNTHESIS","OPERATIONALIZE","NORMALIZE","MAPPING","QA","CRITIC","HANDOFF","LEARN"}
        modes = {step["mode"] for step in payload["steps"]}
        self.assertTrue(required.issubset(modes))

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "processes").mkdir()
            (root / "processes" / "book.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            db = sqlite3.connect(":memory:")
            db.row_factory = sqlite3.Row
            init(db, root)
            loaded = get_process(db, "PROC-ALINA-BOOK-KNOWLEDGE-FACTORY")
            self.assertIsNotNone(loaded)
            self.assertEqual(len(loaded["steps"]), 19)


if __name__ == "__main__":
    unittest.main()
