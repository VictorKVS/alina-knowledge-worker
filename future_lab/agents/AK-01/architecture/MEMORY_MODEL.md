# AK-01 Memory Model

## 1. Working Memory
Scope: one active job/stage.
Contains:
- current task
- current source fragments
- temporary extraction candidates
- current graph slice
- unresolved decisions

Lifecycle:
created with job stage, discarded or checkpointed after stage completion.

## 2. Episodic Memory
Scope: previous AK-01 jobs and outcomes.
Contains:
- prior capsule builds
- failed attempts
- reviewer corrections
- recovery incidents
- successful patterns

Use:
case retrieval and improvement analysis.

## 3. Semantic Memory
Scope: AK-01 own reusable knowledge.
Contains:
- knowledge engineering
- RAG
- agent engineering
- evidence engineering
- procedure/checklist engineering
- evaluation
- security principles

This is AK-01's own professional knowledge base.

## 4. Procedural Memory
Scope: how AK-01 performs work.
Contains:
- extraction workflows
- normalization rules
- graph build procedures
- RAG design procedures
- prompt design procedures
- gap analysis procedures
- escalation procedures

Procedural memory is versioned and testable.

## 5. Audit Memory
Scope: immutable history.
Contains:
- who/what changed
- source and input hashes
- policy versions
- approvals
- failures
- deltas
- qualification decisions

## Rules
- Working memory may be ephemeral.
- Semantic/procedural memory changes require versioning.
- Audit memory is append-only.
- Episodic memory cannot silently become semantic truth.
- Production traces must pass review before promotion into reusable knowledge.
