# AK-01 — Customer Problem & Maturity Map (CPMM)

| Problem | Value | Product task | Function | Done criterion | Metric | Risk | Complexity |
|---|---|---|---|---|---|---|---|
| Knowledge for every agent is built manually | Reuse | automate knowledge design | target-agent decomposition | capability/knowledge map produced | coverage | wrong decomposition | M |
| Sources are unstructured | Machine usability | extract knowledge | Knowledge Unit extraction | schema-valid units | schema validity | hallucinated extraction | H |
| Source authority differs | Evidence quality | classify evidence | source/evidence registry | every source typed | classification accuracy | bad authority model | M |
| Claims conflict | Trust | retain disagreement | contradiction engine | conflicting claims linked | contradiction recall | false contradiction | H |
| Concepts duplicate | Clean graph | normalize entities | entity resolver | aliases merged safely | duplicate rate | over-merge | H |
| Relevance differs by agent | Precision | contextual weighting | weight vector | weights traceable to policy | ranking quality | arbitrary weights | H |
| Vector RAG alone is weak | Better retrieval | hybrid retrieval design | lexical+vector+graph | RAG spec generated | retrieval recall/precision | retrieval noise | H |
| Prompts become monolithic | Maintainability | prompt decomposition | layered prompt spec | policy layers separated | change isolation | conflicting policies | M |
| Missing knowledge is invisible | Coverage | detect gaps | unknown registry | gaps surfaced | gap recall | false completeness | H |
| Knowledge ages | Maintainability | freshness control | source/version tracking | stale knowledge detectable | stale-source rate | outdated decisions | M |

## Product maturity target

MVP target: F3 Automated for one domain.

Expansion target: F4 Self-Verifying across multiple agent classes.

Long-term target: F5/F6 learning/adaptive knowledge factory with controlled human gates.
