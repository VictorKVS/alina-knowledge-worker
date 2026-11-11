import pytest

from ak01.citation_graph import (
    build_seed_citation_graph,
    propose_citation_expansion,
    validate_citation_graph,
)


@pytest.mark.knowledge
def test_openalex_reference_metadata_builds_author_and_citation_edges():
    candidates = [
        {
            "title": "Seed Work",
            "authors_or_issuer": ["Ada Example", "Ben Example"],
            "persistent_identifier_or_official_locator": "https://doi.org/10.1/seed",
            "discovery_channel": "openalex",
            "raw_metadata": {
                "referenced_works": [
                    "https://openalex.org/W100",
                    "https://openalex.org/W200",
                ]
            },
        }
    ]

    graph = build_seed_citation_graph(candidates)

    assert validate_citation_graph(graph) == []
    assert graph["status"] == "GRAPH_READY"

    edge_types = [edge["type"] for edge in graph["edges"]]
    assert edge_types.count("AUTHORED") == 2
    assert edge_types.count("CITES") == 2


@pytest.mark.knowledge
def test_citation_expansion_preserves_discovery_only_boundary():
    graph = build_seed_citation_graph([
        {
            "title": "Seed Work",
            "authors_or_issuer": ["Ada Example"],
            "persistent_identifier_or_official_locator": "doi:10.1/seed",
            "discovery_channel": "openalex",
            "raw_metadata": {
                "referenced_works": ["https://openalex.org/W100"]
            },
        }
    ])

    expansion = propose_citation_expansion(graph)

    assert expansion["status"] == "EXPANSION_READY"
    assert expansion["selection_prohibited"] is True
    assert expansion["work_queries"][0]["reason"] == "backward_citation_expansion"
    assert expansion["author_queries"][0]["reason"] == "author_work_expansion"


@pytest.mark.knowledge
def test_empty_graph_produces_no_expansion_targets():
    graph = build_seed_citation_graph([])

    expansion = propose_citation_expansion(graph)

    assert graph["status"] == "EMPTY_GRAPH"
    assert expansion["status"] == "NO_EXPANSION_TARGETS"
