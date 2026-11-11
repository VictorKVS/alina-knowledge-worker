# AK-01 — System API Contract Draft

## Jobs

POST /v1/knowledge-jobs
GET /v1/knowledge-jobs/{job_id}
POST /v1/knowledge-jobs/{job_id}/run
POST /v1/knowledge-jobs/{job_id}/cancel
GET /v1/knowledge-jobs/{job_id}/events

## Target agent

PUT /v1/knowledge-jobs/{job_id}/target-agent
GET /v1/knowledge-jobs/{job_id}/target-agent

## Sources

POST /v1/knowledge-jobs/{job_id}/sources
GET /v1/knowledge-jobs/{job_id}/sources
GET /v1/sources/{source_id}/versions

## Knowledge

GET /v1/knowledge-jobs/{job_id}/units
GET /v1/knowledge-jobs/{job_id}/graph
GET /v1/knowledge-jobs/{job_id}/contradictions
GET /v1/knowledge-jobs/{job_id}/gaps

## Generated artifacts

GET /v1/knowledge-jobs/{job_id}/procedures
GET /v1/knowledge-jobs/{job_id}/checklists
GET /v1/knowledge-jobs/{job_id}/rag-spec
GET /v1/knowledge-jobs/{job_id}/prompt-package
GET /v1/knowledge-jobs/{job_id}/capsule

## Review and lifecycle

POST /v1/capsules/{capsule_id}/reviews
POST /v1/capsules/{capsule_id}/deltas
GET /v1/capsules/{capsule_id}/versions
POST /v1/capsules/{capsule_id}/requalification

## Contract rules

- every write endpoint uses idempotency key;
- every mutable artifact is versioned;
- source-derived fields must carry provenance reference;
- write operations emit audit events;
- QUALIFIED status cannot be set by AK-01 endpoints.
