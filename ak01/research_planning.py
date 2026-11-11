from __future__ import annotations

from copy import deepcopy
from typing import Any

_SOURCE_MIX = {
    "MISSING_METHOD": [
        "body_of_knowledge",
        "scholarly_synthesis",
        "canonical_book",
        "primary_research",
        "official_documentation",
        "practitioner_case",
    ],
    "MISSING_ALGORITHM": [
        "canonical_book",
        "primary_research",
        "scholarly_synthesis",
        "benchmark",
        "official_documentation",
    ],
    "MISSING_DECISION_RULE": [
        "official_or_normative_source",
        "body_of_knowledge",
        "scholarly_synthesis",
        "comparative_evidence",
        "failure_case",
    ],
    "MISSING_KNOWLEDGE": [
        "body_of_knowledge",
        "canonical_book",
        "scholarly_synthesis",
        "primary_research",
    ],
    "MISSING_EVIDENCE": [
        "primary_source",
        "independent_corroboration",
        "counter_evidence",
    ],
}


def _questions(finding_type: str, subject: str) -> list[str]:
    if finding_type == "MISSING_METHOD":
        return [
            f"What recognized method families solve the task: {subject}?",
            "Under which conditions is each method applicable or contraindicated?",
            "What quality, latency, cost, safety, and resource trade-offs distinguish them?",
            "What failure modes and production limitations are documented?",
        ]
    if finding_type == "MISSING_ALGORITHM":
        return [
            f"What algorithms can perform the operation: {subject}?",
            "What are their computational and resource complexity characteristics?",
            "What constraints determine algorithm selection?",
            "What comparative benchmarks and known failure modes exist?",
        ]
    if finding_type == "MISSING_DECISION_RULE":
        return [
            f"What evidence-based criteria govern the decision: {subject}?",
            "What thresholds, exceptions, and uncertainty conditions are recognized?",
            "What competing rules or interpretations exist?",
            "When must the decision be escalated instead of automated?",
        ]
    if finding_type == "MISSING_KNOWLEDGE":
        return [
            f"What foundational concepts are required to perform: {subject}?",
            "What prerequisites and professional depth are required?",
            "Which concepts are stable foundations and which are fast-changing?",
        ]
    if finding_type == "MISSING_EVIDENCE":
        return [
            f"What primary evidence supports the claim or rule related to: {subject}?",
            "Is there independent corroboration or counter-evidence?",
            "Are there corrections, superseding versions, or known limitations?",
        ]
    return [
        f"What information is missing to resolve: {subject}?",
        "Which authoritative source types can resolve the uncertainty?",
    ]


def build_research_plan(
    trace: dict[str, Any],
    finding: dict[str, Any],
    *,
    constraints: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Turn a traced knowledge/method gap into a conservative research task.

    The planner does not select a solution. It specifies what evidence must be
    found before a later selection stage is allowed.
    """
    finding_type = str(finding.get("type", "UNKNOWN"))
    node_id = str(finding.get("node_id", "UNKNOWN"))
    node = next(
        (item for item in trace.get("nodes", []) if item.get("id") == node_id),
        None,
    )
    subject = str(node.get("label")) if node else str(finding.get("message", "unknown gap"))

    source_mix = deepcopy(
        _SOURCE_MIX.get(
            finding_type,
            ["authoritative_reference", "independent_corroboration"],
        )
    )

    return {
        "plan_id": f'{trace.get("trace_id", "TRACE")}:{node_id}:{finding_type}',
        "derived_from": {
            "trace_id": trace.get("trace_id"),
            "node_id": node_id,
            "finding_type": finding_type,
        },
        "subject": subject,
        "problem_class": "UNCLASSIFIED",
        "research_questions": _questions(finding_type, subject),
        "source_mix": source_mix,
        "constraints": deepcopy(constraints or {}),
        "selection_prohibited": True,
        "required_outputs": [
            "candidate_method_or_algorithm_families",
            "applicability_conditions",
            "decision_criteria",
            "limitations_and_failure_modes",
            "qualified_sources",
            "contradictions_and_counter_evidence",
        ],
        "stop_conditions": [
            "all mandatory research questions are covered",
            "critical claims have qualified evidence",
            "material alternatives are represented",
            "material contradictions are documented",
            "selection criteria are explicit and testable",
        ],
        "status": "RESEARCH_REQUIRED",
    }


def plans_for_trace(
    trace: dict[str, Any],
    *,
    constraints: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    supported = {
        "MISSING_METHOD",
        "MISSING_ALGORITHM",
        "MISSING_DECISION_RULE",
        "MISSING_KNOWLEDGE",
        "MISSING_EVIDENCE",
    }
    return [
        build_research_plan(trace, finding, constraints=constraints)
        for finding in trace.get("findings", [])
        if finding.get("type") in supported
    ]
