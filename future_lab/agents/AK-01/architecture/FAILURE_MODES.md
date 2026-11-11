# AK-01 — Failure Modes, Reactions and Recovery

| Failure | Detection | Immediate Reaction | Recovery | Escalation |
|---|---|---|---|---|
| LLM timeout | timeout | retry with backoff | alternate provider/model | after N retries |
| malformed structured output | schema validator | repair once | rerun extraction | repeated failure |
| source parse failure | parser exception | quarantine source | alternate parser | unsupported format |
| source hash mismatch | checksum | stop ingestion | re-fetch/re-upload | possible tampering |
| prompt injection in source | injection detector/policy | isolate instructions as data | continue with sanitized context | security event |
| duplicate entity merge risk | merge confidence | do not merge automatically | create review task | curator |
| contradictory claims | contradiction engine | retain both | contextual resolution | curator/domain expert |
| vector index unavailable | health check | degrade to sparse+graph | rebuild index | ops |
| graph store unavailable | health check | read cached snapshot | restore/replay | ops |
| database unavailable | health check | stop writes | fail safe | ops |
| event bus unavailable | publish failure | local outbox | replay later | ops |
| provenance missing | validator | block approval | repair source links | curator |
| unsupported claim | evidence validator | mark UNVERIFIED | seek source | curator |
| stale source | freshness rule | flag affected nodes | delta analysis | domain owner |
| RAG retrieves low-trust source | trust filter | demote/block | fallback trusted corpus | none unless persistent |
| capsule review rejected | reviewer | freeze release | rework impacted stages | architect |
| production failure in target agent | QA/trace | preserve trace | root-cause classify | delta engine |
| critical delta impacts many nodes | impact analysis | freeze auto-release | broad regression suite | FATHER gate |

## Failure policy

1. Fail closed for provenance/security/qualification.
2. Fail degraded for retrieval if safe alternatives exist.
3. Never silently drop contradictions.
4. Never auto-promote knowledge after a recovery.
5. Every failure must produce an auditable event.
