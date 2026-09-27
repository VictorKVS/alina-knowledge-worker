import json
from pathlib import Path
import tempfile
import unittest

import k1_pipeline


def write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n", encoding="utf-8")


class K1PipelineTests(unittest.TestCase):
    def test_official_gate_stops_unverified_legal_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = {
                "officiality": {"official_source_verified": False},
                "lifecycle": {"legal_status": "UNVERIFIED"},
            }
            (root / "legal_document_semantic_candidate.json").write_text(
                json.dumps(payload), encoding="utf-8"
            )
            result = k1_pipeline.official_gate(root)
            self.assertEqual(result.status, "HUMAN_GATE")

    def test_master_registry_detects_orphan_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_jsonl(root / "sources.jsonl", [{"source_id": "SRC-1", "sha256": "abc"}])
            write_jsonl(root / "physical_copies.jsonl", [{"source_id": "SRC-NOT-FOUND", "path": "x.pdf"}])
            result = k1_pipeline.validate_master(root)
            self.assertEqual(result.status, "WARN")
            self.assertGreaterEqual(result.warnings, 1)

    def test_metrics_do_not_invent_speedup_or_eta(self):
        stages = [k1_pipeline.StageResult("x", "PASS", records=5, duration_seconds=1.0)]
        metrics = k1_pipeline.compute_metrics(stages)
        self.assertEqual(metrics["speedup_vs_single_stream"], "NO_DATA")
        self.assertEqual(metrics["rework_ratio"], "NO_DATA")
        self.assertEqual(metrics["eta"], "NO_DATA")


if __name__ == "__main__":
    unittest.main()
