# AK-01 — End-to-End Business Process

## Initial specialist creation

```mermaid
flowchart TD
    A[Start: Agent Knowledge Request]
    B[Register Target Agent Profile]
    C[Define Goals / Tasks / Capabilities]
    D[Define Evidence Policy]
    E[Register Source Corpus]
    F[Classify Sources]
    G[Extract Knowledge Units]
    H[Epistemic Typing]
    I[Normalize Entities / Aliases]
    J[Link Claims to Evidence]
    K[Detect Contradictions]
    L[Build Knowledge Graph]
    M[Assign Contextual Attributes / Weights]
    N[Build Procedures / Decision Rules / Checklists]
    O[Design RAG]
    P[Design Prompt Architecture]
    Q[Detect Gaps / Unknowns]
    R[Compose Knowledge Capsule / Agent Knowledge Blueprint]
    S{AKN-01 Review}
    T[Rework]
    U[Approved Knowledge Capsule]
    V[Handoff to AT-01 Training Architect]

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J --> K --> L --> M --> N --> O --> P --> Q --> R --> S
    S -->|REWORK| T --> G
    S -->|APPROVE| U --> V
```

## Training and adaptation loop

```mermaid
flowchart TD
    K0[Approved Knowledge Capsule]
    T0[AT-01 Training Program]
    C0[AC-01 Practice / Labs / Cases]
    A0[Target Agent]
    E0[AQ-01 Evaluation]
    P0[POLYGON]
    D0[Controlled / Production Work]
    O0[Observation & Feedback]
    X0[Competency Gap Analysis]
    R0{Root Cause}
    KD[Knowledge Delta]
    PD[Procedure / Checklist Delta]
    RD[RAG Delta]
    PR[Prompt Delta]
    TD[Training Delta]
    AD[Architecture / Tool Delta]
    RV[AKN-01 Review]
    RT[Targeted Retraining]
    RE[Re-evaluation / Requalification]
    VN[New Specialist Capsule Version]

    K0 --> T0 --> C0 --> A0 --> E0 --> P0 --> D0 --> O0 --> X0 --> R0

    R0 -->|knowledge missing/outdated| KD
    R0 -->|procedure/checklist issue| PD
    R0 -->|retrieval issue| RD
    R0 -->|prompt/policy issue| PR
    R0 -->|skill/practice issue| TD
    R0 -->|capability/tool issue| AD

    KD --> RV
    PD --> RV
    RD --> RV
    PR --> RV
    TD --> RV
    AD --> RV

    RV -->|approved| RT --> RE --> VN
    RV -->|rework| X0
    VN --> D0
```

## Business rule

A specialist capsule is versioned and never silently overwritten.

Every significant change must produce:
1. change reason;
2. impacted knowledge/procedure/RAG/prompt nodes;
3. evidence;
4. approved delta;
5. targeted retraining where required;
6. re-evaluation;
7. new capsule version.
