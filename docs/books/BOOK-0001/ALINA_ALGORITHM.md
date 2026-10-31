# ALINA Algorithm — Technical Book → FATHER

## Input

- one bounded source scope (chapter/section);
- source manifest;
- exact source locators;
- target FATHER capability map.

## Output

A valid `father.book_knowledge_package.v1`.

## Algorithm

### A. Source control

1. Register `source_id`.
2. Record edition/year/ISBN.
3. Freeze processing scope.
4. Record page/chapter boundaries.
5. Do not alter or silently correct source claims.

### B. Translation

1. Translate meaning into Russian.
2. Preserve original technical terms alongside Russian equivalents.
3. Keep formulas, identifiers, tool names and code names unchanged.
4. Attach locator to each translation unit.
5. Mark uncertain translation as `REVIEW_REQUIRED`.

### C. Semantic decomposition

For each bounded unit identify:

- problem;
- concept;
- definition;
- assumption;
- method;
- limitation;
- recommendation;
- tool/reference;
- example;
- experiment;
- conclusion;
- open question.

Do not preserve page order as the only structure. Build a concept hierarchy.

### D. Glossary

For every important term create:

```text
TERM_ID
original term
canonical RU
definition
source definition status
source locators
related terms
FATHER capability links
```

### E. Applications

For each method identify:

- what problem it solves;
- prerequisites;
- when to use;
- when not to use;
- limitations;
- target FATHER products.

### F. Examples

Normalize each important example:

```text
input
→ procedure
→ output
→ lesson
→ reusable pattern
```

### G. Algorithms

Convert procedural source material into:

```text
goal
inputs
preconditions
steps
branches
outputs
failure modes
verification
```

Never invent a branch not supported by the source; additions must be labeled `ALINA_INFERENCE`.

### H. Conclusions

Separate:

- `AUTHOR_CONCLUSION`
- `ALINA_CONCLUSION`

The second must reference the source atoms it combines.

### I. Combinations

Combine atoms only as hypotheses:

```text
KNOW-A + KNOW-B
→ HYPOTHESIS
→ expected benefit
→ conflicts
→ validation needed
```

Never present synthesis as a book claim.

### J. Checklists

Generate operational checklists only from traceable atoms/algorithms.

Each item contains:
- source knowledge IDs;
- pass/fail condition;
- evidence needed.

### K. FATHER mapping

Map each validated atom to zero or more:

- capability;
- block;
- chassis;
- policy;
- test;
- evidence;
- product.

If no destination is justified, use `UNMAPPED` rather than guessing.

### L. Quality gates

A chapter cannot be marked learned until:

- translation traceable;
- semantic coverage reviewed;
- glossary linked;
- algorithms traceable;
- examples reconstructed;
- author vs ALINA conclusions separated;
- combinations labeled as hypotheses;
- checklists traceable;
- provenance complete;
- FATHER mapping reviewed.

## Learning feedback

After every chapter record:

- missed concepts;
- unsupported inferences;
- wrong mappings;
- duplicate atoms;
- terminology errors;
- contradiction misses;
- useful new extraction patterns.

These corrections become gold examples for the next run.
