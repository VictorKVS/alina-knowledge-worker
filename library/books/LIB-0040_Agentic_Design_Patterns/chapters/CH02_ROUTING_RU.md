# CH02 — Routing / Маршрутизация

**Книга:** Antonio Gulli, *Agentic Design Patterns*. **Оригинал:** пользовательский PDF, страницы 34–47 (PDF file page counter). **SOURCE_REVIEWED / CODE_CORRECTED / LAB_DESIGNED / NOT_RUN**.

## 1. Бизнес-постановка

Оператор отправляет задачу системе. По содержанию нужно передать её одному из специализированных исполнителей, не предоставляя неопределённые полномочия модели. Паттерн **Routing** отвечает за выбор пути, не за само выполнение бизнес-операции.

**Текстовая BPMN-модель:** Start(User request) → Task(Classify intent) → Exclusive Gateway(valid category?) → Task(Invoke selected handler) / Task(Ask for clarification) → Task(Validate response) → End. Ветви — взаимоисключающие; классификатор не авторизует реальные действия.

## 2. Блоки и данные

| Блок | Назначение | Вход → выход |
|---|---|---|
| User/API | Приём сообщения | `request:str` → `request_id,request` |
| LLM Router | Классификация в `booker, info, unclear` | `request` → `label` |
| Validator | Проверка известного значения | `label` → `validated_label` |
| RunnableBranch | Ветка по категории | `validated_label,request` → worker |
| Simulated Handler | Учебный ответ (без бронирования) | `request` → `result` |
| Audit (FATHER extension) | Trace и ошибки | `request_id,route,result` → `event` |

В оригинале (PDF 37–40) дана LangChain-демонстрация с `RunnableBranch` и тремя **симулированными обработчиками**, а на PDF 40–46 — пример Google ADK с coordinator/sub-agents.

## 3. Отличия учебного исправления

1. Модель не объявляется исполнителем: Python handler не осуществляет бронирование.
2. Отсутствующий API-ключ выявляется **до** создания LLM.
3. `ChatGoogleGenerativeAI` создаётся в `main`, поэтому не возникает сломанных цепочек при `llm=None`.
4. Label нормализуется; всё неизвестное направляется в `unclear`; prompt injection и ошибки модели не получают полномочия.
5. `RunnablePassthrough.assign` сохраняет исходный `request` без двойного вложения `x["request"]["request"]`.
6. Текст о квантовой физике — информационный запрос, **не** пример `unclear`, поскольку правило относит общие вопросы к `info`.

## 4. От простого к сложному

**A / 20 строк:** `if/elif/else` в Python, без LLM.  
**B / LangChain:** LLM классифицирует, `RunnableBranch` выбирает из функций.  
**C / FATHER:** Router вызывает квалифицированного специалиста по contract, UAG проводит авторизацию инструмента, POLYGON проверяет качество маршрутизации и исходы ошибок.

При увеличении нагрузки выделяем отдельные сервисы, при необходимости API/queue и idempotency; сами функции и их контракты остаются понятными.

## 5. Запуск учебной версии

```powershell
python -m pip install langchain-core langchain-google-genai
$env:GOOGLE_API_KEY="YOUR_KEY"
python examples/ch02_router.py
```

Только симулированные handlers. Коммерческую интеграцию и работу с чужими данными код не выполняет. **API-вызовы и POLYGON не запускались**.

[Python](../examples/ch02_router.py) · [Лаборатория](../labs/CH02/LAB_PROGRAM.md).
