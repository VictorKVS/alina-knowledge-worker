# C0.5 — Canonical Entity Model (draft v1)

Status: PROPOSED / non-destructive

## Identity and provenance
Each entity: id, type, source_refs, version, created_at, updated_at, confidence, verification_status, owner, evidence_refs.

## Entities
Source, Snapshot, Chunk, Claim, Evidence, Document, Requirement, Applicability, Obligation, Role, Competency, Asset, Threat, Vulnerability, AttackScenario, Control, Risk, Method, Agent, AgentVersion, Task, Evaluation, DecisionMemory.

## Relationships
Document --contains--> Requirement
Requirement --applies_to--> Asset
Requirement --requires--> Control
Asset --exposed_to--> Threat
Threat --exploits--> Vulnerability
Vulnerability --enables--> AttackScenario
AttackScenario --affects--> Asset
Control --mitigates--> Risk
Evidence --supports_or_refutes--> Claim
AgentVersion --executes--> Task
Task --produces--> Evidence
Evaluation --scores--> AgentVersion
DecisionMemory --references--> Evidence

## Ownership
KNOWLEDGE_CORE owns canonical evidence and decisions. SecGraph provides security-graph projection. CyberED provides curriculum, tasks and evaluations. OSINT supplies evidence. ALINA runtime is an adapter/cache.

## Gates
Do not promote unverified claims. No automatic destructive schema migrations. Human approval required for production or security-boundary changes.
