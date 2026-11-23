# BOOK-002 — Designing Large Language Model Applications

**Автор:** Suhas Pai · **Подзаголовок:** A Holistic Approach to LLMs · **Издательство:** O’Reilly · **Издание:** март 2025.

> Учебный проект FATHER/ALINA для **начинающего технического студента**: от доступного объяснения до инженерных проектов, испытаний и эксплуатации. Книга предоставлена пользователем в PDF на 765 страниц. Оригинальный PDF здесь не публикуется: © 2025 Suhas Pai, All rights reserved.

## Содержание по оглавлению оригинального PDF

Книга делится на три части:
1. **LLM Ingredients** — составные части языковых моделей (главы 1–4).
2. **Utilizing LLMs** — применение, адаптация, обучение и инференс (главы 5–9).
3. **LLM Application Paradigms** — инструменты, embeddings, RAG и архитектура (главы 10–13).

| № | Глава | Страницы загруженного PDF | Состояние |
|---|---|---|---|
| 1 | Introduction | PDF 27–91 | [Урок 1: разобран](chapters/CH01_RU.md) |
| 2 | Pre-Training Data | PDF 92–167 | [Урок 2: разобран](chapters/CH02_RU.md) |
| 3 | Vocabulary and Tokenization | PDF 168–203 | [Глава 3: изучена](chapters/CH03_RU.md) |
| 4 | Architectures and Learning Objectives | PDF 204–262 | [Глава 4: изучена](chapters/CH04_RU.md) |
| 5 | Adapting LLMs to Your Use Case | PDF 264–328 | [Глава 5: изучена](chapters/CH05_RU.md) |
| 6 | Fine-Tuning | PDF 329–377 | [Глава 6: изучена](chapters/CH06_RU.md) |
| 7 | Advanced Fine-Tuning Techniques | PDF 378–413 | [Глава 7: изучена](chapters/CH07_RU.md) |
| 8 | Alignment Training and Reasoning | PDF 414–458 | [Глава 8: изучена](chapters/CH08_RU.md) |
| 9 | Inference Optimization | PDF 459–491 | [Глава 9: изучена](chapters/CH09_RU.md) |
| 10 | Interfacing LLMs with External Tools | PDF 493–552 | [Глава 10: изучена](chapters/CH10_RU.md) |
| 11 | Representation Learning and Embeddings | PDF 553–603 | [Глава 11: изучена](chapters/CH11_RU.md) |
| 12 | Retrieval-Augmented Generation | PDF 604–682 | [Глава 12: изучена](chapters/CH12_RU.md) |
| 13 | Design Patterns and System Architecture | PDF 683–765 | Ожидает изучения первоисточника |

## Начать изучение

**[Глава 1 — объяснение простыми словами, алгоритм, примеры и проверка](chapters/CH01_RU.md)**

**[Глава 3 — словарь и токенизация](chapters/CH03_RU.md)** · [BPE и аудит tokenizer](practicum/CH03_TOKENIZER_AUDIT_RU.md) · [Экзамен ALINA](learning/CH03_learning_package.json)

**[Глава 2 — учебное пособие по подготовке данных](chapters/CH02_RU.md)** · [Практика](practicum/CH02_DATA_PIPELINE_2026.md) · [Экзамен ALINA](learning/CH02_learning_package.json)

[Практическая работа «Chat with my PDF»: современная реализация](practicum/PRACTICE_CH01_2026.md)

[ALINA — учебные задания и эталоны](learning/CH01_learning_package.json)

[System Architect — образ принятия решений](architect/CH01_THINKING_MODEL_RU.md)

[Что будет дальше: программа по 13 главам](LEARNING_ROADMAP_RU.md)

## ALINA Academy — подготовка специализированных агентов

**[Программа обучения ALINA, OSINT и Document Intelligence](alina_kb/academy/README.md)** — 10 модулей, прикладные учебные кейсы и алгоритм «нужно ли импортировать дубликат».

[OSINT и агенты работы с документами](alina_kb/academy/AGENT_TRACKS_RU.md) · [Алгоритм решения по дубликатам](alina_kb/academy/DOCUMENT_DECISIONS_RU.md) · [Чек-лист](alina_kb/academy/CHECKLIST_RU.md)

## ALINA — база знаний по книге (единый граф)

**[Открыть ALINA Knowledge Core v0.1.0](alina_kb/README.md)** — 307 узлов, 570 связей, словарь, веса, алгоритмы, ролевые представления, правила версионирования.

- [Graph JSON](alina_kb/knowledge_graph.json) — узлы и связи
- [Glossary](alina_kb/glossary.json) — словарь терминов и сокращений
- [Algorithms](alina_kb/algorithms.json) — пошаговые процедуры
- [Role views](alina_kb/roles.json) — единый граф для разных агентов
- [Update rules](alina_kb/schema_policy.md) — обновление после каждой главы
- [Validator](alina_kb/validate_graph.py) — структурная проверка

**Статус:** составлено по главам 1–12 оригинала; глава 13 ещё не импортирована. База на GitHub пока машиночитаемая, но не развёрнута как сервер БД и не подключена к runtime ALINA.

## Качество обучения моделей: алгоритмы и чек-листы

В этом проекте ведётся отдельный инженерный трек, объединяющий вопросы данных, обучения и квалификации. **Глава 2 даёт фундамент данных; обучение весов, адаптация, RLHF и оптимизация изучаются по соответствующим последующим главам.**

- [Подробный алгоритм качественного обучения и 10 quality gates](training/QUALITY_TRAINING_ALGORITHM_RU.md)
- [Чек-листы данных, дедупликации, приватности, holdout, обучения и POLYGON](training/DATASET_QUALITY_CHECKLIST_RU.md)
- [Кейсы принятия решений: prompt, RAG, SFT, PEFT и RL](training/TRAINING_DECISION_CASES_RU.md)

Это пока методики и планы. Выполненные испытания будут отдельно подтверждаться evidence.

## Связь с FATHER

- **ALINA:** обучение, retrieval, управление первоисточниками, подготовка задач.
- **System Architect:** требования, схемы потоков данных, альтернативы архитектуры, ADR.
- **TIMA:** окружение, модели, контейнеры, sizing, эксплуатация.
- **UAG / Security:** доверенные границы, доступы, prompt injection.
- **POLYGON:** независимая проверка качества, безопасности, способности агента действовать.

## Границы проверенного

Главы 1–8 изучены непосредственно по предоставленному оригиналу (PDF 27–458). Главы 1–8 изучены по оригиналу; главы 10–13 ожидают подробного изучения. Мы не приписываем автору наши инженерные рекомендации 2026 года. Задания и практические примеры подготовлены; независимые испытания не выполнялись.

## Методика

[Общий стандарт обучения от первого курса МАИ](../../LEARNING_STANDARD_RU.md) · [Рекомендации по практике 2026](../../PRACTICE_2026_RU.md).

## Глава 4 — архитектура и обучение моделей

[Урок по оригиналу](chapters/CH04_RU.md) · [Практикум Attention и loss](practicum/CH04_TRANSFORMER_TRAINING_RU.md) · [Учебный код](alina_kb/labs/ch04_math.py) · [Упражнения ALINA](learning/CH04_learning_package.json)

Слой знаний ALINA v0.3.0: 92 узла, 184 связи, 11 алгоритмов. Прочитаны главы 1–4; главы 5–13 ещё предстоят.

## Глава 5 — выбор модели, декодирование и структурированные выходы

[Учебный разбор по оригиналу](chapters/CH05_RU.md) · [Практикум ALINA GPT Runtime](practicum/CH05_MODEL_SELECTION_RU.md) · [Демонстрационный код декодирования](alina_kb/labs/ch05_decode.py) · [Задания и эталоны](learning/CH05_learning_package.json)

Граф ALINA v0.4: 120 узлов, 234 связи, 21 алгоритм, по изученным главам 1–5. Реальные испытания моделей и POLYGON отдельно не проводились.

## Глава 6 — fine-tuning и производство проверенных обучающих примеров

[Разбор первоисточника](chapters/CH06_RU.md) · [Практикум Dataset Factory](practicum/CH06_FINETUNING_DATASET_LAB_RU.md) · [Учебные примеры с обозначенными статусами](learning/CH06_dataset_seed_examples.json) · [Вопросы для ALINA](learning/CH06_learning_package.json)

ALINA Knowledge Core v0.5.0: 145 узлов, 280 связей, 17 описанных алгоритмов, главы 1–6 изучены по оригиналу. Fine-tuning не выполнялся; примеры без самостоятельного evidence не квалифицированы.

## Глава 7 — advanced fine-tuning techniques

[Урок CH07 по первоисточнику](chapters/CH07_RU.md) · [Практикум ALINA: RAG, PEFT или continual pre-training](practicum/CH07_ADAPTATION_DECISION_RU.md) · [Задания ALINA](learning/CH07_learning_package.json)

Состояние Knowledge Core v0.6: 193 узла, 371 связь, 21 описанный алгоритм, главы CH01–CH07 изучены. Эксперименты с обучением моделей и независимая квалификация не выполнены.

## Глава 8 — Alignment Training and Reasoning

[Учебный разбор по первоисточнику](chapters/CH08_RU.md) · [Лаборатория A/B/C: достоверность, безопасность и рассуждения](labs/CH08/LAB_PROGRAM.md) · [Проверочные задания](learning/CH08_learning_package.json)

ALINA Knowledge Core v0.7.0: 193 узла, 371 связь, 41 описанный алгоритм. Источники глав 1–8 разобраны. Лаборатории главы 8 **DESIGNED_ONLY / NOT_RUN / NOT_QUALIFIED**; POLYGON не запускался.

## Глава 9 — Inference Optimization

[Разбор главы 9](chapters/CH09_RU.md) · [Лабораторная A/B/C](labs/CH09/LAB_PROGRAM.md) · [Учебный экзамен](learning/CH09_learning_package.json) · [POLYGON: основной независимый экзамен после обучения](alina_kb/qualification/POLYGON_POST_TRAINING_PROTOCOL_RU.md)

Граф ALINA v0.8.0 — 307 узлов, 570 связей, 41 описанный алгоритм. Главы 1–9 разобраны по первоисточнику. Для главы 9 **NOT_RUN / NOT_QUALIFIED**.

## Глава 10 — работа LLM с внешними инструментами

[Разбор главы 10](chapters/CH10_RU.md) · [Лаборатория A/B/C и POLYGON Tool Use](labs/CH10/LAB_PROGRAM.md) · [Обучающие вопросы](learning/CH10_learning_package.json)

ALINA Knowledge Core v0.9.0: 307 узлов, 570 связей, 41 описанный алгоритм, главы 1–10 изучены по оригиналу. Лаборатория Tool Use только спроектирована, NOT_RUN / NOT_QUALIFIED.

## Глава 11 — Representation Learning and Embeddings

[Конспект первоисточника](chapters/CH11_RU.md) · [Лаборатория A/B/C](labs/CH11/LAB_PROGRAM.md) · [Учебный пакет](learning/CH11_learning_package.json)

ALINA Knowledge Core v1.0.0: 307 узлов, 570 связей, 41 описанный алгоритм; прочитаны главы CH01–CH11. Испытания главы 11 НЕ выполнены, POLYGON NOT_QUALIFIED.

## Глава 12 — Retrieval-Augmented Generation

[Конспект по первоисточнику](chapters/CH12_RU.md) · [Лаборатория A/B/C и POLYGON](labs/CH12/LAB_PROGRAM.md) · [Учебный пакет](learning/CH12_learning_package.json)

ALINA Knowledge Core v1.1.0: 307 узлов, 570 связей, 41 описанный алгоритм, главы CH01–CH12 изучены непосредственно по оригиналу. Лаборатория RAG — DESIGNED_ONLY / NOT_RUN / NOT_QUALIFIED.
