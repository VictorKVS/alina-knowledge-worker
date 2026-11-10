from fastapi.testclient import TestClient

from ak01.api import app


client = TestClient(app)


def test_health():
    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").status_code == 200


def test_job_source_extract_flow():
    create = client.post(
        "/v1/knowledge-jobs",
        json={
            "target_agent": {
                "id": "FORECAST-01",
                "role": "Forecasting Agent",
                "tasks": ["forecast"],
                "required_capabilities": ["time_series"],
            },
            "evidence_policy": {
                "minimum_state_for_runtime_use": "VERIFIED",
                "wikipedia_only_for_qualification": False,
                "require_provenance": True,
            },
        },
    )
    assert create.status_code == 200
    job_id = create.json()["id"]

    src = client.post(
        f"/v1/knowledge-jobs/{job_id}/sources",
        json={
            "title": "Forecasting note",
            "version": "1",
            "content": "Forecasting methods require historical observations.",
            "source_type": "TEXT",
            "locator": "body",
        },
    )
    assert src.status_code == 200

    extract = client.post(f"/v1/knowledge-jobs/{job_id}/extract")
    assert extract.status_code == 200
    assert extract.json()["produced"] >= 1

    units = client.get(f"/v1/knowledge-jobs/{job_id}/units")
    assert units.status_code == 200
    payload = units.json()
    assert payload
    assert payload[0]["provenance"]["source_hash"]
    assert payload[0]["provenance"]["locator"]


def test_missing_job_is_404():
    assert client.get("/v1/knowledge-jobs/missing").status_code == 404
