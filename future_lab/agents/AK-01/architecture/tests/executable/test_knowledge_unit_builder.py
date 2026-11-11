import pytest

from ak01.knowledge_unit_builder import (
    build_evidence_bundle,
    build_knowledge_unit,
    validate_knowledge_unit,
)


def _link(claim_id, relation, fragment_id, limitations=None):
    return {
        "claim": {"id": claim_id, "text": "Claim text"},
        "relation": relation,
        "evidence": {
            "fragment_id": fragment_id,
            "text": "Evidence text",
            "locator": "section 1",
            "source_locator": "official:source",
        },
        "limitations": limitations or [],
        "qualification_required": True,
    }


@pytest.mark.knowledge
def test_supported_claim_builds_verified_not_qualified_unit():
    summary = {
        "claim_id": "C1",
        "evidence_state": "SUPPORTED_NOT_QUALIFIED",
    }
    unit = build_knowledge_unit(
        knowledge_id="K1",
        knowledge_type="DECISION_RULE",
        title="Use method A under condition X",
        claim_summary=summary,
        evidence_links=[_link("C1", "SUPPORTS", "F1")],
        decision_rules=["IF X THEN prefer A"],
        tests=["Case X selects A"],
    )

    assert validate_knowledge_unit(unit) == []
    assert unit["state"] == "VERIFIED_NOT_QUALIFIED"
    assert unit["qualification_required"] is True
    assert unit["auto_qualified"] is False


@pytest.mark.knowledge
def test_source_limitations_propagate_into_knowledge_unit():
    summary = {
        "claim_id": "C2",
        "evidence_state": "SUPPORTED_NOT_QUALIFIED",
    }
    unit = build_knowledge_unit(
        knowledge_id="K2",
        knowledge_type="METHOD",
        title="Method B",
        claim_summary=summary,
        evidence_links=[
            _link(
                "C2",
                "SUPPORTS",
                "F2",
                limitations=["Validated only on dataset A"],
            )
        ],
    )

    assert "Validated only on dataset A" in unit["limitations"]


@pytest.mark.knowledge
def test_conflicted_claim_retains_counter_evidence_and_conflicted_state():
    summary = {
        "claim_id": "C3",
        "evidence_state": "CONFLICTED",
    }
    links = [
        _link("C3", "SUPPORTS", "F3"),
        _link("C3", "CONTRADICTS", "F4"),
    ]
    unit = build_knowledge_unit(
        knowledge_id="K3",
        knowledge_type="CLAIM",
        title="Hybrid retrieval improves recall",
        claim_summary=summary,
        evidence_links=links,
    )

    assert validate_knowledge_unit(unit) == []
    assert unit["state"] == "CONFLICTED"
    assert any(link["relation"] == "CONTRADICTS" for link in unit["evidence_links"])
    assert unit["auto_qualified"] is False


@pytest.mark.knowledge
def test_evidence_bundle_is_ready_for_qualification_not_a_certificate():
    summary = {
        "claim_id": "C4",
        "evidence_state": "SUPPORTED_NOT_QUALIFIED",
    }
    unit = build_knowledge_unit(
        knowledge_id="K4",
        knowledge_type="ALGORITHM",
        title="Algorithm A",
        claim_summary=summary,
        evidence_links=[_link("C4", "SUPPORTS", "F5")],
        failure_modes=["Fails when input precondition Y is violated"],
        tests=["Benchmark case 1"],
    )

    bundle = build_evidence_bundle(unit)

    assert bundle["status"] == "READY_FOR_QUALIFICATION"
    assert bundle["qualification_required"] is True
    assert "Fails when input precondition Y is violated" in bundle["failure_modes"]
