from __future__ import annotations

from sqlalchemy.orm import Session

from .models import KnowledgeUnitModel


class SQLAlchemyKnowledgeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, unit: KnowledgeUnitModel) -> KnowledgeUnitModel:
        self.session.add(unit)
        self.session.flush()
        return unit

    def list_for_job(self, job_id: str) -> list[KnowledgeUnitModel]:
        return self.session.query(KnowledgeUnitModel).filter_by(job_id=job_id).all()

    def find_by_canonical_id(self, job_id: str, canonical_id: str) -> list[KnowledgeUnitModel]:
        return (
            self.session.query(KnowledgeUnitModel)
            .filter_by(job_id=job_id, canonical_id=canonical_id)
            .all()
        )
