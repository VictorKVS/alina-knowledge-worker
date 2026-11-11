from __future__ import annotations

from copy import deepcopy
from typing import Any

QUALIFICATION_VERDICTS = {
    "QUALIFIED",
    "REJECTED",
    "NEEDS_MORE_EVIDENCE",
    "CONFLICTED",
}


def qualify_knowledge_unit(
    unit: dict[str, Any],
    *,
    reviewer_id: str,
    reviewer_role: str,
    criteria: dict[str, bool],
    notes: list[str] | None = None,
) -> dict[str, Any]:
    """Apply an external qualification gate to a prepared knowledge unit."""
    if reviewer_id == "AK-01" or reviewer_role.upper() == "AK-01":
        raise PermissionError("AK-01 cannot qualify its own knowledge")

    required_criteria = {
        "provenance_complete",
        "evidence_sufficient",
        "limitations_explicit",
        "counter_evidence_reviewed",
        "tests_present",
    }

    missing_criteria = sorted(required_criteria - set(criteria))
    if missing_criteria:
        return {
            "knowledge_id": unit.get("knowledge_id"),
            "reviewer_id": reviewer_id,
            "reviewer_role": reviewer_role,
            "verdict": "NEEDS_MORE_EVIDENCE",
            "reasons": [f"missing_criterion:{item}" for item in missing_criteria],
            "criteria": deepcopy(criteria),
            "notes": list(notes or []),
            "qualified_state": unit.get("state"),
            "promotion_allowed": False,
        }

    failed = sorted(name for name in required_criteria if criteria.get(name) is not True)

    if unit.get("state") == "CONFLICTED":
        verdict = "CONFLICTED"
        reasons = ["knowledge_unit_contains_material_counter_evidence"]
        promotion_allowed = False
    elif failed:
        verdict = "NEEDS_MORE_EVIDENCE"
        reasons = [f"criterion_failed:{item}" for item in failed]
        promotion_allowed = False
    elif not unit.get("evidence_links"):
        verdict = "REJECTED"
        reasons = ["no_evidence_links"]
        promotion_allowed = False
    else:
        verdict = "QUALIFIED"
        reasons = ["all_qualification_criteria_passed"]
        promotion_allowed = True

    return {
        "knowledge_id": unit.get("knowledge_id"),
        "reviewer_id": reviewer_id,
        "reviewer_role": reviewer_role,
        "verdict": verdict,
        "reasons": reasons,
        "criteria": deepcopy(criteria),
        "notes": list(notes or []),
        "qualified_state": "QUALIFIED" if promotion_allowed else unit.get("state"),
        "promotion_allowed": promotion_allowed,
    }


def apply_qualification(
    unit: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    """Return a promoted copy only when an external record allows promotion."""
    updated = deepcopy(unit)

    if record.get("promotion_allowed") is True and record.get("verdict") == "QUALIFIED":
        updated["state"] = "QUALIFIED"
        updated["qualification_record"] = deepcopy(record)
        updated["auto_qualified"] = False
        return updated

    updated["qualification_record"] = deepcopy(record)
    return updated


def validate_qualification_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if record.get("verdict") not in QUALIFICATION_VERDICTS:
        errors.append("invalid_qualification_verdict")
    if not record.get("reviewer_id"):
        errors.append("missing_reviewer_id")
    if not record.get("reviewer_role"):
        errors.append("missing_reviewer_role")
    if not record.get("reasons"):
        errors.append("missing_reasons")

    if record.get("verdict") == "QUALIFIED" and record.get("promotion_allowed") is not True:
        errors.append("qualified_without_promotion_permission")

    if record.get("verdict") != "QUALIFIED" and record.get("promotion_allowed") is True:
        errors.append("nonqualified_record_allows_promotion")

    return errors
