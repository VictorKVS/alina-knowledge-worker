# AK01-SELF-01 — Control Checkpoint 01

## Control point

Branch: `father/alina-book-mvp`  
HEAD: `478404ea1177090ef7a7344182c0470f6fb8b379`

## Verdict

**PASS — first end-to-end AK-01/FATHER factory-line checkpoint is accepted for the current maturity level.**

This checkpoint proves the integrated deterministic line. It does not certify live external research adapters or production deployment.

## CI evidence

### AK-01 Architecture Gate
- Result: PASS
- Executable architecture tests: **77 passed**
- Mandatory-skip gate: PASS
- No mandatory architecture tests were skipped.

### AK-01 DevSecOps
- Ruff: PASS
- Mypy: PASS
- Bandit: PASS
- Dependency audit: PASS
- Architecture tests inside DevSecOps: **77 passed**
- Dependency audit: no known vulnerabilities reported by the current audit run.

### AK-01 Integration
- Result: PASS
- API integration tests: **3 passed**
- Non-blocking warning: Starlette/FastAPI TestClient deprecation path related to current `httpx` integration.

### General Tests
- Result: PASS
- Windows workflow completed successfully.

## Integrated capabilities proven by this checkpoint

1. Work decomposition with traceable derivation.
2. Gap/finding detection instead of silent invention.
3. Research-plan generation.
4. Source-discovery planning.
5. Source qualification with reject/quarantine/limited acceptance.
6. Claim-to-evidence fragment linking.
7. Knowledge Unit and Evidence Bundle assembly.
8. Independent knowledge qualification; AK-01 cannot self-qualify.
9. Runtime policy blocks unqualified/superseded knowledge and escalates conflicts.
10. Professional Knowledge Graph binds qualified knowledge to professional work.
11. Problem Signature and candidate-method representation.
12. Timing/measurement evidence checks.
13. Method comparison with readiness and hard constraints.
14. NO_DECISION behavior when evidence/measurements/policy are insufficient.
15. Outcome capture: expected vs actual.
16. Evidence-backed root-cause classification.
17. K1–K12 / operational correction routing.
18. Learning Delta with mandatory regression and requalification rules.
19. End-to-end factory-line test.
20. Factory-line orchestrator with stop conditions.

## Control invariants

The checkpoint confirms these current invariants:

- discovery != qualification;
- evidence != truth;
- supported != qualified;
- AK-01 cannot self-qualify;
- unqualified knowledge cannot enter runtime;
- conflicted knowledge requires escalation;
- method choice requires explicit comparison evidence;
- missing hard-constraint values block selection instead of causing implicit behavior;
- outcomes do not rewrite historical evidence;
- correction requires a regression case;
- behavioral/knowledge changes require requalification where applicable.

## Non-blocking technical debt

1. Integration warning:
   `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead.`
   Action: track dependency migration separately; do not change dependencies only to suppress a warning without compatibility tests.

2. GitHub Actions runner warning:
   Node.js 20 deprecation for current action versions.
   Action: update action versions when supported and verify workflows after migration.

## Not yet proven

This checkpoint does **not** yet prove:

- live OpenAlex/Crossref/Semantic Scholar adapters;
- live standards/regulator ingestion;
- real citation-graph expansion;
- production database persistence of the whole factory-run state;
- distributed execution;
- performance under production load;
- POLYGON adversarial qualification;
- shadow-production qualification on real professional work.

## Promotion decision

Current line may be promoted from **DEVELOPMENT** to **TESTED / INTEGRATION-TESTED for the deterministic local factory-line scope**.

It must **not** be marked production-certified yet.

Next controlled stage:
**Live Source/Research Adapter Layer → deterministic fixtures → connector contract tests → source provenance tests → failure/retry/rate-limit tests → full factory-line regression.**
