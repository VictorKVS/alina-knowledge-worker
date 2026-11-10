from __future__ import annotations

import hashlib
import uuid
from typing import Any

from .contradictions import detect_pair
from .domain import Job
from .events import DomainEvent, EventBus
from .extraction import ExtractionEngine
from .repositories import JobRepository


class KnowledgeApplication:
    def __init__(self, jobs: JobRepository, events: EventBus) -> None:
        self.jobs = jobs
        self.events = events
        self.extractor = ExtractionEngine()

    def create_job(self, target: dict[str, Any], policy: dict[str, Any]) -> Job:
        job = Job(id=str(uuid.uuid4()), target=target, policy=policy)
        self.jobs.save(job)
        self._emit(job, "KnowledgeJobCreated")
        return job

    def register_source(self, job_id: str, source: dict[str, Any]) -> dict[str, Any]:
        job = self.jobs.get(job_id)
        content = source.get("content", "")
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        existing = next(
            (s for s in job.sources if s.get("content_hash") == content_hash and s.get("version") == source.get("version", "1")),
            None,
        )
        if existing:
            return existing

        record = {
            **source,
            "id": source.get("id") or str(uuid.uuid4()),
            "version": source.get("version", "1"),
            "content_hash": content_hash,
            "locator": source.get("locator", "body"),
        }
        job.sources.append(record)
        self.jobs.save(job)
        self._emit(job, "SourceRegistered", source_id=record["id"])
        return record

    def extract_all(self, job_id: str, scope_layer: str = "DOMAIN") -> int:
        job = self.jobs.get(job_id)
        produced = 0

        for source in job.sources:
            units = self.extractor.extract(job_id=job.id, source=source, scope_layer=scope_layer)
            for unit in units:
                dedupe = (unit["provenance"]["source_hash"], unit["text"], unit["scope_layer"])
                if any(
                    (u.get("provenance", {}).get("source_hash"), u.get("text"), u.get("scope_layer")) == dedupe
                    for u in job.units
                ):
                    continue
                job.units.append(unit)
                produced += 1

        self._recompute_contradictions(job)
        self.jobs.save(job)
        self._emit(job, "KnowledgeExtractionCompleted", produced=produced)
        return produced

    def get_units(self, job_id: str) -> list[dict[str, Any]]:
        return list(self.jobs.get(job_id).units)

    def get_contradictions(self, job_id: str) -> list[dict[str, Any]]:
        return list(self.jobs.get(job_id).contradictions)

    def _recompute_contradictions(self, job: Job) -> None:
        result: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for i, left in enumerate(job.units):
            for right in job.units[i + 1:]:
                if detect_pair(left["text"], right["text"]):
                    key = tuple(sorted((left["id"], right["id"])))
                    if key in seen:
                        continue
                    seen.add(key)
                    result.append({
                        "id": str(uuid.uuid4()),
                        "claims": [left["id"], right["id"]],
                        "auto_resolved": False,
                    })
        job.contradictions = result

    def _emit(self, job: Job, event_type: str, **payload: Any) -> None:
        record = {"event_type": event_type, **payload}
        job.events.append(record)
        job.audit.append({"action": event_type, **payload})
        self.events.publish(DomainEvent(event_type, {"job_id": job.id, **payload}))
