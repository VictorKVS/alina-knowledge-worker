# AIR-001 Project Charter
**Status:** design candidate, not launched.

## Problem statement
ALINA must solve IB/architecture/RAG questions with version-correct citations and reproducible reasoning. Current gap: source provenance, independent confirmation, reproducible retrieval comparison, abstention on insufficient evidence and tested prompt constraints.

## Boundaries
Within ALINA Analyst block, OSINT acts as research supplier using common FATHER OSINT engine. No separate CRM, frontend, graph DB or channel runner. Source channels: permissible public docs, official vendor/API docs, research papers, public GitHub source/issues, authorized test Telegram sources; other connectors later after separate permission check.

## Functional requirements
FR-01 accept ResearchRequest with scoped question, intended decision and evaluation.
FR-02 generate SearchPlan with multilingual keywords, primary-source priorities, exclusions and budget.
FR-03 preserve source and document versions, dates, license, hash when authorized.
FR-04 claim extraction with exact location and counterevidence.
FR-05 distinguish independent evidence from copies/forward chains.
FR-06 publish candidate Knowledge Pack into quarantine with no auto-promotion.
FR-07 propose prompt/RAG adjustments as change requests with regression tests.
FR-08 define change watchers for new releases, security advisories, outdated technical practices.
FR-09 provide graph trace from question to claim to evidence to decision to test.
FR-10 perform security/privacy/license gates and full audit trail.

## NFR
Reproducibility, explainable citations, scoped permissions, idempotent import, source freshness, offline-compatible test corpus, bounded resource use and stable service contracts.

## Three concept options
A) manual evidence registry and guided search; low risk, low automation;
B) existing OSINT_deepseek collector + semi-automated verification + human review (**preferred pilot candidate**);
C) full multi-agent automatic research platform; deferred due uncertain reliability, expense and permissions.
Selection must be ratified with PoC quality and TCO data. No fabricated ROI.

## Risks
Correlated reposts treated as independent; outdated legal text; model-generated citations; prompt injection; private data leakage; license drift; repository lock-in; noisy watchers.
