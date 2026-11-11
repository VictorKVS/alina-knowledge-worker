from __future__ import annotations

from copy import deepcopy
from typing import Any

def _normalize_score(value: float, direction: str) -> float:
    if direction == "MINIMIZE":
        return -value
    return value


def compare_candidates(
    *,
    candidates: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    criteria: list[dict[str, Any]],
    measurements: dict[str, dict[str, float]],
    hard_constraints: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compare ready candidates against explicit evidence-backed criteria.

    No winner is produced when readiness, measurements, or hard constraints are
    insufficient.
    """
    readiness_by_id = {
        str(item.get("candidate_id")): item
        for item in readiness
    }
    candidate_by_id = {
        str(item.get("candidate_id")): item
        for item in candidates
    }

    eligible_ids: list[str] = []
    excluded: list[dict[str, Any]] = []

    for candidate_id in candidate_by_id:
        ready = readiness_by_id.get(candidate_id, {})
        reasons: list[str] = []

        if ready.get("ready_for_comparison") is not True:
            reasons.append("candidate_not_ready_for_comparison")

        candidate_measurements = measurements.get(candidate_id, {})
        for criterion in criteria:
            name = str(criterion.get("name"))
            if name not in candidate_measurements:
                reasons.append(f"missing_measurement:{name}")

        for constraint in hard_constraints or []:
            metric = str(constraint.get("metric"))
            operator = str(constraint.get("operator"))
            threshold = float(constraint.get("value"))
            observed = candidate_measurements.get(metric)

            if observed is None:
                reasons.append(f"missing_hard_constraint_measurement:{metric}")
                continue

            failed_constraint = (
                operator == "<=" and not float(observed) <= threshold
            ) or (
                operator == ">=" and not float(observed) >= threshold
            )
            if failed_constraint:
                reasons.append(f"hard_constraint_failed:{metric}")

        if reasons:
            excluded.append({
                "candidate_id": candidate_id,
                "reasons": sorted(set(reasons)),
            })
        else:
            eligible_ids.append(candidate_id)

    if not eligible_ids:
        return {
            "decision": "NO_DECISION",
            "selected_candidate_id": None,
            "scores": {},
            "eligible_candidates": [],
            "excluded_candidates": excluded,
            "reason": "no_candidate_passed_readiness_and_constraints",
            "comparison_trace": deepcopy(criteria),
        }

    scores: dict[str, float] = {}
    contributions: dict[str, dict[str, float]] = {}

    for candidate_id in eligible_ids:
        score = 0.0
        contribution: dict[str, float] = {}
        for criterion in criteria:
            name = str(criterion.get("name"))
            weight = float(criterion.get("weight", 1.0))
            direction = str(criterion.get("direction", "MAXIMIZE")).upper()
            observed = float(measurements[candidate_id][name])
            part = _normalize_score(observed, direction) * weight
            contribution[name] = part
            score += part
        scores[candidate_id] = score
        contributions[candidate_id] = contribution

    best_score = max(scores.values())
    winners = sorted(
        candidate_id
        for candidate_id, score in scores.items()
        if abs(score - best_score) < 1e-12
    )

    if len(winners) != 1:
        return {
            "decision": "NO_DECISION",
            "selected_candidate_id": None,
            "scores": scores,
            "score_contributions": contributions,
            "eligible_candidates": eligible_ids,
            "excluded_candidates": excluded,
            "reason": "comparison_tie_requires_additional_evidence_or_policy",
            "comparison_trace": deepcopy(criteria),
        }

    winner = winners[0]
    return {
        "decision": "SELECTED",
        "selected_candidate_id": winner,
        "scores": scores,
        "score_contributions": contributions,
        "eligible_candidates": eligible_ids,
        "excluded_candidates": excluded,
        "reason": "highest_weighted_score_after_hard_constraints",
        "comparison_trace": deepcopy(criteria),
    }


def validate_selection_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if record.get("decision") not in {"SELECTED", "NO_DECISION"}:
        errors.append("invalid_decision")

    if record.get("decision") == "SELECTED" and not record.get("selected_candidate_id"):
        errors.append("selected_without_candidate")

    if record.get("decision") == "NO_DECISION" and record.get("selected_candidate_id"):
        errors.append("no_decision_with_selected_candidate")

    if not record.get("reason"):
        errors.append("missing_decision_reason")

    if not record.get("comparison_trace"):
        errors.append("missing_comparison_trace")

    return errors
