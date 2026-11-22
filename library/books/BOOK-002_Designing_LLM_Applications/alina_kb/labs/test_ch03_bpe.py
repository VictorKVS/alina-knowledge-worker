import unittest
from ch03_bpe import CORPUS,pairs,merge,train

class BPETest(unittest.TestCase):
    def test_first_merge(self):
        counts=pairs([list(x) for x in CORPUS])
        self.assertEqual(counts[("a","p")],3)
        self.assertEqual(train(steps=1)[0][0][0],("a","p"))
    def test_sequence_merge(self):
        self.assertEqual(merge([list("cap")],("a","p")),[["c","ap"]])
    def test_no_loss(self):
        _,seq=train(steps=5)
        self.assertEqual(["".join(x) for x in seq],CORPUS)
    def test_zero_steps(self):
        self.assertEqual(train(steps=0)[0],[])
if __name__=="__main__":unittest.main()
