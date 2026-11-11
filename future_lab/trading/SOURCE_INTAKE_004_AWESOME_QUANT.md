# Quant / Trading Reference Intake 004 — awesome-quant

Источник: **wilsonfreitas/awesome-quant**  
URL: https://github.com/wilsonfreitas/awesome-quant

Тип источника: **CURATED RESOURCE INDEX / DISCOVERY SOURCE**.

Репозиторий представляет собой большой curated-list для quantitative finance. Он полезен как карта инструментов и библиотек, но не как научное доказательство эффективности конкретной торговой стратегии.

## Категории, которые берем в Future Lab

1. Numerical Libraries & Data Structures
2. Financial Instruments & Pricing
3. Technical Indicators
4. Trading & Backtesting
5. Portfolio Optimization & Risk Analysis
6. Factor Analysis
7. Sentiment Analysis & Alternative Data
8. Time Series Analysis
9. Market Data & Data Sources
10. Prediction Markets
11. Calendars & Market Hours
12. Visualization
13. Quant Research Environments

## Technical Indicators — кандидаты на инструментальный слой

Из репозитория выделены библиотеки/проекты:
- TA-Lib / ta-lib-python
- pandas_talib
- Tulipy
- talipp
- streaming_indicators
- ta
- bta-lib
- TTR
- MarketTechnicals.jl
- ta4j
- technical-indicators
- orderflow
- Wickra
- QuantWave

Future Lab не считает индикатор самостоятельным прогнозным методом автоматически.

Правило:

```text
INDICATOR
→ SIGNAL RULE
→ STRATEGY
→ EXECUTION MODEL
→ COSTS / SLIPPAGE
→ BACKTEST
→ WALK-FORWARD / OUT-OF-SAMPLE
→ RISK METRICS
→ QUALIFICATION
```

## Trading & Backtesting — особенно полезно

В awesome-quant есть отдельный раздел Trading & Backtesting, включая проекты, ориентированные на:
- backtesting;
- paper/live trading;
- walk-forward experiments;
- Monte Carlo;
- holdout evaluation;
- anti-leakage / purged cross-validation;
- rule linting;
- execution realism;
- position exits.

Это важный ориентир для архитектуры FATHER Trading Lab.

## Обязательная проверка торговых методов

Для любого торгового паспорта Future Lab обязательны:
- market / asset;
- timeframe;
- data source;
- signal definition;
- entry;
- exit;
- position sizing;
- fees;
- slippage;
- latency assumptions;
- look-ahead bias check;
- survivorship bias check;
- train/test split;
- walk-forward;
- out-of-sample;
- drawdown;
- Sharpe / Sortino / Calmar;
- profit factor;
- turnover;
- benchmark comparison.

## Что не делаем

- Не копируем все библиотеки без оценки.
- Не считаем GitHub popularity доказательством alpha.
- Не считаем технический индикатор рабочей стратегией без правил и backtest.
- Не используем результаты backtest без проверки leakage, fees, slippage и out-of-sample.
- Не смешиваем pricing/risk libraries с directional forecasting.

## Target structure

```text
future_lab/trading/
├── indicators/
├── strategies/
├── market_structure/
├── order_flow/
├── time_series/
├── factor_models/
├── sentiment_alt_data/
├── portfolio_risk/
├── pricing/
├── backtesting/
├── data_sources/
└── research_tooling/
```

## Source role

awesome-quant получает роль:
**RESOURCE_DISCOVERY / TOOL_CATALOG**.

Каждая выбранная библиотека или метод проходит отдельный аудит:
license → maintenance → reproducibility → tests → source authority → integration value.
