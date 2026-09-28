"""ALINA/FATHER K1 autonomous project runner.

Builds approved derived registry layers from existing local audits, validates
each layer, records metrics, and stops at the first genuine human gate.
Original source documents are never modified, moved, deleted, or renamed.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import time
from typing import Any, Callable

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

SCHEMA = "alina-k1-autoproject.v0.2"
LEGAL_KINDS = {
    "FEDERAL_LAW", "FEDERAL_CONSTITUTIONAL_LAW", "PRESIDENT_DECREE",
    "GOVERNMENT_RESOLUTION", "ORDER", "DIRECTIVE", "REGULATION",
    "SANITARY_RULE",
}
APPROACHES = {
    "reuse_existing_audit": {
        "expectation": "Reuse trustworthy inventories instead of rescanning originals.",
        "better_when": "Inventory already has SHA-256, paths and provenance.",
        "worse_when": "Inventory is stale, incomplete or has no strong content identity.",
    },
    "content_addressed_dedup": {
        "expectation": "Use SHA-256 to merge byte-identical copies without deleting originals.",
        "better_when": "One digital file exists at several locations.",
        "worse_when": "Different editions/translations belong to one work but have different bytes.",
    },
    "candidate_first_identity": {
        "expectation": "Keep raw evidence and write inferred metadata only as candidates.",
        "better_when": "Filenames and PDF metadata are noisy.",
        "worse_when": "Metadata is already curated and independently verified.",
    },
    "official_verification_gate": {
        "expectation": "Do not promote legal status/current revision from local PDF evidence alone.",
        "better_when": "Current legal validity matters.",
        "worse_when": "Authoritative verification is unavailable; affected branch must stop.",
    },
}

@dataclass
class StageResult:
    stage: str
    status: str
    read_records: int = 0
    written_records: int = 0
    created: int = 0
    updated: int = 0
    skipped: int = 0
    warnings: int = 0
    errors: int = 0
    duration_seconds: float = 0.0
    detail: str = ""
    gate_reason: str | None = None

class PipelineError(RuntimeError):
    pass

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def json_load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def jsonl_load(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise PipelineError(f"Invalid JSONL {path} line {n}: {exc}") from exc
    return rows

def atomic_text(path: Path, text: str, backup_dir: Path | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and backup_dir is not None:
        backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        shutil.copy2(path, backup_dir / f"{path.name}.{stamp}.bak")
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)

def jsonl_write(path: Path, rows: list[dict[str, Any]], backup_dir: Path | None = None) -> None:
    body = "".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) + "\n" for x in rows)
    atomic_text(path, body, backup_dir)

def stable_source_id(sha256: str) -> str:
    return "SRC-" + sha256[:16].upper()

def source_id_collision_check(rows: list[dict[str, Any]]) -> None:
    seen: dict[str, str] = {}
    for row in rows:
        sid, sha = str(row.get("source_id") or ""), str(row.get("sha256") or "").lower()
        if not sid or not sha:
            continue
        prior = seen.get(sid)
        if prior and prior != sha:
            raise PipelineError(f"source_id collision: {sid} maps to multiple SHA-256 values")
        seen[sid] = sha

def assign_copy_ids(copies: list[dict[str, Any]]) -> None:
    used = {str(x.get("copy_id")) for x in copies if x.get("copy_id")}
    next_id = 1
    for copy in sorted(copies, key=lambda x: (str(x.get("source_id")), str(x.get("path")))):
        if copy.get("copy_id"):
            continue
        while f"COPY-{next_id:06d}" in used:
            next_id += 1
        copy["copy_id"] = f"COPY-{next_id:06d}"
        used.add(copy["copy_id"])
        next_id += 1

def next_legal_id(rows: list[dict[str, Any]]) -> str:
    used = {str(x.get("legal_document_id")) for x in rows if x.get("legal_document_id")}
    n = 1
    while f"LDOC-{n:06d}" in used:
        n += 1
    return f"LDOC-{n:06d}"

def first_existing(candidates: list[Path]) -> Path | None:
    for p in candidates:
        if p.exists():
            return p
    return None

def discover_inputs(home: Path) -> dict[str, Path | None]:
    library = first_existing([
        Path(r"G:\1\OTUS\knowledge\library_inventory\generated\library_inventory.json"),
        home / "OTUS" / "knowledge" / "library_inventory" / "generated" / "library_inventory.json",
    ])
    docs = first_existing([
        Path.home() / "Documents" / "ChatGPT" / "Vibe-coding" / "ib-discovery" / "habr-432466" / "pdf-document-catalog.json",
        home / "ib-discovery" / "habr-432466" / "pdf-document-catalog.json",
    ])
    return {"library_inventory": library, "document_catalog": docs}

def repair_mojibake(text: str | None) -> tuple[str | None, bool]:
    if not text:
        return text, False
    if not any(token in text for token in ("Р", "С", "вЂ")):
        return text, False
    try:
        fixed = text.encode("cp1251").decode("utf-8")
        if fixed != text and "�" not in fixed:
            return fixed, True
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return text, False

def clean_title(text: str | None) -> str | None:
    if not text:
        return text
    x = text.strip()
    x = re.sub(r"(?i)^OceanofPDF\.com[\s_-]*", "", x)
    x = re.sub(r"(?i)^AW[._\-\s]+", "", x)
    x = re.sub(r"(?i)[._\-\s]*www\.EBooksWorld\.ir$", "", x)
    x = x.replace("_", " ")
    x = re.sub(r"\s+", " ", x)
    return x.strip()

def detect_kind(text: str) -> str:
    x = text.lower()
    checks = [
        (r"федеральн\w*\s+конституционн\w*\s+закон", "FEDERAL_CONSTITUTIONAL_LAW"),
        (r"федеральн\w*\s+закон|\b\d+\s*[-–]?\s*фз\b", "FEDERAL_LAW"),
        (r"указ\s+президент", "PRESIDENT_DECREE"),
        (r"постановлен\w*\s+правительств", "GOVERNMENT_RESOLUTION"),
        (r"\bприказ\b", "ORDER"),
        (r"\bраспоряжени", "DIRECTIVE"),
        (r"\bгост\b|\biso[/\s\-]?\d", "STANDARD"),
        (r"санпин", "SANITARY_RULE"),
        (r"\bположение\b|\bрегламент\b", "REGULATION"),
        (r"\bisbn\b", "BOOK"),
    ]
    for pattern, kind in checks:
        if re.search(pattern, x, re.I):
            return kind
    return "UNKNOWN_DOCUMENT"

def source_type(kind: str) -> str:
    if kind in LEGAL_KINDS:
        return "LEGAL_DOCUMENT"
    if kind == "STANDARD":
        return "STANDARD"
    if kind == "BOOK":
        return "BOOK"
    return "DOCUMENT"

def build_master(registry: Path, library_path: Path, backup: Path) -> StageResult:
    raw = json_load(library_path)
    if isinstance(raw, dict):
        items = raw.get("items", [])
        source_root = raw.get("source_root")
    elif isinstance(raw, list):
        items = raw
        source_root = None
    else:
        items = []
        source_root = None
    if not isinstance(items, list) or not items:
        return StageResult("K1.3A_MASTER_REGISTRY", "BLOCKED", errors=1, detail="Library inventory has no items")
    existing_sources = jsonl_load(registry / "sources.jsonl")
    existing_copies = jsonl_load(registry / "physical_copies.jsonl")
    by_sha = {str(x.get("sha256")).lower(): x for x in existing_sources if x.get("sha256")}
    by_path = {str(x.get("path")).lower(): x for x in existing_copies if x.get("path")}
    created = updated = skipped = 0
    for item in items:
        sha = str(item.get("sha256") or "").lower()
        rel = str(item.get("relative_path") or "")
        full = str(item.get("path") or "")
        if not full and source_root and rel:
            full = str(Path(source_root) / rel)
        if not sha:
            skipped += 1
            continue
        sid = stable_source_id(sha)
        src = by_sha.get(sha)
        if src is None:
            src = {
                "source_id": sid, "sha256": sha, "content_digest": f"sha256:{sha}",
                "raw_title": item.get("normalized_title") or item.get("file_name"),
                "canonical_title": None, "format": item.get("format") or item.get("extension"),
                "size_bytes": item.get("size_bytes"), "page_count": item.get("page_count"),
                "physical_copies": 0, "work_id": None, "edition_id": None,
                "identification_status": "UNRESOLVED", "source_status": "DISCOVERED",
                "provenance": [{"imported_from": str(library_path), "imported_at": now_iso()}],
            }
            existing_sources.append(src); by_sha[sha] = src; created += 1
        else:
            if not src.get("content_digest"):
                src["content_digest"] = f"sha256:{sha}"; updated += 1
            else:
                skipped += 1
        if full and full.lower() not in by_path:
            copy = {
                "copy_id": None, "source_id": src["source_id"], "path": full,
                "file_name": item.get("file_name") or Path(full).name,
                "legacy_item_id": item.get("item_id"), "state": "OBSERVED",
                "storage_type": "LOCAL_DISK", "provenance": str(library_path),
            }
            existing_copies.append(copy); by_path[full.lower()] = copy
    existing_copies.sort(key=lambda x: (str(x.get("source_id")), str(x.get("path"))))
    assign_copy_ids(existing_copies)
    counts: dict[str, int] = {}
    for copy in existing_copies:
        counts[copy["source_id"]] = counts.get(copy["source_id"], 0) + 1
    for src in existing_sources:
        src["physical_copies"] = counts.get(src["source_id"], 0)
    source_id_collision_check(existing_sources)
    jsonl_write(registry / "sources.jsonl", existing_sources, backup)
    jsonl_write(registry / "physical_copies.jsonl", existing_copies, backup)
    return StageResult("K1.3A_MASTER_REGISTRY", "PASS", len(items), len(existing_sources),
                       created=created, updated=updated, skipped=skipped,
                       detail=f"sources={len(existing_sources)}; copies={len(existing_copies)}")

def build_identity(registry: Path, backup: Path) -> StageResult:
    sources = jsonl_load(registry / "sources.jsonl")
    rows = []
    changed = mojibake = 0
    for src in sources:
        raw = src.get("raw_title")
        repaired, did_repair = repair_mojibake(raw)
        candidate = clean_title(repaired)
        did_change = candidate != raw
        changed += int(did_change); mojibake += int(did_repair)
        rows.append({
            "source_id": src.get("source_id"), "sha256": src.get("sha256"),
            "raw_title": raw, "repaired_title": repaired, "title_candidate": candidate,
            "mojibake_detected": did_repair, "normalization_changed": did_change,
            "author_candidates": [], "isbn_candidates": [], "work_candidate": None,
            "edition_candidate": None, "identity_confidence": 0.0,
            "identity_status": "NEEDS_IDENTIFICATION" if did_change else "UNRESOLVED",
            "identity_evidence": [{"type": "LEGACY_TITLE", "value": raw}] if raw else [],
        })
    jsonl_write(registry / "identity_candidates.jsonl", rows, backup)
    return StageResult("K1.3B_IDENTITY_PREP", "PASS", len(sources), len(rows),
                       updated=changed, detail=f"normalized={changed}; encoding_repairs={mojibake}")

def import_document_catalog(registry: Path, catalog_path: Path | None, backup: Path) -> StageResult:
    if catalog_path is None:
        return StageResult("K1.4_DOCUMENT_IMPORT", "WARN", warnings=1, detail="Document catalog not discovered")
    docs = json_load(catalog_path)
    if not isinstance(docs, list):
        return StageResult("K1.4_DOCUMENT_IMPORT", "BLOCKED", errors=1, detail="Document catalog root is not a list")
    sources = jsonl_load(registry / "sources.jsonl")
    copies = jsonl_load(registry / "physical_copies.jsonl")
    by_sha = {str(x.get("sha256")).lower(): x for x in sources if x.get("sha256")}
    by_path = {str(x.get("path")).lower(): x for x in copies if x.get("path")}
    created = linked = copy_created = review = 0
    provenance = []
    review_rows = []
    for doc in docs:
        sha = str(doc.get("sha256") or "").lower()
        path = str(doc.get("path") or doc.get("FullName") or "")
        title = doc.get("title_candidate") or doc.get("Name") or (Path(path).name if path else None)
        kind = detect_kind(f"{title or ''} {path}")
        stype = source_type(kind)
        if not sha:
            review += 1
            review_rows.append({"reason":"NO_SHA256","raw_path":path,"title_candidate":title,
                                "review_required":True,"queued_at":now_iso()})
            continue
        src = by_sha.get(sha)
        if src is None:
            src = {
                "source_id": stable_source_id(sha), "sha256": sha, "content_digest": f"sha256:{sha}",
                "raw_title": title, "canonical_title": None, "format": "PDF",
                "size_bytes": doc.get("size") or doc.get("Length"),
                "page_count": doc.get("page_count"), "physical_copies": 0,
                "work_id": None, "edition_id": None,
                "source_type_candidate": stype, "document_kind_candidate": kind,
                "classification_status": "CANDIDATE", "identification_status": "UNRESOLVED",
                "source_status": "DISCOVERED", "legal_status": "UNKNOWN",
                "provenance": [{"imported_from": str(catalog_path), "imported_at": now_iso()}],
            }
            sources.append(src); by_sha[sha] = src; created += 1
        else:
            linked += 1
            src.setdefault("source_type_candidate", stype)
            src.setdefault("document_kind_candidate", kind)
        if path and path.lower() not in by_path:
            copy = {"copy_id":None,"source_id":src["source_id"],"path":path,
                    "file_name":Path(path).name,"legacy_item_id":None,"state":"OBSERVED",
                    "storage_type":"LOCAL_DISK","provenance":str(catalog_path)}
            copies.append(copy); by_path[path.lower()] = copy; copy_created += 1
        provenance.append({
            "source_id": src["source_id"], "source_registry": str(catalog_path),
            "source_path": path, "title_candidate": title,
            "document_kind_candidate": kind, "source_type_candidate": stype,
            "date_number_candidates": doc.get("date_number_candidates"),
            "revision_mentions": doc.get("revision_mentions"),
            "revision_history_excerpt": doc.get("revision_history_excerpt"),
            "review_required": bool(doc.get("review_required")),
            "current_revision_verified": bool(doc.get("current_revision_verified")),
            "linked_at": now_iso(),
        })
    copies.sort(key=lambda x: (str(x.get("source_id")), str(x.get("path"))))
    assign_copy_ids(copies)
    counts: dict[str,int] = {}
    for copy in copies:
        counts[copy["source_id"]] = counts.get(copy["source_id"],0)+1
    for src in sources:
        src["physical_copies"] = counts.get(src["source_id"],0)
    source_id_collision_check(sources)
    jsonl_write(registry / "sources.jsonl", sources, backup)
    jsonl_write(registry / "physical_copies.jsonl", copies, backup)
    jsonl_write(registry / "source_provenance.jsonl", provenance, backup)
    jsonl_write(registry / "document_review_queue.jsonl", review_rows, backup)
    return StageResult("K1.4_DOCUMENT_IMPORT", "PASS", len(docs), len(sources),
                       created=created+copy_created, updated=linked, skipped=review,
                       warnings=review,
                       detail=f"new_sources={created}; linked={linked}; new_copies={copy_created}; review={review}")

def build_legal_registry(registry: Path, backup: Path) -> StageResult:
    sources = jsonl_load(registry / "sources.jsonl")
    old = jsonl_load(registry / "legal_documents.jsonl")
    by_source = {x.get("source_id"):x for x in old}
    rows = []
    created = updated = 0
    candidates = [s for s in sources if s.get("source_type_candidate") in {"LEGAL_DOCUMENT","REGULATORY_DOCUMENT"} or s.get("document_kind_candidate") in LEGAL_KINDS]
    for src in sorted(candidates, key=lambda x: str(x.get("source_id"))):
        row = by_source.get(src.get("source_id"))
        if row is None:
            row = {
                "legal_document_id": next_legal_id(old + rows), "source_id": src.get("source_id"),
                "identity": {"canonical_name":None,"short_name":None,"original_name":src.get("raw_title"),
                             "aliases":[],"document_kind":src.get("document_kind_candidate"),
                             "document_number":None,"issuer":None,"jurisdiction":None,"language":None},
                "lifecycle": {"adoption_date":None,"publication_date":None,"effective_date":None,
                              "expiry_date":None,"legal_status":"UNKNOWN","current_revision_date":None},
                "officiality": {"official_source":None,"official_url":None,
                                "publication_reference":None,"verification_status":"UNVERIFIED"},
                "applicability": {"sectors":[],"organization_types":[],"system_types":[],"subjects":[],
                                  "territories":[],"conditions":[],"exclusions":[]},
                "processing": {"identity_resolved":False,"official_source_verified":False,
                               "legal_status_verified":False,"revision_history_built":False,
                               "structure_parsed":False,"requirements_extracted":False,
                               "definitions_extracted":False,"applicability_extracted":False,
                               "relations_built":False},
                "confidence":{"identity":0.0,"legal_status":0.0,"revision":0.0,"applicability":0.0},
                "evidence":[],"created_at":now_iso(),
            }
            created += 1
        else:
            row["identity"]["original_name"] = row["identity"].get("original_name") or src.get("raw_title")
            row["identity"]["document_kind"] = row["identity"].get("document_kind") or src.get("document_kind_candidate")
            updated += 1
        rows.append(row)
    jsonl_write(registry / "legal_documents.jsonl", rows, backup)
    for name in ("legal_revisions.jsonl","legal_structure.jsonl","legal_relations.jsonl",
                 "legal_requirements.jsonl","legal_definitions.jsonl"):
        p = registry / name
        if not p.exists():
            jsonl_write(p, [], backup)
    return StageResult("K1.5A_LEGAL_REGISTRY", "PASS" if rows else "WARN",
                       len(candidates), len(rows), created=created, updated=updated,
                       warnings=0 if rows else 1, detail=f"legal_documents={len(rows)}")

def extract_pdf_front(path: Path, pages: int = 20) -> tuple[str, int]:
    if PdfReader is None:
        raise PipelineError("pypdf is not installed")
    reader = PdfReader(str(path))
    chunks = []
    read = 0
    for page in reader.pages[:pages]:
        chunks.append(page.extract_text() or "")
        read += 1
    return "\n".join(chunks), read

MONTHS = {"января":1,"февраля":2,"марта":3,"апреля":4,"мая":5,"июня":6,
          "июля":7,"августа":8,"сентября":9,"октября":10,"ноября":11,"декабря":12}

def normalize_ru_date(raw: str) -> str | None:
    raw = raw.strip()
    for fmt in ("%d.%m.%Y","%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            pass
    m = re.match(r"(\d{1,2})\s+([а-яё]+)\s+(\d{4})", raw, re.I)
    if m and m.group(2).lower() in MONTHS:
        try:
            return datetime(int(m.group(3)),MONTHS[m.group(2).lower()],int(m.group(1))).date().isoformat()
        except ValueError:
            return None
    return None

def semantic_from_text(text: str, legal: dict[str,Any], source: dict[str,Any], path: str, pages_read: int) -> dict[str,Any]:
    kind = detect_kind(text)
    nums = []
    for pat in (r"(?i)№\s*([0-9]+(?:-[А-ЯA-Zа-яa-z0-9]+)?)", r"(?i)\b([0-9]+-ФЗ)\b", r"(?i)\b([0-9]+-ФКЗ)\b"):
        nums.extend(m.group(1).strip() for m in re.finditer(pat,text))
    nums = list(dict.fromkeys(nums))
    dates = []
    pat = r"(?i)от\s+(\d{1,2}\s+(?:января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s+\d{4}|\d{2}\.\d{2}\.\d{4})\s*(?:г\.|года)?\s*№"
    for m in re.finditer(pat,text):
        norm = normalize_ru_date(m.group(1))
        if norm:
            dates.append({"raw":m.group(1),"normalized":norm})
    dates = list({x["normalized"]:x for x in dates}.values())
    status_signals = []
    if re.search(r"(?i)утратил[ао]?\s+силу|признать\s+утратившим\s+силу",text):
        status_signals.append({"status":"REPEALED_CANDIDATE","signal":"loss-of-force wording found"})
    if re.search(r"(?i)вступает\s+в\s+силу",text):
        status_signals.append({"status":"EFFECTIVE_CANDIDATE","signal":"entry-into-force wording found"})
    lines=[x.strip() for x in text.splitlines() if len(x.strip())>5][:100]
    name_candidate = next((x for x in lines if re.search(r"(?i)федеральн\w*\s+закон|постановлен|\bприказ\b|\bуказ\b",x)), source.get("raw_title"))
    confidence = min(0.95, 0.10 + 0.20*(kind!="UNKNOWN_DOCUMENT") + 0.20*bool(nums) + 0.20*bool(dates) + 0.15*bool(name_candidate))
    return {
        "schema":"father-legal-semantic-metadata.v0.2",
        "legal_document_id":legal.get("legal_document_id"),"source_id":source.get("source_id"),
        "identity":{"canonical_name_candidate":name_candidate,"document_kind_candidate":kind,
                    "document_number_candidates":nums,"issuer_candidates":[],
                    "jurisdiction_candidate":"RU","language_candidate":"RU"},
        "lifecycle":{"adoption_date_candidates":dates,"publication_date_candidates":[],
                     "effective_date_candidates":[],"revision_date_candidates":[],
                     "expiry_date_candidates":[],"legal_status_signals":status_signals,
                     "legal_status":"UNVERIFIED"},
        "revisions":{"amendment_document_candidates":[],"current_revision_verified":False,
                     "revision_history_verified":False},
        "officiality":{"official_source":None,"official_url":None,"official_source_verified":False},
        "source_evidence":{"sha256":source.get("sha256"),"physical_path":path,"pages_read":pages_read,
                           "extraction_method":"pypdf","extracted_at":now_iso()},
        "confidence":round(confidence,2),"verification_state":"REQUIRES_OFFICIAL_VERIFICATION",
        "next_action":"VERIFY_OFFICIAL_SOURCE_AND_CURRENT_REVISION","generated_at":now_iso(),
    }

def build_semantic_pilot(registry: Path, backup: Path) -> StageResult:
    legal = jsonl_load(registry / "legal_documents.jsonl")
    sources = {x.get("source_id"):x for x in jsonl_load(registry / "sources.jsonl")}
    copies = jsonl_load(registry / "physical_copies.jsonl")
    copy_map: dict[str,list[dict[str,Any]]] = {}
    for c in copies:
        copy_map.setdefault(c.get("source_id"),[]).append(c)
    scored = []
    priority={"FEDERAL_LAW":100,"GOVERNMENT_RESOLUTION":90,"ORDER":80,"PRESIDENT_DECREE":70,"REGULATION":50}
    for doc in legal:
        src=sources.get(doc.get("source_id"))
        if not src: continue
        usable=[c for c in copy_map.get(src.get("source_id"),[]) if c.get("path") and Path(c["path"]).is_file() and Path(c["path"]).suffix.lower()==".pdf"]
        if not usable: continue
        scored.append((priority.get(src.get("document_kind_candidate"),10),doc,src,usable[0]))
    if not scored:
        return StageResult("K1.5C_SEMANTIC_METADATA","HUMAN_GATE",warnings=1,
                           detail="No accessible local PDF for any legal candidate",
                           gate_reason="Provide or map at least one accessible legal-document PDF")
    _,doc,src,copy=max(scored,key=lambda x:x[0])
    try:
        text,pages=extract_pdf_front(Path(copy["path"]),20)
    except Exception as exc:
        return StageResult("K1.5C_SEMANTIC_METADATA","HUMAN_GATE",warnings=1,
                           detail=f"PDF extraction failed: {exc}",
                           gate_reason="PDF requires OCR or extractor repair")
    if len(text.strip()) < 100:
        return StageResult("K1.5C_SEMANTIC_METADATA","HUMAN_GATE",warnings=1,
                           detail=f"Too little extracted text ({len(text.strip())} chars)",
                           gate_reason="Likely scan/OCR required")
    candidate=semantic_from_text(text,doc,src,copy["path"],pages)
    atomic_text(registry/"legal_document_semantic_candidate.json",
                json.dumps(candidate,ensure_ascii=False,indent=2),backup)
    atomic_text(registry/"legal_document_pilot_evidence.txt",text,backup)
    return StageResult("K1.5C_SEMANTIC_METADATA","PASS",1,1,created=1,
                       warnings=int(candidate["confidence"]<0.70),
                       detail=f"pilot={doc.get('legal_document_id')}; pages={pages}; confidence={candidate['confidence']}")

def build_official_queue(registry: Path, backup: Path) -> StageResult:
    p=registry/"legal_document_semantic_candidate.json"
    if not p.exists():
        return StageResult("K1.5D_OFFICIAL_VERIFICATION","BLOCKED",errors=1,detail="semantic candidate missing")
    c=json_load(p)
    official=c.get("officiality") or {}
    lifecycle=c.get("lifecycle") or {}
    if official.get("official_source_verified") and lifecycle.get("legal_status") not in {None,"","UNKNOWN","UNVERIFIED"}:
        return StageResult("K1.5D_OFFICIAL_VERIFICATION","PASS",1,1,detail="official verification already present")
    identity=c.get("identity") or {}
    dates=lifecycle.get("adoption_date_candidates") or []
    task={
        "schema":"father-legal-official-verification-task.v0.2",
        "verification_task_id":"LVERIFY-"+hashlib.sha256(str(c.get("source_id")).encode()).hexdigest()[:12].upper(),
        "legal_document_id":c.get("legal_document_id"),"source_id":c.get("source_id"),
        "candidate_identity":{
            "canonical_name":identity.get("canonical_name_candidate"),
            "document_kind":identity.get("document_kind_candidate"),
            "document_number":(identity.get("document_number_candidates") or [None])[0],
            "adoption_date":(dates or [{}])[0].get("normalized") if dates else None,
            "jurisdiction":identity.get("jurisdiction_candidate"),
        },
        "verification_required":{"source_authenticity":True,"identity":True,"official_publication":True,
                                 "current_revision":True,"legal_status":True,"amendment_history":True},
        "verification_state":{"source_verified":False,"identity_verified":False,
                              "official_source_verified":False,"current_revision_verified":False,
                              "legal_status_verified":False,"amendment_history_verified":False},
        "official_evidence":[],"conflicts":[],"status":"PENDING_OFFICIAL_VERIFICATION",
        "created_at":now_iso(),
    }
    queue_path = registry/"legal_official_verification_queue.jsonl"
    queue = jsonl_load(queue_path)
    existing = {x.get("verification_task_id"): x for x in queue}
    created = 0
    if task["verification_task_id"] in existing:
        prior = existing[task["verification_task_id"]]
        task["created_at"] = prior.get("created_at") or task["created_at"]
        task["official_evidence"] = prior.get("official_evidence") or []
        task["conflicts"] = prior.get("conflicts") or []
        task["verification_state"] = prior.get("verification_state") or task["verification_state"]
        queue = [task if x.get("verification_task_id") == task["verification_task_id"] else x for x in queue]
    else:
        queue.append(task)
        created = 1
    jsonl_write(queue_path,queue,backup)
    return StageResult("K1.5D_OFFICIAL_VERIFICATION","HUMAN_GATE",1,len(queue),created=created,updated=1-created,warnings=1,
                       detail="Official-source/current-revision/legal-status verification required",
                       gate_reason="Review authoritative source evidence before legal status is promoted")

def validate_invariants(registry: Path) -> StageResult:
    sources=jsonl_load(registry/"sources.jsonl")
    copies=jsonl_load(registry/"physical_copies.jsonl")
    source_id_collision_check(sources)
    ids={x.get("source_id") for x in sources}
    orphan=[x for x in copies if x.get("source_id") not in ids]
    duplicate_paths=len(copies)-len({str(x.get("path")).lower() for x in copies if x.get("path")})
    bad_digest=sum(1 for x in sources if x.get("sha256") and x.get("content_digest") not in {None,f"sha256:{x.get('sha256')}"})
    errors=len(orphan)+duplicate_paths+bad_digest
    return StageResult("K1.INVARIANTS","PASS" if errors==0 else "BLOCKED",
                       len(sources)+len(copies),0,errors=errors,
                       detail=f"orphan_copies={len(orphan)}; duplicate_paths={duplicate_paths}; bad_digest={bad_digest}")

def stage_call(name: str, fn: Callable[[],StageResult]) -> StageResult:
    start=time.monotonic()
    try:
        result=fn()
    except Exception as exc:
        result=StageResult(name,"BLOCKED",errors=1,detail=f"{type(exc).__name__}: {exc}")
    result.stage=name
    result.duration_seconds=round(time.monotonic()-start,6)
    return result

def history_metrics(history_path: Path, current: list[StageResult]) -> dict[str,Any]:
    history=[]
    if history_path.exists():
        for line in history_path.read_text(encoding="utf-8-sig").splitlines():
            try: history.append(json.loads(line))
            except Exception: pass
    duration=sum(s.duration_seconds for s in current)
    writes=sum(s.written_records for s in current)
    attempts=sum(s.read_records for s in current)
    auto=sum(1 for s in current if s.status in {"PASS","WARN","SKIP"})
    review=sum(s.warnings for s in current)
    metrics={
        "attempted_stages":len(current),"auto_completed_stages":auto,
        "automation_yield_pct":round(100*auto/len(current),2) if current else 0.0,
        "records_read":attempts,"records_written":writes,
        "created":sum(s.created for s in current),"updated":sum(s.updated for s in current),
        "skipped":sum(s.skipped for s in current),"warnings":review,
        "errors":sum(s.errors for s in current),"wall_seconds":round(duration,6),
        "throughput_records_per_second":round(attempts/duration,3) if duration else None,
        "review_pressure_pct":round(100*review/max(attempts,1),3),
        "rework_ratio":"NO_DATA","speedup_vs_single_stream":"NO_DATA","eta":"NO_DATA",
        "comparable_prior_runs":len(history),
    }
    if history:
        prev=history[-1].get("metrics",{})
        if prev.get("wall_seconds") and attempts==prev.get("records_read"):
            metrics["relative_speed_vs_previous_run"]=round(prev["wall_seconds"]/max(duration,1e-9),3)
    # Rework is intentionally not inferred from ordinary idempotent updates.
    # It becomes measurable only after explicit corrective-work events are recorded.
    return metrics

def expectation_vs_fact(stages: list[StageResult]) -> dict[str, Any]:
    by_stage = {s.stage: s for s in stages}
    def fact(stage: str) -> str:
        s = by_stage.get(stage)
        if not s:
            return "NO_DATA"
        return f"{s.status}: {s.detail}"
    return {
        "reuse_existing_audit": {**APPROACHES["reuse_existing_audit"], "actual": fact("K1.3A_MASTER_REGISTRY")},
        "content_addressed_dedup": {**APPROACHES["content_addressed_dedup"], "actual": fact("K1.INVARIANTS")},
        "candidate_first_identity": {**APPROACHES["candidate_first_identity"], "actual": fact("K1.3B_IDENTITY_PREP")},
        "official_verification_gate": {**APPROACHES["official_verification_gate"], "actual": fact("K1.5D_OFFICIAL_VERIFICATION")},
    }

def append_journal(path: Path, run: dict[str,Any]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    lines=[f"\n## Run {run['run_id']}",f"- Started: {run['started_at']}",
           f"- Finished: {run['finished_at']}",f"- Stop: {run['stop_reason']}",
           f"- First human gate: {run.get('first_human_gate') or 'none'}","",
           "### Stages"]
    for s in run["stages"]:
        lines.append(f"- {s['stage']}: {s['status']} | read={s['read_records']} write={s['written_records']} "
                     f"create={s['created']} update={s['updated']} warn={s['warnings']} err={s['errors']} | {s['detail']}")
    lines += ["","### Metrics",json.dumps(run["metrics"],ensure_ascii=False,indent=2),""]
    with path.open("a",encoding="utf-8") as f: f.write("\n".join(lines))

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--registry-root",default=r"G:\1\FATHER\data\source_registry")
    ap.add_argument("--home-root",default=r"G:\1")
    ap.add_argument("--library-inventory")
    ap.add_argument("--document-catalog")
    ap.add_argument("--output-dir",default=str(Path(__file__).resolve().parent/"data"/"k1-run"))
    args=ap.parse_args()
    registry=Path(args.registry_root); registry.mkdir(parents=True,exist_ok=True)
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    backup=registry/"backup"/"k1-auto"
    discovered=discover_inputs(Path(args.home_root))
    library=Path(args.library_inventory) if args.library_inventory else discovered["library_inventory"]
    catalog=Path(args.document_catalog) if args.document_catalog else discovered["document_catalog"]
    stages=[]
    started=now_iso()
    first_gate=None
    stop_reason="completed"
    if library is None:
        stages.append(StageResult("K1.0_DISCOVERY","HUMAN_GATE",warnings=1,
                                  detail="Library inventory not discovered",
                                  gate_reason="Provide --library-inventory path"))
        first_gate="K1.0_DISCOVERY"; stop_reason="human_gate:K1.0_DISCOVERY"
    else:
        stages.append(StageResult("K1.0_DISCOVERY","PASS",read_records=2,
                                  detail=f"library={library}; document_catalog={catalog or 'NOT_FOUND'}"))
        plan=[
            ("K1.3A_MASTER_REGISTRY",lambda:build_master(registry,library,backup)),
            ("K1.3B_IDENTITY_PREP",lambda:build_identity(registry,backup)),
            ("K1.4_DOCUMENT_IMPORT",lambda:import_document_catalog(registry,catalog,backup)),
            ("K1.INVARIANTS",lambda:validate_invariants(registry)),
            ("K1.5A_LEGAL_REGISTRY",lambda:build_legal_registry(registry,backup)),
            ("K1.5C_SEMANTIC_METADATA",lambda:build_semantic_pilot(registry,backup)),
            ("K1.5D_OFFICIAL_VERIFICATION",lambda:build_official_queue(registry,backup)),
        ]
        for name,fn in plan:
            result=stage_call(name,fn); stages.append(result)
            if result.status in {"BLOCKED","HUMAN_GATE"}:
                stop_reason=f"{result.status.lower()}:{name}"
                if result.status=="HUMAN_GATE": first_gate=name
                break
    history_path=out/"history.jsonl"
    metrics=history_metrics(history_path,stages)
    run={
        "schema":SCHEMA,"run_id":datetime.now().strftime("K1-%Y%m%d-%H%M%S-%f"),
        "started_at":started,"finished_at":now_iso(),
        "registry_root":str(registry),"inputs":{"library_inventory":str(library) if library else None,
        "document_catalog":str(catalog) if catalog else None},
        "stop_reason":stop_reason,"first_human_gate":first_gate,
        "stages":[asdict(s) for s in stages],"metrics":metrics,
        "approaches":APPROACHES,
        "expectation_vs_fact":expectation_vs_fact(stages),
        "safety":{"originals_mutated":False,"originals_moved":False,"originals_deleted":False,
                  "derived_writes_atomic":True,"derived_backups_enabled":True},
    }
    atomic_text(out/"latest.json",json.dumps(run,ensure_ascii=False,indent=2))
    with history_path.open("a",encoding="utf-8") as f:
        f.write(json.dumps(run,ensure_ascii=False)+"\n")
    append_journal(out/"DEV_JOURNAL_K1.md",run)
    print(json.dumps(run,ensure_ascii=False,indent=2))
    return 2 if any(s.status=="BLOCKED" for s in stages) else 0

if __name__=="__main__":
    raise SystemExit(main())
