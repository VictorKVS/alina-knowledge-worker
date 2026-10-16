# ALINA Knowledge Graph Auditor v1

Status: design specification; implementation and tests pending.

## Mission
Extract semantic nodes and relations from documents and GitHub repositories, assign transparent weights, re-evaluate them with GPT as a fallible reviewer, and publish only approved knowledge artifacts for other FATHER agents. The implementation belongs to ALINA Analyst; other agents consume interfaces, not duplicated pipelines.

## Pipeline
Source intake -> versioned snapshot -> extraction -> entity resolution -> claims/relations -> deterministic baseline scoring -> GPT critique -> evidence re-check -> evaluation -> human/automated approval gate -> canonical Knowledge Core -> agent retrieval API.

## Node contract
node_id, type, canonical_label, aliases, source_refs, claim_refs, version, observed_at, valid_from, valid_to, status, provenance, owner.

## Edge contract
edge_id, from_node_id, to_node_id, predicate, evidence_refs, polarity, confidence, scoring_version, reviewer_versions, disagreements, status.

## Weight vector (0..1 unless explicitly categorical)
relevance, evidence_strength, source_reliability, relation_confidence, freshness, criticality, contradiction_risk.
Scores require rubric_id, input_evidence_ids, computed_at, algorithm_version, uncertainty and rationale. Do not collapse unrelated dimensions into a single unexplained score.

## GPT reviewer
Receives source excerpts with stable citations, proposed nodes/edges, deterministic score components and rubric. Returns JSON containing proposed corrections, disagreements, evidence gaps and abstentions. The model may not self-approve, silently rewrite sources, or elevate unsupported claims. Independent verification must use source checks, rules, and labeled test cases; same-model re-query alone is insufficient.

## GitHub workflow
Read-only fetch from approved repos/refs; pin commit SHA and file path; respect licensing and sensitive-data controls. Produce sanitized JSON reports and Markdown reviews on feature branch via PR. Require CI schema/provenance tests and explicit approval for canonical publication. Never auto-push raw private documents or secrets.

## Shared API contracts
GET /knowledge/nodes/{id}
GET /knowledge/edges?node_id=...
POST /knowledge/query (scoped, audited)
GET /knowledge/provenance/{claim_id}
GET /knowledge/evaluations/{run_id}
API paths are proposed contracts, not deployed endpoints.

## Security / DevSecOps
Treat retrieved documents and repository content as untrusted data. Protect against prompt injection, poisoned knowledge, misleading citations, secret exfiltration and unauthorized scope expansion. Enforce permissions outside model; immutable evidence history and rollback.

## MVP acceptance
1. Extract nodes/edges from 3 synthetic documents.
2. Detect aliases and duplicate nodes.
3. Cite exact evidence spans.
4. Compute rubric-based weights with versioning.
5. Flag contradictory evidence and stale sources.
6. Reject unsupported GPT weight changes.
7. Produce sanitized GitHub review artifact.
8. Export approved graph for mock consumer agent.
9. No secret or out-of-scope source access.
10. Repeatable evaluation with golden fixtures.

## Status
No claim of successful tests or deployed services. Next: implement schema, deterministic scoring and fixtures before live GPT integration.
