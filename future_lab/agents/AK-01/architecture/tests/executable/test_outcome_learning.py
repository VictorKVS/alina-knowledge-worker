import pytest

from ak01.outcome_learning import (
    build_method_reputation,
    classify_root_cause,
    record_solution_outcome,
    route_learning_action,
)


def _selection():
    return {
        "decision": "SELECTED",
        "selected_candidate_id": "M1",
        "reason": "highest_weighted_score_after_hard_constraints",
    }


@pytest.mark.knowledge
def test_outcome_records_expected_actual_and_delta():
    outcome = record_solution_outcome(
        problem_id="P1",
        selection_record=_selection(),
        expected_metrics={"latency_ms": 50, "quality": 0.90},
        actual_metrics={"latency_ms": 70, "quality": 0.88},
    )

    assert outcome["metric_deltas"]["latency_ms"] == 20
    assert outcome["metric_deltas"]["quality"] == pytest.approx(-0.02)
    assert outcome["root_cause"] == "UNKNOWN"


@pytest.mark.knowledge
def test_root_cause_requires_evidence_and_routes_learning():
    outcome = record_solution_outcome(
        problem_id="P2",
        selection_record=_selection(),
        expected_metrics={"quality": 0.9},
        actual_metrics={"quality": 0.6},
    )

    with pytest.raises(ValueError):
        classify_root_cause(
            outcome,
            root_cause="K8_DECISION_RULE_INCORRECT",
            evidence=[],
        )

    classified = classify_root_cause(
        outcome,
        root_cause="K8_DECISION_RULE_INCORRECT",
        evidence=["Decision rule selected M1 despite violated applicability condition X"],
    )
    route = route_learning_action(classified)

    assert route["route"] == "DECISION_RULE_REVIEW"


@pytest.mark.knowledge
def test_method_reputation_is_derived_from_immutable_outcomes():
    first = classify_root_cause(
        record_solution_outcome(
            problem_id="P3",
            selection_record=_selection(),
            expected_metrics={"latency_ms": 50},
            actual_metrics={"latency_ms": 45},
        ),
        root_cause="METHOD_LIMITATION",
        evidence=["Observed limitation under context C1"],
    )
    second = classify_root_cause(
        record_solution_outcome(
            problem_id="P4",
            selection_record=_selection(),
            expected_metrics={"latency_ms": 50},
            actual_metrics={"latency_ms": 55},
        ),
        root_cause="EXTERNAL_DEPENDENCY",
        evidence=["Dependency response time increased"],
    )

    reputation = build_method_reputation("M1", [first, second])

    assert reputation["observations"] == 2
    assert reputation["metric_averages"]["latency_ms"] == 50
    assert reputation["root_cause_counts"]["METHOD_LIMITATION"] == 1
    assert reputation["root_cause_counts"]["EXTERNAL_DEPENDENCY"] == 1


@pytest.mark.knowledge
def test_outcome_cannot_be_recorded_without_selected_method():
    with pytest.raises(ValueError):
        record_solution_outcome(
            problem_id="P5",
            selection_record={
                "decision": "NO_DECISION",
                "selected_candidate_id": None,
            },
            expected_metrics={},
            actual_metrics={},
        )
