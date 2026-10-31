# BOOK-0001 — Canonical Chapter Folder Structure

Every chapter folder must follow the same order.

```text
ch01/
  00_SOURCE_MAP.md
  01_TRANSLATION.md
  02_ANALYSIS.md
  03_APPLICATIONS.md
  04_EXAMPLES.md
  05_ALGORITHMS.md
  06_AUTHOR_CONCLUSIONS.md
  07_ALINA_CONCLUSIONS.md
  08_GLOSSARY.md
  09_COMBINATIONS.md
  10_CHECKLISTS.md
  11_FATHER_MAPPING.md
  12_QUALITY_GATE.md
  package.json
```

## 00_SOURCE_MAP.md

Contains:

- chapter title;
- original page range;
- section/page map;
- figure index;
- table index;
- exact local-source locators;
- source hash when available.

The original PDF text and figures are displayed locally by ALINA from the user's lawful copy and are not committed to public GitHub.

## Processing rule

Do not begin the next chapter until `12_QUALITY_GATE.md` says the current chapter is CLOSED.

Sequence:

```text
Chapter 1 source
→ translation
→ analysis
→ application
→ examples
→ algorithms
→ conclusions
→ glossary
→ combinations
→ checklists
→ FATHER mapping
→ quality gate
→ Chapter 2
```

The same pattern repeats for Chapter 2, Chapter 3, and all remaining chapters.
