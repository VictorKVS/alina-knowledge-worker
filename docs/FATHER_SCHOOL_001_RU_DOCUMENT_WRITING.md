# FATHER SCHOOL-001 — Русский язык и профессиональные документы

Status: DESIGN / NOT IMPLEMENTED
Owner: ALINA Analyst (curriculum, evidence, assessments)
Integration: FATHER Knowledge Core / learning-core; FATHER CODEX (first learner)

## Mission
Train and verify reusable professional writing competence for AI agents. The school does not fine-tune model weights by default; it trains and certifies a specific agent configuration (model + prompt + tools + knowledge versions).

## Existing boundaries
- Canonical curriculum and evidence: VictorKVS/KNOWLEDGE_CORE, learning-core; no duplicate KB.
- ALINA orchestrates teaching and competency evaluation, but does not replace FATHER Agent Zoo, CODEX, OSINT or runtime.
- C0.4 database deduplication remains active; do not migrate or create a parallel store during SCHOOL-001.
- Treat external corpora as untrusted; check license and source version before ingesting.

## Learning objectives
1. RU orthography, morphology, syntax, punctuation and formal style.
2. Document types, mandatory fields, templates, versioning, audience and purpose.
3. Preserve semantic force: must/may/prohibited, negation, deadlines, amounts, exceptions.
4. Distinguish linguistic correctness from factual and normative correctness.
5. Trace each substantive statement to an applicable source or explicitly mark uncertainty.
6. Review, explain and correct errors without silently changing meaning.

## Components and contracts
- Source Registry: source_id, origin, revision, language, license, retrieval_date, hash, applicability.
- Curriculum: competency_id, prerequisites, learning_object_ids, assessment_ids, version.
- Lesson: lesson_id, competency_id, objective, materials, exercises, expected behaviors.
- Assessment: assessment_id, private fixtures, rubric, severity, grader_version, result evidence.
- Agent Qualification: agent_id, agent_version, model_id, prompt_version, tool_versions, knowledge_snapshot, assessment_run_id, valid_until, status.
- Skill Pack: skill_id, scope, instructions, tools, source_ids, tests, release status; never automatically grants external execution privileges.

## Minimal vertical slice
1. Register a licensed Russian dictionary and local grammar checker (evaluate LanguageTool); do not redistribute unlicensed texts.
2. Author 20 synthetic Russian writing cases: spelling (4), punctuation (4), formal style (4), semantic preservation (4), document structure (4).
3. Provide one approved technical instruction template; no regulated legal documents in MVP.
4. ALINA composes a lesson and an exercise for FATHER CODEX.
5. CODEX produces a Russian technical instruction using the template.
6. Run deterministic checks plus grammar checker and a separate semantic reviewer.
7. Record errors, provenance, scores and configuration; do not certify if critical semantic alteration is detected.
8. Re-run the same fixture set after any model/prompt/tool/knowledge change.

## Acceptance gates
- 100% of generated claims in the fixture requiring a source have a resolvable citation or are marked unverified.
- 0 critical meaning reversals (obligation vs permission, negation, amount, deadline).
- All mandatory template fields present; no invented dates, names or approvals.
- Test report links each finding to a rule, text span and suggested correction.
- End-to-end evidence: lesson -> exercise -> document -> checker -> independent assessment -> qualification record.
- Human approval remains required for high-stakes or legally binding output.

## Delivery order
S1: approve scope and contracts; S2: fixtures + baseline checker; S3: lesson generator; S4: independent grader; S5: CODEX end-to-end pilot; S6: release to other agents after regression testing.

## Current state
This file is an implementation brief, not proof that the school or checker runs. Start S1 after the existing ALINA C0.4 gate is reconciled with Knowledge Core interfaces.
