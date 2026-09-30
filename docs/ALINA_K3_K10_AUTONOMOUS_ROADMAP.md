# ALINA K3→K10 Autonomous Roadmap

Status: canonical implementation roadmap
Branch: `feature/alina-k3-k10-autopilot`

## Mission

Develop the existing ALINA Knowledge Worker into ALINA Analyst Expert without replacing the proven ingestion pipeline.

Core invariant:

`Source → Fragment → Evidence → Knowledge → Reasoning → Evaluation → Controlled Improvement`

Mechanical extraction is never equivalent to verified knowledge.

## Human involvement

Normal implementation is autonomous. Human approval is required only for:
1. Gate A — Evidence/Knowledge architecture freeze.
2. Gate B — Knowledge promotion policy.
3. Gate C — self-modification/security policy.
4. Gate D — K10 production certification.

Secrets, paid external services, destructive operations, security-boundary changes and production promotion always require human approval.

## Existing foundation

K0 Source discovery — existing.
K1 Catalog/identity/dedup — existing/partial.
K2 Extraction/OCR/provenance — existing.
K3 Evidence — partial.

Existing `alina.py`, extractors, SQLite/FTS5, study routing, provenance, visual evidence, dashboard and tests are retained.

## K3 — Unified Evidence Core

Deliver:
- Source, Fragment, Evidence, Observation, ClaimCandidate schemas.
- Stable IDs and source SHA/locator traceability.
- Evidence lifecycle: RAW → EXTRACTED → REVIEWED → VERIFIED/REJECTED.
- Migration/adapters for existing chunks, reading_notes and visual evidence.

DoD:
- every promoted object traces to source + locator;
- no existing extraction/search regression;
- synthetic tests cover provenance and invalid transitions;
- Gate A artifact produced.

## K4 — Knowledge Extraction

Deliver:
- KnowledgeCandidate schema;
- Concept, Claim, Method, Rule, Procedure, Pattern, AntiPattern, Definition, Constraint, Example, CounterExample;
- extraction provider interface;
- candidate deduplication;
- contradiction capture;
- no direct LLM write to production KB.

DoD:
- deterministic schema validation;
- every candidate has evidence;
- unsupported candidates are rejected/quarantined;
- baseline extraction benchmark exists.

## K5 — ALINA Knowledge Core

Deliver:
- ALINA_ANALYST_KB;
- domain taxonomy for analytical thinking, research, critical thinking, evidence, hypotheses, causal/comparative analysis, intelligence analysis, OSINT, fact-checking, knowledge engineering, IR/RAG/GraphRAG, LLM evaluation and agent engineering;
- candidate → verified → approved knowledge promotion;
- semantic dedup and multi-source support.

DoD:
- production KB contains only policy-valid objects;
- source conflicts remain visible;
- version/history/rollback supported;
- Gate B artifact produced.

## K6 — Knowledge Graph

Deliver:
- typed nodes and edges;
- Knowledge↔Evidence↔Source graph;
- Method/Concept/Claim relations;
- graph validation and orphan detection;
- ontology registry with versioning.

DoD:
- every knowledge node has provenance path;
- graph integrity tests pass;
- invalid/orphan relations are quarantined.

## K7 — RAG v2 / GraphRAG

Deliver:
- retain FTS5 lexical retrieval;
- vector provider interface;
- metadata filtering;
- hybrid fusion;
- reranker interface;
- graph expansion;
- context builder with citations;
- retrieval evaluation.

DoD:
- FTS-only baseline retained;
- hybrid strategies benchmarked against baseline;
- retrieval metrics stored, not guessed;
- fallback works when optional model/provider is unavailable.

## K8 — Analyst Reasoning Engine

Deliver:
- task classifier/router;
- Methods Registry;
- Prompt Registry/Prompt Stack;
- research, comparison, hypothesis, verification, contradiction, timeline, causal and synthesis workflows;
- Critic and Fact Checker stages;
- explicit insufficient-evidence result.

DoD:
- facts/claims/hypotheses/conclusions remain distinct;
- key conclusions trace to evidence;
- workflows are reproducible from run manifests.

## K9 — Evaluation & Competency Lab

Deliver:
- ALINA competency model;
- benchmark registry;
- synthetic/golden test cases;
- grounding, retrieval, contradiction, reasoning and hallucination-resistance metrics;
- regression detection;
- gap clustering/root-cause diagnosis.

DoD:
- every reported score derives from stored test results;
- benchmark version is recorded;
- regressions block promotion;
- competency gaps generate machine-readable learning tasks.

## K10 — Controlled Self-Improvement

Deliver:
- production/candidate separation;
- Observe→Measure→Diagnose→Research→Propose→Test→Evaluate→Promote/Reject→Monitor loop;
- learning-task queue;
- candidate KB/prompt/method/RAG branches;
- rollback;
- audit trail;
- human-controlled production promotion.

DoD:
- ALINA cannot silently rewrite production core;
- candidate must beat/equal policy thresholds without critical regression;
- security and provenance tests pass;
- Gate C completed;
- Gate D certification report generated.

## Autopilot execution rule

For each task:
`PLAN → IMPLEMENT → TEST → MEASURE → DOCUMENT → COMMIT → NEXT`

On failure:
`DIAGNOSE → SAFE FIX → RETEST`

Escalate only after retry budget is exhausted or a human-only boundary is reached.

No readiness percentages are invented. Stage completion is derived only from machine-checkable DoD evidence.
