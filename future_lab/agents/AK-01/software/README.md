# AK-01 — Software Architecture Package

Owner: APO-01 Software Architect

## Objective
Translate approved AK-01 architecture and executable tests into concrete software boundaries.

## Technology profile
- Python 3.12
- FastAPI
- Pydantic v2
- PostgreSQL
- pgvector
- SQLAlchemy 2.x
- Alembic
- NetworkX first; graph DB adapter later
- pytest
- OpenTelemetry

## Design style
Modular monolith + worker for MVP.

## Rules
- domain model independent of FastAPI/DB/LLM provider
- ports/adapters for model, vector, graph, object store and events
- every external call behind an interface
- immutable released capsule versions
- transactional writes where consistency matters
- outbox for reliable event publication
- test adapter is a first-class interface
