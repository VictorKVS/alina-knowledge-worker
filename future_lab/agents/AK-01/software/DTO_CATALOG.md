# AK-01 — DTO Catalog v1

## Commands
CreateKnowledgeJob
RegisterSource
RunKnowledgeJob
MarkSourceStale
BuildProcedure
BuildChecklist
BuildPromptPackage
CreateKnowledgeDelta
ReviewKnowledgeDelta
ReleaseCapsule
RequalifyCapsule
ImpactAnalysisRequest

## Views
KnowledgeJobView
SourceView
SourceVersionView
KnowledgeUnitView
ContradictionView
GraphView
RAGSpecView
PromptPackageView
ProcedureView
ChecklistView
KnowledgeGapView
KnowledgeCapsuleView
CapsuleVersionView
QualificationRecordView
AuditEventView

## Shared fields
- schema_version
- correlation_id
- created_at
- updated_at where mutable
- actor
- namespace

## ProvenanceRef
- source_id
- source_version_id
- source_fragment_id
- locator
- source_hash
- extraction_job_id
- extractor_version

## SecurityContext
- actor_id
- actor_type
- namespace
- permissions
- model_policy
- tool_policy

## ErrorResponse
- code
- category
- message
- retryable
- correlation_id
- details
