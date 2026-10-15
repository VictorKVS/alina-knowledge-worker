# ALINA Red Team — Isolated Polygon v1

Status: architecture proposal; no active attacks or deployments performed.

## Purpose
Authorized adversary emulation against owned, deliberately isolated lab targets only. ALINA Analyst evaluates Blue Team detections, evidence and security control effectiveness.

## Mandatory scope contract
Every run must declare: run_id, authorizer, target inventory, allowlisted CIDRs/IPs, permitted ports/protocols, permitted tools/actions, maximum request rate, time window, CPU/RAM budget, data handling policy, and emergency stop mechanism. Default DENY.

## Enforcement outside the model
- Dedicated network namespace / isolated lab VLAN; egress deny-all with explicit allowlist.
- Lab-only DNS resolver, no host network mode, no privileged containers, no Docker socket mounting.
- Read-only root filesystem where practical, dropped Linux capabilities, seccomp/AppArmor, non-root identity.
- Per-tool authorization proxy that validates every target/action against signed run scope.
- Independent watchdog, resource quotas, immutable audit events, manual kill switch.
- Synthetic accounts and data; never use production secrets.
- Prohibit lateral movement outside lab and deny all scope expansion without human approval.

## Agent workflow
Lead Analyst -> Scenario Planner -> Authorization Gate -> Red Team Agent -> Lab Target -> Blue Team/SOC -> Evidence -> Critic -> Evaluation -> Decision Memory.

## Development artifacts
Scope policy schema, architecture diagram, threat model, attack simulation test plan, lab setup guide, safety acceptance tests, Blue Team detection matrix, audit schema, incident/stop runbook, release gate.

## Acceptance tests
1. In-scope target and allowed action accepted.
2. Out-of-scope IP, DNS resolution and redirected targets denied.
3. Non-allowlisted tool and port denied.
4. Egress blocked at network layer even if prompt/tool policy bypassed.
5. Kill switch stops execution and preserves logs.
6. Run cannot read host secrets or mount host filesystem.
7. Scope changes require new authorization.
8. All claims are linked to reproducible evidence.

## Safety gates
No real target scanning, exploitation, persistence or uncontrolled automation until scope, isolation and human authorization have been verified. This document does not grant authorization.
