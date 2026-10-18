# State of the Project — {{PROJECT}}

**Date:** {{DATE}} (re-dated at every compaction checkpoint, per AGENTS.md
§2.13 — a stale date here is a Finding-class defect)
**Branch:** `{{branch}}` ({{round state}})
**Audience:** an agent (or human) picking this up cold. Read this first,
then follow the pointers.

---

> **CRITICAL NOTICE:** read {{the reports that bound current claims}} before
> citing any comparative number. Provenance rules (AGENTS.md Hazard 2) apply
> to every number in this file.

## 1. What this project is

{{ONE_LINER}}. The owner's goals, in priority order:

1. **{{goal 1 — usually correctness/reproducibility}}**
2. **{{goal 2}}**
3. **{{goal 3}}**
4. **{{goal 4}}**

Later goals must not be pursued by weakening earlier ones.

<!-- What belongs here: the identity, the priority ladder, and the
     non-negotiables. Not the history — the history lives in SPEC's summary
     blocks and git log. -->

## 2. Where the work stands ({{DATE}})

- **The defensible claim:** {{headline, with its provenance}}
- **{{The 3-6 standing findings, each with its milestone/commit}}
- **The process is a contribution:** {{N}} hazards documented; every protocol
  rule traces to a real incident.

## 3. Repository structure (current)

| path | what it is |
|---|---|
| `{{package}}/` | {{the core code}} |
| `tests/` | {{the suite; current count re-verified under `bin/tw-suite`}} |
| `experiments/` | {{the harnesses and result artifacts}} |
| `tools/` | {{the invariant/wiring checkers}} |
| `docs/` | the channels, specs, reports |
| `bin/` | the workflow wrappers |

## 4. The channels (AGENTS.md §2.8 rule 2, §2.13)

| channel | owner |
|---|---|
| `SPEC.md` / `docs/STATE-OF-THE-PROJECT.md` / `docs/BACKLOG.md` | planner |
| `docs/REVIEW_LOG.md` / `docs/IDEAS-REVIEWER.md` | reviewer |
| `docs/WORKER_LOG.md` | worker |
| `ADVISOR_NOTES.md` / `docs/IDEAS-ADVISOR.md` | advisor |
| `docs/INVARIANTS.md` | owner-approved entries |
| `math/MATH-REVIEW.md` / `docs/MATH-REFEREE.md` (optional) | math pair |

Closed rounds live in each channel's summary block; the active round stays
verbatim in SPEC.md.

## 5. Active work ({{round state}})

{{Round N: compiled/not compiled; the milestone ladder one line each; what
is gated and why; what the next decision point is.}}

## 6. Where to look

| question | answer |
|---|---|
| what is the protocol? | [AGENTS.md](../AGENTS.md) |
| what is the current work? | [SPEC.md](../SPEC.md), active round |
| what was gated and when? | [REVIEW_LOG.md](REVIEW_LOG.md) |
| what did the worker deliver? | [WORKER_LOG.md](WORKER_LOG.md) |
| what is parked? | [BACKLOG.md](BACKLOG.md) |
| what is untested? | [IDEAS-REVIEWER.md](IDEAS-REVIEWER.md), [IDEAS-ADVISOR.md](IDEAS-ADVISOR.md) |
| what are the contracts? | [INVARIANTS.md](INVARIANTS.md) |

## 7. How to run things

```bash
bin/tw-suite        # the full suite (baseline count: {{N}} passing)
bin/tw-test <node>  # targeted
{{the project's main entry points / experiment commands}}
```

## 8. Housekeeping state ({{DATE}}, this refresh)

{{Channel sizes vs the ~50k-token thresholds; compactions owed; witnesses
owed; anything the next compaction checkpoint must not forget.}}
