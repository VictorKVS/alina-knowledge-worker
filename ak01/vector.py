from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class VectorHit:
    item_id: str
    score: float
    metadata: dict


class VectorIndex:
    def upsert(self, item_id: str, vector: list[float], metadata: dict) -> None:
        raise NotImplementedError

    def search(self, vector: list[float], limit: int = 10) -> list[VectorHit]:
        raise NotImplementedError


class InMemoryVectorIndex(VectorIndex):
    def __init__(self) -> None:
        self._items: dict[str, tuple[list[float], dict]] = {}

    def upsert(self, item_id: str, vector: list[float], metadata: dict) -> None:
        self._items[item_id] = (vector, metadata)

    def search(self, vector: list[float], limit: int = 10) -> list[VectorHit]:
        # Placeholder deterministic adapter until pgvector implementation is wired.
        return [
            VectorHit(item_id=k, score=0.0, metadata=v[1])
            for k, v in list(self._items.items())[:limit]
        ]
