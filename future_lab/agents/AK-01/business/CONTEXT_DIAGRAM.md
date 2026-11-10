# AK-01 — Business Context Diagram

```mermaid
flowchart LR
    FA[FATHER Architect]
    PM[PM-01 Product Manager]
    AA[AA-01 Agent Architect]
    DE[Domain Expert]
    SP[Source Provider]
    AK[AK-01 Knowledge Architect]
    KC[AKN-01 Knowledge Curator]
    TA[AT-01 Training Architect]
    AC[AC-01 Agent Coach]
    AG[Target Agent / Specialist]
    QA[AQ-01 QA / Evaluator]
    POL[POLYGON]
    OBS[Production Observation]
    CODEX[FATHER_CODEX]
    FL[Future Lab]

    FA -->|target agent request| AK
    PM -->|product goals / scope| AK
    AA -->|role / tasks / capabilities| AK
    DE -->|domain constraints / local practice| AK
    SP -->|books / papers / standards / docs| AK

    AK -->|Knowledge Capsule / Blueprint| KC
    AK -->|training prerequisites| TA
    AK -->|implementation refs| CODEX
    AK -->|methods needing qualification| FL

    KC -->|review / corrections| AK
    TA -->|training program| AC
    AC -->|practice / exercises| AG
    AG -->|task traces / outcomes| QA
    QA -->|competency gaps / failures| AK
    POL -->|adversarial failures| AK
    OBS -->|real cases / local specifics / corrections| AK

    AK -->|Knowledge Delta proposal| KC
    KC -->|approved delta| TA
    TA -->|targeted retraining plan| AC
    AC -->|retraining| AG
    AG -->|retest evidence| QA
    QA -->|qualification result| POL
```

## Interpretation

AK-01 is not a one-time extractor. It is a continuous knowledge-engineering station.

It creates the initial specialist knowledge capsule and later accepts:
- training failures;
- real production cases;
- local organizational knowledge;
- human corrections;
- QA findings;
- POLYGON findings;
- newly published sources.

AK-01 analyzes them and produces a **Knowledge Delta** instead of silently rewriting the current capsule.

Final runtime qualification remains outside AK-01 authority.
