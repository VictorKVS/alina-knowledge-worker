# AK-01 — PostgreSQL Logical Schema

Core tables:
- target_agents
- knowledge_jobs
- sources
- source_versions
- source_fragments
- knowledge_units
- knowledge_edges
- claim_evidence_links
- contradictions
- weight_vectors
- procedures
- procedure_steps
- checklists
- checklist_items
- rag_specs
- prompt_packages
- knowledge_gaps
- knowledge_capsules
- capsule_versions
- knowledge_deltas
- delta_impacts
- reviews
- qualification_records
- audit_events
- outbox_events

## Critical constraints
- source_versions.content_hash UNIQUE per source/version
- released capsule_version immutable at application layer + DB trigger/policy where practical
- knowledge_unit source-derived records require provenance FK
- qualification actor cannot be AK-01
- scope_layer constrained to CORE/DOMAIN/ORGANIZATION/PROJECT/ACTIVE_CONTEXT
- all versioned artifacts contain schema_version and created_at

## Vector data
Store embedding vectors on approved source fragments and/or normalized knowledge units using pgvector.

## Derived indexes
Vector index and graph snapshots are rebuildable. PostgreSQL + object source + provenance are authoritative.
