# AK-01 — Product Vision

## Product
**AK-01 ALINA Knowledge Architect**

## Product class
Meta-agent / Knowledge Engineering Factory Station

## Vision
AK-01 превращает разрозненные источники знаний в доказательную, структурированную и машинно-используемую систему знаний для любого целевого агента FATHER.

AK-01 не является обычным RAG-ботом и не является универсальным аналитиком. Это производственная станция, которая проектирует знания другого агента.

## Problem
При ручном создании каждого нового агента команда снова решает одни и те же задачи:
- какие знания нужны;
- какие источники считать авторитетными;
- как строить граф знаний;
- как задавать веса узлам;
- как проектировать RAG;
- как составлять prompt architecture;
- как фиксировать неизвестное и противоречия;
- как обновлять знания;
- как доказать происхождение утверждений.

Это плохо масштабируется, создаёт дублирование и делает качество агентов непредсказуемым.

## Product promise
Для заданного целевого агента AK-01 создаёт воспроизводимый **Agent Knowledge Blueprint**, включающий:
- knowledge domains;
- knowledge graph;
- contextual node/edge weights;
- evidence/provenance;
- RAG architecture;
- prompt architecture;
- gaps/unknowns;
- prerequisites;
- evaluation requirements.

## North-star outcome
Создание нового агента в FATHER должно начинаться не с ручного написания большого промта, а с формального задания роли и задач, после чего AK-01 проектирует его knowledge layer.

## Product formula

SOURCE CORPUS
+ TARGET AGENT ROLE
+ TASKS
+ REQUIRED CAPABILITIES
+ EVIDENCE POLICY
+ OPERATIONAL CONSTRAINTS
=
AGENT KNOWLEDGE BLUEPRINT

## Strategic value
AK-01 должен стать reusable core block всей FATHER Platform и использоваться для Security, OSINT, Forecasting, DevOps, Legal, Narrative и других агентов.
