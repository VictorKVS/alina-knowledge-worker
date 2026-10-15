# FATHER Visual Agent Designer — technology selection

Status: proposal / not implemented

## Decision
Use @xyflow/react (React Flow, MIT) as the editable graph canvas; retain FATHER-owned node contracts, validation, authorization and execution engine. Do not copy screenshots, proprietary UI assets, or n8n source into the commercial platform.

## Evaluated
- xyflow/xyflow: MIT; preferred node UI foundation.
- n8n-io/n8n: source-available Sustainable Use License; commercial embedding/white-labeling requires license review; use as functional reference only.
- retejs/rete: MIT core, selected advanced plugins have non-commercial restrictions; alternative if dataflow evaluation becomes central.

## User-provided visual references
Dark technical dashboard, luminous workflow edges, status-colored nodes, sidebar palette, inspector, execution log, metrics, responsive canvas. Implement original visuals, not copied artwork.

## Canvas MVP
Node registry: Trigger, Input, Parser, Router, ALINA Lead, Source Scout, RAG, Graph, Model, Tool/MCP, Evidence, Critic, Evaluator, Approval, Output.
Node metadata: node_id, type, version, input/output JSON schema, permissions, timeout, retry, budget, provenance, owner.
UI: add/move/connect nodes, validation, inspector, save/load JSON, execution trace, error states.
Execution: graph validator -> approved orchestrator -> policy gateway -> isolated tools; no direct browser-to-tool execution.
Security: deny-by-default, no credentials in graph JSON, scope controls, audit, prompt injection tests, no live Red Team execution before lab gates.

## Milestones
1. Existing frontend/repository audit; avoid duplicate app.
2. UX wireframe + node registry schema + ADR.
3. React Flow canvas MVP with mock execution and test fixtures.
4. Backend integration with ALINA core and Evidence Store.
5. CyberED workflow, then controlled Cyber Range nodes after authorization gates.

## Acceptance
Save/load graph roundtrip, cycle/type validation, explicit permissions, mock run with reproducible trace, no unauthorized tool invocation, accessible inspector, CI evidence.
