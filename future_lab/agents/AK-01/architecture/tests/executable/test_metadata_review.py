import pytest

from ak01.metadata_review import review_metadata_conflicts, validate_metadata_review
from ak01.source_qualification import assess_source


def _entry():
    return {
        "registry_key": "doi:10.1000/conflict",
        "title": "Hybrid Retrieval Study",
        "source_type": "scientific_article",
        "authors_or_issuer": ["A. Researcher"],
        "publication_or_version_date": "2026",
        "persistent_identifier_or_official_locator": "doi:10.1000/conflict",
        "discovery_channels": ["openalex", "crossref"],
        "discovery_records": [],
        "merge_count": 2,
        "status": "DISCOVERED_UNQUALIFIED",
        "metadata_conflicts": [
            {
                "field": "publication_or_version_date",
                "values": ["2025", "2026"],
                "severity": "REVIEW_REQUIRED",
            }
        ],
        "requires_metadata_review": True,
        "integrity_status": "CURRENT",
        "methodology": "comparative study",
        "claim_fit": "HIGH",
        "authority": "SCIENTIFIC_PRIMARY",
        "limitations": [],
    }


@pytest.mark.knowledge
def test_metadata_review_requires_resolution_for_every_conflicted_field():
    with pytest.raises(ValueError):
        review_metadata_conflicts(
            _entry(),
            reviewer_id="AQ-01",
            reviewer_role="Source Reviewer",
            canonical_values={},
            evidence=["publisher record confirms 2026"],
            rationale="Use publisher version-of-record date",
        )


@pytest.mark.knowledge
def test_resolved_metadata_can_leave_quarantine_but_is_not_auto_qualified():
    reviewed = review_metadata_conflicts(
        _entry(),
        reviewer_id="AQ-01",
        reviewer_role="Source Reviewer",
        canonical_values={"publication_or_version_date": "2026"},
        evidence=["publisher record confirms 2026"],
        rationale="Use publisher version-of-record date",
    )

    assert validate_metadata_review(reviewed) == []
    assert reviewed["metadata_review_resolved"] is True
    assert reviewed["requires_metadata_review"] is False

    result = assess_source(
        reviewed,
        intended_claim="Method A improves quality",
    )

    assert result["verdict"] == "ACCEPT_PRIMARY"
    assert result["ingestion_allowed"] is True
