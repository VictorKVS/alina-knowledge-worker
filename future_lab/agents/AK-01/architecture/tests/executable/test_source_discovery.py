import pytest

from ak01.research_planning import build_research_plan
from ak01.source_discovery import (
    build_source_discovery_plan,
    validate_discovery_plan,
)
from ak01.work_analysis import decompose_work


@pytest.mark.knowledge
def test_discovery_plan_is_traced_to_research_plan():
    trace = decompose_work({
        "id": "CASE-SD1",
        "goal": "Choose a retrieval method",
        "tasks": ["Select retrieval strategy"],
    })
    finding = next(item for item in trace["findings"] if item["type"] == "MISSING_METHOD")
    research = build_research_plan(trace, finding)

    discovery = build_source_discovery_plan(research)

    assert discovery["derived_from_plan"] == research["plan_id"]
    assert validate_discovery_plan(discovery) == []
    assert discovery["seed_source_policy"]["qualification_required_before_acceptance"] is True


@pytest.mark.knowledge
def test_book_and_research_sources_map_to_distinct_discovery_channels():
    research = {
        "plan_id": "RP-1",
        "subject": "information retrieval evaluation",
        "research_questions": ["What metrics are appropriate?"],
        "source_mix": ["canonical_book", "primary_research"],
    }

    discovery = build_source_discovery_plan(research)
    by_type = {
        item["source_type"]: item["channels"]
        for item in discovery["source_channels"]
    }

    assert "university_curriculum" in by_type["canonical_book"]
    assert "openalex" in by_type["primary_research"]
    assert "crossref" in by_type["primary_research"]


@pytest.mark.knowledge
def test_discovery_does_not_accept_sources_by_popularity_or_identifier():
    research = {
        "plan_id": "RP-2",
        "subject": "RAG",
        "research_questions": ["What are the foundational sources?"],
        "source_mix": ["canonical_book", "primary_research"],
    }

    discovery = build_source_discovery_plan(research)
    prohibited = " ".join(discovery["prohibited_actions"]).lower()

    assert "doi or isbn" in prohibited
    assert "author is famous" in prohibited
    assert "ranks highly" in prohibited
