# C0.2 Database Inventory — Consolidated Result

Status: PASSED WITH CLASSIFIED UNKNOWNS

## Local discovery
Sanitized local probe returned 150 datastore/schema artifacts:
- 56 SQLite-like files;
- 94 SQL / Compose / schema artifacts.

## High-value FATHER findings
1. Historical PostgreSQL snapshots explicitly exist for `osint_kb` and `security_kb_reference`.
2. Knowledge Factory SQL appears in multiple historical working copies (FATHER_OPERATOR_CONSOLE, Vibe-coding variants). These are duplication candidates, not automatically independent canonical systems.
3. SecGraph has first-party security schema artifacts including `init_security_kb.sql`, `kg_schema.sql`, course KB schema and seed data.
4. KNOWLEDGE_CORE_IMPORT contains normative-library snapshots and FTS search storage.
5. OSINT_deepseek contains operational SQLite stores (audit, Telegram, cache) plus large third-party research/tool trees. Third-party/test databases must not be promoted into FATHER canonical storage.
6. Numerous tutorial/runtime SQLite databases (Django, Wrangler, image tooling, caches) are unrelated to canonical FATHER knowledge and are classified as EXCLUDE_FROM_CANONICAL unless later evidence proves otherwise.

## Duplicate signals
Repeated table names alone are weak evidence. Examples include auth_group, Cache, _cf_ALARM, alembic_version and collection_metadata; most are framework/runtime artifacts.
A meaningful duplication signal is repeated FATHER SQL/schema files across historical working copies and snapshots.

## Canonical direction for C0.3
- KNOWLEDGE_CORE remains the canonical knowledge architecture.
- Security/Legal projection should reuse existing normative/security structures.
- SecGraph is treated as the security graph projection and schema donor, not replaced by a second ALINA graph.
- OSINT stores remain evidence acquisition/operations sources.
- ALINA SQLite remains local ingestion/runtime evidence cache.
- CyberED is a training/evaluation/source contour for ALINA Security Analyst, not a new canonical database.

## C0.3 mapping targets
Map entities across:
`Source / Snapshot / Chunk / Claim / Evidence / Document / Requirement / Applicability / Role / Responsibility / Asset / Threat / Vulnerability / Scenario / Control / Risk / Competency / Method / Agent / Evaluation / Decision Memory`.

## Data-quality note
The first probe's SQLite table introspection captured only one table per database because the probe reused a cursor while iterating sqlite_master. Therefore table names are useful discovery evidence but NOT a complete schema inventory. C0.3 must use SQL schema artifacts and/or a corrected read-only probe before destructive migration decisions.

No destructive action is authorized by this report.
