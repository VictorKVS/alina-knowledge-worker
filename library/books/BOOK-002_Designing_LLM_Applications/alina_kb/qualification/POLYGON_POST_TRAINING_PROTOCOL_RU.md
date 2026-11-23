# POLYGON — первичная независимая квалификация после обучения агента

**Статус:** ARCHITECTURE_AND_QUALIFICATION_PLAN / NOT_RUN.

## Концепция

ALINA обучает и формирует версионированный пакет компетенций. POLYGON — независимый экзаменатор **после обучения, до допуска**; затем снова при значимом изменении модели, промпта, RAG, инструментов или разрешений. UAG — enforcement прав в среде выполнения, не заменяется экзаменом.

## Принципы независимости

1. Frozen holdout (включая негативные и adversarial cases) не открывать агенту и ALINA.
2. ALINA получает классификацию ошибок и рекомендации, но не закрытые правильные ответы.
3. Критические нарушения безопасности не компенсируются высоким средним баллом.
4. Комиссия/человек утверждает границы ответственности, ролей и доступа; решение `PASS` только с evidence.
5. Квалификация привязана к комбинации: `agent_id / model_hash / prompt_version / kb_version / rag_index_version / tool_contract_revision / runtime_config / security_policy_version`.

## Фазы экзамена

- G1 Source integrity: правомерное происхождение и трассируемость.
- G2 Knowledge: фактическая корректность и базовые определения.
- G3 Reasoning: доказуемые выводы, обработка неоднозначности, UNKNOWN.
- G4 Tool usage: действия только в разрешённой области (проверка UAG).
- G5 Adversarial: prompt injection, ложные источники, противоречия, неверные права.
- G6 Performance: SLA, память/VRAM, стоимость, деградация под нагрузкой.
- G7 Regression: сохранение ранее доказанных компетенций.
- G8 Audit: trace IDs, provenance, финальная подпись и критерии допуска.

## Output example (synthetic, NOT real exam)

```json
{
  "agent_id": "OSINT-001",
  "tested_version": "NOT_SET",
  "status": "NOT_RUN",
  "qualification_scope": ["document-version-classification"],
  "gates": {"knowledge": "NOT_RUN", "reasoning": "NOT_RUN", "tools": "NOT_RUN", "safety": "NOT_RUN", "performance": "NOT_RUN", "regression": "NOT_RUN"},
  "security_violations": null,
  "release_allowed": false,
  "reviewer": null,
  "evidence": []
}
```

## Chapter 8 laboratory connection

[CH08 Alignment/Reasoning](../../labs/CH08/LAB_PROGRAM.md): проверка честности, отказов, источников, логики, защиты от атак. Наборы для обучения ALINA и независимый экзамен POLYGON должны быть разведены.

## Chapter 9 laboratory connection

[CH09 Inference Optimization](../../labs/CH09/LAB_PROGRAM.md): подтверждение качества после cache/quantization/speculation/early exit. Допуск к эксплуатации по изменённой конфигурации только после повторной проверки.

**Запрет:** нет evidence = NOT_RUN / NOT_QUALIFIED. Ни один агент не получает автоматический release PASS на основании собственной самооценки.
