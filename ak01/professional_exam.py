from __future__ import annotations

from copy import deepcopy
from typing import Any

EXAM_LEVELS = {
    "E1_KNOWLEDGE",
    "E2_DECISION",
    "E3_PROCEDURE",
    "E4_FAILURE",
    "E5_ADVERSARIAL",
    "E6_CAPSTONE",
}


def build_exam_spec(
    *,
    role_id: str,
    target_level: str,
    tasks: list[dict[str, Any]],
    acceptance_criteria: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build an exam before training from professional tasks and acceptance criteria."""
    cases: list[dict[str, Any]] = []

    for index, task in enumerate(tasks, start=1):
        task_id = str(task.get("task_id") or f"T{index}")
        task_levels = list(task.get("exam_levels") or ["E2_DECISION", "E3_PROCEDURE"])

        for level in task_levels:
            if level not in EXAM_LEVELS:
                raise ValueError(f"Unsupported exam level: {level}")
            cases.append({
                "case_id": f"{task_id}:{level}",
                "task_id": task_id,
                "level": level,
                "prompt": str(task.get("exam_prompt") or task.get("label") or task_id),
                "expected_output_contract": deepcopy(
                    task.get("expected_output_contract") or {}
                ),
                "required_evidence": list(task.get("required_evidence") or []),
                "critical": bool(task.get("critical", False)),
            })

    criteria_by_task: dict[str, list[dict[str, Any]]] = {}
    for criterion in acceptance_criteria:
        task_id = str(criterion.get("task_id") or "GLOBAL")
        criteria_by_task.setdefault(task_id, []).append(deepcopy(criterion))

    return {
        "role_id": role_id,
        "target_level": target_level,
        "cases": cases,
        "acceptance_criteria": criteria_by_task,
        "pass_policy": {
            "critical_case_min_score": 0.80,
            "overall_min_score": 0.75,
            "critical_case_failure_blocks_pass": True,
        },
        "status": "EXAM_SPEC_READY",
    }


def score_exam_case(
    *,
    case: dict[str, Any],
    submission: dict[str, Any],
    criteria: list[dict[str, Any]],
) -> dict[str, Any]:
    """Score a structured professional case without hidden subjective promotion."""
    if not criteria:
        return {
            "case_id": case.get("case_id"),
            "score": 0.0,
            "criterion_results": [],
            "critical": bool(case.get("critical")),
            "status": "UNSCORABLE_NO_CRITERIA",
        }

    results: list[dict[str, Any]] = []
    total_weight = 0.0
    weighted_score = 0.0

    for criterion in criteria:
        field = str(criterion.get("field") or "")
        weight = float(criterion.get("weight", 1.0))
        expected = criterion.get("expected")
        mode = str(criterion.get("mode", "EQUALS")).upper()
        actual = submission.get(field)

        passed = False
        if mode == "EQUALS":
            passed = actual == expected
        elif mode == "CONTAINS":
            if isinstance(actual, (list, tuple, set)):
                passed = expected in actual
            elif isinstance(actual, str):
                passed = str(expected) in actual
        elif mode == "NON_EMPTY":
            passed = bool(actual)
        elif mode in {"AT_LEAST", "AT_MOST"}:
            if actual is None or expected is None:
                passed = False
            else:
                actual_value = float(actual)
                expected_value = float(expected)
                passed = (
                    actual_value >= expected_value
                    if mode == "AT_LEAST"
                    else actual_value <= expected_value
                )
        else:
            raise ValueError(f"Unsupported scoring mode: {mode}")

        total_weight += weight
        if passed:
            weighted_score += weight

        results.append({
            "criterion_id": criterion.get("criterion_id"),
            "field": field,
            "passed": passed,
            "weight": weight,
            "actual": deepcopy(actual),
            "expected": deepcopy(expected),
        })

    score = weighted_score / total_weight if total_weight else 0.0

    return {
        "case_id": case.get("case_id"),
        "score": score,
        "criterion_results": results,
        "critical": bool(case.get("critical")),
        "status": "SCORED",
    }


def evaluate_exam(
    *,
    exam_spec: dict[str, Any],
    submissions: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Evaluate E1–E6 results and produce a diagnostic qualification decision."""
    all_results: list[dict[str, Any]] = []
    criteria_map = exam_spec.get("acceptance_criteria") or {}

    for case in exam_spec.get("cases", []):
        case_id = str(case.get("case_id"))
        task_id = str(case.get("task_id"))
        submission = submissions.get(case_id, {})
        criteria = list(criteria_map.get(task_id, [])) + list(
            criteria_map.get("GLOBAL", [])
        )
        all_results.append(
            score_exam_case(
                case=case,
                submission=submission,
                criteria=criteria,
            )
        )

    scored = [item for item in all_results if item.get("status") == "SCORED"]
    overall = (
        sum(float(item["score"]) for item in scored) / len(scored)
        if scored
        else 0.0
    )

    policy = exam_spec.get("pass_policy") or {}
    critical_min = float(policy.get("critical_case_min_score", 0.80))
    overall_min = float(policy.get("overall_min_score", 0.75))

    critical_failures = [
        item
        for item in scored
        if item.get("critical") and float(item.get("score", 0.0)) < critical_min
    ]

    passed = overall >= overall_min and not critical_failures

    return {
        "role_id": exam_spec.get("role_id"),
        "target_level": exam_spec.get("target_level"),
        "case_results": all_results,
        "overall_score": overall,
        "critical_failures": [item["case_id"] for item in critical_failures],
        "verdict": "PASS" if passed else "FAIL_DIAGNOSTIC",
        "qualification_granted": False,
        "next_stage": "SHADOW_PRODUCTION" if passed else "TRAINING_DELTA",
    }


def derive_training_gaps(exam_result: dict[str, Any]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []

    for case in exam_result.get("case_results", []):
        if case.get("status") != "SCORED":
            gaps.append({
                "case_id": case.get("case_id"),
                "gap_type": "UNSCORABLE",
                "failed_criteria": [],
            })
            continue

        failed = [
            item.get("criterion_id")
            for item in case.get("criterion_results", [])
            if item.get("passed") is not True
        ]
        if failed:
            gaps.append({
                "case_id": case.get("case_id"),
                "gap_type": "CRITERIA_FAILURE",
                "failed_criteria": failed,
                "score": case.get("score"),
            })

    return gaps
