# MEMORY-BLOCK-001 — контракт памяти для FATHER (проект)

**Версия:** 0.1 · **Статус:** DESIGN_ONLY / NOT_IMPLEMENTED / NOT_QUALIFIED. Основано на изучении Memory Management: Antonio Gulli, PDF 130–151. Это проектный контракт FATHER.

## Назначение

Сохранять и извлекать состояние выполнения и проверенные знания агентов, не превращая memory в канал несанкционированных действий.

## Интерфейсы

| Operation | Input | Output | Инвариант |
|---|---|---|---|
| `get_session` | tenant_id, user_id, session_id | session, version | пользователь имеет доступ к сессии |
| `append_event` | ids, event_id, payload, expected_version | event_ref, new_version | идемпотентность event_id; optimistic lock |
| `search_memory` | tenant_id, actor_id, query, scope, top_k | records, source_refs | ACL filter до возвращения текста |
| `save_memory` | type, statement, provenance, validity, ACL | memory_id, version | непроверенные сведения не маркируются VERIFIED |
| `invalidate_memory` | memory_id, reason, actor | tombstone_ref | удаление/прекращение применимости отражено в индексе |

## Typed envelope (учебный пример)

```json
{
  "schema_version": "0.1",
  "tenant_id": "sandbox",
  "actor_id": "alina-reader",
  "user_id": "test-user",
  "session_id": "s-001",
  "task_id": "t-001",
  "memory_type": "SEMANTIC",
  "statement": "Паттерн требует отдельного контракта памяти",
  "source": {"book_id":"LIB-0040","chapter":"CH08","pdf_pages":[130,151]},
  "trust": "DRAFT",
  "validity": {"expires_at": null, "revision": 1},
  "access_scope": ["sandbox:read"],
  "provenance_sha256": null
}
```

## Изменение при масштабировании

`in-memory dict → SQLite → shared SQL+vector store → distributed API`. Сохранять логический интерфейс `MemoryPort`, меняя конкретный `MemoryAdapter`.

**Проверки:** schema validation, cross-tenant denial, duplicate event, stale version conflict, restart recovery, deletion propagation, prompt injection in retrieved memory, inaccessible document in search results.

## Требование приёмки

До испытаний `NOT_RUN`; критические нарушения изоляции = 0. POLYGON тестирует неизвестные учебному агенту сценарии, а его закрытые эталоны недоступны MemoryService.
