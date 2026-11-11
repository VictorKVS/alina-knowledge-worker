import pytest

@pytest.mark.knowledge
def test_procedure_contains_preconditions_steps_and_stop_conditions(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    result = adapter.build_procedure(job, {
        "method":"ARIMA",
        "task":"time_series_forecasting",
        "limitations":["insufficient_history"]
    })
    assert result.get("steps")
    assert result.get("preconditions") is not None
    assert result.get("stop_conditions") is not None

@pytest.mark.knowledge
def test_checklist_items_are_verifiable(adapter, target_agent_profile, evidence_policy):
    job = adapter.create_job(target_agent_profile, evidence_policy)
    checklist = adapter.build_checklist(job, {"procedure":"forecast"})
    assert checklist.get("items")
    assert all(item.get("criterion") for item in checklist["items"])
