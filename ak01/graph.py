from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class GraphNode:
    id: str
    attrs: dict[str, Any]


@dataclass
class GraphEdge:
    source: str
    target: str
    edge_type: str
    attrs: dict[str, Any]


class GraphStore:
    def add_node(self, node: GraphNode) -> None:
        raise NotImplementedError

    def add_edge(self, edge: GraphEdge) -> None:
        raise NotImplementedError

    def neighbors(self, node_id: str) -> list[str]:
        raise NotImplementedError


class InMemoryGraphStore(GraphStore):
    def __init__(self) -> None:
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)

    def neighbors(self, node_id: str) -> list[str]:
        result = []
        for e in self.edges:
            if e.source == node_id:
                result.append(e.target)
            elif e.target == node_id:
                result.append(e.source)
        return result
