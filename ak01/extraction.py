from __future__ import annotations

import hashlib
import uuid
from typing import Any

from .parser import SourceParser
from .evidence import provenance_complete


class ExtractionEngine:
    version = "ak01-extractor-0.1"

    def __init__(self, parser: SourceParser | None = None) -> None:
        self.parser = parser or SourceParser()

    def extract(self, *, job_id: str, source: dict[str, Any], scope_layer: str = "DOMAIN") -> list[dict[str, Any]]:
        chunks = self.parser.chunk(source.get("content", ""), locator_prefix=source.get("locator", "body"))
        units = []

        for chunk in chunks:
            fragment_id = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()[:16]
            provenance = {
                "source_id": source["id"],
                "source_version_id": f'{source["id"]}:{source.get("version", "1")}',
                "source_fragment_id": fragment_id,
                "locator": chunk.locator,
                "source_hash": source["content_hash"],
                "extraction_job_id": job_id,
                "extractor_version": self.version,
            }
            units.append({
                "id": str(uuid.uuid4()),
                "text": chunk.text,
                "type": "CLAIM",
                "state": "VERIFIED" if provenance_complete(provenance) else "EXTRACTED",
                "scope_layer": scope_layer,
                "provenance": provenance,
            })
        return units
