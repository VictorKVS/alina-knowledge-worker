# FATHER Cyber Range Controller / ALINA Attack Agent v1

Status: design approved in principle by user; implementation not yet verified.

## Responsibility boundary
Controller owns lifecycle, authorization, networks, quotas, snapshots, resets, logs. Attack Agent proposes scoped test steps. Gateway executes only authorized steps. The agent cannot modify its own scope or controller policy.

## State machine
CREATED -> CONFIGURED -> APPROVED -> RUNNING -> PAUSED -> COMPLETED -> RESET.
STOPPED may be entered by independent emergency stop from any active state. Resume from STOPPED requires fresh authorization.

## Components
Operator Console; Range API; Scope Registry; Policy Decision Point; Tool Gateway; Scenario Engine; Isolated Lab Targets; Red/Blue Agents; Evidence Collector; Evaluation; Audit and Observability; Snapshot/Reset.

## Mandatory controls
- No execution without operator-approved scope and time window.
- Dedicated isolated Linux network with deny-by-default egress; explicit target allowlist.
- Tool gateway validates target IP after DNS resolution and again after redirects.
- Per-action tool allowlist and resource quotas; no privileged containers or host socket.
- Controller service account separated from attack agent service account.
- Snapshot before run, restore after run, preserve evidence in separate write-protected store.
- Independent kill switch and watchdog.
- Synthetic credentials and lab-only assets.
- All denied requests audited.
- Kubernetes NetworkPolicy alone is insufficient without verified enforcing CNI and external egress controls.

## Agent contract
Input: run_id, approved_scope_id, scenario_id, permitted_tools, resource_budget, lab_inventory.
Output: proposed_action, rationale, target_ref, expected_observation, evidence_refs.
Tool invocation must be brokered; agent never gets direct host credentials.

## Test cases
1. lifecycle transitions and approval enforcement;
2. in-scope benign simulation accepted;
3. external IP/DNS/redirect denied;
4. unauthorized tool and port denied;
5. pause/stop preempts execution;
6. reset restores snapshot;
7. controller and agent identities separated;
8. complete audit/evidence trace;
9. fail-closed behavior on policy gateway outage;
10. red/blue evaluation produces reproducible report.

## Next delivery
Implement typed contracts and mock controller first, then isolated network enforcement and tests. Do not connect live attack tooling until safety gates pass.
