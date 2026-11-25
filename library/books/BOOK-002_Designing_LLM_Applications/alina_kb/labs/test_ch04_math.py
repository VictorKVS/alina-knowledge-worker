import unittest
from math import e
from ch04_math import cross_entropy_one_hot,perplexity_nats,softmax,toy_attention

class Tests(unittest.TestCase):
    def test_entropy_probability_one(self):
        self.assertAlmostEqual(cross_entropy_one_hot(1.0),0)
    def test_entropy_probability_decrease(self):
        self.assertGreater(cross_entropy_one_hot(0.1),cross_entropy_one_hot(0.8))
    def test_perplexity_natural_logs(self):
        self.assertAlmostEqual(perplexity_nats([1.0]),e)
    def test_weights_normalize(self):
        self.assertAlmostEqual(sum(softmax([1,0,0])),1)
    def test_attention(self):
        weights,output=toy_attention([1,0],[[1,0],[0,1]],[[2,0],[0,2]])
        self.assertGreater(weights[0],weights[1])
        self.assertAlmostEqual(sum(weights),1)
        self.assertAlmostEqual(sum(output),2)
    def test_invalid_probability(self):
        with self.assertRaises(ValueError):cross_entropy_one_hot(0)
if __name__=="__main__":unittest.main()
