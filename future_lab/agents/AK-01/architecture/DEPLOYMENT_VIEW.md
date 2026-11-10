# AK-01 — Service Boundaries and Deployment View

## MVP deployment

```mermaid
flowchart LR
    API[FastAPI AK-01 Service]
    WORKER[Knowledge Worker]
    PG[(PostgreSQL + pgvector)]
    OBJ[(Local/S3 Object Store)]
    GRAPH[(NetworkX snapshot / future graph DB)]
    QUEUE[(Queue / Event Bus)]
    OTEL[OpenTelemetry]
    MODEL[LLM Provider / Local Model]

    API --> PG
    API --> QUEUE
    WORKER --> QUEUE
    WORKER --> PG
    WORKER --> OBJ
    WORKER --> GRAPH
    WORKER --> MODEL
    API --> OTEL
    WORKER --> OTEL
```

## Evolution
MVP:
- modular monolith + worker
- PostgreSQL/pgvector
- NetworkX

Later:
- split heavy ingestion/extraction services
- dedicated graph DB if graph scale/query profile justifies it
- dedicated event bus
- provider routing
