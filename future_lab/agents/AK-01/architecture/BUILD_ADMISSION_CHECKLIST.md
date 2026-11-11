# AK-01 — Build Admission Checklist

## Required before Software Architecture / CODEX

### Product
- [x] Product Vision
- [x] PRD
- [x] CPMM
- [x] Success Metrics
- [x] PM Decision

### Business
- [x] End-to-end process
- [x] Use cases
- [x] continuous learning loop
- [x] knowledge layers
- [x] traceability

### System
- [x] logical architecture
- [x] domain data model
- [x] API draft
- [x] event model
- [x] persistence model
- [x] failure/retry/idempotency

### Agent Architecture
- [x] components
- [x] handoffs
- [x] algorithms/decision logic
- [x] runtime sequences
- [x] resilience
- [x] memory model

### Knowledge Architecture
- [x] core scope
- [x] ontology v1
- [x] runtime knowledge layers
- [x] bootstrap plan

### Tests
- [x] architecture test matrix
- [x] provenance tests
- [x] contradiction tests
- [x] security tests
- [x] retrieval policy tests
- [x] idempotency tests
- [x] lifecycle tests
- [x] resilience tests
- [x] entity normalization tests
- [x] graph integrity tests
- [x] knowledge layer tests
- [x] procedure/checklist tests
- [x] prompt package tests
- [x] freshness/impact tests

### Security
- [x] threat model
- [x] trust boundaries
- [x] mandatory controls
- [ ] security requirements IDs mapped to executable tests

### Qualification
- [x] AK-01 qualification exam
- [ ] golden corpus finalized
- [ ] all mandatory test adapter methods implemented

## Current verdict
**CONDITIONAL PASS**

Software Architect may begin detailed design.
Production implementation may begin only when:
1. security requirements are mapped to tests;
2. golden qualification corpus is frozen;
3. AK01_TEST_ADAPTER contract is accepted by Software Architect.
