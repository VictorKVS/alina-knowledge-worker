import pytest

@pytest.mark.lifecycle
def test_stale_source_marks_impacted_knowledge(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    src = adapter.ingest_source(job, {"title":"Policy","version":"1","content":"Rule A."})
    adapter.extract(job, src)
    impact = adapter.mark_source_stale(job, src)
    assert impact.get("affected_nodes") is not None

@pytest.mark.lifecycle
def test_delta_impact_analysis_finds_dependents(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    impact = adapter.impact_analysis(job, {"node_id":"METHOD-X"})
    assert "procedures" in impact
    assert "prompts" in impact
    assert "rag" in impact
    assert "tests" in impact
