from __future__ import annotations

from abc import ABC, abstractmethod
from .domain import Job


class JobRepository(ABC):
    @abstractmethod
    def save(self, job: Job) -> None: ...

    @abstractmethod
    def get(self, job_id: str) -> Job: ...


class InMemoryJobRepository(JobRepository):
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}

    def save(self, job: Job) -> None:
        self._jobs[job.id] = job

    def get(self, job_id: str) -> Job:
        return self._jobs[job_id]

    def clear(self) -> None:
        self._jobs.clear()
