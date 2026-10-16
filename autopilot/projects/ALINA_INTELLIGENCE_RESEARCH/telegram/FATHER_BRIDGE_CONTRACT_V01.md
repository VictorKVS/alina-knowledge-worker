# FATHER → ALINA Telegram offline bridge v0.1
Date: 2026-10-16. Status: DEV / tests NOT run by this commit.

## Source and scope
Existing OSINT_deepseek/father_osint/collectors/telegram.py emits Material(source_type,source_locator,title,raw_text,published_at,author,metadata); metadata includes chat_id, message_id. That is the source boundary. Our ALINA bridge maps already-exported sanitized dictionaries into candidate-only pipeline.py records.

## Data direction
Existing permitted Telegram collector → authorized export policy + trusted ACL decision → father_bridge.map_material → ALINA topic intake/dedup → UNVERIFIED_CANDIDATE. No canonical RAG write, CRM signal, network calls, secret handling or new TDLib login.

## Security caveat
Boolean authorized_by_policy passed to local function is only a DEMONSTRATION of boundary contract. It is NOT independent authorization or tenant isolation. Real deployment must bind to server-side authenticated connector permissions, source channel ACL and audit decisions, and protect original exports outside GitHub.

## QA
Run python -m unittest discover -s . -p 'test_*.py' -v from module directory (10 planned tests total). Existing QA report currently unverified: a button press does not prove a git push.
## Pending integration gates
Source rights/consent; update/delete event rules; forward provenance; durable checkpoints; trace IDs; retraction; expert review; no silent promotion. Production FATHER Site and Zoos prerequisites apply.
