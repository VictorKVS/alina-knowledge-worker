# Forecast Combination / Ensemble — Source Intake 003

Источник: А.А. Френкель, А.А. Сурков. **«Определение весовых коэффициентов при объединении прогнозов»**, «Вопросы статистики», №12, 2017.

Статус: **SCIENTIFIC_B / academic review**.

Статья рассматривает объединение нескольких индивидуальных прогнозов как взвешенную комбинацию и систематизирует способы вычисления весовых коэффициентов.

## Основные классы методов

### ENS-AVG-01 — Simple Average
Простое арифметическое среднее нескольких прогнозов.

### ENS-TRIM-01 — Trimmed Mean
Усечённое среднее: исключение части экстремальных прогнозов перед агрегированием.

### ENS-OLS-01 — Regression / OLS Combination
Определение весов через регрессионную модель / метод наименьших квадратов.

### ENS-GR-01 — Granger–Ramanathan Combination
Регрессионное объединение прогнозов с ограничениями на веса и анализом необходимости константы.

### ENS-BG-01 — Bates–Granger Error-Variance Combination
Выбор весов с целью минимизации дисперсии ошибки объединённого прогноза.

### ENS-INVERR-01 — Inverse Error Weighting
Вес индивидуального прогноза обратно пропорционален его ретроспективной ошибке.

Варианты ошибок:
- absolute error;
- MAE;
- RMSE / RSS;
- MSE;
- MAPE.

### ENS-INVMSE-01 — Inverse-MSE Weighting
Вес пропорционален обратной MSE и нормируется так, чтобы сумма весов была равна единице.

### ENS-AIC-01 — AIC-weighted Combination
Веса строятся на основе информационного критерия Акаике.

### ENS-BIC-01 — BIC-weighted Combination
Веса строятся на основе байесовского информационного критерия.

### ENS-ADAPT-01 — Adaptive Error Weighting
Веса обновляются по последним ошибкам; возможна экспоненциальная адаптация весов.

### ENS-PAIR-01 — Pairwise Preference
Веса формируются из попарных предпочтений / сравнений индивидуальных прогнозов.

### ENS-FACTOR-01 — Factor-analysis Combination
Комбинация прогнозов с использованием факторного анализа.

### ENS-QP-01 — Quadratic Programming
Веса находятся через задачу квадратичного программирования с ограничениями:
- 0 <= w_i <= 1;
- sum(w_i) = 1.

### ENS-MAPE-OPT-01 — Nonlinear MAPE Optimization
Веса выбираются минимизацией MAPE объединённого прогноза при ограничениях на веса.

## Архитектурный вывод для Future Lab

```text
METHOD A ┐
METHOD B ├─> FORECAST MATRIX
METHOD C ┘
          ↓
      COMBINER
          ↓
   WEIGHT STRATEGY
          ↓
    ENSEMBLE FORECAST
          ↓
      BACKTEST
          ↓
   WEIGHT UPDATE
```

Веса должны быть отдельным объектом, а не частью конкретного прогнозного метода.

## Требования к реализации

Каждая стратегия объединения должна возвращать:
- individual_forecasts;
- weights;
- weight_method;
- training_window;
- error_metric;
- constraints;
- combined_forecast;
- diagnostics.

## Qualification

Статья используется как обзорный академический источник. Для квалификации конкретных методов до RUNNABLE нужно добавить первичные источники (Bates & Granger, Granger & Ramanathan, Stock & Watson и др.), код, unit tests и rolling-origin backtest.
