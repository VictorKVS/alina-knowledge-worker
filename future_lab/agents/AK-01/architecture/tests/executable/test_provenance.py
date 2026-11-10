import pytest


@pytest.mark.provenance
def test_every_source_derived_unit_has_provenance(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    src = adapter.ingest_source(
        job,
        {
            "title": "Authoritative Test Source",
            "version": "1.0",
            "content": "ARIMA is a forecasting method for time series.",
        },
    )

    adapter.extract(job, src)
    units = adapter.get_units(job)

    assert units, "Extraction produced no knowledge units"

    for unit in units:
        assert unit.get("source_version_id")
        assert unit.get("source_fragment_id")
        assert unit.get("source_hash")
        assert unit.get("locator")


@pytest.mark.provenance
def test_missing_provenance_blocks_verified_state(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    src = adapter.ingest_source(
        job,
        {"title": "Broken Source", "version": "1.0", "content": "Claim without locator."},
    )

    adapter.extract(job, src, options={"drop_locator": True})
    units = adapter.get_units(job)

    assert units
    assert all(unit.get("state") != "VERIFIED" for unit in units)
