# BOOK-003 CH07 — лабораторная программа A/B/C

**Тема:** Tips and Best Practices · **Оригинал PDF 134–151** · **DESIGNED_ONLY / NOT_RUN**.

## A — фундаментальная учебная проверка
**Задача:** освоить и проверить ключевой механизм: R&D mindset; small POCs; latency and throughput. Сформировать 8–12 синтетических входов с эталонными результатами. Использовать детерминированные Python mock/stub где возможно, без обращения к реальным клиентским системам.

**Последовательность:**
1. Задать security/privacy и cost budget до разработки
2. Определить POC, baseline и регулярную eval-сборку
3. Version prompts, models, corpus, tools, datasets и policy
4. Измерять latency, throughput, error rates, drift и затраты

**Приёмка A:** вход и выход проверяются по явным схемам; нет скрытых внешних действий; для каждой ошибки сохраняется trace и тип дефекта.

## B — сравнительная лаборатория
**Цель:** сравнить предложенный автором подход с простой контрольной реализацией (например Python workflow без брокера/LLM или baseline retrieval) на одном зафиксированном наборе. Дополнительный вариант — альтернативная модель/брокер только при необходимости и лицензионной допустимости.

**Измерения:** task success, correctness/evidence precision, p50/p95 latency, tokens/cost, recoverability, duplicate side effects, false positives; метрики, не относящиеся к конкретному разделу, помечать N/A. Замораживать baseline и единый test corpus до сравнения. 

**Обязательные негативные случаи:**
- Не подключать сырой LLM-output напрямую к критическим IT-системам.
- Нельзя считать один удачный ответ статистическим подтверждением качества.
- Prompt version без версии model/data/tool не гарантирует воспроизводимость.

## C — интеграция FATHER и экзамен POLYGON
`ALINA evidence KB → Agent Blueprint/Block Matcher → configured module → UAG policy → mock executor / controlled services → evidence → independent POLYGON`.

**Контрольные инварианты:** никакого выхода за согласованный scope, заявка LLM не равна разрешению, источник/редакция/версия доступны для аудита, ошибки приводят к контролируемому завершению. Провести fault injection и regression только в собственной изолированной среде. Передавать ALINA только категории ошибок, не закрытые задания экзамена.

## Планируемые артефакты (не созданы как работающее ПО)
`requirements.md, ADR.md, contracts.json, fixtures.jsonl, golden.jsonl, tests/, traces.jsonl, metrics.json, SHA256_manifest.json, qualification.json`.

**Приёмка:** критических нарушений доступа 0; пороги корректности, стоимости и latency устанавливаются до запуска. Полноценные A/B/C эксперименты — после согласованного завершения книжной программы и объединения ALINA KB.
