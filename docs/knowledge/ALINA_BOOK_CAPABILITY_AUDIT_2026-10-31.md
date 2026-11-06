# ALINA BOOK CAPABILITY AUDIT — 2026-10-31

## Scope

Audit against the target book workflow:

1. translation;
2. semantic decomposition;
3. glossary;
4. applications;
5. examples;
6. algorithms;
7. conclusions;
8. combinations;
9. checklists;
10. FATHER mapping.

## Current implementation status

| Capability | Status | Evidence / current behavior | Required work |
|---|---|---|---|
| File ingestion | READY | PDF/DOC/RTF/EPUB/FB2 extraction exists | keep |
| PDF incremental reading | READY | chunked processing with locators | keep |
| OCR fallback | PARTIAL | Windows OCR path exists | quality gate |
| Source provenance | READY | sha + locator + excerpts | extend to every semantic artifact |
| Book routing | BASIC | folder-based classification, not semantic | replace/augment with semantic classification |
| Translation | NOT IMPLEMENTED | no translation/LLM stage in runtime | add semantic worker |
| Semantic outline | NOT IMPLEMENTED | current notes are mechanical excerpts | add outline extractor |
| Glossary | NOT IMPLEMENTED | no term model/runtime | add glossary entities |
| Applications/use cases | NOT IMPLEMENTED | no extractor | add application model |
| Examples | NOT IMPLEMENTED | no structured example extraction | add example model |
| Algorithms/procedures | NOT IMPLEMENTED | no algorithm extraction | add algorithm model |
| Conclusions | NOT IMPLEMENTED | no author-vs-ALINA conclusion separation | add conclusion entities |
| Combinations/synthesis | NOT IMPLEMENTED | no cross-atom hypothesis engine | add synthesis stage |
| Checklists | NOT IMPLEMENTED | no traceable checklist generator | add checklist stage |
| Knowledge atoms | DESIGN READY | protocol/contract exists | implement runtime |
| Contradictions | DESIGN/PARTIAL | intelligence protocol requires them | implement book-specific detector |
| FATHER mapping | DESIGN READY | protocol + first manual run exists | automate handoff |
| Self-improvement feedback | DESIGN READY | metrics/rules defined | persist corrections and score future runs |

## Key finding

The current ALINA repository is a **reliable document ingestion and process-control foundation**, not yet a semantic knowledge worker.

The next implementation milestone is therefore not "read more books". It is:

> implement the semantic worker that produces a valid `father.book_knowledge_package.v1`.

## Required package per chapter

```text
ORIGINAL
  ↓
TRANSLATION
  ↓
SEMANTIC OUTLINE
  ↓
GLOSSARY
  ↓
APPLICATIONS
  ↓
EXAMPLES
  ↓
ALGORITHMS
  ↓
AUTHOR CONCLUSIONS
  ↓
ALINA SYNTHESIS / COMBINATIONS
  ↓
CHECKLISTS
  ↓
KNOWLEDGE ATOMS
  ↓
FATHER MAPPING
```

## Acceptance rule

A chapter is not considered learned merely because its text was extracted.

It is learned only when:

- translation is traceable;
- semantic coverage is reviewed;
- glossary terms are linked;
- examples and algorithms are reconstructed;
- conclusions are separated by owner;
- combinations are marked as hypotheses;
- checklists trace back to knowledge;
- FATHER mappings are reviewed;
- unresolved contradictions remain visible.
