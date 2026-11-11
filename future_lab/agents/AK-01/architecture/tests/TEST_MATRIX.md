# AK-01 — Architecture-to-Test Matrix

| ID | Architectural requirement | Test type | Expected invariant |
|---|---|---|---|
| T-001 | source provenance preserved | integration | every source-derived unit points to versioned fragment |
| T-002 | unsupported claims blocked | negative | claim without evidence cannot become VERIFIED |
| T-003 | contradictions retained | domain | contradictory claims remain linked, neither silently deleted |
| T-004 | dangerous alias merge prevented | negative | ambiguous merge requires review |
| T-005 | contextual relevance explainable | policy | ranking attributes and policy version are recorded |
| T-006 | RAG trust beats similarity policy | retrieval | blocked/low-trust source cannot win solely by similarity |
| T-007 | prompt injection isolated | security | source instructions cannot change system policy |
| T-008 | qualification separation | authorization | AK-01 cannot set QUALIFIED |
| T-009 | capsule version immutable | versioning | released version cannot be silently overwritten |
| T-010 | delta impact traceable | graph | affected procedures/RAG/prompts/tests are discoverable |
| T-011 | vector outage degrades safely | resilience | sparse/graph fallback or controlled failure |
| T-012 | graph index rebuildable | recovery | graph can be reconstructed from authoritative records |
| T-013 | duplicate job idempotent | reliability | same input_hash+policy does not duplicate units |
| T-014 | event bus outage survivable | resilience | outbox retains events for replay |
| T-015 | local knowledge isolated | domain | ORGANIZATION/PROJECT data does not overwrite CORE |
| T-016 | stale source detected | freshness | affected nodes flagged for review |
| T-017 | retraining follows approved delta | lifecycle | no new capsule release without required reassessment |
| T-018 | cross-agent leakage prohibited | security | namespace isolation holds |
| T-019 | malformed LLM JSON handled | robustness | schema repair/retry then safe failure |
| T-020 | source hash mismatch stops ingest | integrity | source quarantined and event emitted |
