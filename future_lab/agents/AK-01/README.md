# AK-01 — ALINA Knowledge Analyst

Роль: отдельный производственный агент FATHER для извлечения, структурирования и подготовки знаний под конкретного целевого агента.

## Не путать

- AU-01 — анализирует предметную ситуацию.
- AK-01 — превращает источники в знания для агентов.
- AKN-01 — курирует качество, версии и актуальность знаний.

## Основная формула

SOURCE
+ TARGET AGENT
+ AGENT TASKS
+ REQUIRED CAPABILITIES
=
AGENT-SPECIFIC KNOWLEDGE PACK

## Входы

- книги;
- статьи;
- стандарты;
- официальная документация;
- проверенные web-источники;
- профиль целевого агента;
- его задачи и ограничения.

## Выходы

- Knowledge Units;
- Method / Algorithm Passports;
- Formula Units;
- Claim / Evidence records;
- Contradictions;
- Unknowns;
- Knowledge Graph edges;
- Agent Knowledge Pack;
- provenance / traceability.

## Производственный поток

SOURCE INTAKE
→ SOURCE CLASSIFICATION
→ TARGET AGENT ANALYSIS
→ KNOWLEDGE EXTRACTION
→ NORMALIZATION
→ CLAIM / EVIDENCE SPLIT
→ CONTRADICTION CHECK
→ KNOWLEDGE GRAPH
→ METHOD / ALGORITHM PASSPORTS
→ KNOWLEDGE PACK
→ AKN-01 REVIEW
→ CODEX / QA / FUTURE LAB QUALIFICATION
→ QUALIFIED KNOWLEDGE

## Уровни знания

RAW
→ EXTRACTED
→ VERIFIED
→ QUALIFIED

Только QUALIFIED может автоматически использоваться боевым агентом без дополнительного предупреждения.
