import pytest

from ak01.professional_graph import (
    build_professional_graph,
    validate_professional_graph,
)
from ak01.runtime_policy import evaluate_runtime_access, filter_runtime_knowledge


def _trace():
    return {
        "trace_id": "CASE-PG:TRACE",
        "nodes": [
            {
                "id": "P1",
                "type": "PROCESS",
                "label": "Choose retrieval strategy",
                "status": "DRAFT",
                "derived_from": ["CASE-PG"],
            },
            {
                "id": "T1",
                "type": "TASK",
                "label": "Select retrieval method",
                "status": "DRAFT",
                "derived_from": ["CASE-PG"],
            },
            {
                "id": "D1",
                "type": "DECISION",
                "label": "sparse vs dense vs hybrid",
                "status": "DRAFT",
                "derived_from": ["T1"],
            },
        ],
        "edges": [{"from": "P1", "to": "T1", "type": "CONTAINS"}],
    }


def _qualified():
    return {
        "knowledge_id": "K1",
        "title": "Retrieval selection rule",
        "state": "QUALIFIED",
        "evidence_links": [
            {"evidence": {"source_locator": "doi:10.example/retrieval"}}
        ],
        "qualification_record": {"reviewer_id": "AQ-01"},
    }


@pytest.mark.knowledge
def test_only_qualified_knowledge_enters_professional_graph():
    graph = build_professional_graph(
        work_trace=_trace(),
        qualified_units=[_qualified()],
        bindings=[{"work_node_id": "D1", "knowledge_id": "K1"}],
    )

    assert validate_professional_graph(graph) == []
    assert graph["runtime_eligible_knowledge"] == ["K1"]
    assert any(
        edge["from"] == "D1"
        and edge["to"] == "K1"
        and edge["type"] == "SUPPORTED_BY_KNOWLEDGE"
        for edge in graph["edges"]
    )


@pytest.mark.knowledge
def test_unqualified_knowledge_cannot_be_bound_into_runtime_graph():
    unit = _qualified()
    unit["state"] = "VERIFIED_NOT_QUALIFIED"

    with pytest.raises(PermissionError):
        build_professional_graph(
            work_trace=_trace(),
            qualified_units=[unit],
            bindings=[{"work_node_id": "D1", "knowledge_id": "K1"}],
        )


@pytest.mark.knowledge
def test_runtime_policy_blocks_unqualified_and_escalates_conflict():
    allowed = evaluate_runtime_access(_qualified())
    assert allowed["decision"] == "ALLOW"

    unqualified = _qualified()
    unqualified["state"] = "VERIFIED_NOT_QUALIFIED"
    assert evaluate_runtime_access(unqualified)["decision"] == "BLOCK"

    conflicted = _qualified()
    conflicted["state"] = "CONFLICTED"
    assert evaluate_runtime_access(conflicted)["decision"] == "ESCALATE"


@pytest.mark.knowledge
def test_high_criticality_requires_traceable_qualification_record():
    unit = _qualified()
    unit.pop("qualification_record")

    decision = evaluate_runtime_access(unit, task_criticality="HIGH")

    assert decision["decision"] == "ESCALATE"


@pytest.mark.knowledge
def test_runtime_filter_separates_allowed_blocked_and_escalations():
    qualified = _qualified()

    blocked = _qualified()
    blocked["knowledge_id"] = "K2"
    blocked["state"] = "SUPERSEDED"

    conflicted = _qualified()
    conflicted["knowledge_id"] = "K3"
    conflicted["state"] = "CONFLICTED"

    result = filter_runtime_knowledge([qualified, blocked, conflicted])

    assert [item["knowledge_id"] for item in result["allowed"]] == ["K1"]
    assert [item["knowledge_id"] for item in result["blocked"]] == ["K2"]
    assert [item["knowledge_id"] for item in result["escalations"]] == ["K3"]
