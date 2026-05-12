# Discovery

Capture findings during the Discovery phase.

**Project Name:** trade-winds
**Date:** 2026-05-12
**Facilitator:** Codex + John Hightshue

---

## Problem Statement

### Core Problem
Trade Winds is starting over from an older implementation. The first problem is not merely rebuilding the previous app; it is discovering what Trade Winds should be now, what the old implementation taught us, and what the smallest valuable new version should include.

### Why It Matters
A clean restart gives the project a better foundation while preserving the older repo as an artifact of prior learning. Using Loom here also gives the framework its first real pilot project.

### Current State
- The previous implementation is archived as `trade-winds-legacy`.
- The new public GitHub repository is `raichusaurus/trade-winds`.
- The new repo currently contains only this Loom documentation scaffold.
- The product direction, user, MVP, and technical architecture still need discovery.

---

## Stakeholders

### Primary Stakeholders
*Who will directly benefit from solving this problem?*

| Stakeholder | Role | Needs | Constraints |
|-------------|------|-------|-------------|
| John Hightshue | Project owner / builder | A clean, useful project restart and a good Loom pilot | Wants to preserve the old implementation as history |
| Codex | Build collaborator / Loom orchestrator | Clear context, phase outputs, and implementation boundaries | Should avoid premature scaffolding before Discovery |

### Secondary Stakeholders
*Who else is affected by this solution?*

| Stakeholder | Role | Needs | Constraints |
|-------------|------|-------|-------------|
| Loom | Workflow framework under test | Feedback from real project use | Framework updates should remain separate from Trade Winds unless intentionally upstreamed |

### Decision Makers
*Who has the final say on whether we proceed?*

John Hightshue.

---

## Context & Constraints

### Timeline
- **Deadline:** [When do we need this?]
- **Time to market:** [How urgent?]
- **Phase-based release?** [If applicable]

### Resources
- **Budget:** [What's available?]
- **Team:** [Who's working on this?]
- **Infrastructure:** [What do we have?]

### Technical Constraints
- **Existing systems:** [What must we integrate with?]
- **Technology requirements:** [Any mandates?]
- **Scalability needs:** [How big will this get?]

### Organizational Constraints
- **Compliance/Regulatory:** [Any requirements?]
- **Organizational policies:** [Any constraints?]
- **Dependencies:** [What else depends on this?]

---

## Assumptions

### Key Assumptions
*What are you assuming to be true? What needs validation?*

| Assumption | Why We Believe It | How We'll Validate |
|-----------|------------------|-------------------|
| The rewrite should not copy the old architecture by default | The old repo is being preserved as a learning artifact, not treated as the new foundation | Review the legacy repo for lessons before architecture |
| Loom should begin with documentation and discovery | Loom is explicitly documentation-driven and sequential for new projects | Use this pilot to note whether that feels helpful or heavy |
| `trade-winds` should keep the canonical repo name | The legacy repo was renamed and archived | Confirm the new public repo is the active project home |

---

## Risks & Opportunities

### Risks
*What could prevent success?*

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| Rebuilding the old project accidentally | Medium | Medium | Mine the legacy repo for lessons, then make fresh decisions |
| Over-documenting before momentum exists | Medium | Medium | Keep phase docs practical and concise |
| Loom gaps appear during real use | Low | High | Track feedback in `pilot-feedback.md` and upstream later |

### Opportunities
*What unexpected benefits might emerge?*

- Trade Winds can become both a useful project and an example Loom case study.
- The legacy implementation can reveal what to keep, discard, and rethink.
- The pilot can produce concrete improvements for Loom templates and orchestration.

---

## Discovery Outputs

### Key Insights
*What did you learn during discovery?*

TBD after reviewing the legacy project and clarifying the new product vision.

### Open Questions
*What still needs to be explored?*

- What is Trade Winds, in one sentence?
- Who is the primary user?
- What problem should the MVP solve?
- What should the new implementation intentionally avoid from the legacy version?
- What stack choices are constraints versus preferences?

### Next Steps
*What needs to happen before Requirements?*

- Review `trade-winds-legacy` for useful lessons.
- Interview the project owner on product intent, desired experience, and MVP boundaries.
- Summarize "keep / discard / rethink" findings.
- Convert discovery answers into Requirements.

---

## Sign-Off

- **Discovery Lead:** _________________ Date: _______
- **Stakeholder:** _________________ Date: _______
- **Decision Maker:** _________________ Date: _______

**Ready to move to Requirements?** [ ] Yes [ ] No (Explain):

---

*Save this document in your project repo for future reference.*
