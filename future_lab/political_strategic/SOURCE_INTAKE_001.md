# Political & Strategic Forecasting — source intake 001

## Source

User-provided article: **«Прогнозирование и формирование будущего»** (2011).

The article is retained as a *method-discovery source*, not as the sole authority for scientific validation.

## Methods extracted from the source

### PF-DEL-01 — Delphi method

The source describes a repeated expert-round process:
1. experts independently submit forecasts;
2. summaries are circulated to participants;
3. extreme views are commented on;
4. participants revise or defend estimates;
5. rounds repeat until sufficient convergence is reached.

Source-derived status: **METHOD_DISCOVERY**.

Authoritative validation/source still required before qualification.

### PF-SCN-01 — Scenario planning

The source describes scenario development through:
1. clarification of the background/context;
2. identification of influential factors;
3. definition of extreme/minimum/maximum factor states;
4. logical combination into plausible alternative scenarios.

The article also notes the historical use of scenario planning in Shell.

Authoritative corroboration:
- Shell scenarios: scenarios are alternative plausible futures and explicitly **not predictions**.
- Shell has used scenario thinking since the early 1970s.

### PF-FOR-01 — Strategic foresight

The source presents foresight as a combined approach using expert methods, scenarios and trend extrapolation.

Authoritative corroboration:
- OECD Strategic Foresight describes horizon scanning, megatrends analysis, scenario planning, visioning and back-casting.
- OECD treats foresight as preparation for multiple plausible futures, not a single deterministic prediction.

### PF-EXT-01 — Trend extrapolation

The source defines extrapolation as continuation of observed tendencies into the future under an assumption of sufficient inertia/stability.

This method belongs under the mathematical/time-series layer and must be benchmarked against naive/drift/ETS/ARIMA families.

## Important distinction for Future Lab

```text
FORECAST
  attempts to estimate a future value/event/probability

SCENARIO
  explores several plausible futures

FORESIGHT
  explores futures and prepares decisions/actions

BACKCASTING
  starts from a desired future and works backward
```

Do not merge these into one method.

## FATHER implementation target

```text
AU-01 / Future Lab
└── political_strategic/
    ├── delphi/
    ├── scenario_planning/
    ├── strategic_foresight/
    ├── horizon_scanning/
    ├── megatrends/
    ├── backcasting/
    ├── trend_extrapolation/
    └── evaluation/
```

Each method must obtain:
- authoritative source;
- formal workflow/algorithm;
- machine-readable method passport;
- software implementation where computable;
- evidence class;
- applicability/limitations;
- evaluation protocol;
- backtest or decision-quality assessment when backtesting is not meaningful.

## Qualification rule

Scenario planning and foresight are not scored as point forecasts when their purpose is exploration rather than prediction. Their evaluation should focus on coverage of plausible futures, assumption transparency, robustness of decisions and post-hoc usefulness, not raw predictive accuracy alone.
