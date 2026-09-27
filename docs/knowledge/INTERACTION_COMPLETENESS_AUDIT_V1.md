# ALINA Analyst — Interaction Completeness Audit v1

ALINA checks not only visual similarity, but whether the page is functionally complete.

For each visible control ALINA records:

- visible label;
- expected interaction;
- declared target/action;
- implementation status;
- idle state;
- hover state;
- pressed state;
- keyboard focus state;
- disabled/loading states where relevant;
- reduced-motion behavior;
- evidence.

Findings:
- `dead_control` — looks actionable but has no action/target;
- `missing_state` — one of required visual interaction states is absent;
- `misleading_hud` — decorative/informative HUD looks like a clickable control;
- `duplicate_target` — nested controls compete for the same action;
- `route_not_verified` — target exists in contract but has not been verified.

Priority:
1. dead/broken actions;
2. missing keyboard/focus behavior;
3. hover/pressed feedback;
4. polish.

Core rule: **visual completeness is not product completeness.**
