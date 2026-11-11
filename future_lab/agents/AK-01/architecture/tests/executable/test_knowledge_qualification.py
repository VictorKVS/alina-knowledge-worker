import pytest

from ak01.knowledge_qualification import (
    apply_qualification,
    qualify_knowledge_unit,
    validate_qualification_record,
)


def _unit(state="VERIFIED_NOT_QUALIFIED"):
    return {
        "knowledge_id": "K1",
        "state": state,
        "evidence_links": [{"id": "E1"}],
        "auto_qualified": False,
    }


def _criteria(**overrides):
    base = {
        "provenance_complete": True,
        "evidence_sufficient": True,
        "limitations_explicit": True,
        "counter_evidence_reviewed": True,
        "tests_present": True,
    }
    base.update(overrides)
    return base


@pytest.mark.knowledge
def test_ak01_cannot_self_qualify():
    with pytest.raises(PermissionError):
        qualify_knowledge_unit(
            _unit(),
            reviewer_id="AK-01",
            reviewer_role="Knowledge Architect",
            criteria=_criteria(),
        )


@pytest.mark.knowledge
def test_external_reviewer_can_qualify_when_all_criteria_pass():
    record = qualify_knowledge_unit(
        _unit(),
        reviewer_id="AQ-01",
        reviewer_role="Independent Knowledge Evaluator",
        criteria=_criteria(),
    )

    assert validate_qualification_record(record) == []
    assert record["verdict"] == "QUALIFIED"
    assert record["promotion_allowed"] is True

    promoted = apply_qualification(_unit(), record)
    assert promoted["state"] == "QUALIFIED"
    assert promoted["auto_qualified"] is False
    assert promoted["qualification_record"]["reviewer_id"] == "AQ-01"


@pytest.mark.knowledge
def test_failed_evidence_criterion_blocks_promotion():
    record = qualify_knowledge_unit(
        _unit(),
        reviewer_id="AQ-01",
        reviewer_role="Independent Knowledge Evaluator",
        criteria=_criteria(evidence_sufficient=False),
    )

    assert record["verdict"] == "NEEDS_MORE_EVIDENCE"
    assert record["promotion_allowed"] is False

    unchanged = apply_qualification(_unit(), record)
    assert unchanged["state"] == "VERIFIED_NOT_QUALIFIED"


@pytest.mark.knowledge
def test_conflicted_unit_cannot_be_promoted_even_if_criteria_pass():
    record = qualify_knowledge_unit(
        _unit(state="CONFLICTED"),
        reviewer_id="AQ-01",
        reviewer_role="Independent Knowledge Evaluator",
        criteria=_criteria(),
    )

    assert record["verdict"] == "CONFLICTED"
    assert record["promotion_allowed"] is False
