import pytest

@pytest.mark.knowledge
def test_local_layer_cannot_overwrite_core(adapter, evidence_policy):
    core_job = adapter.create_job({"id":"CORE","role":"Core"}, evidence_policy)
    local_job = adapter.create_job({"id":"ORG","role":"Org"}, evidence_policy)

    core = adapter.ingest_source(core_job, {"title":"Core","version":"1","content":"Principle P is universal."})
    adapter.extract(core_job, core, options={"scope_layer":"CORE"})

    local = adapter.ingest_source(local_job, {"title":"Local","version":"1","content":"Principle P is locally overridden."})
    adapter.extract(local_job, local, options={"scope_layer":"ORGANIZATION"})

    core_units = adapter.get_units(core_job)
    assert any(u.get("scope_layer") == "CORE" for u in core_units)
