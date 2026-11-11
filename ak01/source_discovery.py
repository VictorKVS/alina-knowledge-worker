from __future__ import annotations

from copy import deepcopy
from typing import Any

_CHANNELS_BY_SOURCE_TYPE = {
    "body_of_knowledge": ["professional_body", "standards_body", "academic_curriculum"],
    "scholarly_synthesis": ["openalex", "semantic_scholar", "crossref"],
    "canonical_book": ["university_curriculum", "publisher_catalog", "openalex"],
    "primary_research": ["openalex", "semantic_scholar", "crossref"],
    "benchmark": ["primary_research", "official_benchmark", "reproducible_engineering_source"],
    "official_documentation": ["vendor_or_project_official_docs"],
    "practitioner_case": ["engineering_blog", "postmortem_repository", "conference_talk"],
    "official_or_normative_source": ["regulator", "standards_body", "official_registry"],
    "comparative_evidence": ["scholarly_synthesis", "primary_research", "benchmark"],
    "failure_case": ["postmortem_repository", "incident_report", "engineering_blog"],
    "primary_source": ["official_registry", "publisher_version_of_record", "source_owner"],
    "independent_corroboration": ["openalex", "semantic_scholar", "independent_institution"],
    "counter_evidence": ["openalex", "semantic_scholar", "scholarly_synthesis"],
    "authoritative_reference": ["professional_body", "standards_body", "university_curriculum"],
}


def _search_intents(plan: dict[str, Any]) -> list[dict[str, Any]]:
    subject = str(plan.get("subject", ""))
    intents: list[dict[str, Any]] = []
    for question in plan.get("research_questions", []):
        intents.append({
            "subject": subject,
            "question": str(question),
            "query_seed": f"{subject} {question}".strip(),
        })
    return intents


def build_source_discovery_plan(research_plan: dict[str, Any]) -> dict[str, Any]:
    """Translate a research task into auditable source-discovery instructions.

    This stage still does not select or qualify a source. It only decides
    which source classes and discovery channels must be queried.
    """
    source_mix = list(research_plan.get("source_mix", []))
    channels: list[dict[str, Any]] = []

    for source_type in source_mix:
        channels.append({
            "source_type": source_type,
            "channels": deepcopy(
                _CHANNELS_BY_SOURCE_TYPE.get(
                    str(source_type),
                    ["generic_academic_or_official_search"],
                )
            ),
            "purpose": f"Find candidates of type {source_type}",
        })

    return {
        "discovery_plan_id": f'{research_plan.get("plan_id", "PLAN")}:DISCOVERY',
        "derived_from_plan": research_plan.get("plan_id"),
        "subject": research_plan.get("subject"),
        "search_intents": _search_intents(research_plan),
        "source_channels": channels,
        "seed_source_policy": {
            "minimum_seed_roles": [
                "foundation_or_body_of_knowledge",
                "current_synthesis_or_review",
                "primary_or_official_source",
            ],
            "author_expansion_allowed": True,
            "citation_expansion_allowed": True,
            "qualification_required_before_acceptance": True,
        },
        "prohibited_actions": [
            "accept source because it ranks highly in search",
            "accept source because author is famous",
            "accept source because it has DOI or ISBN",
            "promote practitioner discussion to scientific fact without corroboration",
            "select final method before source qualification",
        ],
        "required_candidate_fields": [
            "title",
            "source_type",
            "authors_or_issuer",
            "publication_or_version_date",
            "persistent_identifier_or_official_locator",
            "discovery_channel",
            "reason_found",
        ],
        "status": "DISCOVERY_REQUIRED",
    }


def validate_discovery_plan(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if not plan.get("derived_from_plan"):
        errors.append("missing_research_plan_trace")
    if not plan.get("source_channels"):
        errors.append("missing_source_channels")
    if not plan.get("search_intents"):
        errors.append("missing_search_intents")

    policy = plan.get("seed_source_policy", {})
    if policy.get("qualification_required_before_acceptance") is not True:
        errors.append("qualification_gate_missing")

    return errors
