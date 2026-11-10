# AK-01 — System Traceability

| Business Req | System Component | Primary Data | System Evidence |
|---|---|---|---|
| BR-01 target knowledge | Target Agent Profiler | TargetAgentProfile | capability map |
| BR-02 provenance | Source Registry + Ledger | SourceVersion / Fragment | provenance links |
| BR-03 epistemic control | Epistemic Classifier | KnowledgeUnit | epistemic type |
| BR-04 contradictions | Contradiction Engine | Claim/Evidence | contradiction record |
| BR-05 aliases | Entity Resolver | entity aliases | merge decision |
| BR-06 contextual relevance | Weight Policy Engine | WeightVector | policy version |
| BR-07 retrieval | RAG Architect | RAGSpec | retrieval eval |
| BR-08 prompt layers | Prompt Architect | PromptPackage | schema validation |
| BR-09 gaps | Gap Detector | KnowledgeGap | gap report |
| BR-10 training handoff | Capsule Composer | prerequisite graph | handoff package |
| BR-11 procedures | Procedure Builder | Procedure / Checklist | workflow test |
| BR-12 training failures | Delta Engine | QA traces | root-cause record |
| BR-13 local adaptation | Layering model | scope_layer | local delta |
| BR-14 no silent edits | Review service | KnowledgeDelta | reviewer decision |
| BR-15 version history | Capsule Versioning | CapsuleVersion | lineage |
| BR-16 requalification | Qualification integration | QualificationRecord | retest result |
| BR-17 layer separation | Knowledge model | CORE/DOMAIN/ORG/PROJECT/CONTEXT | scope validation |
