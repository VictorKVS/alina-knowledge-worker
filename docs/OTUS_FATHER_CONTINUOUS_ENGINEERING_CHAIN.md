# OTUS → FATHER Continuous Engineering Document Chain

Status: ACTIVE C0 POLICY

All OTUS stages and FATHER implementation stages are treated as one traceable engineering history. Calculations and decisions are appended in dependency order rather than rewritten as isolated homework answers.

## Canonical chain
`OTUS task/source → requirements → assumptions → input data → formulas → calculations → result → architecture decision → FATHER implementation → tests/benchmark → actual metrics → plan-vs-fact → risks/security → cost/TCO → Decision Memory → next stage`

## Mandatory artifact links
Each stage should retain:
- source lesson/homework ID and version;
- requirements and acceptance criteria;
- input dataset/parameters and units;
- formulas and calculation method;
- calculated values and uncertainty/reserve coefficients;
- architecture impact and ADR/decision link;
- implementation artifact/repository/commit;
- test/evaluation evidence;
- measured actual values when available;
- plan-vs-fact delta;
- security, reliability and cost consequences;
- conclusions and downstream dependencies.

## Sizing-specific continuity
CPU, RAM, GPU/VRAM, storage, network, RPS/concurrency, latency/SLO, model context, tokens, inference throughput, growth, redundancy/HA, headroom, utilization, power where relevant, infrastructure price and TCO are versioned inputs/results. Later OTUS stages consume earlier verified values instead of silently inventing new baselines.

## FATHER rule
A homework result becomes FATHER knowledge only through provenance and verification. Educational assumptions remain marked as assumptions until measured. Production facts never inherit certainty from a homework calculation.

## Document order
Documents should be assembled in chronological/dependency order so the final pack explains how FATHER evolved:
1. task and source;
2. analysis;
3. calculations;
4. architecture;
5. security/reliability;
6. implementation;
7. tests/evaluation;
8. actual measurements;
9. decision memory;
10. next-stage inputs.

## ALINA / Agent Zoo responsibilities
- Inventory Agent finds OTUS/FATHER artifacts.
- Schema Agent extracts structured calculation/decision fields.
- History Agent reconstructs dependency order.
- Analyst checks assumptions and units.
- Architect maps calculations to FATHER decisions.
- Critic searches contradictions and stale baselines.
- Evaluation checks reproducibility.
- ALINA Lead appends verified results to the continuous engineering chain.

No historical calculation is deleted merely because a newer value exists; it is superseded with provenance.
