# AK-01 — Knowledge Layer Model

```mermaid
flowchart TB
    CORE[CORE KNOWLEDGE\nUniversal professional foundations]
    DOMAIN[DOMAIN KNOWLEDGE\nIndustry / specialty]
    ORG[ORGANIZATION KNOWLEDGE\nLocal systems / rules / roles]
    PROJ[PROJECT / TEAM KNOWLEDGE\nRepo / workflows / conventions]
    CTX[ACTIVE CONTEXT\nCurrent task / case]

    CORE --> DOMAIN --> ORG --> PROJ --> CTX
```

## Rules

### CORE
Stable professional foundations. Updated only with strong evidence and broad impact analysis.

### DOMAIN
Specialty knowledge: healthcare security, forecasting, OSINT, Kubernetes, etc.

### ORGANIZATION
Organization-specific architecture, policies, systems, SLA, escalation paths and local terminology.

### PROJECT / TEAM
Repository conventions, project workflows, local tools and current operating procedures.

### ACTIVE CONTEXT
Temporary task/case data. Must not automatically become permanent knowledge.

## Promotion rule

ACTIVE CONTEXT
→ repeated/validated pattern
→ PROJECT or ORGANIZATION candidate
→ AK-01 analysis
→ AKN-01 review
→ versioned Knowledge Delta

No context item is promoted merely because it appeared in one successful run.
