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
| 7 | Advanced Fine-Tuning Techniques | PDF 378–413 | Ожидает изучения первоисточника |
| 8 | Alignment Training and Reasoning | PDF 414–458 | Ожидает изучения первоисточника |
| 9 | Inference Optimization | PDF 459–491 | Ожидает изучения первоисточника |
| 10 | Interfacing LLMs with External Tools | PDF 493–552 | Ожидает изучения первоисточника |
| 11 | Representation Learning and Embeddings | PDF 553–603 | Ожидает изучения первоисточника |
| 12 | Retrieval-Augmented Generation | PDF 604–682 | Ожидает изучения первоисточника |
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

**[Открыть ALINA Knowledge Core v0.1.0](alina_kb/README.md)** — 145 узлов, 280 связей, словарь, веса, алгоритмы, ролевые представления, правила версионирования.

- [Graph JSON](alina_kb/knowledge_graph.json) — узлы и связи
- [Glossary](alina_kb/glossary.json) — словарь терминов и сокращений
- [Algorithms](alina_kb/algorithms.json) — пошаговые процедуры
- [Role views](alina_kb/roles.json) — единый граф для разных агентов
- [Update rules](alina_kb/schema_policy.md) — обновление после каждой главы
- [Validator](alina_kb/validate_graph.py) — структурная проверка

**Статус:** составлено по главам 1–6 оригинала; главы 7–13 ещё не импортированы. База на GitHub пока машиночитаемая, но не развёрнута как сервер БД и не подключена к runtime ALINA.

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

Главы 1–3 изучены непосредственно по предоставленному оригиналу (PDF 27–203). Главы 4–13 ожидают подробного изучения. Мы не приписываем автору наши инженерные рекомендации 2026 года. Задания и практические примеры подготовлены; независимые испытания не выполнялись.

## Методика

[Общий стандарт обучения от первого курса МАИ](../../LEARNING_STANDARD_RU.md) · [Рекомендации по практике 2026](../../PRACTICE_2026_RU.md).

## Глава 4 — архитектура и обучение моделей

[Урок по оригиналу](chapters/CH04_RU.md) · [Практикум Attention и loss](practicum/CH04_TRANSFORMER_TRAINING_RU.md) · [Учебный код](alina_kb/labs/ch04_math.py) · [Упражнения ALINA](learning/CH04_learning_package.json)

Слой знаний ALINA v0.3.0: 92 узла, 184 связи, 11 алгоритмов. Прочитаны главы 1–4; главы 5–13 ещё предстоят.

## Глава 5 — выбор модели, декодирование и структурированные выходы

[Учебный разбор по оригиналу](chapters/CH05_RU.md) · [Практикум ALINA GPT Runtime](practicum/CH05_MODEL_SELECTION_RU.md) · [Демонстрационный код декодирования](alina_kb/labs/ch05_decode.py) · [Задания и эталоны](learning/CH05_learning_package.json)

Граф ALINA v0.4: 120 узлов, 234 связи, 17 алгоритмов, по изученным главам 1–5. Реальные испытания моделей и POLYGON отдельно не проводились.

## Глава 6 — fine-tuning и производство проверенных обучающих примеров

[Разбор первоисточника](chapters/CH06_RU.md) · [Практикум Dataset Factory](practicum/CH06_FINETUNING_DATASET_LAB_RU.md) · [Учебные примеры с обозначенными статусами](learning/CH06_dataset_seed_examples.json) · [Вопросы для ALINA](learning/CH06_learning_package.json)

ALINA Knowledge Core v0.5.0: 145 узлов, 280 связей, 17 описанных алгоритмов, главы 1–6 изучены по оригиналу. Fine-tuning не выполнялся; примеры без самостоятельного evidence не квалифицированы.
