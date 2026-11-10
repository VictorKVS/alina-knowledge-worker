# AK-01 — Knowledge Sufficiency Model

## A knowledge area is sufficient only if all required dimensions pass.

### 1. Concept coverage
Required concepts and prerequisites exist.

### 2. Decision coverage
The agent has enough knowledge to choose between relevant alternatives.

### 3. Procedure coverage
The agent knows how to execute the professional task.

### 4. Limitation coverage
Known assumptions, failure modes and contraindications are represented.

### 5. Evidence coverage
Critical claims have qualified evidence.

### 6. Contradiction coverage
Material disagreements are represented, not silently collapsed.

### 7. Practice coverage
Representative practical cases exist.

### 8. Evaluation coverage
Tests exist at the required professional depth.

### 9. Security/safety coverage
Critical safety/security constraints are represented where applicable.

## Status values
- EMPTY
- PARTIAL
- COVERED
- VERIFIED
- QUALIFICATION_READY
- QUALIFIED

## Stop condition
For a required knowledge item:
- all mandatory subtopics covered;
- required depth achieved;
- no unresolved critical evidence gap;
- no unresolved critical contradiction;
- practice/evaluation artifacts available;
- critical safety/security checks available.

Additional material beyond this point is OPTIONAL unless new evidence or requirements create a delta.
