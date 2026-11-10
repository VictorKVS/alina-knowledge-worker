from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PgVectorHit:
    item_id: str
    score: float
    metadata: dict[str, Any]


class PgVectorAdapter:
    """
    Production adapter contract.

    SQLAlchemy/pgvector wiring is intentionally deferred until PostgreSQL
    integration tests are enabled. This class defines the stable boundary.
    """

    def __init__(self, session_factory, table_name: str = "knowledge_embeddings") -> None:
        self.session_factory = session_factory
        self.table_name = table_name

    def upsert(self, item_id: str, vector: list[float], metadata: dict[str, Any]) -> None:
        raise NotImplementedError("pgvector persistence wiring pending integration stage")

    def search(self, vector: list[float], limit: int = 10) -> list[PgVectorHit]:
        raise NotImplementedError("pgvector search wiring pending integration stage")
