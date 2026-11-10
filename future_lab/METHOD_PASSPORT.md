# Method Passport v1

Каждый метод Future Lab оформляется по одному контракту.

```yaml
method:
  id: TS-SES-01
  name: Simple Exponential Smoothing
  family: time_series
  evidence_class: SCIENTIFIC_A

  purpose:
    predicts:
      - future_level

  authoritative_sources:
    - id: SRC-HYNDMAN-FPP3
      type: academic_text
      url: https://otexts.com/fpp3/

  inputs:
    - observations
    - horizon
    - alpha

  outputs:
    - point_forecast

  assumptions:
    - no material trend
    - no material seasonality

  unsuitable_when:
    - strong trend dominates
    - strong seasonal structure dominates

  algorithm:
    reference: future_lab.methods:simple_exponential_smoothing

  verification:
    unit_tests: true
    backtest_required: true
    recommended_metrics:
      - MAE
      - RMSE

  status: RUNNABLE
```

## Правило допуска

Метод не получает статус `RUNNABLE`, если отсутствует хотя бы одно из:

- источник;
- алгоритм;
- код;
- тест;
- описание предпосылок.

Метод не получает статус `QUALIFIED`, пока не проведён backtesting на релевантном классе задач.

## Репутация метода

Future Lab хранит оценку не «вообще», а по контексту:

```text
method
+ domain
+ horizon
+ data shape
+ task type
+ dataset/version
→ score
```

Поэтому метод может быть сильным для одного режима и слабым для другого.
