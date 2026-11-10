# AK-01 Test Adapter Contract v1

## Purpose
Provide a stable behavioral boundary between architecture tests and implementation.

Environment variable:
AK01_TEST_ADAPTER=<python.module>

## Required operations

### Job lifecycle
create_job(target_agent_profile, evidence_policy)
get_capsule(job, version=None)
release_capsule(capsule_or_delta, requalified=None)
create_delta(capsule, delta_spec)

### Source/knowledge
ingest_source(job, source)
extract(job, source, options=None)
get_units(job)
get_contradictions(job)
get_graph(job)
mark_source_stale(job, source)
impact_analysis(job, change)

### Operational knowledge
build_procedure(job, input_spec)
build_checklist(job, input_spec)
build_prompt_package(job)

### Retrieval/policy
rank(job, candidates)

### Qualification/security
qualify(job, actor)

### Failure/audit
simulate_failure(job, failure_kind)
get_events(job)
get_audit(job)

## Contract semantics

### Determinism
For identical:
- input hashes
- target profile version
- policy version
the adapter must not create duplicate durable knowledge artifacts.

### Error semantics
Authorization/invariant violations MUST raise an exception or return an explicit typed failure; silent success is forbidden.

### Version semantics
Released capsule versions are immutable.

### Provenance semantics
Source-derived outputs expose enough provenance fields for executable tests.

### Implementation independence
The adapter may wrap:
- in-process Python
- FastAPI
- Docker deployment
- remote test environment

Tests MUST NOT depend on private implementation internals.

## Software Architect acceptance
The Software Architect must map every adapter operation to:
- module/service owner
- request/response DTO
- persistence transaction
- emitted events
- error model

before production coding begins.
