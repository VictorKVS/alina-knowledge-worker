import pytest

from ak01.source_qualification import assess_source, validate_assessment


@pytest.mark.knowledge
def test_retracted_source_is_rejected():
    candidate = {
        "title": "Example Paper",
        "source_type": "scientific_article",
        "authors_or_issuer": ["A. Researcher"],
        "publication_or_version_date": "2024",
        "persistent_identifier_or_official_locator": "doi:10.0000/example",
        "integrity_status": "RETRACTED",
        "methodology": "controlled experiment",
        "claim_fit": "HIGH",
        "authority": "SCIENTIFIC_PRIMARY",
        "limitations": [],
    }

    result = assess_source(candidate, intended_claim="Method X improves recall")

    assert result["verdict"] == "REJECT"
    assert result["ingestion_allowed"] is False
    assert validate_assessment(result) == []


@pytest.mark.knowledge
def test_unknown_integrity_quarantines_source_even_if_author_is_famous():
    candidate = {
        "title": "Famous Book",
        "source_type": "book",
        "authors_or_issuer": ["Very Famous Author"],
        "publication_or_version_date": "2026",
        "persistent_identifier_or_official_locator": "isbn:0000000000",
        "scope": "retrieval systems",
        "claim_fit": "HIGH",
        "authority": "SCHOLARLY_BOOK",
        "limitations": [],
    }

    result = assess_source(candidate, intended_claim="Hybrid retrieval is preferred")

    assert result["verdict"] == "QUARANTINE"
    assert result["ingestion_allowed"] is False


@pytest.mark.knowledge
def test_primary_source_with_high_claim_fit_can_be_primary():
    candidate = {
        "title": "Official Standard",
        "source_type": "standard",
        "authors_or_issuer": ["Standards Body"],
        "version": "2.0",
        "persistent_identifier_or_official_locator": "official:standard-2",
        "integrity_status": "CURRENT",
        "scope": "defines mandatory requirement R1",
        "claim_fit": "HIGH",
        "authority": "NORMATIVE_PRIMARY",
        "limitations": [],
    }

    result = assess_source(
        candidate,
        intended_claim="Requirement R1 is mandatory",
        required_role="PRIMARY",
    )

    assert result["verdict"] == "ACCEPT_PRIMARY"
    assert result["ingestion_allowed"] is True


@pytest.mark.knowledge
def test_supporting_source_does_not_silently_fill_primary_role():
    candidate = {
        "title": "Professional Handbook",
        "source_type": "handbook",
        "authors_or_issuer": ["Professional Body"],
        "publication_or_version_date": "2026",
        "persistent_identifier_or_official_locator": "official:handbook",
        "integrity_status": "CURRENT",
        "scope": "professional synthesis",
        "claim_fit": "HIGH",
        "authority": "PROFESSIONAL_REFERENCE",
        "limitations": [],
    }

    result = assess_source(
        candidate,
        intended_claim="Rule Y is legally mandatory",
        required_role="PRIMARY",
    )

    assert result["verdict"] == "ACCEPT_WITH_LIMITS"
    assert "supporting_source_cannot_fill_primary_role_alone" in result["reasons"]
