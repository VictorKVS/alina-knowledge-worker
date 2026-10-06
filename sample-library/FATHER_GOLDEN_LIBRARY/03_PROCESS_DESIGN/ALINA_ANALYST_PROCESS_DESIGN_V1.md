# Алина-аналитик — проектирование рабочих процессов

## Назначение

Алина должна хранить не только знания и выдержки, но и **исполняемые рабочие процессы**. Новый процесс проектируется по цепочке:

```text
ЦЕЛЬ
→ SCOPE / ОГРАНИЧЕНИЯ
→ ВХОДЫ
→ KNOWLEDGE ROUTE
→ РОЛИ / АГЕНТЫ
→ ШАГИ / ЗАВИСИМОСТИ
→ ACTION / TOOL
→ QUALITY GATE
→ EVIDENCE
→ FINDING / GAP / DECISION
→ OUTPUT PACKAGE
→ COMPLETENESS CHECK
→ REGISTRY
→ PILOT RUN
→ RETROSPECTIVE
```

## Главный принцип

Включение агента не означает «пусть сам что-нибудь сделает». Создаётся **WORK RUN** по зарегистрированному процессу. Агент получает следующий разрешённый шаг, выполняет его, сохраняет результат и evidence, переводит шаг в terminal state и только после этого получает следующий.

Обязательные terminal states:

- `DONE`
- `BLOCKED` — с причиной и недостающим входом;
- `NOT_APPLICABLE` — с обоснованием;
- `REVIEW_REQUIRED` — требуется человек/другой агент.

Процесс завершён только когда все обязательные шаги имеют terminal state.

## Модель данных

```text
PROCESS_DEFINITION
  → PROCESS_STEP
      → KNOWLEDGE_REF
      → TOOL
      → QUALITY_GATE
      → EVIDENCE_CONTRACT

WORK_ORDER
  → WORK_RUN
      → WORK_STEP_RUN
          → RESULT
          → EVIDENCE
          → FINDING
          → GAP
          → DECISION
      → OUTPUT_PACKAGE
```

## Роль Алины-аналитика

Алина:

1. принимает цель;
2. определяет scope;
3. перечисляет входные данные;
4. ищет необходимые знания;
5. выбирает роли/агентов;
6. строит граф этапов;
7. задаёт действия и инструменты;
8. задаёт проверки;
9. задаёт evidence;
10. проектирует ошибки, retry и escalation;
11. задаёт findings/gaps/decisions;
12. определяет итоговые артефакты;
13. проверяет полноту;
14. регистрирует процесс;
15. выполняет пилотный прогон;
16. записывает lessons learned.

## Запрет на ложную завершённость

Наличие текста, найденного документа или ответа LLM не означает выполнение шага. Выполнение подтверждается только контрактом шага и его evidence.

## Связь с FATHER

```text
FATHER KNOWLEDGE
    ↓
ALINA KNOWLEDGE ROUTER
    ↓
PROCESS DESIGN
    ↓
PROCESS REGISTRY
    ↓
AGENT RUN
    ↓
EVIDENCE / FINDINGS / OUTPUT
    ↓
LEARNING / PROCESS UPDATE
```
