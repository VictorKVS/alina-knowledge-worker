# FATHER Future Lab — «Расчёты будущего»

Подраздел **AU-01 — Аналитик Универсальный / «Алина Аналитик»**.

Цель Future Lab — не выдавать «предсказания» одним способом, а хранить, запускать, сравнивать и проверять **методы прогнозирования** из разных областей.

## Инженерный принцип

```text
TASK
  ↓
PROBLEM CLASSIFICATION
  ↓
METHOD CANDIDATES
  ↓
ASSUMPTION CHECK
  ↓
RUN METHODS
  ↓
COMPARE / ENSEMBLE
  ↓
FORECAST + UNCERTAINTY
  ↓
KNOWN FUTURE
  ↓
BACKTEST
  ↓
METHOD SCORE REGISTRY
```

Каждый метод обязан иметь:

1. уникальный ID;
2. класс доказательности;
3. авторитетный первоисточник или академический reference;
4. формализованный алгоритм;
5. входы/выходы;
6. предпосылки;
7. область применимости;
8. ограничения и противопоказания;
9. воспроизводимый код;
10. unit/contract tests;
11. backtesting-метрики;
12. историю фактической эффективности.

## Классы

- **SCIENTIFIC_A** — первичные/авторитетные научные и инженерные источники.
- **SCIENTIFIC_B** — признанные вторичные технические источники.
- **EXPERIMENTAL** — исследовательские методы, ещё не квалифицированные.
- **NON_SCIENTIFIC** — культурные/исторические/дивинационные системы. Их правила можно формализовать и тестировать, но нельзя представлять как научно подтверждённый прогноз.

## Начальный пул

### Time Series
- Naive
- Historical Mean
- Drift
- Simple Exponential Smoothing
- далее: ETS, ARIMA/SARIMA, dynamic regression, VAR

### State / Navigation
- Kalman-family
- state-space
- Markov
- HMM

### Probabilistic
- Bayesian models
- Monte Carlo
- probabilistic graphical models

### Event / Risk
- survival / hazard
- reliability
- scenario probability

### Causal
- DAG
- structural causal models
- counterfactuals

### Narrative
См. [Narrative Prediction Pool](narrative/README.md).

### Historical / Divination
См. [Cultural Prediction Lab](cultural/README.md).

## Базовые источники

- Hyndman, R.J., Athanasopoulos, G. — *Forecasting: Principles and Practice*, 3rd ed.: https://otexts.com/fpp3/
- Python edition: https://otexts.com/fpppy/
- NASA — *Navigation Filter Best Practices*: https://ntrs.nasa.gov/citations/20250002787
- Stan Documentation: https://mc-stan.org/users/documentation/
- ECMWF — ensemble prediction / forecast uncertainty: https://www.ecmwf.int/en/research/modelling-and-prediction/quantifying-forecast-uncertainty

## Запуск

```powershell
python -m unittest test_future_lab.py -v
python future_lab/server.py
```

Открыть:

```text
http://127.0.0.1:8771/
```

Сайт является лабораторным интерфейсом; он не означает, что все перечисленные методы уже реализованы.
