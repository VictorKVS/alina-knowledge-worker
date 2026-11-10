# AK-01 — Component API & Handoff Map

## 1. External API

### API Gateway
Receives:
- TargetAgentProfile
- SourceSet
- EvidencePolicy
- ExtractionPolicy
- RuntimeConstraints

Returns:
- job status
- blueprint/capsule
- graph
- gaps
- contradictions
- procedures/checklists
- RAG spec
- prompt package

## 2. Internal service contracts

### Target Agent Profiler
Input:
- role
- tasks
- goals
- constraints

Output:
- capability map
- required knowledge domains
- prerequisite graph seed

### Source Intake
Input:
- source descriptor
- file/URL/content handle

Output:
- SourceVersion
- SourceFragments
- source hash
- metadata

### Knowledge Extractor
Input:
- SourceFragments
- target capability map

Output:
- candidate KnowledgeUnits

### Epistemic Classifier
Input:
- KnowledgeUnit candidate

Output:
- epistemic type
- confidence
- classification rationale

### Entity Normalizer
Input:
- concepts/entities/aliases

Output:
- canonical entities
- alias map
- unresolved candidates

### Evidence Linker
Input:
- claims
- source fragments

Output:
- support links
- counter-evidence links
- provenance chain

### Contradiction Engine
Input:
- normalized claims

Output:
- contradiction records
- unresolved conflict groups

### Graph Builder
Input:
- units
- relations
- evidence

Output:
- graph nodes
- typed edges
- graph version

### Weight Policy Engine
Input:
- graph
- target agent
- policy config

Output:
- contextual ranking attributes
- composite score only if policy defines it

### Procedure Builder
Input:
- methods
- algorithms
- decision rules
- constraints

Output:
- procedures
- stop conditions
- escalation conditions

### Checklist Builder
Input:
- procedures
- validation rules
- risks

Output:
- pre/during/post checklists

### RAG Architect
Input:
- corpus
- graph
- metadata
- target tasks
- trust policy

Output:
- retrieval topology
- filters
- reranking policy
- citation policy

### Prompt Architect
Input:
- role
- procedures
- evidence policy
- tools
- escalation

Output:
- layered prompt package

### Gap Detector
Input:
- target capability map
- current knowledge graph
- evaluation requirements

Output:
- unknowns
- missing sources
- missing procedures
- missing tools

### Capsule Composer
Input:
- all approved artifacts

Output:
- Agent Knowledge Blueprint
- Knowledge Capsule draft

### Knowledge Delta Engine
Input:
- QA failures
- production traces
- local corrections
- new sources

Output:
- delta proposal
- impact map
- retraining scope
