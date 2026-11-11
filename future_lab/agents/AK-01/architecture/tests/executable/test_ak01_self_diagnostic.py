import pytest

from ak01.self_diagnostic import run_ak01_self_diagnostic


@pytest.mark.knowledge
def test_ak01_first_professional_diagnostic_exam_executes_e1_to_e6():
    result = run_ak01_self_diagnostic()

    levels = {
        case["case_id"].split(":", 1)[1]
        for case in result["case_results"]
    }

    assert levels == {
        "E1_KNOWLEDGE",
        "E2_DECISION",
        "E3_PROCEDURE",
        "E4_FAILURE",
        "E5_ADVERSARIAL",
        "E6_CAPSTONE",
    }
    assert result["exam_spec_status"] == "EXAM_SPEC_READY"
    assert result["qualification_granted"] is False


@pytest.mark.knowledge
def test_ak01_current_deterministic_scope_passes_first_diagnostic():
    result = run_ak01_self_diagnostic()

    assert result["verdict"] == "PASS"
    assert result["overall_score"] == pytest.approx(1.0)
    assert result["critical_failures"] == []
    assert result["training_gaps"] == []
    assert result["next_stage"] == "SHADOW_PRODUCTION"
