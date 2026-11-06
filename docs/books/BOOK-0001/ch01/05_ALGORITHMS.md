# Chapter 1 — Algorithms and Procedures

## ALG-CH01-001 — Zero-shot prompt construction

1. State the task precisely.
2. Define allowed output space/format.
3. Provide the input.
4. Prime the expected output position when useful.
5. Evaluate against examples.
6. Version-control the prompt because of prompt drift.

## ALG-CH01-002 — Prompt chaining

1. Decompose the task into subtasks.
2. Define output contract of each subtask.
3. Feed output of stage N into stage N+1.
4. Validate intermediate outputs.
5. Compare chained workflow with single-prompt baseline.

## ALG-CH01-003 — PDF QA / minimal RAG

1. Parse document.
2. Split text into chunks.
3. Compute chunk embeddings.
4. Store/index embeddings.
5. Embed user query.
6. Retrieve top candidate chunks.
7. Assemble query + retrieved context + instructions.
8. Invoke LLM.
9. Return answer.
10. Persist conversation history.
11. Evaluate retrieval relevance and answer quality.

## ALG-CH01-004 — Prototype to production

1. Define accuracy/reliability requirements.
2. Evaluate candidate models.
3. Define metrics and benchmark dataset.
4. Decide whether fine-tuning/adaptation is required.
5. Detect/mitigate hallucination and reasoning failures.
6. Optimize inference latency and cost.
7. Add tools/agents where justified.
8. Improve retrieval/RAG.
9. Add security, observability and evidence.
10. Release only after gates pass.
