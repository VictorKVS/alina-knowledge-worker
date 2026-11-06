# From RAG to a Verified Digital Expert

## The problem with "chat over documents"

The dominant enterprise AI pattern is familiar:

```text
documents
→ chunking
→ embeddings
→ vector search
→ LLM
→ answer
```

This is useful. It is also insufficient for many expert tasks.

A regulation is not only text. It contains subjects, objects, obligations, conditions, exceptions and authority.

A scientific paper is not only text. It contains a hypothesis, method, data, result and limitations.

A detective novel is not only text. It contains actors, events, beliefs, lies, clues, motives and chronology.

A threat-intelligence report is not only text. It contains actors, campaigns, techniques, indicators, confidence and temporal relationships.

If all of these are reduced to anonymous chunks, the system loses part of the structure that makes expert reasoning possible.

## The ALINA hypothesis

ALINA starts from a different premise:

> Before asking an AI to reason over information, identify what kind of information it is and represent it in a form appropriate to that domain.

The pipeline becomes:

```text
SOURCE
→ IDENTIFY
→ CLASSIFY
→ CHOOSE ANALYSIS PROFILE
→ DECOMPOSE
→ LINK
→ WEIGHT
→ VERIFY
→ REASON
```

## Analysis profiles

A profile is more than a prompt.

It defines:

- what entities matter;
- what relations are valid;
- what knowledge types to extract;
- what evidence is required;
- how importance is calculated;
- what critic validates the result;
- what tools may be used.

This lets one general engine support very different expert domains.

## Why the specialist must not equal the model

Models change too quickly to become the permanent identity of a specialist.

Instead:

```text
SPECIALIST
=
COMPETENCY
+ KNOWLEDGE
+ TOOLS
+ WORKFLOW
+ TESTS
+ EVIDENCE
+ BRAIN SLOT
```

The model is replaceable.

A future model becomes the new brain only after it passes the specialist's qualification benchmark.

This preserves years of accumulated knowledge engineering when the model ecosystem changes.

## Evidence-first architecture

An expert system should be able to answer:

- Where did this fact come from?
- Is it a source claim or an analyst inference?
- What evidence supports this relationship?
- How fresh is the information?
- Does another source contradict it?
- Which rule made this conclusion applicable?
- Which model/tool produced the interpretation?

Without those answers, confidence scores can become cosmetic.

## A0–A5 analysis depth

Not every page needs expensive reasoning.

```text
A0 Identify
A1 Extract
A2 Structure
A3 Semantics
A4 Expert analysis
A5 Synthesis / prediction
```

Large corpora can be processed mostly at A0–A2. Deep reasoning is activated selectively.

This is not only an accuracy decision. It is an economic architecture.

## One engine, many experts

The same evidence-first foundation can support:

```text
Book / Narrative Analyst
Security Expert
Scientific Research Analyst
OSINT / Threat Intelligence Analyst
Legal Analyst
Code / Architecture Analyst
```

Their knowledge schemas differ, but the engineering principles remain shared.

## The long-term goal

The target is not another chatbot.

The target is a system that can:

```text
recognize a source
→ understand how it must be analyzed
→ build structured knowledge
→ preserve evidence
→ qualify a domain specialist
→ replace its model without losing the specialist
```

That is the transition from retrieval-augmented generation to **expert engineering**.
