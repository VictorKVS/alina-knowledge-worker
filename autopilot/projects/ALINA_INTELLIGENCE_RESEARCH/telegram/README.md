# ALINA Telegram Intake — offline internal prototype
Status: **DEV / candidate-only**. Does not connect to Telegram, use credentials, issue external calls, approve knowledge or alter ALINA RAG.

## Purpose
Take already acquired authorized records from the existing FATHER Telegram connector and perform initial topic selection for ALINA (prompt, RAG, evaluation, security). Preserve source IDs/link/sha, assign **UNVERIFIED_CANDIDATE**, and exclude non-authorized or off-topic events.

## Input JSONL
Each line: {"chat_id":"demo","message_id":"1","text":"RAG BM25 release https://example.org","authorized":true,"published_at":"2026-10-16T09:00:00Z","url":"https://t.me/example/1"}
The authorized flag is a *trusted connector input* in the real integration; do not allow users to self-assert it as access permission. This offline design does not independently verify provider authorization.

## PowerShell / ALINA Telegram — OFFLINE VALIDATION
```powershell
# ============================================================
# FATHER / ALINA — TELEGRAM INTAKE: OFFLINE TESTS
# ============================================================
Set-Location "G:\1\alina-knowledge-worker\autopilot\projects\ALINA_INTELLIGENCE_RESEARCH\telegram"
python -m unittest discover -s . -p "test_pipeline.py" -v
```
## PowerShell / ALINA Telegram — CANDIDATE IMPORT
```powershell
# ============================================================
# FATHER / ALINA — TELEGRAM INTAKE: AUTHORIZED JSONL IMPORT
# ============================================================
Set-Location "G:\1\alina-knowledge-worker\autopilot\projects\ALINA_INTELLIGENCE_RESEARCH\telegram"
python pipeline.py --input ".\approved_messages.jsonl" --output ".\local_candidates.jsonl"
```
Use your actual checked-out project path; example local path may differ. Never commit real message exports/PII/credentials.

## Next gates
Map real TDLib/TelegramMessage fields to sanitized input with authenticated source policy; handle edits, deletes and forward provenance; durable checkpoints, source rights and independent evidence verification; JSON schema; tracing; quarantined RAG upload only after expert approval.
