# BOOK-002 / Глава 10 — Interfacing LLMs with External Tools

**Первоисточник:** Suhas Pai, *Designing Large Language Model Applications*, предоставленный пользователем оригинальный PDF, 493–552 из 765. Самостоятельный русскоязычный учебный материал, не перевод главы.

**Статус:** SOURCE_REVIEWED / LAB_PROGRAM_DESIGNED / NOT_RUN / NOT_QUALIFIED.

## 1. Карта первоисточника

| PDF | Раздел |
|---|---|
| 493–496 | Мотивы подключения инструментов, способы решения задач |
| 496–498 | Passive approach / retrieval |
| 499–500 | Explicit approach: фиксированная последовательность |
| 501–508 | Autonomous agents, риск, декомпозиция и примеры |
| 508–511 | Шесть компонентов agentic system |
| 511–520 | Web, API, Python, SQL и структурные вызовы tools |
| 523–530 | Prompt repository, session memory, tool docs store |
| 530–533 | Agent loop prompt, ReAct, reflection |
| 533–539 | Guardrails, PII, prompt injection, fallback |
| 540–548 | Verifiers: factuality, completeness, relevance, NLI |
| 549–552 | Orchestration, computer use и KISS |

## 2. Три парадигмы автора

**Passive:** retrieval engine сам подбирает контекст; LLM только формирует ответ. Это основной режим для простого вопроса по документации и защищённого RAG.

**Explicit:** заранее зафиксированный workflow управляет очередностью действий: SQL → вычисление → отчёт. Автор рекомендует его для более надёжных приложений с ограниченными типовыми задачами.

**Autonomous:** модель сама декомпозирует запрос, выбирает инструменты и определяет следующий шаг. Автор предостерегает от чрезмерного доверия автономным агентам для mission-critical задач и указывает риски циклов, ошибочных действий и непредсказуемых отказов.

**Принцип для FATHER (наше инженерное решение):** Explicit-by-default. Полномочия выдаёт UAG, независимая квалификация — POLYGON.

## 3. Определение агента

В книге агент — LLM-driven software, способное автономно взаимодействовать со средой и выполнять действия. Не всякая цепочка prompt является агентом. Возможна частичная автономность и строгая оркестрация.

## 4. Архитектура: шесть компонентов

1. Models: одна или несколько LLM и специализированных моделей.
2. Tools: web, API, code interpreter, SQL.
3. Data stores: источники знаний, репозиторий промптов, журнал сессий, схемы инструментов.
4. Agent loop prompt: итерация выбора действия/получения результата/завершения.
5. Guardrails & verifiers: безопасность и функциональная проверка.
6. Orchestration software: реальное исполнение, state, маршруты, логирование, восстановление.

ReAct и Reflexion — возможные схемы loops, не универсально лучшие; книга подчёркивает хрупкость некоторых ReAct-настроек. Выполнение кода, сгенерированного LLM, рискованно без песочницы.

## 5. Tool interface and trust boundaries

Программный пример для FATHER (наша адаптация):
```json
{
  "tool": "document.search",
  "arguments": {"query": "модель угроз", "max_results": 5},
  "requested_scope": "corpus-public",
  "trace_id": "T-0001"
}
```

Модель составляет запрос, но НЕ исполняет его непосредственно. Строгую схему и разрешения проверяет UAG, исполнитель работает по allowlist, возвращает минимально необходимые данные и audit record. Источники и результаты инструментов **недоверенные данные**, не инструкции для оркестратора.

## 6. Session memory, tool docs and prompt repository

Хранилище сессии содержит прошлые действия, ошибки и замечания проверяющего. Tool documentation store предоставляет схемы API и SQL. Prompt repository хранит примеры успешного поведения. Эти три хранилища **не равны** общей базе фактов ALINA: разные назначения, срок жизни и политика доступа.

## 7. Guardrails и внешние проверки

Автор перечисляет валидаторы PII, prompt injection, unsafe output, web sanitization и поведение при failure: повторить, исправить, отфильтровать, отказаться, журналировать, выбросить исключение. Это не гарантия 100% защиты.

Для проверки абстрактивной сводки отдельно проверяются factuality, specificity, relevance, completeness, repetition, coherence, structure, formatting, ordering, error handling. NLI позволяет поставить вопрос: «следует ли данное утверждение из источника?». Числа и сущности можно дополнительно сверить детерминированными правилами.

## 8. Практика для FATHER

`ALINA Knowledge + Agent Blueprint → explicit orchestrator → tool-call proposal → UAG allow/deny → sandboxed execution → external verification → output/evidence → POLYGON closed qualification`.

Пока идёт изучение книг, это **программа**, а не развёрнутая интеграция.

## 9. Учебные вопросы

1. Чем passive отличается от explicit и autonomous?
2. Почему автор не рекомендует полную автономию в критических задачах?
3. Кто действительно исполняет вызов tools: LLM или оркестратор?
4. Зачем нужны tool documentation и session memory?
5. Почему вызов PythonREPL без изоляции опасен?
6. Чем guardrail отличается от verifier?
7. Почему ReAct-петлю необходимо ограничивать?
8. Как POLYGON проверит компетенцию Tool Use без выдачи закрытого экзамена ALINA?

[Лаборатория A/B/C](../labs/CH10/LAB_PROGRAM.md)
