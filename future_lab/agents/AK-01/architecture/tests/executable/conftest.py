import importlib
import os
import pytest


REQUIRED_METHODS = {
    "create_job",
    "ingest_source",
    "extract",
    "get_units",
    "get_contradictions",
    "rank",
    "qualify",
    "get_capsule",
    "create_delta",
    "release_capsule",
    "simulate_failure",
    "get_events",
    "get_audit",
}


@pytest.fixture(scope="session")
def adapter():
    module_name = os.getenv("AK01_TEST_ADAPTER")
    if not module_name:
        pytest.skip("AK01_TEST_ADAPTER is not configured")

    module = importlib.import_module(module_name)
    missing = sorted(name for name in REQUIRED_METHODS if not hasattr(module, name))
    if missing:
        pytest.fail(f"AK-01 test adapter missing methods: {missing}")

    return module


@pytest.fixture
def target_agent_profile():
    return {
        "id": "FTH-FORECAST-TEST",
        "role": "Forecasting Agent",
        "tasks": ["time_series_forecasting"],
        "required_capabilities": ["method_selection", "backtesting"],
    }


@pytest.fixture
def evidence_policy():
    return {
        "minimum_state_for_runtime_use": "VERIFIED",
        "wikipedia_only_for_qualification": False,
        "require_provenance": True,
    }
