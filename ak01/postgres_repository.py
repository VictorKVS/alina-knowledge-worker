from __future__ import annotations

from sqlalchemy.orm import Session

from .domain import Job
from .models import KnowledgeJobModel
from .repositories import JobRepository


class SQLAlchemyJobRepository(JobRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, job: Job) -> None:
        model = self.session.get(KnowledgeJobModel, job.id)
        if model is None:
            model = KnowledgeJobModel(
                id=job.id,
                target=job.target,
                policy=job.policy,
                status="CREATED",
            )
            self.session.add(model)
        else:
            model.target = job.target
            model.policy = job.policy
        self.session.flush()

    def get(self, job_id: str) -> Job:
        model = self.session.get(KnowledgeJobModel, job_id)
        if model is None:
            raise KeyError(job_id)
        return Job(id=model.id, target=model.target, policy=model.policy)
