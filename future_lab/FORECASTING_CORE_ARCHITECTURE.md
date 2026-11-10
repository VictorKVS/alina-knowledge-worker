# FATHER Forecasting Core — Architecture v1

Статус: **CORE CONTRACT CREATED**.

Назначение: единая база методов прогнозирования для всех агентов FATHER.

## Принцип

Агент не хранит собственную копию математических методов. Агент формулирует задачу, ограничения и контекст, а Forecasting Core выбирает, запускает, сравнивает и квалифицирует методы.

```text
AGENT TASK
   ↓
FORECAST REQUEST
   ↓
TASK CLASSIFIER
   ↓
METHOD SELECTOR
   ↓
METHOD REGISTRY / PASSPORTS
   ↓
RUNNERS
   ↓
COMPARE / ENSEMBLE
   ↓
UNCERTAINTY
   ↓
BACKTEST / VALIDATION
   ↓
METHOD SCORE REGISTRY
   ↓
RESOURCE / ENERGY PROFILE
   ↓
FORECAST RESPONSE
```

## Forecast Request Contract

```yaml
forecast_request:
  request_id:
  agent_id:
  domain:
  task_type:
  target:
  horizon:
  data_ref:
  data_shape:
  constraints:
    latency_ms:
    cpu:
    ram_mb:
    gpu:
    vram_mb:
    energy_budget:
    cost_budget:
  required_outputs:
    - point_forecast
    - interval
    - probability
    - scenarios
  evidence_policy:
  allowed_method_classes:
  forbidden_method_classes:
```

## Forecast Response Contract

```yaml
forecast_response:
  request_id:
  selected_methods:
  rejected_methods:
  assumptions:
  predictions:
  ensemble:
  uncertainty:
  evidence:
  backtest:
  method_scores:
  resources:
    cpu:
    ram:
    gpu:
    vram:
    latency:
    energy:
    energy_status: MEASURED|ESTIMATED|UNKNOWN
  limitations:
  confidence:
  decision_notes:
  versions:
```

## Core modules

- PMP-01 Method Registry
- Method Passport Catalog
- Method Selector
- Method Runner Interface
- Ensemble Engine
- Uncertainty Engine
- Backtest Engine
- Score Registry
- Resource Profiler
- Energy Profiler
- Evidence / Provenance Ledger
- Qualification Gate

## All-agent usage

PM-01 → demand/adoption/value forecasts  
AB-01 → process/load/SLA/cost forecasts  
AS-01 → state transitions/failures/timeouts  
AA-01 → agent success/tool load/workflow forecasts  
APO-01 → RPS/latency/capacity/resource forecasts  
Security → threats/incidents/risk/escalation  
OSINT → hypotheses/events/object behavior  
ALINA BOOK → event/character/relationship/plot forecasts  
TIMA → CPU/RAM/GPU/energy/capacity  
Trading → price/volatility/regime/risk  
Celestial → position/event/orbital state

## Qualification rule

No agent may declare a forecasting method QUALIFIED locally.

Qualification belongs to Future Lab and requires:
- source/evidence;
- algorithm;
- implementation;
- tests;
- relevant backtest/validation;
- context-specific score;
- limitations;
- resource profile;
- energy profile where measurable.

## Selection objective

Method selection is multi-objective:

```text
QUALITY
+ ROBUSTNESS
+ CALIBRATION
+ EXPLAINABILITY
+ REPRODUCIBILITY
--------------------------------
LATENCY
+ COST
+ ENERGY
+ COMPLEXITY
```

This is an architectural decision model, not a universal scientific scalar formula.
