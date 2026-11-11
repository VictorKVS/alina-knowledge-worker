from __future__ import annotations

from copy import deepcopy
from typing import Any

from .claim_evidence import build_evidence_link, summarize_claim_evidence
from .knowledge_qualification import apply_qualification, qualify_knowledge_unit
from .knowledge_unit_builder import build_knowledge_unit
from .learning_delta import propose_learning_delta
from .method_selection import compare_candidates
from .outcome_learning import (
    classify_root_cause,
    record_solution_outcome,
    route_learning_action,
)
from .problem_solving import (
    build_problem_signature,
    build_problem_solution_graph,
    register_candidate_method,
)
from .research_planning import plans_for_trace
from .source_discovery import build_source_discovery_plan
from .source_qualification import assess_source
from .work_analysis import decompose_work


def _stage(name: str, status: str, artifact: Any) -> dict[str, Any]:
    return {
        "stage": name,
        "status": status,
        "artifact": deepcopy(artifact),
    }


def prepare_knowledge_acquisition_run(
    *,
    work_object: dict[str, Any],
    constraints: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Start a factory run and stop at source discovery planning."""
    trace = decompose_work(work_object)
    research_plans = plans_for_trace(trace, constraints=constraints)
    discovery_plans = [
        build_source_discovery_plan(plan)
        for plan in research_plans
    ]

    stages = [
        _stage("WORK_DECOMPOSITION", "COMPLETED", trace),
        _stage("RESEARCH_PLANNING", "COMPLETED", research_plans),
        _stage("SOURCE_DISCOVERY_PLANNING", "COMPLETED", discovery_plans),
    ]

    return {
        "run_id": f'{trace.get("trace_id", "TRACE")}:FACTORY',
        "work_object": deepcopy(work_object),
        "trace": trace,
        "research_plans": research_plans,
        "discovery_plans": discovery_plans,
        "stages": stages,
        "next_required_stage": "SOURCE_DISCOVERY_EXECUTION",
        "status": "WAITING_FOR_SOURCE_CANDIDATES",
    }


def qualify_candidate_into_knowledge(
    *,
    run: dict[str, Any],
    candidate: dict[str, Any],
    intended_claim: str,
    fragment: dict[str, Any],
    claim_id: str,
    knowledge_id: str,
    knowledge_type: str,
    knowledge_title: str,
    relation: str,
    rationale: str,
    reviewer_id: str,
    reviewer_role: str,
    qualification_criteria: dict[str, bool],
    required_role: str = "SUPPORTING",
    decision_rules: list[str] | None = None,
    procedures: list[str] | None = None,
    limitations: list[str] | None = None,
    failure_modes: list[str] | None = None,
    tests: list[str] | None = None,
) -> dict[str, Any]:
    """Advance a run from a source candidate to externally qualified knowledge."""
    updated = deepcopy(run)
    assessment = assess_source(
        candidate,
        intended_claim=intended_claim,
        required_role=required_role,
    )
    updated["stages"].append(
        _stage("SOURCE_QUALIFICATION", assessment["verdict"], assessment)
    )

    if assessment.get("ingestion_allowed") is not True:
        updated["status"] = "BLOCKED_BY_SOURCE_QUALIFICATION"
        updated["next_required_stage"] = "SOURCE_DISCOVERY_EXECUTION"
        return updated

    link = build_evidence_link(
        claim_id=claim_id,
        claim_text=intended_claim,
        source_assessment=assessment,
        fragment=fragment,
        relation=relation,
        rationale=rationale,
    )
    summary = summarize_claim_evidence(claim_id, [link])
    unit = build_knowledge_unit(
        knowledge_id=knowledge_id,
        knowledge_type=knowledge_type,
        title=knowledge_title,
        claim_summary=summary,
        evidence_links=[link],
        decision_rules=decision_rules,
        procedures=procedures,
        limitations=limitations,
        failure_modes=failure_modes,
        tests=tests,
    )
    updated["stages"].append(_stage("CLAIM_EVIDENCE", "COMPLETED", link))
    updated["stages"].append(_stage("KNOWLEDGE_UNIT", unit["state"], unit))

    qualification = qualify_knowledge_unit(
        unit,
        reviewer_id=reviewer_id,
        reviewer_role=reviewer_role,
        criteria=qualification_criteria,
    )
    promoted = apply_qualification(unit, qualification)
    updated["stages"].append(
        _stage("KNOWLEDGE_QUALIFICATION", qualification["verdict"], qualification)
    )
    updated["knowledge_unit"] = promoted

    if promoted.get("state") != "QUALIFIED":
        updated["status"] = "BLOCKED_BY_KNOWLEDGE_QUALIFICATION"
        updated["next_required_stage"] = "KNOWLEDGE_REVIEW"
        return updated

    updated["status"] = "QUALIFIED_KNOWLEDGE_READY"
    updated["next_required_stage"] = "PROBLEM_SOLUTION"
    return updated


def solve_with_qualified_knowledge(
    *,
    run: dict[str, Any],
    problem_spec: dict[str, Any],
    method_specs: list[dict[str, Any]],
    criteria: list[dict[str, Any]],
    measurements: dict[str, dict[str, float]],
    hard_constraints: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build candidates and make a selection only when qualified knowledge exists."""
    updated = deepcopy(run)
    unit = updated.get("knowledge_unit")

    if not unit or unit.get("state") != "QUALIFIED":
        updated["status"] = "BLOCKED_RUNTIME_NO_QUALIFIED_KNOWLEDGE"
        updated["next_required_stage"] = "KNOWLEDGE_QUALIFICATION"
        return updated

    problem = build_problem_signature(**problem_spec)
    candidates = [
        register_candidate_method(
            problem_signature=problem,
            **method_spec,
        )
        for method_spec in method_specs
    ]
    graph = build_problem_solution_graph(
        problem_signature=problem,
        candidates=candidates,
        qualified_knowledge_ids={str(unit["knowledge_id"])},
    )
    updated["stages"].append(_stage("PROBLEM_SIGNATURE", "COMPLETED", problem))
    updated["stages"].append(
        _stage("PROBLEM_SOLUTION_GRAPH", graph["selection_status"], graph)
    )

    selection = compare_candidates(
        candidates=candidates,
        readiness=graph["candidate_readiness"],
        criteria=criteria,
        measurements=measurements,
        hard_constraints=hard_constraints,
    )
    updated["stages"].append(
        _stage("METHOD_SELECTION", selection["decision"], selection)
    )
    updated["selection"] = selection

    if selection.get("decision") != "SELECTED":
        updated["status"] = "NO_DECISION"
        updated["next_required_stage"] = "MORE_EVIDENCE_OR_POLICY"
        return updated

    updated["status"] = "METHOD_SELECTED"
    updated["next_required_stage"] = "EXECUTION_AND_OUTCOME"
    return updated


def close_run_with_learning(
    *,
    run: dict[str, Any],
    expected_metrics: dict[str, float],
    actual_metrics: dict[str, float],
    root_cause: str,
    root_cause_evidence: list[str],
    affected_artifacts: list[str],
    proposed_change: str,
    regression_case: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Close a selected-method run and create a mandatory learning delta."""
    updated = deepcopy(run)
    selection = updated.get("selection") or {}

    outcome = record_solution_outcome(
        problem_id=str(
            updated.get("stages", [])[-3]
            .get("artifact", {})
            .get("problem_id", updated.get("run_id"))
        ),
        selection_record=selection,
        expected_metrics=expected_metrics,
        actual_metrics=actual_metrics,
        context=context,
    )
    classified = classify_root_cause(
        outcome,
        root_cause=root_cause,
        evidence=root_cause_evidence,
    )
    action = route_learning_action(classified)
    delta = propose_learning_delta(
        learning_action=action,
        affected_artifacts=affected_artifacts,
        proposed_change=proposed_change,
        regression_case=regression_case,
    )

    updated["stages"].append(_stage("OUTCOME", "RECORDED", classified))
    updated["stages"].append(_stage("LEARNING_ACTION", action["route"], action))
    updated["stages"].append(_stage("LEARNING_DELTA", "PROPOSED", delta))
    updated["outcome"] = classified
    updated["learning_delta"] = delta
    updated["status"] = "LEARNING_DELTA_REQUIRED"
    updated["next_required_stage"] = "PATCH_REGRESSION_REQUALIFICATION"
    return updated
