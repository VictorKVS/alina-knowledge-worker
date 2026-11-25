# BOOK-003 CH05 — лабораторная программа A/B/C

**Тема:** Starting Your Data Migration Project · **Оригинал PDF 104–119** · **DESIGNED_ONLY / NOT_RUN**.

## A — фундаментальная учебная проверка
**Задача:** освоить и проверить ключевой механизм: Document and data source inventory. Сформировать 8–12 синтетических входов с эталонными результатами. Использовать детерминированные Python mock/stub где возможно, без обращения к реальным клиентским системам.

**Последовательность:**
1. Составить source inventory, owner/license/ACL, formats, revisions
2. Оценить объём, частоту изменений, throughput и expected cost
3. Разделить raw, parsed, cleaned, chunked и indexed datasets
4. Включить incremental sync, checksums, dedup и rollback

**Приёмка A:** вход и выход проверяются по явным схемам; нет скрытых внешних действий; для каждой ошибки сохраняется trace и тип дефекта.

## B — сравнительная лаборатория
**Цель:** сравнить предложенный автором подход с простой контрольной реализацией (например Python workflow без брокера/LLM или baseline retrieval) на одном зафиксированном наборе. Дополнительный вариант — альтернативная модель/брокер только при необходимости и лицензионной допустимости.

**Измерения:** task success, correctness/evidence precision, p50/p95 latency, tokens/cost, recoverability, duplicate side effects, false positives; метрики, не относящиеся к конкретному разделу, помечать N/A. Замораживать baseline и единый test corpus до сравнения. 

**Обязательные негативные случаи:**
- Не поглощать конфиденциальные документы в публичные обучающие наборы.
- Не объявлять все извлечённые связи графа достоверными.
- Игнорирование изменений/удалений документов создаёт устаревшую базу.

## C — интеграция FATHER и экзамен POLYGON
`ALINA evidence KB → Agent Blueprint/Block Matcher → configured module → UAG policy → mock executor / controlled services → evidence → independent POLYGON`.

**Контрольные инварианты:** никакого выхода за согласованный scope, заявка LLM не равна разрешению, источник/редакция/версия доступны для аудита, ошибки приводят к контролируемому завершению. Провести fault injection и regression только в собственной изолированной среде. Передавать ALINA только категории ошибок, не закрытые задания экзамена.

## Планируемые артефакты (не созданы как работающее ПО)
`requirements.md, ADR.md, contracts.json, fixtures.jsonl, golden.jsonl, tests/, traces.jsonl, metrics.json, SHA256_manifest.json, qualification.json`.

**Приёмка:** критических нарушений доступа 0; пороги корректности, стоимости и latency устанавливаются до запуска. Полноценные A/B/C эксперименты — после согласованного завершения книжной программы и объединения ALINA KB.
