# CH09 — Инженерная лабораторная программа: ускорение и оптимизация инференса

**Первоисточник:** Suhas Pai, BOOK-002, PDF 459–491. **SOURCE_REVIEWED / DESIGNED_ONLY / NOT_RUN / NOT_QUALIFIED.**

## Главная цель

Найти воспроизводимый компромисс качества и скорости для задач ALINA/FATHER, проверив ограничения памяти и безопасность. Ничего не объявлять ускоренным до фактических замеров.

## A. Уровень учебного эксперимента

**A1 — кэш:** сравнить повторную обработку неизменного префикса и безопасное использование cache; на mock runtime вручную измерить экономию повторных операций, затем при доступном checkpoint проверить реальный KV-cache.

**A2 — quantization:** на синтетических числах выполнить FP32 → FP16/BF16/INT8 и обратное преобразование; проверить знаки, ноль, отрицательные числа, выбросы и saturation.

**A3 — theoretical memory:** расчёт веса модели по `parameter_count × bits_per_weight / 8`, отдельно добавить estimate KV-cache и runtime; отметить формат GB/GiB.

**A4 — speculative:** смоделировать draft acceptance на дискретных вероятностях, не выдавать toy simulation за ускорение реальной LLM.

## B. Сравнительные эксперименты

**B1:** один разрешённый точный checkpoint, одинаковые prompt versions и dataset, варианты: context-cache off/on, quantization поддерживаемых битностей, batch=1 и concurrency 2/4.

**B2:** при наличии runtime support проверить speculative on/off, acceptance rate, p95 и extra RAM.

**B3:** ранжировать варианты по Quality × Latency × VRAM × Total Cost; выбрать Pareto-допустимые конфигурации, не скрывать critical FAIL средними значениями.

**B4:** distillation/early exit — отдельно только при наличии доступа к весам, прав на адаптацию и воспроизводимого учебного набора; не мешать запуску первого FATHER.

Собирать TTFT, end-to-end latency p50/p95/p99, output tokens/sec, throughput, RAM/VRAM peak, correctness, citation accuracy, invalid JSON rate, cache hit rate, cost, process crashes.

## C. Интеграционная лаборатория FATHER

`ALINA produces task requirements → TIMA sizes compute → FATHER Architect selects candidate → Model Gateway applies safe runtime → UAG enforces data scope → POLYGON qualifies agent and configuration`.

Требования: cache isolation по tenant/security/source revision, prompt version, trace IDs, no sensitive data leakage, bounded queue, timeout, retry, audit, rollback to qualified version. Запрещать оптимизацию, которая ухудшает критическую компетенцию.

## Варианты

- **Lite:** ручные вычисления + Python standard libs + фиксированные fixtures.
- **Standard:** разрешённая локальная модель + сравнение cache/precision.
- **Research:** поддерживаемые open-weight модели, speculative, early exit, distillation, throughput under load.

## Программа негативных тестов

1. Изменился системный промпт, а cache не инвалидирован.
2. Tenant A пытается использовать KV-cache Tenant B.
3. После quantization агент уверенно выдаёт неверные нормативные ссылки.
4. Под длинным контекстом модель достигает OOM/latency timeout.
5. Несогласованные параллельно сгенерированные разделы.
6. Partial failures в speculative draft/target workflow.

## Квалификация POLYGON

**Заранее** определить SLA и quality floor в зависимости от роли. Строгие блокировки: любое неразрешённое обращение, критическая утечка, ложное заявление о выполненной проверке, невозможность rollback. Сравнить с baseline на независимых задачах. Допуск относится к версии **модели + prompt + RAG + runtime + параметрам оптимизации + dataset scope**.

**Артефакты после будущего прогона:** dataset manifest, hardware software versions, runbook, trace logs, metrics.json, security_negative_cases, model hashes, ADR, qualification.json, signed tag/SBOM для поставки.

**Итог на дату подготовки:** LAB_PREPARED / NOT_RUN. Никаких измерений или ускорений пока не подтверждено.
