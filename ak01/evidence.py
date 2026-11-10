from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Provenance:
    source_id: str
    source_version_id: str
    source_fragment_id: str
    locator: str
    source_hash: str
    extraction_job_id: str
    extractor_version: str


def provenance_complete(p: dict) -> bool:
    required = {
        "source_id",
        "source_version_id",
        "source_fragment_id",
        "locator",
        "source_hash",
        "extraction_job_id",
        "extractor_version",
    }
    return required.issubset(p) and all(p.get(k) for k in required)
