# World Landscape — Components ALINA Can Learn From

ALINA should not reimplement mature infrastructure when good open-source components already exist. The differentiating layer should be analysis routing, knowledge schemas, evidence and expert qualification.

## Document ingestion

### Docling
GitHub: https://github.com/docling-project/docling

Useful for:
- PDF and office-document understanding;
- layout-aware conversion;
- tables and structured document representation;
- canonical ingestion before ALINA classification.

### Unstructured
GitHub: https://github.com/Unstructured-IO/unstructured

Useful for:
- partitioning heterogeneous documents;
- metadata extraction;
- document-element pipelines.

## Scientific literature

### GROBID
GitHub: https://github.com/kermitt2/grobid

Useful for:
- scientific PDF structure;
- authors and affiliations;
- sections;
- citations and references.

ALINA can place a scientific analysis profile above this extraction layer.

## Narrative analysis

### BookNLP
GitHub: https://github.com/booknlp/booknlp

Useful for:
- character/entity extraction;
- coreference;
- quotation and speaker attribution;
- event-oriented literary NLP.

ALINA's target layer goes further into motives, beliefs, causal structures, secrets, plot threads and genre-specific reasoning.

## Graph-oriented retrieval

### Microsoft GraphRAG
GitHub: https://github.com/microsoft/graphrag

Useful concepts:
- entity and relation extraction;
- claims;
- graph-based corpus representation;
- hierarchical summarization.

### LightRAG
GitHub: https://github.com/HKUDS/LightRAG

Useful concepts:
- knowledge graph + vector retrieval;
- separate model roles in the pipeline;
- graph-aware retrieval strategies.

## Routing and composability

### LlamaIndex
GitHub: https://github.com/run-llama/llama_index

Useful concepts:
- router/query-engine selection;
- composable retrieval systems;
- metadata-driven routing.

ALINA extends the routing idea from "which retriever?" to "which analytical method and knowledge schema?"

## Security knowledge

### MITRE ATT&CK CTI
GitHub: https://github.com/mitre-attack/attack-stix-data

Useful for:
- machine-readable threat entities;
- techniques;
- relationships;
- STIX-based cyber knowledge.

### OpenCTI
GitHub: https://github.com/OpenCTI-Platform/opencti

Useful for:
- cyber threat knowledge graphs;
- relationships;
- sources;
- confidence;
- temporal context.

### NIST OSCAL
GitHub: https://github.com/usnistgov/OSCAL

Useful pattern:
- machine-readable security controls;
- implementation and assessment data;
- structured compliance artifacts.

## What ALINA adds

The open-source landscape contains strong components, but the project target is the orchestration layer:

```text
SOURCE CLASSIFICATION
+ DOMAIN / GENRE TAXONOMY
+ ANALYSIS PROFILE REGISTRY
+ A0–A5 DEPTH ROUTING
+ TYPED KNOWLEDGE
+ DOMAIN-SPECIFIC WEIGHTS
+ EVIDENCE / PROVENANCE
+ CRITIC / CONTRADICTION CONTROL
+ SPECIALIST QUALIFICATION
```

The goal is not to replace Docling, GROBID, BookNLP, STIX, GraphRAG or similar systems.

The goal is to make them possible components of a larger evidence-first expert-engineering pipeline.
