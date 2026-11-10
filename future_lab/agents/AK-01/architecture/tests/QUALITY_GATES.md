# AK-01 — Quality Gates Before Code and Release

## GATE A — Architecture Testability
PASS only when:
- every critical requirement has at least one test;
- failure reaction is defined;
- security boundary has negative tests;
- data fixtures are specified.

## GATE B — Contract Freeze for MVP
PASS only when:
- API DTOs versioned;
- event envelopes versioned;
- knowledge/capsule schemas versioned;
- inter-agent handoffs have acceptance tests.

## GATE C — Build Admission
Software implementation may start only after A+B PASS.

## GATE D — Pull Request
Required:
- unit tests
- contract tests
- type/lint
- SAST
- dependency scan
- secret scan
- schema tests

## GATE E — Integration
Required:
- PostgreSQL integration
- pgvector retrieval
- object store
- queue/outbox
- model adapter
- graph persistence/rebuild
- failure injection

## GATE F — Security
Required:
- injection
- access isolation
- provenance integrity
- tool policy
- supply chain checks

## GATE G — POLYGON
Required:
- adversarial corpus
- contradictory sources
- stale sources
- large corpus
- provider outage
- corrupted indexes
- regression suite

## GATE H — Release
Only when:
- all mandatory tests green;
- known residual risks recorded;
- rollback verified;
- evidence bundle generated.
