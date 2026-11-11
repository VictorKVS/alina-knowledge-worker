# AK-01 — Controlled Iterative Growth Loop

## Principle
AK-01 is not built as a finished "super-agent". It is grown through auditable iterations.

## Loop

1. TASK PACKAGE
2. AK-01 DRAFT RESULT
3. TRACE CAPTURE
4. AUTOMATED TESTS
5. INDEPENDENT REVIEW
6. PROBLEM DISCOVERY
7. ROOT-CAUSE CLASSIFICATION
8. PATCH THROUGH GIT
9. REGRESSION TEST
10. PROMOTION OF PROVEN CAPABILITY

## Capability promotion
A capability may move:
EXPERIMENTAL → DEVELOPMENT → TESTED → INTEGRATION-TESTED → QUALIFIED

Promotion requires:
- trace completeness;
- no unresolved critical defects;
- passing regression tests;
- explicit reviewer evidence.

## Separation of duties
AK-01 may propose, decompose and explain.
AK-01 may NOT self-qualify its own capability.

## Git evidence
Every correction must be attributable to:
- input case;
- failing test or review finding;
- root cause;
- changed artifact/code;
- new or updated regression test;
- commit SHA;
- post-fix result.
