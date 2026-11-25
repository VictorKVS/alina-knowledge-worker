# BOOK-002 CH13 — лаборатория архитектурных паттернов / FATHER / POLYGON

**Первоисточник:** Suhas Pai, PDF 683–700; **SOURCE_REVIEWED / DESIGNED_ONLY / NOT_RUN / NOT_QUALIFIED**.

## Цель

Выбрать из multi-LLM, cascade, router, specialized LLM и declarative programming решения, дающие лучшее качество/стоимость/латентность без потери доказательности. Никаких реальных замеров и моделей до отдельного прогона.

## A — базовая, детерминированная

- 12 синтетических задач (6 простых, 4 средних, 2 сложных) с заранее известными компетенциями и качеством имитированных моделей.
- Смоделировать фиксированную большую модель, cascade и router.
- Посчитать суммарное число обращений, стоимость, примерный latency budget, правильные/ошибочные маршруты.
- Проверить, что самодекларация `model_confidence` не принимается за доказательство correctness.
- Сделать ADR по выбору explicit / cascade / router.

## B — сравнительная

- На едином frozen dataset замерить: small-only, large-only, small→large cascade, router, task-specialist.
- Отдельно сверить confidence calibration и external verification.
- Для простой QA задачи сравнить Python+typed JSON schema, DSPy, LMQL (где поддерживаются в выбранной среде).
- Обязательные метрики: task success, evidence precision, unsupported claims, incorrect routing %, repeatability, p50/p95/p99, token/energy cost, timeout, OOM.
- Разделить train/tuning и закрытый POLYGON holdout.

## C — FATHER интеграционная квалификация

`ALINA Knowledge Fabric → Agent Factory/Block Matcher → route/cascade → model/tool adapter → UAG → verifier → POLYGON`.

Проверки:
1. Неправильный routing, модель не умеет вызов нужного инструмента.
2. Модель декларирует высокую уверенность, но выдаёт ложный факт.
3. Неподдерживаемая конфигурация выдана как совместимая.
4. Внутренний источник без разрешения попал в чужой контекст.
5. Регрессия при смене малой/средней/большой модели.
6. Сбой подзадачи приводит к fail-closed / bounded retry, не выдает PASS.
7. FRODO не получает доступ к сканированию без explicit scope.

## Evidence и допуск

`source_manifest, model_versions, architecture_ADR, skill_contracts, trace.jsonl, metrics.json, cost_profile, test_reports, security_review, qualification.json`. Критические нарушения безопасности/прав = 0. Все остальные пороги замораживать до испытания.

**Текущий статус:** только программа; ПО, интеграционный прогон и POLYGON certification НЕ выполнены.
