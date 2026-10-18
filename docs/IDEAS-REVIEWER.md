# IDEAS — reviewer-owned hypotheses and untested ideas

> **Owner.** Reviewer. This is the reviewer's append-only channel for
> hypotheses, untested ideas, and parked discussions that are **not active
> work**. Each dated entry carries the reviewer's `Role:` trailer.
>
> **Contract.** Append-only; dated sections. An idea **graduates out** of
> this file when it becomes a milestone — the planner compiles it into
> `SPEC.md`, and the entry here gains a `Graduated to M<n>` line (the full
> text stays here). Graduation lines and compaction of existing entries are
> reviewer-only writes. Corrections are new entries that supersede, never
> edits.
>
> **Relationship to the tested record:** tested hypotheses and their
> verdicts live in the dated reports and channel entries they produced;
> this file holds *untested* ideas only. When an idea here is tested, its
> verdict goes to the relevant report/channel and the entry here gains a
> verdict pointer.

---

## Entry format

```markdown
## YYYY-MM-DD — {{title}}

**Source:** {{owner food-for-thought | a gate finding | a report}}
**Status:** parked | proposed | graduated

**The observation.** {{what motivated the idea, with the evidence already in
the record (provenance rules apply to these numbers too)}}

**The candidate mechanism(s).** {{numbered; the falsifier each would need}}

**The cheap falsifier first.** {{the smallest experiment that could kill
the idea — propose it before any implementation}}

Role: reviewer({{REVIEWER_MODEL}})
```

<!-- A graduated entry gains: **Graduated to M<n>** (SPEC Round {{N}}).
     Compaction: the reviewer collapses graduated and refuted entries to one
     line each past ~50k tokens; witnessed; gated. -->
