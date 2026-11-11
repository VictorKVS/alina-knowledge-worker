# AK-01 — Event Catalog v1

## Job
KnowledgeJobCreated
KnowledgeJobStarted
KnowledgeJobFailed
KnowledgeJobCompleted

## Source
SourceRegistered
SourceVersionCreated
SourceIntegrityFailed
SourceMarkedStale
SourceQuarantined

## Knowledge
KnowledgeUnitExtracted
KnowledgeUnitVerified
ContradictionDetected
MergeCandidateCreated
KnowledgeGraphBuilt
KnowledgeGapDetected

## Operational
ProcedureGenerated
ChecklistGenerated
RAGSpecGenerated
PromptPackageGenerated

## Capsule
CapsuleDraftCreated
CapsuleReviewRequested
CapsuleApproved
CapsuleReworkRequested
KnowledgeDeltaProposed
KnowledgeDeltaApproved
RetrainingRequested
RequalificationStarted
RequalificationPassed
RequalificationFailed
CapsuleVersionReleased

## Security
PromptInjectionDetected
UnauthorizedQualificationAttempt
CrossNamespaceAccessDenied
SecretExposurePrevented
ToolPermissionDenied
ProvenanceIntegrityViolation

## Reliability
DependencyUnavailable
StageRetryScheduled
CircuitBreakerOpened
DerivedIndexRebuildStarted
DerivedIndexRebuildCompleted

## Event requirements
Every event includes:
- event_id
- event_type
- occurred_at
- correlation_id
- causation_id
- actor
- namespace
- payload_version
- payload
