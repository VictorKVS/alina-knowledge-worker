# LAB-0040-CH08 — Memory Management (A/B/C)

**Источник:** Antonio Gulli, PDF 130–151. **Статус:** DESIGNED_ONLY / NOT_RUN / NOT_QUALIFIED.

## A — для начинающего (Python, без модели)

Написать один `MemoryStore` на словарях: `session_id → events[]`, `user_id → memories[]`. Создать 5 синтетических пользователей и 3 сессии. Проверить, что хранится в контексте, что в состоянии, а что во внешнем долговременном хранилище. Условия: каждый user видит только свои записи, при отсутствии памяти возвращается `NOT_FOUND`.

## B — инженерное сравнение (SQLite / адаптер)

Зафиксировать контракт `MemoryPort`. Сравнить `DictAdapter` и `SQLiteAdapter` на одинаковых fixtures: persist/restart, duplicate event, optimistic version, removal, summary drift и incorrect access. Сравнить с документированным паттерном `Session/State/MemoryService` в ADK или equivalent LangGraph store после выбора совместимой версии.

Метрики: точность извлечения, отсутствие чужих данных, восстановление после перезапуска, дубли событий, latency p95, размер хранилища и качество summarization.

## C — интеграция ALINA / FRODO / POLYGON

Проектный сценарий: ALINA ищет проверенные знания в общедоступном корпусе; FRODO получает только разрешённую проекцию; UAG контролирует запросы и инструменты; POLYGON скрывает holdout от учебных сессий. Провести негативные кейсы на синтетических материалах: подмена system prompt через retrieved note, смешивание арендаторов, устаревшие записи, replay event, ложная summary.

**До последующего запуска:** сохранять ADR, SHA256, immutable provenance, tool/version manifests, tests, telemetry, security and qualification evidence. Никакие результаты заранее не выдумывать.
