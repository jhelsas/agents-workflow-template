# REVIEW_LOG — diff reviewer → planner channel

> **Append-only contract.** This file is the stable, inter-agent channel
> from the **diff reviewer** to the **planner**. Diff reviewer findings are appended
> as dated sections at the bottom; earlier sections are **never edited or
> deleted**. Corrections are appended as new dated entries that supersede
> the old ones. This keeps the planner's prompt-prefix cache stable across
> cycles: the path never changes, only the tail grows.
>
> **Single owner: the diff reviewer.** The diff reviewer commits only its own entries
> here (AGENTS.md §2.10). Dated one-off artefacts
> (`docs/reports/YYYY-MM-DD-*.md`) remain immutable snapshots and are
> referenced from here, not edited.

---

## Entry format

<!-- One entry per gate (or per batched set of gates). Triggered once per
     completed milestone, batched at round closes — never mid-milestone,
     never casual Q&A. Gates COMMITTED diffs only (§2.10 rule 3): if the
     material is uncommitted, wait for the worker's handoff note. Return a
     binary PASS/FAIL with line-level critiques. -->

```markdown
## YYYY-MM-DD — Diff reviewer: M{{n}} gate — {{PASS|FAIL}} ({{one-line verdict}})

**Scope:** commits `{{hash}}..{{hash}}` (the diff + the milestone's SPEC
criteria).
**Findings:** {{line-level critiques; every claim cites file:line}}
**Flags carried forward:** {{what the next gate must check}}
**Provenance notes:** {{any number that did not re-derive from committed
artifacts — a Hazard-2 finding, not a footnote}}

Role: diff-reviewer({{REVIEWER_MODEL}})
```

<!-- Compaction (AGENTS.md §2.13): when this file exceeds ~50k tokens, the
     diff reviewer (its owner) collapses closed entries into one line each under
     a "## Compacted record" block; the worker or planner witnesses the
     block against the record; the diff reviewer gates the witness verdict. -->
