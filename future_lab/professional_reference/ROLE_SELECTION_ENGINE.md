# FATHER — Role Selection Engine

## Purpose
Convert product requirements into one or more professional roles.

## Input
- product class
- required functions
- quality class
- non-functional requirements
- regulatory/security constraints
- target infrastructure
- delivery constraints

## Process

1. Extract product tasks.
2. Extract decisions required for each task.
3. Map tasks/decisions to competencies.
4. Compare competency demand against profession references.
5. Score role coverage.
6. Detect uncovered competencies.
7. Decide:
   - single specialist;
   - composite specialist;
   - multi-agent team;
   - provisional new profession.
8. Produce role plan.

## Role coverage
A role is acceptable only when:
- all mandatory tasks are covered;
- all critical competencies reach required depth;
- no critical quality/security area is uncovered.

## Multi-agent trigger
Prefer a team when:
- one role would require several unrelated K5 domains;
- separation of duties is required;
- independent review is required;
- security/safety requires an independent role;
- workload can be decomposed with clear contracts.

## Output
- selected_roles
- role_rationale
- competency_coverage
- uncovered_gaps
- required_new_profile
- qualification_requirements
