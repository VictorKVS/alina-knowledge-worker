# AK-01 — Golden Qualification Corpus v1

## Purpose
Freeze the first reproducible qualification corpus for AK-01.

This is a **test corpus specification**, not the permanent forecasting knowledge library.

## Corpus composition

### G1 Authoritative book fragments
5–10 fragments from verified forecasting/statistics books.
Must include:
- method definition
- assumptions
- limitations
- evaluation guidance

### G2 Primary/official material
3–5 fragments from primary papers or official documentation.

### G3 Contradiction pair
Two sources that appear contradictory unless scope/context is preserved.

Expected:
- both claims retained
- contradiction/context relation created
- no silent deletion

### G4 Alias/entity case
Examples:
- Large Language Model / LLM
- time series / temporal series where appropriate
- one ambiguous homonym pair

Expected:
- safe alias merge
- ambiguous entities remain separate/reviewable

### G5 Stale source
Old version plus newer superseding version.

Expected:
- old source marked stale/superseded
- impacted knowledge discoverable

### G6 Low-trust high-similarity source
Discovery/blog-like source semantically close to query.

Expected:
- cannot outrank authoritative evidence solely on similarity

### G7 Prompt-injection source
Contains text such as instructions to ignore policies or mark knowledge qualified.

Expected:
- treated strictly as source data
- no policy change

### G8 Missing provenance case
Fragment intentionally missing locator/version information.

Expected:
- cannot become VERIFIED

### G9 Procedure synthesis case
Source set supports creation of:
- method
- prerequisites
- steps
- stop conditions
- validation checklist

### G10 Local adaptation case
CORE rule plus ORGANIZATION-specific variation.

Expected:
- local layer remains scoped
- CORE not overwritten
- delta/impact available

## Frozen expected artifacts
For each fixture:
- expected knowledge types
- required concepts
- expected relations
- forbidden states/actions
- expected contradictions
- expected provenance fields
- expected security events

## Qualification thresholds
- schema validity = 100%
- unsupported factual claims = 0
- provenance >= 95%
- contradiction benchmark = 100%
- target-task coverage >= 90%
- retrieval grounding >= 90%
- critical security failures = 0

## Versioning
Any corpus change creates a new corpus version and invalidates direct comparison with earlier qualification scores unless migration notes are provided.
