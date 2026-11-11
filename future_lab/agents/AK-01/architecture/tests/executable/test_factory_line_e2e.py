import pytest

from ak01.claim_evidence import build_evidence_link, summarize_claim_evidence
from ak01.knowledge_qualification import apply_qualification, qualify_knowledge_unit
from ak01.knowledge_unit_builder import build_knowledge_unit
from ak01.method_selection import compare_candidates
from ak01.outcome_learning import (
    classify_root_cause,
    record_solution_outcome,
    route_learning_action,
)
from ak01.problem_solving import (
    build_problem_signature,
    build_problem_solution_graph,
    register_candidate_method,
)
from ak01.professional_graph import build_professional_graph
from ak01.research_planning import build_research_plan
from ak01.runtime_policy import evaluate_runtime_access
from ak01.source_discovery import build_source_discovery_plan
from ak01.source_qualification import assess_source
from ak01.work_analysis import decompose_work


@pytest.mark.knowledge
def test_first_complete_father_factory_line():
    trace = decompose_work({
        "id": "E2E-001",
        "goal": "Choose a retrieval strategy under latency constraint",
        "tasks": [
            {
                "label": "Select retrieval strategy",
                "decisions": ["sparse vs dense vs hybrid"],
            }
        ],
    })

    finding = next(
        item
        for item in trace["findings"]
        if item["type"] == "MISSING_DECISION_RULE"
    )
    research_plan = build_research_plan(
        trace,
        finding,
        constraints={"latency_ms": 100},
    )
    assert research_plan["selection_prohibited"] is True

    discovery_plan = build_source_discovery_plan(research_plan)
    assert (
        discovery_plan["seed_source_policy"][
            "qualification_required_before_acceptance"
        ]
        is True
    )

    source_assessment = assess_source(
        {
            "title": "Retrieval Evaluation Reference",
            "source_type": "scientific_synthesis",
            "authors_or_issuer": ["Independent Research Group"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "doi:10.example/retrieval",
            "integrity_status": "CURRENT",
            "methodology": "comparative evaluation",
            "claim_fit": "HIGH",
            "authority": "SCIENTIFIC_SYNTHESIS",
            "limitations": ["Results depend on corpus and query distribution"],
        },
        intended_claim="Hybrid retrieval is a candidate when lexical and semantic signals matter",
    )
    assert source_assessment["ingestion_allowed"] is True

    evidence_link = build_evidence_link(
        claim_id="C-RETRIEVAL-1",
        claim_text="Hybrid retrieval is a candidate when lexical and semantic signals matter",
        source_assessment=source_assessment,
        fragment={
            "fragment_id": "F-1",
            "locator": "section 4",
            "text": "Hybrid retrieval combines lexical and semantic signals.",
        },
        relation="SUPPORTS",
        rationale="The source directly describes the combined retrieval mechanism.",
    )

    claim_summary = summarize_claim_evidence(
        "C-RETRIEVAL-1",
        [evidence_link],
    )
    assert claim_summary["auto_qualified"] is False

    unit = build_knowledge_unit(
        knowledge_id="K-RETRIEVAL-1",
        knowledge_type="DECISION_RULE",
        title="Hybrid retrieval candidate rule",
        claim_summary=claim_summary,
        evidence_links=[evidence_link],
        decision_rules=[
            "Consider hybrid retrieval when both exact lexical and semantic matching matter"
        ],
        failure_modes=["Fusion weighting may degrade ranking quality"],
        tests=["Compare against sparse and dense baselines on representative queries"],
    )
    assert unit["state"] == "VERIFIED_NOT_QUALIFIED"

    qualification_record = qualify_knowledge_unit(
        unit,
        reviewer_id="AQ-01",
        reviewer_role="Independent Knowledge Evaluator",
        criteria={
            "provenance_complete": True,
            "evidence_sufficient": True,
            "limitations_explicit": True,
            "counter_evidence_reviewed": True,
            "tests_present": True,
        },
    )
    qualified_unit = apply_qualification(unit, qualification_record)
    assert qualified_unit["state"] == "QUALIFIED"

    professional_graph = build_professional_graph(
        work_trace=trace,
        qualified_units=[qualified_unit],
        bindings=[
            {
                "work_node_id": "T1.D1",
                "knowledge_id": "K-RETRIEVAL-1",
            }
        ],
    )
    assert "K-RETRIEVAL-1" in professional_graph["runtime_eligible_knowledge"]
    assert evaluate_runtime_access(qualified_unit)["decision"] == "ALLOW"

    problem = build_problem_signature(
        problem_id="P-RETRIEVAL-1",
        statement="Choose retrieval method for mixed lexical/semantic search",
        expected_output="Selected method with traceable rationale",
        constraints={"latency_ms": 100},
        problem_class="RANKING",
    )

    hybrid = register_candidate_method(
        problem_signature=problem,
        method_id="M-HYBRID",
        method_name="Hybrid retrieval",
        method_family="retrieval",
        knowledge_ids=["K-RETRIEVAL-1"],
        applicability=["mixed lexical and semantic matching"],
        metrics=["quality", "latency_ms"],
        timing={
            "measured_latency_ms": 80,
            "measurement_source": "benchmark:E2E-001",
        },
        failure_modes=["fusion weighting sensitivity"],
        evidence_refs=["doi:10.example/retrieval"],
    )

    graph = build_problem_solution_graph(
        problem_signature=problem,
        candidates=[hybrid],
        qualified_knowledge_ids={"K-RETRIEVAL-1"},
    )
    assert graph["selection_status"] == "READY_FOR_COMPARISON"

    selection = compare_candidates(
        candidates=[hybrid],
        readiness=graph["candidate_readiness"],
        criteria=[
            {"name": "quality", "weight": 1.0, "direction": "MAXIMIZE"},
            {"name": "latency_ms", "weight": 0.01, "direction": "MINIMIZE"},
        ],
        measurements={
            "M-HYBRID": {
                "quality": 0.92,
                "latency_ms": 80,
            }
        },
        hard_constraints=[
            {"metric": "latency_ms", "operator": "<=", "value": 100},
        ],
    )
    assert selection["decision"] == "SELECTED"
    assert selection["selected_candidate_id"] == "M-HYBRID"

    outcome = record_solution_outcome(
        problem_id="P-RETRIEVAL-1",
        selection_record=selection,
        expected_metrics={"quality": 0.92, "latency_ms": 80},
        actual_metrics={"quality": 0.75, "latency_ms": 82},
        context={"query_distribution": "changed"},
    )

    classified = classify_root_cause(
        outcome,
        root_cause="K8_DECISION_RULE_INCORRECT",
        evidence=[
            "Observed query distribution violated the decision rule assumptions"
        ],
    )
    learning = route_learning_action(classified)

    assert learning["route"] == "DECISION_RULE_REVIEW"
    assert learning["status"] == "LEARNING_ACTION_REQUIRED"
