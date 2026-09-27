"""K1 auto-pipeline controller for local FATHER/ALINA source registries.

The controller never mutates source documents. It validates approved K1
artifacts, records measurable process metrics, and stops at the first review
gate that requires human or authoritative legal verification.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from typing import Any

APPROACHES = {
    "reuse_existing_audit": {
        "expectation": "Reuse existing inventories instead of rescanning originals.",
        "better_when": "A trustworthy inventory with hashes/provenance already exists.",
        "worse_when": "Inventory is stale, incomplete, or lacks content hashes.",
    },
    "sha256_dedup": {
        "expectation": "Collapse byte-identical copies without deleting originals.",
        "better_when": "The same digital file exists in multiple locations.",
        "worse_when": "Different editions/translations represent the same work but have different hashes.",
    },
    "candidate_first_identity": {
        "expectation": "Extract candidates first; verify before promoting them to canonical fields.",
        "better_when": "Filenames/metadata are noisy and false positives are costly.",
        "worse_when": "Very clean curated metadata already exists and extra review adds little value.",
    },
    "official_verification_gate": {
        "expectation": "Never assert current legal status from a local PDF alone.",
        "better_when": "Legal/current-revision correctness matters.",
        "worse_when": "No authoritative source is reachable; pipeline must stop for review.",
    },
}

@dataclass
class StageResult:
    stage: str
    status: str
    records: int = 0
    warnings: int = 0
    errors: int = 0
    duration_seconds: float = 0.0
    detail: str = ""

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows

def timed(stage: str, fn) -> StageResult:
    started = time.monotonic()
    result = fn()
    result.duration_seconds = round(time.monotonic() - started, 6)
    result.stage = stage
    return result

def validate_master(root: Path) -> StageResult:
    sources = read_jsonl(root / "sources.jsonl")
    copies = read_jsonl(root / "physical_copies.jsonl")
    if not sources:
        return StageResult("", "BLOCKED", errors=1, detail="sources.jsonl missing or empty")
    by_id = {str(x.get("source_id")) for x in sources if x.get("source_id")}
    orphan = sum(1 for x in copies if x.get("source_id") not in by_id)
    missing_hash = sum(1 for x in sources if not x.get("sha256"))
    return StageResult("", "PASS" if orphan == 0 else "WARN", len(sources),
                       warnings=missing_hash + orphan,
                       detail=f"physical_copies={len(copies)}; orphan_copies={orphan}; sources_without_sha={missing_hash}")

def validate_identity(root: Path) -> StageResult:
    rows = read_jsonl(root / "identity_candidates.jsonl")
    if not rows:
        return StageResult("", "BLOCKED", errors=1, detail="identity_candidates.jsonl missing or empty")
    unresolved = sum(1 for x in rows if x.get("identity_status") in {None, "UNRESOLVED", "NEEDS_IDENTIFICATION"})
    mojibake = sum(1 for x in rows if x.get("mojibake_detected"))
    return StageResult("", "PASS", len(rows), warnings=unresolved,
                       detail=f"unresolved={unresolved}; mojibake_detected={mojibake}")

def validate_document_import(root: Path) -> StageResult:
    preview = read_jsonl(root / "document_corpus_import_preview.jsonl")
    if not preview:
        return StageResult("", "SKIP", detail="document corpus preview not present")
    review = sum(1 for x in preview if x.get("review_required") is True or x.get("import_action") == "REVIEW_NO_HASH")
    legal = sum(1 for x in preview if x.get("source_type_candidate") == "LEGAL_DOCUMENT")
    new = sum(1 for x in preview if x.get("import_action") == "CREATE_SOURCE_CANDIDATE")
    return StageResult("", "PASS", len(preview), warnings=review,
                       detail=f"legal_candidates={legal}; new_sources={new}; review={review}")

def validate_legal_registry(root: Path) -> StageResult:
    rows = read_jsonl(root / "legal_documents.jsonl")
    if not rows:
        return StageResult("", "BLOCKED", errors=1, detail="legal_documents.jsonl missing or empty")
    unresolved = sum(1 for x in rows if ((x.get("processing") or {}).get("identity_resolved") is not True))
    return StageResult("", "PASS", len(rows), warnings=unresolved,
                       detail=f"identity_unresolved={unresolved}")

def validate_semantic_candidate(root: Path) -> StageResult:
    path = root / "legal_document_semantic_candidate.json"
    if not path.exists():
        return StageResult("", "BLOCKED", errors=1, detail="semantic candidate missing")
    row = read_json(path)
    identity = row.get("identity") or {}
    lifecycle = row.get("lifecycle") or {}
    number_count = len(identity.get("document_number_candidates") or [])
    date_count = len(lifecycle.get("adoption_date_candidates") or [])
    confidence = float(row.get("confidence") or 0.0)
    warnings = int(number_count == 0) + int(date_count == 0) + int(confidence < 0.70)
    return StageResult("", "PASS" if warnings < 3 else "WARN", 1, warnings=warnings,
                       detail=f"number_candidates={number_count}; adoption_dates={date_count}; confidence={confidence:.2f}")

def official_gate(root: Path) -> StageResult:
    path = root / "legal_document_semantic_candidate.json"
    if not path.exists():
        return StageResult("", "BLOCKED", errors=1, detail="cannot evaluate official gate without semantic candidate")
    row = read_json(path)
    official = row.get("officiality") or {}
    lifecycle = row.get("lifecycle") or {}
    verified = bool(official.get("official_source_verified"))
    status = lifecycle.get("legal_status")
    if verified and status not in {None, "", "UNVERIFIED", "UNKNOWN"}:
        return StageResult("", "PASS", 1, detail=f"official_source_verified=true; legal_status={status}")
    return StageResult("", "HUMAN_GATE", 1, warnings=1,
                       detail="Official source/current revision/legal status are not verified.")

def compute_metrics(stages):
    attempted = len(stages)
    auto_completed = sum(1 for s in stages if s.status in {"PASS", "SKIP", "WARN"})
    duration = sum(s.duration_seconds for s in stages)
    records = sum(s.records for s in stages)
    throughput = records / duration if duration > 0 else None
    return {
        "attempted_stages": attempted,
        "auto_completed_stages": auto_completed,
        "human_gates": sum(1 for s in stages if s.status == "HUMAN_GATE"),
        "blocked_stages": sum(1 for s in stages if s.status == "BLOCKED"),
        "automation_yield_pct": round(100 * auto_completed / attempted, 2) if attempted else 0.0,
        "warning_count": sum(s.warnings for s in stages),
        "error_count": sum(s.errors for s in stages),
        "records_observed": records,
        "wall_seconds": round(duration, 6),
        "observed_records_per_second": round(throughput, 3) if throughput is not None else None,
        "rework_ratio": "NO_DATA",
        "speedup_vs_single_stream": "NO_DATA",
        "eta": "NO_DATA",
        "note": "No speedup/rework/ETA is invented without comparable telemetry.",
    }

def write_outputs(out_dir: Path, run):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "latest.json").write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out_dir / "history.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(run, ensure_ascii=False) + "\n")
    journal = out_dir / "DEV_JOURNAL_K1.md"
    lines = [
        "# K1 development journal", "",
        f"## Run {run['run_id']}",
        f"- Started: {run['started_at']}",
        f"- Finished: {run['finished_at']}",
        f"- Stop reason: {run['stop_reason']}",
        f"- First human gate: {run['first_human_gate'] or 'none'}",
        "", "### Stage results",
    ]
    for s in run["stages"]:
        lines.append(f"- {s['stage']} — {s['status']} — records={s['records']}, warnings={s['warnings']}, errors={s['errors']} — {s['detail']}")
    lines += ["", "### Metrics", json.dumps(run["metrics"], ensure_ascii=False, indent=2), ""]
    with journal.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-root", default=r"G:\1\FATHER\data\source_registry")
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parent / "data" / "k1-run"))
    args = parser.parse_args()
    root = Path(args.registry_root)
    out_dir = Path(args.output_dir)
    stages = []
    first_gate = None
    stop_reason = "completed"
    checks = [
        ("K1.3A_MASTER_REGISTRY", validate_master),
        ("K1.3B_IDENTITY_PREP", validate_identity),
        ("K1.4_DOCUMENT_IMPORT", validate_document_import),
        ("K1.5A_LEGAL_REGISTRY", validate_legal_registry),
        ("K1.5C_SEMANTIC_METADATA", validate_semantic_candidate),
        ("K1.5D_OFFICIAL_VERIFICATION_GATE", official_gate),
    ]
    started = utc_now()
    for name, fn in checks:
        result = timed(name, lambda fn=fn: fn(root))
        stages.append(result)
        if result.status == "BLOCKED":
            stop_reason = f"blocked_at:{name}"
            break
        if result.status == "HUMAN_GATE":
            first_gate = name
            stop_reason = f"human_gate:{name}"
            break
    run = {
        "schema": "alina-k1-run.v0.1",
        "run_id": datetime.now().strftime("K1-%Y%m%d-%H%M%S"),
        "started_at": started,
        "finished_at": utc_now(),
        "registry_root": str(root),
        "first_human_gate": first_gate,
        "stop_reason": stop_reason,
        "stages": [asdict(s) for s in stages],
        "metrics": compute_metrics(stages),
        "approaches": APPROACHES,
        "expectation_vs_fact": {key: {**value, "actual": "MEASURE_FROM_RUN_HISTORY"} for key, value in APPROACHES.items()},
    }
    write_outputs(out_dir, run)
    print(json.dumps(run, ensure_ascii=False, indent=2))
    return 2 if any(s.status == "BLOCKED" for s in stages) else 0

if __name__ == "__main__":
    raise SystemExit(main())
