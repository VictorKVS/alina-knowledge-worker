# AK-01 — Exceptions and Business Rules

## EX-01 Source has no verifiable origin
Action:
- mark source UNVERIFIED
- extraction allowed only as low-trust/discovery material
- cannot support QUALIFIED knowledge

## EX-02 Two sources contradict
Action:
- create contradiction record
- preserve both claims
- attach evidence/counter-evidence
- do not auto-resolve unless policy permits and evidence supports

## EX-03 Same concept appears under aliases
Action:
- create candidate merge
- retain aliases
- require confidence threshold or reviewer approval for destructive merge

## EX-04 Source contains prompt injection
Action:
- treat source text as untrusted data
- block source instructions from affecting AK-01 control policy
- log security event

## EX-05 Missing page/section
Action:
- preserve available source location
- mark provenance completeness gap
- do not fabricate location

## EX-06 High similarity, low authority
Action:
- retrieval trust filter can demote result
- similarity never overrides evidence policy

## EX-07 Target agent changes role
Action:
- create new target-agent version
- recompute relevance weights
- reassess RAG and prompt overlays
- do not overwrite prior blueprint lineage

## EX-08 Source becomes stale
Action:
- flag affected knowledge units
- queue review
- calculate impacted graph neighborhood
