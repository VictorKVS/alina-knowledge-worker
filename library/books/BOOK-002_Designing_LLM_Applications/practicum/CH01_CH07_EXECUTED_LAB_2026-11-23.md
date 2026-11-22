# FATHER / ALINA — CH01–CH07 practical lab evidence

**Executed:** 2026-11-23; synthetic, controlled, local Python. **Qualification status: NOT_QUALIFIED**.
  
## Results (actually executed)

| Scope | Result | Notes |
|---|---:|---|
| BPE toy merge (CH03) | 4/4 PASS | tests of original uploaded lab code |
| Attention/loss/perplexity toy (CH04) | 6/6 PASS | numerical tests of original code |
| Greedy/top-k/top-p toy (CH05) | 6/6 PASS | distribution given externally, not LLM |
| Document integrated suite | 8/8 PASS | 20 synthetic docs, SHA256, SQLite and char TF-IDF |
| Document classification | 20/20 exact for **easy constructed scenarios** | NOT extrapolatable to real data |
| SQLite persistence + JSON schema | 20 records + 20 valid JSON | schema cannot verify facts |
| Retrieval | relevant IB topic at top-1 | char-ngrams TF-IDF, duplicates not filtered |
| Actual tiny causal Transformer training | CE 2.963867 → 0.262216 | 100 steps, synthetic repetitive training-overlapping data, CPU; **not production LLM** |
| Actual low-rank matrix update | MSE 9.625332 → ~0 | training 20 adapter parameters, base 24 frozen; NOT LLM LoRA |
| SentencePiece (freshly trained BPE) | 25 tokens; roundtrip exact | synthetic corpus, not pretrained model tokenizer |

**Positive unit/integration tests: 24/24 PASS. Separately designed adversarial checks: 3/3 FAIL.** Never combine these into an unqualified "all tests passed" claim.

## Adversarial FAIL findings

- **FAIL-01**: accepting untrusted `previous_id` lets unrelated text be classified as NEW_VERSION.
- **FAIL-02**: SHA256 content equality does not establish source authenticity or rights.
- **FAIL-03**: retrieval returns duplicates as multiple top-k sources.

All three block POLYGON qualification of this pipeline.

## Not performed

No real GPT API inference, pretrained local LLM evaluation, fine-tuning of a pretrained checkpoint, PEFT/QLoRA in LLM, continual pretraining/replay, model merging, production RAG or real document holdout. CH01/02/06/07 are represented by partial pipeline or toy algebra, not completed end-to-end technology qualification.

## Reproduction

Source code, synthetic dataset, SQLite, JSON metrics, exact logs, environment package versions, and SHA256 manifest were produced as a ZIP artifact in the conversation. This GitHub record **does not imply the source ZIP is present in the repository**. Standalone GitHub reproducibility needs uploading that ZIP or adding its files.

## Next required gates

1. Fix three reported vulnerabilities and rerun adversarial checks.
2. Create provenance-verified source corpus and independent holdout.
3. Compare deterministic-only vs GPT vs local model on identical tasks.
4. Measure citation accuracy, false merges, authorization, privacy, latency, total cost.
5. Record model versions, test environment, approvals and signature before promotion.

**Engineering baseline:** no "ready" claims without independent evidence and integration qualification.
