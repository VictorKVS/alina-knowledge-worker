import pytest

from ak01.development_controller import (
    build_development_plan,
    evaluate_stage_result,
    next_stage,
)


@pytest.mark.knowledge
def test_q1_pass_promotes_to_hidden_cases_not_production():
    decision = evaluate_stage_result(
        current_stage="Q1_DETERMINISTIC_DIAGNOSTIC",
        result={"verdict": "PASS"},
        critical_failures=[],
        training_gaps=[],
    )

    assert decision["decision"] == "PROMOTE"
    assert decision["next_stage"] == "Q2_HIDDEN_CASES"
    assert decision["promotion_allowed"] is True

    plan = build_development_plan(stage_decision=decision)

    assert plan["action"] == "BUILD_NEXT_STAGE_TESTS"
    assert plan["target_stage"] == "Q2_HIDDEN_CASES"


@pytest.mark.knowledge
def test_critical_failure_routes_to_training_and_same_stage_retest():
    decision = evaluate_stage_result(
        current_stage="Q4_POLYGON",
        result={"verdict": "FAIL"},
        critical_failures=["prompt_injection_override"],
        training_gaps=[
            {
                "case_id": "P-17",
                "failed_criteria": ["evidence_policy_preserved"],
            }
        ],
    )

    assert decision["decision"] == "TRAIN_AND_RETEST"
    assert decision["next_stage"] == "Q4_POLYGON"
    assert decision["promotion_allowed"] is False

    plan = build_development_plan(stage_decision=decision)

    assert plan["action"] == "TARGETED_TRAINING"
    assert "regression_test" in plan["required_outputs"]
    assert "targeted_retest" in plan["required_outputs"]


@pytest.mark.knowledge
def test_stage_order_is_explicit():
    assert next_stage("Q2_HIDDEN_CASES") == "Q3_TRANSFER"
    assert next_stage("Q6_SHADOW_PRODUCTION") == "Q7_QUALIFICATION_BOARD"
    assert next_stage("Q8_CONTINUOUS_REQUALIFICATION") is None
