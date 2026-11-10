# AK-01 — End-to-End Business Process

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
    M[Assign Contextual Weights]
    N[Design RAG]
    O[Design Prompt Architecture]
    P[Detect Gaps / Unknowns]
    Q[Compose Agent Knowledge Blueprint]
    R{AKN-01 Review}
    S[Rework]
    T[Approved Blueprint]
    U[Handoff to AA-01 / AT-01 / CODEX / QA / Future Lab]
    V[End]

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J --> K --> L --> M --> N --> O --> P --> Q --> R
    R -->|REWORK| S --> G
    R -->|APPROVE| T --> U --> V
```

## Business rule
No blueprint can be marked APPROVED without:
- provenance coverage;
- explicit unknowns;
- contradiction register;
- target-agent relevance mapping;
- reviewer decision.
