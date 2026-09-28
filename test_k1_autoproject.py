import json
from pathlib import Path
import tempfile
import unittest

import k1_autoproject as k1


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


class K1AutoProjectTests(unittest.TestCase):
    def test_mojibake_repair_is_non_destructive_candidate(self):
        bad = "Р¤СѓРЅРґР°РјРµРЅС‚Р°Р»СЊРЅС‹Р№"
        fixed, changed = k1.repair_mojibake(bad)
        self.assertTrue(changed)
        self.assertNotEqual(fixed, bad)

    def test_master_build_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            backup = root / "backup"
            registry.mkdir()
            inventory = root / "inventory.json"
            sha = "a" * 64
            write_json(inventory, {
                "source_root": str(root / "books"),
                "items": [{
                    "item_id":"BOOK-1","relative_path":"a.pdf","file_name":"a.pdf",
                    "normalized_title":"Book A","format":"PDF","extension":".pdf",
                    "size_bytes":10,"page_count":1,"sha256":sha
                }]
            })
            first = k1.build_master(registry, inventory, backup)
            second = k1.build_master(registry, inventory, backup)
            sources = k1.jsonl_load(registry / "sources.jsonl")
            copies = k1.jsonl_load(registry / "physical_copies.jsonl")
            self.assertEqual(first.status, "PASS")
            self.assertEqual(second.status, "PASS")
            self.assertEqual(len(sources), 1)
            self.assertEqual(len(copies), 1)
            self.assertEqual(sources[0]["physical_copies"], 1)


    def test_master_build_accepts_array_inventory_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            backup = root / "backup"
            registry.mkdir()
            inventory = root / "inventory-array.json"
            sha = "e" * 64
            write_json(inventory, [{
                "item_id":"BOOK-2","path":str(root/"b.pdf"),"file_name":"b.pdf",
                "normalized_title":"Book B","format":"PDF","extension":".pdf",
                "size_bytes":11,"page_count":2,"sha256":sha
            }])
            result = k1.build_master(registry, inventory, backup)
            self.assertEqual(result.status, "PASS")
            self.assertEqual(len(k1.jsonl_load(registry / "sources.jsonl")), 1)

    def test_document_import_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            backup = root / "backup"
            registry.mkdir()
            k1.jsonl_write(registry / "sources.jsonl", [], backup)
            k1.jsonl_write(registry / "physical_copies.jsonl", [], backup)
            catalog = root / "catalog.json"
            write_json(catalog, [{
                "sha256":"b"*64,
                "path":str(root/"152-fz.pdf"),
                "title_candidate":"Федеральный закон 152-ФЗ",
                "page_count":20,"size":1000,
                "review_required":False,
                "current_revision_verified":False
            }])
            k1.import_document_catalog(registry, catalog, backup)
            k1.import_document_catalog(registry, catalog, backup)
            self.assertEqual(len(k1.jsonl_load(registry/"sources.jsonl")), 1)
            self.assertEqual(len(k1.jsonl_load(registry/"physical_copies.jsonl")), 1)


    def test_existing_generic_source_is_promoted_by_catalog_legal_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            backup = root / "backup"
            registry.mkdir()
            sha = "f" * 64
            k1.jsonl_write(registry / "sources.jsonl", [{
                "source_id": k1.stable_source_id(sha),
                "sha256": sha,
                "content_digest": "sha256:" + sha,
                "raw_title": "document.pdf",
                "source_type_candidate": "DOCUMENT",
                "document_kind_candidate": "UNKNOWN_DOCUMENT"
            }])
            k1.jsonl_write(registry / "physical_copies.jsonl", [])
            catalog = root / "catalog.json"
            write_json(catalog, [{
                "sha256": sha,
                "path": str(root / "152-fz.pdf"),
                "title_candidate": "Федеральный закон 152-ФЗ",
                "page_count": 10,
                "size": 100,
                "review_required": False,
                "current_revision_verified": False
            }])
            result = k1.import_document_catalog(registry, catalog, backup)
            src = k1.jsonl_load(registry / "sources.jsonl")[0]
            self.assertEqual(result.status, "PASS")
            self.assertEqual(src["source_type_candidate"], "LEGAL_DOCUMENT")
            self.assertEqual(src["document_kind_candidate"], "FEDERAL_LAW")

    def test_legal_registry_can_promote_from_provenance_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            backup = root / "backup"
            sha = "1" * 64
            sid = k1.stable_source_id(sha)
            k1.jsonl_write(root / "sources.jsonl", [{
                "source_id": sid,
                "sha256": sha,
                "content_digest": "sha256:" + sha,
                "raw_title": "unknown.pdf"
            }])
            k1.jsonl_write(root / "source_provenance.jsonl", [{
                "source_id": sid,
                "title_candidate": "Приказ Минздрава № 123",
                "source_path": "x.pdf",
                "date_number_candidates": ["№ 123"]
            }])
            result = k1.build_legal_registry(root, backup)
            rows = k1.jsonl_load(root / "legal_documents.jsonl")
            self.assertEqual(result.status, "PASS")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["identity"]["document_kind"], "ORDER")

    def test_invariants_block_duplicate_physical_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sha = "c"*64
            k1.jsonl_write(root/"sources.jsonl", [{
                "source_id":k1.stable_source_id(sha),"sha256":sha,
                "content_digest":"sha256:"+sha
            }])
            k1.jsonl_write(root/"physical_copies.jsonl", [
                {"source_id":k1.stable_source_id(sha),"path":"x.pdf"},
                {"source_id":k1.stable_source_id(sha),"path":"x.pdf"},
            ])
            result = k1.validate_invariants(root)
            self.assertEqual(result.status, "BLOCKED")

    def test_semantic_parser_does_not_promote_legal_status(self):
        text = "ФЕДЕРАЛЬНЫЙ ЗАКОН от 27 июля 2006 г. № 152-ФЗ вступает в силу"
        legal={"legal_document_id":"LDOC-1"}
        src={"source_id":"SRC-1","sha256":"d"*64,"raw_title":"152-ФЗ"}
        candidate=k1.semantic_from_text(text,legal,src,"x.pdf",1)
        self.assertEqual(candidate["identity"]["document_number_candidates"][0],"152-ФЗ")
        self.assertEqual(candidate["lifecycle"]["adoption_date_candidates"][0]["normalized"],"2006-07-27")
        self.assertEqual(candidate["lifecycle"]["legal_status"],"UNVERIFIED")
        self.assertFalse(candidate["officiality"]["official_source_verified"])

    def test_official_queue_is_human_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            backup=root/"backup"
            write_json(root/"legal_document_semantic_candidate.json",{
                "legal_document_id":"LDOC-1","source_id":"SRC-1",
                "identity":{"canonical_name_candidate":"Test","document_kind_candidate":"ORDER",
                            "document_number_candidates":["1"],"jurisdiction_candidate":"RU"},
                "lifecycle":{"adoption_date_candidates":[{"normalized":"2026-01-01"}],"legal_status":"UNVERIFIED"},
                "officiality":{"official_source_verified":False}
            })
            result=k1.build_official_queue(root,backup)
            self.assertEqual(result.status,"HUMAN_GATE")
            rows=k1.jsonl_load(root/"legal_official_verification_queue.jsonl")
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]["status"],"PENDING_OFFICIAL_VERIFICATION")

    def test_metrics_keep_unmeasured_values_as_no_data(self):
        stages=[k1.StageResult("x","PASS",read_records=5,written_records=5,duration_seconds=1)]
        with tempfile.TemporaryDirectory() as tmp:
            m=k1.history_metrics(Path(tmp)/"history.jsonl",stages)
        self.assertEqual(m["speedup_vs_single_stream"],"NO_DATA")
        self.assertEqual(m["eta"],"NO_DATA")
        self.assertEqual(m["rework_ratio"],"NO_DATA")


if __name__ == "__main__":
    unittest.main()
