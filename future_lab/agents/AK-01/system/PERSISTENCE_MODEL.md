# AK-01 — Persistence Model

## PostgreSQL
Authoritative transactional metadata:
- jobs
- target agents
- sources
- source versions
- fragments metadata
- knowledge units
- claims/evidence links
- contradictions
- gaps
- procedures/checklists
- specs
- capsule versions
- deltas
- reviews
- qualification records

## Object Storage
Raw and normalized source files.

## Vector Index
Semantic retrieval index over approved fragments and knowledge units.

## Graph Store
Knowledge graph topology and graph queries.

MVP may use PostgreSQL + pgvector + NetworkX persisted snapshots before introducing a dedicated graph database.

## Audit / Provenance Ledger
Append-only events and provenance transformations.

## Principle
No store independently defines truth.
Authoritative state is reconstructed through versioned records + provenance + review status.
