# BOOK-003 — Building Complex Multi-Agent Systems Using Pattern Prompting

Tim O’Brien, Packt (May 2026), ISBN 978-1-80611-429-0. **Источник: пользовательский PDF, SHA-256 `d96fb8b53a85fb1d0aa3f95f58db0b85374aa9a07cd99e18c3db620dca892ee2`**. Оригинальный PDF не публикуем. Авторский конспект по оригиналу, не копия текста.

# CH07: Tips and Best Practices

**PDF:** 134–151 (включительно); **SOURCE_REVIEWED / EDUCATIONAL_DRAFT / LAB_DESIGNED / NOT_RUN / NOT_QUALIFIED**.

## Содержание по первоисточнику
- R&D mindset; small POCs; latency and throughput
- Drift and non-determinism
- Security: injection, leakage, PII, output validation
- Token budgets and cost governance
- Prompt versioning, rollback, testing and red team

## Тщательный разбор
### 1. R&D mindset; small POCs; latency and throughput
Автор рекомендует практическое экспериментирование и короткие POC, ранние SLO/latency goals, тестирование под нагрузкой и управление drift. Это операционные правила на протяжении жизненного цикла.

### 2. Drift and non-determinism
Раздел безопасности описывает prompt injection, утечку через context window, PII, проверку выхода и отраслевые compliance-риски; для FRODO это карта защитных проверок.

### 3. Security: injection, leakage, PII, output validation
Промпты следует версионировать подобно коду, с владельцем, ревью и откатом. Недетерминированность LLM означает необходимость повторных оценок и достаточных выборок.

## Инженерный алгоритм: наша адаптация для FATHER
1. Задать security/privacy и cost budget до разработки
2. Определить POC, baseline и регулярную eval-сборку
3. Version prompts, models, corpus, tools, datasets и policy
4. Измерять latency, throughput, error rates, drift и затраты
5. Использовать red-team cases на разрешённой среде и review результатов

## Типовые ошибки и ограничения
- Не подключать сырой LLM-output напрямую к критическим IT-системам.
- Нельзя считать один удачный ответ статистическим подтверждением качества.
- Prompt version без версии model/data/tool не гарантирует воспроизводимость.

## Применение в FATHER / ALINA / FRODO / POLYGON
FATHER Trust & Competency Lab: ADR, signed releases, evidence, costs; FRODO — проверка prompt injection/PII в sandbox.

## Вопросы для самостоятельной проверки
1. Почему нужны многократные LLM-тесты?
2. Как версионировать промпты?
3. Чем SLO отличается от отдельной latency-пробы?
4. Как спланировать red-team испытание без доступа к чужой инфраструктуре?

## Доказательства и квалификация
Перед запуском лаборатории необходимо зафиксировать версию модели, источников, конфигурации, тестового набора, объём разрешённых действий и критерии приёмки. Не считать исходный конспект квалификацией работающего компонента.

[Лабораторная программа](../labs/CH07/LAB_PROGRAM.md)
