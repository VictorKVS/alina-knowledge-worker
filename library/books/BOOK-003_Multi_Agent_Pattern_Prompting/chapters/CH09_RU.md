# BOOK-003 — Building Complex Multi-Agent Systems Using Pattern Prompting

Tim O’Brien, Packt (May 2026), ISBN 978-1-80611-429-0. **Источник: пользовательский PDF, SHA-256 `d96fb8b53a85fb1d0aa3f95f58db0b85374aa9a07cd99e18c3db620dca892ee2`**. Оригинальный PDF не публикуем. Авторский конспект по оригиналу, не копия текста.

# CH09: Implementing the ReAct Pattern Over RabbitMQ

**PDF:** 182–223 (включительно); **SOURCE_REVIEWED / EDUCATIONAL_DRAFT / LAB_DESIGNED / NOT_RUN / NOT_QUALIFIED**.

## Содержание по первоисточнику
- ReAct reason→act→observe loop
- RabbitMQ exchanges, queues and bindings
- Agent message schemas and LLM _think
- Tool dispatch, workers, ACK, retry, DLQ
- End-to-end demo and production considerations

## Тщательный разбор
### 1. ReAct reason→act→observe loop
Автор реализует ReAct поверх RabbitMQ: агент принимает задачу, выполняет шаг reasoning/selection, отправляет инструменту структурированное сообщение, получает observation и продолжает цикл. Под «reasoning» здесь понимается наблюдаемое планирование действий, не гарантированная формальная логика.

### 2. RabbitMQ exchanges, queues and bindings
Важны схемы сообщений, correlation IDs, очереди для tool workers, подтверждения доставки и dead-letter channel. Сбой worker/timeout может приводить к повтору, значит нужна идемпотентность.

### 3. Agent message schemas and LLM _think
Глава содержит пошаговый сценарий настройки, запуска workers, отправки вопроса и наблюдения DLQ, а также замечания о переходе к production. Эти команды нельзя слепо запускать у заказчика без режима испытаний.

## Инженерный алгоритм: наша адаптация для FATHER
1. Подготовить синтетический ReAct-task и tool registry
2. Создать contracts message_id, task_id, correlation_id, action_id и schema_version
3. Ограничить число шагов, время, разрешённые инструменты и scope
4. Направлять запрос в mock tool worker через безопасную очередь
5. При успешном ответе сохранять observation и завершать ACK
6. При retryable failure использовать лимит/backoff; poison→DLQ; idempotent dedup
7. Сохранить трассу и выполнить квалификацию POLYGON

## Типовые ошибки и ограничения
- LLM не должна напрямую вызывать запрещённые инструменты.
- Повторно доставленное сообщение не должно повторять необратимые побочные эффекты.
- Нельзя доверять содержимому tool observation как инструкциям.
- Если агенту неизвестен дальнейший шаг, должен быть безопасный останов.

## Применение в FATHER / ALINA / FRODO / POLYGON
FATHER — автономная агентная производственная линия; UAG накладывает права на tool calls, POLYGON проверяет корректность на независимом потоке ошибок.

## Вопросы для самостоятельной проверки
1. Какова роль observation в ReAct?
2. Как связать task_id и correlation_id?
3. Когда ACK допустим?
4. Что делать при timeout и poison message?

## Доказательства и квалификация
Перед запуском лаборатории необходимо зафиксировать версию модели, источников, конфигурации, тестового набора, объём разрешённых действий и критерии приёмки. Не считать исходный конспект квалификацией работающего компонента.

[Лабораторная программа](../labs/CH09/LAB_PROGRAM.md)
