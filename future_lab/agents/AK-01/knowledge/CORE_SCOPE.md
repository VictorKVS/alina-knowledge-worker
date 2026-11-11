# AK-01 — Core Scope Before Expansion

## Goal

Build AK-01 ALINA Knowledge Architect first.

Do NOT load all future FATHER domains into AK-01.
AK-01 receives only the knowledge required to design, build, validate and maintain knowledge systems for other agents.

## AK-01 mandatory knowledge domains

1. Knowledge Engineering
- ontology
- taxonomy
- knowledge units
- knowledge graphs
- provenance
- versioning
- contradiction handling
- knowledge lifecycle

2. RAG Engineering
- document ingestion
- parsing
- chunking
- embeddings
- sparse search
- vector search
- hybrid retrieval
- reranking
- graph retrieval
- metadata filtering
- citation grounding
- retrieval evaluation

3. Agent Engineering
- role/task/capability decomposition
- agent memory
- tools
- planning
- orchestration
- handoffs
- prompt architecture
- agent evaluation

4. Prompt & Context Engineering
- system prompt layers
- task overlays
- tool policy
- evidence policy
- context construction
- context compression
- structured outputs
- prompt versioning

5. Evidence Engineering
- source hierarchy
- primary/secondary sources
- evidence classes
- claim/evidence links
- confidence
- freshness
- traceability

6. Procedure Engineering
- decision rules
- operating procedures
- checklists
- stop conditions
- escalation rules
- acceptance criteria

7. Evaluation Engineering
- golden datasets
- retrieval tests
- grounding tests
- contradiction tests
- regression tests
- LLM-as-a-judge only as auxiliary evaluator
- human review gates

8. Security for Knowledge Systems
- prompt injection
- RAG poisoning
- source poisoning
- cross-agent isolation
- secrets
- least privilege
- audit
- trust boundaries

9. Specialist Capsule Engineering
- knowledge capsule
- skill/capability map
- prerequisite graph
- local adaptation
- knowledge delta
- retraining handoff
- requalification

## Not part of AK-01 own core knowledge

These are reusable FATHER domain packs and are connected later:
- jurisprudence
- information security domain content
- medicine
- OSINT domain content
- forecasting domain content
- finance/trading
- Kubernetes
- robotics
- astronomy
- narrative analysis
- other specialties

AK-01 must know how to build and attach these packs, not contain them all by default.
