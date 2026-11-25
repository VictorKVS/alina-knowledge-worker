import unittest
from search import search, tokenize

class TestSearch(unittest.TestCase):
    def test_rag_document_found(self):
        self.assertEqual(search("RAG информация")[0][1], "rag")

    def test_gpu_document_found(self):
        self.assertEqual(search("GPU видеопамять")[0][1], "gpu")

    def test_out_of_scope_has_no_fake_answer(self):
        self.assertEqual(search("акваланг морская звезда"), [])

    def test_empty_question(self):
        self.assertEqual(search("?!"), [])

    def test_normalization(self):
        self.assertEqual(tokenize("RAG rag"), {"rag"})

if __name__ == "__main__":
    unittest.main()
