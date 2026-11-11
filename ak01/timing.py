from __future__ import annotations

from copy import deepcopy
from typing import Any


def build_timing_budget(
    *,
    total_budget_ms: float,
    stages: list[dict[str, Any]],
) -> dict[str, Any]:
    allocated = sum(float(stage.get("budget_ms", 0.0)) for stage in stages)
    remaining = total_budget_ms - allocated

    return {
        "total_budget_ms": float(total_budget_ms),
        "stages": deepcopy(stages),
        "allocated_ms": allocated,
        "remaining_ms": remaining,
        "over_budget": remaining < 0,
        "complete_allocation": abs(remaining) < 1e-9,
    }


def validate_timing_candidate(
    candidate: dict[str, Any],
    *,
    required_latency_ms: float | None = None,
) -> dict[str, Any]:
    timing = candidate.get("timing") or {}
    measured = timing.get("measured_latency_ms")
    source = timing.get("measurement_source")

    blockers: list[str] = []
    if measured is None:
        blockers.append("missing_measured_latency")
    if not source:
        blockers.append("missing_timing_evidence")

    within_budget = None
    if measured is not None and required_latency_ms is not None:
        within_budget = float(measured) <= float(required_latency_ms)
        if not within_budget:
            blockers.append("latency_budget_exceeded")

    return {
        "candidate_id": candidate.get("candidate_id"),
        "measured_latency_ms": measured,
        "required_latency_ms": required_latency_ms,
        "within_budget": within_budget,
        "blockers": blockers,
        "timing_ready": not blockers,
    }
