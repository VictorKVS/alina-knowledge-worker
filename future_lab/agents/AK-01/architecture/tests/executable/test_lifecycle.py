import pytest


@pytest.mark.lifecycle
def test_released_capsule_is_immutable(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    capsule = adapter.get_capsule(job)

    released = adapter.release_capsule(capsule)
    original_version = released["version"]

    delta = adapter.create_delta(
        released,
        {
            "root_cause": "LOCAL_KNOWLEDGE_MISSING",
            "changes": [{"op": "add", "path": "/knowledge/local_rule", "value": "X"}],
        },
    )

    assert delta["base_version"] == original_version
    assert adapter.get_capsule(job, version=original_version) == released


@pytest.mark.lifecycle
def test_delta_requires_requalification_before_new_release(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    capsule = adapter.release_capsule(adapter.get_capsule(job))

    delta = adapter.create_delta(
        capsule,
        {"root_cause": "PROCEDURE_INCORRECT", "changes": [{"op": "replace", "path": "/procedure/1"}]},
    )

    with pytest.raises(Exception):
        adapter.release_capsule(delta, requalified=False)
