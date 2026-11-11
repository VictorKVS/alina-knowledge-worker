from __future__ import annotations

from copy import deepcopy
from typing import Any


PROBLEM_CLASSES = {
    "SEARCH",
    "MATCHING",
    "RANKING",
    "OPTIMIZATION",
    "PREDICTION",
    "DETECTION",
    "DIAGNOSIS",
    "PLANNING",
    "SCHEDULING",
    "CONTROL",
    "CLASSIFICATION",
    "GENERATION",
    "VALIDATION",
    "ARGUMENTATION",
    "RISK_ASSESSMENT",
    "ROOT_CAUSE_ANALYSIS",
    "MULTI_CRITERIA_DECISION",
    "UNKNOWN",
}


def build_problem_signature(
    *,
    problem_id: str,
    statement: str,
    expected_output: str,
    constraints: dict[str, Any] | None = None,
    uncertainty: list[str] | None = None,
    failure_cost: str = "UNKNOWN",
    reversibility: str = "UNKNOWN",
    frequency: str = "UNKNOWN",
    scale: str = "UNKNOWN",
    criticality: str = "NORMAL",
    problem_class: str = "UNKNOWN",
) -> dict[str, Any]:
    normalized_class = problem_class.upper()
    if normalized_class not in PROBLEM_CLASSES:
        normalized_class = "UNKNOWN"

    return {
        "problem_id": problem_id,
        "statement": statement,
        "expected_output": expected_output,
        "constraints": deepcopy(constraints or {}),
        "uncertainty": list(uncertainty or []),
        "failure_cost": failure_cost,
        "reversibility": reversibility,
        "frequency": frequency,
        "scale": scale,
        "criticality": criticality.upper(),
        "problem_class": normalized_class,
        "status": "SIGNATURE_READY",
    }


def register_candidate_method(
    *,
    problem_signature: dict[str, Any],
    method_id: str,
    method_name: str,
    method_family: str,
    knowledge_ids: list[str],
    applicability: list[str] | None = None,
    contraindications: list[str] | None = None,
    metrics: list[str] | None = None,
    timing: dict[str, Any] | None = None,
    resource_requirements: dict[str, Any] | None = None,
    failure_modes: list[str] | None = None,
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "candidate_id": method_id,
        "problem_id": problem_signature.get("problem_id"),
        "name": method_name,
        "family": method_family,
        "knowledge_ids": list(knowledge_ids),
        "applicability": list(applicability or []),
        "contraindications": list(contraindications or []),
        "metrics": list(metrics or []),
        "timing": deepcopy(timing or {}),
        "resource_requirements": deepcopy(resource_requirements or {}),
        "failure_modes": list(failure_modes or []),
        "evidence_refs": list(evidence_refs or []),
        "status": "CANDIDATE",
    }


def assess_candidate_readiness(
    candidate: dict[str, Any],
    *,
    qualified_knowledge_ids: set[str],
) -> dict[str, Any]:
    missing_knowledge = sorted(
        set(candidate.get("knowledge_ids", [])) - set(qualified_knowledge_ids)
    )
    missing_evidence = not bool(candidate.get("evidence_refs"))
    missing_metrics = not bool(candidate.get("metrics"))
    missing_failure_modes = not bool(candidate.get("failure_modes"))

    blockers: list[str] = []
    if missing_knowledge:
        blockers.append("unqualified_or_missing_knowledge")
    if missing_evidence:
        blockers.append("missing_evidence")
    if missing_metrics:
        blockers.append("missing_metrics")
    if missing_failure_modes:
        blockers.append("missing_failure_modes")

    return {
        "candidate_id": candidate.get("candidate_id"),
        "ready_for_comparison": not blockers,
        "blockers": blockers,
        "missing_knowledge_ids": missing_knowledge,
    }


def build_problem_solution_graph(
    *,
    problem_signature: dict[str, Any],
    candidates: list[dict[str, Any]],
    qualified_knowledge_ids: set[str],
) -> dict[str, Any]:
    nodes = [{
        "id": problem_signature.get("problem_id"),
        "type": "PROBLEM",
        "label": problem_signature.get("statement"),
        "status": problem_signature.get("status"),
    }]
    edges: list[dict[str, str]] = []
    readiness: list[dict[str, Any]] = []

    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id"))
        nodes.append({
            "id": candidate_id,
            "type": "METHOD",
            "label": candidate.get("name"),
            "status": candidate.get("status", "CANDIDATE"),
        })
        edges.append({
            "from": str(problem_signature.get("problem_id")),
            "to": candidate_id,
            "type": "HAS_CANDIDATE",
        })

        for knowledge_id in candidate.get("knowledge_ids", []):
            nodes.append({
                "id": knowledge_id,
                "type": "KNOWLEDGE",
                "label": knowledge_id,
                "status": (
                    "QUALIFIED"
                    if knowledge_id in qualified_knowledge_ids
                    else "UNQUALIFIED"
                ),
            })
            edges.append({
                "from": candidate_id,
                "to": knowledge_id,
                "type": "REQUIRES_KNOWLEDGE",
            })

        readiness.append(
            assess_candidate_readiness(
                candidate,
                qualified_knowledge_ids=qualified_knowledge_ids,
            )
        )

    unique_nodes = {str(node["id"]): node for node in nodes}

    return {
        "graph_id": f'{problem_signature.get("problem_id")}:SOLUTION',
        "problem_signature": deepcopy(problem_signature),
        "nodes": list(unique_nodes.values()),
        "edges": edges,
        "candidate_readiness": readiness,
        "selection_status": (
            "READY_FOR_COMPARISON"
            if readiness and all(item["ready_for_comparison"] for item in readiness)
            else "RESEARCH_OR_QUALIFICATION_REQUIRED"
        ),
        "selected_candidate_id": None,
    }


def validate_problem_solution_graph(graph: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not graph.get("problem_signature"):
        errors.append("missing_problem_signature")
    if graph.get("selected_candidate_id") is not None:
        errors.append("candidate_selected_before_comparison")
    if not graph.get("candidate_readiness"):
        errors.append("missing_candidate_readiness")
    return errors
