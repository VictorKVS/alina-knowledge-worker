# CH04 — Reflection / Рефлексия (Generator–Critic)

**Источник:** Antonio Gulli, *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems*, пользовательский PDF **страницы файла 63–76**. Ключевые места: определение и роли 63–64; области применения 65–66; авторский LangChain-код 67–70; ADK 70–71; ограничения и рисунки 71–75.

**Происхождение:** термины и учебный сценарий — из книги; проверки и компоненты FATHER ниже — наше проектное дополнение. **SOURCE_REVIEWED / ADAPTED_CODE / LAB_DESIGNED_ONLY / API_NOT_TESTED / POLYGON_NOT_QUALIFIED**.

## 1. Что исправляет паттерн

Первый ответ генератора может быть неверным. В отличие от Chaining (строгая последовательность) и Routing (выбор пути), **Reflection** создаёт обратную связь: `Generate → Critique → Revise → Critique...`.

В оригинале выделены два подхода: (1) один агент рецензирует себя, (2) **Producer–Critic** — логически разные роли. Их можно вызвать последовательно на одной модели с различными системными промптами. Это **не обязательно два независимых LLM-процесса** и не равнозначно внешней объективной экспертизе.

## 2. Бизнес-процесс и шлюзы (BPMN-проекция)

```text
[Start: задача + критерии]
          |
       Producer ──> Draft v1
          |           |
          |        Critic
          |           |
          +---< Gateway: улучшать? >---+
          |                             |
   [pass/advisory]                  [revise]
          |                             |
 External Validator           Feedback → Producer
          |                             |
  [requirements met?]     [iteration >= max?] --yes--> REVIEW_REQUIRED
          |
  Verified Result / REVIEW_REQUIRED
```

Невозможность получить положительный ответ за ограниченное число итераций означает **неуспешную квалификацию**, а не бесконечный цикл. Авторский код останавливается по `CODE_IS_PERFECT` или лимиту 3 итераций (стр. 68–69).

## 3. Инженерные блоки

| Компонент | Вход → выход | Ответственность |
|---|---|---|
| Task Contract | requirements → constraints | фиксировать ожидаемое поведение |
| Producer | task, previous, feedback → candidate | создавать новую версию |
| Critic | task, candidate → critique | находить вероятные ошибки |
| Iteration Controller | state + advisory verdict → next action | max_cycles, лимиты и останов |
| Deterministic Checker | candidate → syntax/schema outcome | проверка без доверия к оценке LLM |
| Test Runner (отдельный контур) | sandboxed candidate + fixtures → evidence | фактическая проверка поведения |
| POLYGON (внешняя квалификация) | frozen version + holdout → pass/fail | скрытые независимые задания |

## 4. Авторский пример: факториал

Гулли демонстрирует задачу генерации функции `calculate_factorial(n)` с `0! = 1`, отрицательные значения должны давать `ValueError`, функция должна иметь docstring (стр. 67–69).

Авторский LangChain пример использует GPT-4o, `message_history` и максимум 3 цикла. Модель-критик сообщает `CODE_IS_PERFECT` или формирует замечания. Второй вариант (Google ADK) демонстрирует `SequentialAgent` из Writer и Reviewer с ключами состояния `draft_text` и `review_output` (стр. 70–71).

## 5. Наши исправления

1. **Provider-independent:** `create_chat_model(ModelConfig.from_env())`, одна логика для Ollama, Gemini, OpenAI, Anthropic, OpenAI-compatible.
2. **No untrusted execution:** генерация Python кода не даёт ему права запускаться. AST разбирает синтаксис, проверяет top-level имя, **не правильность алгоритма**.
3. **No false PASS:** даже точный сигнал `CRITIQUE_PASS` остаётся рекомендацией. Итог упражнения — `REVIEW_REQUIRED`, пока независимые тесты не предоставят доказательство.
4. **Bounded cycles:** максимум 3, журнал всех версий и критики, без безграничного накопления context.
5. **No API secrets in prompts/logs:** не сохранять токены провайдеров или конфиденциальные данные в отчёт.
6. **Structured evidence:** результат формируется JSON-файлом с версиями кода и замечаний; для реальной аттестации необходимы отдельные isolated functional tests.

## 6. Как это связано с FATHER

- ALINA Producer: создаёт утверждение/код/краткое описание из источника; Critic ищет пропуски, затем внешний **Evidence Checker** сравнивает с исходной страницей.
- FATHER_CODEX Producer: генерирует функцию; Critic даёт review, но acceptance определяется тестами, security baseline и human commit.
- POLYGON: независим от обучающего feedback, holdout не становится долговременной памятью агента.
- UAG: контролирует, может ли агент исполнять инструменты; замена промпта не даёт новых полномочий.

## 7. Риски

| Риск | Проектная мера |
|---|---|
| Producer и Critic повторяют общую ошибку | separate model/criteria и независимые тесты |
| Infinite reflection | max_cycles и бюджет токенов |
| «Код идеален» без тестов | always `REVIEW_REQUIRED` до внешних evidence |
| Сбой генерации/ревью | явный `ERROR`, журнал, retry policy |
| Контекст растёт с каждой итерацией | ограниченный state с предыдущей версией |
| Prompt injection в candidate | трактовать candidate как untrusted data |
| Подмена tool permissions | UAG отдельно от LLM |

## 8. Установка и запуск

```powershell
python -m pip install langchain-core langchain-ollama
$env:AGENT_LLM_PROVIDER = "ollama"
$env:AGENT_LLM_MODEL = "ministral-3:8b"
python examples/ch04_reflection.py
python -m unittest discover -s tests -p "test_ch04_reflection.py" -v
```

Код **не выполняет** функцию факториала, полученную от модели. Отчёт записывается локально в `reflection_output.json`; не считать его тестовым PASS.

## 9. Вопросы для инженера

1. Что отличает Reflection от просто двух последовательных вызовов LLM?
2. Почему два промпта одной модели не дают независимой фактической проверки?
3. Когда критика полезна, а когда лучше вызвать валидатор с эталоном?
4. Что остановит цикл, если модель всегда просит «исправить»?
5. Какая информация нужна для воспроизводимого испытания у POLYGON?
