# AK-01 — Security Threat Model

Owner: SA-01 Security Architect

## Assets
- source corpus
- source versions and hashes
- knowledge units
- knowledge graph
- provenance ledger
- prompts and policies
- RAG indexes
- specialist capsules
- secrets/credentials
- audit events
- qualification records

## Trust boundaries
1. User / external source → AK-01 intake
2. Source content → parser/extractor
3. LLM provider → AK-01
4. AK-01 → tools / storage
5. AK-01 → target-agent namespaces
6. AK-01 → AKN-01 / AT-01 / QA / POLYGON
7. CI/CD → production runtime

## Threat classes

### Spoofing
- forged source identity
- forged reviewer identity
- forged agent namespace

### Tampering
- source mutation
- provenance tampering
- graph corruption
- capsule overwrite
- event/audit manipulation

### Repudiation
- unlogged knowledge change
- untraceable qualification decision

### Information Disclosure
- cross-agent leakage
- secret exposure
- source content leakage to external LLM

### Denial of Service
- oversized documents
- graph explosion
- prompt bombs
- provider exhaustion
- queue saturation

### Elevation of Privilege
- AK-01 self-qualification
- tool permission escape
- namespace escape
- policy override through prompt injection

## AI-specific threats
- prompt injection
- indirect prompt injection
- RAG poisoning
- retrieval manipulation
- malicious embeddings/index entries
- model hallucination with false provenance
- unsafe tool calls
- context poisoning
- stale knowledge used as current truth

## Mandatory controls
- source-as-data isolation
- least privilege
- namespace isolation
- source hashing/versioning
- immutable audit
- schema validation
- trust/evidence filters
- reviewer gates
- tool allowlists
- secret isolation
- model/provider routing policy
- timeout/rate limits
- content size/depth limits
- dependency/SBOM scanning
- rollback to last known good capsule

## Residual-risk rule
Any unmitigated SEV-1 threat blocks release.
