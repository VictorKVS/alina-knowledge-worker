from __future__ import annotations

from copy import deepcopy
from typing import Any


def review_metadata_conflicts(
    entry: dict[str, Any],
    *,
    reviewer_id: str,
    reviewer_role: str,
    canonical_values: dict[str, Any],
    evidence: list[str],
    rationale: str,
) -> dict[str, Any]:
    """Resolve registry metadata conflicts with an auditable review record."""
    conflicts = list(entry.get("metadata_conflicts") or [])
    if not conflicts:
        raise ValueError("Metadata review requires existing conflicts")
    if not reviewer_id or not reviewer_role:
        raise ValueError("Metadata review requires reviewer identity and role")
    if not evidence:
        raise ValueError("Metadata review requires evidence")
    if not rationale:
        raise ValueError("Metadata review requires rationale")

    conflicted_fields = {str(item.get("field")) for item in conflicts}
    missing_resolutions = sorted(
        field
        for field in conflicted_fields
        if field not in canonical_values
    )
    if missing_resolutions:
        raise ValueError(
            "Missing canonical values for conflicted fields: "
            + ", ".join(missing_resolutions)
        )

    updated = deepcopy(entry)

    for field, value in canonical_values.items():
        if field in conflicted_fields:
            updated[field] = deepcopy(value)

    record = {
        "reviewer_id": reviewer_id,
        "reviewer_role": reviewer_role,
        "conflicts_reviewed": deepcopy(conflicts),
        "canonical_values": deepcopy(canonical_values),
        "evidence": list(evidence),
        "rationale": rationale,
        "verdict": "RESOLVED",
    }

    updated["metadata_review_record"] = record
    updated["metadata_review_resolved"] = True
    updated["requires_metadata_review"] = False
    updated["status"] = "DISCOVERED_UNQUALIFIED"

    return updated


def validate_metadata_review(entry: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if entry.get("metadata_review_resolved") is True:
        record = entry.get("metadata_review_record") or {}

        if not record.get("reviewer_id"):
            errors.append("missing_metadata_reviewer_id")
        if not record.get("reviewer_role"):
            errors.append("missing_metadata_reviewer_role")
        if not record.get("evidence"):
            errors.append("missing_metadata_review_evidence")
        if not record.get("rationale"):
            errors.append("missing_metadata_review_rationale")
        if record.get("verdict") != "RESOLVED":
            errors.append("invalid_metadata_review_verdict")
        if entry.get("requires_metadata_review") is True:
            errors.append("resolved_metadata_still_requires_review")

    return errors
