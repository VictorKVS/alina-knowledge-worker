from __future__ import annotations

from typing import Any
import networkx as nx

from .graph import GraphEdge, GraphNode, GraphStore


class NetworkXGraphStore(GraphStore):
    def __init__(self) -> None:
        self.graph = nx.MultiDiGraph()

    def add_node(self, node: GraphNode) -> None:
        self.graph.add_node(node.id, **node.attrs)

    def add_edge(self, edge: GraphEdge) -> None:
        self.graph.add_edge(
            edge.source,
            edge.target,
            edge_type=edge.edge_type,
            **edge.attrs,
        )

    def neighbors(self, node_id: str) -> list[str]:
        if node_id not in self.graph:
            return []
        result = set(self.graph.successors(node_id)) | set(self.graph.predecessors(node_id))
        return sorted(result)

    def snapshot(self) -> dict[str, Any]:
        return {
            "nodes": [
                {"id": node_id, **attrs}
                for node_id, attrs in self.graph.nodes(data=True)
            ],
            "edges": [
                {"source": u, "target": v, **attrs}
                for u, v, attrs in self.graph.edges(data=True)
            ],
        }
