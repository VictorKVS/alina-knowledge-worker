# BOOK-0001 — Chapter Processing Map

The book is processed chapter-by-chapter through ALINA Book Knowledge Factory.

| Scope | Theme | Required ALINA outputs | FATHER destination |
|---|---|---|---|
| Preface | goals, audience, scope | source model, reading intent, boundaries | knowledge governance |
| Ch.1 | introduction, prompting, PDF chatbot, prototype→production | glossary, RAG prototype, production gaps | core/RAG/model/eval |
| Ch.2 | pre-training data | data sourcing, filtering, dedup, PII, contamination | data pipeline/security |
| Ch.3 | tokenization/vocabulary | tokenizer concepts and constraints | model profile |
| Ch.4 | architecture/training | model internals, objectives, architecture | Model Zoo |
| Ch.5 | model selection / prompting / evaluation context | selection rules, prompt behavior | Model Router / Eval |
| Ch.6 | fine-tuning | use cases, datasets, tuning decisions | adaptation pipeline |
| Ch.7 | efficient/domain adaptation | PEFT / continued training | model adaptation |
| Ch.8 | hallucination / reasoning / alignment | limitations, mitigation, reasoning | guardrails/eval |
| Ch.9 | inference optimization | latency/cost/caching/quantization | runtime/inference |
| Ch.10 | tools and agents | tool use, decomposition, agency | Agent/Tool/MCP |
| Ch.11 | embeddings / retrieval | embedding and chunking quality | RAG blocks |
| Ch.12 | RAG | robust retrieval pipeline | C2_KNOWLEDGE_RAG |
| Ch.13 | design patterns / system architecture | multi-LLM, architecture patterns | chassis/blocks/router |

## Completion states

Each chapter progresses through:

```text
REGISTERED
→ TRANSLATED
→ SEMANTICALLY_DECOMPOSED
→ GLOSSARY_LINKED
→ EXAMPLES_STRUCTURED
→ ALGORITHMS_EXTRACTED
→ CHECKLISTS_BUILT
→ KNOWLEDGE_NORMALIZED
→ FATHER_MAPPED
→ REVIEWED
```
