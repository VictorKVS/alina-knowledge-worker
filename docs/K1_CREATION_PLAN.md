# ALINA / FATHER — K1 Creation and Development Plan

## Goal
Build a traceable source-to-knowledge pipeline for books, technical documents and legal/regulatory material without confusing discovery, extraction, inference and legal verification.

## Canonical model
PHYSICAL_COPY -> SOURCE -> DOCUMENT -> REVISION -> STRUCTURAL_UNIT -> EVIDENCE -> KNOWLEDGE -> COMPETENCE

## Autonomous execution boundary

| Stage | Action | Automatic | Stop condition |
|---|---|---:|---|
| K1.0 | discover known inventories/catalogs | yes | required library inventory cannot be found |
| K1.3A | create/upsert Master Source Registry | yes | malformed inventory or identity collision |
| K1.3B | build identity candidates | yes | malformed source registry |
| K1.4 | import/upsert document corpus | yes | malformed document catalog |
| K1.INVARIANTS | validate source/copy integrity | yes | orphan copy, duplicate physical path, digest conflict |
| K1.5A | create/upsert legal-document registry | yes | unsafe registry inconsistency |
| K1.5C | select legal pilot and extract semantic metadata | yes | inaccessible PDF, OCR/extractor required |
| K1.5D | create/update official verification task | yes | HUMAN_GATE until authoritative verification exists |
| K1.6+ | structure, clauses, requirements, definitions | next phase | starts only after verification policy is satisfied |

## Idempotency and durability
Repeated runs must not create duplicate SOURCE, PHYSICAL_COPY, LEGAL_DOCUMENT or verification-task entities. Derived files are written atomically. Before replacement, the previous derived file is copied into the K1 backup area.

## Evidence policy
Raw source identity and extracted evidence are preserved separately from normalized/inferred candidates. A confidence score never promotes a legal-status assertion. EFFECTIVE, REPEALED, current revision and similar fields require authoritative verification.

## Measurement model
Every run captures records read/written, created/updated/skipped, stage duration, warnings/errors, review pressure, automation yield, throughput and history. Relative speed may be shown only for comparable runs with the same observed input volume.

Speedup versus one-stream baseline, rework ratio and ETA remain NO_DATA until the required telemetry exists.

## Experiment model
For each approach store:
- expectation;
- conditions where it should perform better;
- conditions where it can perform worse;
- observed stage result;
- runtime metrics.

The dashboard is an experiment board, not a decorative status page.

## Human review policy
GREEN: mandatory evidence checks passed; continue automatically.
YELLOW: ambiguity is isolated into a review queue; unaffected branches may continue.
RED/BLOCKED: invariant or prerequisite failure; stop the affected pipeline branch.
HUMAN_GATE: a decision or authoritative verification cannot be safely inferred.

## Runtime outputs
Runtime data remains local under data/k1-run:
- latest.json;
- history.jsonl;
- DEV_JOURNAL_K1.md.

Real books, extracted passages, private registries and runtime history are not committed to Git.
