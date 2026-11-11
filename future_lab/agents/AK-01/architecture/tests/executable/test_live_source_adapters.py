import pytest

from ak01.live_source_adapters import CrossrefAdapter, OpenAlexAdapter
from ak01.source_adapters import SourceQuery


@pytest.mark.knowledge
def test_openalex_adapter_maps_api_result_to_source_candidate():
    def fake_get(url, headers):
        assert "api.openalex.org/works" in url
        assert "search=hybrid+retrieval" in url
        assert headers["Accept"] == "application/json"
        return {
            "results": [
                {
                    "id": "https://openalex.org/W1",
                    "doi": "https://doi.org/10.1000/example",
                    "display_name": "Hybrid Retrieval Study",
                    "publication_date": "2026-01-01",
                    "authorships": [
                        {"author": {"display_name": "A. Researcher"}},
                        {"author": {"display_name": "B. Researcher"}},
                    ],
                }
            ]
        }

    adapter = OpenAlexAdapter(json_get=fake_get)
    results = adapter.search(
        SourceQuery(
            query_id="Q1",
            query_text="hybrid retrieval",
            source_type="primary_research",
            limit=5,
        )
    )

    assert len(results) == 1
    assert results[0].title == "Hybrid Retrieval Study"
    assert results[0].authors_or_issuer == [
        "A. Researcher",
        "B. Researcher",
    ]
    assert (
        results[0].persistent_identifier_or_official_locator
        == "https://doi.org/10.1000/example"
    )
    assert results[0].discovery_channel == "openalex"


@pytest.mark.knowledge
def test_openalex_adapter_skips_untraceable_result_without_locator():
    adapter = OpenAlexAdapter(
        json_get=lambda url, headers: {
            "results": [{"display_name": "No Locator"}]
        }
    )

    results = adapter.search(
        SourceQuery(
            query_id="Q2",
            query_text="test",
            source_type="primary_research",
        )
    )

    assert results == []


@pytest.mark.knowledge
def test_crossref_adapter_maps_bibliographic_result():
    def fake_get(url, headers):
        assert "api.crossref.org/works" in url
        assert "query.bibliographic=rag+evaluation" in url
        assert headers["User-Agent"].startswith("FATHER-AK01")
        return {
            "message": {
                "items": [
                    {
                        "DOI": "10.1000/rag",
                        "title": ["RAG Evaluation"],
                        "author": [
                            {"given": "Ada", "family": "Example"},
                        ],
                        "published-print": {
                            "date-parts": [[2026, 5, 10]]
                        },
                    }
                ]
            }
        }

    adapter = CrossrefAdapter(json_get=fake_get)
    results = adapter.search(
        SourceQuery(
            query_id="Q3",
            query_text="rag evaluation",
            source_type="primary_research",
            limit=3,
        )
    )

    assert len(results) == 1
    assert results[0].title == "RAG Evaluation"
    assert results[0].authors_or_issuer == ["Ada Example"]
    assert results[0].publication_or_version_date == "2026-5-10"
    assert (
        results[0].persistent_identifier_or_official_locator
        == "https://doi.org/10.1000/rag"
    )
    assert results[0].discovery_channel == "crossref"


@pytest.mark.knowledge
def test_crossref_adapter_skips_record_without_doi():
    adapter = CrossrefAdapter(
        json_get=lambda url, headers: {
            "message": {
                "items": [
                    {"title": ["No DOI"]}
                ]
            }
        }
    )

    results = adapter.search(
        SourceQuery(
            query_id="Q4",
            query_text="test",
            source_type="primary_research",
        )
    )

    assert results == []
