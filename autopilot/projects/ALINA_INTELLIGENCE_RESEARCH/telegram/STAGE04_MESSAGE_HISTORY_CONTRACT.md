# Stage 04: ALINA Telegram Message History (offline)
Status: development prototype only; NOT connected to TDLib or production.
Input event new/edit/delete with chat_id, message_id, text and connector-validated authorization. MessageHistory keeps a per-message revision chain and SHA-256 of each version. A delete creates tombstone. Duplicate edits do not increase revision.
## Limitations and risk
- Data currently stored in memory; lost on restart. Persistent append-only store, cryptographic integrity, replay and idempotency across runs remain TODO.
- This is not independent authorization: trusted caller must enforce server-side channel access.
- Forwards, source independence, citations, attachment metadata, trace IDs and retraction propagation are not implemented.
- Do not store private message content in GitHub. No automatic CRM or RAG promotions.
- Tests are synthetic; execution must be confirmed by GitHub QA report.
