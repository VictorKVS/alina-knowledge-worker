from __future__ import annotations

from copy import deepcopy
from typing import Any

VERDICTS = {
    "ACCEPT_PRIMARY",
    "ACCEPT_SUPPORTING",
    "ACCEPT_WITH_LIMITS",
    "DISCOVERY_ONLY",
    "QUARANTINE",
    "REJECT",
}


def _required_checks(candidate: dict[str, Any]) -> dict[str, bool]:
    return {
        "identity_present": bool(candidate.get("title")),
        "source_type_present": bool(candidate.get("source_type")),
        "issuer_or_authors_present": bool(candidate.get("authors_or_issuer")),
        "date_or_version_present": bool(
            candidate.get("publication_or_version_date") or candidate.get("version")
        ),
        "locator_present": bool(
            candidate.get("persistent_identifier_or_official_locator")
        ),
        "integrity_status_present": bool(candidate.get("integrity_status")),
        "methodology_or_scope_present": bool(
            candidate.get("methodology") or candidate.get("scope")
        ),
        "claim_fit_present": bool(candidate.get("claim_fit")),
        "limitations_present": "limitations" in candidate,
    }


def _hard_failures(candidate: dict[str, Any], checks: dict[str, bool]) -> list[str]:
    failures: list[str] = []

    if not checks["identity_present"]:
        failures.append("missing_identity")
    if not checks["source_type_present"]:
        failures.append("missing_source_type")
    if not checks["locator_present"]:
        failures.append("missing_persistent_identifier_or_official_locator")

    integrity = str(candidate.get("integrity_status", "")).upper()
    if integrity in {"RETRACTED", "TAMPERED", "INVALID"}:
        failures.append(f"integrity_failure:{integrity.lower()}")

    return failures


def assess_source(
    candidate: dict[str, Any],
    *,
    intended_claim: str,
    required_role: str = "SUPPORTING",
) -> dict[str, Any]:
    """Assess a discovered source candidate without ingesting it as knowledge."""
    checks = _required_checks(candidate)
    hard_failures = _hard_failures(candidate, checks)

    reasons: list[str] = []
    limitations = deepcopy(candidate.get("limitations") or [])

    if hard_failures:
        verdict = "REJECT"
        reasons.extend(hard_failures)
    elif (
        candidate.get("requires_metadata_review") is True
        and candidate.get("metadata_review_resolved") is not True
    ):
        verdict = "QUARANTINE"
        reasons.append("metadata_conflict_requires_review")
        limitations.append("metadata_conflict_unresolved")
    else:
        integrity = str(candidate.get("integrity_status", "")).upper()
        claim_fit = str(candidate.get("claim_fit", "")).upper()
        authority = str(candidate.get("authority", "")).upper()
        methodology = str(candidate.get("methodology", "")).strip()
        scope = str(candidate.get("scope", "")).strip()

        if not checks["integrity_status_present"]:
            verdict = "QUARANTINE"
            reasons.append("integrity_status_unknown")
        elif claim_fit not in {"HIGH", "MEDIUM", "LOW"}:
            verdict = "DISCOVERY_ONLY"
            reasons.append("claim_fit_not_assessed")
        elif claim_fit == "LOW":
            verdict = "DISCOVERY_ONLY"
            reasons.append("low_claim_fit")
        elif authority in {"OFFICIAL_PRIMARY", "NORMATIVE_PRIMARY", "SCIENTIFIC_PRIMARY"}:
            if claim_fit == "HIGH" and (methodology or scope):
                verdict = "ACCEPT_PRIMARY"
                reasons.append("primary_authority_with_high_claim_fit")
            else:
                verdict = "ACCEPT_WITH_LIMITS"
                reasons.append("primary_authority_but_scope_or_fit_limited")
        elif authority in {
            "SCIENTIFIC_SYNTHESIS",
            "SCHOLARLY_BOOK",
            "PROFESSIONAL_REFERENCE",
            "PRACTITIONER_EVIDENCE",
        }:
            if claim_fit == "HIGH":
                verdict = "ACCEPT_SUPPORTING"
                reasons.append("supporting_authority_with_high_claim_fit")
            else:
                verdict = "ACCEPT_WITH_LIMITS"
                reasons.append("supporting_source_with_partial_claim_fit")
        else:
            verdict = "DISCOVERY_ONLY"
            reasons.append("authority_not_sufficient_for_acceptance")

        if integrity in {"CORRECTED", "SUPERSEDED"} and verdict.startswith("ACCEPT"):
            verdict = "ACCEPT_WITH_LIMITS"
            reasons.append(f"integrity_status:{integrity.lower()}")

    if required_role == "PRIMARY" and verdict == "ACCEPT_SUPPORTING":
        verdict = "ACCEPT_WITH_LIMITS"
        reasons.append("supporting_source_cannot_fill_primary_role_alone")

    return {
        "candidate_snapshot": deepcopy(candidate),
        "intended_claim": intended_claim,
        "required_role": required_role,
        "checks": checks,
        "hard_failures": hard_failures,
        "verdict": verdict,
        "reasons": reasons,
        "limitations": limitations,
        "ingestion_allowed": verdict in {
            "ACCEPT_PRIMARY",
            "ACCEPT_SUPPORTING",
            "ACCEPT_WITH_LIMITS",
        },
        "qualification_complete": verdict != "QUARANTINE",
    }


def validate_assessment(assessment: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if assessment.get("verdict") not in VERDICTS:
        errors.append("invalid_verdict")
    if not assessment.get("intended_claim"):
        errors.append("missing_intended_claim")
    if not assessment.get("checks"):
        errors.append("missing_checks")
    if not assessment.get("reasons"):
        errors.append("missing_reasons")

    if assessment.get("verdict") == "REJECT" and assessment.get("ingestion_allowed"):
        errors.append("rejected_source_cannot_be_ingested")

    if assessment.get("verdict") == "QUARANTINE" and assessment.get("ingestion_allowed"):
        errors.append("quarantined_source_cannot_be_ingested")

    return errors
