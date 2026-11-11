import pytest

from ak01.problem_solving import (
    build_problem_signature,
    build_problem_solution_graph,
    register_candidate_method,
    validate_problem_solution_graph,
)
from ak01.timing import build_timing_budget, validate_timing_candidate


@pytest.mark.knowledge
def test_problem_signature_precedes_method_selection():
    signature = build_problem_signature(
        problem_id="PR1",
        statement="Choose a retrieval strategy",
        expected_output="Selected strategy with evidence",
        constraints={"latency_ms": 100},
        problem_class="RANKING",
    )

    candidate = register_candidate_method(
        problem_signature=signature,
        method_id="M1",
        method_name="Hybrid retrieval",
        method_family="retrieval",
        knowledge_ids=["K1"],
        metrics=["Recall@K", "NDCG"],
        failure_modes=["poor fusion weighting"],
        evidence_refs=["doi:example"],
    )

    graph = build_problem_solution_graph(
        problem_signature=signature,
        candidates=[candidate],
        qualified_knowledge_ids={"K1"},
    )

    assert validate_problem_solution_graph(graph) == []
    assert graph["selection_status"] == "READY_FOR_COMPARISON"
    assert graph["selected_candidate_id"] is None


@pytest.mark.knowledge
def test_unqualified_required_knowledge_blocks_candidate_readiness():
    signature = build_problem_signature(
        problem_id="PR2",
        statement="Diagnose service failure",
        expected_output="Root cause",
        problem_class="ROOT_CAUSE_ANALYSIS",
    )
    candidate = register_candidate_method(
        problem_signature=signature,
        method_id="M2",
        method_name="Fault-tree analysis",
        method_family="diagnostic",
        knowledge_ids=["K-FTA"],
        metrics=["diagnosis_accuracy"],
        failure_modes=["incomplete fault model"],
        evidence_refs=["standard:fta"],
    )

    graph = build_problem_solution_graph(
        problem_signature=signature,
        candidates=[candidate],
        qualified_knowledge_ids=set(),
    )

    readiness = graph["candidate_readiness"][0]
    assert readiness["ready_for_comparison"] is False
    assert "K-FTA" in readiness["missing_knowledge_ids"]
    assert graph["selection_status"] == "RESEARCH_OR_QUALIFICATION_REQUIRED"


@pytest.mark.knowledge
def test_missing_evidence_metrics_or_failure_modes_blocks_comparison():
    signature = build_problem_signature(
        problem_id="PR3",
        statement="Find a route",
        expected_output="Route",
        problem_class="PLANNING",
    )
    candidate = register_candidate_method(
        problem_signature=signature,
        method_id="M3",
        method_name="Candidate algorithm",
        method_family="graph_search",
        knowledge_ids=["K3"],
    )

    graph = build_problem_solution_graph(
        problem_signature=signature,
        candidates=[candidate],
        qualified_knowledge_ids={"K3"},
    )

    blockers = graph["candidate_readiness"][0]["blockers"]
    assert "missing_evidence" in blockers
    assert "missing_metrics" in blockers
    assert "missing_failure_modes" in blockers


@pytest.mark.knowledge
def test_timing_budget_detects_overallocation():
    budget = build_timing_budget(
        total_budget_ms=1000,
        stages=[
            {"name": "ASR", "budget_ms": 250},
            {"name": "LLM", "budget_ms": 500},
            {"name": "TTS", "budget_ms": 300},
        ],
    )

    assert budget["over_budget"] is True
    assert budget["remaining_ms"] == -50


@pytest.mark.knowledge
def test_timing_claim_requires_measurement_source():
    signature = build_problem_signature(
        problem_id="PR4",
        statement="Choose low-latency method",
        expected_output="Method",
    )
    candidate = register_candidate_method(
        problem_signature=signature,
        method_id="M4",
        method_name="Fast method",
        method_family="example",
        knowledge_ids=[],
        timing={"measured_latency_ms": 20},
    )

    result = validate_timing_candidate(candidate, required_latency_ms=50)

    assert result["within_budget"] is True
    assert result["timing_ready"] is False
    assert "missing_timing_evidence" in result["blockers"]
