from __future__ import annotations

from typing import Any

from .claim_evidence import build_evidence_link, summarize_claim_evidence
from .factory_line import (
    close_run_with_learning,
    prepare_knowledge_acquisition_run,
    qualify_candidate_into_knowledge,
    solve_with_qualified_knowledge,
)
from .knowledge_qualification import apply_qualification, qualify_knowledge_unit
from .knowledge_unit_builder import build_knowledge_unit
from .metadata_review import review_metadata_conflicts
from .method_selection import compare_candidates
from .outcome_learning import (
    classify_root_cause,
    record_solution_outcome,
    route_learning_action,
)
from .professional_exam import build_exam_spec, derive_training_gaps, evaluate_exam
from .source_qualification import assess_source


def build_ak01_self_exam_spec() -> dict[str, Any]:
    return build_exam_spec(
        role_id="AK-01",
        target_level="ARCHITECT",
        tasks=[
            {
                "task_id": "E1",
                "label": "Respect epistemic and qualification boundaries",
                "exam_prompt": "Show that discovery/support does not equal qualification",
                "exam_levels": ["E1_KNOWLEDGE"],
                "critical": True,
            },
            {
                "task_id": "E2",
                "label": "Choose evidence route",
                "exam_prompt": "Assess a source candidate without silent trust promotion",
                "exam_levels": ["E2_DECISION"],
                "critical": True,
            },
            {
                "task_id": "E3",
                "label": "Assemble professional knowledge",
                "exam_prompt": "Build and externally qualify a traceable knowledge unit",
                "exam_levels": ["E3_PROCEDURE"],
                "critical": True,
            },
            {
                "task_id": "E4",
                "label": "Diagnose failed professional outcome",
                "exam_prompt": "Classify root cause and route correction",
                "exam_levels": ["E4_FAILURE"],
                "critical": True,
            },
            {
                "task_id": "E5",
                "label": "Handle adversarial ambiguity",
                "exam_prompt": "Quarantine conflicting metadata and refuse incomplete decisions",
                "exam_levels": ["E5_ADVERSARIAL"],
                "critical": True,
            },
            {
                "task_id": "E6",
                "label": "Run end-to-end professional factory case",
                "exam_prompt": "From work object to selected method and learning delta",
                "exam_levels": ["E6_CAPSTONE"],
                "critical": True,
            },
        ],
        acceptance_criteria=[
            {
                "criterion_id": "E1-C1",
                "task_id": "E1",
                "field": "supported_not_auto_qualified",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E1-C2",
                "task_id": "E1",
                "field": "ak01_self_qualification_blocked",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E2-C1",
                "task_id": "E2",
                "field": "retracted_source_rejected",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E2-C2",
                "task_id": "E2",
                "field": "ingestion_blocked",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E3-C1",
                "task_id": "E3",
                "field": "provenance_complete",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E3-C2",
                "task_id": "E3",
                "field": "externally_qualified",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E4-C1",
                "task_id": "E4",
                "field": "root_cause_classified",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E4-C2",
                "task_id": "E4",
                "field": "correction_route",
                "mode": "EQUALS",
                "expected": "DECISION_RULE_REVIEW",
                "weight": 1,
            },
            {
                "criterion_id": "E5-C1",
                "task_id": "E5",
                "field": "metadata_conflict_quarantined",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E5-C2",
                "task_id": "E5",
                "field": "missing_constraint_returns_no_decision",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E6-C1",
                "task_id": "E6",
                "field": "method_selected",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
            {
                "criterion_id": "E6-C2",
                "task_id": "E6",
                "field": "learning_delta_created",
                "mode": "EQUALS",
                "expected": True,
                "weight": 1,
            },
        ],
    )


def _e1_submission() -> dict[str, Any]:
    assessment = {
        "candidate_snapshot": {
            "title": "Qualified Source",
            "persistent_identifier_or_official_locator": "doi:10.example/e1",
        },
        "verdict": "ACCEPT_PRIMARY",
        "limitations": [],
        "ingestion_allowed": True,
    }
    link = build_evidence_link(
        claim_id="E1-C",
        claim_text="Claim",
        source_assessment=assessment,
        fragment={
            "fragment_id": "E1-F",
            "locator": "section 1",
            "text": "Evidence",
        },
        relation="SUPPORTS",
        rationale="Direct support",
    )
    summary = summarize_claim_evidence("E1-C", [link])

    blocked = False
    unit = {
        "knowledge_id": "E1-K",
        "state": "VERIFIED_NOT_QUALIFIED",
        "evidence_links": [link],
    }
    try:
        qualify_knowledge_unit(
            unit,
            reviewer_id="AK-01",
            reviewer_role="AK-01",
            criteria={
                "provenance_complete": True,
                "evidence_sufficient": True,
                "limitations_explicit": True,
                "counter_evidence_reviewed": True,
                "tests_present": True,
            },
        )
    except PermissionError:
        blocked = True

    return {
        "supported_not_auto_qualified": (
            summary["evidence_state"] == "SUPPORTED_NOT_QUALIFIED"
            and summary["auto_qualified"] is False
        ),
        "ak01_self_qualification_blocked": blocked,
    }


def _e2_submission() -> dict[str, Any]:
    result = assess_source(
        {
            "title": "Retracted Source",
            "source_type": "scientific_article",
            "authors_or_issuer": ["Researcher"],
            "publication_or_version_date": "2025",
            "persistent_identifier_or_official_locator": "doi:10.example/retracted",
            "integrity_status": "RETRACTED",
            "methodology": "experiment",
            "claim_fit": "HIGH",
            "authority": "SCIENTIFIC_PRIMARY",
            "limitations": [],
        },
        intended_claim="Method A works",
    )
    return {
        "retracted_source_rejected": result["verdict"] == "REJECT",
        "ingestion_blocked": result["ingestion_allowed"] is False,
    }


def _e3_submission() -> dict[str, Any]:
    assessment = assess_source(
        {
            "title": "Primary Source",
            "source_type": "scientific_article",
            "authors_or_issuer": ["Researcher"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "doi:10.example/e3",
            "integrity_status": "CURRENT",
            "methodology": "comparative study",
            "claim_fit": "HIGH",
            "authority": "SCIENTIFIC_PRIMARY",
            "limitations": [],
        },
        intended_claim="Method A is applicable under condition X",
        required_role="PRIMARY",
    )
    link = build_evidence_link(
        claim_id="E3-C",
        claim_text="Method A is applicable under condition X",
        source_assessment=assessment,
        fragment={
            "fragment_id": "E3-F",
            "locator": "section 4",
            "text": "Method A is applicable under condition X",
        },
        relation="SUPPORTS",
        rationale="Direct statement",
    )
    summary = summarize_claim_evidence("E3-C", [link])
    unit = build_knowledge_unit(
        knowledge_id="E3-K",
        knowledge_type="DECISION_RULE",
        title="Method A applicability",
        claim_summary=summary,
        evidence_links=[link],
        tests=["Case X"],
    )
    record = qualify_knowledge_unit(
        unit,
        reviewer_id="AQ-01",
        reviewer_role="Independent Evaluator",
        criteria={
            "provenance_complete": True,
            "evidence_sufficient": True,
            "limitations_explicit": True,
            "counter_evidence_reviewed": True,
            "tests_present": True,
        },
    )
    promoted = apply_qualification(unit, record)
    evidence = promoted["evidence_links"][0]["evidence"]
    return {
        "provenance_complete": bool(
            evidence.get("fragment_id")
            and evidence.get("locator")
            and evidence.get("source_locator")
        ),
        "externally_qualified": promoted["state"] == "QUALIFIED",
    }


def _e4_submission() -> dict[str, Any]:
    selection = {
        "decision": "SELECTED",
        "selected_candidate_id": "M1",
        "reason": "highest_weighted_score_after_hard_constraints",
    }
    outcome = record_solution_outcome(
        problem_id="E4-P",
        selection_record=selection,
        expected_metrics={"quality": 0.9},
        actual_metrics={"quality": 0.5},
    )
    classified = classify_root_cause(
        outcome,
        root_cause="K8_DECISION_RULE_INCORRECT",
        evidence=["Rule did not include applicability condition X"],
    )
    action = route_learning_action(classified)
    return {
        "root_cause_classified": classified["root_cause"] == "K8_DECISION_RULE_INCORRECT",
        "correction_route": action["route"],
    }


def _e5_submission() -> dict[str, Any]:
    reviewed_entry = {
        "registry_key": "doi:10.example/e5",
        "title": "Conflicted",
        "source_type": "scientific_article",
        "authors_or_issuer": ["A"],
        "publication_or_version_date": "2026",
        "persistent_identifier_or_official_locator": "doi:10.example/e5",
        "discovery_channels": ["openalex", "crossref"],
        "discovery_records": [],
        "merge_count": 2,
        "status": "DISCOVERED_UNQUALIFIED",
        "metadata_conflicts": [
            {
                "field": "publication_or_version_date",
                "values": ["2025", "2026"],
                "severity": "REVIEW_REQUIRED",
            }
        ],
        "requires_metadata_review": True,
        "integrity_status": "CURRENT",
        "methodology": "study",
        "claim_fit": "HIGH",
        "authority": "SCIENTIFIC_PRIMARY",
        "limitations": [],
    }
    quarantined = assess_source(
        reviewed_entry,
        intended_claim="Claim",
    )

    selection = compare_candidates(
        candidates=[{"candidate_id": "M1"}],
        readiness=[{"candidate_id": "M1", "ready_for_comparison": True}],
        criteria=[{"name": "quality", "weight": 1.0, "direction": "MAXIMIZE"}],
        measurements={"M1": {"quality": 0.9, "latency_ms": 20}},
        hard_constraints=[{"metric": "latency_ms", "operator": "<="}],
    )

    return {
        "metadata_conflict_quarantined": quarantined["verdict"] == "QUARANTINE",
        "missing_constraint_returns_no_decision": selection["decision"] == "NO_DECISION",
    }


def _e6_submission() -> dict[str, Any]:
    run = prepare_knowledge_acquisition_run(
        work_object={
            "id": "E6-RUN",
            "goal": "Choose retrieval method",
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
            "persistent_identifier_or_official_locator": "doi:10.example/e6",
            "integrity_status": "CURRENT",
            "methodology": "comparative evaluation",
            "claim_fit": "HIGH",
            "authority": "SCIENTIFIC_SYNTHESIS",
            "limitations": ["Corpus dependent"],
        },
        intended_claim="Hybrid retrieval is useful for mixed lexical and semantic matching",
        fragment={
            "fragment_id": "E6-F",
            "locator": "section 4",
            "text": "Hybrid retrieval combines lexical and semantic signals.",
        },
        claim_id="E6-C",
        knowledge_id="E6-K",
        knowledge_type="DECISION_RULE",
        knowledge_title="Hybrid retrieval candidate rule",
        relation="SUPPORTS",
        rationale="Direct support",
        reviewer_id="AQ-01",
        reviewer_role="Independent Evaluator",
        qualification_criteria={
            "provenance_complete": True,
            "evidence_sufficient": True,
            "limitations_explicit": True,
            "counter_evidence_reviewed": True,
            "tests_present": True,
        },
        decision_rules=["Consider hybrid when lexical and semantic signals matter"],
        failure_modes=["Fusion weighting sensitivity"],
        tests=["Representative query benchmark"],
    )

    run = solve_with_qualified_knowledge(
        run=run,
        problem_spec={
            "problem_id": "E6-P",
            "statement": "Choose retrieval method",
            "expected_output": "Selected method",
            "constraints": {"latency_ms": 100},
            "problem_class": "RANKING",
        },
        method_specs=[
            {
                "method_id": "M-HYBRID",
                "method_name": "Hybrid retrieval",
                "method_family": "retrieval",
                "knowledge_ids": ["E6-K"],
                "metrics": ["quality", "latency_ms"],
                "timing": {
                    "measured_latency_ms": 80,
                    "measurement_source": "benchmark:e6",
                },
                "failure_modes": ["Fusion weighting sensitivity"],
                "evidence_refs": ["doi:10.example/e6"],
            }
        ],
        criteria=[
            {"name": "quality", "weight": 1.0, "direction": "MAXIMIZE"},
            {"name": "latency_ms", "weight": 0.01, "direction": "MINIMIZE"},
        ],
        measurements={"M-HYBRID": {"quality": 0.9, "latency_ms": 80}},
        hard_constraints=[{"metric": "latency_ms", "operator": "<=", "value": 100}],
    )
    method_selected = run["status"] == "METHOD_SELECTED"

    run = close_run_with_learning(
        run=run,
        expected_metrics={"quality": 0.9, "latency_ms": 80},
        actual_metrics={"quality": 0.7, "latency_ms": 82},
        root_cause="K8_DECISION_RULE_INCORRECT",
        root_cause_evidence=["Applicability condition was incomplete"],
        affected_artifacts=["decision-rule:hybrid-selection"],
        proposed_change="Add corpus/query distribution condition",
        regression_case="Changed distribution triggers reconsideration",
    )

    return {
        "method_selected": method_selected,
        "learning_delta_created": (
            run["status"] == "LEARNING_DELTA_REQUIRED"
            and run["learning_delta"]["regression_required"] is True
        ),
    }


def run_ak01_self_diagnostic() -> dict[str, Any]:
    spec = build_ak01_self_exam_spec()
    submissions = {
        "E1:E1_KNOWLEDGE": _e1_submission(),
        "E2:E2_DECISION": _e2_submission(),
        "E3:E3_PROCEDURE": _e3_submission(),
        "E4:E4_FAILURE": _e4_submission(),
        "E5:E5_ADVERSARIAL": _e5_submission(),
        "E6:E6_CAPSTONE": _e6_submission(),
    }
    result = evaluate_exam(exam_spec=spec, submissions=submissions)
    result["training_gaps"] = derive_training_gaps(result)
    result["exam_spec_status"] = spec["status"]
    return result
