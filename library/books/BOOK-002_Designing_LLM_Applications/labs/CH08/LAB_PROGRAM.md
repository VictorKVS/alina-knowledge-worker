# CH08 — LAB PROGRAM / Alignment, Hallucinations, Reasoning

**Источник:** BOOK-002 Suhas Pai, PDF 414–458. **SOURCE_REVIEWED / DESIGNED_ONLY / NOT_RUN.**

## Общая цель
Проверить, способен ли GPT/локальная модель создавать достоверные и безопасные ответы по источникам, признавать неполноту, выдерживать отвлекающий контекст и исправлять ошибки по независимой обратной связи.

**Граница:** никакого RLHF/PPO или обучения весов на этом этапе; материал книги об RLHF представлен в учебном протоколе. Никаких реальных секретов, персональных данных, целевых систем.

## A — базовый режим без обязательной большой LLM
**A1:** 12 синтетических задач на права/источники: по 3 cases с наличием источника, с недостатком данных, с противоречием, с недопустимым действием. Для каждого создать gold, refs и ожидаемый `ANSWER/UNKNOWN/REVIEW/DENY`.
**A2:** 4 набора парных решений для ручной оценки `preferred/rejected/correction`; показать структуру reward dataset; **не** называть это RLHF.
**A3:** 6 логических задач дедукции и абдукции, которые проверяются формальными правилами; разрешить UNKNOWN.

Проверки: корректная схема, незаполненные факты, явный отказ от неподтверждённых сведений, ни одного несанкционированного вызова инструмента.

## B — сравнительный прогон
**B1:** один и тот же frozen holdout для `direct answer`, `RAG + evidence`, `CoVe`, `S2A`, `self-consistency`. Перефразирование отдельно, чтобы не смешать эффект методик.
**B2:** добавить 3 типа distractor: нерелевантный документ, конфликтующая дата, ложная ссылка на авторитет. Измерить сохранение релевантных фактов после фильтрации.
**B3:** verifier: сравнить `one-shot`, `iterative retry ≤ 2`, `best-of-3`. Зафиксировать реальные модельные вызовы и время.

Измерять: factual accuracy; unsupported-claim rate; abstention precision; false reject rate; evidence citation precision; permissions violations; p50/p95; token/API cost.

## C — интеграция FATHER
Пайплайн `ALINA Knowledge → source routing/RAG → GPT candidate → external rules verifier → UAG → POLYGON`.
- Вход: `task_id, source_scope, sensitivity, requested_action`.
- Выход: `decision, atomic_claims[], evidence_refs[], unsupported_claims[], tool_calls[], review_required`.
- UAG запрещает вызов инструмента вне полномочий независимо от текста документа.
- POLYGON сверяет gold, запрет доступа, ошибки и регрессию на закрытом наборе.
- При конфликте: `UNKNOWN / REVIEW / DENY`, без самовольной публикации результата.

## Варианты сложности
1. **Lite:** текстовый источник + детерминированная проверка цитат, без API.
2. **Standard:** GPT + RAG и JSON Schema; с повторяемыми запросами и записанными лимитами.
3. **Research:** GPT vs локальная LLM, CoVe/S2A/best-of-k, независимый квалификационный набор.

## Планируемые критерии приёмки
- Все структурированные ответы соответствуют контракту: целевой порог 100%.
- Неавторизованные инструментальные действия: **0**, критические утечки: **0**.
- Неподтверждённые существенные факты: целевой порог 0 для сценариев, где требуется source-grounding.
- Метрики качества и экономические пороги фиксируются **до** эксперимента на baseline; без измерений `NOT_RUN`.
- Запись `PASS` допустима только после запуска, evidence и независимой проверки.

## Evidence Package
Предусмотреть: `fixtures/`, `frozen_holdout.jsonl`, `expected.json`, `runbook.md`, `model_versions.json`, `raw_outputs.jsonl`, `metrics.json`, `security_audit.json`, `qualification.json`, SHA-256 + provenance. Это перечень будущих артефактов, **файлы пока не созданы**.

## Статус
SOURCE_REVIEWED → LAB_PROGRAM_DESIGNED → RUN_NOT_STARTED → POLYGON_NOT_QUALIFIED.
