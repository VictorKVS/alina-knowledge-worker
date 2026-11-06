# ALINA — Evidence-First Knowledge Analyst

> **From documents to structured, verifiable expertise.**  
> ALINA is an experimental knowledge-analysis system for turning heterogeneous sources into structured knowledge, evidence-linked graphs, domain-specific analysis profiles, and eventually qualified digital specialists.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Primary%20runtime-Windows-0078D6?logo=windows&logoColor=white)](#current-runtime)
[![Status](https://img.shields.io/badge/status-active%20R%26D-7C3AED)](#project-status)
[![Architecture](https://img.shields.io/badge/architecture-evidence--first-0F766E)](docs/architecture/KNOWLEDGE_ANALYSIS_ENGINE.md)
[![Pages](https://img.shields.io/badge/demo-GitHub%20Pages-222?logo=github)](https://victorkvs.github.io/alina-knowledge-worker/)

---

## Why ALINA exists

Most AI knowledge systems still follow a simplified pattern:

```text
documents → chunks → embeddings → RAG → answer
```

ALINA explores a deeper model:

```text
SOURCE
  ↓
IDENTIFY
  ↓
CLASSIFY
  ↓
DOMAIN / GENRE / SUBDOMAIN
  ↓
SELECT ANALYSIS PROFILE
  ↓
A0–A5 ANALYSIS DEPTH
  ↓
DECOMPOSE INTO KNOWLEDGE ATOMS
  ↓
ENTITIES + EVENTS + CLAIMS + RELATIONS + EVIDENCE
  ↓
KNOWLEDGE GRAPH + RETRIEVAL
  ↓
CRITIC / VERIFICATION
  ↓
DOMAIN EXPERT
```

The goal is not merely to retrieve passages. The goal is to preserve **what a source says, what kind of knowledge it contains, how claims are connected, how reliable they are, and which expert workflow should process them**.

---

## Core idea: one engine, many analysis profiles

ALINA should not analyze a novel, a scientific paper, a regulation, a threat report and source code with the same algorithm.

The architecture separates a universal knowledge pipeline from domain-specific profiles:

```text
UNIVERSAL KNOWLEDGE ENGINE
        +
ANALYSIS PROFILE
        =
SPECIALIZED ANALYST
```

Examples:

```text
general engine + fiction.detective
general engine + fiction.science_fiction
general engine + science.paper
general engine + security.regulation
general engine + security.threat_report
general engine + code.repository
```

A source may activate several profiles at once. A military science-fiction novel can combine narrative, science-fiction, military and political-analysis modules instead of being forced into one label.

See:
- [Knowledge Analysis Engine](docs/architecture/KNOWLEDGE_ANALYSIS_ENGINE.md)
- [Source & Profile Matrix](docs/architecture/SOURCE_PROFILE_MATRIX.md)
- [Engineering Principles](docs/principles/PRINCIPLES.md)

---

## Analysis depth: A0 → A5

ALINA uses a staged model so expensive reasoning is applied only where needed.

| Level | Purpose | Typical output |
|---|---|---|
| **A0 — Identify** | What is this source? | type, author, date, language, version |
| **A1 — Extract** | What is explicitly present? | entities, terms, events, requirements |
| **A2 — Structure** | How is it connected? | relations, timelines, graph edges |
| **A3 — Semantics** | What does it mean? | interpretation, motives, implications |
| **A4 — Expert analysis** | What follows in this domain? | risks, contradictions, causal chains |
| **A5 — Synthesis** | What new conclusion can be justified? | scenarios, recommendations, prediction |

This is intentionally different from sending every page directly to the largest LLM.

---

## Knowledge is typed, not just chunked

A useful knowledge base needs more than text fragments.

ALINA's target knowledge model includes:

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

Every important knowledge node should retain provenance:

```text
source
source fragment
source class
confidence
authority
freshness
applicability
relations
evidence
```

The system should be able to explain **why** a conclusion exists, not only produce it.

---

## Domain examples

### Fiction & narrative analysis

A common narrative core:

```text
CHARACTERS
EVENTS
LOCATIONS
OBJECTS
TIMELINE
RELATIONS
CAUSES
CONSEQUENCES
MOTIVES
BELIEFS
SECRETS
CONFLICTS
CLUES
PLOT THREADS
```

Then genre-specific modules add their own logic.

**Detective:** suspects, clues, alibis, lies, motive, probability of guilt.  
**Science fiction:** technology, scientific assumptions, constraints, plausibility, second-order effects.  
**Drama:** relationships, emotional state, conflict, moral dilemmas, turning points.  
**Military fiction:** forces, objectives, logistics, command decisions, tactics and consequences.

### Information security

The same engine can process a very different knowledge schema:

```text
LAW / STANDARD / REQUIREMENT
        ↓
APPLICABILITY
        ↓
SYSTEM / ASSET / INFORMATION
        ↓
THREAT / ATTACK SCENARIO
        ↓
RISK
        ↓
CONTROL
        ↓
IMPLEMENTATION
        ↓
VERIFICATION / EVIDENCE
```

This allows a future ALINA Security expert to reason across regulatory requirements, technical controls, threat intelligence and implementation evidence instead of treating them as unrelated document folders.

### Scientific literature

```text
RESEARCH QUESTION
HYPOTHESIS
METHOD
DATA
EXPERIMENT
RESULT
LIMITATION
CLAIM
CITATION
REPRODUCIBILITY
```

---

## Current runtime

The repository already contains a working local document-processing layer.

Current capabilities include:

- local background document processing;
- SQLite + FTS5 storage;
- provenance-preserving text fragments;
- queue state and resumable processing;
- TXT / MD / JSON / YAML ingestion;
- PDF chunked processing with saved position;
- Windows OCR fallback for scans;
- EPUB / FB2 / RTF / DOC handling;
- local web dashboard;
- structured process definitions and execution states;
- Windows-oriented installation and supervision scripts;
- test suite and CI support.

Important: **the current runtime is not yet the complete ALINA analytical architecture described above**. The repository distinguishes implemented ingestion/runtime capabilities from the research architecture under active development.

---

## Project status

```text
DOCUMENT INGESTION           ████████████████████  implemented
LOCAL INDEX / PROVENANCE     ████████████████████  implemented
PROCESS ENGINE               ████████████████████  implemented

SOURCE CLASSIFICATION        ███████░░░░░░░░░░░░░  design / R&D
ANALYSIS PROFILE REGISTRY    ███████░░░░░░░░░░░░░  design / R&D
A0–A5 DEPTH ROUTING          ██████░░░░░░░░░░░░░░  design / R&D
KNOWLEDGE GRAPH              ██████░░░░░░░░░░░░░░  design / R&D
WEIGHT ENGINE                █████░░░░░░░░░░░░░░░  design / R&D
DOMAIN EXPERT QUALIFICATION  ████░░░░░░░░░░░░░░░░  design / R&D
```

These percentages are roadmap indicators, not benchmark claims.

---

## Relation to FATHER

ALINA is designed as a specialist layer that can be produced and qualified by the broader **FATHER expert factory** architecture.

The separation is deliberate:

```text
SPECIALIST
  ├── role
  ├── competency pack
  ├── knowledge graph
  ├── workflows
  ├── tools
  ├── tests
  ├── evidence
  └── BRAIN SLOT
```

The LLM is a replaceable brain, not the specialist itself. A future model can replace the current model only after passing the specialist's qualification suite.

---

## Research notes & articles

### Architecture
- [Knowledge Analysis Engine](docs/architecture/KNOWLEDGE_ANALYSIS_ENGINE.md)
- [Source & Analysis Profile Matrix](docs/architecture/SOURCE_PROFILE_MATRIX.md)

### Principles
- [ALINA Engineering Principles](docs/principles/PRINCIPLES.md)

### Research
- [World Landscape: parsers, GraphRAG, domain knowledge and expert systems](docs/research/WORLD_LANDSCAPE.md)

### Articles
- [From RAG to Verified Digital Expert](docs/articles/01_FROM_RAG_TO_VERIFIED_EXPERT.md)

### Media
- [Media Kit & Social Positioning](docs/media/MEDIA_KIT.md)

---

## Public demo

Prepared demo:

**https://victorkvs.github.io/alina-knowledge-worker/**

The public Pages demo is a presentation layer. The local document-processing service remains local by design and should not be exposed directly to the Internet without separate authentication and deployment hardening.

---

## Local start

Requires Python 3.11+ on Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item config.example.json config.json
.\.venv\Scripts\python.exe alina.py --serve
```

Open:

```text
http://127.0.0.1:8768
```

Install as a background Windows process:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
```

Run tests:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s . -p "test_*.py" -v
```

---

## Research direction

The long-term target is:

```text
ANY SOURCE
  ↓
understand what it is
  ↓
choose the correct analytical method
  ↓
decompose it into typed knowledge
  ↓
preserve evidence and uncertainty
  ↓
connect knowledge into a graph
  ↓
apply domain-specific reasoning
  ↓
qualify the specialist on real tasks
```

**ALINA is not intended to be another chat interface over a folder of PDFs.  
It is an attempt to engineer verifiable digital expertise.**

---

## License / usage

This repository is currently an active research and engineering project. Before commercial reuse or redistribution, review the repository's licensing status and the licenses of any external components integrated in future versions.

---

Maintained by **VictorKVS**.
