# C0.3 Canonical Schema Mapping

Status: PASSED AT ENTITY/OWNERSHIP LEVEL; COLUMN-LEVEL MIGRATION DEFERRED

## Rule
C0.3 maps semantic ownership first. Historical/local SQL is evidence or a donor until the current owner and compatibility are verified.

| Entity / concern | Canonical owner | Projection / producer | C0 decision |
|---|---|---|---|
| Source, Snapshot, provenance | KNOWLEDGE_CORE | ALINA ingestion, OSINT | KEEP / ADAPTER |
| Chunk | KNOWLEDGE_CORE retrieval layer | ALINA FTS/runtime | ADAPTER |
| Claim, Evidence | KNOWLEDGE_CORE | OSINT, ALINA Analyst | CANONICAL |
| Document, Requirement | Security Knowledge projection | CyberED/Legal sources | CANONICAL PROJECTION |
| Applicability, Responsibility | Security/Legal projection | ALINA Legal/Security Analyst | CANONICAL PROJECTION |
| Asset, Threat, Vulnerability, Scenario | Security graph projection | SecGraph | KEEP / MAP |
| Control, Risk | shared Security + graph boundary | SecGraph / Security KB | MERGE BY ID/RELATION, NOT TABLE FLATTENING |
| Role, Competency | Role Knowledge System | Competency Lab / ALINA Project | CANONICAL |
| Knowledge, Method | KNOWLEDGE_CORE | ALINA Methods/KB | CANONICAL |
| Agent, AgentVersion | Agent Factory | ALINA Self | CANONICAL |
| Evaluation | Eval/Competency layer | CyberED + Evaluation Lab | CANONICAL |
| DecisionMemory | KNOWLEDGE_CORE | all verified workflows | CANONICAL |
| Runtime cache/audit | owning application | ALINA/OSINT/etc. | LOCAL, NOT GLOBAL TRUTH |

## Cross-domain IDs
Canonical objects require stable IDs and provenance. Relationships cross domains by ID/reference. No forced single-table mega-schema.

Core path:
`SOURCE → SNAPSHOT → CHUNK → CLAIM → EVIDENCE → REQUIREMENT → APPLICABILITY → ROLE → COMPETENCY → KNOWLEDGE → METHOD → AGENT → ACTION → CONTROL → RESULT/EVIDENCE → EVALUATION → DECISION MEMORY`

Security path:
`ASSET → THREAT → VULNERABILITY → ATTACK SCENARIO → CONTROL → RISK`

Legal/security bridge:
`DOCUMENT → REQUIREMENT → OBLIGATION → APPLICABILITY → ROLE/RESPONSIBILITY → CONTROL → REQUIRED EVIDENCE`

## Historical schema classification
- repeated Knowledge Factory SQL across working copies: MERGE/DEDUP candidate;
- `osint_kb` snapshot: ADAPTER/MIGRATION SOURCE, not automatically canonical;
- `security_kb_reference` snapshot: REFERENCE/DONOR pending compatibility;
- local SecGraph SQL: DONOR/EVIDENCE because current connected repo does not expose those exact paths;
- third-party research/test schemas: EXCLUDE;
- tutorial/runtime/cache databases: EXCLUDE from canonical knowledge.

## ALINA Security Analyst + CyberED
CyberED is the curriculum/evaluation/source projection. It may produce tasks, expected evidence, rubrics and verified learning artifacts. It does not own global truth.

Training loop:
`CyberED lesson → Security Analyst task → evidence → analysis → evaluator → competency result → verified knowledge/method → Decision Memory`

## Gate result
C0.3 is sufficient to proceed to semantic duplicate detection. Exact column-level migration is intentionally deferred until an actual migration is proposed; no destructive migration is currently needed.
