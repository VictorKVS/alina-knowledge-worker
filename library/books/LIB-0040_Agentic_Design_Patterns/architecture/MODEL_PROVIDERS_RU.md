# FATHER ModelAdapter — одна агентная логика, разные LLM

**LIB-0040 / Antonio Gulli — CH02 Routing, CH03 Parallelization** · *наше расширение FATHER, не код автора*. **CODE_DESIGNED / UNIT_TESTS_PENDING / PROVIDER_E2E_NOT_RUN / POLYGON_NOT_QUALIFIED**.

## Главный принцип

Агент вызывает **LangChain BaseChatModel interface**, а конкретную модель создаёт `model_adapter.create_chat_model(ModelConfig)`. Код маршрутизатора, параллельной ветки, промпты, контракты данных и обработчики от выбора провайдера не меняются.

`Input → Router/Parallel Pattern → BaseChatModel (Adapter) → Ollama|OpenAI|Gemini|Anthropic|OpenAI-compatible → Output`.

**«Любая» означает модель с поддерживаемым адаптером или совместимым API**, а не произвольную бинарную модель без сервера/API. Функции tool-calling, structured output, streaming и JSON mode доступны не у каждой модели: для них требуются отдельные capability tests.

## Параметры

| Переменная | Описание | Пример |
|---|---|---|
| `AGENT_LLM_PROVIDER` | `ollama`, `openai`, `gemini`, `anthropic`, `openai-compatible` | `ollama` |
| `AGENT_LLM_MODEL` | Имя конкретной модели | `ministral-3:8b` |
| `AGENT_LLM_BASE_URL` | URL кастомного endpoint | `http://127.0.0.1:11434` |
| `AGENT_LLM_API_KEY` | Ключ OpenAI-compatible endpoint | secret |
| `AGENT_LLM_TEMPERATURE` | Температура, по умолчанию 0 | `0` |
| `AGENT_LLM_TIMEOUT` | Таймаут в секундах (для ChatOpenAI) | `45` |

Cloud native: `OPENAI_API_KEY` для OpenAI, `GOOGLE_API_KEY` для Gemini, `ANTHROPIC_API_KEY` для Anthropic. Секреты никогда не коммитить в Git.

## Запуск 1: локально, Ollama, без облачного API

```powershell
python -m pip install langchain-core langchain-ollama
ollama list
$env:AGENT_LLM_PROVIDER="ollama"
$env:AGENT_LLM_MODEL="ministral-3:8b"
python examples/ch02_router.py
python examples/ch03_parallelization.py
```

При необходимости `ollama serve` запускается отдельно. Модель должна уже быть загружена. Не нужно подключать Google/OpenAI.

## Запуск 2: OpenAI

```powershell
python -m pip install langchain-core langchain-openai
$env:AGENT_LLM_PROVIDER="openai"
$env:AGENT_LLM_MODEL="gpt-4o-mini"
$env:OPENAI_API_KEY="<secret>"
python examples/ch02_router.py
```

## Запуск 3: Gemini

```powershell
python -m pip install langchain-core langchain-google-genai
$env:AGENT_LLM_PROVIDER="gemini"
$env:AGENT_LLM_MODEL="gemini-2.5-flash"
$env:GOOGLE_API_KEY="<secret>"
python examples/ch02_router.py
```

## Запуск 4: Anthropic

```powershell
python -m pip install langchain-core langchain-anthropic
$env:AGENT_LLM_PROVIDER="anthropic"
$env:AGENT_LLM_MODEL="claude-sonnet-4-5"
$env:ANTHROPIC_API_KEY="<secret>"
python examples/ch02_router.py
```

## Запуск 5: LM Studio / llama.cpp / vLLM / другое OpenAI-compatible API

```powershell
python -m pip install langchain-core langchain-openai
$env:AGENT_LLM_PROVIDER="openai-compatible"
$env:AGENT_LLM_MODEL="my-local-model"
$env:AGENT_LLM_BASE_URL="http://127.0.0.1:1234/v1"
python examples/ch02_router.py
```

Для удалённого сервиса используем HTTPS и `AGENT_LLM_API_KEY`. Использование ChatOpenAI с совместимым API не гарантирует поддержку vendor-specific extension. При наличии официальной LangChain-интеграции конкретного вендора она предпочтительнее. Не используйте placeholder в удалённом контуре.

## Контроль качества

В `tests/test_model_adapter.py` — полностью офлайновые тесты config validation. Отдельно для каждого провайдера нужны:
- `healthcheck`: API доступен, модель существует;
- `router_benchmark`: label accuracy, invalid-label/abstain;
- `parallel_benchmark`: все три ветви завершаются, соблюдаются timeout/rate limits;
- `security`: никакие вызовы за пределами UAG/scope, нет утечки secrets;
- `POLYGON`: независимые тесты после freeze версии model/prompts/adapters.

Замена модели не является доказательством эквивалентности поведения: каждый новый provider/model должен пройти собственный квалификационный прогон.
