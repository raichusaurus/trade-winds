# Planning & Decomposition Template

Use this template to turn architecture into an executable plan for humans and agents.

**Project Name:** trade-winds  
**Date:** 2026-05-12  
**Planning Lead:** Codex + John Hightshue

---

## Scope

### Planning Scope
[Project, service, feature, subproject, or task-level mini-Loom]

### Inputs
- Discovery document:
- Requirements document:
- Architecture document:
- Open decisions:

---

## Work Breakdown

### Workstreams
| Workstream | Purpose | Owner | Scope | Notes |
|------------|---------|-------|-------|-------|
| | | | | |

### Implementation Slices
| Slice | Outcome | Depends On | Priority |
|-------|---------|------------|----------|
| | | | |

---

## Ownership Boundaries

### Ownership Map
| Owner | Files/Modules/Services | Responsibilities | Out of Scope |
|-------|------------------------|------------------|--------------|
| | | | |

### Shared Areas
| Shared Area | Owners | Coordination Rule |
|-------------|--------|-------------------|
| | | |

---

## Dependencies & Sequencing

### Dependency Graph
[Diagram or list the dependency order]

### Critical Path
[What must happen first, and what blocks delivery?]

### Parallel Work
| Workstream | Can Start When | Integration Point |
|------------|----------------|-------------------|
| | | |

---

## Agent Context Packets

### Context Packet: [Workstream Name]
- **Owner:** [Agent/person]
- **Goal:** [What this workstream must accomplish]
- **Relevant requirements:** [Links or references]
- **Relevant architecture decisions:** [Links or references]
- **Owned files/services/modules:** [Scope]
- **Contracts to preserve:** [APIs, schemas, events, interfaces]
- **Risks and assumptions:** [Known concerns]
- **Expected output:** [Patch, design, test plan, report, etc.]
- **Handoff notes required:** [What must be reported when done]

*[Duplicate for each workstream]*

---

## Integration Plan

### Checkpoints
| Checkpoint | Purpose | Required Evidence | Owner |
|------------|---------|-------------------|-------|
| | | | |

### Conflict Resolution
[How do we handle overlapping edits, contract changes, or design deviations?]

### Escalation Path
[When should an agent stop and ask for direction?]

---

## Delivery Plan

### Milestones
| Milestone | Outcome | Workstreams Included | Exit Criteria |
|-----------|---------|----------------------|---------------|
| | | | |

### Initial Sequential Plan
[For first implementation, what is the safest waterfall-style order?]

### Later Agile Cycles
[After the foundation exists, what smaller loops should continue iteratively?]

---

## Approval

- **Planning Lead:** _________________ Date: _______
- **Tech Lead:** _________________ Date: _______
- **Product Owner:** _________________ Date: _______

**Ready to move to Contracts & Tests / CI/CD?** [ ] Yes [ ] No (Explain):

---

*Save this document in your project repo. Use it to brief agents and coordinate implementation.*
