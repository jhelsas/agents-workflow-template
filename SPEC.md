# SPEC.md — the milestone register

> **Owner:** the planner. This file is the planner→worker channel: the
> current milestone list, compiled from the owner's goals, the diff reviewer's
> gate findings (REVIEW_LOG), the advisor's findings, and the BACKLOG
> graduations. The worker executes it verbatim; nobody else writes it.
>
> **Compaction (AGENTS.md §2.13):** closed rounds collapse into the summary
> blocks below (one line per milestone: number, status, commit, one-line
> outcome). **Open milestones, pending decisions, and the active round stay
> verbatim.** Full text: `git log SPEC.md`. The worker witnesses each
> compaction block against the record at resume; the diff reviewer gates the
> witness verdict.

---

# Closed-round summary (example format)

<!-- One block per compaction pass; one row per round; never edited after
     the witness verdict is gated. "Open items carried" lines record the
     no-open-item-lost check. -->

| Round | Milestones | Commits | Outcome (one line) |
|---|---|---|---|
| 1 | M1-M4 | `abc1234..def5678` | correctness remediation; M3's negative result recorded |
| 2 | M5-M7 | (see git log) | the floor fix; either verdict honest — M6 refuted the premise |

Open items carried into Round 3 (the no-open-item-lost check): **M8** stays
held (its falsifier did not fire); **M9** deferred to BACKLOG with a
recorded reason.

---

# Round 3 — {{TITLE}} (ACTIVE — the template)

**Source:** the owner's {{DATE}} directive, the diff reviewer's Round-2 batched
gate (REVIEW_LOG {{commit}}), the advisor's Finding {{N}}.

**The state at compile ({{DATE}}):** one paragraph — what is done, what the
last gates said, what the current baseline is. Every number cited carries
its file/commit (Hazard 2). No milestone may be compiled from a number that
cannot be re-derived from a committed artifact.

**The round's design thesis:** one paragraph — the axis this round moves,
and why now. No milestone composes an ungated mechanism with another; each
arm names its baseline in its falsifier.

## Round-3 global rules

1. The standing execution discipline carries: `bin/tw-test` / `bin/tw-suite`
   / `bin/tw-commit`; every new flag default-off with a bit-identity pin
   and a reachability check (Hazard 8/11); the both-directions check
   wherever a comparison is touched (Hazard 6).
2. **Either verdict is a result** — negatives are recorded with the same
   rigor as positives.
3. The worker stops at the owner's word (§2.14); each milestone is
   independently committable.

## Milestone 12 — {{TITLE}}

**Files:** `{{package}}/{{module}}.py`
**Test:** `bin/tw-test tests/test_{{module}}.py -q`
**Done when:** {{the observable, testable completion condition}}
**Status:** pending

### Task 12.1 — {{TITLE}}

**Files:** `{{package}}/{{module}}.py` (the {{function}} site only)
**Test:** `bin/tw-test tests/test_{{module}}.py::test_{{red_pin}} -q`
**Done when:** the red pin turns green and the existing suite is untouched.
**Controls:** the M{{n}} bit-identity pin — with the new flag off (the
default), the output of {{entry point}} is bit-identical to the pre-change
commit; a reachability probe asserts the flag actually reaches the output.
**Markers to observe:** {{the intermediate quantity}} in the run ledger;
values outside {{range}} falsify the approach (the veto floor).
**Hazards:** Hazard 1 (the default is duplicated at {{sites}} — single-source
it); Hazard 6 (the sort at {{line}}); Hazard 8 (the parameter was dead).
**Provenance:** the report records script, revision, CLI, config, and the
result files. **Status:** pending

### Task 12.2 — ...

(same format; each task gates the next)

---

<!-- Milestone status conventions:
     pending | COMPLETE (`hash`, YYYY-MM-DD — one-line outcome) |
     DEFERRED (→ BACKLOG, reason) | HELD (condition stated)
     A milestone with a compiled decomposition lists its tasks with their
     own statuses; the milestone is COMPLETE only when every task is. -->
