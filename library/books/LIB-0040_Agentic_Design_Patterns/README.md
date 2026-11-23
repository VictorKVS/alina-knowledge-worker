# LIB-0040 / Agentic Design Patterns — Antonio Gulli

**Книга:** *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems* — Antonio Gulli. Полный PDF предоставлен владельцем библиотеки. В оригинале 21 глава (паттерн на главу) и приложения; PDF содержит 458 страниц.

**Оригинальный пользовательский PDF:** SHA-256 `6a5ba08eb8d745a1109f739cf4fb8830b8fac8452c05a68d2349d2dab1ff58dd`; файл не выкладывается в репозиторий, не копируется на публичные серверы.

**Внешний русский перевод:** [TaiPanCy / agentic-design-patterns-book-rus](https://github.com/TaiPanCy/agentic-design-patterns-book-rus). [Глава 8 «Управление памятью»](https://github.com/TaiPanCy/agentic-design-patterns-book-rus/blob/main/%D0%A7%D0%B0%D1%81%D1%82%D1%8C%202/%D0%93%D0%BB%D0%B0%D0%B2%D0%B0%208.%20%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%D1%8E.md). Репозиторий перевода не имеет явно указанной лицензии в GitHub metadata при проверке 2026-11-23; права на републикацию перевода не подтверждены. Не копировать полный текст ни оригинала, ни перевода.

## Что подготовлено

- [Глава 8 — собственный инженерный разбор FATHER](chapters/CH08_MEMORY_MANAGEMENT_RU.md), по оригиналу PDF 130–151 и сопоставлению с русским переводом.
- [Memory Block Contract](architecture/MEMORY_BLOCK_CONTRACT_RU.md): назначение, интерфейсы, схемы, отказоустойчивость, tenant isolation.
- [Лаборатория A/B/C](labs/CH08/LAB_PROGRAM.md): от простой session memory до масштабирования и POLYGON.
- [Реестр источников](sources.json): оригинал PDF, проверенный внешний перевод и ограничения авторских прав.

**Состояние:** `CH08_SOURCE_REVIEWED / STUDY_CREATED / LAB_DESIGNED / NOT_RUN / NOT_QUALIFIED`. Остальные 20 глав не объявляются изученными: предусмотрен дальнейший последовательный разбор всей книги.

## Отношение к FATHER

Одна общая память/KB в ALINA, а у FRODO, TIMA и других агентов — отдельные разрешённые представления знаний, сессии, рабочее состояние и собственные политики долговременного хранения. Память — данные, но не полномочия на tool-use. Закрытые экзаменационные задания POLYGON не сохраняются в обучающую память.

