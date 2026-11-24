# DUAL AGENT DECISION LAB — Story Agent vs Game Agent

**Учебный прототип FATHER**, прикреплённый к LIB-0040 CH05. Две агентные задачи развиваются **одновременно на общем контракте действий**, но используют разные модели мира, критерии качества, опасности и инструментальный арсенал.

**Состояние:** DESIGN + CODE_CREATED; офлайновые/LLM-тесты запускаются отдельно; `NOT_QUALIFIED`. Это не доказанная реализация конкретной вакансии, поскольку её реальные требования неизвестны.

## Сравнение

| | Narrative Agent | Game Agent |
|---|---|---|
| Цель | логически связный эпизод с завязкой, уликой и раскрытием | достичь цели, сохранить здоровье, соблюсти ограничение ходов |
| Состояние | известные события/факты/причинные связи | position, hp, visibility/scout, budget |
| Действия | establish, clue, reveal, brief_end | scout, move, rush |
| Предусловия | событие reveal не происходит без clue | нельзя двигаться после конца игры/без бюджета |
| Риск | сюжетная непоследовательность и невнятный конец | гибель, потеря HP, расход времени |
| Проверка | causal/continuity constraints (позже - scene evidence) | deterministic world transition, reach-goal, survival |
| «Обучение» | feedback и библиотека сценарных паттернов | policy evaluation, logs, позже RL/curriculum |
| Инструменты | story KB, character graph, scene validator | observe state, legal actions, simulator step, reward |

## Единая производственная линия

```text
Task + constraints + strategy
          ↓
  Domain Env.observe()
          ↓
  Env.available() + preconditions
          ↓
  Decision Policy (rules or LLM via ModelAdapter)
          ↓
  Independent legality/safety check
          ↓
  Env.step(allowed_action)
          ↓
  Observation + trace
          ↓
  Success? Deadline? Replan?
```

Важно: модель не выбирает между абстрактными «кругом и треугольником». Она получает цель, назначение действий, ожидаемый эффект, ограничения времени/риска, историю и **предусловия**, затем предлагает решение. Конкретный переход мира принадлежит **симулятору Python**. Самоописание модели не подтверждает успеха.

## Быстрый старт — без LLM

```powershell
Set-Location 'G:\1\alina-knowledge-worker\library\books\LIB-0040_Agentic_Design_Patterns'
python .\projects\DUAL_AGENT_DECISION_LAB\dual_agents.py
python -m unittest discover -s .\projects\DUAL_AGENT_DECISION_LAB -p 'test_*.py' -v
```

**Ожидается:** два JSON-отчёта, traces выбора и результат каждого мира. Демо намеренно маленькое. Испытания необходимо реально провести.

## Подключение Ollama (уже используемый ModelAdapter)

```powershell
$env:AGENT_DECISION_MODE='llm'
$env:AGENT_LLM_PROVIDER='ollama'
$env:AGENT_LLM_MODEL='ministral-3:8b'
$env:AGENT_STRATEGY='careful'
python .\projects\DUAL_AGENT_DECISION_LAB\dual_agents.py
```

Два LLM-агента могут конкурировать за ресурсы одной GPU; Python ThreadPool означает конкурентные вызовы, не гарантирует ускорения GPU. Ограничить время и число шагов; не передавать чужую приватную информацию в промпты.

## Изменяем стратегию

```powershell
$env:AGENT_DECISION_MODE='rule'
$env:AGENT_STRATEGY='fast'
python .\projects\DUAL_AGENT_DECISION_LAB\dual_agents.py
$env:AGENT_STRATEGY='careful'
python .\projects\DUAL_AGENT_DECISION_LAB\dual_agents.py
```

Сравнить `chosen.reason`, `risk`, количество шагов, успех и remaining budget. **Правила исходного симулятора иллюстративные** — их веса не выучены по данным и не являются оптимальными.

## Следующие инженерные уровни

A. Доказать работу обоих игрушечных миров + формальные предусловия и отрицательные тесты.

B. Подключить настоящие инструменты: Story — чтение страниц, граф персонажей/событий, source citations; Game — `reset/step/observe` API, множество допустимых действий, reward, replay. Отдельно проверять, правильно ли работает model tool-calling, а не только JSON decision.

C. Эксперимент с обучением: CurriculumGenerator → симуляция → Feedback → обновление внешних skill cards и ranking policy → строгий regression. **Не смешивать это с fine-tuning весов модели**.

D. Масштаб: параллельные эпизоды с сохранением event log, tenant isolation, UAG, POLYGON holdout и бенчмарком ошибок/latency/cost. Не делать queue/Redis/K8s обязательными для первого этапа.

## Первичные источники

- Antonio Gulli *Agentic Design Patterns* CH02–05, CH08 — пользовательский PDF в частной библиотеке (не републиковать).
- [Generative Agents: Interactive Simulacra of Human Behavior](https://research.google/pubs/generative-agents-interactive-simulacra-of-human-behavior/), Park et al., UIST 2023 — персонажи: memory, reflection, planning.
- [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://voyager.minedojo.org/), 2023 — игровой curriculum, skill library, feedback.
- [Gymnasium Env API](https://gymnasium.farama.org/api/env/) — reset/step, terminated/truncated.
- [PettingZoo](https://pettingzoo.farama.org/) — последующий уровень многоагентной игровой среды.

## Авторское право и evidence

В репозитории размещены только собственные учебные тексты и код, а не главы книги. Для каждого расширения оформить ADR, контракт данных, тесты, trace, SHA-256/provenance и испытание в составе конечного изделия до статуса READY.
