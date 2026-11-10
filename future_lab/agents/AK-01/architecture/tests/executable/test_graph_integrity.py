import pytest

@pytest.mark.knowledge
def test_graph_has_no_unexplained_orphan_verified_nodes(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    src = adapter.ingest_source(job, {"title":"Graph","version":"1","content":"ARIMA is a method for time-series forecasting."})
    adapter.extract(job, src)
    graph = adapter.get_graph(job)
    for node in graph.get("nodes", []):
        if node.get("state") == "VERIFIED":
            assert node.get("provenance") or node.get("source_fragment_id")
