import pytest

from ak01.professional_exam import (
    build_exam_spec,
    derive_training_gaps,
    evaluate_exam,
)


def _spec():
    return build_exam_spec(
        role_id="AK-01",
        target_level="ARCHITECT",
        tasks=[
            {
                "task_id": "T1",
                "label": "Choose a source for a professional claim",
                "exam_prompt": "Select and justify the evidence route",
                "exam_levels": ["E2_DECISION", "E4_FAILURE"],
                "critical": True,
            },
            {
                "task_id": "T2",
                "label": "Build an evidence-backed knowledge unit",
                "exam_prompt": "Produce a traceable knowledge unit",
                "exam_levels": ["E3_PROCEDURE", "E6_CAPSTONE"],
                "critical": True,
            },
        ],
        acceptance_criteria=[
            {
                "criterion_id": "C1",
                "task_id": "T1",
                "field": "source_qualified",
                "mode": "EQUALS",
                "expected": True,
                "weight": 2,
            },
            {
                "criterion_id": "C2",
                "task_id": "T1",
                "field": "counter_evidence_reviewed",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "C3",
                "task_id": "T2",
                "field": "provenance_complete",
                "mode": "EQUALS",
                "expected": True,
                "weight": 2,
            },
            {
                "criterion_id": "C4",
                "task_id": "T2",
                "field": "auto_qualified",
                "mode": "EQUALS",
                "expected": False,
                "weight": 2,
            },
        ],
    )


@pytest.mark.knowledge
def test_exam_spec_is_built_before_training_from_tasks():
    spec = _spec()

    assert spec["status"] == "EXAM_SPEC_READY"
    assert {case["level"] for case in spec["cases"]} == {
        "E2_DECISION",
        "E3_PROCEDURE",
        "E4_FAILURE",
        "E6_CAPSTONE",
    }


@pytest.mark.knowledge
def test_professional_exam_pass_is_diagnostic_not_production_qualification():
    spec = _spec()
    submissions = {
        case["case_id"]: (
            {
                "source_qualified": True,
                "counter_evidence_reviewed": True,
            }
            if case["task_id"] == "T1"
            else {
                "provenance_complete": True,
                "auto_qualified": False,
            }
        )
        for case in spec["cases"]
    }

    result = evaluate_exam(exam_spec=spec, submissions=submissions)

    assert result["verdict"] == "PASS"
    assert result["qualification_granted"] is False
    assert result["next_stage"] == "SHADOW_PRODUCTION"


@pytest.mark.knowledge
def test_critical_case_failure_blocks_exam_and_creates_training_gap():
    spec = _spec()
    submissions = {
        case["case_id"]: (
            {
                "source_qualified": False,
                "counter_evidence_reviewed": True,
            }
            if case["task_id"] == "T1"
            else {
                "provenance_complete": True,
                "auto_qualified": False,
            }
        )
        for case in spec["cases"]
    }

    result = evaluate_exam(exam_spec=spec, submissions=submissions)
    gaps = derive_training_gaps(result)

    assert result["verdict"] == "FAIL_DIAGNOSTIC"
    assert result["critical_failures"]
    assert any("C1" in item["failed_criteria"] for item in gaps)



@pytest.mark.knowledge
def test_numeric_exam_criterion_with_missing_threshold_fails_safely():
    spec = build_exam_spec(
        role_id="AK-01",
        target_level="ARCHITECT",
        tasks=[
            {
                "task_id": "TN",
                "label": "Meet latency target",
                "exam_levels": ["E2_DECISION"],
                "critical": True,
            }
        ],
        acceptance_criteria=[
            {
                "criterion_id": "CN",
                "task_id": "TN",
                "field": "latency_ms",
                "mode": "AT_MOST",
                "expected": None,
                "weight": 1,
            }
        ],
    )

    result = evaluate_exam(
        exam_spec=spec,
        submissions={"TN:E2_DECISION": {"latency_ms": 20}},
    )

    assert result["verdict"] == "FAIL_DIAGNOSTIC"
    assert result["case_results"][0]["criterion_results"][0]["passed"] is False
