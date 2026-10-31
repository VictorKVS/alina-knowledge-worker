# ALINA Algorithm — Chapter-by-Chapter Technical Book Study

## Canonical chapter order

Every chapter is processed in the same visible order:

```text
CHAPTER N
  ↓
0. ORIGINAL SOURCE VIEW
  ↓
1. RUSSIAN TRANSLATION
  ↓
2. SEMANTIC ANALYSIS
  ↓
3. APPLICATION AREAS
  ↓
4. EXAMPLES / CASES
  ↓
5. ALGORITHMS / PROCEDURES
  ↓
6. AUTHOR CONCLUSIONS
  ↓
7. ALINA CONCLUSIONS
  ↓
8. GLOSSARY / CONCEPT DICTIONARY
  ↓
9. COMBINATIONS / HYPOTHESES
  ↓
10. CHECKLISTS
  ↓
11. FATHER MAPPING
  ↓
12. QUALITY GATE
  ↓
NEXT CHAPTER
```

## 0. Original source view

The original book remains the first layer.

ALINA must expose locally:

- original chapter pages;
- original diagrams/figures/images;
- original tables;
- captions;
- page numbers;
- chapter/section boundaries.

The public GitHub repository must NOT contain the full copyrighted chapter or copied figures.

GitHub stores only:

- exact page/section map;
- figure/table index;
- short evidence snippets where necessary;
- derived translation and analysis;
- hashes/locators back to the local source.

### Local source contract

```text
BOOK PDF
  -> chapter page range
  -> page image / original text view
  -> figure/table anchors
  -> source locator
```

A user reviewing a chapter should always be able to go back from any derived statement to the exact page/figure in the local source.

## 1. Russian translation

Translate the chapter section-by-section.

For each translation unit preserve:

- source page;
- source section;
- original technical term;
- Russian equivalent;
- uncertainty marker when needed.

Do not silently simplify away technical distinctions.

## 2. Semantic analysis

Decompose the chapter into:

- problem;
- concepts;
- definitions;
- assumptions;
- methods;
- constraints;
- failure modes;
- tradeoffs;
- recommendations;
- open questions;
- relationships between concepts.

## 3. Application areas

For each important concept/method answer:

- where can it be used?
- what problem does it solve?
- what prerequisites are required?
- when should it NOT be used?
- what FATHER/ALINA products may benefit?

## 4. Examples / cases

Reconstruct each meaningful example as:

```text
purpose
inputs
procedure
outputs
lesson
reusable pattern
source locator
```

## 5. Algorithms / procedures

When the chapter contains a procedure, convert it into:

```text
goal
inputs
preconditions
steps
branches
outputs
failure modes
verification
source locator
```

If the source does not define an algorithm, do not invent one.

## 6. Author conclusions

Store conclusions explicitly attributable to the author.

## 7. ALINA conclusions

Store ALINA synthesis separately.

Every ALINA conclusion must cite the source-derived knowledge atoms it combines.

## 8. Glossary / concept dictionary

Maintain a cumulative book glossary.

Each term:

- original term;
- canonical Russian term;
- definition;
- source pages;
- first chapter seen;
- related terms;
- FATHER capability links.

The glossary is cumulative across chapters.

## 9. Combinations / hypotheses

Combine ideas only as ALINA hypotheses.

```text
KNOW-A + KNOW-B
  -> hypothesis
  -> expected benefit
  -> conflicts
  -> validation needed
```

Never present a combination as a statement from the book.

## 10. Checklists

Generate operational checklists only from traceable knowledge or algorithms.

Each checklist item must have:

- source knowledge IDs;
- pass/fail condition;
- expected evidence.

## 11. FATHER mapping

Map validated knowledge to:

- capability;
- block;
- chassis;
- policy;
- test;
- evidence;
- product.

If no mapping is justified, record `UNMAPPED`.

## 12. Chapter quality gate

A chapter is closed only when:

- original page range is registered;
- figures/tables are indexed;
- translation is traceable;
- semantic coverage is reviewed;
- glossary is updated;
- applications are identified where supported;
- examples are structured;
- algorithms are extracted where present;
- author and ALINA conclusions are separated;
- combinations are labeled as hypotheses;
- checklists are traceable;
- FATHER mapping is reviewed;
- unresolved questions remain visible.

Only then move to the next chapter.

## Book completion rule

```text
CH01 CLOSED
→ CH02
→ CH02 CLOSED
→ CH03
...
→ CH13 CLOSED
→ CROSS-CHAPTER SYNTHESIS
→ REPOSITORY SCOUTING
→ REUSE / ADAPT / BUILD
```

## Learning feedback

After each chapter record:

- missed concepts;
- unsupported inferences;
- wrong mappings;
- terminology errors;
- missed figures/tables;
- contradiction misses;
- useful new extraction patterns.

These corrections become gold examples for the next chapter.
