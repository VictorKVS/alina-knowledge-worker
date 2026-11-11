# AK-01 Executable Architecture Tests

These tests are written **before** production implementation.

They validate architecture contracts, not implementation internals.

## Adapter contract

The future implementation must expose a Python module named by:

```bash
AK01_TEST_ADAPTER=ak01.testing_adapter
```

The module must provide:

- create_job(...)
- ingest_source(...)
- extract(...)
- get_units(...)
- get_contradictions(...)
- rank(...)
- qualify(...)
- get_capsule(...)
- create_delta(...)
- release_capsule(...)
- simulate_failure(...)
- get_events(...)
- get_audit(...)

The adapter may call a local service, in-process application, Docker environment, or remote test deployment.

## Running

```bash
pytest future_lab/agents/AK-01/architecture/tests/executable -q
```

Without AK01_TEST_ADAPTER the suite is skipped.

At BUILD ADMISSION / CI the variable becomes mandatory and skipping is treated as a gate failure.

## Markers

- contract
- provenance
- knowledge
- security
- resilience
- lifecycle
- retrieval
