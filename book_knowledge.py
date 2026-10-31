"""Semantic book knowledge package storage and validation.

This module does not call an LLM. It validates and stores semantic artifacts
produced by an authorized semantic worker, preserving provenance and keeping
source-derived content separate from ALINA inference.
"""
from __future__ import annotations

import json
from pathlib import Path
import time

SCHEMA = "father.book_knowledge_package.v1"
REQUIRED = {
    "source", "scope", "original_index", "translation", "semantic_outline",
    "glossary", "applications", "examples", "algorithms", "conclusions",
    "combinations", "checklists", "knowledge_atoms", "father_mapping", "quality",
}


class BookKnowledgeError(ValueError):
    pass


def init(db):
    db.executescript("""
    CREATE TABLE IF NOT EXISTS book_packages(
      package_id TEXT PRIMARY KEY,
      source_id TEXT NOT NULL,
      scope TEXT NOT NULL,
      schema_name TEXT NOT NULL,
      status TEXT NOT NULL,
      path TEXT,
      payload TEXT NOT NULL,
      created REAL NOT NULL,
      updated REAL NOT NULL
    );
    CREATE TABLE IF NOT EXISTS book_package_events(
      id INTEGER PRIMARY KEY,
      at REAL NOT NULL,
      package_id TEXT NOT NULL,
      kind TEXT NOT NULL,
      detail TEXT
    );
    """)


def _need(condition, message, errors):
    if not condition:
        errors.append(message)


def validate_package(payload: dict) -> list[str]:
    errors = []
    _need(isinstance(payload, dict), "package must be an object", errors)
    if errors:
        return errors

    _need(payload.get("schema") == SCHEMA, f"schema must be {SCHEMA}", errors)
    missing = sorted(REQUIRED - set(payload))
    if missing:
        errors.append("missing sections: " + ", ".join(missing))

    source = payload.get("source")
    scope = payload.get("scope")
    _need(isinstance(source, str) and source.startswith("SRC-"), "source must be SRC-*", errors)
    _need(isinstance(scope, str) and bool(scope.strip()), "scope is required", errors)

    translation = payload.get("translation", [])
    _need(isinstance(translation, list) and bool(translation), "translation must contain traceable units", errors)
    if isinstance(translation, list):
        for i, item in enumerate(translation):
            _need(isinstance(item, dict), f"translation[{i}] must be an object", errors)
            if isinstance(item, dict):
                _need(bool(item.get("locator")), f"translation[{i}] missing locator", errors)
                _need(bool(item.get("ru_summary")), f"translation[{i}] missing ru_summary", errors)

    glossary = payload.get("glossary", [])
    _need(isinstance(glossary, list), "glossary must be a list", errors)
    if isinstance(glossary, list):
        for i, term in enumerate(glossary):
            if not isinstance(term, dict):
                errors.append(f"glossary[{i}] must be an object")
                continue
            for field in ("term_id", "original_term", "canonical_ru", "definition", "locators"):
                _need(bool(term.get(field)), f"glossary[{i}] missing {field}", errors)

    algorithms = payload.get("algorithms", [])
    _need(isinstance(algorithms, list), "algorithms must be a list", errors)
    if isinstance(algorithms, list):
        for i, algo in enumerate(algorithms):
            if not isinstance(algo, dict):
                errors.append(f"algorithms[{i}] must be an object")
                continue
            _need(bool(algo.get("algorithm_id")), f"algorithms[{i}] missing algorithm_id", errors)
            _need(bool(algo.get("steps")), f"algorithms[{i}] missing steps", errors)
            _need(bool(algo.get("source_locators")), f"algorithms[{i}] missing source_locators", errors)

    conclusions = payload.get("conclusions", [])
    if isinstance(conclusions, list):
        for i, conclusion in enumerate(conclusions):
            if not isinstance(conclusion, dict):
                errors.append(f"conclusions[{i}] must be an object")
                continue
            _need(conclusion.get("owner") in {"AUTHOR", "ALINA"}, f"conclusions[{i}] owner must be AUTHOR or ALINA", errors)
            _need(bool(conclusion.get("source_locators") or conclusion.get("input_knowledge_ids")),
                  f"conclusions[{i}] lacks traceability", errors)

    combinations = payload.get("combinations", [])
    if isinstance(combinations, list):
        for i, combo in enumerate(combinations):
            if not isinstance(combo, dict):
                errors.append(f"combinations[{i}] must be an object")
                continue
            _need(bool(combo.get("input_knowledge_ids")), f"combinations[{i}] missing input_knowledge_ids", errors)
            _need(bool(combo.get("validation_needed")), f"combinations[{i}] missing validation_needed", errors)

    checklists = payload.get("checklists", [])
    if isinstance(checklists, list):
        for i, checklist in enumerate(checklists):
            if not isinstance(checklist, dict):
                errors.append(f"checklists[{i}] must be an object")
                continue
            _need(bool(checklist.get("source_knowledge_ids")), f"checklists[{i}] missing source_knowledge_ids", errors)
            _need(bool(checklist.get("items")), f"checklists[{i}] missing items", errors)
            _need(bool(checklist.get("pass_fail_rule")), f"checklists[{i}] missing pass_fail_rule", errors)

    quality = payload.get("quality", {})
    _need(isinstance(quality, dict), "quality must be an object", errors)
    if isinstance(quality, dict):
        for gate in ("translation_traceable", "inference_separated", "provenance_complete"):
            _need(gate in quality, f"quality missing {gate}", errors)

    return errors


def package_id(payload: dict) -> str:
    source = payload.get("source", "SRC-UNKNOWN")
    scope_id = payload.get("scope_id") or payload.get("scope", "scope")
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(scope_id))
    return f"{source}::{safe}"


def load_package(path: Path) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate_package(payload)
    if errors:
        raise BookKnowledgeError("; ".join(errors))
    return payload


def store_package(db, payload: dict, path: str | None = None) -> dict:
    errors = validate_package(payload)
    if errors:
        raise BookKnowledgeError("; ".join(errors))

    ident = package_id(payload)
    now = time.time()
    status = payload.get("status", "REVIEW_REQUIRED")
    existing = db.execute("SELECT created FROM book_packages WHERE package_id=?", (ident,)).fetchone()
    created = existing[0] if existing else now
    db.execute(
        """INSERT INTO book_packages(package_id,source_id,scope,schema_name,status,path,payload,created,updated)
           VALUES(?,?,?,?,?,?,?,?,?)
           ON CONFLICT(package_id) DO UPDATE SET source_id=excluded.source_id,scope=excluded.scope,
             schema_name=excluded.schema_name,status=excluded.status,path=excluded.path,
             payload=excluded.payload,updated=excluded.updated""",
        (ident, payload["source"], payload["scope"], payload["schema"], status, path,
         json.dumps(payload, ensure_ascii=False), created, now),
    )
    db.execute(
        "INSERT INTO book_package_events(at,package_id,kind,detail) VALUES(?,?,?,?)",
        (now, ident, "stored", status),
    )
    return {"package_id": ident, "status": status, "errors": []}


def import_package_file(db, path: Path) -> dict:
    payload = load_package(path)
    return store_package(db, payload, str(path))


def summary(db) -> dict:
    total = db.execute("SELECT count(*) FROM book_packages").fetchone()[0]
    by_status = dict(db.execute("SELECT status,count(*) FROM book_packages GROUP BY status").fetchall())
    recent = [
        dict(row) for row in db.execute(
            "SELECT package_id,source_id,scope,status,path,updated FROM book_packages ORDER BY updated DESC LIMIT 10"
        ).fetchall()
    ]
    return {"packages": total, "by_status": by_status, "recent": recent}


def list_packages(db) -> list[dict]:
    return [
        dict(row) for row in db.execute(
            "SELECT package_id,source_id,scope,status,path,created,updated FROM book_packages ORDER BY updated DESC"
        ).fetchall()
    ]


def import_bundled_packages(db, base: Path) -> list[dict]:
    """Import canonical derived book packages shipped with the repository."""
    imported = []
    root = Path(base) / "docs" / "books"
    if not root.exists():
        return imported
    for path in sorted(root.glob("BOOK-*/ch*/package.json")):
        try:
            result = import_package_file(db, path)
            imported.append({"path": str(path), **result})
        except (OSError, json.JSONDecodeError, BookKnowledgeError) as exc:
            ident = str(path)
            db.execute(
                "INSERT INTO book_package_events(at,package_id,kind,detail) VALUES(?,?,?,?)",
                (time.time(), ident, "import_error", str(exc)[:1000]),
            )
            imported.append({"path": str(path), "status": "ERROR", "error": str(exc)})
    return imported
