# AK-01 — Event Model

Core events:

- KnowledgeJobCreated
- TargetAgentProfileRegistered
- SourceRegistered
- SourceVersionCreated
- SourceParsed
- KnowledgeExtractionStarted
- KnowledgeUnitExtracted
- EvidenceLinked
- ContradictionDetected
- KnowledgeGraphBuilt
- WeightPolicyApplied
- ProcedureGenerated
- ChecklistGenerated
- RAGSpecGenerated
- PromptPackageGenerated
- KnowledgeGapDetected
- CapsuleDraftCreated
- CapsuleReviewRequested
- CapsuleApproved
- CapsuleReworkRequested
- TrainingHandoffCreated
- CompetencyGapDetected
- KnowledgeDeltaProposed
- KnowledgeDeltaApproved
- RetrainingRequested
- RequalificationStarted
- RequalificationPassed
- RequalificationFailed
- CapsuleVersionReleased

## Event envelope

```json
{
  "event_id": "uuid",
  "event_type": "KnowledgeUnitExtracted",
  "occurred_at": "RFC3339",
  "job_id": "uuid",
  "target_agent_id": "string",
  "actor": "AK-01",
  "correlation_id": "uuid",
  "causation_id": "uuid",
  "payload_version": "1.0",
  "payload": {}
}
```
