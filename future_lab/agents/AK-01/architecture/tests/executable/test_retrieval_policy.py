import pytest


@pytest.mark.retrieval
def test_low_trust_high_similarity_does_not_override_policy(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)

    trusted = {
        "id": "trusted-standard",
        "similarity": 0.82,
        "authority": "PRIMARY",
        "trust": 1.0,
    }
    untrusted = {
        "id": "untrusted-blog",
        "similarity": 0.99,
        "authority": "DISCOVERY",
        "trust": 0.1,
    }

    ranked = adapter.rank(job, [untrusted, trusted])

    assert ranked[0]["id"] == "trusted-standard"
