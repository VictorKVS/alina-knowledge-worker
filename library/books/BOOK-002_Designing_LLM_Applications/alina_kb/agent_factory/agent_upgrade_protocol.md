# Протокол контролируемой модернизации всех агентов FATHER

## Предусловие

Есть установленный агент, версия blueprint, проверяемый контракт, текущая оценка и зарегистрированный сбой или требование изменения.

## Не менять весь агент без диагностики

| Симптом | Первая гипотеза | Слой для изменения | Что измерить |
| --- | --- | --- | --- |
| Неправильный факт | Источник отсутствует, устарел, плохо найден | Knowledge / RAG | groundedness, citation validity, recall@k |
| Неправильная структура ответа | Prompt/schema не задаёт строгую форму | Prompt / output validation | schema pass rate |
| Неверный вызов инструмента | Tool contract или рабочая логика | Workflow / UAG | unauthorized actions, tool errors |
| Повторяемая ошибка рассуждения | Требуется уточнить метод или тренировать навык | Knowledge / Learning / SFT candidate | frozen task accuracy |
| Потери на длинном тексте | Chunking, retrieval, context budget | RAG / data | retrieval coverage / latency |
| Избыточная стоимость | Избыточный контекст, неверный выбор модели | RAG / Model deployment | tokens, throughput, cost |
| Регрессия после обновления | Несовместимость версий | Versioned full bundle | old vs new on same tests |
| Утечка или превышение полномочий | Ошибка доверенных границ | Security / UAG | zero critical violations |

## Алгоритм

```text
incident / eval failure
  -> classify_error
  -> trace_to_source_prompt_retrieval_tool_or_model
  -> generate change hypothesis
  -> propose minimal affected packages and ADR
  -> sandbox experiment with paired baseline
  -> independent POLYGON qualification
  -> security and contract regression
  -> human approval
  -> signed release, evidence, rollback
  -> monitor outcomes -> feed ALINA graph
```

**Запрещено:** считать успехом снижение loss без проверки задач; учить агента на закрытом экзамене; позволять FATHER Architect менять собственные права или критерии оценки; отключать UAG в результате prompt optimization.

## Версионировать вместе

`agent_blueprint_version`, `model_version`, `prompt_sha256`, `rag_index_version`, `source_manifest_version`, `tool_contract_version`, `eval_dataset_version`, `security_policy_version`, `build_provenance`, `decision_adr`.

## Неподтверждённые этапы

План не является автоматизированным pipeline. Runtime, эксперименты, интеграционные тесты и POLYGON ещё потребуют реализации.
