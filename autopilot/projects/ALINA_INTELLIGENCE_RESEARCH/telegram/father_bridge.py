"""Offline bridge from an approved FATHER Telegram Material export into ALINA.
No TDLib access, no credentials, no network, no automatic knowledge promotion.
"""
from __future__ import annotations
from typing import Any, Iterable
from pipeline import ingest, Candidate

def map_material(material: dict[str, Any], *, authorized_by_policy: bool) -> dict[str, Any]:
    if material.get("source_type") != "telegram":
        raise ValueError("expected Telegram material")
    meta = material.get("metadata") or {}
    if not isinstance(meta, dict):
        raise ValueError("invalid metadata")
    return {
        "authorized": authorized_by_policy,
        "chat_id": str(meta.get("chat_id") or ""),
        "message_id": str(meta.get("message_id") or ""),
        "text": str(material.get("raw_text") or ""),
        "url": material.get("source_locator"),
        "published_at": material.get("published_at"),
    }

def bridge_batch(materials: Iterable[dict[str, Any]], *, authorized_by_policy: bool) -> tuple[list[Candidate], dict]:
    return ingest(map_material(item, authorized_by_policy=authorized_by_policy) for item in materials)
