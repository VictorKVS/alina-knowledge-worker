from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from .models import OutboxEventModel


def enqueue_event(session: Session, event_type: str, payload: dict) -> OutboxEventModel:
    event = OutboxEventModel(
        id=str(uuid.uuid4()),
        event_type=event_type,
        payload=payload,
        delivered=False,
    )
    session.add(event)
    return event


def pending_events(session: Session, limit: int = 100):
    return (
        session.query(OutboxEventModel)
        .filter(OutboxEventModel.delivered.is_(False))
        .order_by(OutboxEventModel.created_at.asc())
        .limit(limit)
        .all()
    )


def mark_delivered(session: Session, event: OutboxEventModel) -> None:
    event.delivered = True
