import pytest

@pytest.mark.contract
def test_prompt_package_is_layered(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    pkg = adapter.build_prompt_package(job)
    required = {
        "system_core","role","domain_policy","evidence_policy",
        "tool_policy","decision_policy","output_contract","escalation_policy"
    }
    assert required.issubset(pkg.keys())
