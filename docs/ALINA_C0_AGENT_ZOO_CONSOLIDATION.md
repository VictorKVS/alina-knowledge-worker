# ALINA C0 Consolidation — Agent Zoo Mission

## Purpose
C0 is the mandatory consolidation stage before new K3→K10 structures are allowed to duplicate existing FATHER assets.

ALINA Lead orchestrates Agent Zoo. Agents operate READ → ANALYZE → MAP → PROPOSE → TEST. Existing production repositories, databases and schemas are not deleted, renamed, moved or mass-migrated during C0.

## Three canonical verticals
1. **ALINA Legal & Compliance / «Алина Правовед»** — normative documents, clauses, requirements, applicability, obligations, role/responsibility basis, controls and evidence.
2. **ALINA Project / Organization & Competency** — professions, roles, tasks, competencies, knowledge, skills, tools, interfaces and team dependencies.
3. **ALINA Self / Agent Engineering** — ALINA's own competencies, knowledge, methods, prompts, RAG, tools, evaluation and controlled improvement.

These are competency domains of one ALINA Core, not three independent products.

## Shared end-to-end model
`Document → Requirement → Obligation → Role → Competency → Knowledge → Method → Agent → Action → Control → Evidence`

No edge implying personal/legal responsibility may be invented. Responsibility must retain its legal/organizational basis and provenance.

## Zoo roles
- Inventory Agent — repositories, databases, schemas, documents and services.
- History Agent — README/ADR/journals/commits and original purpose.
- Schema Agent — entities, fields, APIs and semantic overlap.
- Dedup Agent — KEEP / MERGE / ADAPTER / MIGRATE / DEPRECATE / MISSING proposals.
- Graph Agent — cross-system entity/relationship map.
- Legal Analyst — validates legal provenance/status/responsibility semantics.
- Competency Analyst — maps profession→role→task→competency→knowledge/skill.
- ALINA Self Analyst — maps ALINA competency/method/RAG/evaluation gaps.
- Architect Agent — proposes canonical ownership and integration boundaries.
- Critic Agent — attacks assumptions, provenance loss and unsafe merges.
- Evaluation Agent — verifies mappings with tests and three vertical cases.
- ALINA Lead — synthesis, conflict resolution, task creation and escalation.

## C0 work packages
- C0.1 Repository Inventory
- C0.2 Database Inventory
- C0.3 Schema Mapping
- C0.4 Duplicate/Overlap Detection
- C0.5 Canonical Entity Model
- C0.6 Ownership Map
- C0.7 Integration/Adapter Map
- C0.8 Migration Plan (proposal only)
- C0.9 Three Vertical Test Cases
- C0.10 Consolidation Report + K3/K4 resume decision

## Required inventory scope
At minimum inspect/locate:
- alina-knowledge-worker
- KNOWLEDGE_CORE assets
- osint_kb / normative assets
- security_kb_reference
- SecGraph
- Specialist Factory / Agent Factory assets

Missing or inaccessible systems are recorded as UNKNOWN, never reconstructed from assumptions.

## Exit criteria
C0 passes only when:
- each discovered major entity has a canonical owner or explicit unresolved status;
- overlaps have KEEP/MERGE/ADAPTER/MIGRATE/DEPRECATE/MISSING decisions;
- no destructive production change occurred;
- all three vertical scenarios can be represented by the proposed canonical model;
- provenance survives end-to-end;
- Critic findings are resolved or explicitly accepted;
- machine-readable inventory/mapping artifacts exist.

After PASS, Autopilot resumes K3/K4 implementation against the consolidated model.
