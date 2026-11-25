# BOOK-002 — глава 12: Retrieval-Augmented Generation

**Первоисточник:** Suhas Pai, Designing Large Language Model Applications; пользовательский PDF, страницы 604–682/765. Русскоязычное авторское учебное изложение, не дословный перевод.

**Статус:** SOURCE_REVIEWED / LAB_DESIGNED / TESTS_NOT_RUN / NOT_QUALIFIED.

## Карта первоисточника

| PDF | Содержательная тема |
|---|---|
| 604–608 | Причины RAG, long-tail facts, обновление знаний и citations |
| 609–612 | Четыре применения RAG, динамическое решение о retrieval |
| 613–625 | Rewrite: PRF, HyDE, keyword expansion, topic drift, decomposition |
| 625–636 | Retrieve: BM25, hybrid, metadata filtering, generative retrieval, GraphRAG |
| 636–645 | Rerank: cross-encoder, ColBERT, pointwise/pairwise/listwise |
| 645–656 | Refine: extractive/abstractive summaries, Chain-of-Note |
| 656–665 | Insert and Generate; active retrieval / FLARE, citations |
| 665–670 | RAG and conversational memory management |
| 670–672 | Retrieval of in-context examples / LLM-R |
| 672–674 | RAG during model training / REALM |
| 674–682 | Limitations; long context versus RAG; RAG versus fine-tuning |

## 1. Зачем нужен RAG

Автор определяет RAG широко: усиление работы модели внешними данными. Типичные преимущества — локальная/закрытая предметная информация, новые факты, ссылки, long-tail сведения и меньшие затраты на обновление знаний в сравнении с постоянным обучением весов. Но retrieval может сам вносить ошибки, а доступность данных ещё не доказывает их достоверности.

Четыре типа задач (609–610): извлечение внешних фактов, контекста истории, few-shot примеров и документации инструментов. **FATHER:** разделять категории памяти, сроки действия и доверие к источникам.

## 2. Полный конвейер

`query → rewrite → retrieve → rerank → refine → insert → generate → verify`.

Не каждая стадия обязательна; оптимальность и стоимость проверяются через ablation. Проверка должна относиться к каждой стадии, а не только к финальному ответу.

## 3. Rewrite

Автор рассматривает PRF, HyDE и гибридные методы расширения; для complex tasks — query decomposition. Риск topic drift (622). **FATHER:** не разрешать переписанному запросу менять идентификатор документа, статус, дату или рамки доступа.

## 4. Retrieval

BM25 — сильный недорогой baseline; vector-only не подходит для всех точных совпадений. Hybrid search объединяет keyword и dense embeddings. Метаданные нужны для точной фильтрации. Автор также обсуждает generative retrieval и GraphRAG; построение графа может быть дорого и не гарантирует точных отношений.

Приоритет метрики на первом шаге — **recall** требуемых доказательств. Даже превосходный генератор не может доказать факт из документа, который retrieval не нашёл.

## 5. Rerank и Refine

Reranking помогает ранжировать кандидатов более точной моделью (cross-encoders, ColBERT, LLM-based ranking). Refine уменьшает шум и длину источников, включая Chain-of-Note: отдельная заметка для каждого документа, указывающая наличие ответа, только полезного контекста или нерелевантность.

**FATHER:** переработанная заметка — производный артефакт; доказательство остаётся за исходным `source_id / edition / page / span / hash`.

## 6. Insert и Generate

Порядок материалов в контексте может влиять на ответ; «lost in the middle» и шум требуют экспериментальной проверки. FLARE динамически инициирует retrieval по мере генерации; не всякий model API открывает token log-probabilities, поэтому некоторые способы экспериментальны для определённых моделей.

## 7. Memory / Examples / Training

Retrieval подходит для поиска истории и прогресса, а также отбора релевантных эталонных примеров. REALM иллюстрирует совместное обучение модели и retrieval; это не обязательный компонент нашего первого RAG.

## 8. Ограничения

Автора занимают ошибки поиска, противоречия источников, недостаточное понимание и сравнительные tradeoffs RAG с длинным контекстом и fine-tuning. Новые факты обычно проще обновить в KB/RAG; устойчивое новое поведение может потребовать fine-tuning. Порог выбирается по задаче и измерениям.

## 9. FATHER / ALINA Analytical Core

`source provenance → parse → versioned chunks → ACL/edition pre-filter → lexical+dense retrieval → rerank → evidence notes → atomized claims → deterministic/NLI verifier → knowledge graph / response`.

Не считать `cosine similarity`, `LLM agreement` или `CoN` независимым доказательством. Закрытый holdout POLYGON отделён от обучающей базы ALINA.

**Обязательные метрические группы:** retrieval recall@k, MRR, source grounding, citation precision, unsupported claim rate, abstention quality, authorization violations, latency p95, token/compute cost, update & rollback correctness.

## Контрольные вопросы

1. Почему у RAG есть внешнее знание, контекст истории, примеры и tool docs?
2. Как topic drift мешает retrieval?
3. Когда BM25 лучше dense-only?
4. Почему source ACL лучше применять до попадания текста в LLM?
5. Чем rerank отличается от refine?
6. Как CoN обнаруживает отсутствие доказательств?
7. Почему FLARE зависит от возможностей модели/runtime?
8. Когда использовать RAG, длинный контекст или fine-tuning?

[Лаборатория A/B/C](../labs/CH12/LAB_PROGRAM.md)
