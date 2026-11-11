# AK-01 Live Source Adapters

## Purpose

Live adapters are discovery-only components. They translate external APIs into the common FATHER SourceCandidate contract.

## Current adapters

- OpenAlex
- Crossref

## Boundary

Adapters may:
- issue discovery queries;
- map external metadata;
- preserve identifiers and raw metadata;
- report transport failures.

Adapters may not:
- assert source quality;
- mark a source ACCEPTED;
- infer that DOI implies trust;
- promote candidates into qualified knowledge.

## OpenAlex mapping

Work search uses the OpenAlex works endpoint with a search query and bounded result count. Candidate provenance preserves the OpenAlex/DOI locator and raw returned metadata.

## Crossref mapping

Bibliographic discovery uses the Crossref works endpoint with query.bibliographic and bounded rows. Candidate provenance uses DOI as the persistent locator.

## Test strategy

CI does not depend on external network availability. HTTP JSON retrieval is injected into each adapter, and contract tests use deterministic API-shaped fixtures.

A separate live smoke workflow may be introduced later with:
- explicit timeout;
- non-destructive read-only calls;
- bounded rate;
- failure classification;
- no source acceptance based solely on smoke success.
