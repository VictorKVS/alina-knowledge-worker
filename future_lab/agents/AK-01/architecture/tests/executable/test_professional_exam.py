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
