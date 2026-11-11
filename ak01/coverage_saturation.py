from __future__ import annotations

from copy import deepcopy
from typing import Any

REQUIRED_DIMENSIONS = {
    "concept",
    "decision",
    "procedure",
    "limitation",
    "evidence",
    "contradiction",
    "practice",
    "evaluation",
    "safety_security",
}


def assess_coverage(
    *,
    requirements: list[dict[str, Any]],
    evidence_items: list[dict[str, Any]],
) -> dict[str, Any]:
    coverage: dict[str, dict[str, Any]] = {}
    for requirement in requirements:
        requirement_id = str(requirement.get("requirement_id"))
        dimensions = set(requirement.get("required_dimensions") or [])
        dimensions = dimensions & REQUIRED_DIMENSIONS

        covered_dimensions: set[str] = set()
        supporting_items: list[str] = []

        for item in evidence_items:
            if requirement_id not in set(item.get("requirement_ids") or []):
                continue
            supporting_items.append(str(item.get("evidence_id")))
            for dimension in item.get("dimensions") or []:
                if dimension in REQUIRED_DIMENSIONS:
                    covered_dimensions.add(str(dimension))

        missing = sorted(dimensions - covered_dimensions)

        coverage[requirement_id] = {
            "required_dimensions": sorted(dimensions),
            "covered_dimensions": sorted(covered_dimensions),
            "missing_dimensions": missing,
            "supporting_evidence_ids": supporting_items,
            "status": "COVERED" if not missing else "PARTIAL",
        }

    all_covered = bool(coverage) and all(
        item["status"] == "COVERED"
        for item in coverage.values()
    )

    return {
        "coverage": coverage,
        "all_requirements_covered": all_covered,
    }


def assess_saturation(
    *,
    coverage_result: dict[str, Any],
    iteration_history: list[dict[str, Any]],
    mandatory_alternatives_covered: bool,
    material_contradictions_documented: bool,
    failure_modes_covered: bool,
) -> dict[str, Any]:
    if not coverage_result.get("all_requirements_covered"):
        return {
            "decision": "EXPAND",
            "reason": "mandatory_knowledge_requirements_not_covered",
        }

    if not mandatory_alternatives_covered:
        return {
            "decision": "EXPAND",
            "reason": "material_alternatives_missing",
        }

    if not material_contradictions_documented:
        return {
            "decision": "EXPAND",
            "reason": "material_contradictions_not_documented",
        }

    if not failure_modes_covered:
        return {
            "decision": "EXPAND",
            "reason": "failure_modes_not_covered",
        }

    if len(iteration_history) < 2:
        return {
            "decision": "EXPAND",
            "reason": "insufficient_search_iterations_for_saturation",
        }

    last_two = iteration_history[-2:]
    material_new_counts = [
        int(item.get("material_new_findings", 0))
        for item in last_two
    ]
    if any(count > 0 for count in material_new_counts):
        return {
            "decision": "EXPAND",
            "reason": "recent_iterations_added_material_findings",
        }

    return {
        "decision": "STOP",
        "reason": "mandatory_coverage_complete_and_recent_iterations_saturated",
        "coverage_snapshot": deepcopy(coverage_result),
    }


def validate_coverage_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if "coverage" not in result:
        errors.append("missing_coverage")
    if "all_requirements_covered" not in result:
        errors.append("missing_all_requirements_covered")

    return errors
