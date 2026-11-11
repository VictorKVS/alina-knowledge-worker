# AK-01 — Source Qualification Engine

## Mission
Determine whether a candidate source is suitable to contribute knowledge to an agent.

The engine never treats existence, popularity, DOI/ISBN, search rank or citation count as sufficient evidence of quality.

## Pipeline

CANDIDATE SOURCE
→ IDENTIFY OBJECT TYPE
→ VERIFY IDENTITY
→ VERIFY VERSION / CORRECTIONS / RETRACTIONS
→ VERIFY PUBLISHER / VENUE / AUTHORSHIP
→ ASSESS METHODOLOGICAL QUALITY
→ ASSESS RELEVANCE TO TARGET CLAIM
→ ASSESS RECENCY / APPLICABILITY
→ ASSESS CONFLICTS / LIMITATIONS
→ ASSIGN SOURCE CLASS
→ ASSIGN PERMITTED USE
→ LINK CLAIMS TO EVIDENCE

## Verdicts
- ACCEPT_PRIMARY
- ACCEPT_SUPPORTING
- ACCEPT_WITH_LIMITS
- DISCOVERY_ONLY
- QUARANTINE
- REJECT

## Hard rejection / quarantine signals
- retracted work
- unverifiable identity or fabricated venue
- unresolved source integrity mismatch
- anonymous high-impact claim with no evidence
- predatory or deceptive publication signals
- severe methodological defect for the claim being used
- source content altered without traceable version
- known paper-mill/fabrication concern without resolution

## Important
Source quality is claim-dependent.
A source can be strong for one claim and weak for another.
