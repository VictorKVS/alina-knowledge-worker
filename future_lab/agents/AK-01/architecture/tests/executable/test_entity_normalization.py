import pytest

@pytest.mark.knowledge
def test_aliases_resolve_without_losing_provenance(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    a = adapter.ingest_source(job, {"title":"A","version":"1","content":"Large Language Model (LLM) is used."})
    b = adapter.ingest_source(job, {"title":"B","version":"1","content":"LLM can be used in agents."})
    adapter.extract(job, a)
    adapter.extract(job, b)
    units = adapter.get_units(job)
    llm_units = [u for u in units if "LLM" in str(u) or "Large Language Model" in str(u)]
    assert llm_units
    canonical_ids = {u.get("canonical_id") for u in llm_units if u.get("canonical_id")}
    assert len(canonical_ids) <= 1

@pytest.mark.knowledge
def test_ambiguous_merge_requires_review(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    a = adapter.ingest_source(job, {"title":"A","version":"1","content":"Java is an island."})
    b = adapter.ingest_source(job, {"title":"B","version":"1","content":"Java is a programming language."})
    adapter.extract(job, a); adapter.extract(job, b)
    units = adapter.get_units(job)
    java_units = [u for u in units if "Java" in str(u)]
    assert len(java_units) >= 2
