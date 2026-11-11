import pytest

from ak01.source_registry import register_candidates, validate_registry


@pytest.mark.knowledge
def test_same_doi_from_openalex_and_crossref_merges_into_one_entry():
    candidates = [
        {
            "title": "Hybrid Retrieval Study",
            "source_type": "primary_research",
            "authors_or_issuer": ["A. Researcher"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "https://doi.org/10.1000/X",
            "discovery_channel": "openalex",
            "raw_metadata": {"id": "W1"},
        },
        {
            "title": "Hybrid Retrieval Study",
            "source_type": "primary_research",
            "authors_or_issuer": ["A. Researcher", "B. Researcher"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "doi:10.1000/x",
            "discovery_channel": "crossref",
            "raw_metadata": {"DOI": "10.1000/X"},
        },
    ]

    registry = register_candidates(candidates)

    assert validate_registry(registry) == []
    assert registry["input_count"] == 2
    assert registry["unique_count"] == 1
    assert registry["duplicate_count"] == 1

    entry = registry["entries"][0]
    assert entry["registry_key"] == "doi:10.1000/x"
    assert entry["discovery_channels"] == ["openalex", "crossref"]
    assert entry["merge_count"] == 2
    assert entry["status"] == "DISCOVERED_UNQUALIFIED"
    assert entry["authors_or_issuer"] == [
        "A. Researcher",
        "B. Researcher",
    ]


@pytest.mark.knowledge
def test_distinct_dois_do_not_merge_even_with_same_title():
    registry = register_candidates([
        {
            "title": "Same Title",
            "persistent_identifier_or_official_locator": "doi:10.1/a",
            "discovery_channel": "openalex",
        },
        {
            "title": "Same Title",
            "persistent_identifier_or_official_locator": "doi:10.1/b",
            "discovery_channel": "crossref",
        },
    ])

    assert registry["unique_count"] == 2
    assert registry["duplicate_count"] == 0


@pytest.mark.knowledge
def test_title_date_fallback_is_used_only_when_locator_is_absent():
    registry = register_candidates([
        {
            "title": "  Example   Book ",
            "publication_or_version_date": "2026",
            "discovery_channel": "catalog-a",
        },
        {
            "title": "example book",
            "publication_or_version_date": "2026",
            "discovery_channel": "catalog-b",
        },
    ])

    assert registry["unique_count"] == 1
    assert registry["entries"][0]["registry_key"] == "title:example book|date:2026"



@pytest.mark.knowledge
def test_metadata_conflicts_are_preserved_for_review():
    registry = register_candidates([
        {
            "title": "Hybrid Retrieval Study",
            "source_type": "primary_research",
            "authors_or_issuer": ["A. Researcher"],
            "publication_or_version_date": "2026",
            "persistent_identifier_or_official_locator": "doi:10.1000/conflict",
            "discovery_channel": "openalex",
        },
        {
            "title": "Hybrid Retrieval Study Revised",
            "source_type": "primary_research",
            "authors_or_issuer": ["A. Researcher", "B. Researcher"],
            "publication_or_version_date": "2025",
            "persistent_identifier_or_official_locator": "https://doi.org/10.1000/conflict",
            "discovery_channel": "crossref",
        },
    ])

    entry = registry["entries"][0]

    assert entry["requires_metadata_review"] is True
    fields = {item["field"] for item in entry["metadata_conflicts"]}
    assert "title" in fields
    assert "publication_or_version_date" in fields
    assert "authors_or_issuer" in fields
