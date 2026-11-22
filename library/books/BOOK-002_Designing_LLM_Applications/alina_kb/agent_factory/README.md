# ALINA — главный архитектор знаний, промптов, RAG и обучения агентов FATHER

**Версия:** 0.1.0 (архитектурный контракт). **Связь:** BOOK-002 / ALINA Knowledge Core.

## Миссия

ALINA получает требования к компетенции агента, проектирует его базу знаний, словарь и алгоритмы, формирует системные инструкции, RAG-конвейер и учебную программу. После независимых испытаний POLYGON она анализирует ошибки и предлагает версионированное улучшение. FATHER Agent Factory собирает и исполняет разрешённые версии компонентов.

**ALINA — единый интеллектуальный control plane; знания разделяются на ролевые представления и права, а не копируются в отдельные несогласованные базы.**

## Пять обязательных пакетов на каждого агента

1. **Knowledge Package:** узлы, связи, определения, сокращения, алгоритмы, источники, валидность и provenance.
2. **Prompt Package:** role, objective, instructions, reasoning procedure на уровне явных шагов, schema, tool policies, refusal/escalation, prompt version, prompt tests.
3. **RAG Package:** corpora, source ACL, chunking, metadata filters, embeddings/index strategy, rerank, citation policy, freshness/expiry, no-evidence response, injection defense.
4. **Learning Package:** syllabus/prerequisites, tutorials, tasks, public gold examples, feedback plan, competence and progression gates.
5. **Qualification Package:** independent eval plan, frozen datasets, negative tests, robustness/security/regression evidence, owners, exit criteria. Закрытые ответы POLYGON не копировать в открытую учебную базу.

**Дополнительно:** Capability Contract: вход, выход, инструменты, допустимые действия, performance/cost/resource SLO, зависимости и ownership.

## Контур проектирования

```text
Customer requirements
   -> ALINA goal and competence model
   -> ALINA Source Registry and Knowledge Graph
   -> ALINA Knowledge + Prompt + RAG + Learning Packages
   -> FATHER Architect design review / ADR
   -> FATHER Agent Factory assembly (code + tools + workflow)
   -> UAG policy enforcement
   -> POLYGON independent qualification
   -> human release gate
   -> production telemetry and incident feedback
   -> ALINA diagnosis -> change proposal -> new version
```

## ALINA для FATHER Architect — проектировщика самой платформы

FATHER Architect — отдельный **потребитель ALINA** с доступом к архитектурным знаниям, контрактам компонентов, ADR, библиотеке паттернов, тестовым результатам и истории системы. Он предлагает проекты архитектурных изменений. ALINA готовит Knowledge/Prompt/RAG/Learning Packages для этого агента так же, как для OSINT, TIMA и CODEX.

**Защита от самоподтверждения:** FATHER Architect не принимает свои архитектурные решения в обход человека; ALINA не имеет права публиковать новое доверенное знание только потому, что его предложила собственная модель; POLYGON независим от инструкции агента, который испытывается.

## Диагностика модернизации

1. Определить конкретный невыполненный контракт и класс ошибки.
2. Проверить: недостаток источников или устаревшая информация → Knowledge/RAG.
3. Неверное следование процедуре или формат ответа → Prompt/Schema/Workflow.
4. Недопустимые действия → policy/tool/UAG, а не только prompt.
5. Устойчивый дефицит навыка → оценить SFT/PEFT/дополнительные методы обучения после baseline.
6. Сравнить кандидата с текущей версией на замороженном наборе и независимом holdout.
7. Обновить только нужный пакет с version, provenance, ADR и rollback.
8. Принять выпуск через POLYGON и human approval.

## Ограничение готовности

Это **опубликованный архитектурный проект**, не развёрнутая система создания агентов. Никакие обучение моделей, подключение реального RAG или самосовершенствование FATHER этим документом не подтверждаются.

## Первоисточник и наши расширения

Suhas Pai, *Designing Large Language Model Applications*, CH1–CH2: роль данных, источников, очистки, качества и прототипа PDF-RAG. Конкретная 5-пакетная система ALINA, Agent Factory и управление модернизацией — самостоятельная архитектура FATHER, а не цитата книги. Остальные главы будут включаться после изучения оригинала.
