import pytest


@pytest.mark.security
def test_source_hash_mismatch_quarantines_source(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    src = adapter.ingest_source(
        job,
        {"title":"Integrity Source","version":"1","content":"Trusted content."},
    )
    result = adapter.check_source_integrity(job, src, observed_hash="tampered")
    assert result.get("quarantined") is True
    assert result.get("allowed_for_verified_knowledge") is False


@pytest.mark.security
def test_tool_least_privilege_denies_unapproved_tool(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    with pytest.raises(Exception):
        adapter.invoke_tool(job, tool_name="unapproved_admin_tool", args={})


@pytest.mark.security
def test_secret_not_sent_to_unapproved_external_model(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    result = adapter.send_model_context(
        job,
        provider="external-unapproved",
        context={"text":"password=SUPER_SECRET_TEST_VALUE"},
    )
    assert "SUPER_SECRET_TEST_VALUE" not in str(result)
    assert result.get("blocked") or result.get("redacted")
