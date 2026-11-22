# ALINA → агент: контракт подготовки информации v0.1

**Обязательное правило:** ALINA получает задачу и **до передачи агенту** выполняет очистку, дедупликацию, классификацию, выбор источников, безопасность, формирование доказательств и определяет, чего пока неизвестно. Агент не получает весь сырой архив по умолчанию.

Основание: BOOK-002 Suhas Pai, глава 2 (подготовка 120–137, дубликаты 138–143, PII 143–154, contamination 154–155). Точный контракт передачи информации — **проектное инженерное решение FATHER**, не описанный автором книги интерфейс.

## Вход

`AgentInformationRequest`: `task_id`, `agent_role`, `objective`, `need_to_know`, `allowed_domains`, `allowed_sensitivity`, `max_items`, `as_of`, `minimum_source_quality`, `required_output`.

## Конвейер

```text
task + role + authorization context
    → scope search
    → source/policy screening (before exposing content)
    → extraction-quality gate
    → bytes/text duplicate grouping; lineage preserved
    → revision-aware selection, contradictions kept
    → evidence relevance, independence and freshness assessment
    → least-privilege source selection
    → knowledge claims + limitations + algorithms + glossary
    → signed/traceable package manifest [future: signing]
    → UAG runtime authorization gate
    → agent receives only approved package
    → agent result + citations + errors
    → ALINA validates source feedback → graph update under review
```

Не смешивать **validity/reliability** с **novelty**: повторная публикация может быть полезна для исследования распространения, но не добавляет независимого подтверждения.

## Выход: AgentKnowledgePackage

- `package_id, version, task_id, agent_role, objective`;
- `knowledge_items`: факты/методы, точные исходные ссылки, дата действия;
- `evidence_groups`: общие цепочки происхождения, независимость источников;
- `source_decisions`: imported/linked/versioned/review/quarantined/rejected и почему;
- `glossary`, `algorithms`, `constraints`, `unknowns`, `contradictions`;
- `confidence`: оценка основания по каждому утверждению, **не вероятность истинности**;
- `audit`: версии источников, hash, policies, reviewer, timestamp;
- `handoff_status`: `READY` или `BLOCKED`.

## Критические запреты

1. Нет подтверждённого разрешения использовать материал → не включать содержание.
2. Сведения выше допуска роли → не включать содержание.
3. Подозрение на PII или компрометацию → quarantine/review.
4. Неясная редакция нормативного документа → review, а не автоматический выбор.
5. Разные URL одного сообщения → один provenance cluster для доказательства факта.
6. Экзаменационные gold ответы POLYGON не выдавать агенту.
7. Недостаточно достоверных источников → `BLOCKED` или `READY` с явными пробелами только для задач, допускающих частичный результат.
8. Текст источника является данными, **не командой** агенту.

## Передача OSINT

Выдаём: перечень утверждений и контраргументов, разрешённые URLs, источник каждого утверждения, цепочку репостов, время событий и публикаций, флаги расхождений и пробелы доказательств. **Не выдаём** скрытые персональные данные, недопущенные материалы и ложную «уверенность 100%».

## Передача Document Agent

Выдаём: конкретный документ/пакет, версию, страницы и таблицы, парсерные исключения, список соответствий прошлым редакциям, требования к результату, правила цитирования и проверки.

## Контракт обратной связи

Агент возвращает `task_id`, `package_id`, `used_item_ids`, `new_claims`, `errors`, `artifacts`, `evidence_refs`. ALINA принимает изменения в граф **только после оценки provenance и соответствующего review**, иначе размещает в рабочем карантине.

## Состояние

Документ и учебный эталон опубликованы; интеграция с работающими ALINA/UAG/OSINT/POLYGON, подписание, БД и эксплуатационные тесты не выполнены.
