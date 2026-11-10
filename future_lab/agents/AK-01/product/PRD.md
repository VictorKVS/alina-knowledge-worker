# AK-01 — Product Requirements Document (PRD)

## 1. Executive summary
AK-01 — мета-агент для автоматизированного проектирования базы знаний, RAG, графа знаний и prompt architecture для других агентов FATHER.

Главный результат работы продукта — **Agent Knowledge Blueprint**, пригодный для последующей реализации, обучения, тестирования и эксплуатации целевого агента.

## 2. Target users
### Primary
- FATHER Architect
- Agent Architect
- Knowledge Curator
- Product/System Analyst

### Secondary
- Security Architect
- Training Architect
- Domain Expert
- QA/Evaluator

## 3. Jobs To Be Done
### JTBD-01
Когда создаётся новый агент, я хочу формально определить, какие знания ему нужны, чтобы не собирать базу знаний вручную.

### JTBD-02
Когда у меня есть книги, статьи, стандарты и документация, я хочу превратить их в структурированные Knowledge Units с точным provenance.

### JTBD-03
Когда источники противоречат друг другу, я хочу сохранить обе позиции и увидеть evidence/counter-evidence, а не получить скрытое усреднение.

### JTBD-04
Когда база знаний готова, я хочу получить RAG architecture и prompt architecture, соответствующие задачам конкретного агента.

### JTBD-05
Когда знания обновляются, я хочу понимать, какие узлы, решения, промты и retrieval-политики стали устаревшими.

## 4. Product scope

### In scope
- target-agent decomposition;
- source intake;
- source classification;
- knowledge extraction;
- epistemic typing;
- provenance tracking;
- entity normalization;
- claim/evidence linking;
- contradiction detection;
- knowledge graph generation;
- contextual weighting;
- RAG specification;
- prompt architecture specification;
- gap/unknown registry;
- Agent Knowledge Blueprint;
- downstream handoff.

### Out of scope
- final autonomous runtime qualification;
- direct modification of production agents;
- curriculum generation;
- unrestricted autonomous web crawling;
- destructive changes to source corpus.

## 5. Functional requirements
FR-01 Accept Target Agent Profile.
FR-02 Accept heterogeneous source corpus.
FR-03 Preserve source identity/version/location.
FR-04 Extract typed Knowledge Units.
FR-05 Classify FACT/CLAIM/EVIDENCE/COUNTER_EVIDENCE/HYPOTHESIS/INTERPRETATION/ASSUMPTION/LIMITATION/UNKNOWN.
FR-06 Normalize aliases and duplicate concepts.
FR-07 Build typed graph nodes and edges.
FR-08 Compute contextual weight vector.
FR-09 Preserve contradictions.
FR-10 Build RAG Spec.
FR-11 Build layered Prompt Spec.
FR-12 Detect missing knowledge.
FR-13 Produce Agent Knowledge Blueprint.
FR-14 Validate output against schema.
FR-15 Produce full audit/provenance trail.

## 6. Non-functional requirements
NFR-01 Reproducibility.
NFR-02 Traceability.
NFR-03 Model-provider independence.
NFR-04 Retrieval-provider independence.
NFR-05 Graph-backend independence.
NFR-06 Security by default.
NFR-07 Idempotent job execution where applicable.
NFR-08 Versioned contracts.
NFR-09 Observability.
NFR-10 Human approval for critical policy changes.

## 7. Knowledge quality rules
- Wikipedia cannot be sole qualification evidence.
- LLM-generated knowledge without source support remains unverified.
- Contradictions must not be silently removed.
- Composite weights are policy outputs, not scientific truth.
- Every source-derived unit must retain provenance.
- QUALIFIED status is outside AK-01 authority.

## 8. MVP
Input:
- one Target Agent Profile;
- 1–20 documents;
- evidence policy;
- extraction policy.

Output:
- ≥ 1 valid Agent Knowledge Blueprint;
- Knowledge Units;
- knowledge graph;
- RAG spec;
- prompt spec;
- gaps;
- provenance.

## 9. First acceptance target
**FATHER Forecasting Agent**

Corpus:
- forecasting books;
- academic sources;
- method registry.

Expected result:
BOOK/PAPER → AK-01 → Knowledge Units → Weighted Graph → RAG Spec → Prompt Spec → Blueprint → Evidence Chain.

## 10. Acceptance criteria
AC-01 Schema-valid blueprint = 100%.
AC-02 Source-derived factual claims with provenance ≥ 95%.
AC-03 Unsupported factual claims = 0 in golden benchmark.
AC-04 Benchmark contradictions preserved = 100%.
AC-05 Duplicate concept normalization succeeds on benchmark aliases.
AC-06 Target-task knowledge coverage ≥ 90% on agreed benchmark.
AC-07 RAG retrieval grounding pass rate ≥ 90%.
AC-08 No production modification permissions.
