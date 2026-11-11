# Narrative Prediction Pool — ALINA BOOK 2

Это доменный Prediction Pack для художественных произведений. Он не заменяет общую математику Future Lab, а добавляет структурные модели повествования.

## Входное состояние

```text
CHARACTERS
EVENTS
RELATIONS
GOALS
MOTIVES
LOCATIONS
TIMELINE
PLOT THREADS
OPEN QUESTIONS
CONFLICTS
FORESHADOWING
GENRE
```

## Семейства методов

### NP-01 — Story Structure
Проверяет положение текущего состояния относительно известных структур повествования: Hero's Journey, актовые структуры и другие формализованные схемы.

### NP-02 — Character Goal / Need
Прогнозирует действие из:
```text
NEED → GOAL → OBSTACLE → CHOICE → CONSEQUENCE
```

### NP-03 — Unresolved Plot Threads
Ранжирует незавершённые сюжетные линии по вероятности ближайшего развития.

### NP-04 — Cause–Effect Graph
Использует граф причин и последствий:
```text
EVENT → STATE CHANGE → NEW CONSTRAINT → NEXT ACTION
```

### NP-05 — Relationship Dynamics
Прогнозирует переходы отношений:
```text
trust / distrust / alliance / conflict / dependence / betrayal
```

### NP-06 — Genre Prior
Использует жанр как prior, но никогда как доказательство конкретного события.

### NP-07 — Markov / State Transition
Строит эмпирические переходы между типами narrative states при наличии корпуса.

### NP-08 — Bayesian Hypothesis Update
Обновляет вероятности конкурирующих гипотез по мере появления новых сцен.

### NP-09 — LLM Abductive Reasoning
LLM предлагает объяснения и возможные продолжения; результат всегда имеет класс `hypothesis`, пока не подтверждён данными.

### NP-10 — Ensemble
Объединяет несколько независимых методов и сохраняет вклад каждого.

## Источники для теоретических схем

Каждая конкретная схема должна получить собственный паспорт и первоисточник/академический reference перед статусом RUNNABLE. Изображения и интернет-шпаргалки могут использоваться как визуальное сырьё для проектирования интерфейса, но не как доказательная база метода.

## Backtesting ALINA BOOK 2

```text
chapters 1..N
→ forecast N+1
→ reveal actual N+1
→ compare
→ error analysis
→ update method score
```

Метрики:

- EVENT HIT
- CHARACTER HIT
- RELATIONSHIP HIT
- PLOT HIT
- LOCATION HIT
- MOTIVE HIT
- SURPRISE MISS

Дополнительно должны появиться calibration и ranking metrics для вероятностных прогнозов.
