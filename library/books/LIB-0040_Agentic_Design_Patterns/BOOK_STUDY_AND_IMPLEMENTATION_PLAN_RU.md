# LIB-0040 — План изучения и внедрения Agentic Design Patterns в FATHER

**Источник:** Antonio Gulli, *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems* (пользовательский оригинал, 458 PDF-страниц, 21 глава и приложения; SHA-256 в README).  
**Статус:** WORK_PLAN_CREATED / CH06_SOURCE_NOT_YET_REVIEWED / IMPLEMENTATION_NOT_STARTED.  
**Дата назначения работ:** 2026-11-25.  
**Главный принцип:** один паттерн книги = один инженерно разобранный алгоритм + одна исполняемая лаборатория + измеримый вклад в FATHER. Без деклараций об испытаниях без логов.

## 0. Обязательный вход IDEA+ перед каждым паттерном

Применять [FATHER IDEA+ v1.0](https://github.com/VictorKVS/FATHER_CODEX/blob/main/docs/protocols/FATHER_IDEA_PLUS_PROTOCOL_V1.md):
1. **WHY:** конкретная задача, условия и метрики; зачем нужен паттерн?
2. **INTERNAL_SCOUT:** какие наши компоненты уже выполняют функцию? код/тесты/commit, а не только название.
3. **WORLD_SCOUT:** где в литературе, официальной документации, научных работах и GitHub есть реальный подход?
4. **COMPOSITION:** схема соединения существующих компонентов с адаптерами и контрактами.
5. **FEASIBILITY:** что технически доступно на установленной платформе и с какой надёжностью; GO / CONDITIONAL_GO / RESEARCH / NO_GO.
6. **NEXT_STAGE:** какие конкретные измеримые изменения технологии дадут основания пересмотреть решение.
7. **BUILD:** минимум необходимых новых блоков. Независимая приёмка.

IDEA+ документирован в другом репозитории, но пока **не реализован как автоматический шлюз**.

## 1. Фактическое состояние по имеющимся материалам

| Глава | Паттерн | Имеющиеся артефакты | Следующее действие | Статус |
|---|---|---|---|---|
| CH01 | Prompt Chaining | не подтверждён отдельный завершённый комплект | сверить оригинал; учебная карточка, код, тесты | TODO |
| CH02 | Routing | chapters/CH02, examples/ch02_router.py, labs/CH02 | интеграционные и негативные тесты, метрики | DESIGNED; NOT_QUALIFIED |
| CH03 | Parallelization | chapters/CH03, examples/ch03_parallelization.py, labs/CH03 | конкурентность, отмена, частичные ошибки, измерения | DESIGNED; NOT_QUALIFIED |
| CH04 | Reflection | chapters/CH04, examples/ch04_reflection.py, tests/test_ch04_reflection.py | реальные LLM испытания, независимый evidence checker | OFFLINE_TESTS_PASS (по пользовательскому журналу 6/6); NOT_QUALIFIED |
| CH05 | Tool Use | chapters/CH05, examples/ch05_tool_use.py, tests/test_ch05_tool_use.py | сохранить runtime trace; негативные случаи и mock UAG | OFFLINE_TESTS_PASS (7/7), Ollama qwen3:8b 3/3 демонстрационных сценария по пользовательскому журналу; NOT_QUALIFIED |
| **CH06** | **Planning** | отдельный подтверждённый учебный комплект не найден | **ПЕРВООЧЕРЕДНАЯ РАБОТА** | TODO / SOURCE_REVIEW_REQUIRED |
| CH07 | после CH06: название и содержание сверить по оригиналу | не подтверждено | изучить после CH06 | TODO |
| CH08 | Memory Management | chapters/CH08, architecture/MEMORY_BLOCK_CONTRACT_RU.md, labs/CH08 | запустить лаборатории A/B/C, проверить разделение памяти | SOURCE_REVIEWED / LAB_DESIGNED / NOT_QUALIFIED |
| CH09–CH21 | остальные паттерны | отдельное выполнение не подтверждено | последовательно пройти по оригинальному оглавлению | BACKLOG |

**Примечание:** приведённые runtime-результаты CH05 сообщены пользователем и не сопровождаются загруженным в GitHub полным trace/evidence. Их нельзя выдавать за независимую POLYGON-квалификацию.

## 2. Шаблон обязательной обработки каждой главы

Создать для главы `CHxx`:
1. `chapters/CHxx_<SLUG>_RU.md`: назначение, **что именно утверждает автор**, страницы PDF, схема процесса/алгоритм, условия применимости, ограничения, типовые ошибки; отделить идеи FATHER от содержания книги.
2. `architecture/CHxx_<SLUG>_IDEA_PLUS.md`: задача, сравнение с существующими FATHER блоками, ссылки на официальные/научные/репозиторные аналоги, лицензионные и аппаратные ограничения, feasibility verdict.
3. `examples/chxx_<slug>.py`: сначала минимальный проверяемый алгоритм без LLM, затем LLM ModelAdapter (Ollama/OpenAI/Gemini/Anthropic там, где применимо), без самовольных внешних действий.
4. `tests/test_chxx_<slug>.py`: happy path, negative, malformed schema, timeout/cancel, repeated calls, permissions and isolation when applicable.
5. `labs/CHxx/LAB_PROGRAM.md`: A — детерминированный baseline; B — реальная модель; C — FATHER composition / UAG / POLYGON.
6. `evidence/CHxx/` (создавать при реальных испытаниях): command, Python/model/dependency versions, model digest where available, immutable input hashes, output trace, test report and qualification decision.
7. `architecture/AGENT_PATTERNS_CATALOG_RU.md`: обновить entry лишь после подтверждения главы, не при одном создании плана.

**Приёмка главы:** точность по первоисточнику; работоспособный код; воспроизводимые тесты; отдельный уровень `DESIGNED / OFFLINE_PASS / RUNTIME_PASS / INTEGRATION_PASS / POLYGON_QUALIFIED`; демонстрация конкретного применения в общей производственной линии FATHER. Не публиковать полный текст книги или стороннего перевода.

## 3. Текущая работа: CH06 — Planning

**Цель лаборатории:** определить, когда планирование действительно улучшает исполнение, и создать **контролируемый планировщик задач**, который не выдаёт намерение за результат.

### CH06-P0 — SOURCE_REVIEW
- Открыть исходную главу 6 и точно записать страницы, определения, примеры, алгоритмы, инструменты и ограничения **по автору**, не реконструировать их по общим знаниям.
- Сверить используемые в примерах API с актуальными официальными руководствами; датировать проверку.
- Выделить различия `plan`, `execution`, `observation`, `replan`, `validation`, `done`.

### CH06-P1 — IDEA+ / FEASIBILITY
- Сценарий 1: "создать небольшой FastAPI endpoint с тестами" — сравнить простую процедуру против отдельного Planning Agent.
- Сценарий 2: "загрузить книгу, извлечь события, проверить evidence, построить граф" — проверить зависимости, достаточность уже существующих ALINA-компонентов.
- Найти готовые аналоги в официальных фреймворках и GitHub, зафиксировать лицензии/версии/интерфейсы, не объявлять обнаружение при отсутствии поиска.
- Критерии: полное выполнение цели, корректность зависимостей, доля отклонённых ошибочных планов, восстановление после сбоя, стоимость/время относительно baseline.

### CH06-P2 — MINIMAL BASELINE (без LLM)
- Типизированные `Task`, `Plan`, `Step`, `Dependency`, `Evidence`.
- DAG-проверка (циклы, недостижимые зависимости), лимиты шагов, статусы `PENDING/RUNNING/FAILED/VERIFIED/BLOCKED`.
- Исполнять только явно разрешённые mock tools, не использовать реальные внешние изменения.
- Терминальное `DONE` возможно только после независимой проверки всех обязательных шагов.

### CH06-P3 — MODEL ADAPTER
- Ollama `qwen3:8b`, `ministral-3:8b`: генерация строго структурированного плана; проверка схемы; корректировка после отклонённого плана.
- LLM выдаёт предложения, но не разрешения; executor и policy gate внешние.
- Для облачных моделей — только после разрешения и соблюдения политики данных.

### CH06-P4 — FATHER COMPOSITION
- Соединить `IDEA+ -> Planning -> Tool Use CH05 -> Reflection CH04 -> Evidence Checker -> Memory CH08 -> POLYGON` по контрактам.
- Повторно использовать готовые узлы, не дублировать ALINA/FATHER_CORE.
- Негативные испытания: prompt injection, запрещённое действие, зависимость от неуспешного этапа, циклы, ограничение бюджета, потеря state, невалидный tool result.

### CH06-P5 — BENCHMARK / ADMISSION
- Сравнить `no-planner` и `planner` на одинаковом, заранее зафиксированном наборе задач и бюджете.
- Метрики: end-to-end success, verified success, plan validity, cost, elapsed time, retries, human interventions, safety violations.
- Полный отчёт с trace и hash; решение `ADOPT / CONDITIONAL / REJECT`.
- При отсутствии измеримого улучшения **не вводить** Planning Agent в производство.

## 4. Порядок выполнения

**Сейчас:** CH06-P0 → P1 → P2 → P3 → P4 → P5.  
**Затем:** закрыть пробелы CH01 и CH07, испытать лабораторию CH08, пройти CH09–CH21 по проверенному оглавлению. Дополнительно исправить неполную приёмку CH02–CH05.  
**После каждой главы:** обновить общий каталог паттернов и карту применения FATHER.

## 5. Ограничения и безопасность

- Не считать READMEs и программные примеры квалификацией.
- Строго отделять анализ содержания книги от собственных идей FATHER.
- Не хранить закрытые экзаменационные задания POLYGON в обучающей памяти.
- Не выполнять LLM-generated code без изоляции, лимитов и санкционирования.
- Сохранять human commits, ADR, контракты, SHA-256, provenance, SBOM и evidence; signed releases только при наличии разрешённого ключа.
