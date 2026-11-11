# AK-01 — FATHER Product Lifecycle

Product: **AK-01 ALINA Knowledge Architect**  
Type: Meta-Agent / Knowledge Engineering Factory Station  
Current maturity: **DESIGNED, NOT YET PRODUCTION-QUALIFIED**

---

## STAGE 00 — IDEA / CONCEPT

### Problem
FATHER needs agents with domain knowledge, prompts, RAG, knowledge graphs, weights, evidence policies and update mechanisms.

Building these manually for every agent does not scale and leads to:
- inconsistent knowledge structures;
- weak provenance;
- duplicated RAG pipelines;
- ad-hoc prompts;
- missing contradictions;
- unverifiable weights;
- poor maintainability.

### Product idea
Create a meta-agent that can design the knowledge system of any target agent.

### Formula

SOURCE CORPUS
+ TARGET AGENT ROLE
+ TASKS
+ CAPABILITIES
+ EVIDENCE POLICY
+ OPERATIONAL CONSTRAINTS
=
AGENT KNOWLEDGE BLUEPRINT

### Gate 00
Status: PASS

Reason: problem and product boundary are explicit.

---

## STAGE 01 — PM-01 PRODUCT MANAGER

### Users
- FATHER Architect
- Agent Architect
- Knowledge Curator
- Training Architect
- Security Architect
- Domain teams

### Jobs to be done
1. Build a knowledge architecture for a target agent.
2. Convert sources into structured knowledge units.
3. Build knowledge graphs and contextual weights.
4. Design target-agent RAG.
5. Design layered prompt architecture.
6. Identify missing knowledge and contradictions.
7. Produce a machine-readable Agent Knowledge Blueprint.

### Value
Reduce repeated manual knowledge engineering and make agent knowledge traceable, reusable and testable.

### MVP
Input:
- target agent profile;
- 1–20 source documents;
- extraction/evidence policy.

Output:
- knowledge units;
- graph;
- weights;
- RAG spec;
- prompt spec;
- gaps;
- provenance;
- Agent Knowledge Blueprint.

### Non-goals
- autonomous production qualification;
- autonomous curriculum generation;
- autonomous destructive changes to production agents.

### Success metrics
- source traceability coverage >= 95%;
- unsupported factual claims in generated blueprint = 0 in golden tests;
- knowledge-unit schema validity = 100%;
- contradiction retention = 100% for benchmark cases;
- retrieval grounding pass rate >= 90%;
- target-task knowledge coverage measured against benchmark set.

### Gate 01
Status: PASS WITH METRICS TO VALIDATE

---

## STAGE 02 — AB-01 BUSINESS ANALYSIS

### Business process

REQUEST
→ TARGET AGENT DECOMPOSITION
→ SOURCE INTAKE
→ EXTRACTION
→ NORMALIZATION
→ EVIDENCE LINKING
→ GRAPH BUILD
→ WEIGHTING
→ RAG DESIGN
→ PROMPT DESIGN
→ GAP ANALYSIS
→ BLUEPRINT
→ REVIEW

### Functional requirements
FR-01 ingest heterogeneous sources.
FR-02 preserve source/version/page/section provenance.
FR-03 extract typed knowledge.
FR-04 classify epistemic status.
FR-05 create typed graph nodes and edges.
FR-06 assign contextual weights.
FR-07 detect contradictions.
FR-08 design target-agent RAG.
FR-09 design layered prompt architecture.
FR-10 produce knowledge blueprint.
FR-11 expose gaps/unknowns.
FR-12 hand off prerequisites to Training Architect.

### Business rules
- no unsupported source claim;
- Wikipedia cannot independently qualify knowledge;
- contradictions are retained;
- weights are contextual, not absolute truth;
- critical policy changes require human approval.

### Gate 02
Status: PASS

---

## STAGE 03 — AS-01 SYSTEM ANALYSIS

### Core entities
- Source
- SourceVersion
- TargetAgentProfile
- KnowledgeUnit
- Claim
- Evidence
- CounterEvidence
- Contradiction
- KnowledgeNode
- KnowledgeEdge
- WeightVector
- RAGSpec
- PromptSpec
- KnowledgeGap
- AgentKnowledgeBlueprint

### Core states

Knowledge:
RAW → EXTRACTED → VERIFIED → QUALIFIED → DEPRECATED

Job:
CREATED → INGESTING → EXTRACTING → NORMALIZING → GRAPHING → DESIGNING_RAG → DESIGNING_PROMPT → REVIEW → COMPLETE | FAILED

### Main APIs

POST /knowledge-jobs
GET /knowledge-jobs/{id}
POST /knowledge-jobs/{id}/sources
POST /knowledge-jobs/{id}/target-agent
POST /knowledge-jobs/{id}/run
GET /knowledge-jobs/{id}/blueprint
GET /knowledge-jobs/{id}/graph
GET /knowledge-jobs/{id}/gaps
GET /knowledge-jobs/{id}/evidence

### Required persistence
- relational store for jobs/metadata;
- object storage for source files;
- vector index for semantic retrieval;
- graph store or graph abstraction;
- immutable provenance/audit log.

### Gate 03
Status: PARTIAL

Missing:
- executable API contract;
- persistence implementation;
- migration schema;
- retry/idempotency policy.

---

## STAGE 04 — AA-01 AGENT ARCHITECTURE

### AK-01 internal modules

AK-01
├── Task/Role Decomposer
├── Source Classifier
├── Knowledge Extractor
├── Epistemic Classifier
├── Entity Normalizer
├── Claim-Evidence Linker
├── Contradiction Engine
├── Knowledge Graph Builder
├── Weighting Engine
├── RAG Architect
├── Prompt Architect
├── Gap Detector
├── Blueprint Composer
└── Self-Audit

### Agent memory
- working memory: current extraction job;
- episodic memory: prior blueprint jobs;
- semantic memory: AK-01 own knowledge base;
- procedural memory: extraction/RAG/prompt/graph policies.

### Tool access
READ:
- source corpus
- metadata
- knowledge registry
- target-agent definitions

WRITE:
- extracted knowledge workspace
- graph
- blueprint
- gaps

DENIED BY DEFAULT:
- production target-agent modification
- source deletion
- qualification promotion

### Gate 04
Status: PASS AT DESIGN LEVEL

---

## STAGE 05 — APO-01 SOFTWARE ARCHITECTURE

### Reference architecture

SOURCE ADAPTERS
      ↓
INGESTION
      ↓
PARSER / NORMALIZER
      ↓
KNOWLEDGE PIPELINE
      ↓
┌───────────────────────────┐
│ Knowledge Store           │
│ Vector Index              │
│ Graph Store               │
│ Provenance Ledger         │
└───────────────────────────┘
      ↓
AK-01 ORCHESTRATOR
      ↓
BLUEPRINT API

### Recommended implementation profile
- Python 3.12
- FastAPI
- PostgreSQL
- pgvector
- object storage abstraction
- NetworkX first, graph DB adapter later
- Pydantic contracts
- background job queue only when needed
- OpenTelemetry
- pytest

### Design rules
- model/provider independent;
- retrieval-provider independent;
- graph-backend independent;
- configuration driven;
- all outputs schema validated;
- all source-derived fields provenance linked.

### Gate 05
Status: PARTIAL

Missing executable implementation.

---

## STAGE 06 — SA-01 SECURITY ARCHITECTURE

### Threats
1. Prompt injection in source documents.
2. Malicious or poisoned knowledge sources.
3. False provenance.
4. Cross-agent data leakage.
5. Unauthorized source access.
6. RAG poisoning.
7. Tool abuse.
8. Silent model hallucination.
9. Supply-chain compromise.
10. Sensitive data extraction.

### Mandatory controls
- treat source text as untrusted data;
- never execute instructions from source content;
- source allow/deny policy;
- content hashing;
- source/version provenance;
- tenant/agent namespace separation;
- least privilege;
- immutable audit;
- output schema validation;
- citation verification;
- secret isolation;
- dependency scanning;
- human gate for critical knowledge-policy changes.

### Gate 06
Status: DESIGN PASS / IMPLEMENTATION PENDING

---

## STAGE 07 — FATHER_CODEX BUILD

### Required deliverables
- service skeleton;
- domain models;
- contracts;
- ingestion pipeline;
- extraction pipeline;
- graph builder;
- weighting engine;
- RAG spec generator;
- prompt spec generator;
- blueprint composer;
- CLI/API;
- sample configuration;
- tests.

### Gate 07
Status: NOT STARTED

---

## STAGE 08 — TIMA / DEVSECOPS

### Required
- Dockerfile
- compose
- dependency lock
- CI
- lint/typecheck/test
- SAST
- secret scan
- dependency scan
- SBOM
- container scan
- observability
- resource limits

### Gate 08
Status: NOT STARTED

---

## STAGE 09 — AQ-01 QA / EVALUATOR

### Golden test suites
A. Provenance tests
B. Knowledge extraction tests
C. Epistemic typing tests
D. Contradiction tests
E. Graph topology tests
F. Weight-policy tests
G. RAG retrieval tests
H. Prompt-grounding tests
I. Schema tests
J. Regression tests

### Critical negative tests
- malicious instructions inside PDF;
- two sources disagree;
- obsolete source vs new source;
- Wikipedia-only claim;
- missing page metadata;
- duplicated concept aliases;
- unsupported formula;
- low-authority highly similar retrieval result.

### Gate 09
Status: NOT STARTED

---

## STAGE 10 — POLYGON

### Scenarios
P-01 poisoned corpus
P-02 prompt injection document
P-03 contradictory standards
P-04 stale documentation
P-05 missing evidence
P-06 false citation candidate
P-07 100k-node graph
P-08 huge mixed corpus
P-09 multilingual corpus
P-10 adversarial target-agent profile

### Pass conditions
No unauthorized execution.
No silent evidence promotion.
No cross-agent leakage.
No unsupported QUALIFIED status.
All critical decisions auditable.

### Gate 10
Status: NOT STARTED

---

## STAGE 11 — RELEASE

Release criteria:
- API stable;
- contracts versioned;
- golden suite green;
- security gates green;
- provenance coverage target met;
- reproducible Docker build;
- rollback path;
- documentation;
- example Forecasting Agent blueprint.

Status: NOT READY

---

## STAGE 12 — SRE / OBSERVATION

Metrics:
- extraction throughput
- schema failure rate
- unsupported claim rate
- retrieval hit rate
- citation coverage
- contradiction detection recall
- graph orphan rate
- stale source rate
- job failure/retry rate
- latency
- tokens/cost
- CPU/RAM/GPU
- energy when measurable

Status: PLANNED

---

## STAGE 13 — AU-01 / ANALYSIS

Analyze:
- failed extractions;
- retrieval misses;
- false contradictions;
- weak sources;
- prompt failures;
- graph quality;
- knowledge coverage.

Status: PLANNED

---

## STAGE 14 — IMPROVEMENT LOOP

OBSERVATION
→ FAILURE CASE
→ ROOT CAUSE
→ KNOWLEDGE / PROMPT / RAG / WEIGHT UPDATE
→ TEST
→ POLYGON
→ RELEASE

Status: PLANNED

---

# Current FATHER verdict

AK-01 has passed:
- IDEA
- PRODUCT
- BUSINESS
- AGENT DESIGN

AK-01 is partially complete at:
- SYSTEM ANALYSIS
- SOFTWARE ARCHITECTURE
- SECURITY ARCHITECTURE

AK-01 has NOT yet passed:
- BUILD
- DEVSECOPS
- QA
- POLYGON
- RELEASE
- PRODUCTION

## Current maturity

F1–F2 boundary:
- standardized concept;
- reusable contracts;
- architecture defined;
- not yet executable/qualified.

## Next factory operation

Build AK-01 MVP end-to-end on one real target:

**TARGET: FATHER Forecasting Agent**

Acceptance demo:

BOOK/PAPER
→ AK-01
→ Knowledge Units
→ Weighted Knowledge Graph
→ RAG Spec
→ Prompt Spec
→ Agent Knowledge Blueprint
→ reviewable evidence chain.

Only after this demo passes QA and POLYGON does AK-01 move to F3 Automated.
