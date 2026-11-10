from __future__ import annotations

import hashlib
import uuid
from typing import Any

from .domain import Job
from .repositories import JobRepository
from .events import DomainEvent, EventBus


class KnowledgeApplication:
    def __init__(self, jobs: JobRepository, events: EventBus) -> None:
        self.jobs = jobs
        self.events = events

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

    def _emit(self, job: Job, event_type: str, **payload: Any) -> None:
        record = {"event_type": event_type, **payload}
        job.events.append(record)
        job.audit.append({"action": event_type, **payload})
        self.events.publish(DomainEvent(event_type, {"job_id": job.id, **payload}))
