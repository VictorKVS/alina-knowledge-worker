# Agent Pattern Catalog — инженерные паттерны AI-агентов

Это **наша инженерная адаптация** паттернов из книги Antonio Gulli (публичного текста книги в репозитории нет).

| Паттерн | Книга/PDF | Компоненты | Вход → выход | Простое → промышленное |
|---|---|---|---|---|
| PAT-002 Routing / Delegation | CH02, 34–47 | Intent Classifier, Validator, Branch, Handler | `request` → `route → result` | if/else → LCEL → qualified FATHER worker |
| PAT-003 Parallelization | CH03, 48–63 | Fan-out, Independent Tasks, Join, Synthesis | `topic` → `{summary, questions, key_terms}` → answer | asyncio → RunnableParallel → distributed aggregator |
| PAT-004 Reflection / Generator–Critic | CH04, 63–76 | Producer, Critic, Iteration Controller, External Validator | `task` → `candidate → critique → revise` | self-review → provider-adapter loop → evidence-based FATHER acceptance |
| PAT-005 Tool Use / Function Calling | CH05, 77+ | Tool Registry, Schema Gate, LLM, Executor, Observation, UAG | `request` → `tool_calls[]` → `ToolMessage` → answer | 1 function → bind_tools loop → permissioned service |

## Инварианты

- Решение модели не является разрешением на выполнение инструментов.
- Параллельны лишь независимые задачи; синтез зависит от всех обязательных ветвей.
- Изолировать `user/tenant/task/branch` в каждом обмене.
- Указать ошибку конкретного этапа; не объявлять фрагмент результата полноценным ответом.
- Сохранить source page, version, tests, evidence и POLYGON qualification — отдельно от кода.

**Статус:** SOURCE_REVIEWED / DESIGN_CREATED / EXAMPLES_NOT_EXECUTED.
