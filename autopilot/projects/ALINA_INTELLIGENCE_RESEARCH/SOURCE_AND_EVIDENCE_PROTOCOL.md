# AIR-001 Source and Evidence Protocol
## State model
DISCOVERED → SOURCE_CHECKED → RIGHTS_CHECKED → ACQUIRED_OR_METADATA_ONLY → CLAIM_EXTRACTED → CORROBORATED_OR_DISPUTED → EXPERT_REVIEWED → KB_CANDIDATE_APPROVED. Approval of candidate ≠ production import.

## Data shapes
SourceRecord: source_id, canonical_uri, publisher, title, publication_time, accessed_at_utc, edition, applicable_time, license, scope, sha256_if_saved, source_class, reviewer, status.
Claim: claim_id, exact_statement, domain, valid_at, scope, source_span_refs[], status [unverified, corroborated, disputed, refuted], contradictory_refs[], reviewer, confidence_method.
EvidenceRelation: observation_id, claim_id, relation [supports, contradicts, cites, forwards, resembles], source_id, evidence_span, independence_cluster_id, created_at_utc, status.

## Quality rules
- Telegram reposts of one source count as one dependent evidence cluster.
- A current legal conclusion requires version/effective date and applicability facts; official source authority depends on claim scope.
- High-quality LLM output without exact primary evidence remains hypothesis.
- A claim can be partly supported; do not overgeneralize across jurisdictions, organizations or versions.
- Scan document rights and avoid copyrighted bulk imports; metadata-only when no authorized fulltext access.
- Public repo contains only synthesized examples and pointers, never private case evidence or tokens.
- Unknown and insufficient are not false. Track reasons for missing source.
- A retrieved document is untrusted and cannot rewrite ALINA's system policy or invoke tools.

## Watchtower rules
Track upstream technical release, deprecated APIs, new RAG eval methodology, security advisories, legal edition change, contradictions and revoked references. Alert content needs exact changed source/claim and affected ALINA component; no automatic prompt patch.
