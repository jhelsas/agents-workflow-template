# BACKLOG — the deferred-milestone and todo register

> **Purpose.** A stable, append-only register of milestones and todos that
> are **deferred** (parked, gated, or queued) so they are not lost while
> the project progresses — and so they can be **written off** deliberately
> when the time comes. The active work lives in [`SPEC.md`](../SPEC.md);
> the untested ideas live in
> [`docs/IDEAS-REVIEWER.md`](IDEAS-REVIEWER.md) and
> [`docs/IDEAS-ADVISOR.md`](IDEAS-ADVISOR.md); this file holds the
> *committed-but-not-now* items.
>
> **Contract.** Append-only; dated sections; the **planner owns the
> milestone statuses** (it compiles SPEC.md and updates the statuses here);
> any role may append a deferral. An item leaves this file by one of two
> routes: **graduated** (the planner compiles it into SPEC.md — the entry
> gains a `Graduated to M<n>` line) or **written off** (a dated entry states
> the reason — refuted, superseded, or no longer relevant). The full text
> stays; corrections supersede, never edit.
>
> **The write-off rule.** An item is written off only with a stated reason
> and a pointer to the evidence (a report, a commit, a measured result).
> "We forgot about it" is not a write-off; "M34 refuted it" is.

---

## YYYY-MM-DD — The deferred milestones (the current register)

| item | what it is | source | gate / reason | status |
|---|---|---|---|---|
| **M{{n}}** | {{one line}} | SPEC Round {{N}} | {{the condition that un-blocks it}} | deferred |
| **{{item}}** | {{one line}} | REVIEW_LOG {{date}} | **graduated to M{{m}}** (SPEC Round {{N}}) | graduated |
| **{{item}}** | {{one line}} | {{channel}} | {{held: the falsifier did not fire}} | held |

## YYYY-MM-DD — The deferred todos (smaller items)

- **{{todo}}** — {{one line; who owes it; what gates it}}.

## YYYY-MM-DD — The written-off items (the do-not-re-propose list)

| item | written off because | evidence |
|---|---|---|
| **{{item}}** | {{refuted / superseded / no longer relevant}} | {{report or commit}} |

<!-- The write-off list is the do-not-re-propose register: an idea refuted
     here does not return as a "new" idea without new evidence. Compaction:
     planner-owned; witnessed; gated (AGENTS.md §2.13). -->
