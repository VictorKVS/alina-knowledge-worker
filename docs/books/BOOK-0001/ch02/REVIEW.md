# BOOK-0001 / Chapter 2 — ALINA Review Notes

## Core lesson

Pre-training data is not background metadata. It is part of the model's engineering risk profile.

## Chapter-to-FATHER transformation

```text
RAW SOURCES
  ↓
EXTRACT / CLEAN
  ↓
LANGUAGE ID
  ↓
QUALITY FILTER
  ↓
DEDUP
  ↓
PII REMEDIATION
  ↓
BENCHMARK DECONTAMINATION
  ↓
DATA MIXTURE
  ↓
ORDERING
  ↓
DATASET EVIDENCE
```

## High-value implementation reference mentioned by the source

- Hugging Face DataTrove — candidate for later repository scouting.
- Current status: SOURCE-MENTIONED ONLY.
- Do not mark REUSE/ADAPT until license, architecture, maintenance, security and integration fit are reviewed.

## ALINA learning corrections

1. Do not treat "cleaner data" as a single dimension.
2. Keep privacy, bias, duplication and benchmark contamination as separate concerns.
3. Do not infer that removing more data always improves quality.
4. Record preprocessing-induced distribution shift as a risk.
5. Data transparency belongs in model selection evidence.
