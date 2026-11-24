# DATA CONTRACT — Narrative Theory KB, v0.1

Each method card is JSON, text in Russian.

- `id`: stable `NAR-###`
- `name`: названия метода
- `task`: конкретный вопрос BOOK Agent
- `source_id`: `SRC-###` from sources.json
- `source_quality`: `PRIMARY_AUTHOR_TEXT` or `SECONDARY_DERIVED`
- `pdf_pages`: 1-indexed PDF page numbers, not printed page numbers
- `short_quote`: короткая дословная цитата на языке PDF; до 20 слов; отдельно перевод/объяснение
- `author_claim`: верная парафраза позиции автора, не наш алгоритм
- `engineering_algorithm`: **наш алгоритм** в виде шагов
- `required_inputs`: data contract для анализа
- `output_fields`: ожидаемые структурированные поля
- `applicability`: когда применять
- `limitations`: исключения и риск ложноположительных выводов
- `checks`: конкретные условия проверки и отрицательные примеры
- `status`: `SOURCE_REVIEWED / ALGORITHM_DRAFT / NOT_QUALIFIED` и т.п.

**Source references:** URL/внутренний идентификатор на исходный **пользовательский** файл, SHA-256 из sources.json, PDF страница. Не публиковать исходные тексты и не включать защищённые длинные примеры в README.

**Candidate application record:**
```json
{
  "method_id": "NAR-003",
  "target_work_id": "BOOK-0001",
  "evidence": [{"fragment_id":"F-012","quote":"...","offset_start":0,"offset_end":10}],
  "inference": {"finding": "reader question raised", "confidence": null},
  "review": {"claim_supported": false, "reason": "NOT_REVIEWED"}
}
```

`confidence` недопустимо трактовать как объективную вероятность без калибровки. Любой `PASS` требует как минимум фрагментов оригинальной анализируемой книги и независимого benchmark. UAG защищает права на инструменты и данные.
