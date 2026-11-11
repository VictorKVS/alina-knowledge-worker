import pytest


@pytest.mark.contract
def test_same_input_and_policy_do_not_duplicate_units(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)

    source = {
        "title": "Idempotent Source",
        "version": "1",
        "content": "Baseline forecast repeats the last observed value.",
    }

    src1 = adapter.ingest_source(job, source)
    adapter.extract(job, src1)
    count1 = len(adapter.get_units(job))

    src2 = adapter.ingest_source(job, source)
    adapter.extract(job, src2)
    count2 = len(adapter.get_units(job))

    assert count2 == count1
