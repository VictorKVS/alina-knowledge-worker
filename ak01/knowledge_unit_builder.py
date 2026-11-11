from __future__ import annotations

from copy import deepcopy
from typing import Any


def build_knowledge_unit(
    *,
    knowledge_id: str,
    knowledge_type: str,
    title: str,
    claim_summary: dict[str, Any],
    evidence_links: list[dict[str, Any]],
    prerequisites: list[str] | None = None,
    decision_rules: list[str] | None = None,
    procedures: list[str] | None = None,
    limitations: list[str] | None = None,
    failure_modes: list[str] | None = None,
    tests: list[str] | None = None,
) -> dict[str, Any]:
    """Build an evidence-backed Knowledge Unit without self-qualification."""
    scoped_links = [
        deepcopy(link)
        for link in evidence_links
        if link.get("claim", {}).get("id") == claim_summary.get("claim_id")
    ]

    inherited_limitations: list[str] = []
    for link in scoped_links:
        for item in link.get("limitations", []):
            if item not in inherited_limitations:
                inherited_limitations.append(item)

    all_limitations = list(limitations or [])
    for item in inherited_limitations:
        if item not in all_limitations:
            all_limitations.append(item)

    state = "EVIDENCE_LINKED"
    if claim_summary.get("evidence_state") == "CONFLICTED":
        state = "CONFLICTED"
    elif claim_summary.get("evidence_state") == "SUPPORTED_NOT_QUALIFIED":
        state = "VERIFIED_NOT_QUALIFIED"

    return {
        "knowledge_id": knowledge_id,
        "knowledge_type": knowledge_type,
        "title": title,
        "state": state,
        "claim_id": claim_summary.get("claim_id"),
        "evidence_state": claim_summary.get("evidence_state"),
        "evidence_links": scoped_links,
        "prerequisites": list(prerequisites or []),
        "decision_rules": list(decision_rules or []),
        "procedures": list(procedures or []),
        "limitations": all_limitations,
        "failure_modes": list(failure_modes or []),
        "tests": list(tests or []),
        "qualification_required": True,
        "auto_qualified": False,
    }


def build_evidence_bundle(unit: dict[str, Any]) -> dict[str, Any]:
    return {
        "knowledge_id": unit.get("knowledge_id"),
        "definition_or_claim": unit.get("title"),
        "prerequisites": deepcopy(unit.get("prerequisites", [])),
        "decision_rules": deepcopy(unit.get("decision_rules", [])),
        "procedures": deepcopy(unit.get("procedures", [])),
        "limitations": deepcopy(unit.get("limitations", [])),
        "failure_modes": deepcopy(unit.get("failure_modes", [])),
        "tests": deepcopy(unit.get("tests", [])),
        "evidence_links": deepcopy(unit.get("evidence_links", [])),
        "evidence_state": unit.get("evidence_state"),
        "qualification_required": unit.get("qualification_required") is True,
        "status": "READY_FOR_QUALIFICATION"
        if unit.get("state") in {"VERIFIED_NOT_QUALIFIED", "CONFLICTED"}
        else "INCOMPLETE",
    }


def validate_knowledge_unit(unit: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in ("knowledge_id", "knowledge_type", "title", "claim_id", "evidence_state"):
        if not unit.get(field):
            errors.append(f"missing_{field}")

    if not unit.get("evidence_links"):
        errors.append("missing_evidence_links")

    if unit.get("qualification_required") is not True:
        errors.append("qualification_gate_missing")

    if unit.get("auto_qualified") is not False:
        errors.append("auto_qualification_forbidden")

    if unit.get("state") == "CONFLICTED" and not any(
        link.get("relation") == "CONTRADICTS"
        for link in unit.get("evidence_links", [])
    ):
        errors.append("conflicted_state_without_counter_evidence")

    return errors
