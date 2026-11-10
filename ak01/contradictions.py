from __future__ import annotations

import re


def normalize_claim(text: str) -> tuple[str, bool]:
    value = text.lower().strip().rstrip(".")
    negated = bool(re.search(r"\b(not|does not|isn't|cannot|can't)\b", value))
    normalized = re.sub(r"\bdoes not\b|\bnot\b|\bisn't\b|\bcannot\b|\bcan't\b", "", value)
    normalized = re.sub(r"\brequires\b", "require", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized, negated


def detect_pair(a: str, b: str) -> bool:
    na, neg_a = normalize_claim(a)
    nb, neg_b = normalize_claim(b)
    return na == nb and neg_a != neg_b
