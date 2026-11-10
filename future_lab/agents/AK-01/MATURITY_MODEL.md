# AK-01 Knowledge Architect — Maturity Model

AK-01 evolves as a meta-agent that builds knowledge systems for other agents.

## M0 — SOURCE READER
Reads documents and extracts passages.

Exit criteria:
- source ingestion works
- provenance preserved
- no hallucinated citations

## M1 — STRUCTURED EXTRACTOR
Extracts concepts, methods, formulas, claims, assumptions, limitations.

Exit criteria:
- Knowledge Unit contract populated
- source location attached
- entity normalization works

## M2 — KNOWLEDGE GRAPH BUILDER
Builds nodes, typed edges and evidence links.

Node classes:
- CONCEPT
- METHOD
- ALGORITHM
- FORMULA
- DATASET
- METRIC
- TOOL
- CLAIM
- EVIDENCE
- ASSUMPTION
- LIMITATION
- TASK
- CAPABILITY
- SKILL

Edge classes:
- REQUIRES
- SUPPORTS
- CONTRADICTS
- IMPLEMENTS
- MEASURES
- APPLIES_TO
- DERIVED_FROM
- ALTERNATIVE_TO
- SUPERSEDES
- PART_OF
- PRECEDES

Exit criteria:
- graph is queryable
- duplicate concepts merge safely
- contradictions retained

## M3 — WEIGHTED KNOWLEDGE MODEL
Assigns contextual weights to nodes and edges.

Weight dimensions:
- authority
- evidence_strength
- task_relevance
- recency
- applicability
- confidence
- prerequisite_importance
- operational_criticality
- contradiction_penalty

No universal scalar is authoritative. Aggregate score is policy/configuration driven.

## M4 — RAG DESIGNER
Builds a retrieval architecture for the target agent.

Produces:
- corpus map
- chunking policy
- metadata schema
- hybrid retrieval plan
- reranking policy
- graph retrieval policy
- source trust filters
- citation policy
- freshness/update policy

## M5 — AGENT KNOWLEDGE ARCHITECT
Designs the target agent's:
- knowledge domains
- capability map
- prompt architecture
- RAG architecture
- tool knowledge
- decision rules
- uncertainty policy
- escalation policy
- required knowledge states

## M6 — AGENT BUILDER INPUT PRODUCER
Produces a complete Agent Knowledge Blueprint consumed by downstream builders.

Outputs:
- AGENT_KNOWLEDGE_BLUEPRINT
- SYSTEM_PROMPT_SPEC
- RAG_SPEC
- KNOWLEDGE_GRAPH_SPEC
- NODE_WEIGHT_POLICY
- EVALUATION_SPEC
- UNKNOWN_GAPS
- TRAINING_PREREQUISITES

## M7 — SELF-AUDITING KNOWLEDGE FACTORY
Runs:
- contradiction scans
- stale-source scans
- orphan-node scans
- weak-evidence scans
- retrieval coverage tests
- prompt-grounding tests
- knowledge-gap detection

## M8 — ADAPTIVE KNOWLEDGE FACTORY
Learns from target-agent failures and updates:
- weights
- retrieval
- missing knowledge
- prompt constraints
- evaluation cases

Human approval remains required for critical policy or evidence-class changes.
