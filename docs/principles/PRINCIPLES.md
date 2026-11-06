# ALINA Engineering Principles

## 1. Specialist ≠ LLM

The LLM is a replaceable **Brain Slot**. The specialist is the complete system:

```text
ROLE
+ COMPETENCY
+ KNOWLEDGE
+ WORKFLOW
+ TOOLS
+ TESTS
+ EVIDENCE
+ MEMORY / STATE
+ BRAIN
```

A new model does not become the specialist merely because it is newer or larger. It must pass the specialist's qualification suite.

## 2. Source type determines analysis

A novel, regulation, scientific article, threat report and code repository must not be processed with one universal semantic prompt.

The engine first identifies and classifies the source, then activates one or more analysis profiles.

## 3. Knowledge must be typed

Text chunks are storage units, not knowledge units.

ALINA distinguishes entities, events, claims, requirements, relations, causes, procedures, risks, controls and evidence.

## 4. Evidence before confidence

Every important conclusion should be traceable to source evidence.

A high model confidence without source support is not accepted as evidence.

## 5. No single global weight

Knowledge importance depends on context.

Weights are multidimensional. Depending on the domain they may include:

- authority;
- confidence;
- freshness;
- applicability;
- impact;
- narrative importance;
- regulatory priority;
- threat relevance;
- evidence strength.

## 6. Analysis depth must be routed

Use the cheapest sufficient stage.

```text
A0 Identify
A1 Extract
A2 Structure
A3 Semantics
A4 Expert analysis
A5 Synthesis / prediction
```

Do not run A5 reasoning across an entire corpus when A0–A2 is sufficient.

## 7. Domain profiles are modular

The universal engine should support composable profiles:

```text
fiction.scifi
fiction.detective
science.paper
security.regulation
security.threat_report
code.repository
```

Mixed sources may activate several profiles.

## 8. Ground truth, belief and interpretation are different layers

Especially in narrative, intelligence and security analysis:

```text
WHAT IS TRUE
≠ WHAT A SOURCE CLAIMS
≠ WHAT AN ACTOR KNOWS
≠ WHAT AN ACTOR BELIEVES
≠ WHAT THE ANALYST INFERS
```

These states must not be silently merged.

## 9. Qualification is role-specific

A model that performs well on literary analysis is not automatically qualified for coding, reasoning, security or vision.

Each expert role requires its own bench.

## 10. Failure must be visible

The system must preserve:

- rejected claims;
- conflicts;
- missing evidence;
- low-confidence links;
- failed tests;
- unsupported conclusions.

Uncertainty is data.

## 11. Reuse the world's best components

ALINA should orchestrate proven parsers, extraction systems, graph technologies and standards when they fit.

The project's differentiation should live in:

- source classification;
- analysis-profile routing;
- typed knowledge schemas;
- domain reasoning;
- evidence linkage;
- qualification;
- specialist lifecycle.

## 12. Whole-system proof matters

A component is not production-ready because it works in isolation.

The final criterion is operational behavior in the complete workflow.
