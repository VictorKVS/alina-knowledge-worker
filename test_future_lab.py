import unittest

from future_lab.methods import drift, historical_mean, mae, naive, rmse, simple_exponential_smoothing


class FutureLabTests(unittest.TestCase):
    def test_naive(self):
        self.assertEqual(naive([1, 2, 3], 2).forecast, [3.0, 3.0])

    def test_mean(self):
        self.assertEqual(historical_mean([1, 2, 3], 1).forecast, [2.0])

    def test_drift(self):
        self.assertEqual(drift([1, 3, 5], 2).forecast, [7.0, 9.0])

    def test_ses(self):
        r = simple_exponential_smoothing([10, 14], alpha=0.5, horizon=2)
        self.assertEqual(r.forecast, [12.0, 12.0])

    def test_metrics(self):
        self.assertEqual(mae([1, 2], [1, 4]), 1.0)
        self.assertAlmostEqual(rmse([1, 2], [1, 4]), 2 ** 0.5)


if __name__ == "__main__":
    unittest.main()
