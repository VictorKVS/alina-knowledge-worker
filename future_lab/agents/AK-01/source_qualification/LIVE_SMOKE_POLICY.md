# AK-01 Live Source Smoke Policy

## Goal

Detect live API drift and availability problems without coupling deterministic CI quality to external network reliability.

## Workflow

`AK-01 Live Source Smoke` checks:
- OpenAlex discovery;
- Crossref discovery;
- at least one returned candidate;
- presence of a persistent identifier or official locator.

## Safety boundary

The smoke workflow:
- is read-only;
- uses bounded result counts;
- has a bounded job timeout;
- is non-blocking for deterministic CI;
- does not qualify or ingest sources;
- must never promote a source to trusted knowledge.

## Failure meaning

A live smoke failure means one of:
- upstream unavailable;
- rate limiting;
- API/schema drift;
- network/DNS/TLS failure;
- adapter mapping drift.

It does **not** by itself mean that the deterministic factory line is defective.

A repeated live smoke failure should create an adapter investigation issue/delta before production reliance.
