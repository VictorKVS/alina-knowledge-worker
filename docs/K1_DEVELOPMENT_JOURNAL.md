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


## 2026-09-28 — K1 autonomous project hardening

### Architecture change
K1 is no longer only a validator of pre-created artifacts. The new k1_autoproject.py can build missing approved derived layers from the existing local inventory and document catalog, then validate them before continuing.

### Automatic path
K1.0 discovery -> K1.3A Master Registry build/upsert -> K1.3B identity candidates -> K1.4 document-corpus import/upsert -> invariant checks -> K1.5A legal registry -> K1.5C semantic legal pilot -> K1.5D official-verification queue.

### Safety decisions
- originals are read-only;
- no automatic delete/move/rename;
- derived registry writes are atomic;
- prior derived files are backed up before replacement;
- source identity is anchored to full SHA-256 while legacy SRC-* IDs remain compatible;
- raw titles are preserved; normalized titles remain candidates;
- copy IDs and legal-document IDs are collision-safe on reruns;
- official-verification tasks are upserted instead of replacing the queue.

### Human-gate policy
Automation stops only for a genuine unresolved dependency:
- required inventory path cannot be discovered;
- no accessible legal PDF is available;
- PDF requires OCR/extractor repair;
- official source/current revision/legal status is not verified;
- an invariant violation would make continued writes unsafe.

### Metrics policy
Recorded: stage time, records read/written, created/updated/skipped, warnings/errors, throughput, review pressure, automation yield, run history and relative speed against a comparable prior run.

Not inferred without evidence: speedup versus a one-stream baseline, rework ratio, or ETA.

### Validation added
Synthetic tests cover idempotent master import, idempotent document import, mojibake repair, duplicate-path invariant blocking, legal metadata extraction without status promotion, official human gate, and NO_DATA handling for unsupported metrics.
