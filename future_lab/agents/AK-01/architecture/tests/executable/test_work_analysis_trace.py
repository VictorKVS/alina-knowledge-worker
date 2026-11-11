import pytest

from ak01.work_analysis import decompose_work, find_problems, validate_trace


@pytest.mark.knowledge
def test_work_decomposition_preserves_derivation_and_rationale():
    trace = decompose_work({
        "id": "CASE-001",
        "goal": "Prepare a security compliance conclusion",
        "tasks": [
            {
                "label": "Determine applicable requirements",
                "decisions": ["Which regulatory requirements apply?"],
            }
        ],
    })

    assert validate_trace(trace) == []
    assert trace["nodes"]
    for node in trace["nodes"]:
        assert node["derived_from"]
        assert node["rationale"]


@pytest.mark.knowledge
def test_unknown_decision_rule_is_reported_not_invented():
    trace = decompose_work({
        "id": "CASE-002",
        "goal": "Choose a retrieval method",
        "tasks": [
            {
                "label": "Select retrieval strategy",
                "decisions": ["sparse vs dense vs hybrid"],
            }
        ],
    })

    problem_types = {x["type"] for x in trace["findings"]}
    assert "MISSING_DECISION_RULE" in problem_types

    result = find_problems(trace)
    assert result["valid_trace"] is True
    assert result["ready_for_promotion"] is False


@pytest.mark.knowledge
def test_explicit_method_is_traced_without_claiming_qualification():
    trace = decompose_work({
        "id": "CASE-003",
        "goal": "Search documents",
        "tasks": [
            {
                "label": "Retrieve candidate documents",
                "method": "hybrid retrieval",
            }
        ],
    })

    method_nodes = [n for n in trace["nodes"] if n["type"] == "METHOD"]
    assert len(method_nodes) == 1
    assert method_nodes[0]["label"] == "hybrid retrieval"
    assert method_nodes[0]["status"] == "DRAFT"
