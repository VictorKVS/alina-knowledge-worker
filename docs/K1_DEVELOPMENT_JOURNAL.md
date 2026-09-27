# ALINA / FATHER — Development Journal

## 2026-09-27 — K1 automation experiment

### Decision
The approved K1 source-ingestion logic is converted from manual one-step commands into a measurable automated pipeline. The pipeline stops at the first point where a human decision or authoritative external verification is required.

### Approved automatic path
1. K1.3A — validate Master Source Registry.
2. K1.3B — validate identity-preparation layer.
3. K1.4 — validate document-corpus import state.
4. K1.5A — validate legal-document registry.
5. K1.5C — validate semantic legal metadata candidate.
6. K1.5D — stop at Official Verification Gate unless official source, current revision and legal status are verified.

### First planned human gate
Legal/official verification. A local PDF, filename or high confidence score is not enough to assert that a regulatory document is currently effective.

### Metrics introduced
Each run records stage duration, records observed, PASS/WARN/BLOCKED/HUMAN_GATE, warnings/errors, automation yield, first human gate and validation throughput.

No invented acceleration or completion forecast is allowed. Speed-up, rework ratio and ETA are shown as NO_DATA until comparable telemetry exists.

### Approach comparison
The dashboard compares expectation versus observed evidence for:
- reuse of prior audits instead of rescans;
- SHA-256 deduplication;
- candidate-first identity resolution;
- authoritative-source gate for legal status.

### Data policy
Actual books, extracted passages, private registries and runtime journals stay under local data/ and are not committed. Git contains code, plans and schemas only.
