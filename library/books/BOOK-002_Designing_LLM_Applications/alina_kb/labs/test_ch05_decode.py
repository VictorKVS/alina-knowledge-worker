import unittest
from ch05_decode import greedy,sample_top_k,sample_top_p,normalize

class TestDecode(unittest.TestCase):
    def test_normalization(self):self.assertAlmostEqual(sum(normalize([6,3,1])),1)
    def test_greedy(self):self.assertEqual(greedy(["a","b"],[0.6,0.4]),"a")
    def test_top_k_one(self):self.assertEqual(sample_top_k(["a","b"],[0.3,0.7],1),"b")
    def test_top_p_threshold(self):self.assertEqual(sample_top_p(["a","b"],[0.9,0.1],0.8),"a")
    def test_bad_k(self):
        with self.assertRaises(ValueError):sample_top_k(["a"],[1],2)
    def test_bad_p(self):
        with self.assertRaises(ValueError):sample_top_p(["a"],[1],0)
if __name__=="__main__":unittest.main()
