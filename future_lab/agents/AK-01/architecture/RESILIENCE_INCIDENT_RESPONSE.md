# AK-01 — Resilience and Incident Response

## Resilience patterns
- idempotency keys
- stage checkpoints
- transactional outbox
- retry with exponential backoff
- circuit breaker for model/tool providers
- bulkhead isolation between jobs
- dead-letter queue
- immutable audit events
- source/content hashes
- versioned contracts
- read-only degraded mode

## Incident severity

### SEV-1
- cross-agent data leakage
- provenance corruption
- unauthorized qualification
- systemic prompt injection success
- destructive graph corruption

Reaction:
- freeze affected pipeline
- revoke write path
- preserve evidence
- notify FATHER security gate
- rollback to last known good capsule/version

### SEV-2
- repeated extraction corruption
- major retrieval outage
- graph index corruption
- large-scale job failure

Reaction:
- stop impacted stage
- switch to degraded mode if safe
- rebuild from provenance + source registry

### SEV-3
- single job/parser/model failure
- temporary provider outage

Reaction:
- retry/fallback
- isolate job

## Recovery Point
Authoritative rebuild sources:
- Source Registry
- Object Store
- PostgreSQL metadata
- Audit/Provenance Ledger

Vector and graph indexes are rebuildable derived stores.
