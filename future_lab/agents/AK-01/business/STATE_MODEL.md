# AK-01 — Business State Model

## Knowledge Job states

```mermaid
stateDiagram-v2
    [*] --> CREATED
    CREATED --> INGESTING
    INGESTING --> EXTRACTING
    EXTRACTING --> NORMALIZING
    NORMALIZING --> GRAPHING
    GRAPHING --> PROCEDURE_DESIGN
    PROCEDURE_DESIGN --> RAG_DESIGN
    RAG_DESIGN --> PROMPT_DESIGN
    PROMPT_DESIGN --> GAP_ANALYSIS
    GAP_ANALYSIS --> REVIEW
    REVIEW --> REWORK: changes required
    REWORK --> EXTRACTING
    REVIEW --> APPROVED: reviewer approves
    APPROVED --> TRAINING_HANDOFF
    TRAINING_HANDOFF --> OBSERVATION
    OBSERVATION --> DELTA_ANALYSIS: failures / local specifics / new sources
    DELTA_ANALYSIS --> DELTA_REVIEW
    DELTA_REVIEW --> REWORK: rejected
    DELTA_REVIEW --> RETRAINING: approved
    RETRAINING --> REQUALIFICATION
    REQUALIFICATION --> OBSERVATION: pass
    REQUALIFICATION --> REWORK: fail

    INGESTING --> FAILED
    EXTRACTING --> FAILED
    NORMALIZING --> FAILED
    GRAPHING --> FAILED
    PROCEDURE_DESIGN --> FAILED
    RAG_DESIGN --> FAILED
    PROMPT_DESIGN --> FAILED
    GAP_ANALYSIS --> FAILED

    FAILED --> REWORK
```

## Knowledge Unit states

```mermaid
stateDiagram-v2
    [*] --> RAW
    RAW --> EXTRACTED
    EXTRACTED --> VERIFIED
    VERIFIED --> QUALIFIED
    VERIFIED --> SUPERSEDED
    QUALIFIED --> SUPERSEDED
    SUPERSEDED --> ARCHIVED
```

## Specialist Capsule states

```mermaid
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> KNOWLEDGE_APPROVED
    KNOWLEDGE_APPROVED --> TRAINING
    TRAINING --> EVALUATION
    EVALUATION --> QUALIFIED: pass
    EVALUATION --> TRAINING: fail
    QUALIFIED --> DEPLOYED
    DEPLOYED --> REVIEW_REQUIRED: new evidence / local gap / failure
    REVIEW_REQUIRED --> DELTA_APPROVED
    DELTA_APPROVED --> RETRAINING
    RETRAINING --> REQUALIFICATION
    REQUALIFICATION --> DEPLOYED: pass
    REQUALIFICATION --> RETRAINING: fail
    DEPLOYED --> DEPRECATED
```

AK-01 may propose deltas and support VERIFIED knowledge workflows.
AK-01 cannot independently promote runtime knowledge or a specialist capsule to QUALIFIED.
