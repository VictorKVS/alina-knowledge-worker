# AK-01 — Security Requirements

Owner: SA-01 Security Architect

## SR-001 Source-as-Data Isolation
Source content MUST never be interpreted as system/control instructions.
Mapped tests:
- test_security.py::test_source_prompt_injection_cannot_change_system_policy

## SR-002 Qualification Separation
AK-01 MUST NOT be authorized to set runtime knowledge/capsule state to QUALIFIED.
Mapped tests:
- test_security.py::test_ak01_cannot_self_qualify

## SR-003 Cross-Agent Namespace Isolation
Knowledge, sources, traces and indexes from one target agent MUST NOT be readable by another unauthorized agent namespace.
Mapped tests:
- test_security.py::test_cross_agent_namespace_isolation

## SR-004 Provenance Integrity
Every source-derived knowledge unit MUST preserve immutable provenance references.
Mapped tests:
- test_provenance.py::test_every_source_derived_unit_has_provenance
- test_provenance.py::test_missing_provenance_blocks_verified_state

## SR-005 Source Integrity
Source mutation/hash mismatch MUST stop or quarantine ingestion.
Mapped architecture test:
- T-020 source hash mismatch stops ingest
Status: executable test required before release.

## SR-006 RAG Trust Enforcement
High similarity MUST NOT override configured source trust/evidence policy.
Mapped tests:
- test_retrieval_policy.py::test_low_trust_high_similarity_does_not_override_policy

## SR-007 Released Capsule Immutability
Released capsule versions MUST be immutable; changes occur only through versioned deltas.
Mapped tests:
- test_lifecycle.py::test_released_capsule_is_immutable

## SR-008 Requalification After Significant Change
A changed specialist capsule MUST NOT be released when required requalification has not passed.
Mapped tests:
- test_lifecycle.py::test_delta_requires_requalification_before_new_release

## SR-009 Auditability
Security-relevant failures and recovery actions MUST generate audit/event evidence.
Mapped tests:
- test_resilience.py::test_failure_produces_auditable_reaction

## SR-010 Least Privilege for Tools
Tool use MUST be controlled by explicit allowlists/permissions.
Status: executable test required before release.

## SR-011 Secret Protection
Secrets MUST NOT be exposed to unapproved external model/tool contexts.
Status: executable test required before release.

## SR-012 Supply-Chain Controls
Dependencies/images MUST pass approved SCA/container/SBOM policies before release.
Validation:
- CI security gate
- SBOM
- dependency scan
- container scan

## SR-013 Safe Degraded Mode
Loss of a derived retrieval/index component MUST NOT silently produce falsely trusted output.
Mapped tests:
- resilience/failure recovery suite

## SR-014 No Silent Knowledge Promotion
Episodic/production observations MUST NOT automatically become reusable VERIFIED/QUALIFIED semantic knowledge.
Validation:
- lifecycle + delta review tests

## SR-015 Security Event Retention
Critical security decisions/events MUST be retained in append-only audit storage.
Validation:
- audit/event tests

## Release rule
Any failed SR-001, SR-002, SR-003, SR-004, SR-005, SR-010 or SR-011 is release-blocking.
