# BOOK-002 — Алгоритм качественного обучения моделей и подготовки агентов

**Версия:** v0.1 · **Дата:** 2026-11-22 · **Назначение:** FATHER / ALINA / System Architect / ML Engineer / POLYGON.

> **Разделение происхождения:** §1–§3 привязаны к главе 2 *Designing Large Language Model Applications*, Suhas Pai (оригинальный PDF, стр. 92–167). §§4–9 — предлагаемые инженерные процедуры FATHER, частично выходящие за рамки главы 2. **Не путать предобучение LLM, SFT, RLHF/RL, RAG и изменение внешней памяти агента.**

## 1. Что мы пытаемся доказать

**Нельзя начинать обучение с команды «скачаем побольше данных».** Сначала в письменном виде определяем:

- Целевой навык и допустимый класс задач (например, «архитектор строит корректную DFD»).
- Область применимости: языки, форматы, специальности, виды документов, опасные случаи.
- Данные входа и ожидаемые выходы.
- Метрики и порог допуска, **заданные до испытаний**, включая безопасность и стоимость.
- Базовое решение для сравнения: правила, поиск, промпт, RAG или существующая модель.

**Gate 0:** нет воспроизводимой постановки задачи и baseline — обучение не запускать.

## 2. Первичный источник: какие аспекты данных влияют на обучение

| PDF | Раздел | Главный инженерный вопрос |
| --- | --- | --- |
| 92–98 | Ingredients of an LLM | Что за данные, токенизатор, цель обучения и архитектура? |
| 99–106 | Pre-Training Data Requirements | Где взять достаточные данные и чего в них недостаёт? |
| 107–119 | Popular / Synthetic Datasets | Какие источники, права, риски и синтетика? |
| 120–137 | Preprocessing, filtering | Как извлекать полезный текст и не разрушать смысл? |
| 138–143 | Deduplication and memorization | Какие повторы допустимы, что запоминается, где риски приватности? |
| 143–154 | PII detection/remediation | Какие данные человека присутствуют и каковы последствия обработки? |
| 154–155 | Training Set Decontamination | Не видела ли модель экзаменационные вопросы заранее? |
| 156–161 | Data Mixtures / ordering | Как сбалансировать домены и порядок подачи? |
| 161–167 | Downstream / Bias | Как проверить реальные навыки и ошибки распределения? |

**Автор не даёт универсальных «идеальных» долей корпуса или порога perplexity.** Его примеры из исследований нельзя автоматически назначать правилами FATHER.

## 3. Алгоритм создания датасета

```text
SOURCE_INTAKE
  └─ 01_source_register       источник, hash, права, лицензия, дата, версия
     └─ 02_extract            текст, таблицы, заголовки, привязка к страницам
        └─ 03_validate         проверка качества извлечения и полноты
           └─ 04_normalize     только документированные безопасные преобразования
              └─ 05_quality    релевантность, читаемость, представительство доменов
                 └─ 06_dedup   exact → near; semantic — отдельный контроль
                    └─ 07_sensitive PII / secrets / правовые ограничения
                       └─ 08_split   раздельные train, validation, test, holdout
                          └─ 09_decontamination exact, n-grams, near; ручная проверка
                             └─ 10_mix     документированные доли и порядок обучения
                                └─ 11_manifest source lineage + статистика
                                   └─ 12_approval human + security + POLYGON
```

**Порядок не универсален:** часть проверок, например изоляция запрещённых данных и legal gate, выполняется *до* анализа содержимого; процедуры очистки и дедупликации могут меняться местами при доказанной необходимости.

### Входной контракт одной записи (наша схема)

```json
{
  "record_id": "SAMPLE-0001",
  "source_id": "SRC-001",
  "source_version": "2026-11-22",
  "source_sha256": "64-character-digest-required",
  "source_span": "page:12,section:3",
  "license_status": "REVIEW_REQUIRED",
  "processing_permission": "NOT_APPROVED",
  "domain": "ai_architecture",
  "language": "ru",
  "text_hash": "64-character-digest-required",
  "sensitive_data_status": "NOT_REVIEWED",
  "dataset_role": "UNASSIGNED",
  "quality_status": "PENDING"
}
```

Демонстрационные значения выше — шаблон, не настоящие SHA-256. В рабочих данных hashes рассчитываются и проверяются.

### Дедупликация: три независимых механизма

**Exact:** нормализованный текст → SHA-256 → равные хэши в одной группе. Это проверка только *выбранной нормализации*.

**Near:** вычислить признаки сходства (например, shingles + MinHash/LSH), затем проверить кандидаты по выбранному порогу. Порог должен утверждаться после выборочного аудита: иначе можно ошибочно объединить разные редакции нормативного документа.

**Semantic:** embedding similarity и экспертная проверка. Сходный смысл не гарантирует взаимозаменяемости, точности или одинакового правового статуса.

**Gate:** каждая группировка сохраняет все `source_id`, оригинальные hashes и ссылки на варианты. Удалять исходные данные необратимо без политики и аудита нельзя.

### Проверка загрязнения экзаменов

1. Создать непересекающиеся группы документов по первоисточнику и семейству связанных документов.
2. Отделить закрытый holdout до подготовки обучающих примеров.
3. Выполнить проверку точного совпадения и n-gram пересечений.
4. Запустить near-duplicate проверку; для спорных случаев — независимая экспертиза.
5. Не включать эталонные ответы POLYGON в RAG, train, подсказки или публичные примеры на этапе квалификации.
6. Сохранить протокол: набор проверок, найденные пересечения, исключения и допуски.

**Нулевая найденная контаминация не доказывает, что её вообще нет.** Проверки уменьшают риск, но не дают абсолютной гарантии.

## 4. Алгоритм выбора способа улучшения (инженерная надстройка FATHER)

```text
define_failure()
  if answer_is_stale_or_missing:
      test_source_registry_and_retrieval()
  elif output_schema_is_broken:
      test_schema_control_and_prompt()
  elif tool_action_is_wrong:
      test_workflow_permissions_and_deterministic_logic()
  elif stable_skill_deficit_remains:
      compare_prompt_vs_RAG_vs_SFT_or_PEFT()
  if feedback_has_verifiable_reward_and_safe_environment:
      evaluate_RL_or_preference_optimization_as_separate_project()
  perform_regression_and_security_evaluation()
```

Нельзя считать внешнюю память или retrieval дообучением весов. RLHF/DPO/RL требуют собственных данных, критериев и экспериментов и подробно изучаются в следующих главах.

## 5. Качественное обучение и контроль эксперимента

**Перед обучением:** зафиксировать базовую модель и лицензию, tokenizer/version, все данные и разрешения, контрольные наборы, обучаемые параметры, гиперпараметры, ресурсы, расчётную стоимость, метрики качества и stop-conditions.

**Во время:** логировать шаг, эпоху, train/validation loss, время, потребление VRAM, исключения, контрольные точки. Нельзя выводить обобщающую способность только из снижения train loss.

**После:** измерить качество по заранее замороженным срезам: целевая задача, общие задачи, безопасность, редкие случаи, неизвестные формулировки. Повторить несколько запусков при важной неопределённости.

**Выпуск:** модель и адаптер имеют идентификаторы, hashes, SBOM/build provenance (где применимо), сохранённые ссылки на данные и эксперименты, решение человека и независимые evidence POLYGON.

## 6. Метрики и формулы

**Retention ratio:** `N_accepted / N_source`. Не является метрикой качества, только описывает объём.

**Exact duplicate rate:** `N_exact_duplicates / N_source`. Не отражает near/semantic duplicates.

**Contamination observed:** `N_flagged_eval_items / N_eval_items`. Это частота **обнаруженных** пересечений, не абсолютная оценка отсутствия утечек.

**Coverage by slice:** `N_covered_cases / N_required_cases`. Классы случаев и пороги должны быть согласованы с заказчиком.

**Acceptance rate:** `N_passed_hard_gates / N_exam_cases`; критические нарушения могут блокировать выпуск независимо от среднего процента.

**Quality delta:** `Q(candidate) - Q(baseline)` на *том же* frozen dataset при сопоставимых условиях.

Метрики фиксировать отдельно по домену, сложности, чувствительности и типу ошибки, а не только одним средним.

## 7. Ролевой контракт FATHER

| Роль | Вход | Выход и ответственность |
| --- | --- | --- |
| Product/Business Analyst | Бизнес-цель | Измеримые задачи, приоритеты, стоимость ошибки |
| System Analyst | Процессы, категории данных | Требования, контракты, DFD |
| ALINA | Первичные источники, допуск | Knowledge, Training, Learning Packages с provenance |
| ML Engineer | Датасет, base model, план | Воспроизводимое обучение, checkpoints, metrics |
| System Architect | Workload, privacy, ресурсы | ADR способа улучшения и размещения |
| TIMA | План, среда, требования | Инфраструктура, мониторинг и measurement evidence |
| Security/UAG | Права, потоки, API | Isolation, secrets, право доступа и обработки |
| POLYGON | Holdout, критерии, артефакты | Независимые PASS/FAIL, регрессия, отчёт |
| Human owner | Полное evidence | Решение о допуске и выпуске |

## 8. Quality gates

```text
QG0 Requirements approved
QG1 Source rights/provenance approved
QG2 Extraction/quality audit approved
QG3 Dedup and sensitive-data review approved
QG4 Holdout isolated; contamination report reviewed
QG5 Candidate method and compute plan approved
QG6 Training evidence reproducible
QG7 Holdout + safety + regression passed
QG8 Deployment security/latency/cost passed
QG9 Human-approved release; rollback ready
```

Любой `FAIL` по критическому пункту → блокировка следующего этапа. Любой `UNKNOWN` → запрос evidence, а не автоматический PASS.

## 9. Учебная программа

Начинающий студент объясняет смысл и выполняет нормализацию и exact dedup. Разработчик добавляет near dedup, quality review, split и автоматические тесты. ML Engineer сравнивает методики на frozen holdout. Architect объясняет trade-offs и ресурсы. POLYGON проводит квалификацию.

**Текущий статус документа:** DESIGN_PROPOSED; источники прочитаны; сквозная система не реализована и не квалифицирована.
