from __future__ import annotations

from copy import deepcopy
from typing import Any


STAGES = [
    "Q0_ENGINEERING_BASELINE",
    "Q1_DETERMINISTIC_DIAGNOSTIC",
    "Q2_HIDDEN_CASES",
    "Q3_TRANSFER",
    "Q4_POLYGON",
    "Q5_LIVE_RESEARCH",
    "Q6_SHADOW_PRODUCTION",
    "Q7_QUALIFICATION_BOARD",
    "Q8_CONTINUOUS_REQUALIFICATION",
]


def next_stage(current_stage: str) -> str | None:
    if current_stage not in STAGES:
        raise ValueError(f"Unknown qualification stage: {current_stage}")
    index = STAGES.index(current_stage)
    if index == len(STAGES) - 1:
        return None
    return STAGES[index + 1]


def evaluate_stage_result(
    *,
    current_stage: str,
    result: dict[str, Any],
    critical_failures: list[str] | None = None,
    training_gaps: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Convert stage evidence into a controlled development decision."""
    if current_stage not in STAGES:
        raise ValueError(f"Unknown qualification stage: {current_stage}")

    failures = list(critical_failures or [])
    gaps = deepcopy(training_gaps or [])
    verdict = str(result.get("verdict", "UNKNOWN")).upper()

    if failures:
        return {
            "current_stage": current_stage,
            "decision": "TRAIN_AND_RETEST",
            "next_stage": current_stage,
            "critical_failures": failures,
            "training_gaps": gaps,
            "promotion_allowed": False,
            "reason": "critical_failures_present",
        }

    if verdict not in {"PASS", "QUALIFIED_FOR_SCOPE", "QUALIFIED_WITH_LIMITS"}:
        return {
            "current_stage": current_stage,
            "decision": "TRAIN_AND_RETEST",
            "next_stage": current_stage,
            "critical_failures": failures,
            "training_gaps": gaps,
            "promotion_allowed": False,
            "reason": "stage_verdict_not_pass",
        }

    target = next_stage(current_stage)

    return {
        "current_stage": current_stage,
        "decision": "PROMOTE" if target else "MAINTAIN_REQUALIFICATION",
        "next_stage": target or current_stage,
        "critical_failures": [],
        "training_gaps": gaps,
        "promotion_allowed": target is not None,
        "reason": "stage_gate_passed",
    }


def build_development_plan(
    *,
    stage_decision: dict[str, Any],
) -> dict[str, Any]:
    """Create the next development action from a stage decision."""
    if stage_decision.get("decision") == "TRAIN_AND_RETEST":
        return {
            "action": "TARGETED_TRAINING",
            "target_stage": stage_decision.get("current_stage"),
            "inputs": deepcopy(stage_decision.get("training_gaps", [])),
            "required_outputs": [
                "root_cause_mapping",
                "learning_delta",
                "git_patch",
                "regression_test",
                "targeted_retest",
            ],
            "status": "DEVELOPMENT_REQUIRED",
        }

    if stage_decision.get("decision") == "PROMOTE":
        return {
            "action": "BUILD_NEXT_STAGE_TESTS",
            "target_stage": stage_decision.get("next_stage"),
            "inputs": [],
            "required_outputs": [
                "test_case_set",
                "acceptance_criteria",
                "independent_evaluation_path",
                "stage_gate",
            ],
            "status": "NEXT_STAGE_REQUIRED",
        }

    return {
        "action": "CONTINUOUS_REQUALIFICATION",
        "target_stage": stage_decision.get("current_stage"),
        "inputs": [],
        "required_outputs": [
            "change_monitoring",
            "incident_triggered_retest",
            "periodic_scope_requalification",
        ],
        "status": "MAINTENANCE",
    }
