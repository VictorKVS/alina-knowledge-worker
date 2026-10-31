# ALINA Book Processing Algorithm v1

## Purpose

Deterministic semantic processing of a technical book into a FATHER-ready knowledge package.

## Input

- source file;
- source metadata;
- bounded processing scope (chapter/section/pages);
- target language: Russian;
- target project: FATHER.

## Output

A package conforming to `father.book_knowledge_package.v1`.

## Algorithm

### A. SOURCE CONTROL

1. Compute/record source hash.
2. Register title, author, edition, year and source ID.
3. Bind every extracted unit to chapter/section/page locator.
4. Never commit the copyrighted source file into the public knowledge repository.

Gate: `SOURCE_REGISTERED`.

### B. STRUCTURAL PASS

1. Detect parts, chapters, sections, figures, tables, exercises, notes, warnings and references.
2. Preserve original order.
3. Build a structural index.

Gate: `STRUCTURE_CAPTURED`.

### C. TRANSLATION PASS

For each bounded source unit:

1. understand sentence/paragraph in context;
2. translate meaning into Russian;
3. preserve technical term in English on first occurrence;
4. avoid adding knowledge absent from source;
5. retain locator;
6. mark ambiguous translation for review.

Gate: `TRANSLATION_TRACEABLE`.

### D. SEMANTIC DECOMPOSITION

Classify each meaningful unit as one or more of:

- definition;
- fact/claim;
- mechanism;
- pattern;
- limitation;
- recommendation;
- use case;
- example;
- algorithm/procedure;
- experiment/exercise;
- warning;
- open question;
- tool/repository reference.

Then group by idea, not just page order.

Gate: `SEMANTIC_OUTLINE_READY`.

### E. GLOSSARY

For each important concept:

1. canonical English term;
2. canonical Russian term;
3. source-supported definition;
4. explanation in FATHER context, separately labeled;
5. synonyms/aliases;
6. related concepts;
7. source locators.

Merge duplicates only when meanings are compatible.

Gate: `GLOSSARY_LINKED`.

### F. APPLICATIONS AND EXAMPLES

For every application/example:

```text
PROBLEM
→ PRECONDITIONS
→ INPUT
→ METHOD
→ OUTPUT
→ LIMITATIONS
→ WHAT IT TEACHES
```

Keep tutorial library choices separate from architectural requirements.

Gate: `EXAMPLES_RECONSTRUCTED`.

### G. ALGORITHMS

Convert procedural material into:

```text
GOAL
INPUTS
PRECONDITIONS
STEPS
BRANCHES
OUTPUTS
FAILURE MODES
METRICS
SOURCE
```

Do not invent missing steps silently.

Gate: `ALGORITHMS_TRACEABLE`.

### H. CONCLUSIONS

Create two namespaces:

- `AUTHOR_CONCLUSION`
- `ALINA_CONCLUSION`

An ALINA conclusion must list supporting knowledge IDs and must never be represented as text from the author.

Gate: `INFERENCE_SEPARATED`.

### I. COMBINATION ENGINE

Combine compatible knowledge atoms across chapters.

For every combination:

1. input knowledge IDs;
2. hypothesis;
3. expected engineering benefit;
4. conflicts/assumptions;
5. what would falsify it;
6. validation/test required.

Combinations are hypotheses until tested.

Gate: `COMBINATIONS_EXPLICIT`.

### J. CHECKLIST GENERATOR

Turn validated algorithms, limitations and recommendations into operational checklists.

Every checklist item must trace to:
- source knowledge ID, or
- validated FATHER decision.

No orphan checklist items.

Gate: `CHECKLIST_TRACEABLE`.

### K. FATHER MAPPING

For each knowledge atom decide:

```text
IGNORE
REFERENCE_ONLY
CAPABILITY
ADR_CANDIDATE
BLOCK_CANDIDATE
CHASSIS_CANDIDATE
POLICY_CANDIDATE
TEST_CANDIDATE
EVIDENCE_REQUIREMENT
PRODUCT_PATTERN
```

Mapping is a proposal until reviewed.

Gate: `FATHER_MAPPING_REVIEWED`.

### L. IMPLEMENTATION SCOUTING

Only after semantic extraction is closed:

1. search official docs and GitHub implementations;
2. record repo, version/tag/commit, license and maintenance status;
3. map candidate to capability;
4. test in isolation/sandbox;
5. compare alternatives;
6. decide `REUSE / ADAPT / BUILD / REJECT`.

Gate: `IMPLEMENTATION_DECISION_RECORDED`.

### M. QUALITY / LEARNING LOOP

Measure:

- translation traceability;
- semantic coverage;
- provenance completeness;
- glossary coverage;
- unsupported inference rate;
- duplicate rate;
- algorithm/checklist traceability;
- contradiction detection;
- mapping precision;
- wrong recommendation rate.

Corrections become training cases.

## Chapter terminal state

`KNOWLEDGE_PACKAGE_READY` only when required gates are closed.

## Book terminal state

`BOOK_ASSIMILATED` only when:

- all chapter packages are ready;
- cross-chapter glossary is deduplicated;
- combinations are reviewed;
- FATHER mappings are consolidated;
- unresolved contradictions/gaps remain explicitly visible;
- implementation candidates are tracked separately from source knowledge.
