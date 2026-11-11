from __future__ import annotations

from copy import deepcopy
from typing import Any


RELATION_TYPES = {
    "SUPPORTS",
    "CONTRADICTS",
    "LIMITS",
    "DEFINES",
    "IMPLEMENTS",
    "DERIVES",
}


def build_evidence_link(
    *,
    claim_id: str,
    claim_text: str,
    source_assessment: dict[str, Any],
    fragment: dict[str, Any],
    relation: str,
    rationale: str,
) -> dict[str, Any]:
    """Create a traceable claim-evidence relation.

    Evidence links may only be built from source assessments that allow ingestion.
    The link itself does not qualify the claim as true.
    """
    if relation not in RELATION_TYPES:
        raise ValueError(f"Unsupported relation: {relation}")

    if source_assessment.get("ingestion_allowed") is not True:
        raise PermissionError("Source assessment does not permit evidence ingestion")

    locator = fragment.get("locator")
    text = fragment.get("text")
    fragment_id = fragment.get("fragment_id")

    if not locator or not text or not fragment_id:
        raise ValueError("Evidence fragment requires fragment_id, locator, and text")

    candidate = source_assessment.get("candidate_snapshot", {})

    return {
        "link_id": f'{claim_id}:{fragment_id}:{relation}',
        "claim": {
            "id": claim_id,
            "text": claim_text,
            "state": "EVIDENCE_LINKED",
        },
        "relation": relation,
        "evidence": {
            "fragment_id": fragment_id,
            "text": text,
            "locator": locator,
            "source_title": candidate.get("title"),
            "source_locator": candidate.get(
                "persistent_identifier_or_official_locator"
            ),
            "source_version": (
                candidate.get("version")
                or candidate.get("publication_or_version_date")
            ),
            "source_verdict": source_assessment.get("verdict"),
        },
        "rationale": rationale,
        "limitations": deepcopy(source_assessment.get("limitations") or []),
        "qualification_required": True,
    }


def summarize_claim_evidence(
    claim_id: str,
    links: list[dict[str, Any]],
) -> dict[str, Any]:
    scoped = [link for link in links if link.get("claim", {}).get("id") == claim_id]
    by_relation = {relation: 0 for relation in RELATION_TYPES}

    for link in scoped:
        relation = link.get("relation")
        if relation in by_relation:
            by_relation[relation] += 1

    contradictions = by_relation["CONTRADICTS"]
    support = by_relation["SUPPORTS"] + by_relation["DEFINES"] + by_relation["DERIVES"]

    if not scoped:
        evidence_state = "NO_EVIDENCE"
    elif contradictions and support:
        evidence_state = "CONFLICTED"
    elif contradictions:
        evidence_state = "COUNTER_EVIDENCE_ONLY"
    elif support:
        evidence_state = "SUPPORTED_NOT_QUALIFIED"
    else:
        evidence_state = "EVIDENCE_PRESENT_NOT_SUPPORTING"

    return {
        "claim_id": claim_id,
        "evidence_state": evidence_state,
        "relation_counts": by_relation,
        "link_count": len(scoped),
        "qualification_allowed": evidence_state in {
            "SUPPORTED_NOT_QUALIFIED",
            "CONFLICTED",
        },
        "auto_qualified": False,
    }


def validate_evidence_link(link: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if link.get("relation") not in RELATION_TYPES:
        errors.append("invalid_relation")

    claim = link.get("claim", {})
    if not claim.get("id") or not claim.get("text"):
        errors.append("missing_claim")

    evidence = link.get("evidence", {})
    for field in ("fragment_id", "text", "locator", "source_locator"):
        if not evidence.get(field):
            errors.append(f"missing_evidence_{field}")

    if link.get("qualification_required") is not True:
        errors.append("qualification_gate_missing")

    return errors
