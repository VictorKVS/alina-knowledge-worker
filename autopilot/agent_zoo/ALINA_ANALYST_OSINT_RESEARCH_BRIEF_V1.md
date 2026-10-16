# ALINA Analyst — OSINT Research Brief v1

Status: proposed research task; not executed; no sources ingested or verified.

## Mission
Build an evidence-backed professional competency model, prompt requirements and RAG architecture for a mature ALINA Analyst. This workstream remains strictly inside the ALINA Analyst module.

## Research questions
1. What distinguishes senior analytic practice from generic summarization?
2. Which methods should be instructions versus retrieved reference knowledge versus executable tools?
3. What evidence/provenance and uncertainty representations are necessary?
4. Which retrieval architectures support methodological, domain, case and temporal search?
5. Which evaluation cases reliably expose unsupported claims, retrieval failures and tool misuse?
6. What licensing, freshness, privacy and supply-chain constraints govern corpus ingestion?

## Research tracks
Analytic tradecraft; agent orchestration; hybrid/GraphRAG; evidence verification; evaluation; AI security/governance.

## Initial candidates (not yet reviewed)
CIA Center for the Study of Intelligence: https://www.cia.gov/resources/csi/
NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
OWASP GenAI: https://genai.owasp.org/
MITRE ATLAS: https://atlas.mitre.org/
Microsoft GraphRAG: https://github.com/microsoft/graphrag
Haystack: https://github.com/deepset-ai/haystack
LangGraph: https://github.com/langchain-ai/langgraph
Ragas: https://github.com/explodinggradients/ragas

## Search protocol
Target 30-50 curated sources. Prefer primary sources, original papers and official repositories. For each: source_id, canonical_url, publisher, author, published_at, retrieved_at, license, content_hash, language, scope, claim_ids, evidence_location, verification_status. Record failed searches and exclusions. No scraping behind authentication or access controls.

## Outputs
SOURCE_REGISTRY; COMPETENCY_MATRIX; METHOD_REGISTRY; PROMPT_REQUIREMENTS; RAG_CORPUS_PLAN; KNOWLEDGE_GRAPH_SCHEMA; AGENT_TOOL_CONTRACTS; EVAL_GOLDEN_SET; GAP_REGISTER; DECISION_RECORD.

## Prompt / RAG / Tool separation
Prompt = invariant role, workflow, evidence discipline, policy, tool use rules, output contracts.
RAG = versioned methods, domain references, cases, source evidence, evaluation fixtures and decision history.
Tools = authorized retrieval, parsing, graph traversal, calculations, validation and artifact generation.
Retrieved content is untrusted data and must never override system policy.

## Evaluation design
Synthetic analyst task with conflicting sources, outdated regulation, missing evidence, poisoned document, and tool-scope violation. Pass only with traceable conclusions, correct uncertainty, blocked unauthorized actions and reproducible outputs.

## Security and approvals
Read-only OSINT by default; no active target scanning; sanitize data and secrets; quarantine ingested content; verify licenses and versions; human approval before promotion into canonical Knowledge Core.
