# AK-01 — Agent Architecture Package

Owner: AA-01 Agent Architect
Product: AK-01 ALINA Knowledge Architect

## Objective
Define AK-01 as an orchestrated agent system with explicit components, APIs, events, algorithms, failure modes, recovery actions and handoffs.

## Core principle
AK-01 is not a single prompt.
It is a controlled agent system composed of:
- deterministic services,
- LLM-assisted extractors/classifiers,
- retrieval components,
- policy engines,
- storage,
- validation,
- human review gates,
- monitoring and recovery.

## Top-level architecture

```mermaid
flowchart TB
    UI[Control Center / Client]
    APIGW[AK-01 API Gateway]
    ORCH[Agent Orchestrator]
    POLICY[Policy Engine]
    MEMORY[Working / Episodic / Semantic Memory]

    PROF[Target Agent Profiler]
    SRC[Source Intake]
    PARSE[Parser / Normalizer]
    EXT[Knowledge Extractor]
    EPI[Epistemic Classifier]
    NORM[Entity Normalizer]
    EVID[Evidence Linker]
    CONTR[Contradiction Engine]
    GRAPH[Graph Builder]
    WEIGHT[Weight / Ranking Policy]
    PROC[Procedure Builder]
    CHECK[Checklist Builder]
    RAG[RAG Architect]
    PROMPT[Prompt Architect]
    GAP[Gap Detector]
    CAPS[Capsule Composer]
    DELTA[Knowledge Delta Engine]

    SR[(Source Registry)]
    SQL[(PostgreSQL)]
    OBJ[(Object Store)]
    VEC[(Vector Index)]
    GDB[(Graph Store)]
    AUD[(Audit / Provenance Ledger)]
    EVT[(Event Bus)]

    CUR[AKN-01 Curator]
    TRAIN[AT-01 Training Architect]
    QA[AQ-01 Evaluator]
    POLY[POLYGON]
    CODEX[FATHER_CODEX]

    UI --> APIGW --> ORCH
    ORCH <--> POLICY
    ORCH <--> MEMORY

    ORCH --> PROF
    ORCH --> SRC
    SRC --> OBJ
    SRC --> SR
    SRC --> PARSE
    PARSE --> EXT
    EXT --> EPI --> NORM --> EVID --> CONTR --> GRAPH
    GRAPH --> GDB
    EXT --> SQL
    EXT --> VEC
    EVID --> AUD
    GRAPH --> WEIGHT
    WEIGHT --> PROC
    PROC --> CHECK
    CHECK --> RAG
    RAG --> PROMPT
    PROMPT --> GAP
    GAP --> CAPS

    CAPS --> CUR
    QA --> DELTA
    POLY --> DELTA
    DELTA --> ORCH

    CUR --> TRAIN
    CAPS --> CODEX

    ORCH <--> EVT
```
