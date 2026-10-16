import unittest
from message_history import MessageHistory

class MessageHistoryTests(unittest.TestCase):
    def setUp(self):
        self.h = MessageHistory()
        self.base = {"authorized": True, "chat_id": "demo", "message_id": "1"}
    def test_new(self):
        self.assertEqual(self.h.apply(dict(self.base, type="new", text="RAG"))["revision"], 1)
    def test_edit(self):
        self.h.apply(dict(self.base, type="new", text="RAG"))
        self.assertEqual(self.h.apply(dict(self.base, type="edit", text="RAG v2"))["revision"], 2)
    def test_duplicate_edit(self):
        self.h.apply(dict(self.base, type="new", text="RAG"))
        self.assertEqual(self.h.apply(dict(self.base, type="edit", text="RAG"))["change"], "unchanged")
    def test_delete(self):
        self.h.apply(dict(self.base, type="new", text="RAG"))
        self.assertTrue(self.h.apply(dict(self.base, type="delete"))["change"] == "delete")
        self.assertTrue(self.h.messages[("demo", "1")].deleted)
    def test_not_authorized(self):
        with self.assertRaises(PermissionError):
            self.h.apply(dict(self.base, authorized=False, type="new", text="RAG"))
    def test_unknown_edit(self):
        with self.assertRaises(ValueError):
            self.h.apply(dict(self.base, type="edit", text="RAG"))
if __name__ == "__main__":
    unittest.main()
