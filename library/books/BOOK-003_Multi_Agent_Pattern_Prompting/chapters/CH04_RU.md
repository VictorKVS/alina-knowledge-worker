# BOOK-003 — Building Complex Multi-Agent Systems Using Pattern Prompting

Tim O’Brien, Packt (May 2026), ISBN 978-1-80611-429-0. **Источник: пользовательский PDF, SHA-256 `d96fb8b53a85fb1d0aa3f95f58db0b85374aa9a07cd99e18c3db620dca892ee2`**. Оригинальный PDF не публикуем. Авторский конспект по оригиналу, не копия текста.

# CH04: Building Your First RAG App

**PDF:** 80–103 (включительно); **SOURCE_REVIEWED / EDUCATIONAL_DRAFT / LAB_DESIGNED / NOT_RUN / NOT_QUALIFIED**.

## Содержание по первоисточнику
- Meaning of production-grade software
- Queues, topics and RabbitMQ
- EIP patterns for a production RAG pipeline
- LLM client: Template Method, Adapter, Strategy
- Deployment configuration

## Тщательный разбор
### 1. Meaning of production-grade software
Автор рассматривает production-grade не как факт наличия модели, а как набор свойств безопасности, надёжности, эксплуатационной пригодности, тестируемости и совместимости. Таблица на PDF стр. 82 описывает эти свойства.

### 2. Queues, topics and RabbitMQ
RabbitMQ вводится для разделения производящих и потребляющих компонентов, буферизации, маршрутизации и восстановления после отказов; узлы не должны рассчитывать на идеальное поведение LLM endpoint.

### 3. EIP patterns for a production RAG pipeline
LLM-клиент проектируется через Template Method, Adapter и Strategy, позволяющие заменить поставщика или способ отправки без переписывания конвейера.

## Инженерный алгоритм: наша адаптация для FATHER
1. Определить границы RAG: ingest, retrieve, generate, verify
2. Выбрать очереди, routing key, contract и correlation ID
3. Сделать адаптер LLM поставщика и стратегию retry/timeout
4. Проверить ACK/DLQ, idempotency и поведение при отключении модели
5. Задокументировать SLO, версию манифеста и rollout

## Типовые ошибки и ограничения
- Очередь не гарантирует exactly-once без дополнительного контроля побочных эффектов.
- Нельзя ACK до успешного завершения бизнес-обработки.
- Манифест инфраструктуры не доказывает production readiness.

## Применение в FATHER / ALINA / FRODO / POLYGON
FATHER может применить этот паттерн к передаче задания ALINA→worker→verifier, но RabbitMQ вводим только при доказанной потребности.

## Вопросы для самостоятельной проверки
1. Какие свойства определяют production-grade?
2. Чем полезны Adapter и Strategy для LLM?
3. Для чего нужны correlation ID и DLQ?
4. Почему в RabbitMQ важны ACK и idempotency?

## Доказательства и квалификация
Перед запуском лаборатории необходимо зафиксировать версию модели, источников, конфигурации, тестового набора, объём разрешённых действий и критерии приёмки. Не считать исходный конспект квалификацией работающего компонента.

[Лабораторная программа](../labs/CH04/LAB_PROGRAM.md)
