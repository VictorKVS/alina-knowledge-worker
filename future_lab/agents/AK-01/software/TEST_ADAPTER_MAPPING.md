# AK-01 — Test Adapter to Software Mapping

| Adapter operation | Application owner | Main DTO | Persistence/Event |
|---|---|---|---|
| create_job | JobService | CreateKnowledgeJob | knowledge_jobs / KnowledgeJobCreated |
| ingest_source | SourceService | RegisterSource | sources/source_versions / SourceRegistered |
| extract | ExtractionService | ExtractRequest | knowledge_units / KnowledgeUnitExtracted |
| get_units | JobService | KnowledgeUnitView | PostgreSQL |
| get_contradictions | GraphService | ContradictionView | contradictions |
| get_graph | GraphService | GraphView | graph adapter |
| rank | RetrievalService | RankRequest | no required write |
| qualify | QualificationService | QualificationCommand | qualification_records |
| get_capsule | CapsuleService | CapsuleView | capsule_versions |
| create_delta | DeltaService | CreateDelta | knowledge_deltas |
| release_capsule | CapsuleService | ReleaseCapsule | capsule_versions / CapsuleVersionReleased |
| simulate_failure | TestFaultPort | FaultCommand | test-only |
| get_events | EventQuery | EventView | event/outbox store |
| get_audit | AuditQuery | AuditView | audit ledger |
| build_procedure | ProcedureService | ProcedureBuildRequest | procedures |
| build_checklist | ProcedureService | ChecklistBuildRequest | checklists |
| build_prompt_package | PromptService | PromptBuildRequest | prompt_packages |
| mark_source_stale | SourceService | StaleSourceCommand | source_versions / SourceStale |
| impact_analysis | DeltaService | ImpactRequest | derived impact result |

## Acceptance
The production code MUST provide a testing_adapter module implementing this behavioral boundary.
