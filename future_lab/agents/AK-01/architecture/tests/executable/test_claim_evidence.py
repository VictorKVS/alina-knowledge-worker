import pytest

from ak01.claim_evidence import (
    build_evidence_link,
    summarize_claim_evidence,
    validate_evidence_link,
)


def _accepted_source():
    return {
        "candidate_snapshot": {
            "title": "Authoritative Source",
            "version": "2.0",
            "persistent_identifier_or_official_locator": "official:source-2",
        },
        "verdict": "ACCEPT_PRIMARY",
        "limitations": ["Applies only to systems in scope"],
        "ingestion_allowed": True,
    }


@pytest.mark.knowledge
def test_evidence_link_preserves_fragment_and_source_trace():
    link = build_evidence_link(
        claim_id="C1",
        claim_text="Requirement R1 is mandatory",
        source_assessment=_accepted_source(),
        fragment={
            "fragment_id": "F1",
            "locator": "section 4.2",
            "text": "Systems in scope shall implement requirement R1.",
        },
        relation="SUPPORTS",
        rationale="The fragment directly states the mandatory requirement.",
    )

    assert validate_evidence_link(link) == []
    assert link["evidence"]["fragment_id"] == "F1"
    assert link["evidence"]["locator"] == "section 4.2"
    assert link["evidence"]["source_locator"] == "official:source-2"
    assert link["limitations"] == ["Applies only to systems in scope"]
    assert link["qualification_required"] is True


@pytest.mark.knowledge
def test_rejected_or_quarantined_source_cannot_be_ingested_as_evidence():
    source = _accepted_source()
    source["ingestion_allowed"] = False
    source["verdict"] = "QUARANTINE"

    with pytest.raises(PermissionError):
        build_evidence_link(
            claim_id="C2",
            claim_text="Method X is optimal",
            source_assessment=source,
            fragment={
                "fragment_id": "F2",
                "locator": "page 10",
                "text": "Method X performed best in this experiment.",
            },
            relation="SUPPORTS",
            rationale="Candidate evidence.",
        )


@pytest.mark.knowledge
def test_support_and_counter_evidence_produce_conflicted_state():
    source = _accepted_source()
    support = build_evidence_link(
        claim_id="C3",
        claim_text="Hybrid retrieval improves recall",
        source_assessment=source,
        fragment={
            "fragment_id": "F3",
            "locator": "table 2",
            "text": "Hybrid retrieval improved recall on dataset A.",
        },
        relation="SUPPORTS",
        rationale="Direct empirical support.",
    )
    counter = build_evidence_link(
        claim_id="C3",
        claim_text="Hybrid retrieval improves recall",
        source_assessment=source,
        fragment={
            "fragment_id": "F4",
            "locator": "table 5",
            "text": "No recall improvement was observed on dataset B.",
        },
        relation="CONTRADICTS",
        rationale="Direct counter-evidence.",
    )

    summary = summarize_claim_evidence("C3", [support, counter])

    assert summary["evidence_state"] == "CONFLICTED"
    assert summary["relation_counts"]["SUPPORTS"] == 1
    assert summary["relation_counts"]["CONTRADICTS"] == 1
    assert summary["auto_qualified"] is False


@pytest.mark.knowledge
def test_supported_claim_is_not_auto_qualified():
    link = build_evidence_link(
        claim_id="C4",
        claim_text="Algorithm A has lower latency",
        source_assessment=_accepted_source(),
        fragment={
            "fragment_id": "F5",
            "locator": "benchmark 1",
            "text": "Algorithm A completed in less time than Algorithm B.",
        },
        relation="SUPPORTS",
        rationale="Benchmark evidence.",
    )

    summary = summarize_claim_evidence("C4", [link])

    assert summary["evidence_state"] == "SUPPORTED_NOT_QUALIFIED"
    assert summary["qualification_allowed"] is True
    assert summary["auto_qualified"] is False
