# Работа с Алиной

Приложение локальное, основной целевой запуск — Windows и Python 3.11+.
Установка зависимостей: `python -m pip install -r requirements.txt`.
Проверка: `python -B -m unittest discover -s . -p "test_*.py" -v`.
Тест RTF требует Windows; не выдавайте пропуск платформенных проверок за их успех.
Не включайте data/, config.json, книги, их выдержки или секреты в коммиты.
Сохраняйте loopback-привязку сервера и проверки Origin/токена для изменений.
Не называйте механическое извлечение обучением модели, проверкой фактов или продвижением в KB.
Тестовые материалы должны быть синтетическими. Не запускайте install.ps1 в облачной среде.

## Визуальный аналитик

Для задач сравнения эталонного дизайна и реализации используйте протокол `docs/knowledge/BOOKCRAFT_VISUAL_ANALYST_V1.md` и контракт `docs/knowledge/visual-analysis-contract.v1.json`. Аналитик фиксирует наблюдаемые расхождения, приоритет и доказательства; не называет реализацию идентичной без измеримого сравнения и не подменяет инженера при выборе способа исправления.


## Trend & Demand Analyst

Для анализа востребованности контента используйте `docs/knowledge/TREND_ANALYST_PROTOCOL_V1.md` и `docs/knowledge/trend-recommendation-contract.v1.json`.

Аналитик обязан разделять наблюдаемые метрики, интерпретацию тренда, прогноз и рекомендацию. Прогнозы показывают временной горизонт, источники и confidence; при недостатке данных используется `insufficient_evidence`. После теста рекомендация должна получить исход `useful / neutral / wrong / inconclusive`, чтобы система училась на качестве собственных советов.


## Процессы Алины-аналитика

Для новых рабочих процессов используйте контракт `docs/knowledge/process-contract.v1.json` и мета-процесс `processes/alina_process_design.v1.json`.

Не считайте ответ LLM выполнением шага. RUN должен пройти последовательные `work_step_runs`; каждый обязательный шаг завершается только `DONE / BLOCKED / NOT_APPLICABLE / REVIEW_REQUIRED`. Причина обязательна для всех terminal-state кроме `DONE`. Результат и evidence сохраняются отдельно и остаются трассируемыми к `run_id + step_id`.


## Технический аудит с пентестом

Основной процесс технического аудита: `processes/security_audit_with_pentest.v1.json`.

Обязательная последовательность:

```text
DISCOVERY → INVENTORY → SAFE AUDIT → CONFIGURATION AUDIT
→ VULNERABILITY ASSESSMENT → THREAT MODEL → RISK ENGINE
→ APPROVAL GATE → ACTIVE PENTEST (optional)
→ NORMALIZED FINDINGS → COMPLIANCE MAPPING
→ CONTROLS → SECURITY ARCHITECTURE
→ IMPLEMENTATION PLAN → RETEST → REPORT/EVIDENCE
```

ACTIVE_TEST запрещён без подтверждённого authorization/scope. Если разрешение не получено, активный шаг закрывается `NOT_APPLICABLE` с причиной, а сам аудит продолжается в безопасном режиме.

Не объединяйте сущности `Finding`, `Vulnerability`, `Threat Scenario`, `Pentest Verified`, `Compliance GAP`, `Risk` и `Control`. Сканер/CVE не является доказательством взлома или нарушения конкретного требования. Используйте `docs/knowledge/security-audit-result-model.v1.json`.


## Scientific Prompt / RAG / Knowledge Engineering

Для проектирования интеллектуального пакета агента обязательно использовать:
- `docs/knowledge/SCIENTIFIC_PROMPT_RAG_KB_ENGINEERING_V1.md`;
- `processes/alina_intelligence_package_design.v1.json`;
- `docs/knowledge/intelligence-package-contract.v1.json`.

Алина не должна считать Prompt, RAG или Knowledge Base готовыми без baseline, контролируемого эксперимента, held-out test, regression, security и evidence. При сравнении меняется только один фактор: Prompt, RAG, KB или Model; остальные фиксируются. Извлечение текста не означает истинность знания. Каждый knowledge atom должен иметь provenance. Противоречия, rejected hypotheses и negative knowledge сохраняются, а не скрываются.

Финальный handoff в Agent Factory разрешён только после gate `INTELLIGENCE_PACKAGE_VERIFIED`.


## Book → Knowledge → FATHER Engineering

Для извлечения знаний из книг и длинных технических источников используйте:
- `docs/knowledge/ALINA_BOOK_TO_FATHER_KNOWLEDGE_PROTOCOL_V1.md`;
- `processes/alina_book_knowledge_factory.v1.json`;
- учебные gold-cases в `docs/knowledge/training/`.

Алина обязана разделять source-supported content и собственную инженерную интерпретацию. Книга может породить knowledge atom и candidate capability, но не делает блок production-ready и не определяет единственно правильную реализацию. После закрытия extraction scope допускается отдельный этап repository scouting и выбор REUSE / ADAPT / BUILD / REJECT. Ошибочные или исправленные mappings сохраняются как learning feedback для следующих прогонов.
