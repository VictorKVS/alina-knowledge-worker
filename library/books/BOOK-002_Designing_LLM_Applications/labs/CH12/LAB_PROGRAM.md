# BOOK-002 CH12 — лабораторная программа RAG / ALINA / POLYGON

**Источник:** Suhas Pai, PDF 604–682; SOURCE_REVIEWED. **Статус: DESIGNED_ONLY / NOT_RUN / NOT_QUALIFIED.**

## Цель и гипотезы

Проверить, как ALINA извлекает нужный факт с точной цитатой из проверенного корпуса, отделяя ошибки retrieval от ошибок generation. Сравнить стоимость и качество полного RAG-конвейера с простыми альтернативами.

### Вариант A: управляемый корпус без LLM

- 30 синтетических документов: 5 актуальных и 5 устаревших версий, 5 отрицаний, 5 точных ID, 5 вводящих в заблуждение, 5 ограниченных по доступу.
- 24 заранее размеченных запроса: составные, с редакциями, с отсутствием ответа, точным ID и конфликтом источников.
- Разметить `source_id, page, revision, applicability, scope, sha256, evidence_span, correct_answer`.
- Сравнить строковый поиск/FTS/BM25, реестр версий и защиту от ложных совпадений.
- Проверить `NO_EVIDENCE / REVIEW` и отдельный отказ по полномочиям.

**Метрики:** recall@k, exact-source accuracy, unauthorized retrieval=0, false merge count, correct abstention.

### Вариант B: сравнить этапы RAG

На одном frozen наборе, отдельно и кумулятивно:
1. BM25; dense embeddings; hybrid retrieval.
2. С query rewrite и без; PRF и HyDE только при доступном runtime.
3. Reranker и без него.
4. CoN и без него; контроль сохранения исходных source spans.
5. Разные chunk sizes, overlapping и metadata-aware разбиение.
6. Long-context baseline и RAG с одинаковыми правами, где технически возможно.

Зафиксировать retrieval recall@k/MRR, citation groundedness, unsupported claims, latency, memory and token cost. Исходное тестовое множество не менять между сравнениями.

### Вариант C: интеграционный экзамен POLYGON

`ALINA ingest/source provenance → parser/chunk → versioned hybrid index → UAG permission prefilter → retrieve/rerank/refine → GPT/local LLM → verification → output with citations → POLYGON`.

- Условия допуска: изоляция tenancy/roles; отсутствие чужих документов во входном контексте; точные цитаты и корректные версии; 0 выполненных неразрешённых действий.
- Экзамен: закрытые вопросы с потерянным контекстом, изменённым нормативом, противоречием, ложной авторитетной фразой, отсутствующим фактом и prompt injection в найденном документе.
- Не передавать ALINA закрытый holdout, а в обратной связи выдавать только категории ошибок и требуемые компетенции.
- Квалификационный паспорт связывает модель, промпт, индекс, corpus hash, tools, UAG policy и versioned eval-set.

### Обязательное разделение ошибок

`RETRIEVAL_MISS`: нужный документ отсутствует в top-k.
`RERANKING_ERROR`: нужный документ найден, но исключён или потерян при перерасстановке.
`REFINE_LOSS`: важная оговорка/число/область действия потеряна при сокращении.
`GENERATION_UNSUPPORTED`: ответ содержит неподтверждённое утверждение при доступном контексте.
`AUTHORIZATION_VIOLATION`: данные вне scope попали в retrieval/context.
`VERSION_CONFLICT`: неверная редакция или противоречивые источники.

### Метрики и условия приёмки

Критические нарушения доступа и сведения без допуска к раскрытию = 0. Пороги качества, latency и стоимости зафиксировать **до запуска**. Проверять independent holdout, воспроизводимость, regression после обновления KB. При отсутствии доказательств — NOT_RUN/FAIL, не объявлять PASS по генеративной самооценке.

### Требуемые будущие артефакты

`dataset_manifest.json`, `gold_queries.jsonl`, `source_spans.jsonl`, `index_manifest.json`, `query_rewrites.jsonl`, `retrieval_rankings.jsonl`, `verified_claims.jsonl`, `tests/`, `metrics.json`, `qualifications/POLYGON.json`, SHA256/ADR/evidence.

**Эти исполняемые артефакты пока не созданы — это программа последующих испытаний.**
