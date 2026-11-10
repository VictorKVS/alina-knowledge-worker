from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


def utcnow():
    return datetime.now(timezone.utc)


class KnowledgeJobModel(Base):
    __tablename__ = "knowledge_jobs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    target: Mapped[dict] = mapped_column(JSON, nullable=False)
    policy: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="CREATED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class SourceModel(Base):
    __tablename__ = "sources"
    __table_args__ = (UniqueConstraint("job_id", "content_hash", "version", name="uq_source_version_hash"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("knowledge_jobs.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    version: Mapped[str] = mapped_column(String(64), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    locator: Mapped[str] = mapped_column(String(512), default="body", nullable=False)
    quarantined: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    stale: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class KnowledgeUnitModel(Base):
    __tablename__ = "knowledge_units"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("knowledge_jobs.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    unit_type: Mapped[str] = mapped_column(String(64), nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    scope_layer: Mapped[str] = mapped_column(String(32), nullable=False)
    provenance: Mapped[dict] = mapped_column(JSON, nullable=False)
    canonical_id: Mapped[str | None] = mapped_column(String(256), nullable=True)


class CapsuleVersionModel(Base):
    __tablename__ = "capsule_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    capsule_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    released: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class OutboxEventModel(Base):
    __tablename__ = "outbox_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    delivered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
