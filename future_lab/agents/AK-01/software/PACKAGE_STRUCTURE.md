# AK-01 — Python Package Structure

```text
src/ak01/
├── __init__.py
├── api/
│   ├── app.py
│   ├── dependencies.py
│   ├── errors.py
│   └── routes/
│       ├── jobs.py
│       ├── sources.py
│       ├── knowledge.py
│       ├── capsules.py
│       └── health.py
├── domain/
│   ├── enums.py
│   ├── entities.py
│   ├── value_objects.py
│   ├── events.py
│   ├── errors.py
│   └── policies.py
├── contracts/
│   ├── dto.py
│   ├── source.py
│   ├── knowledge.py
│   ├── graph.py
│   ├── rag.py
│   ├── prompt.py
│   ├── capsule.py
│   └── events.py
├── application/
│   ├── orchestrator.py
│   ├── job_service.py
│   ├── source_service.py
│   ├── extraction_service.py
│   ├── graph_service.py
│   ├── procedure_service.py
│   ├── retrieval_service.py
│   ├── prompt_service.py
│   ├── capsule_service.py
│   └── delta_service.py
├── ports/
│   ├── model.py
│   ├── repositories.py
│   ├── vector.py
│   ├── graph.py
│   ├── object_store.py
│   ├── event_bus.py
│   └── clock.py
├── adapters/
│   ├── llm/
│   ├── postgres/
│   ├── pgvector/
│   ├── networkx/
│   ├── object_store/
│   └── events/
├── knowledge/
│   ├── extractor.py
│   ├── epistemic.py
│   ├── normalization.py
│   ├── evidence.py
│   ├── contradictions.py
│   └── ontology.py
├── procedures/
│   ├── builder.py
│   └── checklist.py
├── retrieval/
│   ├── hybrid.py
│   ├── ranking.py
│   └── trust.py
├── prompts/
│   ├── builder.py
│   └── layers.py
├── lifecycle/
│   ├── versioning.py
│   ├── delta.py
│   ├── impact.py
│   └── qualification.py
├── security/
│   ├── authorization.py
│   ├── namespaces.py
│   ├── source_isolation.py
│   ├── secrets.py
│   └── policy.py
├── observability/
│   ├── logging.py
│   ├── metrics.py
│   └── tracing.py
└── testing_adapter.py
```
