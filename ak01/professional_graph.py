from __future__ import annotations

from copy import deepcopy
from typing import Any


PROFESSIONAL_NODE_TYPES = {
    "WORK_OBJECT",
    "PROCESS",
    "TASK",
    "DECISION",
    "METHOD",
    "ALGORITHM",
    "RULE",
    "PROCEDURE",
    "KNOWLEDGE",
    "TOOL",
    "QUALITY_CRITERION",
    "FAILURE_MODE",
}

PROFESSIONAL_EDGE_TYPES = {
    "CONTAINS",
    "REQUIRES_DECISION",
    "SOLVED_BY",
    "IMPLEMENTED_BY",
    "GOVERNED_BY",
    "SUPPORTED_BY_KNOWLEDGE",
    "USES_TOOL",
    "VERIFIED_BY",
    "FAILS_AS",
}


def build_professional_graph(
    *,
    work_trace: dict[str, Any],
    qualified_units: list[dict[str, Any]],
    bindings: list[dict[str, str]],
) -> dict[str, Any]:
    """Build a professional execution/knowledge graph from traced work and qualified knowledge."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []

    for node in work_trace.get("nodes", []):
        node_type = str(node.get("type", ""))
        if node_type in PROFESSIONAL_NODE_TYPES:
            nodes.append({
                "id": str(node.get("id")),
                "type": node_type,
                "label": str(node.get("label", "")),
                "status": str(node.get("status", "DRAFT")),
                "derived_from": deepcopy(node.get("derived_from", [])),
            })

    qualified_by_id = {
        str(unit.get("knowledge_id")): unit
        for unit in qualified_units
        if unit.get("state") == "QUALIFIED"
    }

    for knowledge_id, unit in qualified_by_id.items():
        nodes.append({
            "id": knowledge_id,
            "type": "KNOWLEDGE",
            "label": str(unit.get("title", knowledge_id)),
            "status": "QUALIFIED",
            "derived_from": [
                link.get("evidence", {}).get("source_locator")
                for link in unit.get("evidence_links", [])
                if link.get("evidence", {}).get("source_locator")
            ],
        })

    node_ids = {node["id"] for node in nodes}

    for edge in work_trace.get("edges", []):
        source = str(edge.get("from"))
        target = str(edge.get("to"))
        edge_type = str(edge.get("type"))
        if source in node_ids and target in node_ids and edge_type in PROFESSIONAL_EDGE_TYPES:
            edges.append({"from": source, "to": target, "type": edge_type})

    for binding in bindings:
        task_or_decision = str(binding.get("work_node_id", ""))
        knowledge_id = str(binding.get("knowledge_id", ""))
        if task_or_decision not in node_ids:
            raise ValueError(f"Unknown work node: {task_or_decision}")
        if knowledge_id not in qualified_by_id:
            raise PermissionError(
                f"Knowledge {knowledge_id} is not QUALIFIED and cannot enter runtime graph"
            )
        edges.append({
            "from": task_or_decision,
            "to": knowledge_id,
            "type": "SUPPORTED_BY_KNOWLEDGE",
        })

    return {
        "graph_id": f'{work_trace.get("trace_id", "TRACE")}:PROFESSIONAL',
        "nodes": nodes,
        "edges": edges,
        "runtime_eligible_knowledge": sorted(qualified_by_id),
    }


def validate_professional_graph(graph: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    node_ids: set[str] = set()

    for node in graph.get("nodes", []):
        node_id = str(node.get("id", ""))
        if not node_id:
            errors.append("node_missing_id")
            continue
        if node_id in node_ids:
            errors.append(f"duplicate_node:{node_id}")
        node_ids.add(node_id)

        if node.get("type") not in PROFESSIONAL_NODE_TYPES:
            errors.append(f"invalid_node_type:{node_id}")

        if node.get("type") == "KNOWLEDGE" and node.get("status") != "QUALIFIED":
            errors.append(f"runtime_graph_contains_unqualified_knowledge:{node_id}")

    for edge in graph.get("edges", []):
        if edge.get("from") not in node_ids:
            errors.append(f"edge_missing_source:{edge.get('from')}")
        if edge.get("to") not in node_ids:
            errors.append(f"edge_missing_target:{edge.get('to')}")
        if edge.get("type") not in PROFESSIONAL_EDGE_TYPES:
            errors.append(f"invalid_edge_type:{edge.get('type')}")

    return errors
