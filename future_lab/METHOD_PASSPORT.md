# Method Passport v2

Все прогнозные, аналитические, сетевые, экспертные и сравнительные методы Future Lab оформляются по единому контракту.

```yaml
method:
  id: TS-SES-01
  name: Simple Exponential Smoothing
  family: time_series
  status: RUNNABLE
  evidence_class: SCIENTIFIC_A

  purpose:
    predicts:
      - future_level

  inputs:
    - observations
    - horizon
    - alpha

  outputs:
    - point_forecast
    - diagnostics

  algorithm:
    summary: recursive exponentially weighted level
    code: future_lab.methods:simple_exponential_smoothing

  applications:
    - short-horizon level forecasting
    - baseline comparison

  assumptions:
    - no material trend
    - no material seasonality

  limitations:
    - strong trend reduces adequacy
    - structural breaks invalidate historical pattern

  unsuitable_when:
    - assumptions are materially violated
    - validation data are unavailable

  verification:
    unit_tests: true
    backtest_required: true
    recommended_metrics:
      - MAE
      - RMSE
      - MASE

  sources:
    - SRC-HYNDMAN-FPP3

  conclusion:
    summary: use for level-only processes and as a transparent benchmark
```

## Обязательные поля паспорта

1. **Что предсказывает / решает.**
2. **Входные данные.**
3. **Выход.**
4. **Алгоритм / формула.**
5. **Где применять.**
6. **Предпосылки.**
7. **Ограничения.**
8. **Когда не применять.**
9. **Метрики проверки.**
10. **Источники и класс доказательности.**
11. **Код и тесты.**
12. **Backtesting / qualification.**
13. **Практический вывод.**

## Правило допуска

`DISCOVERED` — метод найден и описан.

`DESIGNED` — определено место в архитектуре и контракт.

`RUNNABLE` — есть источник, алгоритм, код, тест и описание предпосылок.

`QUALIFIED` — выполнен backtesting на релевантном классе задач и зарегистрирован score.

`CATALOG_ONLY` — хранится для исторического/сравнительного исследования, но не используется как научно квалифицированный прогноз.

## Репутация метода

```text
method
+ domain
+ horizon
+ data shape
+ task type
+ dataset/version
+ implementation/version
→ score
```

Один и тот же метод может быть сильным в одном режиме и слабым в другом. Поэтому глобального «лучшего метода» в реестре нет.
