# CH04 / Reflection — лабораторная программа A/B/C

**Источник:** Antonio Gulli, PDF 63–76. **DESIGNED_ONLY; ещё не выполнялась.**

## A. 20–30 строк, без LLM
Написать `producer(task)` с двумя версиями заранее известного ответа и `critic(candidate)`, сверяющий формальные условия. Цикл с max_iterations=3. При отсутствии PASS возвращать `REVIEW_REQUIRED`, а не бесконечно повторять.

## B. Локальная Ollama / universal ModelAdapter
Использовать `examples/ch04_reflection.py` на `ministral-3:8b` и `qwen3:8b`. Сохранить raw response/critique, parse status, число вызовов (два на итерацию), время, ошибки. Отдельно провести **изолированные функциональные тесты** `n=0 → 1`, `n=1 → 1`, `n=5 → 120`, `n=-1 → ValueError`, включая нежелательные типы; не запускать неизвестный код напрямую на основной машине. Базовый пример **не** выполняет сгенерированный код.

## C. FATHER / ALINA / POLYGON
Producer извлекает утверждения из главы; Critic формирует список проверяемых замечаний; Evidence Checker сопоставляет с первоисточниками и provenance; UAG разрешает только approved capabilities. POLYGON имеет закрытый набор, не доступный памяти агента. Итог: `PASS` только по внешним доказательствам, иначе `FAIL/REVIEW_REQUIRED`.

### Приёмка
Сохранить model name, version, prompt hashes, iterations, reason for stop, candidate SHA-256, tests, time/cost, provenance and security audit. Отделять «есть успешный запуск» от «правильно работает». 
