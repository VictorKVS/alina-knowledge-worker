from pathlib import Path
import tempfile
import unittest

from PIL import Image

from visual_review import compare_images


class VisualReviewTests(unittest.TestCase):
    def test_identical_images_have_zero_pixel_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a = root / "a.png"
            b = root / "b.png"
            Image.new("RGB", (64, 32), (10, 20, 30)).save(a)
            Image.new("RGB", (64, 32), (10, 20, 30)).save(b)

            report = compare_images(a, b)

            self.assertTrue(report["comparison"]["same_size"])
            self.assertFalse(report["comparison"]["resampled_for_metrics"])
            self.assertEqual(report["comparison"]["normalized_mae"], 0.0)
            self.assertEqual(report["comparison"]["changed_pixel_ratio"], 0.0)
            self.assertIsNone(report["comparison"]["difference_bbox"])
            self.assertEqual(report["semantic_review_status"], "required")

    def test_size_mismatch_is_explicit_and_metrics_are_resampled(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ref = root / "ref.png"
            impl = root / "impl.png"
            Image.new("RGB", (80, 40), (20, 30, 40)).save(ref)
            Image.new("RGB", (40, 20), (20, 30, 40)).save(impl)

            report = compare_images(ref, impl)

            self.assertFalse(report["comparison"]["same_size"])
            self.assertTrue(report["comparison"]["resampled_for_metrics"])
            self.assertEqual(report["comparison"]["normalized_mae"], 0.0)
            self.assertEqual(
                report["observations"][0]["category"], "viewport_geometry"
            )

    def test_pixel_difference_is_measured_without_semantic_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ref = root / "ref.png"
            impl = root / "impl.png"
            Image.new("RGB", (32, 32), (0, 0, 0)).save(ref)
            Image.new("RGB", (32, 32), (255, 255, 255)).save(impl)

            report = compare_images(ref, impl, threshold=24)

            self.assertGreater(report["comparison"]["normalized_mae"], 0.9)
            self.assertEqual(report["comparison"]["changed_pixel_ratio"], 1.0)
            self.assertEqual(
                report["semantic_review_note"].startswith("Pixel metrics are evidence"),
                True,
            )


if __name__ == "__main__":
    unittest.main()
