from __future__ import annotations

from copy import deepcopy
from typing import Any

DELTA_TARGETS = {
    "KNOWLEDGE",
    "RAG",
    "PROCEDURE",
    "CHECKLIST",
    "DECISION_RULE",
    "PROMPT_POLICY",
    "TOOL_SKILL",
    "LOCAL_KNOWLEDGE",
    "AGENT_ARCHITECTURE",
    "METHOD",
    "INPUT_CONTRACT",
    "DEPENDENCY_RESILIENCE",
}


_ROUTE_TO_TARGET = {
    "KNOWLEDGE_ACQUISITION": "KNOWLEDGE",
    "KNOWLEDGE_REFRESH": "KNOWLEDGE",
    "KNOWLEDGE_REVIEW": "KNOWLEDGE",
    "RAG_RETRIEVAL_REVIEW": "RAG",
    "PROCEDURE_AUTHORING": "PROCEDURE",
    "PROCEDURE_REVIEW": "PROCEDURE",
    "CHECKLIST_REVIEW": "CHECKLIST",
    "DECISION_RULE_REVIEW": "DECISION_RULE",
    "PROMPT_POLICY_REVIEW": "PROMPT_POLICY",
    "TOOL_TRAINING": "TOOL_SKILL",
    "LOCAL_KNOWLEDGE_DELTA": "LOCAL_KNOWLEDGE",
    "AGENT_ARCHITECTURE_REVIEW": "AGENT_ARCHITECTURE",
    "METHOD_REVIEW": "METHOD",
    "INPUT_CONTRACT_REVIEW": "INPUT_CONTRACT",
    "DEPENDENCY_RESILIENCE_REVIEW": "DEPENDENCY_RESILIENCE",
}


def propose_learning_delta(
    *,
    learning_action: dict[str, Any],
    affected_artifacts: list[str],
    proposed_change: str,
    regression_case: str,
) -> dict[str, Any]:
    route = str(learning_action.get("route", ""))
    target = _ROUTE_TO_TARGET.get(route)

    if target not in DELTA_TARGETS:
        raise ValueError(f"Unsupported learning route: {route}")
    if not affected_artifacts:
        raise ValueError("Learning delta requires affected artifacts")
    if not regression_case:
        raise ValueError("Learning delta requires a regression case")

    requalification_required = target in {
        "KNOWLEDGE",
        "DECISION_RULE",
        "METHOD",
        "AGENT_ARCHITECTURE",
        "PROCEDURE",
        "CHECKLIST",
        "PROMPT_POLICY",
        "TOOL_SKILL",
        "LOCAL_KNOWLEDGE",
    }

    return {
        "problem_id": learning_action.get("problem_id"),
        "candidate_id": learning_action.get("candidate_id"),
        "root_cause": learning_action.get("root_cause"),
        "route": route,
        "target": target,
        "affected_artifacts": list(affected_artifacts),
        "proposed_change": proposed_change,
        "regression_case": regression_case,
        "source_evidence": deepcopy(learning_action.get("evidence", [])),
        "status": "PROPOSED",
        "regression_required": True,
        "requalification_required": requalification_required,
        "applied": False,
    }


def mark_delta_applied(
    delta: dict[str, Any],
    *,
    commit_sha: str,
    regression_test_id: str,
) -> dict[str, Any]:
    if not commit_sha:
        raise ValueError("Applied delta requires commit SHA")
    if not regression_test_id:
        raise ValueError("Applied delta requires regression test ID")

    updated = deepcopy(delta)
    updated["status"] = "APPLIED_PENDING_VALIDATION"
    updated["applied"] = True
    updated["commit_sha"] = commit_sha
    updated["regression_test_id"] = regression_test_id
    return updated


def validate_learning_delta(delta: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if delta.get("target") not in DELTA_TARGETS:
        errors.append("invalid_delta_target")
    if not delta.get("affected_artifacts"):
        errors.append("missing_affected_artifacts")
    if delta.get("regression_required") is not True:
        errors.append("regression_requirement_missing")
    if not delta.get("regression_case"):
        errors.append("missing_regression_case")
    if delta.get("applied") is True:
        if not delta.get("commit_sha"):
            errors.append("applied_delta_missing_commit")
        if not delta.get("regression_test_id"):
            errors.append("applied_delta_missing_regression_test")

    return errors
