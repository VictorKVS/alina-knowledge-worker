# ALINA Analyst — Module Boundary

Status: scope decision.

## In scope (this workstream only)
Task intake; investigation planning; source/document ingestion through existing services; evidence and provenance; hypothesis/contradiction analysis; knowledge graph views; verification and evaluation; reporting and decision memory; Analyst-only visual workflow editor.

## External dependencies (interfaces only)
FATHER core, shared Knowledge Core/RAG, Agent Zoo, OSINT, Cyber Range/Red Team/Blue Team, deployment infrastructure and general-purpose platform dashboard. Do not implement or duplicate these systems in this workstream.

## Visual workflow nodes
Task -> Plan -> Sources -> Evidence -> Graph/Reasoning -> Verify -> Report -> Decision Memory.
Optional external-tool node uses a versioned interface with explicit authorization, never embeds external agent implementations.

## Delivery order
1. Analyst workflow schema and UI wireframe.
2. Analyst-only canvas with save/load and validation.
3. Mock end-to-end research run and tests.
4. Real adapters to approved shared services.
5. Evaluation and release evidence.

## Acceptance
Analyst-only functionality demonstrable end-to-end; provenance and uncertainty explicit; no unauthorized tool invocation; no unrelated FATHER modules introduced.
