# WORKER_LOG — worker → diff reviewer channel

> **Append-only contract.** This file is the stable, inter-agent channel
> from the **worker** to the **diff reviewer**. Findings, escalations and
> handoffs are appended as dated sections at the bottom; earlier sections
> are **never edited or deleted**. Corrections are appended as new dated
> entries that supersede the old ones (the REVIEW_LOG convention). The path
> never changes, only the tail grows, so the diff reviewer's prompt-prefix cache
> stays stable.

---

## Entry format

<!-- One entry per milestone (or per worked batch), written BEFORE the
     handoff to the diff reviewer. The entry is the diff reviewer's gate input: say
     what changed, what was run, what the numbers were, and what is
     reserved. Either verdict is honest — a negative result is a result
     (Standing rule 2). -->

```markdown
## YYYY-MM-DD — Worker: M{{n}} — {{one-line outcome}}

**What changed:** {{files, commits}}
**Tests:** {{the targeted commands run, their results}}
**The numbers:** {{every figure with its result file / commit (Hazard 2)}}
**Negative results:** {{what did not work, recorded, not dropped}}
**Reservations:** {{paths still in progress — "work in progress, do not
touch" (§2.10 rule 2)}}
**Handoff:** {{ready to gate | blocked on {{X}}}}

Role: worker({{WORKER_MODEL}})
```

<!-- Compaction (AGENTS.md §2.13): when this file exceeds ~50k tokens, the
     worker (its owner) collapses closed entries into one line each; another
     role witnesses the block; the diff reviewer gates the witness verdict. -->
