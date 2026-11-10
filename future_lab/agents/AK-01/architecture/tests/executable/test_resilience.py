import pytest


@pytest.mark.resilience
@pytest.mark.parametrize(
    "failure_kind",
    ["model_timeout", "vector_index_down", "event_bus_down", "worker_crash"],
)
def test_failure_produces_auditable_reaction(adapter, target_agent_profile, evidence_policy, failure_kind):
    job = adapter.create_job(target_agent_profile, evidence_policy)

    adapter.simulate_failure(job, failure_kind)

    events = adapter.get_events(job)
    audit = adapter.get_audit(job)

    assert events, f"No events emitted for {failure_kind}"
    assert audit, f"No audit record for {failure_kind}"

    serialized = str(events) + str(audit)
    assert failure_kind in serialized
    assert "QUALIFIED" not in serialized or "unauthorized" in serialized.lower()
