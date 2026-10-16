# AIR-001 Technical Search Mission Register
**These are planned searches, not collected evidence.** Each job requires authorized sources and logged query/date.

| ID | Research question | Suggested searches | Preferred sources | Output |
|---|---|---|---|---|
| SR-01 | How to split system prompt, RAG and tools? | system prompt invariants, agent tool scope, RAG untrusted context | official model docs, OWASP, agent frameworks | prompt requirements |
| SR-02 | How to retrieve exact regulatory clauses? | Russian legal documents BM25 vector hybrid query, heading-aware chunking, metadata filters | papers, docs, experiments | corpus design |
| SR-03 | How to calibrate citations/abstention? | RAG citation accuracy, claim entailment, evidence sufficiency, calibration | original publications and eval docs | evidence methodology |
| SR-04 | How to handle revisions? | bitemporal retrieval, effective date, document versioning, normative corpus | official docs and engineering research | temporal contract |
| SR-05 | How to measure RAG? | recall@k, citation correctness, faithfulness, abstention, leakage tests | Ragas, retrieval papers, own benchmarks | gold evaluation |
| SR-06 | How to prevent document injection? | OWASP LLM retrieval injection, access boundary | OWASP/NIST/advisories | security controls |
| SR-07 | Which graph relations improve retrieval? | GraphRAG source provenance, entity linking, graph eval | original GraphRAG, papers | graph schema |
| SR-08 | How do senior analysts test hypotheses? | structured analytic techniques, competing hypotheses, evidence calibration | original analytic manuals, publications | competency/method registry |
| SR-09 | What does OSINT messenger monitoring contribute? | early signal detection, technical channel announcements, link source expansion | permitted Telegram sources then official upstream verification | watch rules |
| SR-10 | Which dependencies can be safely reused? | release licenses, vulnerabilities, open source governance | upstream code, LICENSE, SBOM, advisories | donor decision |

## Initial confirmed starting *candidates*, not findings
https://www.cia.gov/resources/csi/
https://www.nist.gov/itl/ai-risk-management-framework
https://genai.owasp.org/
https://atlas.mitre.org/
https://github.com/microsoft/graphrag
https://github.com/deepset-ai/haystack
https://github.com/langchain-ai/langgraph
https://github.com/explodinggradients/ragas
Curation target: 30–50 independent sources with exact claim/source/version evidence. No quota-driven promotion.

## Pilot user case
Question: "How should ALINA retrieve a currently applicable requirement with an exact clause citation and refuse to invent obligations if missing?" Compare BM25-only, vector-only and hybrid on permissioned CyberED sample documents using an expert-labeled gold set.
