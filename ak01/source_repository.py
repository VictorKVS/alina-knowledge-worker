from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from .models import SourceModel


class SQLAlchemySourceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, *, job_id: str, title: str, version: str, content: str, content_hash: str, locator: str) -> SourceModel:
        existing = (
            self.session.query(SourceModel)
            .filter_by(job_id=job_id, content_hash=content_hash, version=version)
            .one_or_none()
        )
        if existing is not None:
            return existing

        item = SourceModel(
            id=str(uuid.uuid4()),
            job_id=job_id,
            title=title,
            version=version,
            content=content,
            content_hash=content_hash,
            locator=locator,
        )
        self.session.add(item)
        self.session.flush()
        return item

    def get(self, source_id: str) -> SourceModel:
        item = self.session.get(SourceModel, source_id)
        if item is None:
            raise KeyError(source_id)
        return item

    def list_for_job(self, job_id: str) -> list[SourceModel]:
        return self.session.query(SourceModel).filter_by(job_id=job_id).all()

    def mark_stale(self, source_id: str) -> SourceModel:
        item = self.get(source_id)
        item.stale = True
        self.session.flush()
        return item
