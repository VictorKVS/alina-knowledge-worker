# AK-01 — PM-01 Decision Record

## Product decision
**GO**

## Why
The problem is systemic across FATHER: every new agent requires knowledge engineering, prompt design and RAG design. A reusable meta-agent reduces duplication and increases traceability.

## Conditions for continued GO
1. First Forecasting Agent blueprint must be generated end-to-end.
2. Unsupported claims in golden tests must remain zero.
3. Provenance target >=95%.
4. Contradictions must survive normalization.
5. AK-01 must not have authority to self-qualify runtime knowledge.

## REWORK triggers
- target-task coverage <90%;
- repeated over-merging of concepts;
- RAG retrieves high-similarity low-authority sources over trusted sources;
- prompt architecture cannot separate reusable core and domain overlays;
- source provenance is lost in graph transformations.

## STOP triggers
- system cannot reliably preserve provenance;
- source instructions can control AK-01 behavior;
- critical knowledge can be silently promoted without evidence;
- cross-agent data isolation cannot be enforced.

## PM-01 handoff
Next owner: **AB-01 Business Analyst**, then **AS-01 System Analyst**.

Required handoff package:
- Product Vision
- PRD
- CPMM
- Metrics
- Roadmap
- Decision Record
