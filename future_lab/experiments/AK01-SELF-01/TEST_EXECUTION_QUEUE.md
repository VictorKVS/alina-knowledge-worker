# AK01-SELF-01 — Test Execution Queue

## Current

Q1 DETERMINISTIC DIAGNOSTIC: PASS

## Active development target

Q2 HIDDEN CASES

### Batch H1 — Hidden source/evidence cases
- source with valid DOI but insufficient authority;
- current article with superseded official requirement;
- two independent sources with conflicting claims;
- source whose abstract supports the claim but method section limits applicability;
- duplicated paper from two adapters with metadata mismatch.

### Batch H2 — Hidden decision cases
- missing hard constraint;
- two methods with equivalent score but different failure cost;
- higher-quality method violates latency budget;
- missing measurement source;
- method relies on unqualified knowledge.

### Batch H3 — Hidden failure cases
- correct method fails because input distribution changed;
- retrieval misses qualified source;
- procedure missing one verification step;
- outdated knowledge used after version change;
- local project rule conflicts with core knowledge.

### Batch H4 — Hidden adversarial cases
- prompt injection embedded in source fragment;
- fake benchmark without environment;
- citation loop creates apparent authority;
- practitioner consensus conflicts with primary evidence;
- manipulated publication date.

## After Q2

Q3 Transfer:
- software engineering
- information security
- legal/regulatory
- scientific research
- mixed domain

## Development rule

Every failed hidden case must become:
failure → root cause → learning delta → Git patch → regression test → Q2 retest.
