from __future__ import annotations

from copy import deepcopy
from typing import Any

ROOT_CAUSES = {
    "K1_KNOWLEDGE_MISSING",
    "K2_KNOWLEDGE_OUTDATED",
    "K3_KNOWLEDGE_INCORRECT",
    "K4_RETRIEVAL_FAILURE",
    "K5_PROCEDURE_MISSING",
    "K6_PROCEDURE_INCORRECT",
    "K7_CHECKLIST_INSUFFICIENT",
    "K8_DECISION_RULE_INCORRECT",
    "K9_PROMPT_POLICY",
    "K10_TOOL_SKILL",
    "K11_LOCAL_KNOWLEDGE",
    "K12_AGENT_CAPABILITY",
    "METHOD_LIMITATION",
    "INPUT_QUALITY",
    "EXTERNAL_DEPENDENCY",
    "UNKNOWN",
}


def record_solution_outcome(
    *,
    problem_id: str,
    selection_record: dict[str, Any],
    expected_metrics: dict[str, float],
    actual_metrics: dict[str, float],
    context: dict[str, Any] | None = None,
    incident_notes: list[str] | None = None,
) -> dict[str, Any]:
    selected = selection_record.get("selected_candidate_id")
    if selection_record.get("decision") != "SELECTED" or not selected:
        raise ValueError("Outcome requires a completed method selection")

    deltas: dict[str, float] = {}
    for name, expected in expected_metrics.items():
        if name in actual_metrics:
            deltas[name] = float(actual_metrics[name]) - float(expected)

    return {
        "problem_id": problem_id,
        "candidate_id": selected,
        "selection_reason": selection_record.get("reason"),
        "expected_metrics": deepcopy(expected_metrics),
        "actual_metrics": deepcopy(actual_metrics),
        "metric_deltas": deltas,
        "context": deepcopy(context or {}),
        "incident_notes": list(incident_notes or []),
        "root_cause": "UNKNOWN",
        "root_cause_evidence": [],
        "status": "OUTCOME_RECORDED",
    }


def classify_root_cause(
    outcome: dict[str, Any],
    *,
    root_cause: str,
    evidence: list[str],
) -> dict[str, Any]:
    if root_cause not in ROOT_CAUSES:
        raise ValueError(f"Unsupported root cause: {root_cause}")
    if not evidence:
        raise ValueError("Root-cause classification requires evidence")

    updated = deepcopy(outcome)
    updated["root_cause"] = root_cause
    updated["root_cause_evidence"] = list(evidence)
    updated["status"] = "ROOT_CAUSE_CLASSIFIED"
    return updated


def route_learning_action(outcome: dict[str, Any]) -> dict[str, Any]:
    root_cause = outcome.get("root_cause", "UNKNOWN")

    routes = {
        "K1_KNOWLEDGE_MISSING": "KNOWLEDGE_ACQUISITION",
        "K2_KNOWLEDGE_OUTDATED": "KNOWLEDGE_REFRESH",
        "K3_KNOWLEDGE_INCORRECT": "KNOWLEDGE_REVIEW",
        "K4_RETRIEVAL_FAILURE": "RAG_RETRIEVAL_REVIEW",
        "K5_PROCEDURE_MISSING": "PROCEDURE_AUTHORING",
        "K6_PROCEDURE_INCORRECT": "PROCEDURE_REVIEW",
        "K7_CHECKLIST_INSUFFICIENT": "CHECKLIST_REVIEW",
        "K8_DECISION_RULE_INCORRECT": "DECISION_RULE_REVIEW",
        "K9_PROMPT_POLICY": "PROMPT_POLICY_REVIEW",
        "K10_TOOL_SKILL": "TOOL_TRAINING",
        "K11_LOCAL_KNOWLEDGE": "LOCAL_KNOWLEDGE_DELTA",
        "K12_AGENT_CAPABILITY": "AGENT_ARCHITECTURE_REVIEW",
        "METHOD_LIMITATION": "METHOD_REVIEW",
        "INPUT_QUALITY": "INPUT_CONTRACT_REVIEW",
        "EXTERNAL_DEPENDENCY": "DEPENDENCY_RESILIENCE_REVIEW",
        "UNKNOWN": "ROOT_CAUSE_INVESTIGATION",
    }

    return {
        "problem_id": outcome.get("problem_id"),
        "candidate_id": outcome.get("candidate_id"),
        "root_cause": root_cause,
        "route": routes[root_cause],
        "evidence": deepcopy(outcome.get("root_cause_evidence", [])),
        "status": "LEARNING_ACTION_REQUIRED",
    }


def build_method_reputation(
    candidate_id: str,
    outcomes: list[dict[str, Any]],
) -> dict[str, Any]:
    scoped = [
        outcome for outcome in outcomes
        if outcome.get("candidate_id") == candidate_id
    ]

    root_causes: dict[str, int] = {}
    metric_history: dict[str, list[float]] = {}

    for outcome in scoped:
        cause = str(outcome.get("root_cause", "UNKNOWN"))
        root_causes[cause] = root_causes.get(cause, 0) + 1

        for metric, value in outcome.get("actual_metrics", {}).items():
            metric_history.setdefault(metric, []).append(float(value))

    metric_averages = {
        metric: sum(values) / len(values)
        for metric, values in metric_history.items()
        if values
    }

    return {
        "candidate_id": candidate_id,
        "observations": len(scoped),
        "root_cause_counts": root_causes,
        "metric_averages": metric_averages,
        "historical_outcome_ids": [
            f'{item.get("problem_id")}:{index}'
            for index, item in enumerate(scoped, start=1)
        ],
        "note": "Derived reputation; historical outcome records remain immutable inputs.",
    }
