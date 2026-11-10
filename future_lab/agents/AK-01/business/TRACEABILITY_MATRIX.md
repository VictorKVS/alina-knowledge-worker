# AK-01 — Business Traceability Matrix

| Req | Business need | Function | Data | Evidence | Done |
|---|---|---|---|---|---|
| BR-01 | know what agent must know | target-agent decomposition | profile/tasks/capabilities | role/task spec | capability map exists |
| BR-02 | trust extracted knowledge | provenance | source/version/location | source registry | provenance >=95% |
| BR-03 | avoid hallucinated facts | epistemic typing | claims/evidence | citations | unsupported claims = 0 benchmark |
| BR-04 | preserve disagreements | contradiction engine | claim/counterclaim | evidence links | contradictions retained |
| BR-05 | remove duplicate concepts | entity normalization | aliases/entities | normalization evidence | benchmark aliases resolved |
| BR-06 | context-aware relevance | weighting engine | attributes/weight policy | policy/config | ranking explainable |
| BR-07 | retrieve correct knowledge | RAG designer | chunks/index/graph | retrieval tests | grounding >=90% |
| BR-08 | avoid monolithic prompts | prompt architect | prompt layers | prompt spec | layers separated |
| BR-09 | expose missing knowledge | gap detector | unknown registry | gap reports | gaps visible |
| BR-10 | enable downstream training | training handoff | prerequisite graph/competencies | handoff contract | AT-01 can consume |
| BR-11 | convert knowledge into action | procedure builder | methods/rules/tasks | procedures/checklists | task procedure exists |
| BR-12 | learn from training failures | competency gap analysis | attempts/errors/evals | QA traces | root cause classified |
| BR-13 | adapt to local practice | local knowledge layer | org/team/project sources | local evidence | local delta created |
| BR-14 | avoid uncontrolled self-editing | delta governance | proposed changes | curator decision | no silent overwrite |
| BR-15 | preserve specialist history | capsule versioning | version lineage | audit trail | versions traceable |
| BR-16 | maintain competence after changes | requalification | delta + test scope | exam results | changed areas retested |
| BR-17 | separate universal and local knowledge | layered capsule model | core/domain/org/project/context | layer metadata | every local unit scoped |
