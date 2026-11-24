# ALINA Narrative Theory KB — литературная база знаний и исполняемых методик

**Проект FATHER / ALINA, основан 2026-11-24.** Это отдельный проект **внутри существующего GitHub-репозитория** `alina-knowledge-worker`; новый независимый GitHub repository не создавался.

## Миссия

Превратить литературу о сценаристике, композиции, сценах и психологии персонажей в **систему проверяемых алгоритмов**, пригодных для BOOK Agent (анализ произведения) и Game Narrative Agent (сюжеты/квесты). Цель — не пересказ, а воспроизводимый `источник → метод → алгоритм → тест → оценка`.

## Первоначальные материалы

| ID | Работа | Полученный файл | Аудит | Статус |
|---|---|---|---|---|
| SRC-001 | John Truby, «Анатомия истории» (русский текст) | `rwrfw3.pdf` | 432 стр., авторский текст перевода | VERIFIED_IDENTITY / PARTIALLY_REVIEWED |
| SRC-002 | K.M. Weiland, *Structuring Your Novel* | `_OceanofPDF.com_...pdf` | 208 стр., англоязычный авторский текст | VERIFIED_IDENTITY / PARTIALLY_REVIEWED |
| SRC-003 | Robert McKee, *Story*, Part 3 | `robert-mckee-story-part3.pdf` | 183 стр., **только часть 3**, главы 7–13 | VERIFIED_IDENTITY / PARTIALLY_REVIEWED |
| SRC-004 | Weiland: infographic by Matt Gemmell | `structuring_your_novel_chart.pdf` | 2 стр., **производная схема**, автор Matt Gemmell | VERIFIED_IDENTITY / CHART_REVIEWED |
| SRC-005 | Lisa Cron, *Story Genius* (пересказ Bookey) | `story-genius.pdf` | 169 стр., автор текста **Bookey**, не книга Lisa Cron | SECONDARY_SUMMARY / NOT_PRIMARY |
| SRC-006 | Shawn Coyne, *The Story Grid* (пересказ Bookey) | `the-story-grid.pdf` | 117 стр., **пересказ Bookey**, не авторский текст Coyne | SECONDARY_SUMMARY / NOT_PRIMARY |

**Права:** пользовательские PDF не публикуем, не копируем главы или большие фрагменты на GitHub. Сохраняем метаданные, SHA-256, PDF-page, краткую точную цитату и **собственную инженерную интерпретацию**. Заявление о наличии этих файлов не означает права на их распространение.

## Библиотека алгоритмов

| ID | Метод | Источник | Продукт |
|---|---|---|---|
| NAR-001 | Семь этапов истории | SRC-001, PDF стр. 41–43 | карта сюжетного развития |
| NAR-002 | От замысла к изменению героя | SRC-001, PDF стр. 19–20, 35–36 | аналитика внутренней арки |
| NAR-003 | Hook: читательский вопрос | SRC-002, PDF стр. 13–17 | диагностика начала книги |
| NAR-004 | Цель → конфликт → поворот в сцене | SRC-003, PDF стр. 102–103 (печатные стр. 233–234) | проверка динамики сцены |
| NAR-005 | Сопоставление структурных вех | SRC-004, PDF стр. 1–2 | структурная карта, **не жесткий норматив** |

Подробности: [cards/](cards/), [структура БЗ](DATA_CONTRACT.md), [каталог](sources.json).

## Инварианты

1. Каждая карточка содержит тип знания, краткую цитату, PDF страницу и метку `PRIMARY_AUTHOR_TEXT` / `SECONDARY_DERIVED`.
2. Оригинальная **методика автора** и **наш алгоритм реализации** помечены отдельно.
3. Методы сценаристики — практические эвристики, **не универсальные законы**. Возражения между авторами храним, не «сводим к одному истинному».
4. `BOOK_AGENT.analysis` читает исходный роман и ссылается на **сам роман**, а `THEORY_KB` объясняет метод. Нельзя подтверждать события романа страницами теоретической книги.
5. `DESIGNED` ≠ `TESTED` ≠ `QUALIFIED`: в текущем коммите карточки и локальные validator tests подготовлены; реальные испытания BOOk Agent не проводились.

## Pipeline

```text
private PDF → source registry → page/fragment capture → quotation check
→ knowledge claim → author-method interpretation → our algorithm
→ positive/negative example → machine schema validation
→ manually labeled literary text → precision/recall assessment
→ POLYGON held-out stories → admission to Agent Factory
```

## Запуск в PowerShell

```powershell
Set-Location 'G:\1\alina-knowledge-worker'
git fetch origin
git switch feature/father-book-library-index-20261122
git pull --ff-only
python .\projects\ALINA_NARRATIVE_THEORY_KB\validate.py
```

Валидация проверяет структуру записей и обязательные evidence, **но не фактическую достоверность литературоведческих выводов**. Для этого нужна ручная проверка первоисточника и benchmark.

## Последующая работа

Последовательно проходить каждую главу всех авторских текстов, собирать новые карточки, увеличивать тестовый корпус, проверять качество распознавания на незнакомых рассказах. Пересказы Bookey использовать только как указатели на темы, без выдачи их за первоисточник.
