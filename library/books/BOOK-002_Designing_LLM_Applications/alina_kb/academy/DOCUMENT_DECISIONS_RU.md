# Алгоритм — тащить ли дубликат в базу ALINA?

**Источник идеи:** Suhas Pai, BOOK-002, CH02 PDF 138–143 — exact, approximate и semantic duplicates; обработка и качество PDF 120–137; PII PDF 143–154. **Решения ниже — инженерная надстройка FATHER.**

## Два независимых вопроса

**1. Имеем ли право получать и использовать документ?** Если нет — `REJECT` или `QUARANTINE`; если неизвестно — `REVIEW` без импорта содержимого.

**2. Добавляет ли он новое знание или evidence?** То же содержимое может иметь **новый URL/редакцию/дату/подпись**; происхождение всегда сохранять.

## Решения

| Решение | Применение |
|---|---|
| INGEST_NEW | Уникальный разрешённый полезный документ/новое свидетельство |
| LINK_DUPLICATE | Идентичные байты или нормализованный текст; сохранить оба source_id |
| NEW_VERSION | Изменённый регламент, документ новой редакции, новая дата |
| RELATED_VARIANT | Перевод, перепечатка, уточнение, близкая тема |
| REVIEW | Спорные near/semantic дубликаты, неясные права или качество |
| QUARANTINE | Чувствительные сведения / неизвестные разрешения |
| REJECT | Подтверждённая невозможность требуемого использования |

## Алгоритм

```text
check_rights_and_pii
 → preserve_source_identity + raw_sha256
 → parse_text_tables_and_revision
 → assess_extraction_quality
 → exact_bytes_and_normalized_content_match
 → check_document_version_and_legal_identity
 → compare_near_duplicate_candidates
 → identify_new_claims_and_independent_evidence
 → choose destination (graph / RAG / training / metadata only)
 → write decision, rationale, links, reviewer, audit
```

**Не удалять автоматически** документ с другим годом, редакцией, периодом действия или уникальными таблицами. Для OSINT перепечатка полезна как свидетельство распространения информации, но не подтверждает исходное утверждение независимо.

## Качество алгоритма

`false_merge_rate = wrongly_merged / audited_merged` и `source_retention = preserved_source_ids / received_source_ids`.

Порог похожести определять **только** после разметки эталонного набора для конкретной предметной области. Никаких универсальных 90% или 95% для юридических документов.

Нужно хранить **raw file hash**, **normalized text hash** и **semantic candidate status** отдельно.
