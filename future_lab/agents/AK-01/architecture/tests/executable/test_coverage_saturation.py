import pytest

from ak01.coverage_saturation import (
    assess_coverage,
    assess_saturation,
    validate_coverage_result,
)


@pytest.mark.knowledge
def test_missing_required_dimension_keeps_requirement_partial():
    result = assess_coverage(
        requirements=[
            {
                "requirement_id": "KR1",
                "required_dimensions": [
                    "concept",
                    "decision",
                    "limitation",
                ],
            }
        ],
        evidence_items=[
            {
                "evidence_id": "E1",
                "requirement_ids": ["KR1"],
                "dimensions": ["concept", "decision"],
            }
        ],
    )

    assert validate_coverage_result(result) == []
    assert result["all_requirements_covered"] is False
    assert result["coverage"]["KR1"]["missing_dimensions"] == ["limitation"]


@pytest.mark.knowledge
def test_complete_coverage_still_expands_when_alternative_missing():
    coverage = assess_coverage(
        requirements=[
            {
                "requirement_id": "KR1",
                "required_dimensions": ["concept", "decision"],
            }
        ],
        evidence_items=[
            {
                "evidence_id": "E1",
                "requirement_ids": ["KR1"],
                "dimensions": ["concept", "decision"],
            }
        ],
    )

    result = assess_saturation(
        coverage_result=coverage,
        iteration_history=[
            {"material_new_findings": 0},
            {"material_new_findings": 0},
        ],
        mandatory_alternatives_covered=False,
        material_contradictions_documented=True,
        failure_modes_covered=True,
    )

    assert result["decision"] == "EXPAND"
    assert result["reason"] == "material_alternatives_missing"


@pytest.mark.knowledge
def test_saturation_stops_only_after_full_coverage_and_two_stable_iterations():
    coverage = assess_coverage(
        requirements=[
            {
                "requirement_id": "KR1",
                "required_dimensions": [
                    "concept",
                    "decision",
                    "limitation",
                    "contradiction",
                    "practice",
                    "evaluation",
                ],
            }
        ],
        evidence_items=[
            {
                "evidence_id": "E1",
                "requirement_ids": ["KR1"],
                "dimensions": [
                    "concept",
                    "decision",
                    "limitation",
                    "contradiction",
                    "practice",
                    "evaluation",
                ],
            }
        ],
    )

    result = assess_saturation(
        coverage_result=coverage,
        iteration_history=[
            {"material_new_findings": 0},
            {"material_new_findings": 0},
        ],
        mandatory_alternatives_covered=True,
        material_contradictions_documented=True,
        failure_modes_covered=True,
    )

    assert result["decision"] == "STOP"
    assert (
        result["reason"]
        == "mandatory_coverage_complete_and_recent_iterations_saturated"
    )
