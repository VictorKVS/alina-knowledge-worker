# FATHER / ALINA Knowledge Analysis Engine

## Goal

Build a universal engine that can accept heterogeneous information, determine what kind of source it is, select the correct analysis strategy, decompose the source into typed knowledge, preserve provenance and feed specialized digital experts.

## Reference pipeline

```text
SOURCE
  ↓
1. SOURCE IDENTIFICATION
  ↓
2. SOURCE CLASSIFICATION
  ↓
3. DOMAIN / GENRE / SUBDOMAIN CLASSIFICATION
  ↓
4. ANALYSIS PROFILE SELECTION
  ↓
5. DEPTH ROUTING (A0–A5)
  ↓
6. SPECIALIZED EXTRACTION
  ↓
7. NORMALIZATION
  ↓
8. ENTITY / EVENT / CLAIM / RELATION GRAPH
  ↓
9. EVIDENCE LINKING
  ↓
10. WEIGHTING
  ↓
11. CRITIC / CONTRADICTION CONTROL
  ↓
12. DOMAIN KNOWLEDGE STORE
  ↓
13. SPECIALIST REASONING
```

## 1. Source identification

Identify format and basic metadata without deep reasoning:

- file / URL / message / repository / dataset;
- MIME / extension;
- author / publisher where available;
- date;
- language;
- version;
- checksum;
- acquisition timestamp.

Output: `SourcePassport`.

## 2. Source classification

Primary classes:

- fiction;
- scientific;
- educational;
- professional;
- regulatory;
- technical documentation;
- web;
- news / media;
- OSINT / CTI;
- code;
- dataset;
- report;
- mixed.

Classification is probabilistic, not a forced single label.

Example:

```json
{
  "source_type": {
    "fiction": 0.88,
    "historical": 0.42
  }
}
```

## 3. Domain classification

Independent from format.

A PDF can belong to security, medicine, physics, law, economics or several domains simultaneously.

## 4. Analysis profile selection

Profiles are executable analytical contracts.

A profile defines:

- knowledge types to extract;
- entities;
- relations;
- validation rules;
- weights;
- tools;
- preferred models;
- critic;
- output schema.

Example:

```yaml
profile: security.regulation
extract:
  - requirement
  - subject
  - object
  - condition
  - exception
relations:
  - applies_to
  - requires
  - supersedes
weights:
  - authority
  - applicability
  - freshness
```

## 5. A0–A5 depth routing

### A0 — Identify
Metadata and source passport.

### A1 — Extract
Explicit entities, terms, requirements, events.

### A2 — Structure
Relations, hierarchy, timeline and graph structure.

### A3 — Semantics
Interpretation, meaning, motives and implications.

### A4 — Expert analysis
Causal analysis, risk, contradictions and domain decisions.

### A5 — Synthesis / prediction
New conclusions, recommendations, scenarios and predictions.

The router decides the cheapest sufficient depth for each fragment or query.

## 6. Canonical knowledge model

The canonical layer should support:

```text
ENTITY
EVENT
FACT
CLAIM
RULE
REQUIREMENT
RELATION
CAUSE
HYPOTHESIS
OPINION
PROCEDURE
METHOD
RISK
CONTROL
EVIDENCE
PREDICTION
```

Domain-specific types extend this model rather than replacing it.

## 7. Provenance

Every knowledge node should retain:

```text
source_id
fragment_id
location
extraction_method
timestamp
model/tool version
confidence
verification status
```

## 8. Weight engine

No single universal `weight`.

Generic dimensions:

- confidence;
- authority;
- relevance;
- freshness;
- applicability;
- impact;
- evidence strength.

Profiles can add domain-specific weights.

## 9. Contradiction control

The engine must distinguish:

- duplicate;
- supporting;
- conflicting;
- superseding;
- uncertain;
- not comparable.

Conflicts are first-class objects, not text that disappears into embeddings.

## 10. Specialist handoff

The knowledge engine does not itself have to become every expert.

It produces an evidence-linked state that a specialist can consume:

```text
KNOWLEDGE STATE
+ COMPETENCY PACK
+ TOOLS
+ WORKFLOW
+ BRAIN
=
SPECIALIST
```

## Design objective

The core value is not parsing alone. It is the combination:

```text
classification
+ analytical routing
+ typed knowledge
+ evidence
+ domain profiles
+ qualification
```
