# ALINA Book → Knowledge → FATHER Protocol v1

## Purpose

Train ALINA to convert books and long-form technical sources into traceable engineering knowledge for FATHER.

ALINA is **not** a summarizer in this process.

The target output is:

```text
SOURCE
  -> CLAIM / CONCEPT
  -> NORMALIZED KNOWLEDGE ATOM
  -> ENGINEERING IMPLICATION
  -> CAPABILITY
  -> ADR / DECISION CANDIDATE
  -> BLOCK / CHASSIS / POLICY TARGET
  -> TEST / EVIDENCE TARGET
  -> PRODUCT DESTINATION
```

## Non-negotiable rules

1. Extraction does not imply truth.
2. A source-derived statement must remain distinguishable from ALINA inference.
3. No knowledge atom without provenance.
4. No architectural decision is accepted only because one book says so.
5. External validation and repository scouting are separate stages.
6. Conflicts between sources are preserved.
7. Rejected ideas remain as negative knowledge.
8. Copyrighted source text is not copied into the KB beyond minimal quotation necessary for evidence.
9. A book can suggest a block; only tests and evidence can make the block production-ready.
10. ALINA must never silently fill gaps with general knowledge.

## Knowledge atom classes

- `FACT` — explicitly supported by the source.
- `CONCEPT` — definition or architectural idea from the source.
- `RECOMMENDATION` — author advice.
- `LIMITATION` — failure mode, caveat or boundary.
- `PATTERN` — reusable implementation or architecture pattern.
- `EXPERIMENT` — exercise or test proposed by the source.
- `TOOL_REFERENCE` — framework, repository, API or product mentioned.
- `OPEN_QUESTION` — unresolved issue in the source.
- `ALINA_INFERENCE` — ALINA mapping or interpretation, never presented as source fact.

## Required fields per atom

```json
{
  "knowledge_id": "KNOW-...",
  "source_id": "SRC-...",
  "source_scope": "chapter/section/page",
  "class": "FACT|CONCEPT|RECOMMENDATION|LIMITATION|PATTERN|EXPERIMENT|TOOL_REFERENCE|OPEN_QUESTION|ALINA_INFERENCE",
  "statement": "...",
  "source_support": "explicit|strong|partial",
  "confidence": 0.0,
  "engineering_implication": "...",
  "capabilities": [],
  "candidate_artifacts": [],
  "validation_needed": [],
  "status": "EXTRACTED|MAPPED|VALIDATED|REJECTED|IMPLEMENTED|PROVEN"
}
```

## Learning loop

For each chapter:

1. Register source scope.
2. Extract candidate atoms.
3. Remove duplicates.
4. Separate source statements from ALINA inference.
5. Map atoms to FATHER capabilities.
6. Identify missing evidence.
7. Search for external implementations only after the extraction pass is closed.
8. Compare candidate implementations.
9. Choose REUSE / ADAPT / BUILD / REJECT.
10. Record tests and evidence.
11. Review errors in ALINA's extraction.
12. Update ALINA rules when repeated mistakes appear.

## Self-improvement signals

ALINA tracks:

- unsupported inference rate;
- provenance completeness;
- duplicate atom rate;
- mapping precision;
- contradiction detection rate;
- wrong implementation recommendation rate;
- missed high-value knowledge;
- stale-source rate.

A failed or corrected mapping becomes a training example for the next run.

## First training source

`SRC-BOOK-0001`

*Designing Large Language Model Applications: A Holistic Approach to LLMs* — Suhas Pai, O'Reilly, 2025.

The first controlled run uses Preface + Chapter 1 only.
