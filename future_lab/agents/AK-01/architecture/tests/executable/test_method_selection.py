import pytest

from ak01.method_selection import compare_candidates, validate_selection_record


@pytest.mark.knowledge
def test_hard_latency_constraint_excludes_slow_candidate_before_scoring():
    candidates = [
        {"candidate_id": "A"},
        {"candidate_id": "B"},
    ]
    readiness = [
        {"candidate_id": "A", "ready_for_comparison": True},
        {"candidate_id": "B", "ready_for_comparison": True},
    ]
    criteria = [
        {"name": "quality", "weight": 1.0, "direction": "MAXIMIZE"},
        {"name": "latency_ms", "weight": 0.01, "direction": "MINIMIZE"},
    ]
    measurements = {
        "A": {"quality": 0.90, "latency_ms": 80},
        "B": {"quality": 0.99, "latency_ms": 300},
    }

    result = compare_candidates(
        candidates=candidates,
        readiness=readiness,
        criteria=criteria,
        measurements=measurements,
        hard_constraints=[
            {"metric": "latency_ms", "operator": "<=", "value": 100},
        ],
    )

    assert validate_selection_record(result) == []
    assert result["decision"] == "SELECTED"
    assert result["selected_candidate_id"] == "A"
    assert any(item["candidate_id"] == "B" for item in result["excluded_candidates"])


@pytest.mark.knowledge
def test_missing_measurement_blocks_candidate_instead_of_guessing():
    result = compare_candidates(
        candidates=[{"candidate_id": "A"}],
        readiness=[{"candidate_id": "A", "ready_for_comparison": True}],
        criteria=[
            {"name": "quality", "weight": 1.0, "direction": "MAXIMIZE"},
            {"name": "cost", "weight": 1.0, "direction": "MINIMIZE"},
        ],
        measurements={"A": {"quality": 0.9}},
    )

    assert result["decision"] == "NO_DECISION"
    assert result["selected_candidate_id"] is None
    assert "missing_measurement:cost" in result["excluded_candidates"][0]["reasons"]


@pytest.mark.knowledge
def test_unready_candidate_is_excluded():
    result = compare_candidates(
        candidates=[{"candidate_id": "A"}],
        readiness=[{"candidate_id": "A", "ready_for_comparison": False}],
        criteria=[{"name": "quality", "weight": 1.0, "direction": "MAXIMIZE"}],
        measurements={"A": {"quality": 1.0}},
    )

    assert result["decision"] == "NO_DECISION"
    assert "candidate_not_ready_for_comparison" in result["excluded_candidates"][0]["reasons"]


@pytest.mark.knowledge
def test_exact_tie_requires_more_evidence_or_policy():
    result = compare_candidates(
        candidates=[{"candidate_id": "A"}, {"candidate_id": "B"}],
        readiness=[
            {"candidate_id": "A", "ready_for_comparison": True},
            {"candidate_id": "B", "ready_for_comparison": True},
        ],
        criteria=[{"name": "quality", "weight": 1.0, "direction": "MAXIMIZE"}],
        measurements={
            "A": {"quality": 0.9},
            "B": {"quality": 0.9},
        },
    )

    assert result["decision"] == "NO_DECISION"
    assert result["reason"] == "comparison_tie_requires_additional_evidence_or_policy"


@pytest.mark.knowledge
def test_missing_hard_constraint_threshold_blocks_candidate_instead_of_crashing():
    result = compare_candidates(
        candidates=[{"candidate_id": "A"}],
        readiness=[{"candidate_id": "A", "ready_for_comparison": True}],
        criteria=[{"name": "quality", "weight": 1.0, "direction": "MAXIMIZE"}],
        measurements={"A": {"quality": 0.9, "latency_ms": 20}},
        hard_constraints=[
            {"metric": "latency_ms", "operator": "<="},
        ],
    )

    assert result["decision"] == "NO_DECISION"
    assert (
        "missing_hard_constraint_value:latency_ms"
        in result["excluded_candidates"][0]["reasons"]
    )
