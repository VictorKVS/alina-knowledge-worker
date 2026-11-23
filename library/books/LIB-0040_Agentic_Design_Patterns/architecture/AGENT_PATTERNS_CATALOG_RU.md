# Agent Pattern Catalog — маршрутизация и параллелизация

Это **наша инженерная адаптация** паттернов из книги Antonio Gulli (публичного текста книги в репозитории нет).

| Паттерн | Книга/PDF | Компоненты | Вход → выход | Простое → промышленное |
|---|---|---|---|---|
| PAT-002 Routing / Delegation | CH02, 34–47 | Intent Classifier, Validator, Branch, Handler | `request` → `route → result` | if/else → LCEL → qualified FATHER worker |
| PAT-003 Parallelization | CH03, 48–63 | Fan-out, Independent Tasks, Join, Synthesis | `topic` → `{summary, questions, key_terms}` → answer | asyncio → RunnableParallel → distributed aggregator |

## Инварианты

- Решение модели не является разрешением на выполнение инструментов.
- Параллельны лишь независимые задачи; синтез зависит от всех обязательных ветвей.
- Изолировать `user/tenant/task/branch` в каждом обмене.
- Указать ошибку конкретного этапа; не объявлять фрагмент результата полноценным ответом.
- Сохранить source page, version, tests, evidence и POLYGON qualification — отдельно от кода.

**Статус:** SOURCE_REVIEWED / DESIGN_CREATED / EXAMPLES_NOT_EXECUTED.
