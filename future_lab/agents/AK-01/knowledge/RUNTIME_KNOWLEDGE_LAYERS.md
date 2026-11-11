# AK-01 — Runtime Knowledge Layers

AK-01 itself should not retrieve all knowledge all the time.

Runtime context is composed from layers:

SYSTEM CORE
+ AK-01 ROLE
+ CURRENT JOB POLICY
+ TARGET AGENT PROFILE
+ RELEVANT AK-01 OWN KNOWLEDGE
+ CURRENT SOURCE EVIDENCE
+ CURRENT WORKING STATE

## Retrieval order

1. identify job stage
2. identify required AK-01 capability
3. retrieve corresponding internal knowledge
4. retrieve target source evidence
5. apply evidence/trust filters
6. assemble context
7. execute stage
8. validate output
9. persist provenance

## Example

Task:
Design RAG for Forecasting Agent.

AK-01 retrieves from its own KB:
- RAG architecture
- hybrid retrieval
- metadata design
- reranking
- evaluation

Separately retrieves from target sources:
- forecasting domain concepts
- forecasting method hierarchy
- domain-specific evidence requirements

The two knowledge spaces remain separated.
