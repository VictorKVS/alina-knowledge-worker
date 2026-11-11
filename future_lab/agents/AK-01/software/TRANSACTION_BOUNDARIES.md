# AK-01 — Transaction and Consistency Boundaries

## Atomic operations
- create job + initial audit event
- register source version + hash metadata
- create knowledge unit + provenance link
- release capsule version + outbox event
- approve/reject knowledge delta + audit event
- qualification record + status transition

## Outbox
Business state and outbox event are committed in one DB transaction.
Publisher sends events asynchronously and marks them delivered.

## Idempotency
Mutating commands accept idempotency keys.
Natural key includes:
- operation
- target/job id
- input hash
- policy version

## Eventual consistency
Allowed for:
- vector indexing
- graph snapshot rebuild
- analytics/metrics
- secondary search indexes

## Fail-closed consistency
Required for:
- provenance
- authorization
- qualification
- released capsule versioning
