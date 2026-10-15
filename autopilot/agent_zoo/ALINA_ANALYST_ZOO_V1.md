# ALINA Analyst — Agent Zoo v1

Status: design baseline; agents below are contracts, not claims of running deployments.

## Mission
Convert raw inputs into evidence-backed, reproducible analytical decisions.

## Orchestration
Lead Analyst -> Task Classifier -> Planner -> parallel specialist agents -> Evidence Verifier -> Critic -> Evaluator -> Reporter -> Decision Memory.

## Agent roster
| ID | Agent | Mission | Output |
|---|---|---|---|
| A01 | Lead Analyst | decompose task, orchestrate | task plan |
| A02 | Source Scout | discover lawful sources | source registry |
| A03 | Evidence Collector | preserve provenance | evidence bundle |
| A04 | Entity Resolver | normalize entities/IDs | entity mappings |
| A05 | Graph Analyst | connect entities and relationships | graph claims |
| A06 | Legal/Compliance Analyst | determine normative applicability | requirement mapping |
| A07 | Threat Analyst | model threats and attack scenarios | threat hypotheses |
| A08 | Risk Analyst | evaluate likelihood, impact, uncertainty | risk register |
| A09 | Security Architect | map controls and gaps | control plan |
| A10 | OSINT Analyst | passive, authorized external research | OSINT evidence |
| A11 | Critic/Verifier | challenge claims and detect contradictions | verification verdict |
| A12 | Evaluation Agent | score groundedness, completeness, safety | evaluation record |
| A13 | Report Agent | produce traceable deliverables | report |
| A14 | Learning Agent | propose updates to KB/methods | change proposal |

## Common contract
Inputs: task_id, scope, permitted_sources, context_refs, budget, policy_version.
Outputs: structured artifact, evidence_refs, uncertainty, errors, run_id, agent_version.
Statuses: proposed, implemented, tested, approved, deployed.

## Security
Read-only by default; explicit authorization for active scans. Treat external content as untrusted. No secrets in evidence. No self-promotion of claims or autonomous production modification.

## First acceptance case
CyberED case: asset -> threat -> vulnerability -> scenario -> risk -> normative requirement -> control -> evidence -> gap -> recommendation. Test citations, false positives, abstention, contradictions and traceability.
