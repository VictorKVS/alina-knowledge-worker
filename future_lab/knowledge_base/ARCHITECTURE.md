# FATHER Predictive Knowledge Base — Combat Block v1

Статус: **DESIGNED / CORE CONTRACT CREATED**

Назначение: единый боевой блок базы знаний по прогнозированию и предиктивным вычислениям для всех агентов FATHER.

## 1. Главный принцип

Ни один прогнозный алгоритм не допускается к боевому использованию только потому, что он описан в LLM, Википедии или одном учебном материале.

Боевой алгоритм должен иметь доказательную цепочку:

SOURCE
→ THEORY
→ FORMULA
→ ALGORITHM
→ IMPLEMENTATION
→ TEST
→ BACKTEST / VALIDATION
→ RESOURCE PROFILE
→ QUALIFICATION
→ AGENT USE

## 2. Иерархия источников

1. ORIGINAL PAPER / PRIMARY SOURCE
2. ACADEMIC BOOK / MONOGRAPH
3. OFFICIAL STANDARD / UNIVERSITY MATERIAL
4. AUTHORITATIVE LIBRARY DOCUMENTATION
5. WIKIPEDIA — только навигационный слой

Wikipedia не может быть единственным основанием статуса QUALIFIED.

## 3. Боевой объект знания

Каждый алгоритм хранится как Algorithm Knowledge Unit.

Обязательные поля:
- algorithm_id
- name
- family
- task_types
- domains
- mathematical_basis
- assumptions
- limitations
- unsuitable_when
- primary_sources
- book_sources
- source_sections
- wikipedia_reference
- formulas
- pseudocode
- reference_implementation
- tests
- validation
- backtests
- metrics
- uncertainty
- resource_profile
- energy_profile
- implementation_version
- qualification_status
- provenance

## 4. Статусы

DISCOVERED
→ SOURCED
→ FORMALIZED
→ IMPLEMENTED
→ TESTED
→ VALIDATED
→ QUALIFIED
→ DEPRECATED

## 5. Боевой допуск

Для QUALIFIED обязательно:
- минимум один авторитетный источник;
- формальный алгоритм;
- воспроизводимая реализация;
- unit tests;
- domain-relevant validation/backtest;
- ограничения и предпосылки;
- контекстная оценка качества;
- resource profile;
- provenance.

## 6. Архитектура

FATHER PREDICTIVE KNOWLEDGE BASE
│
├── SOURCE REGISTRY
├── BOOK REGISTRY
├── PAPER REGISTRY
├── METHOD REGISTRY
├── ALGORITHM REGISTRY
├── FORMULA REGISTRY
├── IMPLEMENTATION REGISTRY
├── TEST REGISTRY
├── DATASET REGISTRY
├── BACKTEST REGISTRY
├── SCORE REGISTRY
├── RESOURCE REGISTRY
├── ENERGY REGISTRY
├── PROVENANCE LEDGER
└── QUALIFICATION GATE

## 7. Выдача агентам

AGENT
→ FORECAST REQUEST
→ KNOWLEDGE QUERY
→ CANDIDATE ALGORITHMS
→ FILTER BY ASSUMPTIONS / CONSTRAINTS
→ RUN
→ VALIDATE
→ RETURN PREDICTION + UNCERTAINTY + EVIDENCE + COST

## 8. Неизменяемое правило

Агент не копирует алгоритм в себя. Он обращается к единому Knowledge/Compute Core.

## 9. Связь с Future Lab

Knowledge Base = знания и доказательства.
Compute Engine = исполнимые алгоритмы.
Future Lab = квалификационный полигон.
Forecasting Core = сервис выбора и исполнения.
