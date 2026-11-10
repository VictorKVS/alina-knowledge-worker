# Future Lab — MASTER INDEX v1

Статус: инвентаризация того, что уже создано в AU-01 / Future Lab.

## 1. Ядро

| Компонент | Статус | Файл |
|---|---|---|
| Prediction Method Pool PMP-01 | CREATED | `method-registry.v1.json` |
| Method Passport | CREATED | `METHOD_PASSPORT.md` |
| Python baseline methods | RUNNABLE | `methods.py` |
| Local server | RUNNABLE | `server.py` |
| Windows launcher | RUNNABLE | `start_future_lab.ps1` |
| Web UI | MVP | `site/` |

## 2. Реально реализованные математические методы

| ID | Метод | Семейство | Код | Статус |
|---|---|---|---|---|
| TS-NAIVE-01 | Naive forecast | Time Series / Baseline | yes | RUNNABLE |
| TS-MEAN-01 | Historical Mean | Statistics / Baseline | yes | RUNNABLE |
| TS-DRIFT-01 | Drift | Time Series / Trend | yes | RUNNABLE |
| TS-SES-01 | Simple Exponential Smoothing | Time Series | yes | RUNNABLE |

Реализованные метрики:
- MAE
- RMSE

Дополнительно зафиксированы из учебного источника:
- TS-ABS-GROWTH-01 — средний абсолютный прирост [DISCOVERED];
- TS-GROWTH-RATE-01 — средний темп роста [DISCOVERED];
- TS-TREND-LINE-01 — прогноз по линии тренда [DISCOVERED];
- TS-INTERVAL-01 — интервальная оценка прогноза [DISCOVERED].

Источник intake: `future_lab/time_series/SOURCE_INTAKE_002_SIMPLE_EXTRAPOLATION.md`.

## 3. Уже заведённые, но ещё не реализованные научные направления

| ID / группа | Направление | Статус |
|---|---|---|
| NAV-KALMAN-01 | Kalman / state estimation | PLANNED |
| PROB-BAYES-01 | Bayesian probabilistic models | PLANNED |
| ENS-01 | Ensemble forecasting | PLANNED |
| ETS / ARIMA / SARIMA | Advanced time series | PLANNED |
| Markov / HMM | State-transition prediction | PLANNED |
| Monte Carlo | Simulation | PLANNED |
| Survival / Hazard | Time-to-event | PLANNED |
| Causal models | Causal / counterfactual prediction | PLANNED |

## 3A. Graph & Network Methods

Статус: **DESIGNED / DISCOVERED**.

Зафиксированы:
- Shortest Path;
- Minimum Spanning Tree;
- Maximum Flow / Minimum Cut;
- Travelling Salesman Problem;
- Critical Path Method (CPM);
- PERT;
- GERT.

Назначение:
- оптимизация маршрутов и порядка действий;
- вычисление bottleneck/throughput;
- сетевое планирование FATHER Factory;
- критический путь и временные резервы;
- вероятностные workflow агентов;
- графы зависимостей, знаний и причинности.

Пакет: `future_lab/graph_network/`.

## 4. Narrative Prediction Pool

Статус: **DESIGNED / NOT YET QUALIFIED**.

Есть каталог направлений:
- Story Structure
- Character Goal / Need
- Unresolved Plot Threads
- Cause–Effect Graph
- Relationship Dynamics
- Genre Prior
- Markov / State Transition
- Bayesian Hypothesis Update
- LLM Abductive Reasoning
- Ensemble

Назначение: квалификационный прогнозный контур **ALINA BOOK 2**.

## 5. Political / Strategic Forecasting

Статус: **SOURCE INTAKE CREATED**.

Уже извлечены как отдельные методологические направления:
- Delphi
- Scenario Planning
- Strategic Foresight
- Trend Extrapolation

Следующие связанные методы, уже определённые архитектурно:
- Horizon Scanning
- Megatrends
- Backcasting
- Evaluation of scenarios / foresight

Важно:
- point forecast;
- scenario;
- foresight;
- backcasting

считаются разными типами аналитической задачи и не должны оцениваться одной метрикой.

## 6. Cultural Prediction Lab

Статус: **CATALOG CREATED**.

Уже выделены:
- Astrology
- Palmistry / Chiromancy
- Numerology
- historical/divinatory systems

Класс:
`NON_SCIENTIFIC`.

Они могут:
- иметь формализованный алгоритм;
- запускаться;
- проходить blind/backtest;
- сравниваться с baseline.

Они не могут:
- повышать scientific confidence;
- маркироваться как научно подтверждённые без соответствующих доказательств.

## 7. Источники, уже привязанные к проекту

- Hyndman & Athanasopoulos — Forecasting: Principles and Practice.
- NASA — Navigation Filter Best Practices.
- Stan Documentation.
- ECMWF — ensemble prediction / uncertainty.
- Nature — материал для научной оценки заявлений астрологии.
- PubMed/NCBI — историко-научный материал по palmistry/chiromancy.
- Пользовательский источник «Прогнозирование и формирование будущего» — discovery source для Delphi / scenarios / foresight / extrapolation.

## 8. Текущая карта проекта

```text
AU-01 / FUTURE LAB
│
├── CORE
│   ├── Method Registry
│   ├── Method Passport
│   ├── Method Selector [planned]
│   ├── Backtest Engine [partial: metrics only]
│   └── Score Registry [planned]
│
├── MATH / TIME SERIES
│   ├── Naive            [RUNNABLE]
│   ├── Mean             [RUNNABLE]
│   ├── Drift            [RUNNABLE]
│   └── SES              [RUNNABLE]
│
├── GRAPH / NETWORK
│   ├── Shortest Path    [DISCOVERED]
│   ├── MST              [DISCOVERED]
│   ├── Max Flow         [DISCOVERED]
│   ├── TSP              [DISCOVERED]
│   ├── CPM              [DISCOVERED]
│   ├── PERT             [DISCOVERED]
│   └── GERT             [DISCOVERED]
│
├── NARRATIVE
│   └── ALINA BOOK 2 Prediction Pool [DESIGNED]
│
├── POLITICAL / STRATEGIC
│   ├── Delphi           [DISCOVERED]
│   ├── Scenarios        [DISCOVERED]
│   ├── Foresight        [DISCOVERED]
│   └── Extrapolation    [DISCOVERED]
│
├── CULTURAL
│   ├── Astrology        [CATALOG_ONLY]
│   └── Palmistry        [CATALOG_ONLY]
│
└── SITE
    └── Future Lab MVP   [RUNNABLE]
```

## 9. Что НЕ считать готовым

Пока не реализованы и не квалифицированы:
- ARIMA/SARIMA;
- Kalman;
- Markov/HMM;
- Bayesian engine;
- Monte Carlo;
- causal inference;
- weather pack;
- trade/commercial pack;
- political event forecasting engine;
- text prediction pack;
- universal Method Selector;
- persistent Method Score Registry.

Они входят в архитектуру, но не должны отображаться как готовые runnable methods.

## 10. Следующий производственный порядок

```text
CURRENT INVENTORY
↓
MATH BASE
↓
BACKTEST ENGINE
↓
METHOD SCORE REGISTRY
↓
METHOD SELECTOR
↓
DOMAIN PACKS
   ├── Narrative
   ├── Weather
   ├── Trade
   ├── Political/Strategic
   ├── Text
   ├── Security
   └── OSINT
```

Это текущая точка отсчёта Future Lab.
