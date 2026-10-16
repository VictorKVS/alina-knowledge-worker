import unittest
from father_bridge import map_material, bridge_batch

class FatherBridgeTests(unittest.TestCase):
    def setUp(self):
        self.material = {
            "source_type": "telegram",
            "source_locator": "https://t.me/demo/4",
            "raw_text": "RAG query reranking released",
            "published_at": "2026-10-16T09:00:00Z",
            "metadata": {"chat_id": "demo", "message_id": "4"}
        }
    def test_normalizes_father_material(self):
        r = map_material(self.material, authorized_by_policy=True)
        self.assertEqual(r["message_id"], "4")
        self.assertEqual(r["url"], "https://t.me/demo/4")
    def test_missing_permission_excluded(self):
        items, stats = bridge_batch([self.material], authorized_by_policy=False)
        self.assertEqual(items, [])
        self.assertEqual(stats["skipped"], 1)
    def test_known_topic_is_quarantined(self):
        items, _ = bridge_batch([self.material], authorized_by_policy=True)
        self.assertEqual(items[0].status, "UNVERIFIED_CANDIDATE")
    def test_wrong_type_rejected(self):
        with self.assertRaises(ValueError):
            map_material({"source_type":"email"}, authorized_by_policy=True)
    def test_deduplicate(self):
        items, stats = bridge_batch([self.material, self.material], authorized_by_policy=True)
        self.assertEqual(len(items), 1)
        self.assertEqual(stats["duplicates"], 1)
if __name__ == "__main__":
    unittest.main()
