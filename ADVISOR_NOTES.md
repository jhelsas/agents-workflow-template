# ADVISOR_NOTES.md — Interactive Q&A findings and handoffs

**Purpose:** Record conclusions from interactive advisor sessions (Q&A,
data verification, hypothesis exploration) for forwarding to the planner
and the reviewer. This file grows by append; it is not edited retroactively.

**Audience:** planner (for reframing scope), reviewer (for context on next
gates), worker (for diagnostics).

**Stable path:** referenced in AGENTS.md §2.8 rule 2 (append-only
inter-agent channels). Single owner: the advisor.

---

## Entry format

<!-- One entry per session or finding. The advisor answers and verifies; it
     does NOT compile SPEC.md, run PASS/FAIL gates, or execute the TDD loop
     (AGENTS.md §2.8 rule 6). Every number carries its provenance (Hazard
     2/2c: the recorded config, the right tolerance for non-reproducible
     components). Ideas that are not yet findings go to
     docs/IDEAS-ADVISOR.md, not here. -->

```markdown
## YYYY-MM-DD — Advisor: Finding {{n}} — {{one-line statement}}

**Question (from the owner / planner / reviewer):** {{the question as asked}}
**Method:** {{how it was verified — commands, files, commits}}
**Answer:** {{the finding, with every number's provenance}}
**Confidence and caveats:** {{what would falsify this; what was NOT checked}}
**Forwarded to:** {{planner (scope) | reviewer (gate context) | BACKLOG}}

Role: advisor({{ADVISOR_MODEL}})
```

<!-- Compaction (AGENTS.md §2.13): the advisor (its owner) collapses closed
     findings into one line each past ~50k tokens; another role witnesses;
     the reviewer gates the witness verdict. -->
