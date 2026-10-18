# MATH-REVIEW — the math-reviewer channel (optional: math-heavy projects)

> **Append-only contract.** This file is the stable channel of the
> **math reviewer** (AGENTS.md §2.8 rule 6a — the formal math gate). It
> grows by dated sections at the bottom; earlier sections are never edited
> or deleted — corrections append as new dated entries that supersede old
> ones (the REVIEW_LOG convention). **Single owner: the math reviewer.**
> Other roles read it; they do not write it.
>
> **The workspace.** The `math/` directory (including `math/items/`, the
> per-item reproduction artifacts, and `math/reports/`) is math-reviewer
> owned — other roles read it, never write it. The math reviewer edits no
> file outside `math/`: its deliverables reach the tree only as *proposals*
> (pins landed by the worker, spec-page sections landed by the page's
> owner, INVARIANTS entries owner-approved).
>
> **The standing pointer convention.** Whenever any role — worker,
> reviewer, advisor, planner — has a *doubt* about a derivation, a formula,
> a numeric freeze, a floor, a tolerance, or an update rule, it **logs a
> one-line pointer** in its *own* channel ("math item →
> `math/MATH-REVIEW.md`, the question in one line") so the math reviewer
> can check it later. Doubts are logged, never silently dropped. Never
> write the pointer into `math/` itself.

---

## What the role does

1. **Pre-execution checks** of every SPEC compile carrying a formula,
   derivation, numeric freeze, floor, tolerance, or update rule — before
   the worker executes it.
2. **Back-verification** of shipped math via reproduction artifacts
   (`math/items/<id>/`: the script, the revision, the CLI, the config, the
   result — file-first, never a masked pipe).
3. **The derivation queue** — open mathematical questions, each with its
   falsifiable check.
4. **The second pass** on core-math diffs, per AGENTS.md §2.8 rule 9.

## Entry format

```markdown
## YYYY-MM-DD — Math reviewer: {{the item}} — {{verdict}}

**Item:** {{the derivation / freeze / diff under review, with its SPEC
milestone or commit}}
**Check:** {{the reproduction artifact (`math/items/<id>/`) or the analytic
argument, stated so it can be re-run}}
**Verdict:** {{correct | incorrect (the error, at the equation/line) |
inconclusive (what is missing)}}
**Proposal:** {{if incorrect — the fix as a PROPOSAL (the worker lands it)}}

Role: math-reviewer({{MATH_REVIEWER_MODEL}})
```

<!-- Casual math Q&A goes to the ADVISOR, not here. Escalations from the
     math referee (docs/MATH-REFEREE.md) arrive as advisory input, never as
     verdicts. Compaction: math-reviewer-owned; witnessed; gated. -->
