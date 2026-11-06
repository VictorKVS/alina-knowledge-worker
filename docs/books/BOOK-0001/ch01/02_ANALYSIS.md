# Chapter 1 — Semantic Analysis

## Main problems

1. Что такое LLM и где проходят её ограничения.
2. Как управлять моделью через prompt/context.
3. Как построить минимальный прикладной LLM prototype.
4. Почему prototype success не доказывает production readiness.
5. Какие инженерные слои появляются при переходе к production.

## Core concepts

- LLM
- token/context
- prompt
- zero-shot prompting
- few-shot prompting
- chain-of-thought
- prompt chaining
- adversarial prompting
- prompt drift
- embeddings
- vector retrieval
- RAG
- evaluation
- hallucination
- latency / cost
- tools / agents

## Important tradeoffs

- CoT может помогать reasoning-задачам, но увеличивает число токенов и стоимость.
- Prompt chaining удобнее для многошаговых задач, но создаёт более сложный workflow.
- Similarity retrieval не гарантирует answerability.
- Более сильная модель не устраняет необходимость versioning/evaluation.

## Failure modes

- prompt drift;
- irrelevant retrieval;
- hallucination;
- faulty reasoning;
- uncontrolled cost/latency;
- over-reliance on a single model/API;
- adversarial prompting;
- treating prototype behavior as evidence of reliability.
