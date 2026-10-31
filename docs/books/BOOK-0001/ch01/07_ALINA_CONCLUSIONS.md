# Chapter 1 — ALINA Conclusions

These are ALINA-derived, not direct statements of the book.

## A1 — FATHER must model LLM applications as composed systems

Derived from:
- PDF chatbot pipeline;
- prototype-to-production roadmap.

Implication:
`PRODUCT != MODEL`. A product is model + retrieval + workflow + state + security + evaluation + observability + configuration.

## A2 — Prompt is a versioned engineering artifact

Derived from:
- prompt drift;
- output-control examples.

Implication:
FATHER needs Prompt Registry + prompt version + model compatibility + regression evidence.

## A3 — Retrieval requires its own evidence

Derived from:
- PDF chatbot retrieval behavior;
- similarity vs answerability limitation.

Implication:
Retriever/reranker/evaluator should be separate blocks.

## A4 — Security must sit outside the model

Derived from:
- adversarial prompting;
- alignment weakness.

Implication:
Guardrails/UAG/authorization/audit must not rely only on model refusal behavior.
