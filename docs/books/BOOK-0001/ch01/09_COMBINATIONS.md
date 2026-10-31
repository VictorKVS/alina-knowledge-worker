# Chapter 1 — ALINA Combinations / Hypotheses

## HYP-CH01-001

Prompt drift + model selection + evaluation  
→ Prompt Registry should store model compatibility and regression evidence.

Validation needed:
- same prompt across multiple model versions;
- regression dataset.

## HYP-CH01-002

Prompt chaining + tools + agents  
→ workflow/orchestration should be a separate FATHER block rather than embedded in prompts.

Validation needed:
- compare chained prompt-only flow with graph/workflow engine.

## HYP-CH01-003

RAG prototype + similarity limitation  
→ retrieval quality must have an independent evaluator/reranker gate.

Validation needed:
- retrieval benchmark;
- answerability labels.

## HYP-CH01-004

Adversarial prompting + prototype-to-production gap  
→ production security requires controls external to the LLM.

Validation needed:
- red-team prompt suite;
- policy enforcement outside model output.
