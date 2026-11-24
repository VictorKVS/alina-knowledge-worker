# CH05 — Tool Use / Function Calling — инженерный разбор FATHER

**Первоисточник:** Antonio Gulli, *Agentic Design Patterns*, глава 5, оригинальный PDF начиная с **страницы 77 файла**. Примеры LangChain — страницы 80–83, CrewAI — 83–86, Google ADK и прикладные сервисы — далее в этой главе. Сопоставлен пользовательский русский фрагмент «Практический пример кода (LangChain)» и продолжение (CrewAI/ADK/Vertex). Текст ниже — **собственная учебная переработка**, не републикация книги или перевода.

**Статус:** SOURCE_REVIEWED / ORIGINAL_ERRORS_IDENTIFIED / ADAPTED_CODE / OFFLINE_TESTS_DESIGNED / NOT_RUN / NOT_QUALIFIED.

## 1. Бизнес-задача — гайка и набор инструментов

Пользователь: «Открути гайку». Языковая модель **не откручивает гайку**. Она может предложить инструмент `unscrew_nut` с аргументами. Исполнительная программа проверяет полномочия, допустимое состояние и параметры и вызывает реальный адаптер только после разрешения. Для физической системы дополнительно необходимы безопасность оборудования, сенсоры и контроллер — LLM не является safety-critical контуром.

Учебный безопасный пример: «Умножь 125 на 48». LLM должна вернуть структурированный вызов `multiply(a=125,b=48)`; Python считает 6000; наблюдение возвращается модели; она пишет окончательный ответ. Второй инструмент `lookup_demo_fact` возвращает **статические** записи, не веб-поиск.

## 2. BPMN-проекция процесса

```text
Start(user_request)
   ↓
Task(Enumerate allowlisted tools, typed schemas)
   ↓
Task(LLM selects tool + arguments)
   ↓
XOR Gateway(tool requested?)
   ├── No → End(text response)
   └── Yes → Task(Validate name, args, actor scope)
                     ↓
                XOR Gateway(authorized?)
                   ├── No → End(DENIED)
                   └── Yes → Task(Execute allowlisted tool)
                                    ↓
                                 Task(Observe result)
                                    ↓
                                 Task(Append ToolMessage)
                                    ↓
                             XOR Gateway(step limit?)
                                ├── Within limit → LLM
                                └── Exceeded → End(LIMIT_REACHED)
```

**Модель предлагает вызов, но не исполняет его самостоятельно.** Паттерн не равен фактической выдаче прав.

## 3. Контракт блоков

| Компонент | Input → output | Ответственность |
|---|---|---|
| ModelAdapter | env/model → BaseChatModel | выбор провайдера, не выбор полномочий |
| Tool Registry | `tool_name/schema` → allowlist | декларации функций и их форматов |
| Tool Calling LLM | `user+tool_descriptions` → `tool_calls[]` | предложение действий |
| Schema Gate | `name,args` → valid/invalid | проверка типов и диапазонов |
| UAG (будущее) | `actor,resource,action,context` → allow/deny | независимая авторизация |
| Tool Executor | validated call → typed result | исполнение выбранного безопасного инструмента |
| Observation | output/error → ToolMessage | передача результата обратно LLM |
| Iteration Controller | history,step,count → continue/stop | исключение бесконечного цикла |

## 4. Что показывает оригинал

### LangChain (PDF 80–83)
`@tool` определяет инструмент `search_information` со статической таблицей ответов. В исходном коде используется Gemini `gemini-2.0-flash`, `create_tool_calling_agent`, `AgentExecutor`, а запросы группируются через `asyncio.gather`. Это **имитация поиска информации**, не реальный live weather provider.

### CrewAI (PDF 83–86)
Финансовый агент получает `get_stock_price` со значениями тикеров из словаря. Значения **симулированы**, не текущие котировки. `Agent,Task,Crew` описывают роль, задачу и оркестрацию; `allow_delegation=False` не превращает Crew в распределённую многоагентную систему.

### Google ADK (в предоставленном русском фрагменте)
Показаны `google_search`, `BuiltInCodeExecutor`, работа сессий `Runner/InMemorySessionService`, поиск Vertex AI и Extensions. Это **разные классы средств**, не аналогичные по риску: доступ к вебу, исполнение кода, чтение корпоративных данных и бизнес-операции требуют различных разрешений.

## 5. Ошибки и важные поправки по предоставленным примерам

1. **Устаревающие API LangChain.** `create_tool_calling_agent`/`AgentExecutor` относятся к старому API LangChain; для современной реализации используем прямой `llm.bind_tools` и управляемый цикл с `ToolMessage`. Не утверждать, что старые API одинаково работают во всех версиях.
2. **Лишняя аутентификация:** Gemini-пример запрашивает сразу `GOOGLE_API_KEY` и `OPENAI_API_KEY`, хотя подключённый `ChatGoogleGenerativeAI` требует только нужный ключ Google. При Ollama ключи не нужны.
3. **Ложная актуальность:** запись `weather in london: 15°C` и фиксированные котировки не должны маркироваться current/latest. Неизвестный запрос должен давать `NOT_FOUND`, а не убедительный выдуманный «результат поиска».
4. **Проверка модели:** не любая LLM качественно поддерживает `tool_calls`. Проверять tool-calling отдельно для `ministral-3:8b` и `qwen3:8b`. Обычный ответ текстом — не исполнение инструмента.
5. **Google ADK ошибка имён:** пример `root_agent = ADKAgent(...)` содержит импорт `Agent`, но в показанном фрагменте нет определения `ADKAgent`. Должно использоваться одно согласованное имя.
6. **Асинхронность ADK:** не смешивать синхронный `Runner.run` и async `Runner.run_async`; `nest_asyncio` для отдельного `python script.py` не нужен.
7. **CrewAI:** демонстрационная цена не является реальной рыночной ценой; `OPENAI_API_KEY` в приведённом примере — конфигурация по умолчанию, а не требование паттерна.
8. **Code Execution:** результат LLM нельзя без контроля выполнять на основной машине. Нужны sandbox, resource/time limits, filesystem/network isolation, независимая верификация. Наша лаборатория **не исполняет сгенерированный Python**.
9. **UAG/Policy:** tool schema и `bind_tools` не авторизуют действия — это отдельный слой.

## 6. Исправленный учебный пример

[examples/ch05_tool_use.py](../examples/ch05_tool_use.py):
- **Provider-neutral** — общий `model_adapter.py`, Ollama/OpenAI/Gemini/Anthropic/OpenAI-compatible;
- `@tool lookup_demo_fact`, `@tool multiply` — только чтение фиксированного набора данных и вычисление;
- LLM возвращает список `tool_calls`, программа сверяет имена с allowlist, проверяет аргументы инструментом и добавляет `ToolMessage`;
- максимум 3 раунда выбора, 4 инструментальных вызова, явные статусы `COMPLETED/DENIED/LIMIT_REACHED/INVALID_TOOL_CALL`;
- по результату `COMPLETED` обязательно смотреть `trace` — модель могла ответить без вызова инструментов, и такой ответ **не доказывает Tool Use**.

## 7. Выбор уровня реализации

**Уровень A:** программа сама выбирает `multiply` без LLM, 20–30 строк.  
**Уровень B:** одна LLM + 2 проверенных инструмента + 1 Python процесс + trace.  
**Уровень C:** FATHER: Tool Registry + UAG + typed envelopes + audit + отдельные сервисы/queues при необходимости + POLYGON.

Практика: не превращать простой калькулятор в отдельный сервер без подтверждённой необходимости. Одинаковый `ToolPort` интерфейс может реализовываться и Python-функцией, и HTTP сервисом.

## 8. Недостающая независимая квалификация

Для `multiply(125,48)` проверять `trace` с фактическим вызовом и наблюдением, а не только ответ `6000`. Отдельно проверять отсутствие вызовов неразрешённых инструментов, пустые/неверные аргументы, лимиты, сбои моделей и повторные вызовы.

Полный контроль FATHER: human commits, ADR, contracts, SHA-256/provenance, evidence, signed release, SBOM. Все стадии пока **NOT_QUALIFIED**.

## 9. Запуск PowerShell

```powershell
Set-Location 'G:\1\alina-knowledge-worker'
git pull --ff-only
Set-Location '.\library\books\LIB-0040_Agentic_Design_Patterns'
$env:AGENT_LLM_PROVIDER = 'ollama'
$env:AGENT_LLM_MODEL = 'ministral-3:8b'
python .\examples\ch05_tool_use.py
python -m unittest discover -s tests -p 'test_ch05_tool_use.py' -v
```
