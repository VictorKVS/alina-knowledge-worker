# ALINA graph contract v0.1

## Stable IDs

`B002-{KEY}` идентификаторы для источниковых понятий; `ROLE-{NAME}` для представлений ролей. Узел имеет source, page-span, kind, origin, status, version, owner.

## Weights

- **Importance:** 1–5, редакционная важность для обучения агентов.
- **Confidence:** 0–1, оценка покрытия определений первоисточником; `null` для предложенных компонентов FATHER.
- **Edge weight:** 0–1, проектная релевантность связи. Не математическая вероятность, не параметр LLM.
- Любое изменение веса требует `weight_change_reason` и версии.

## Node lifecycle

`DRAFT → SOURCE_MAPPED → HUMAN_REVIEWED → PRACTICED → QUALIFIED`. Нельзя перескакивать через `POLYGON`. Узлы в созданном графе пока DESCRIBED_NOT_QUALIFIED — они **не** квалифицированные навыки.

## Source isolation

Оригинальный защищённый текст книги не копировать в открытый GitHub. Цитирования ведут на страницу частного PDF с source ID. Только краткие самостоятельные определения и наши методики.

## Training separation

Knowledge records не равны training examples. Eval/holdout и gold POLYGON — отдельные защищённые наборы; даже если имеются записи в знаниях, нельзя считать, что модель «освоила» их без проверки.

## Agent visibility

Role views — фильтр над одним графом. Не создавать независимые предметные базы. UAG обеспечивает доступ в runtime. Актуализацию графа выполняет ALINA через review.

## Version/revision

На каждую главу — новая версия graph + glossary + algorithms. Старые ID не менять без ADR и migration map. Указывать факт/интерпретация/проект FATHER раздельно.

## Tests

Validator: IDs unique; all related nodes exist; source pages within reviewed chapters; importance 1..5; confidence proper; all role targets exist; glossary maps 1:1; referenced algorithm concepts exist.

**Дополнительное требование:** проверка структуры не доказывает смысловую правильность. ALINA и человек делают semantic review с PDF.
