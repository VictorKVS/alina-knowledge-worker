# AK-01 — Adapter Status

## Added
- SQLAlchemyJobRepository
- VectorIndex port + InMemoryVectorIndex
- GraphStore port + InMemoryGraphStore
- ModelProvider port + NullModelProvider
- ObjectStore port + LocalObjectStore
- SecurityContext / namespace authorization
- initial PostgreSQL SQL migration baseline

## Next
- PostgreSQL source/knowledge/capsule repositories
- pgvector SQL adapter
- NetworkX-backed graph adapter
- actual model provider adapter
- encrypted object storage/S3 adapter
- secret manager
- correlation middleware
- OpenTelemetry exporters
