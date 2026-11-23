# LIB-0040 CH02 — Routing / Delegation: A/B/C

**Источник:** Antonio Gulli, PDF 34–47. **DESIGNED_ONLY / NOT_RUN / NOT_QUALIFIED**.

## A (начинающий)
Реализовать `route(request) -> label` в Python без LLM, на 12 контрольных фразах с ожидаемой категорией. Проверить, что `unclear` не выдаёт разрешения на действия.

## B (LLM + LangChain)
Использовать `examples/ch02_router.py`. На 30 synthetic cases сравнить rule-based classifier и LLM router: accuracy, invalid-label rate, latency, cost, ambiguity rate. Сохранить исходный текст и предсказанную категорию без секретов.

## C (FATHER)
Заменить simulated handler на mock Agent Capability, добавить `capability_id`, schema, scope, UAG authorization, trace и POLYGON. Тестировать инъекции в пользовательском сообщении, отказ доступа, неизвестную роль и fail-closed. Не выполнять настоящих бронирований/изменений.
