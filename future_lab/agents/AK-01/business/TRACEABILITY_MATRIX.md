# AK-01 — Business Traceability Matrix

| Req | Business need | Function | Data | Evidence | Done |
|---|---|---|---|---|---|
| BR-01 | know what agent must know | target-agent decomposition | profile/tasks/capabilities | role/task spec | capability map exists |
| BR-02 | trust extracted knowledge | provenance | source/version/location | source registry | provenance >=95% |
| BR-03 | avoid hallucinated facts | epistemic typing | claims/evidence | citations | unsupported claims = 0 benchmark |
| BR-04 | preserve disagreements | contradiction engine | claim/counterclaim | evidence links | contradictions retained |
| BR-05 | remove duplicate concepts | entity normalization | aliases/entities | normalization evidence | benchmark aliases resolved |
| BR-06 | context-aware relevance | weighting engine | weight vectors | policy/config | ranking accepted |
| BR-07 | retrieve correct knowledge | RAG designer | chunks/index/graph | retrieval tests | grounding >=90% |
| BR-08 | avoid monolithic prompts | prompt architect | prompt layers | prompt spec | layers separated |
| BR-09 | expose missing knowledge | gap detector | unknown registry | gap reports | gaps visible |
| BR-10 | enable downstream training | training handoff | prereq graph/weights | contract | AT-01 can consume |
