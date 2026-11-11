# AK-01 — Test Data Strategy

## Dataset classes

### GOLDEN
Human-reviewed expected Knowledge Units, relations, evidence and outputs.

### CONTRADICTION
Pairs/sets of sources with deliberate factual or contextual disagreement.

### ALIAS
Known synonyms, acronyms, homonyms and dangerous near-duplicates.

### INJECTION
Documents containing instructions attempting to override AK-01 policies.

### STALE
Multiple versions of the same source with superseded requirements.

### CORRUPT
Broken PDFs/text, malformed metadata, wrong hashes and incomplete fragments.

### LOCALITY
CORE, DOMAIN, ORGANIZATION, PROJECT and ACTIVE_CONTEXT knowledge with overlapping terms.

### RETRIEVAL
Queries with known relevant, irrelevant and low-trust passages.

### FAILURE
Inputs designed to trigger provider timeout, index loss, queue outage and partial processing.

## Golden test object

Each test fixture records:
- fixture_id
- source_hashes
- target_agent_profile
- policy_version
- expected_units
- expected_relations
- forbidden_outputs
- expected_errors
- expected_events
- reviewer
- fixture_version

## Rule

Production data is not copied blindly into tests.
Sensitive data must be synthetic, anonymized or specifically approved.
