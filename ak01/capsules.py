from __future__ import annotations

import copy
from dataclasses import dataclass, field


@dataclass
class Capsule:
    id: str
    job_id: str
    version: str = "0.1.0"
    status: str = "DRAFT"
    artifacts: dict = field(default_factory=dict)


def release_capsule(capsule: Capsule, *, requalified: bool = False) -> Capsule:
    if capsule.status == "RELEASED":
        raise ValueError("released capsule is immutable")
    if capsule.artifacts.get("requires_requalification") and not requalified:
        raise PermissionError("requalification required")
    released = copy.deepcopy(capsule)
    released.status = "RELEASED"
    return released
