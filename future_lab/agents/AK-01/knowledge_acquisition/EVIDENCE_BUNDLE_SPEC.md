# AK-01 — Evidence Bundle Specification

Each critical knowledge item should be represented as an Evidence Bundle.

## Bundle contents
- knowledge_id
- definition
- mechanism
- prerequisites
- decision_rules
- procedures
- limitations
- failure_modes
- alternatives
- implementation_notes
- tests
- source_refs
- contradiction_refs
- confidence_notes
- freshness_policy

## Minimum evidence bundle by depth

K0:
- one verified definition/reference

K1:
- definition
- mechanism
- one authoritative explanation

K2:
- K1
- procedure/example
- basic validation

K3:
- K2
- alternatives
- decision criteria
- limitations

K4:
- K3
- design guidance
- failure modes
- independent corroboration
- practical cases

K5:
- K4
- optimization
- diagnosis
- edge cases
- conflicting evidence handling
- advanced qualification cases

## Rule
Depth is defined by professional capability, not by token count or number of documents.
