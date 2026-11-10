# AK-01 Knowledge Ontology v1

## Purpose
Canonical ontology for AK-01 knowledge engineering.

## Node types
- CONCEPT
- FACT
- CLAIM
- EVIDENCE
- COUNTER_EVIDENCE
- HYPOTHESIS
- INTERPRETATION
- ASSUMPTION
- LIMITATION
- METHOD
- ALGORITHM
- FORMULA
- PROCEDURE
- PROCEDURE_STEP
- DECISION_RULE
- CHECKLIST
- METRIC
- DATASET
- TOOL
- TASK
- CAPABILITY
- SKILL
- RISK
- ANTI_PATTERN
- UNKNOWN
- SOURCE
- SOURCE_VERSION
- SOURCE_FRAGMENT
- AGENT_PROFILE
- KNOWLEDGE_GAP
- KNOWLEDGE_DELTA
- QUALIFICATION_RECORD

## Edge types
- IS_A
- PART_OF
- REQUIRES
- PRECEDES
- SUPPORTS
- CONTRADICTS
- DERIVED_FROM
- IMPLEMENTS
- APPLIES_TO
- MEASURES
- USES
- PRODUCES
- CONSUMES
- ALTERNATIVE_TO
- SUPERSEDES
- VALIDATED_BY
- TESTED_BY
- TRAINED_BY
- QUALIFIED_BY
- AFFECTS

## Mandatory invariants
1. Every source-derived node must have provenance.
2. CLAIM cannot become FACT without evidence policy approval.
3. CONTRADICTS must preserve both sides.
4. QUALIFIED requires external qualification evidence.
5. PROCEDURE must have at least one step.
6. DECISION_RULE must reference condition and action.
7. CHECKLIST items must be testable.
8. SOURCE_VERSION is immutable after registration.
9. CORE knowledge cannot be overwritten by ORGANIZATION/PROJECT/ACTIVE_CONTEXT.
10. KNOWLEDGE_DELTA must reference base version and impacted nodes.

## Knowledge states
RAW
→ EXTRACTED
→ VERIFIED
→ QUALIFIED
→ SUPERSEDED
→ ARCHIVED

## Scope layers
CORE
DOMAIN
ORGANIZATION
PROJECT
ACTIVE_CONTEXT

## Required provenance fields
- source_id
- source_version_id
- fragment_id
- locator
- source_hash
- extraction_job_id
- extractor_version
- created_at

## Merge policy
Automatic merge only when:
- canonical identity confidence exceeds configured threshold;
- no namespace/scope conflict;
- no destructive provenance loss.

Otherwise create MERGE_CANDIDATE for review.
