import pytest

from ak01.research_planning import build_research_plan, plans_for_trace
from ak01.work_analysis import decompose_work


@pytest.mark.knowledge
def test_missing_method_becomes_traced_research_task_without_solution():
    trace = decompose_work({
        "id": "CASE-R1",
        "goal": "Search a professional knowledge base",
        "tasks": ["Retrieve relevant evidence"],
    })
    finding = next(item for item in trace["findings"] if item["type"] == "MISSING_METHOD")

    plan = build_research_plan(trace, finding)

    assert plan["derived_from"]["trace_id"] == trace["trace_id"]
    assert plan["derived_from"]["node_id"] == finding["node_id"]
    assert plan["selection_prohibited"] is True
    assert plan["status"] == "RESEARCH_REQUIRED"
    assert "candidate_method_or_algorithm_families" in plan["required_outputs"]


@pytest.mark.knowledge
def test_decision_rule_research_requires_criteria_alternatives_and_contradictions():
    trace = decompose_work({
        "id": "CASE-R2",
        "goal": "Choose retrieval strategy",
        "tasks": [{
            "label": "Select retrieval strategy",
            "decisions": ["sparse vs dense vs hybrid"],
        }],
    })

    plans = plans_for_trace(trace)
    plan = next(
        item
        for item in plans
        if item["derived_from"]["finding_type"] == "MISSING_DECISION_RULE"
    )

    joined_questions = " ".join(plan["research_questions"]).lower()
    assert "criteria" in joined_questions
    assert "competing" in joined_questions
    assert "escalated" in joined_questions
    assert "material alternatives are represented" in plan["stop_conditions"]
    assert "material contradictions are documented" in plan["stop_conditions"]


@pytest.mark.knowledge
def test_algorithm_gap_requests_complexity_benchmarks_and_failure_modes():
    trace = {
        "trace_id": "CASE-R3:TRACE",
        "nodes": [{
            "id": "T1",
            "type": "TASK",
            "label": "Find shortest feasible route",
            "derived_from": ["CASE-R3"],
            "rationale": "Declared task",
            "confidence": "HIGH",
            "status": "DRAFT",
        }],
        "findings": [{
            "type": "MISSING_ALGORITHM",
            "node_id": "T1",
            "message": "No algorithm selected.",
        }],
    }

    plan = plans_for_trace(trace)[0]

    text = " ".join(plan["research_questions"]).lower()
    assert "complexity" in text
    assert "benchmarks" in text
    assert "failure modes" in text
    assert "benchmark" in plan["source_mix"]
