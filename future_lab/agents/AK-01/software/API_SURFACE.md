# AK-01 — API Surface v1

## Jobs
POST /v1/knowledge-jobs
GET /v1/knowledge-jobs/{job_id}
POST /v1/knowledge-jobs/{job_id}/run
POST /v1/knowledge-jobs/{job_id}/cancel
GET /v1/knowledge-jobs/{job_id}/events

## Sources
POST /v1/knowledge-jobs/{job_id}/sources
GET /v1/knowledge-jobs/{job_id}/sources
GET /v1/sources/{source_id}/versions
POST /v1/sources/{source_id}/mark-stale

## Knowledge
GET /v1/knowledge-jobs/{job_id}/units
GET /v1/knowledge-jobs/{job_id}/graph
GET /v1/knowledge-jobs/{job_id}/contradictions
GET /v1/knowledge-jobs/{job_id}/gaps
POST /v1/knowledge-jobs/{job_id}/impact-analysis

## Operational artifacts
POST /v1/knowledge-jobs/{job_id}/procedures/build
POST /v1/knowledge-jobs/{job_id}/checklists/build
POST /v1/knowledge-jobs/{job_id}/prompt-package/build
GET /v1/knowledge-jobs/{job_id}/rag-spec

## Capsules
GET /v1/knowledge-jobs/{job_id}/capsule
GET /v1/capsules/{capsule_id}/versions
POST /v1/capsules/{capsule_id}/deltas
POST /v1/capsules/{capsule_id}/release
POST /v1/capsules/{capsule_id}/reviews
POST /v1/capsules/{capsule_id}/requalification

## Health
GET /health/live
GET /health/ready

## API rules
- mutating endpoints accept Idempotency-Key
- all responses include correlation_id
- versioned DTOs
- authorization checked before domain execution
- qualification transitions require authorized external actor
