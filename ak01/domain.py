from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class KnowledgeState(str, Enum):
    RAW = "RAW"
    EXTRACTED = "EXTRACTED"
    VERIFIED = "VERIFIED"
    QUALIFIED = "QUALIFIED"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"


class ScopeLayer(str, Enum):
    CORE = "CORE"
    DOMAIN = "DOMAIN"
    ORGANIZATION = "ORGANIZATION"
    PROJECT = "PROJECT"
    ACTIVE_CONTEXT = "ACTIVE_CONTEXT"


@dataclass
class Job:
    id: str
    target: dict[str, Any]
    policy: dict[str, Any]
    sources: list[dict[str, Any]] = field(default_factory=list)
    units: list[dict[str, Any]] = field(default_factory=list)
    contradictions: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    audit: list[dict[str, Any]] = field(default_factory=list)
    capsule_versions: dict[str, dict[str, Any]] = field(default_factory=dict)
    stale_sources: set[str] = field(default_factory=set)
