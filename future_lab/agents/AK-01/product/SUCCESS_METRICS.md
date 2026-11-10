# AK-01 — Product Success Metrics

## North Star
**Verified Knowledge Blueprint Yield (VKBY)**

Share of target-agent jobs that produce a complete, schema-valid, evidence-traceable blueprint accepted by downstream architecture review.

## Quality metrics
- provenance coverage
- unsupported claim rate
- contradiction recall
- duplicate-node rate
- orphan-node rate
- knowledge coverage
- retrieval grounding pass rate
- stale-source detection rate
- schema validation rate

## Efficiency metrics
- analyst time saved per target agent
- time-to-first-blueprint
- knowledge units extracted per hour
- cost per processed source
- tokens per knowledge unit
- rework rate

## Reliability metrics
- job success rate
- retry rate
- deterministic replay variance
- parser failure rate
- vector/graph indexing failure rate

## Security metrics
- prompt-injection escape rate
- cross-agent leakage incidents
- unauthorized-write attempts blocked
- poisoned-source detections
- citation verification failures

## MVP thresholds
- schema validity: 100%
- unsupported factual claims in golden suite: 0
- provenance coverage: >=95%
- contradiction preservation: 100% on benchmark
- retrieval grounding: >=90%
- target-task coverage: >=90%
