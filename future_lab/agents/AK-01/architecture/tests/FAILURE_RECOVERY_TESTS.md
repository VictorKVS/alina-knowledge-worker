# AK-01 — Failure and Recovery Tests

## F-01 Model Provider Timeout
Expected: exponential backoff; circuit breaker after threshold; auditable failure.

## F-02 Parser Failure
Expected: source quarantine; remaining independent sources continue.

## F-03 PostgreSQL Write Failure
Expected: no false completion; transaction rollback; stage remains retryable.

## F-04 Vector Index Failure
Expected: controlled degradation or explicit unavailable state.

## F-05 Graph Store Failure
Expected: cached/read-only mode if safe; rebuild path exists.

## F-06 Event Bus Failure
Expected: transactional outbox retains event for later replay.

## F-07 Worker Crash Mid-Stage
Expected: checkpoint/idempotency prevents duplicate output.

## F-08 Corrupted Derived Index
Expected: rebuild from Source Registry + PostgreSQL + Provenance Ledger.

## F-09 Partial Capsule Build
Expected: capsule not marked review-ready.

## F-10 Critical Provenance Loss
Expected: fail closed; release frozen; SEV-1/2 policy applied based on scope.

## Recovery assertions
Every recovery test must assert:
- state before failure
- injected failure
- state after failure
- emitted event
- audit record
- retry/escalation decision
- absence of unauthorized promotion
