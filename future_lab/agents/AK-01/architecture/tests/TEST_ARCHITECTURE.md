# AK-01 — Test Architecture

Owner: AQ-01 Test Architect / AA-01 Architecture Gate
Product: AK-01 ALINA Knowledge Architect

## Principle

Architecture is not accepted as build-ready until its behavior can be verified.

REQ / ARCHITECTURE
→ TESTABLE INVARIANT
→ TEST CASE
→ TEST DATA
→ EXPECTED RESULT
→ FAILURE REACTION
→ AUTOMATED GATE
→ IMPLEMENTATION

Software is written to satisfy the approved tests, not the reverse.

## Test layers

1. Schema & Contract Tests
2. Domain Invariant Tests
3. Knowledge Extraction Tests
4. Provenance Tests
5. Epistemic Classification Tests
6. Entity Resolution Tests
7. Contradiction Tests
8. Graph Integrity Tests
9. Weight / Ranking Policy Tests
10. Procedure / Checklist Tests
11. RAG Retrieval Tests
12. Prompt Policy Tests
13. Capsule Composition Tests
14. Versioning / Delta Tests
15. Inter-Agent Contract Tests
16. Security Tests
17. Fault / Recovery Tests
18. Performance / Capacity Tests
19. Regression Tests
20. POLYGON / Adversarial Tests

## Mandatory rule

No test may rely on the implementation detail it is supposed to verify.
Acceptance tests are derived from requirements, contracts and architecture invariants.
