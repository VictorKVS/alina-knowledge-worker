# AK-01 — Logical System Architecture

```mermaid
flowchart TB
    UI[Control Center / API Client]
    API[AK-01 API Gateway]
    ORCH[Knowledge Job Orchestrator]

    TP[Target Agent Profiler]
    SI[Source Intake]
    PARSE[Parser / Normalizer]
    EXT[Knowledge Extractor]
    EPI[Epistemic Classifier]
    ENT[Entity Resolver]
    EVD[Claim-Evidence Linker]
    CON[Contradiction Engine]
    KG[Knowledge Graph Builder]
    WGT[Weight Policy Engine]
    PROC[Procedure / Checklist Builder]
    RAG[RAG Architect]
    PRM[Prompt Architect]
    GAP[Gap Detector]
    COMP[Capsule Composer]
    DELTA[Knowledge Delta Engine]

    SR[(Source Registry)]
    OBJ[(Object Storage)]
    SQL[(PostgreSQL)]
    VEC[(Vector Index)]
    GDB[(Graph Store)]
    AUD[(Provenance / Audit Ledger)]
    EVT[(Event Bus)]

    AKN[AKN-01 Review]
    AT[AT-01 Training Architect]
    QA[AQ-01 Evaluator]
    POL[POLYGON]

    UI --> API --> ORCH
    ORCH --> TP
    ORCH --> SI
    SI --> OBJ
    SI --> SR
    SI --> PARSE
    PARSE --> EXT
    EXT --> EPI --> ENT --> EVD --> CON --> KG
    KG --> GDB
    EXT --> SQL
    EXT --> VEC
    EVD --> AUD
    KG --> WGT
    WGT --> PROC
    PROC --> RAG
    RAG --> PRM
    PRM --> GAP
    GAP --> COMP
    COMP --> SQL
    COMP --> AKN

    QA --> DELTA
    POL --> DELTA
    DELTA --> ORCH

    AKN -->|approved capsule| AT

    ORCH <--> EVT
```

## Design principle

AK-01 is not one LLM prompt. It is an orchestrated system of deterministic services, retrieval, structured stores and LLM-assisted transformations.

LLM calls are replaceable implementation details inside selected modules.
