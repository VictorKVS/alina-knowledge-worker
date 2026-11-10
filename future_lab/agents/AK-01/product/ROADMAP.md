# AK-01 — Product Roadmap

## R0 — Product Definition
Status: DONE
- Vision
- PRD
- CPMM
- success metrics
- boundaries
- first acceptance target

## R1 — System Design
Goal: executable system specification.
- API contract
- persistence model
- graph model
- job state machine
- retry/idempotency
- source versioning

Exit: AS-01 Gate PASS.

## R2 — MVP Build
Goal: end-to-end execution.
- ingestion
- extraction
- epistemic typing
- provenance
- graph build
- weighting
- RAG spec generator
- prompt spec generator
- blueprint composer

Exit: one Forecasting Agent blueprint generated automatically.

## R3 — QA + Security
- golden datasets
- contradiction benchmark
- injection tests
- source poisoning tests
- citation verification
- regression suite

Exit: AQ-01 and Security gates green.

## R4 — POLYGON
- adversarial corpus
- obsolete sources
- multilingual corpus
- large graph
- false citation pressure
- conflicting standards

Exit: no critical gate failures.

## R5 — Release 1.0
- stable contracts
- Docker
- CI/CD
- observability
- rollback
- documentation

## R6 — Multi-domain
Targets:
- Forecasting
- Security
- OSINT
- DevOps/Kubernetes
- Legal

## R7 — Self-auditing
- stale knowledge scans
- weak evidence scans
- orphan graph scans
- retrieval coverage tests
- prompt grounding tests

## R8 — Adaptive
- feedback from target-agent failures
- controlled weight updates
- RAG improvements
- missing knowledge discovery
