import unittest
from decision import Source, classify

class TestDocumentIntake(unittest.TestCase):
    def test_denied(self): self.assertEqual(classify(Source("a", "denied")), "REJECT")
    def test_unknown_rights(self): self.assertEqual(classify(Source("a")), "QUARANTINE")
    def test_sensitive(self): self.assertEqual(classify(Source("a", "approved", sensitive=True)), "QUARANTINE")
    def test_incomplete(self): self.assertEqual(classify(Source("a", "approved", extraction_ok=False)), "REVIEW")
    def test_new_revision_priority(self): self.assertEqual(classify(Source("a", "approved", exact_duplicate=True, new_revision=True)), "NEW_VERSION")
    def test_duplicate(self): self.assertEqual(classify(Source("a", "approved", exact_duplicate=True)), "LINK_DUPLICATE")
    def test_syndicated(self): self.assertEqual(classify(Source("a", "approved", syndicated=True)), "RELATED_VARIANT")
    def test_new_evidence(self): self.assertEqual(classify(Source("a", "approved", new_evidence=True)), "INGEST_NEW")
    def test_near_uncertain(self): self.assertEqual(classify(Source("a", "approved", near_match=True)), "REVIEW")
if __name__ == "__main__": unittest.main()
