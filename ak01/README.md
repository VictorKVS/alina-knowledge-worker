# AK-01 Runtime MVP

Run:

```bash
python -m pip install -r requirements-ak01.txt
uvicorn ak01.api:app --reload
```

Initial endpoints:
- GET /health/live
- GET /health/ready
- POST /v1/knowledge-jobs
- GET /v1/knowledge-jobs/{job_id}
- POST /v1/knowledge-jobs/{job_id}/sources

The architecture tests continue to use `ak01.testing_adapter`.
The production-shaped service and the adapter converge incrementally.
