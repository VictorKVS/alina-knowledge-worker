import pytest

from ak01.source_adapter_policy import classify_adapter_failure
from ak01.source_adapters import (
    FixtureSourceAdapter,
    SourceQuery,
    run_discovery_queries,
)


@pytest.mark.knowledge
def test_fixture_adapter_returns_traceable_candidates():
    adapter = FixtureSourceAdapter([
        {
            "title": "Hybrid Retrieval Study",
            "abstract": "hybrid retrieval combines lexical and semantic search",
            "keywords": ["retrieval"],
            "source_type": "primary_research",
            "authors_or_issuer": ["Researcher A"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "doi:10.example/hybrid",
        }
    ])

    result = run_discovery_queries(
        adapter=adapter,
        queries=[
            SourceQuery(
                query_id="Q1",
                query_text="hybrid retrieval",
                source_type="primary_research",
            )
        ],
    )

    assert result["status"] == "CANDIDATES_READY"
    candidate = result["candidates"][0]
    assert candidate["discovery_channel"] == "fixture"
    assert candidate["persistent_identifier_or_official_locator"] == "doi:10.example/hybrid"
    assert candidate["raw_metadata"]["title"] == "Hybrid Retrieval Study"


@pytest.mark.knowledge
def test_fixture_adapter_honors_query_limit():
    fixtures = [
        {
            "title": f"Retrieval Study {i}",
            "abstract": "retrieval",
            "persistent_identifier_or_official_locator": f"doi:{i}",
        }
        for i in range(5)
    ]
    adapter = FixtureSourceAdapter(fixtures)

    result = run_discovery_queries(
        adapter=adapter,
        queries=[
            SourceQuery(
                query_id="Q2",
                query_text="retrieval",
                source_type="primary_research",
                limit=2,
            )
        ],
    )

    assert len(result["candidates"]) == 2


@pytest.mark.knowledge
@pytest.mark.parametrize(
    ("status_code", "failure_class", "retryable"),
    [
        (429, "RATE_LIMIT", True),
        (503, "UPSTREAM_UNAVAILABLE", True),
        (401, "AUTHORIZATION", False),
        (404, "NOT_FOUND", False),
    ],
)
def test_adapter_failure_policy(status_code, failure_class, retryable):
    result = classify_adapter_failure(status_code=status_code)

    assert result["failure_class"] == failure_class
    assert result["retryable"] is retryable
