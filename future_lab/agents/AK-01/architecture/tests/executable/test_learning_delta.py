import pytest

from ak01.learning_delta import (
    mark_delta_applied,
    propose_learning_delta,
    validate_learning_delta,
)


@pytest.mark.knowledge
def test_decision_rule_failure_generates_requalification_delta():
    action = {
        "problem_id": "P1",
        "candidate_id": "M1",
        "root_cause": "K8_DECISION_RULE_INCORRECT",
        "route": "DECISION_RULE_REVIEW",
        "evidence": ["Rule failed under condition X"],
    }

    delta = propose_learning_delta(
        learning_action=action,
        affected_artifacts=["decision-rule:retrieval-selection"],
        proposed_change="Add condition X to applicability guard",
        regression_case="Condition X must block method M1",
    )

    assert validate_learning_delta(delta) == []
    assert delta["target"] == "DECISION_RULE"
    assert delta["regression_required"] is True
    assert delta["requalification_required"] is True


@pytest.mark.knowledge
def test_applied_delta_requires_git_commit_and_regression_test():
    action = {
        "problem_id": "P2",
        "candidate_id": "M2",
        "root_cause": "K5_PROCEDURE_MISSING",
        "route": "PROCEDURE_AUTHORING",
        "evidence": ["Missing recovery step"],
    }
    delta = propose_learning_delta(
        learning_action=action,
        affected_artifacts=["procedure:recovery"],
        proposed_change="Add recovery verification step",
        regression_case="Recovery workflow verifies restored state",
    )

    with pytest.raises(ValueError):
        mark_delta_applied(
            delta,
            commit_sha="",
            regression_test_id="test_recovery",
        )

    applied = mark_delta_applied(
        delta,
        commit_sha="abc123",
        regression_test_id="test_recovery",
    )

    assert validate_learning_delta(applied) == []
    assert applied["status"] == "APPLIED_PENDING_VALIDATION"
    assert applied["commit_sha"] == "abc123"


@pytest.mark.knowledge
def test_unknown_learning_route_cannot_create_silent_delta():
    with pytest.raises(ValueError):
        propose_learning_delta(
            learning_action={
                "problem_id": "P3",
                "candidate_id": "M3",
                "root_cause": "UNKNOWN",
                "route": "UNSUPPORTED_ROUTE",
                "evidence": ["unknown"],
            },
            affected_artifacts=["x"],
            proposed_change="change",
            regression_case="case",
        )
