from __future__ import annotations

from typing import Any


def build_seed_citation_graph(
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a citation/author graph from source-candidate metadata.

    The graph is discovery-only. It preserves external identifiers and never
    treats citation count as a quality verdict.
    """
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, str]] = []

    for candidate in candidates:
        locator = str(
            candidate.get("persistent_identifier_or_official_locator") or ""
        ).strip()
        if not locator:
            continue

        work_id = f"work:{locator.lower()}"
        nodes[work_id] = {
            "id": work_id,
            "type": "WORK",
            "label": candidate.get("title"),
            "locator": locator,
            "discovery_channel": candidate.get("discovery_channel"),
            "status": "DISCOVERED_UNQUALIFIED",
        }

        for author in candidate.get("authors_or_issuer") or []:
            author_name = str(author).strip()
            if not author_name:
                continue
            author_id = f"author:{author_name.lower()}"
            nodes.setdefault(
                author_id,
                {
                    "id": author_id,
                    "type": "AUTHOR",
                    "label": author_name,
                    "status": "DISCOVERED_IDENTITY",
                },
            )
            edges.append(
                {
                    "from": author_id,
                    "to": work_id,
                    "type": "AUTHORED",
                }
            )

        raw = candidate.get("raw_metadata") or {}
        for ref in raw.get("referenced_works") or []:
            ref_locator = str(ref).strip()
            if not ref_locator:
                continue
            ref_id = f"work:{ref_locator.lower()}"
            nodes.setdefault(
                ref_id,
                {
                    "id": ref_id,
                    "type": "WORK",
                    "label": ref_locator,
                    "locator": ref_locator,
                    "status": "DISCOVERED_REFERENCE",
                },
            )
            edges.append(
                {
                    "from": work_id,
                    "to": ref_id,
                    "type": "CITES",
                }
            )

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "status": "GRAPH_READY" if nodes else "EMPTY_GRAPH",
    }


def propose_citation_expansion(
    graph: dict[str, Any],
    *,
    max_work_queries: int = 20,
) -> dict[str, Any]:
    referenced = [
        node
        for node in graph.get("nodes", [])
        if node.get("type") == "WORK"
        and node.get("status") == "DISCOVERED_REFERENCE"
    ]

    query_targets = [
        {
            "locator": node.get("locator"),
            "reason": "backward_citation_expansion",
        }
        for node in referenced[:max_work_queries]
    ]

    authors = [
        node
        for node in graph.get("nodes", [])
        if node.get("type") == "AUTHOR"
    ]

    return {
        "work_queries": query_targets,
        "author_queries": [
            {
                "author": node.get("label"),
                "reason": "author_work_expansion",
            }
            for node in authors
        ],
        "selection_prohibited": True,
        "status": (
            "EXPANSION_READY"
            if query_targets or authors
            else "NO_EXPANSION_TARGETS"
        ),
    }


def validate_citation_graph(graph: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    node_ids = {
        str(node.get("id"))
        for node in graph.get("nodes", [])
        if node.get("id")
    }

    for edge in graph.get("edges", []):
        if edge.get("from") not in node_ids:
            errors.append(f"missing_edge_source:{edge.get('from')}")
        if edge.get("to") not in node_ids:
            errors.append(f"missing_edge_target:{edge.get('to')}")
        if edge.get("type") not in {"AUTHORED", "CITES"}:
            errors.append(f"invalid_edge_type:{edge.get('type')}")

    return errors
