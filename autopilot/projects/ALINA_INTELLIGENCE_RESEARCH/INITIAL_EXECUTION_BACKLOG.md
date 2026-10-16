# AIR-001 Initial Backlog
Status: all tasks PLANNED. Only documentation has been authored.
| Task | Priority | Evidence needed |
|---|---|---|
| AIR-01 inventory current OSINT_deepseek TDLib/RAG/verification code, validate branch and tests | P0 | CI/local test results |
| AIR-02 identify authoritative technical primary source candidates and review licensing | P0 | source registry records |
| AIR-03 define 30–50 gold research questions by competencies | P0 | labels and references |
| AIR-04 create 3 retrieval benchmark baselines (BM25, vector, hybrid) on authorized corpus | P0 | precision/recall/latency |
| AIR-05 label claims and counterevidence including repost clusters | P0 | evidence QA |
| AIR-06 test ALINA prompt version candidate and refusal/abstention | P0 | eval log |
| AIR-07 test malicious PDF/message prompt injection and ACL leaks | P0 | security evidence |
| AIR-08 design source watchtower for tech changes and docs revisions | P1 | versioned alert schema |
| AIR-09 graph schema and FATHER Canvas display contract | P1 | UX + API review |
| AIR-10 source quality, donor licensing, maintenance reports | P1 | license guard dossier |
| AIR-11 candidate Knowledge Pack with 10 products | P1 | artifact validation |
| AIR-12 ADR and approved KB/prompt promotion process | P1 | explicit signoff |

## Work ownership
ALINA analyst = research brief, hypotheses, claim decisions. OSINT core = permitted acquisition/provenance. FATHER Security/License Guard = tools, rights and scans. Architect = interfaces, sizing, ADR. Reviewer = source and decision acceptance.

## Proof-of-work sequence
Audit existing code and corpus → source candidate vetting → gold dataset → benchmark design → governance + cost review → approve → controlled PoC (only after readiness gate).

## Hard stop
Do not change ALINA runtime prompt/RAG, run Telegram scraper, or import external donor code as part of this documentation task.
