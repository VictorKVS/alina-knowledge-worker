# ALINA / FATHER — K1 Creation and Development Plan

## Goal
Build a traceable source-to-knowledge pipeline for books, technical documents and legal/regulatory material without confusing file discovery with factual or legal verification.

## Core model
PHYSICAL_COPY -> SOURCE -> DOCUMENT -> REVISION -> STRUCTURAL_UNIT -> EVIDENCE -> KNOWLEDGE -> COMPETENCE

## Current automation boundary

| Stage | Automatic | Gate condition |
|---|---:|---|
| K1.3A Master Registry | yes | missing/inconsistent master registry |
| K1.3B Identity preparation | yes | missing identity layer |
| K1.4 Document import validation | yes | warnings go to review queue |
| K1.5A Legal registry validation | yes | legal registry missing |
| K1.5C Semantic metadata | yes | low confidence is flagged |
| K1.5D Official verification | conditional | human/authoritative verification required when status/revision is unverified |
| K1.6+ structure/requirements | planned | starts only after verification policy is satisfied |

## Measurement model
For each run capture:
- count of records entering each stage;
- elapsed time per stage;
- warnings and hard errors;
- review-queue share;
- automation yield to first human gate;
- rework ratio when reruns are comparable;
- throughput;
- speedup vs 1-stream baseline only when baseline exists;
- ETA only when remaining volume and stable throughput are known.

## Experiment principle
Every approach has an expectation and conditions where it should work better or worse. Observed facts must replace expectations over time.

## Review policy
Green candidates can continue automatically only when mandatory evidence checks pass. Yellow candidates go to review. Red/blocked candidates stop the affected branch. High confidence alone never asserts that a legal document is currently effective.

## Dashboard
The local dashboard shows:
1. expected vs observed performance;
2. stage funnel;
3. first human gate;
4. review pressure;
5. warnings/errors;
6. throughput and run history;
7. NO_DATA instead of invented speedup, rework or ETA.
