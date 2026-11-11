import pytest

from ak01.factory_line import (
    close_run_with_learning,
    execute_source_discovery,
    prepare_knowledge_acquisition_run,
    qualify_candidate_into_knowledge,
    solve_with_qualified_knowledge,
)
from ak01.source_adapters import FixtureSourceAdapter


def _criteria():
    return {
        "provenance_complete": True,
        "evidence_sufficient": True,
        "limitations_explicit": True,
        "counter_evidence_reviewed": True,
        "tests_present": True,
    }


@pytest.mark.knowledge
def test_orchestrator_stops_at_discovery_before_sources_exist():
    run = prepare_knowledge_acquisition_run(
        work_object={
            "id": "ORCH-1",
            "goal": "Choose retrieval strategy",
            "tasks": [
                {
                    "label": "Select retrieval strategy",
                    "decisions": ["sparse vs dense vs hybrid"],
                }
            ],
        },
        constraints={"latency_ms": 100},
    )

    assert run["status"] == "WAITING_FOR_SOURCE_CANDIDATES"
    assert run["next_required_stage"] == "SOURCE_DISCOVERY_EXECUTION"
    assert [stage["stage"] for stage in run["stages"]] == [
        "WORK_DECOMPOSITION",
        "RESEARCH_PLANNING",
        "SOURCE_DISCOVERY_PLANNING",
    ]


@pytest.mark.knowledge
def test_orchestrator_blocks_rejected_source_without_downstream_fabrication():
    run = prepare_knowledge_acquisition_run(
        work_object={
            "id": "ORCH-2",
            "goal": "Choose method",
            "tasks": ["Choose method"],
        }
    )

    blocked = qualify_candidate_into_knowledge(
        run=run,
        candidate={
            "title": "Bad Source",
            "source_type": "paper",
            "authors_or_issuer": ["Unknown"],
            "publication_or_version_date": "2025",
            "persistent_identifier_or_official_locator": "doi:bad",
            "integrity_status": "RETRACTED",
            "methodology": "test",
            "claim_fit": "HIGH",
            "authority": "SCIENTIFIC_PRIMARY",
            "limitations": [],
        },
        intended_claim="Method A works",
        fragment={
            "fragment_id": "F1",
            "locator": "p1",
            "text": "Method A works",
        },
        claim_id="C1",
        knowledge_id="K1",
        knowledge_type="METHOD",
        knowledge_title="Method A",
        relation="SUPPORTS",
        rationale="Direct statement",
        reviewer_id="AQ-01",
        reviewer_role="Evaluator",
        qualification_criteria=_criteria(),
    )

    assert blocked["status"] == "BLOCKED_BY_SOURCE_QUALIFICATION"
    assert "knowledge_unit" not in blocked


@pytest.mark.knowledge
def test_orchestrator_runs_to_delta_when_all_gates_pass():
    run = prepare_knowledge_acquisition_run(
        work_object={
            "id": "ORCH-3",
            "goal": "Choose retrieval strategy",
            "tasks": [
                {
                    "label": "Select retrieval strategy",
                    "decisions": ["sparse vs dense vs hybrid"],
                }
            ],
        },
        constraints={"latency_ms": 100},
    )

    run = qualify_candidate_into_knowledge(
        run=run,
        candidate={
            "title": "Retrieval Study",
            "source_type": "scientific_synthesis",
            "authors_or_issuer": ["Research Group"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "doi:good",
            "integrity_status": "CURRENT",
            "methodology": "comparative evaluation",
            "claim_fit": "HIGH",
            "authority": "SCIENTIFIC_SYNTHESIS",
            "limitations": ["Corpus dependent"],
        },
        intended_claim="Hybrid retrieval is useful for mixed lexical and semantic matching",
        fragment={
            "fragment_id": "F1",
            "locator": "section 4",
            "text": "Hybrid retrieval combines lexical and semantic signals.",
        },
        claim_id="C1",
        knowledge_id="K1",
        knowledge_type="DECISION_RULE",
        knowledge_title="Hybrid retrieval candidate rule",
        relation="SUPPORTS",
        rationale="Direct support",
        reviewer_id="AQ-01",
        reviewer_role="Independent Evaluator",
        qualification_criteria=_criteria(),
        decision_rules=["Consider hybrid when lexical and semantic signals matter"],
        failure_modes=["Fusion weighting sensitivity"],
        tests=["Representative query benchmark"],
    )
    assert run["status"] == "QUALIFIED_KNOWLEDGE_READY"

    run = solve_with_qualified_knowledge(
        run=run,
        problem_spec={
            "problem_id": "P1",
            "statement": "Choose retrieval method",
            "expected_output": "Selected method",
            "constraints": {"latency_ms": 100},
            "problem_class": "RANKING",
        },
        method_specs=[
            {
                "method_id": "M1",
                "method_name": "Hybrid retrieval",
                "method_family": "retrieval",
                "knowledge_ids": ["K1"],
                "metrics": ["quality", "latency_ms"],
                "timing": {
                    "measured_latency_ms": 80,
                    "measurement_source": "benchmark:1",
                },
                "failure_modes": ["Fusion weighting sensitivity"],
                "evidence_refs": ["doi:good"],
            }
        ],
        criteria=[
            {"name": "quality", "weight": 1.0, "direction": "MAXIMIZE"},
            {"name": "latency_ms", "weight": 0.01, "direction": "MINIMIZE"},
        ],
        measurements={"M1": {"quality": 0.9, "latency_ms": 80}},
        hard_constraints=[
            {"metric": "latency_ms", "operator": "<=", "value": 100},
        ],
    )
    assert run["status"] == "METHOD_SELECTED"

    run = close_run_with_learning(
        run=run,
        expected_metrics={"quality": 0.9, "latency_ms": 80},
        actual_metrics={"quality": 0.7, "latency_ms": 82},
        root_cause="K8_DECISION_RULE_INCORRECT",
        root_cause_evidence=["Applicability condition was incomplete"],
        affected_artifacts=["decision-rule:hybrid-selection"],
        proposed_change="Add corpus/query distribution condition",
        regression_case="Changed query distribution must trigger reconsideration",
    )

    assert run["status"] == "LEARNING_DELTA_REQUIRED"
    assert run["learning_delta"]["regression_required"] is True
    assert run["learning_delta"]["requalification_required"] is True



@pytest.mark.knowledge
def test_orchestrator_executes_discovery_through_adapter():
    run = prepare_knowledge_acquisition_run(
        work_object={
            "id": "ORCH-DISCOVERY-1",
            "goal": "Choose hybrid retrieval method",
            "tasks": ["hybrid retrieval"],
        }
    )
    adapter = FixtureSourceAdapter([
        {
            "title": "Hybrid Retrieval Evidence",
            "abstract": "hybrid retrieval evidence",
            "match_queries": ["hybrid retrieval"],
            "source_type": "primary_research",
            "authors_or_issuer": ["Researcher"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "doi:10.example/discovery",
        }
    ])

    result = execute_source_discovery(
        run=run,
        adapter=adapter,
        per_query_limit=3,
    )

    assert result["status"] == "SOURCE_CANDIDATES_READY"
    assert result["next_required_stage"] == "SOURCE_QUALIFICATION"
    assert result["source_candidates"]
    assert result["source_candidates"][0]["discovery_channel"] == "fixture"


@pytest.mark.knowledge
def test_orchestrator_stops_when_adapter_returns_no_candidates():
    run = prepare_knowledge_acquisition_run(
        work_object={
            "id": "ORCH-DISCOVERY-2",
            "goal": "Find unknown method",
            "tasks": ["unknown method"],
        }
    )
    adapter = FixtureSourceAdapter([])

    result = execute_source_discovery(
        run=run,
        adapter=adapter,
    )

    assert result["status"] == "WAITING_FOR_SOURCE_CANDIDATES"
    assert result["next_required_stage"] == "SOURCE_DISCOVERY_EXECUTION"



@pytest.mark.knowledge
def test_orchestrator_deduplicates_same_source_across_discovery_records():
    run = prepare_knowledge_acquisition_run(
        work_object={
            "id": "ORCH-DISCOVERY-DEDUP",
            "goal": "hybrid retrieval",
            "tasks": ["hybrid retrieval"],
        }
    )
    adapter = FixtureSourceAdapter([
        {
            "title": "Hybrid Retrieval Study",
            "abstract": "hybrid retrieval",
            "match_queries": ["hybrid retrieval"],
            "source_type": "primary_research",
            "authors_or_issuer": ["Researcher A"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "https://doi.org/10.1000/x",
            "discovery_channel": "fixture-a",
        },
        {
            "title": "Hybrid Retrieval Study",
            "abstract": "hybrid retrieval",
            "match_queries": ["hybrid retrieval"],
            "source_type": "primary_research",
            "authors_or_issuer": ["Researcher A", "Researcher B"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "doi:10.1000/X",
            "discovery_channel": "fixture-b",
        },
    ])

    result = execute_source_discovery(
        run=run,
        adapter=adapter,
        per_query_limit=10,
    )

    assert result["status"] == "SOURCE_CANDIDATES_READY"
    assert result["source_registry"]["input_count"] >= 2
    assert result["source_registry"]["unique_count"] == 1
    assert result["source_registry"]["duplicate_count"] >= 1
    assert len(result["source_candidates_unique"]) == 1
