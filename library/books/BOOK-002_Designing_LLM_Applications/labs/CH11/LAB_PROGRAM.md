# BOOK-002 / CH11 — лаборатория Embeddings, Search, Chunking

**Источник:** Suhas Pai, PDF 553–603. **SOURCE_REVIEWED / DESIGNED_ONLY / NOT_RUN**.

## Общая цель

Доказать на независимом контрольном корпусе, что ALINA извлекает нужные фрагменты, не путает противоположные утверждения, версии и права доступа, сохраняет точную provenance и находит long-range зависимости.

## Лаборатория A — базовая

**A1. Геометрия:** вручную и Python рассчитать dot, cosine и Euclidean для 5 игрушечных векторов, проверить нормализацию, нулевые и переполненные значения, корректную обработку несовпадающих размерностей.

**A2. Контроль поиска:** 24 синтетических документа: 6 точных релевантных, 6 перефразов, 6 отрицаний, 6 ложноположительных/устаревших. Для каждого задать правильные source_id и gold labels, не допускать training/test leakage.

**A3. Chunking:** разметить 3 учебных документа, где правила из начала текста действуют на данные в конце; сохранить table/heading/scope и версии. Сравнить paragraph-only и overlapping windows.

**Метрики:** Recall@k, MRR, false-positive rate on negations, source-span validity, parse completeness. Не считать результаты известными заранее.

## Лаборатория B — сравнение

**B1.** BM25/лексический baseline против 2 embedding models (при наличии допустимых весов/лицензий). Query/document encoding соответствуют назначению модели.

**B2.** Сравнить chunk strategies: fixed, overlap, metadata-aware, layout-aware, semantic; late chunking отдельно при наличии совместимой long-context embedding модели.

**B3.** Сравнить FP32, INT8, binary, Matryoshka и product quantization, где действительно поддерживаются. Измерить размер индекса, Recall@k, точность hard negatives и p95; не переносить результат одного корпуса на другой.

**B4.** Для triplet/contrastive fine-tuning отдельно сравнить fine-tuned и базовую модель на замороженном независимом holdout и обнаружить возможные регрессии.

## Лаборатория C — интеграция FATHER

`ALINA reads source → parse → chunk + metadata → embedding model → indexed store → retrieval → authoritative claims verifier → knowledge graph → POLYGON independent exam`.

- UAG фильтрует разрешённые corpus IDs **до** отправки данных в LLM.
- Каждая возвращённая запись содержит `source_id, edition, page, section, offset, hash, access_scope`.
- Дубликаты сворачиваются только после проверки фактической идентичности, а не cosine.
- Если документ говорит «НЕ», индекс не должен автоматически подтверждать позитивное утверждение.
- При конфликте редакций → REVIEW до разрешения версии.

## Варианты реализации

1. **Lite:** Python + SQLite/FTS и детерминированные проверки; без GPT.
2. **Standard:** Sentence Transformers + локальный индекс/pgvector/FAISS или Qdrant, сравнение с BM25.
3. **Research:** multiple embedding models + MRL/binary/PQ + long-range/late chunking + triplet training.

## Граница квалификации POLYGON

Закрытые экзаменационные запросы и источники не должны попадать в обучающие данные ALINA. Проверять как релевантность, так и доказательность, отрицания, доступы, несвязанные версии, пропущенные таблицы, ложные дубликаты. Целевой статус 0 нарушений полномочий; другие пороги фиксировать **до** прогона.

## Evidence, которое потребуем после запуска

Corpus/source manifest SHA256, parsed docs, chunk maps, embedding model revision, vector index version, gold query labels, retrieval logs, Recall@k/MRR, adversarial cases, benchmark environment, ADR and POLYGON qualification.

**Пока это программа испытаний, код или результаты не выдаются за выполненные.**
