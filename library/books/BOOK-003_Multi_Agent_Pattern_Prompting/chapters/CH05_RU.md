# BOOK-003 — Building Complex Multi-Agent Systems Using Pattern Prompting

Tim O’Brien, Packt (May 2026), ISBN 978-1-80611-429-0. **Источник: пользовательский PDF, SHA-256 `d96fb8b53a85fb1d0aa3f95f58db0b85374aa9a07cd99e18c3db620dca892ee2`**. Оригинальный PDF не публикуем. Авторский конспект по оригиналу, не копия текста.

# CH05: Starting Your Data Migration Project

**PDF:** 104–119 (включительно); **SOURCE_REVIEWED / EDUCATIONAL_DRAFT / LAB_DESIGNED / NOT_RUN / NOT_QUALIFIED**.

## Содержание по первоисточнику
- Document and data source inventory
- ETL tool evaluation
- Throughput/capacity and incremental updates
- Privacy, security, CI/CD and validation
- Hybrid search, data cleaning, graph databases

## Тщательный разбор
### 1. Document and data source inventory
Глава начинается с инвентаризации документов и оценки пригодности источников для ingestion. Полнота охвата, тип формата, права доступа и качество парсинга критичнее выбора красивой базы.

### 2. ETL tool evaluation
Автор разбирает ETL и планы непрерывной загрузки с лимитами пропускной способности, стоимостью, безопасностью и тестами; это длительный производственный процесс, а не одноразовая команда.

### 3. Throughput/capacity and incremental updates
Описываются ограничения чисто векторного извлечения, необходимость hybrid search и возможное использование графа знаний. Граф без подтверждения извлечённых отношений остаётся гипотезой.

## Инженерный алгоритм: наша адаптация для FATHER
1. Составить source inventory, owner/license/ACL, formats, revisions
2. Оценить объём, частоту изменений, throughput и expected cost
3. Разделить raw, parsed, cleaned, chunked и indexed datasets
4. Включить incremental sync, checksums, dedup и rollback
5. Измерить retrieval quality и проследить каждую запись к источнику

## Типовые ошибки и ограничения
- Не поглощать конфиденциальные документы в публичные обучающие наборы.
- Не объявлять все извлечённые связи графа достоверными.
- Игнорирование изменений/удалений документов создаёт устаревшую базу.

## Применение в FATHER / ALINA / FRODO / POLYGON
Прямое ядро исследовательской фабрики ALINA: source registry → ETL → verified KB; FRODO получает только разрешённую проекцию.

## Вопросы для самостоятельной проверки
1. Что должно войти в паспорт источника?
2. Как измерить ingestion throughput?
3. Как обработать новую редакцию документа?
4. Почему требуется hybrid retrieval?

## Доказательства и квалификация
Перед запуском лаборатории необходимо зафиксировать версию модели, источников, конфигурации, тестового набора, объём разрешённых действий и критерии приёмки. Не считать исходный конспект квалификацией работающего компонента.

[Лабораторная программа](../labs/CH05/LAB_PROGRAM.md)
