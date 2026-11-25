# CH06 — Planning: практическая программа A/B/C

**Основа:** Antonio Gulli, *Agentic Design Patterns*, PDF 98–110.  
**Дата:** 2026-11-25.  
**Статус:** LAB_SPECIFIED / CODE_NOT_RUN / NOT_QUALIFIED.

## A. Обычный алгоритм — без LLM

**Задача:** безопасно обработать мини-процесс `source -> parse -> verify -> report`.
- Typed `Goal`, `Step`, `Plan`, `TraceEvent`; разрешённые действия только из mock registry.
- Валидатор: уникальные ID, известные зависимости, отсутствие циклов, выполнимые предусловия, максимум 8 шагов, бюджетная граница, запрет `delete`, `shell`, `network_write`.
- `executor`: запуск по допустимому топологическому порядку, явные статусы, зависимый этап не выполняется при ошибке предшествующего.
- Независимый `goal_checker` подтверждает результат конкретными полями данных/доказательств.
- Метрики: `valid_plan_rate`, `verified_goal_success`, `step_count`, `duration_ms`, `cost_per_accepted_result`.

**Негативные тесты:**
1. цикл `A -> B -> A`;
2. отсутствующая зависимость;
3. дублированные ID;
4. незарегистрированный инструмент;
5. превышение бюджета;
6. сбой шага и правильная блокировка потомка;
7. ложная маркировка завершения без evidence;
8. перезапуск после checkpoint без повторного опасного вызова.

## B. LLM Planner — существующий ModelAdapter

- `qwen3:8b`, `ministral-3:8b`; один и тот же GoalContract, одинаковые ограничения и набор инструментов.
- LLM генерирует **только проект плана JSON**, без исполнения; проверка формата/циклов/полномочий детерминированной программой.
- Максимум 2 пересмотра, лимит токенов и времени, логировать расходы, статус проверки и причины отказа.
- Сравнить с A на одинаковом наборе задач; получить вердикт `ADOPT / CONDITIONAL / REJECT`.

## C. FATHER Composition + POLYGON

```text
IDEA+ -> Feasibility + Cost Gate -> PlanningProposal
      -> Validation(DAG/UAG/Budget)
      -> CH05 ToolExecutor (allowlisted)
      -> Observations + CH04 Reflection
      -> CH08 Memory/checkpoint (scoped)
      -> Independent Evidence Checker -> POLYGON -> qualified result
```

Критерии: абсолютный запрет неразрешённых действий, bounded retries/replan, isolation `user/tenant/task`, корректные budget abort, валидность evidence, восстановление после сбоя. Сравнение экономики всей цепочки с простым workflow. Документы и код не равны `POLYGON_QUALIFIED`.

## D. Визуализация в Dashboard

Русская и английская карточки: интерактивный DAG, текущий шаг, журнал изменений плана, статусы и блокировки, сравнение затрат и успехов `fixed_workflow vs planner`. До появления реальных прогонов — явно показывать `NO_DATA`.

## Приёмка

Сохранить commit/hash исходного кода, версию Python, зависимости, LLM model/tag/digest, промпт и его SHA-256, тестовый набор с provenance, логи, source page, смету стоимости, итоговые статусы. Готовность доказывается в составе сквозной FATHER-линии.
