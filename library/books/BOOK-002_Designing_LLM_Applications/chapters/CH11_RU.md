# BOOK-002 / Глава 11 — Representation Learning and Embeddings

**Первоисточник:** Suhas Pai, *Designing Large Language Model Applications*, пользовательский PDF 553–603 из 765; напрямую изучен. Это самостоятельный русский учебный конспект, не текст книги.

**Состояние:** SOURCE_REVIEWED / LAB_DESIGNED / NOT_RUN / NOT_QUALIFIED.

## Карта по первоисточнику

| PDF | Раздел |
|---|---|
| 553–559 | Представления, embeddings, pooling, Sentence Transformers |
| 559–567 | Semantic search, метрики similarity, противоположный смысл |
| 567–575 | Fine-tuning, triplets, hard negatives, triplet loss, multiple negatives |
| 576–578 | Instruction embeddings / description-based retrieval |
| 579–583 | MTEB, Matryoshka, компромиссы размерности |
| 584–588 | Binary / integer embeddings, product quantization |
| 588–597 | Parsing, chunking, windows, layout, semantic/late chunking |
| 598–601 | Векторные БД, фильтры, многоуровневые представления |
| 601–603 | Интерпретация embedding, Sparse Autoencoders |

## 1. Математика и смысл

Embedding: модель преобразует текстовую единицу в вектор фиксированной размерности. Pooling: CLS/mean/max/weighted/last-token, выбор зависит от архитектуры/цели обучения.

Cosine: `dot(a,b)/(norm(a)*norm(b))`; для единично нормированных векторов cosine = dot. Альтернативы: Euclidean и dot product; использовать меру, совместимую с обучением модели.

**Критическое предупреждение автора:** смысловое сходство само по себе недостаточно определяет требуемый тип отношения. Высокую similarity могут получить противоположные утверждения о выходе на пенсию (PDF 564–567). Следовательно, **для FATHER** cosine — поиск кандидатов, а не доказательство логической связи.

## 2. Зачем обучать embeddings

Тройки `(anchor, positive, negative)`, в том числе hard negatives, особенно полезны для различения противоположных утверждений. Triplet loss `max(d(a,p)-d(a,n)+margin,0)`. Другой вариант — Multiple Negatives Ranking Loss. Все негативные метки должны быть проверены, нельзя генерировать их без evidence и объявлять эталоном.

## 3. Инструкции для embedding

INSTRUCTOR добавляет описание предметной области, типа текста и задачи. Для FATHER можно сравнить обычный и instruction-conditioned embedding для запросов по законам и техническим стандартам, но это пока гипотеза эксперимента.

## 4. Compression и стоимость

Matryoshka Representation Learning позволяет обучить векторы, пригодные для усечения по заданным размерностям. Binary/int8 и product quantization уменьшают память ценой потенциального ухудшения поиска. 100 млн × 768 × FP32 — приблизительно 307.2 GB числовых данных, **без индекса и метаданных**. Для нашего стартового масштаба оптимизацию не утверждаем без результатов.

## 5. Parsing и chunking

Автор подробно разбирает: overlap/sliding window, metadata, layout, semantic и late chunking. Основная причина ошибок RAG часто возникает **ещё до** LLM: потерянная структура документа, неправильно прочитанная таблица, пропущенная единица измерения или область действия условия (PDF 588–597).

**FATHER-адаптация:** сохранять `document_id + edition + section + page + offset + applicability_scope + hash`. Вектор даёт поиск, граф — тип доказанной связи, исходник — проверку истинности.

## 6. Vector stores и explainability

Векторные системы поддерживают поиск близких соседей, фильтрацию метаданных, обновления и удаление. Многоуровневые embeddings используют единицы предложения, абзаца, раздела и документа. Sparse Autoencoders в конце главы исследуются как путь к интерпретируемым признакам embedding.

## 7. Практический вывод для ALINA

`source → parse + provenance → chunks + scope → embedding/index → candidate retrieval → claim/negation/version verification → typed knowledge graph → evidence`.

Схожие векторы **не** дают автоматически `DUPLICATES`, `CONTRADICTS` или `SUPERSEDES`: такие связи требуют независимых проверок. Для POLYGON особенно важны негативные пары и ошибки контекста.

## Контрольные вопросы

1. Чем CLS pooling отличается от mean pooling?
2. Почему cosine — не показатель истинности?
3. Что такое hard negative и зачем он нужен?
4. Чем triplet loss отличается от Multiple Negatives Ranking Loss?
5. Что дает Matryoshka Representation Learning?
6. Почему binary embeddings не всегда хуже int8?
7. В каких случаях контекст соседнего chunk обязателен?
8. Почему векторную базу нельзя считать полноценной базой доказательств?

[Лаборатория A/B/C](../labs/CH11/LAB_PROGRAM.md)
