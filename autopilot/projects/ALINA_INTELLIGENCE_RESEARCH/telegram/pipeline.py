"""Offline Telegram -> ALINA research intake. No network or Telegram login.
Input must be an authorized, already-collected export. No prompt/RAG promotion.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

TOPICS: dict[str, tuple[str, ...]] = {
    "rag": ("rag", "retrieval", "bm25", "rerank", "эмбеддинг", "векторн", "поиск", "chunking"),
    "prompt": ("prompt", "промпт", "инструкц", "system message", "prompt injection"),
    "evaluation": ("eval", "faithfulness", "citation", "benchmark", "метрик", "оценк"),
    "security": ("devsecops", "security", "уязвим", "owasp", "безопасност"),
}
MAX_TEXT = 50_000

@dataclass(frozen=True)
class Candidate:
    provider: str
    chat_id: str
    message_id: str
    locator: str
    published_at: str | None
    text_sha256: str
    topics: tuple[str, ...]
    links: tuple[str, ...]
    status: str
    trust: str
    text: str

def classify(text: str) -> tuple[str, ...]:
    val = text.casefold()
    return tuple(k for k, needles in TOPICS.items() if any(n in val for n in needles))

def process_record(row: dict) -> Candidate | None:
    if not isinstance(row, dict):
        raise ValueError("record must be an object")
    # Access permission is supplied by an external approved connector, never guessed.
    if row.get("authorized") is not True:
        return None
    chat_id = str(row.get("chat_id", "")).strip()
    message_id = str(row.get("message_id", "")).strip()
    txt = str(row.get("text", ""))
    if not chat_id or not message_id or len(txt) > MAX_TEXT:
        raise ValueError("invalid chat/message identifiers or oversized content")
    topics = classify(txt)
    if not topics:
        return None
    links = tuple(dict.fromkeys(re.findall(r"https?://[^\s<>\"']+", txt)))[:20]
    locator = str(row.get("url") or f"telegram://{chat_id}/{message_id}")
    return Candidate("telegram", chat_id, message_id, locator,
        str(row["published_at"]) if row.get("published_at") else None,
        hashlib.sha256(txt.encode("utf-8")).hexdigest(), topics, links,
        "UNVERIFIED_CANDIDATE", "SIGNAL_ONLY", txt)

def ingest(records: Iterable[dict]) -> tuple[list[Candidate], dict]:
    accepted: dict[tuple[str, str], Candidate] = {}
    total = skipped = duplicates = 0
    for record in records:
        total += 1
        item = process_record(record)
        if item is None:
            skipped += 1
            continue
        key = item.chat_id, item.message_id
        if key in accepted:
            duplicates += 1
            continue
        accepted[key] = item
    return list(accepted.values()), {"total": total, "skipped": skipped,
                                      "duplicates": duplicates, "candidates": len(accepted)}

def run_file(source: Path, out: Path) -> dict:
    if source.resolve() == out.resolve():
        raise ValueError("output cannot overwrite input")
    with source.open(encoding="utf-8") as fh:
        records = (json.loads(line) for line in fh if line.strip())
        candidates, stats = ingest(records)
    out.parent.mkdir(parents=True, exist_ok=True)
    # Do not include source content in public repositories. Local output only.
    with out.open("w", encoding="utf-8") as fh:
        for item in candidates:
            fh.write(json.dumps(asdict(item), ensure_ascii=False) + "\n")
    return stats

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Offline ALINA Telegram candidate intake")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run_file(args.input, args.output), ensure_ascii=False))
