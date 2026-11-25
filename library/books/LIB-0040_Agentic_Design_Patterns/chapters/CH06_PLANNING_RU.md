# CH06 — Planning / Планирование агента — инженерный разбор FATHER

**Книга:** Antonio Gulli, *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems*.  
**Оригинал:** пользовательский PDF, **физические страницы файла 98–110 из 458**; внутри главы напечатаны страницы 1–13.  
**Reviewed on:** 2026-11-25.  
**Статус:** SOURCE_REVIEWED / ENGINEERING_DERIVATION / EXTERNAL_ANALOGUES_SCOUTED / IMPLEMENTATION_NOT_STARTED / NOT_QUALIFIED.

## 1. Суть паттерна, строго по книге

Planning — переход из исходного состояния к целевому через последовательность спроектированных действий. Агент получает **цель и ограничения**, но способ достижения может быть неизвестен. План должен обновляться по мере поступления новой информации. **Особенно важно (PDF 98):** автор противопоставляет динамическое планирование **предопределённому workflow**. Если решение известно и повторяется, фиксированный процесс надёжнее и предсказуемее. Решающий вопрос автора: *должен ли способ выполнения быть открыт во время работы или он уже известен?*

### Карта фрагментов оригинала
| Физические страницы PDF | Что в книге |
|---|---|
| 98 | Что такое planning; исходное/целевое состояние; адаптация, trade-off гибкость/предсказуемость |
| 99 | Автоматизация процессов, навигация, исследования, поддержка; пример CrewAI |
| 100–101 | CrewAI: один Agent/Task, план + краткое резюме по заданной теме |
| 101–105 | Google Gemini Deep Research: многошаговый поиск, пересмотр плана, синтез и источники |
| 105–108 | OpenAI Deep Research API: пример кода, веб-поиск, citations и steps (описание на момент написания книги) |
| 108–110 | At a Glance, rule of thumb, Fig.4, выводы и ссылки |

### Что *показывает*, а чего *не доказывает* пример CrewAI
На PDF 100–101 задаётся один агент `Article Planner and Writer`, задача: сначала составить буллет-план по RL, затем написать около 200 слов. `Process.sequential` используется при **одной** задаче. Это **учебный пример планирования перед текстом**, а не доказательство промышленного динамического DAG-планирования, восстановлений, исполнения произвольных инструментов или измеренного превосходства над baseline.

### Deep Research как более развитый пример
PDF 101–108 описывает iterative research: исходный план → поиск источников → обнаружение информационных пробелов → дополнительные запросы → синтез и цитирование. В книге также показан исторический API-пример OpenAI. Имена моделей и параметры этого кода — **исторические сведения из оригинала, не гарантированно актуальные сегодня**. Источник, факт и модельную интерпретацию разделять.

## 2. FATHER IDEA+ перед подключением Planner

**Требование:** сделать исполнение сложной идеи более успешным, но не ухудшить надёжность и экономику.

Вопросы допуска:
1. Можно ли выполнить задачу детерминированным кодом или фиксированным workflow?
2. Есть ли неизвестные зависимости, альтернативные пути, непредсказуемые внешние условия?
3. Какие существующие блоки FATHER уже покрывают задачу?
4. Какая система фактически *исполняет* план; кто определяет права, бюджеты, внешние действия?
5. Насколько planning улучшает итоговую долю квалифицированных результатов при одинаковом наборе задач?
6. Не стоит ли планировщик дороже, чем выигрыш от него?

**Правило:** `Plan ≠ Permission ≠ Execution ≠ Verification`.

## 3. Декомпозиция универсального Planning Engine

```text
IDEA+ / FEASIBILITY + COST GATE
        |
        v
GoalContract + InitialState + AllowedCapabilities
        |
        v
Planner (deterministic template OR LLM proposal)
        |
        v
Schema Gate -> Dependency DAG Gate -> Policy/UAG Gate -> Budget Gate
        |          |                   |                  |
        +---- REJECT / REPLAN / HUMAN_REVIEW <-------------+
        |
        v
Execution Controller -> Tool Use CH05 -> Observation / Trace
        |                                       |
        +---------- Verify step evidence <------+
        |
        v
Goal Checker: criteria satisfied? 
     YES -> VERIFIED_RESULT
     NO  -> bounded replan / WAIT / STOP
        |
        v
Memory CH08: session event and validated provenance; POLYGON qualification separately
```

**Наша инженерная надстройка:** строгие схемы, DAG-валидация, UAG, лимиты бюджетов и шагов, evidence и POLYGON. Это не утверждение о том, что они реализованы в примерах книги.

### Контракты
- `GoalContract`: `goal_id, objective, constraints, acceptance_criteria, required_evidence, max_cost`.
- `Plan`: `plan_id, goal_id, revision, steps, assumptions, estimated_cost, evidence_sources`.
- `PlanStep`: `step_id, action, capability, dependencies, preconditions, postconditions, timeout_s, max_attempts, estimated_cost, evidence_required`.
- `Observation`: `step_id, result, error, evidence_refs, actual_cost, ts`.
- `PlanDecision`: `APPROVED | REVISE | REJECT | REVIEW_REQUIRED`.
- `ExecutionStatus`: `PENDING | READY | RUNNING | FAILED | BLOCKED | VERIFIED`.

**Валидация:** уникальность step_id; ссылки только на существующие steps; запрет циклов, запрещённых capabilities, неограниченных шагов, завышенного бюджета; `VERIFIED` лишь после внешнего evidence checker.

## 4. WORLD_SCOUT — проверяемые аналоги

Проверено 2026-11-25; ссылки — **прямые источники**, а не свидетельства успешного воспроизведения у нас.

| Проект | Архитектурная идея | Полезность для FATHER | Открытая проблема |
|---|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) / [persistence docs](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx) | State graph + checkpoints; восстановление | Adapt orchestration/state ports, не копировать логику | Цена и сложность интеграции; требуется измерение |
| [CrewAI](https://github.com/crewAIInc/crewAI) / [quickstarts](https://github.com/crewAIInc/crewAI-quickstarts) | Tasks, crews, flows и planning | Сопоставление с примером автора; быстрый PoC | Нельзя выводить качество из наличия planning-функции |
| [AutoGen](https://github.com/microsoft/autogen) / [Magentic-One orchestrator](https://github.com/microsoft/autogen/blob/main/python/packages/autogen-agentchat/src/autogen_agentchat/teams/_group_chat/_magentic_one/_magentic_one_orchestrator.py) | Оркестрация специализированных агентов; task ledger/replanning | Идеи ledger, наблюдений и replanning | Сложность, эксплуатационные риски, версии |
| [LangGraph official reference](https://reference.langchain.com/python/langgraph/overview) | SQLite/Postgres checkpoint adapters | Подключить к существующему хранению при необходимости | Поддержка конкретного набора зависимостей |

**Предварительный выбор:** для первой лаборатории использовать **Python stdlib baseline** и существующий ModelAdapter. Не устанавливать ни один новый тяжёлый фреймворк до сравнительного эксперимента.

## 5. INTERNAL_SCOUT — наши существующие компоненты

| Актив | Фактическое состояние | Повторное применение |
|---|---|---|
| `examples/model_adapter.py` | Универсальный адаптер моделей CH02/CH03/CH04/CH05 | REUSE/ADAPT для предложения планов |
| `examples/ch05_tool_use.py` | Safe tool calling, лимиты, trace; есть демо на Ollama | ADAPT как executor mock tools |
| `examples/ch04_reflection.py` | Generator–Critic, offline тесты | ADAPT для критики плана, не считать доказательством |
| `architecture/MEMORY_BLOCK_CONTRACT_RU.md` | Контракт CH08, runtime ещё не квалифицирован | RESEARCH для сохранения и восстановления |
| FATHER IDEA+ protocol | Документ в отдельном FATHER_CODEX GitHub | INPUT: gate; пока ручная проверка |
| FATHER Cost Engineering | Документ в отдельном FATHER_CODEX GitHub | INPUT: бюджет и измерение; автоматического metering пока нет |

## 6. ЭКОНОМИКА: baseline против planner

Обязательный протокол сравнения одинаковых заданий:
- `fixed_workflow` — количество LLM вызовов 0 для планирования, потом фактическое выполнение;
- `llm_planner` — генерация плана, критика, повторное планирование и выполнение;
- учесть input/output/cached tokens, вызовы инструментов, storage, retries, верификацию и время человека;
- outcome denominator: **количество независимо принятых конечных результатов**;
- `cost_per_qualified_result = total_attempt_cost / accepted_results`, не делить на число запланированных шагов.

**Нет измерений:** никакого утверждения «planner выгоднее/качественнее» до эксперимента.

## 7. Лаборатория A/B/C и критерии остановки

**A. Детерминированный baseline:** создать typed Plan, DAG validator, minimal mock execution; тесты на циклы, missing deps, duplicate IDs, capability deny, budget exceeded, dependent failure.

**B. Ollama:** `qwen3:8b` и `ministral-3:8b` через ModelAdapter возвращают JSON Plan; программа валидирует, но не выполняет неизвестные вызовы. Измерить schema validity, plan correctness, tokens/latency, revisions.

**C. Composition:** IDEA+ → Planner → CH05 Tool Use → CH04 Critic → Evidence Checker → CH08 Memory → POLYGON; реализовать трассировку, bounded replan и эксперимент на безопасных данных.

**STOP:** `max_steps`, `max_replans`, `max_attempts`, `max_cost`, `deadline`, human approval. Никакой бесконечной рекурсии или автономных изменений production-среды.

## 8. FATHER Dashboard — CH06 page requirements

Сайт: `FATHER_CODEX/docs/index.html` — будущая отдельная карточка CH06. В русской/английской версиях показывать:
1. «Кому нужен planner?» — интерактивное решение *workflow vs planning*.
2. DAG с зависимостями задач и условиями допуска.
3. Trace: план, события, пересмотры, бюджет, фактические evidence.
4. Сравнение fixed workflow и planning по verified success, latency, tokens, dollars.
5. Ссылки на оригинал (без публикации защищённого PDF), аналоги GitHub, код, тесты, POLYGON qualification.

## 9. Ключевые выводы

1. Planning — не обязательный слой каждого агента.
2. Динамическое перепланирование нужно только если `how` заранее неизвестно или меняется.
3. В книге описаны простой текстовый учебный пример и сложные исследовательские системы; не приравнивать их уровни.
4. План — предложение, инструмент — отдельно авторизованная возможность, задача выполнена — только с подтверждением.
5. Решение о внедрении в FATHER принимает сравнительный эксперимент по стоимости **квалифицированного результата**.
