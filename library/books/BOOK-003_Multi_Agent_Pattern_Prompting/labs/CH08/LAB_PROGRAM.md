# BOOK-003 CH08 — лабораторная программа A/B/C

**Тема:** Pattern-Guided Coding: Using Patterns as the Design Vocabulary for GenAI Systems Built on RabbitMQ · **Оригинал PDF 152–181** · **DESIGNED_ONLY / NOT_RUN**.

## A — фундаментальная учебная проверка
**Задача:** освоить и проверить ключевой механизм: Shared pattern vocabulary for coding agents. Сформировать 8–12 синтетических входов с эталонными результатами. Использовать детерминированные Python mock/stub где возможно, без обращения к реальным клиентским системам.

**Последовательность:**
1. Описать requirement, role map и messaging constraints
2. Разложить решение на GoF, EIP и reliability patterns
3. Зафиксировать каждое решение с Approve/Modify/Reject
4. Сгенерировать конфигурацию, диаграммы, security и DLQ manifests

**Приёмка A:** вход и выход проверяются по явным схемам; нет скрытых внешних действий; для каждой ошибки сохраняется trace и тип дефекта.

## B — сравнительная лаборатория
**Цель:** сравнить предложенный автором подход с простой контрольной реализацией (например Python workflow без брокера/LLM или baseline retrieval) на одном зафиксированном наборе. Дополнительный вариант — альтернативная модель/брокер только при необходимости и лицензионной допустимости.

**Измерения:** task success, correctness/evidence precision, p50/p95 latency, tokens/cost, recoverability, duplicate side effects, false positives; метрики, не относящиеся к конкретному разделу, помечать N/A. Замораживать baseline и единый test corpus до сравнения. 

**Обязательные негативные случаи:**
- Команды Topologos — команды шаблона, не встроенные команды RabbitMQ.
- Нельзя автоматически считать сгенерированный YAML корректным.
- Aggregated result нельзя принимать до проверки correlation ID, timeout и неполного набора ответов.

## C — интеграция FATHER и экзамен POLYGON
`ALINA evidence KB → Agent Blueprint/Block Matcher → configured module → UAG policy → mock executor / controlled services → evidence → independent POLYGON`.

**Контрольные инварианты:** никакого выхода за согласованный scope, заявка LLM не равна разрешению, источник/редакция/версия доступны для аудита, ошибки приводят к контролируемому завершению. Провести fault injection и regression только в собственной изолированной среде. Передавать ALINA только категории ошибок, не закрытые задания экзамена.

## Планируемые артефакты (не созданы как работающее ПО)
`requirements.md, ADR.md, contracts.json, fixtures.jsonl, golden.jsonl, tests/, traces.jsonl, metrics.json, SHA256_manifest.json, qualification.json`.

**Приёмка:** критических нарушений доступа 0; пороги корректности, стоимости и latency устанавливаются до запуска. Полноценные A/B/C эксперименты — после согласованного завершения книжной программы и объединения ALINA KB.
