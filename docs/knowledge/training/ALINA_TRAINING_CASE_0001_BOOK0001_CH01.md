# ALINA TRAINING CASE 0001

## Source

- `SRC-BOOK-0001`
- Suhas Pai — *Designing Large Language Model Applications*
- Scope: Preface + Chapter 1

## Objective

Teach ALINA to transform a technical source into engineering knowledge without confusing:

- source fact;
- author recommendation;
- ALINA inference;
- architecture decision;
- implementation evidence.

## Gold examples

### Example 1

**Source-supported concept:** a prototype can be easy to build while production requires accuracy and reliability guarantees.

**Correct ALINA mapping:**

```text
class: CONCEPT
engineering implication: introduce production-readiness criteria
candidate artifact: Production Readiness Gate
validation needed: define measurable acceptance tests
```

**Incorrect behavior:** "Therefore FATHER must use framework X."

Reason: the source does not support that implementation choice.

### Example 2

**Source-supported pattern:** PDF QA pipeline contains parsing, chunking, embeddings, vector storage, retrieval, generation and conversation history.

**Correct ALINA mapping:** decompose into replaceable RAG capabilities.

**Incorrect behavior:** treat the tutorial's chosen libraries as mandatory FATHER architecture.

### Example 3

**Source-supported limitation:** vector similarity does not guarantee that retrieved text contains the answer.

**Correct ALINA mapping:** retrieval quality requires separate evaluation / reranking / answerability checks.

**Incorrect behavior:** report cosine similarity as proof of answer correctness.

## Expected learning outcome

ALINA passes this case when she can:

1. preserve provenance for every extracted atom;
2. identify source vs inference;
3. generate capability mappings without inventing implementation facts;
4. produce candidate FATHER destinations;
5. explicitly mark what still requires external validation;
6. retain limitations and negative knowledge instead of discarding them.
