# Source & Analysis Profile Matrix

This document defines the first working taxonomy for ALINA's Analysis Profile Registry.

## Fiction

### Narrative Core

Always available for fiction:

- characters;
- events;
- locations;
- objects;
- timeline;
- relations;
- causes;
- consequences;
- motives;
- beliefs;
- secrets;
- conflicts;
- clues;
- plot threads.

### Genre profiles

| Profile | Additional analytical focus |
|---|---|
| `fiction.science_fiction` | technology, scientific assumptions, constraints, plausibility, societal effects |
| `fiction.hard_scifi` | physical consistency, engineering assumptions, quantitative constraints |
| `fiction.cyberpunk` | technology-power relations, surveillance, corporations, identity |
| `fiction.space_opera` | factions, geopolitics, logistics, large-scale conflict |
| `fiction.post_apocalypse` | resource scarcity, survival systems, social reconstruction |
| `fiction.time_travel` | timeline consistency, causality, paradoxes |
| `fiction.alternate_history` | divergence points, historical dependencies, counterfactual chains |
| `fiction.detective` | crime, suspects, clues, alibis, motive, deception |
| `fiction.noir` | moral ambiguity, power relations, unreliable accounts |
| `fiction.thriller` | threat escalation, timing, pursuit, risk |
| `fiction.drama` | relationships, emotion, moral dilemmas, turning points |
| `fiction.romance` | relationship dynamics, goals, attachment, conflict |
| `fiction.horror` | threat model, uncertainty, fear mechanisms, survival |
| `fiction.historical` | historical context, chronology, deviations, social constraints |
| `fiction.military` | forces, command, objectives, logistics, tactics, losses |
| `fiction.spy` | intelligence, cover, deception, assets, operations |
| `fiction.fantasy` | world rules, magic system, factions, constraints |
| `fiction.litrpg` | progression system, stats, rules, economy, game mechanics |
| `fiction.portal` | transition mechanism, adaptation, knowledge asymmetry |

A work can activate several profiles with confidence scores.

## Scientific sources

| Profile | Focus |
|---|---|
| `science.paper` | question, hypothesis, method, data, results, limitations |
| `science.review` | literature coverage, competing schools, evidence synthesis |
| `science.monograph` | conceptual structure, definitions, argument chain |
| `science.experiment` | variables, controls, method, reproducibility |
| `science.dataset` | provenance, schema, quality, bias, coverage |

## Professional literature

| Profile | Focus |
|---|---|
| `professional.textbook` | concepts, procedures, examples, learning objectives |
| `professional.handbook` | procedures, reference rules, decision criteria |
| `professional.casebook` | cases, decisions, outcomes, lessons |
| `professional.methodology` | method, prerequisites, sequence, validation |
| `professional.standard` | normative rules, implementation requirements |

## Information security

| Profile | Focus |
|---|---|
| `security.regulation` | subject, object, condition, obligation, exception, deadline |
| `security.professional_book` | concepts, controls, architecture, practice |
| `security.threat_report` | actor, TTP, IOC, target, campaign, confidence |
| `security.incident` | timeline, evidence, root cause, impact, remediation |
| `security.architecture` | assets, trust boundaries, controls, attack paths |
| `security.risk` | asset, threat, vulnerability, likelihood, impact, treatment |
| `security.control` | objective, implementation, effectiveness, evidence |
| `security.cti` | actor, malware, technique, campaign, relationship, source |

## Legal / regulatory

| Profile | Focus |
|---|---|
| `legal.law` | subject, scope, rights, duties, exceptions, responsibility |
| `legal.regulation` | mandatory requirements, procedure, authority |
| `legal.case` | facts, positions, evidence, reasoning, holding |
| `legal.contract` | parties, obligations, rights, deadlines, liability |

## Code and software

| Profile | Focus |
|---|---|
| `code.repository` | modules, dependencies, APIs, data flow, risks |
| `code.file` | functions, classes, logic, errors |
| `code.architecture` | components, boundaries, interfaces, deployment |
| `code.security` | trust boundaries, vulnerabilities, controls |
| `code.documentation` | intended behavior, APIs, constraints |

## Web and media

A web page is a container, not a knowledge class.

The router should first classify the page as:

- official source;
- scientific publication;
- company site;
- product documentation;
- news;
- blog;
- forum;
- social media;
- marketing;
- OSINT source.

Then apply the relevant domain profile.

## Mixed sources

Profiles compose.

Example:

```text
military science-fiction novel
=
narrative_core
+ fiction.science_fiction
+ fiction.military
+ political-analysis module
```

The Analysis Profile Registry should support inheritance and composition rather than duplicating universal extraction logic.
