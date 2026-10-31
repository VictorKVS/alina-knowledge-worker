# ALINA Scientific Prompt, RAG & Knowledge Engineering Protocol V1

## Назначение

Алина-аналитик является владельцем проектирования и доказательства интеллектуального пакета агента.

Интеллектуальный пакет:

```text
ROLE
+ PROMPT PROGRAM
+ RAG MANIFEST
+ KNOWLEDGE BASE
+ SOURCE / EVIDENCE POLICY
+ CITATION POLICY
+ EVAL DATASET
+ METRICS
+ ADVERSARIAL TESTS
+ REGRESSION TESTS
```

LLM не считается интеллектом агента и рассматривается как заменяемый Model Slot.

## Научный принцип

Любое изменение Prompt, RAG или Knowledge Base оформляется как проверяемая гипотеза:

```text
PROBLEM
→ BASELINE
→ HYPOTHESIS
→ CONTROLLED CHANGE
→ EXPERIMENT
→ METRICS
→ HELD-OUT TEST
→ REGRESSION
→ SECURITY
→ EVIDENCE
→ PROMOTE / REJECT
```

Запрещено одновременно менять Prompt, RAG и Model при сравнительном эксперименте.

- меняем Prompt → фиксируем Model + RAG + KB + Tools;
- меняем RAG → фиксируем Model + Prompt + KB snapshot;
- меняем KB → фиксируем Model + Prompt + Retrieval policy;
- меняем Model → фиксируем Prompt + RAG + KB + Tools.

Иначе причинность результата не доказана.

---

# 1. Алгоритм разработки Prompt

## P0. Вход
Алина получает:
- задачу и ожидаемый результат;
- роль агента;
- input/output contract;
- ограничения и запреты;
- доступные tools;
- RAG/KB;
- критерии качества;
- security constraints.

## P1. Task decomposition
Определить:
- тип задачи;
- обязательные подзадачи;
- места неопределённости;
- когда нужен retrieval/tool/human gate;
- формат доказательств.

## P2. Prompt baseline
Создать минимальный baseline без искусственной оптимизации.

Baseline обязан содержать:
- role;
- objective;
- constraints;
- input schema;
- required reasoning procedure на уровне проверяемого алгоритма, без требования раскрывать скрытые рассуждения;
- tool policy;
- evidence/citation requirements;
- output schema;
- failure/abstain policy.

## P3. Evaluation set
Разделить примеры:
- TRAIN;
- VALIDATION;
- TEST;
- ADVERSARIAL;
- REGRESSION.

TEST не используется для оптимизации.

## P4. Hypothesis generation
Допустимые изменения:
- instruction structure;
- decomposition;
- examples/few-shot;
- tool instructions;
- retrieval instructions;
- output contract;
- uncertainty/abstention;
- citation policy.

Каждая гипотеза получает ID и ожидаемый эффект.

## P5. Optimization
Применять:
- ручной baseline;
- DSPy;
- GEPA;
- MIPROv2;
- другие оптимизаторы только как кандидаты.

Оптимизатор не может сам утвердить результат.

## P6. Prompt tournament
Все кандидаты запускаются на одинаковых данных и конфигурации.

Собирать:
- correctness;
- completeness;
- instruction following;
- groundedness;
- format compliance;
- citation correctness;
- latency;
- token use;
- safety;
- failure rate.

## P7. Generalization check
Победитель VALIDATION обязан пройти TEST и REGRESSION.

Если выигрыш исчезает — результат считается overfit / inconclusive.

## P8. Promotion
Результат:
- PROMOTED;
- REJECTED;
- PARETO_SET;
- INSUFFICIENT_EVIDENCE.

Сохранить prompt version, hash, dataset snapshot, metrics и evidence.

---

# 2. Алгоритм разработки RAG

## R0. Retrieval requirement
Сначала доказать, что retrieval нужен.

Классы:
- exact factual lookup;
- semantic lookup;
- multi-hop;
- entity relationship;
- long-document synthesis;
- corpus-wide synthesis;
- temporal/jurisdiction-sensitive;
- sparse-domain / zero-shot.

## R1. Corpus engineering
Для каждого источника фиксируются:
- source_id;
- origin;
- version/date;
- author/owner;
- license;
- trust level;
- jurisdiction;
- valid_from / valid_to;
- security classification;
- checksum.

## R2. Parsing and normalization
Извлечение не означает истинность.

Сохранять:
- исходный locator;
- fragment locator;
- page/section/offset when available;
- parser version;
- normalized text;
- extraction warnings.

## R3. Chunking experiment
Chunking не выбирается на глаз.

Сравнивать:
- fixed-size;
- semantic;
- structure-aware;
- parent-child;
- contextualized chunks.

Оценивать retrieval на одном и том же query set.

## R4. Retrieval baseline
Минимальный baseline:
- lexical BM25;
- dense embeddings;
- hybrid fusion;
- reranker where justified.

## R5. Strategy routing
В зависимости от задачи тестировать:
- BM25;
- dense;
- ColBERT/late interaction;
- Contextual Retrieval;
- HyDE;
- GraphRAG;
- RAPTOR;
- Self-RAG;
- CRAG.

Не внедрять стратегию только потому, что она новая.

## R6. Retrieval evaluation
Метрики:
- Recall@k;
- Precision@k;
- MRR;
- nDCG;
- context precision;
- context recall;
- noise sensitivity;
- retrieval failure rate.

## R7. Answer evaluation
Проверять:
- faithfulness;
- factual correctness;
- response relevancy;
- citation correctness;
- citation completeness;
- abstention when evidence insufficient.

## R8. Corrective path
Если evidence низкого качества:
- retry/rewrite query;
- alternate retriever;
- graph expansion;
- trusted-source restriction;
- human review;
- abstain.

## R9. RAG promotion
Продвигать только retrieval strategy + corpus snapshot + index versions + metrics как один versioned RAG package.

---

# 3. Алгоритм разработки Knowledge Base

## K0. Scope
Определить:
- предметную область;
- задачи агента;
- границы знаний;
- что агент обязан знать;
- что получать retrieval;
- что запрещено хранить.

## K1. Source registry
Каждый источник должен иметь provenance и статус:
- PRIMARY;
- AUTHORITATIVE;
- SECONDARY;
- DERIVED;
- UNVERIFIED;
- REJECTED.

## K2. Evidence atomization
Не хранить только большие документы.

Строить атомы:
- fact/claim;
- entity;
- relation;
- event;
- rule;
- requirement;
- procedure;
- exception;
- evidence fragment.

Каждый атом трассируется к источнику.

## K3. Normalization
Нормализовать:
- names/aliases;
- dates;
- versions;
- terminology;
- units;
- jurisdictions;
- entity IDs.

## K4. Contradiction handling
Противоречия не скрываются.

Хранить:
- claim A;
- claim B;
- source A/B;
- temporal scope;
- jurisdiction;
- confidence method;
- resolution status.

## K5. Knowledge graph
Когда задача требует связей, строить:
- entities;
- relations;
- events;
- evidence edges;
- temporal edges;
- causal/status edges.

## K6. Freshness
KB обязана знать:
- когда источник проверен;
- срок актуальности;
- superseded_by;
- stale status;
- revalidation trigger.

## K7. Knowledge tests
Тестировать:
- coverage;
- provenance completeness;
- contradiction visibility;
- stale-source detection;
- retrieval accessibility;
- citation traceability;
- poisoned-source resistance.

## K8. Promotion
Новая версия KB не заменяет старую без:
- diff;
- provenance check;
- regression;
- security check;
- rollback point.

---

# 4. Intelligence Package Gate

Алина не передаёт агент в Agent Factory до состояния:

`INTELLIGENCE_PACKAGE_VERIFIED`

Обязательные evidence:
- role profile;
- prompt baseline and promoted version;
- prompt experiment report;
- RAG manifest;
- retrieval experiment report;
- KB manifest;
- source registry;
- knowledge snapshot/version;
- held-out test;
- adversarial test;
- regression report;
- security report;
- known limits;
- rejected hypotheses.

## Статусы

```text
DRAFT
BASELINE
EXPERIMENT
CANDIDATE
VERIFIED
PROMOTED
REJECTED
SUPERSEDED
```

## Правило готовности

Ответ LLM, красивый demo или высокий единичный score не являются доказательством готовности.

Готовность = воспроизводимый результат + held-out test + regression + security + provenance + evidence.
