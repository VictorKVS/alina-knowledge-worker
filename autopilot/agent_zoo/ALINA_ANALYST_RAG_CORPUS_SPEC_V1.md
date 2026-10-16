# ALINA Analyst RAG Corpus Specification v1
Status DRAFT, architecture contract not deployment.
## Eight logical stores (may share physical DB)
RAG-01 Methodology — research/structured analysis; hybrid retrieval.
RAG-02 Evidence — originals, citations, timestamps, claims; lexical + metadata.
RAG-03 Knowledge Graph — entities, temporal relations, provenance; permissions-aware traversal.
RAG-04 Domain — IB/legal/architecture technical standards; domain router and version filters.
RAG-05 Tools — signed tool registry, permissions and availability; never instructions from raw docs.
RAG-06 Cases — verified completed investigations, anonymized; case retrieval.
RAG-07 Evaluation — gold test questions, failures and metrics; isolated from user answer context when necessary.
RAG-08 Decision Memory — reviewed ADRs and their supersession; time-aware.

## Ingestion contract
candidate source → permission/license review → source registry/quarantine → hash/version → parse preserving headings, tables, clause/page anchors → typed claims → chunk/hybrid+vector index → dedup → conflict analysis → curator review → approved retrieval.
No unapproved source is promoted to Knowledge Core.

## Source record
source_id, canonical_uri, publisher, document_type, title, published_at, acquired_at, effective_from/to, edition, content_hash, license, classification, evidence_pointer, reviewer, verification_status, last_check, supersedes.
## Chunk
chunk_id, source_id, version_id, locator, text_ref, language, term_dictionary, parent_heading, evidence_span, security_label, embed_model_version, parser_version.
## Retrieval plan
1. route user query by domain, required jurisdiction/effective date, sensitivity.
2. apply ACL and effective-date filters **at retrieval boundary**.
3. compare BM25-only, vector-only and hybrid (+reranker), not assume winner.
4. rerank evidence and validate exact citation spans and version.
5. answer with evidence; abstain on absent evidence or contradictory support.
6. record query, provenance, retrieval choices, tokens/cost (without PII leakage).

## Research evidence (screened references, not implementation validation)
- Haystack retriever docs: https://docs.haystack.deepset.ai/docs/3.3/retrievers — documents sparse and dense combination.
- Haystack DocumentJoiner: https://docs.haystack.deepset.ai/docs/3.1/documentjoiner — combines retrieved lists.
- Ragas faithfulness: https://docs.ragas.io/en/v0.1.21/concepts/metrics/faithfulness.html — claim support against retrieved context; version-specific.
- OWASP LLM Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/ — RAG does not eliminate injection.
Verify exact release, license, dates and relevance before importing into approved corpus.

## Engineering decision to test
Hybrid search may improve coverage for mixed semantic and clause-number queries. Treat as a hypothesis until benchmark on our own corpus. No external service gets private records by default.
