import pytest


@pytest.mark.knowledge
def test_contradictory_claims_are_preserved(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)

    src_a = adapter.ingest_source(
        job,
        {"title": "Source A", "version": "1", "content": "Method X requires condition Y."},
    )
    src_b = adapter.ingest_source(
        job,
        {"title": "Source B", "version": "1", "content": "Method X does not require condition Y."},
    )

    adapter.extract(job, src_a)
    adapter.extract(job, src_b)

    contradictions = adapter.get_contradictions(job)
    units = adapter.get_units(job)

    assert contradictions, "Expected contradiction record"
    texts = [u.get("text", "") for u in units]
    assert any("requires condition Y" in t for t in texts)
    assert any("does not require condition Y" in t for t in texts)
