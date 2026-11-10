# ALINA-BOOK as a FATHER Product

## Product position

ALINA-BOOK is the first qualification showcase for **AU-01 — Universal Analyst / “Alina Analyst”**.

It is not a separate analytical core. The reusable block is AU-01; ALINA-BOOK supplies the narrative domain pack, product UI and benchmark workflows.

```text
FATHER PLATFORM
      |
      +-- AU-01 Universal Analyst
             |
             +-- Narrative Pack
                    |
                    +-- ALINA-BOOK
```

## Why this product is the first factory run

Narrative analysis exercises the same primitives required by later OSINT and security products:

- entity extraction;
- event extraction;
- relationships;
- chronology;
- claims and evidence;
- contradictions;
- hypotheses;
- uncertainty;
- forecasting;
- backtesting;
- traceable reporting.

The Alice benchmark is therefore a **qualification case**, not a hard-coded subject specialization.

## Reuse-first rule

Existing repository capabilities are retained where suitable:

- local document processing;
- provenance-preserving fragments;
- SQLite/FTS runtime;
- resumable processing;
- process engine;
- dashboard;
- tests;
- A0–A5 analysis concept.

FATHER additions wrap and qualify these capabilities rather than replacing them without evidence.

## MVP route

```text
SOURCE
  -> INGEST
  -> STRUCTURE
  -> ENTITIES / EVENTS / RELATIONS / CLAIMS
  -> TIMELINE
  -> EVIDENCE / PROVENANCE
  -> HYPOTHESES
  -> FORECAST
  -> KNOWN FUTURE
  -> BACKTEST
  -> ERROR ANALYSIS
  -> REPORT
```

## MVP boundary

The MVP must be executable end-to-end. Deep reasoning stages may initially use deterministic fixtures, but every simulated component must be explicitly marked.

The product must never represent fixture data as live research or generated model text as verified evidence.

## Factory rule

Each station on the FATHER Production Floor must produce:

1. a versioned artifact;
2. status;
3. evidence;
4. open decisions;
5. blockers;
6. handoff contract.

A station is not DONE because an LLM produced prose.

## Target releases

- **0.1 / AU-01 M0** — working product case, jobs/status, deterministic narrative fixture, result contract.
- **0.2 / AU-01 M1** — real structured extraction for entities/events/relations/claims.
- **0.3 / AU-01 M2** — evidence and provenance graph.
- **0.4 / AU-01 M3** — hypotheses, contradictions and unknown registry.
- **0.5 / AU-01 M4** — forecast and backtesting.
- **1.0** — first qualified ALINA-BOOK product release through POLYGON.

## Acceptance principle

A release is acceptable only if a result can be traced from:

```text
user/product requirement
  -> process step
  -> analysis output
  -> evidence/source
  -> verification test
  -> release evidence
```
