# BOOK-002 / CH07 — Advanced Fine-Tuning Techniques

**Источник:** Suhas Pai, *Designing Large Language Model Applications*, пользовательский PDF, стр. 378–413/765; непосредственно изучен. Оригинальный учебный конспект, не перевод и не воспроизведение книги. **CH07 SOURCE_REVIEWED**, технологии не проверялись в FATHER.

## Карта разделов

| Страницы PDF | Содержание |
|---|---|
| 378–380 | Мотивации: domain, task, knowledge, controllability; три семейства методов |
| 380–384 | Continual pre-training, DAPT, TAPT, lifelong learning и доменные корпуса |
| 385–387 | Catastrophic forgetting, replay, distillation, regularization, learning rate |
| 388–390 | Parameter expansion, DEMix, приоритет RAG для новых фактов |
| 391–398 | PEFT и bottleneck adapters |
| 398–402 | Prefix-tuning, trainable soft prompt tuning |
| 402–403 | Subset methods, bias-only fine-tuning |
| 404–408 | Multi-model ensembling; LLM-Blender PairRanker / GenFuser |
| 408–413 | Merging/fusion, weighted averaging, adapter merging, риски |

## 1. Продолженное предобучение

**Continual pre-training:** используем существующий checkpoint, затем продолжаем обучение на новом корпусе. По книге характерные случаи: доменная терминология, стиль, новый язык или непрерывное обучение. **DAPT** означает domain-adaptive pre-training; **TAPT** — task-adaptive pre-training на текстах ближе к целевой задаче. Обычное fine-tuning на инструкциях не тождественно дальнейшему самоконтролируемому предобучению.

Опасность — **catastrophic forgetting**: новые тексты могут снижать старые компетенции. Автор описывает replay старых данных, distillation, регуляризацию и расширение параметров. Его иллюстративная стратегия replay начинается с примерно 25% новых данных и может увеличивать их долю; это **не универсальный гиперпараметр для FATHER**.

### FATHER-вывод

Если ALINA получила новый закон, страницу стандарта или свежую информацию, сначала обновляем версионируемую базу знаний и RAG. Не запускаем обучение весов автоматически. На PDF 390 автор явно советует для новых знаний зачастую предпочесть RAG.

## 2. PEFT: несколько классов методов

PEFT уменьшает число обновляемых параметров:
- **Bottleneck adapters** — узкие дополнительные модули в Transformer с проекцией вниз и вверх; база может оставаться замороженной.
- **Prefix-tuning** — обучаемые векторы, влияющие на представления на нескольких слоях.
- **Soft prompt tuning** — обучаемые виртуальные векторы на входе. **Это не редактирование обычного текстового системного промпта.**
- **Subset methods** — обновление только выбранных существующих параметров, например bias (BitFit).
- **Low-rank methods** — семейство PEFT с низкоранговыми обновлениями, включая LoRA, уже рассмотренную в CH06.

Эффективность памяти не означает отсутствие сложности: нужны веса, права на адаптацию, датасеты и квалификация, а иногда увеличивается задержка инференса.

## 3. Model ensembling vs model merging

**Ensembling:** отправляем вход нескольким моделям, сравниваем/синтезируем их ответы. Пример из книги — LLM-Blender: PairRanker ранжирует, GenFuser объединяет выходы. Веса не объединяются.

**Merging/fusion:** арифметически или иным способом комбинируем параметры совместимых моделей/адаптеров. Книга рассматривает averaging, weighted averaging, interpolation, adapter soup. Это экспериментальное направление: улучшения не гарантированы, а безопасность и несанкционированные утечки нужно проверять заново. Не считать model averaging механизмом гарантированного удаления конфиденциальных данных.

## 4. Какая стратегия нужна ALINA

**Наше инженерное расширение, не указание автора:** GPT в роли ALINA использует Knowledge/Prompt/RAG/Learning/Qualification Packages. Первые улучшения реализуются без изменения весов: исправление источников, retrieval, шагов workflow, обычного промпта, формата выходов и детерминированных проверок.

Если стабильный дефицит компетенции подтверждён, ALINA оформляет заявку `ModelAdaptationProposal`:
- роль и конкретная ошибка;
- baseline и ожидаемая метрика;
- сравнение non-weight alternatives;
- доступный правомерный dataset;
- обучаемый механизм;
- затраты, совместимость, лицензия;
- regression и независимый holdout;
- human approval, rollback и evidence.

FATHER Architect утверждает техническую реализацию, POLYGON независимо проверяет, UAG отвечает за действия и доступ к инструментам.

## 5. Контрольные вопросы

1. Чем DAPT и TAPT отличаются от supervised instruction tuning?
2. Что такое catastrophic forgetting и как работает replay?
3. Почему для новых фактов RAG часто лучше continual pre-training?
4. Чем bottleneck adapter отличается от LoRA?
5. Чем soft prompt отличается от текстового system prompt?
6. Почему объединить ответы моделей не то же самое, что объединить веса?
7. Почему улучшение доменной задачи требует проверки регрессий?
8. Зачем модели с несколькими задачами могут потребоваться отдельные адаптеры?

## Статус

SOURCE_REVIEWED; KNOWLEDGE_DESIGNED; NO_TRAINING_RUN; NO_INFERENCE_COMPARISON; NOT_POLYGON_QUALIFIED.

[Практикум](../practicum/CH07_ADAPTATION_DECISION_RU.md)
