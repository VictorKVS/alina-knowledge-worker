from __future__ import annotations

from copy import deepcopy
from typing import Any


BLOCKED_STATES = {
    "RAW",
    "EXTRACTED",
    "EVIDENCE_LINKED",
    "VERIFIED_NOT_QUALIFIED",
    "CONFLICTED",
    "SUPERSEDED",
    "ARCHIVED",
}


def evaluate_runtime_access(
    knowledge_unit: dict[str, Any],
    *,
    task_criticality: str = "NORMAL",
) -> dict[str, Any]:
    """Decide whether a knowledge unit may be used during professional execution."""
    state = str(knowledge_unit.get("state", "UNKNOWN")).upper()
    criticality = task_criticality.upper()

    if state == "QUALIFIED":
        decision = "ALLOW"
        reason = "knowledge_is_qualified"
    elif state == "CONFLICTED":
        decision = "ESCALATE"
        reason = "material_counter_evidence_present"
    elif state in BLOCKED_STATES:
        decision = "BLOCK"
        reason = f"knowledge_state_not_runtime_eligible:{state.lower()}"
    else:
        decision = "BLOCK"
        reason = "unknown_knowledge_state"

    if criticality in {"HIGH", "SAFETY_CRITICAL"} and decision == "ALLOW":
        record = knowledge_unit.get("qualification_record") or {}
        if not record.get("reviewer_id"):
            decision = "ESCALATE"
            reason = "critical_task_requires_traceable_qualification_record"

    return {
        "knowledge_id": knowledge_unit.get("knowledge_id"),
        "knowledge_state": state,
        "task_criticality": criticality,
        "decision": decision,
        "reason": reason,
        "runtime_snapshot": deepcopy(knowledge_unit) if decision == "ALLOW" else None,
    }


def filter_runtime_knowledge(
    units: list[dict[str, Any]],
    *,
    task_criticality: str = "NORMAL",
) -> dict[str, Any]:
    decisions = [
        evaluate_runtime_access(unit, task_criticality=task_criticality)
        for unit in units
    ]
    return {
        "allowed": [
            item["runtime_snapshot"]
            for item in decisions
            if item["decision"] == "ALLOW"
        ],
        "blocked": [
            item
            for item in decisions
            if item["decision"] == "BLOCK"
        ],
        "escalations": [
            item
            for item in decisions
            if item["decision"] == "ESCALATE"
        ],
        "decisions": decisions,
    }
