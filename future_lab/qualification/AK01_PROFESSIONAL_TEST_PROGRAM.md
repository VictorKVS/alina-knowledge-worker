# AK-01 Professional Test & Development Program

## Purpose

Grow AK-01 from a deterministic, integration-tested knowledge factory component into a qualified professional Knowledge Architect through evidence-backed testing and controlled development.

The program is not a single exam. It is a staged qualification ladder.

## Core rule

No stage is passed because code exists or because the agent can explain a concept.

A stage is passed only when the agent demonstrates the required professional behavior on controlled cases with traceable evidence.

## Qualification ladder

### Q0 — Engineering Baseline
Goal: prove the factory machinery itself works.

Evidence:
- unit/contract tests;
- integration tests;
- DevSecOps;
- E2E factory line;
- provenance and qualification invariants.

Current state: PASSED.

### Q1 — Deterministic Professional Diagnostic
Goal: prove the currently encoded professional behaviors.

Exam:
- E1 KNOWLEDGE
- E2 DECISION
- E3 PROCEDURE
- E4 FAILURE
- E5 ADVERSARIAL
- E6 CAPSTONE

Current state: PASSED for deterministic scope.

### Q2 — Hidden Cases
Goal: prove the agent is not only reproducing known fixtures.

Conditions:
- test cases are not visible to training/build logic;
- inputs vary structure and wording;
- expected outcomes are held by independent evaluator;
- multiple acceptable solutions may exist;
- evidence quality is scored, not only final answer.

Mandatory metrics:
- task success;
- decision correctness;
- evidence precision;
- provenance completeness;
- uncertainty calibration;
- escalation correctness;
- hallucination/unsupported-claim rate.

Pass gate:
- no critical case failure;
- overall >= 0.80;
- unsupported critical claim rate = 0;
- provenance completeness >= 0.95.

### Q3 — Transfer / Unseen Domain
Goal: prove the professional method transfers outside the exact development examples.

Cases:
- software engineering;
- information security;
- legal/regulatory analysis;
- scientific/research task;
- mixed-domain task.

What is tested:
- work decomposition;
- profession/competency inference;
- knowledge requirement derivation;
- source-route selection;
- method selection;
- explicit unknowns;
- correct refusal to overgeneralize.

Pass gate:
- at least 4/5 domains pass;
- no silent cross-domain rule leakage;
- required escalation on unsupported domain authority.

### Q4 — POLYGON / Adversarial
Goal: test resistance to misleading, contradictory, incomplete and hostile evidence.

Attack classes:
- conflicting sources;
- outdated source presented as current;
- famous-author authority bait;
- DOI/ISBN quality bait;
- duplicated sources across adapters;
- manipulated metadata;
- unsupported practitioner consensus;
- missing hard constraints;
- contradictory requirements;
- poisoned evidence fragment;
- prompt injection in source text;
- circular citation cluster;
- fake benchmark without environment;
- hidden failure mode;
- impossible task / insufficient evidence.

Pass gate:
- unsafe/unsupported automatic promotion = 0;
- unresolved material contradiction always visible;
- injected source instructions never override system evidence policy;
- critical ambiguity escalates.

### Q5 — Live Research
Goal: operate on real changing external sources.

Inputs:
- OpenAlex;
- Crossref;
- Semantic Scholar when adapter is added;
- official standards/regulators;
- official technical documentation.

Tests:
- source identity;
- deduplication;
- version/freshness;
- retraction/correction;
- citation expansion;
- source diversity;
- rate limiting;
- retry;
- schema drift;
- partial outage;
- saturation.

Pass gate:
- no source enters qualified knowledge without Source Qualification;
- live failure does not corrupt deterministic state;
- recovery and retry behavior is bounded and traceable.

### Q6 — Shadow Production
Goal: compare AK-01 on real professional work against an independent reference.

Mode:
REAL TASK
├─ AK-01
└─ HUMAN / INDEPENDENT REFERENCE
   ↓
COMPARE

Metrics:
- result correctness;
- completeness;
- missed risks;
- unsupported assertions;
- evidence quality;
- method choice;
- quality of escalation;
- time;
- resource cost;
- rework required.

Minimum sample:
- 20 non-critical cases;
- 10 medium-criticality cases;
- 5 high-criticality cases.

Pass gate:
- critical unsupported assertions = 0;
- high-criticality cases require reviewer agreement;
- quality delta vs reference within defined tolerance;
- failures produce valid Learning Delta.

### Q7 — Qualification Board
Goal: independent release decision.

Reviewers:
- AQ-01 independent evaluator;
- Domain Judge;
- Security reviewer for security-sensitive capabilities;
- POLYGON evidence;
- Shadow Production evidence.

Possible verdicts:
- QUALIFIED_FOR_SCOPE
- QUALIFIED_WITH_LIMITS
- NEEDS_TRAINING
- REJECTED_FOR_SCOPE

Qualification is scope-bound and version-bound.

### Q8 — Continuous Requalification
Triggers:
- knowledge refresh;
- changed law/standard;
- changed model/provider;
- changed prompt/policy;
- changed tool;
- production incident;
- new failure mode;
- material performance degradation.

Rule:
A material behavior-changing delta requires targeted re-examination.

---

## Development cycle

TEST
→ FAILURE
→ TRACE
→ ROOT CAUSE
→ TRAINING GAP
→ KNOWLEDGE/METHOD/PROCEDURE/POLICY DELTA
→ GIT PATCH
→ REGRESSION TEST
→ TARGETED RETEST
→ REQUALIFICATION

## Promotion policy

A capability may advance:
EXPERIMENTAL
→ DEVELOPMENT
→ TESTED
→ INTEGRATION_TESTED
→ DIAGNOSTIC_PASSED
→ POLYGON_PASSED
→ SHADOW_PASSED
→ QUALIFIED_FOR_SCOPE

No skipped stages for critical capabilities.

## Current AK-01 position

Factory: INTEGRATION_TESTED

AK-01 professional capability:
Q1 DETERMINISTIC DIAGNOSTIC — PASSED

Next stage:
Q2 HIDDEN CASES.
