# AK-01 — Business Use Cases

## UC-01 Create Knowledge Blueprint
Actor: FATHER Architect / Agent Architect

Input:
- target agent profile
- goals
- tasks
- capabilities
- evidence policy
- sources

Output:
- Agent Knowledge Blueprint

Success:
- blueprint is schema-valid
- knowledge coverage threshold reached
- provenance present

## UC-02 Add Source
Actor: Source Provider / Domain Expert

Flow:
1. register source
2. identify type/version/edition
3. classify authority
4. hash/version source
5. queue extraction

Exceptions:
- duplicate source
- unsupported format
- source inaccessible
- source version conflict

## UC-03 Extract Knowledge
Actor: AK-01

Output:
- Knowledge Units
- epistemic type
- source location
- confidence
- relations

## UC-04 Build Knowledge Graph
Actor: AK-01

Output:
- typed nodes
- typed edges
- provenance links
- contradiction links
- prerequisite links

## UC-05 Design Target-Agent RAG
Actor: AK-01

Output:
- corpus partitions
- chunking policy
- metadata
- hybrid retrieval policy
- graph retrieval
- reranking
- trust filters
- citation policy

## UC-06 Design Prompt Architecture
Actor: AK-01

Output:
- system core
- role layer
- domain policy
- evidence policy
- tool policy
- decision policy
- output contract
- escalation policy
- task overlays

## UC-07 Review Blueprint
Actor: AKN-01

Decision:
APPROVE | REWORK | REJECT

## UC-08 Generate Training Handoff
Actor: AK-01

Output to AT-01:
- capability map
- prerequisite graph
- competency weights
- weak areas
- evaluation requirements
