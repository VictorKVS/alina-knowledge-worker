# AIR-001 Deliverables & Acceptance
## The ten canonical products from ALINA Research Brief
| ID | Artifact | Pass criterion |
|---|---|---|
| 01 | SOURCE_REGISTRY | 30–50 curated, provenance-version-license reviewed relevant source records (target, not achieved) |
| 02 | COMPETENCY_MATRIX | senior analyst behaviors mapped to measurable tests |
| 03 | METHOD_REGISTRY | methodology, prerequisites, risk, applicability and source |
| 04 | PROMPT_REQUIREMENTS | compact invariant rules, tool constraints and output schemas |
| 05 | RAG_CORPUS_PLAN | 8 logical evidence stores, authorized ingestion and temporal versioning |
| 06 | KNOWLEDGE_GRAPH_SCHEMA | claim, source, evidence, independence, change and decision relations |
| 07 | AGENT_TOOL_CONTRACTS | scopes, read/write, error paths, timeout, audit |
| 08 | EVAL_GOLDEN_SET | at least 30–50 expert-reviewed pilot QA pairs with verified clause spans |
| 09 | GAP_REGISTER | unresolved issues with risk, owner, priority and next action |
| 10 | DECISION_RECORD | ADR options, evidence, test result and signoff; no premature approval |

## Evaluation
Claim citation accuracy, provenance completeness, independent source clustering precision, context recall@k, unsupported claim rate, correct abstention, retriever performance and cost, protection against injected instructions, ACL separation.
Metrics require baseline measurement and label calibration; no invented pass percentages. Mandatory zero accepted policy violations in controlled negative tests, with explicit test count and coverage.

## Gates
G0–G4 business/security/legal requirements → G5 alternatives → G6 resource model → G7 design approval → FATHER Site + Zoos E2E → runtime pilot → evidence results → promotion signoff.
This GitHub publication is **documentation completed, not testing executed**.
