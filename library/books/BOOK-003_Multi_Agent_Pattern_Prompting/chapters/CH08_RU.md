# BOOK-003 — Building Complex Multi-Agent Systems Using Pattern Prompting

Tim O’Brien, Packt (May 2026), ISBN 978-1-80611-429-0. **Источник: пользовательский PDF, SHA-256 `d96fb8b53a85fb1d0aa3f95f58db0b85374aa9a07cd99e18c3db620dca892ee2`**. Оригинальный PDF не публикуем. Авторский конспект по оригиналу, не копия текста.

# CH08: Pattern-Guided Coding: Using Patterns as the Design Vocabulary for GenAI Systems Built on RabbitMQ

**PDF:** 152–181 (включительно); **SOURCE_REVIEWED / EDUCATIONAL_DRAFT / LAB_DESIGNED / NOT_RUN / NOT_QUALIFIED**.

## Содержание по первоисточнику
- Shared pattern vocabulary for coding agents
- Topologos four-phase iterative approval
- RabbitMQ producers/consumers: Strategy, Command, Template Method, Adapter
- Manual ACK and multi-tier DLQ
- Single RAG → dual-LLM Scatter-Gather case study

## Тщательный разбор
### 1. Shared pattern vocabulary for coding agents
Глава вводит Pattern-Guided Coding (PGC): точная терминология GoF/EIP помогает передавать архитектурные требования кодовым агентам и снижать неявность решений. Это метод инженерного общения, не доказанная автоматическая гарантия корректности.

### 2. Topologos four-phase iterative approval
Topologos разделяет design pattern layer и RabbitMQ topology. Процедура Clarification → Pattern Analysis → Iterative Approval → Final Output задаёт явное согласование решения до генерации артефактов.

### 3. RabbitMQ producers/consumers: Strategy, Command, Template Method, Adapter
На примере single-LLM RAG → dual-LLM Scatter-Gather показывается, как меняются exchanges/queues/aggregator и остаются прежними некоторые инварианты маршрутизации. Корреляционное окно агрегатора требует отдельного контроля.

## Инженерный алгоритм: наша адаптация для FATHER
1. Описать requirement, role map и messaging constraints
2. Разложить решение на GoF, EIP и reliability patterns
3. Зафиксировать каждое решение с Approve/Modify/Reject
4. Сгенерировать конфигурацию, диаграммы, security и DLQ manifests
5. Проверить schema, binding/routing, multi-tenancy и failure modes
6. Разрешать deployment только после внешнего approval и квалификации

## Типовые ошибки и ограничения
- Команды Topologos — команды шаблона, не встроенные команды RabbitMQ.
- Нельзя автоматически считать сгенерированный YAML корректным.
- Aggregated result нельзя принимать до проверки correlation ID, timeout и неполного набора ответов.

## Применение в FATHER / ALINA / FRODO / POLYGON
Это прямой кандидат для Agent Factory и Block Matcher: описание цепочки из проверенных паттернов → генерируемый, но обязательно проверяемый контракт.

## Вопросы для самостоятельной проверки
1. Четыре фазы Topologos?
2. Зачем Pattern-Guided Coding?
3. Как работает Scatter-Gather?
4. Как не допустить двойного исполнения после retry?

## Доказательства и квалификация
Перед запуском лаборатории необходимо зафиксировать версию модели, источников, конфигурации, тестового набора, объём разрешённых действий и критерии приёмки. Не считать исходный конспект квалификацией работающего компонента.

[Лабораторная программа](../labs/CH08/LAB_PROGRAM.md)
