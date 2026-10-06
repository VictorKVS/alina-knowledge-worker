# Alina Analyst Process Engine v1

Алина использует два разных слоя:

- **Knowledge source layer** — документы, книги, методы и выдержки.
- **Executable process layer** — зарегистрированные процессы и фактические RUN.

## База SQLite

При старте `alina.py` модуль `process_engine.py` создаёт:

- `process_definitions` — версии зарегистрированных процессов;
- `process_steps` — атомарные шаги;
- `work_runs` — конкретные запуски работы;
- `work_step_runs` — состояние каждого шага запуска.

JSON из каталога `processes/` автоматически регистрируются в БД.

## Исполнение

```text
PROCESS
  ↓
CREATE RUN
  ↓
STEP READY
  ↓
IN_PROGRESS
  ↓
RESULT + EVIDENCE
  ↓
DONE / BLOCKED / NOT_APPLICABLE / REVIEW_REQUIRED
  ↓
NEXT STEP
  ↓
...
  ↓
RUN DONE / BLOCKED / REVIEW_REQUIRED
```

Нельзя перейти к PENDING-шагу напрямую. Нельзя использовать `BLOCKED`, `NOT_APPLICABLE` или `REVIEW_REQUIRED` без объяснения. Terminal-state не переписывается молча в том же RUN.

## API

Чтение:

- `GET /api/processes`
- `GET /api/process?process_id=...`
- `GET /api/run?run_id=...`
- `GET /api/run/next?run_id=...`

Изменение доступно только через существующий локальный token/origin guard:

- `POST /api/run/start/<process_id>`
- `POST /api/run/<run_id>/step/<step_id>`

## Первый мета-процесс

`PROC-ALINA-PROCESS-DESIGN` проектирует новые процессы по цепочке:

```text
GOAL → SCOPE → INPUTS → KNOWLEDGE → ROLES → STEPS
→ ACTIONS/TOOLS → QUALITY GATES → EVIDENCE
→ STATES/FAILURES → FINDINGS/GAPS → OUTPUT
→ COMPLETENESS → REGISTRATION → PILOT → RETROSPECTIVE
```

## Первый прикладной процесс

`RUNBOOK-WEB-SECURITY-001` — Web Security / Authorized Pentest.

ACTIVE_TEST разрешается только после подтверждённого scope. Это ограничение является частью определения процесса, а не рекомендацией интерфейса.
