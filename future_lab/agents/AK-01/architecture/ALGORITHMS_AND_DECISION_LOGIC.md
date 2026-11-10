# AK-01 — Algorithms and Decision Logic

## Extraction
Candidate techniques:
- structure-aware parsing
- section-aware chunking
- schema-constrained LLM extraction
- rule-based pattern extraction for formulas/tables
- confidence scoring based on evidence availability

## Entity normalization
Algorithms:
- exact normalized string match
- token similarity
- embedding similarity
- acronym/alias dictionary
- graph-neighborhood similarity
- human review above merge-risk threshold

## Contradiction detection
Pipeline:
1. cluster claims by subject/predicate
2. normalize units/time/version/context
3. semantic contradiction classifier
4. evidence comparison
5. mark unresolved if context differs

## Graph construction
Algorithms:
- typed edge generation
- connected-component checks
- orphan detection
- cycle detection where DAG semantics required
- prerequisite topological sort

## Weighting
Do not let the LLM invent arbitrary final scores.
Use explainable attributes:
- authority
- evidence
- relevance
- recency
- applicability
- confidence
- prerequisite importance
- operational criticality
- contradiction penalty

Ranking policy may use:
- weighted linear scoring
- rule-based dominance
- Pareto filtering
- learned reranker later, after benchmark data exists

## Retrieval
Hybrid retrieval:
- sparse/BM25
- dense vector
- graph neighborhood expansion
- metadata filtering
- reciprocal-rank or weighted fusion
- reranking
- evidence trust filter

## Procedure synthesis
Build from:
METHOD + PRECONDITIONS + DECISION RULES + LIMITATIONS + VALIDATION RULES

## Gap detection
Compare:
required capabilities/knowledge
MINUS
verified graph coverage

## Impact analysis
When a node changes:
- traverse outgoing dependency edges
- find affected procedures
- find affected prompts
- find affected RAG partitions
- find affected training modules
- define targeted regression/requalification set
