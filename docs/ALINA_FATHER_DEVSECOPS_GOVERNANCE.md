# ALINA Analyst / Agent Zoo — FATHER DevSecOps Governance

Status: DESIGN BASELINE (not certification or deployment evidence)

## Lifecycle
1. Scope / business goal / stakeholder requirements
2. Source and regulatory applicability registry
3. Threat model, trust boundaries, risk register
4. Architecture: C4 context/container/component, data flows, ADRs
5. Data/entity schema and agent input-output contracts
6. Implementation plan, acceptance criteria, test cases
7. Feature-branch implementation with review
8. CI: lint/type checks, unit/integration, SAST, SCA, secret scan, SBOM, container scan
9. LLM/agent evaluation: groundedness, citations, prompt injection, tool authorization, PII leakage, refusal/abstention, reproducibility
10. Human approval, release, rollback plan
11. Runtime audit, metrics, incident handling, drift and continuous improvement

## Required documentation per change
Requirement ID -> Design/ADR -> Threat -> Control -> Code/PR -> Test -> Evidence -> Decision -> Release -> Observability.
Never label a planned check as passed without run evidence.

## Regulatory applicability (Russia)
Candidate sources to assess by system type and current editions: 149-FZ, 152-FZ, 187-FZ, Government Decree 1119, FSTEC orders 17/21/235/239 where applicable, FSB Order 378 where applicable, sector rules, GOST, contractual obligations. Confirm validity, version, scope and exceptions against official publications before asserting applicability. Avoid treating all acts as universally applicable.

## LLM-specific threats
OWASP LLM Top 10, MITRE ATLAS, RAG poisoning, prompt injection, tool privilege escalation, exfiltration, hallucinated compliance, unsafe autonomy, supply chain and model provenance.

## Release gates
G0 requirements approved; G1 architecture and threat model approved; G2 tests/CI evidence; G3 security/evaluation acceptance; G4 deployment authorization; G5 post-release evidence.
Human approval required for active OSINT scans, security boundary changes, production writes and destructive migrations.

## Artifacts
requirements.md; applicability_matrix.csv; architecture.md; adr/; threat_model.md; risk_register.csv; agent_contracts/; test_plan.md; eval_cases.jsonl; sbom; ci_evidence/; release_checklist.md; operations_runbook.md; decision_log.md.
