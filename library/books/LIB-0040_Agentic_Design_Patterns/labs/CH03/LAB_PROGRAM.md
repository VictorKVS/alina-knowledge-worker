# LIB-0040 CH03 — Parallelization / Scatter-Gather: A/B/C

**Источник:** Antonio Gulli, PDF 48–63; LangChain `RunnableParallel` + synthesis. **DESIGNED_ONLY / NOT_RUN / NOT_QUALIFIED**.

## A — без LLM
Создать 3 синтетических асинхронных обработчика, например `asyncio.sleep()` + фиксированный ответ. Сравнить `sequential` с `asyncio.gather()` и проверить, что итог содержит все три результата, а не произвольный порядок завершения.

## B — LangChain
Программа `examples/ch03_parallelization.py`: `OPENAI_API_KEY`, 3 независимых `Runnable`, `RunnableParallel`, затем synthesis. Сравнить sequential baseline и parallel. Записать versions/model, latency p50/p95, количество вызовов (в норме 4), token cost, failures/rate limits. Фактического теста здесь пока нет.

## C — FATHER / POLYGON
Адаптировать три ветви для ALINA: источники/термины/вопросы (либо три independent source readers). Ввести явный `task_id, branch_id, evidence_refs, status`; fan-in принимает только нужные ветви с одним `task_id`. При timeout — управляемый отказ или явный `PARTIAL`, никогда неподтверждённое `PASS`. Проверить retries, duplicates, out-of-order delivery, mixed-tenant inputs, prompt injection in a branch result. POLYGON использует независимый закрытый набор.

## Приёмка
Функциональная корректность, schema-valid result, complete fan-in, отсутствие cross-tenant mix, 0 неразрешённых tool calls; производственные пороги установить до прогона; `NOT_RUN` до реального замера.
