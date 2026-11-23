# BOOK-003 — POLYGON qualification protocol (design only)

**Holdout bank:** изолирован от ALINA training и публичных `learning/` примеров. В репозитории только требования, ни одного закрытого экзаменационного примера.

1. Воспроизводимо идентифицировать применимый паттерн из письменных требований.
2. Собрать минимальную multi-agent микоархитектуру с контрактами.
3. Доказать корректное routing/correlation/retry/DLQ/idempotency на mock inputs.
4. Выполнить failing-worker, duplicate delivery, slow-LLM, tool-deny и rollback сценарии.
5. Подтвердить source provenance, tenant ACL и отсутствие несанкционированных действий.
6. Сравнить простую синхронную архитектуру с RabbitMQ и обосновать выбор.
7. Оценить ограничения LLM и корректный ABSTAIN/REVIEW в неоднозначных случаях.
8. Подписать квалификацию для определённой версии агента, tools, prompt, model, KB, policy и benchmark.

**Результаты:** PASS / FAIL / INSUFFICIENT_EVIDENCE, а до испытаний только NOT_RUN. Порог качества и бюджета зафиксировать до закрытого экзамена; critical auth violations = 0.
