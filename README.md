# agent-workflow-template

A portable multi-agent workflow for **milestone-driven, evidence-gated**
software and research projects. It is distilled from the operating protocol of
a long-running research project; every rule in it traces to a measured
incident, not to a hypothetical.

The folder mirrors the **root of an adopting project**. Copy everything
(except this README) into your project root and adapt the placeholders.

---

## 1. The model in one page

**Roles** (six; the last two are optional for math-heavy projects):

| role | tier | what it does | never does |
|---|---|---|---|
| **owner** | human | rules, arbitrates, approves invariants and scope | — |
| **planner** | strong model, high effort | compiles `SPEC.md` rounds, owns STATE/BACKLOG, terminates after compile | executes, gates, chats |
| **worker** | cheap model | the TDD loop: implementation, tests, data crunching, reports | compiles specs, gates |
| **diff reviewer** | mid model, high effort | batched PASS/FAIL gates on committed diffs only | reads the whole codebase, commits others' work |
| **advisor** | cheap model | interactive Q&A, sanity checks, data verification | compiles, gates, executes |
| **math reviewer** (opt.) | strongest model | formal math gate: derivations, floors, tolerances, update rules; **reached only via the math referee** (§2.8 rules 6a/6b) | writes outside its workspace |
| **math referee** (opt.) | cheap model | low-cost math pre-screen (PASS/FAIL/ESCALATE), advisory only; **the sole forwarder to the math reviewer** (§2.8 rule 6b) | authorizes anything |

**The loop:** owner states goals → planner compiles a round of milestones
into `SPEC.md` (each with exact files + exact test command + task
decomposition) → worker executes milestones one at a time under the TDD
protocol, appending to `WORKER_LOG` and committing each deliverable →
diff reviewer gates the batched committed diffs at round close → findings go back
to the planner via `REVIEW_LOG` → repeat. The advisor answers questions on
demand. The owner rules at every escalation.

**The discipline that makes it work:**

- **Append-only, single-owner channels.** Each inter-agent file has exactly
  one writer; it grows at the tail so prompt-prefix caches stay stable.
- **Every claim carries provenance.** No number is quoted without its file,
  commit, and revision. Negative results are recorded, never dropped.
- **Hazards are incidents, not advice.** The hazard register in AGENTS.md §2.4
  records real past failures so they are not repeated.
- **Cost is tiered by role.** Expensive models spend their tokens on
  judgment; cheap models do the reading and the execution.
- **The high-frequency rules are executable.** Wrapper-level guards
  (`tools/protocol_guards.py`, AGENTS.md §2.15) catch honest mistakes — a
  missing trailer, a deleted channel line, `--lf` with no recorded failure —
  at the `bin/*` boundary, and a hermetic test suite pins the wiring.

## 2. Folder map

```
agent-workflow-template/
├── README.md                    ← this guide (do not copy into the project)
├── AGENTS.md                    ← the operating manual (the protocol)
├── SPEC.md                      ← the milestone register (planner-owned)
├── ADVISOR_NOTES.md             ← advisor → planner/diff reviewer channel
├── bin/
│   ├── tw-test                  ← targeted test wrapper (env prefix + --lf guard)
│   ├── tw-suite                 ← full-suite pre-commit gate
│   ├── tw-commit                ← commit wrapper (identity + trailers + guards)
│   └── tw-review-diff           ← diff reviewer packet packager (diff + criteria only)
├── tools/
│   └── protocol_guards.py       ← the executable protocol guards (AGENTS.md §2.15)
├── tests/
│   └── test_protocol_guards.py  ← hermetic guard tests (keep green)
├── .gitignore                   ← guard/host-local state (.tw_last_failure, .tw_guards.log)
├── roles/                      ← the six canonical role definitions (host-neutral)
│   ├── worker.md  diff-reviewer.md  advisor.md  planner.md
│   └── math-reviewer.md  math-referee.md  (the optional math pair)
├── .agents/agents/             ← example host adapters (goose) — pointers to roles/
├── docs/
│   ├── STATE-OF-THE-PROJECT.md  ← the situation report (read FIRST)
│   ├── REVIEW_LOG.md            ← diff reviewer → planner channel
│   ├── WORKER_LOG.md            ← worker → diff reviewer channel
│   ├── IDEAS-REVIEWER.md        ← diff reviewer-owned untested ideas
│   ├── IDEAS-ADVISOR.md         ← advisor-owned untested ideas
│   ├── BACKLOG.md               ← deferred register + write-off list
│   ├── INVARIANTS.md            ← the contract register (executable witnesses)
│   └── MATH-REFEREE.md          ← optional: low-cost math screen
└── math/
    └── MATH-REVIEW.md           ← optional: formal math-review channel
```

**Core set** (every project): AGENTS, SPEC, STATE, REVIEW_LOG, WORKER_LOG,
ADVISOR_NOTES, IDEAS-REVIEWER, IDEAS-ADVISOR, BACKLOG, INVARIANTS, the four
`bin/` wrappers, `tools/protocol_guards.py`,
`tests/test_protocol_guards.py`, and the four core role definitions under
`roles/`.
**Optional** (math-heavy projects only): `docs/MATH-REFEREE.md`,
`math/MATH-REVIEW.md`, and the two math role definitions.

## 3. Adoption checklist

1. **Copy the skeleton.** Everything above except this README into the
   project root. `roles/` is committed and travels with the clone — the
   workflow does not assume any particular agent host. If your host
   discovers agent files from its own directory (goose: `.agents/agents/`,
   a custom agent with a `name:` frontmatter — goose reads `AGENTS.md`
   itself as a context file, `CONTEXT_FILE_NAMES` defaults to
   `["AGENTS.md", ".goosehints"]`, so only `roles/<role>.md` needs the
   pointer), keep the **thin pointer adapters** this template ships there,
   pointed at your `roles/<role>.md` — never copy the canonical content
   (AGENTS.md §2.0). Any other host: create the same thin-pointer pattern
   wherever it auto-loads, and gitignore that directory. Not using goose?
   Delete `.agents/` — for any other host (or a human),
   `roles/<role>.md` is the definition to load.
2. **Fill the placeholders** (see §4 below) across AGENTS.md, SPEC.md,
   STATE, and the `bin/` wrappers.
3. **Adapt `bin/`** to your test runner and environment. The contract is not
   the command — it is that *nobody retypes the environment prefix by hand*
   and nobody runs a bare global test inside a milestone. `bin/tw-commit`
   commits **staged changes only**: stage your deliverables before the
   wrapper.
4. **Run the guard suite and keep it green:** `python -B -m pytest
   tests/test_protocol_guards.py -q`. It is hermetic (throwaway git
   fixtures) and pins the wrapper wiring (AGENTS.md §2.15). Adopt the
   shipped `.gitignore` — it covers the guard state (`.tw_last_failure`,
   `.tw_guards.log`).
5. **Seed the hazard register** (AGENTS.md §2.4). It starts with the generic
   classes already listed there; from then on, every real incident in YOUR
   project becomes a numbered hazard with the file, the line, the failure,
   and the fix. An empty hazard register is a lie of omission — expect the
   first incidents within a week and record them.
6. **Assign models per role** and pin reasoning effort explicitly for each
   (AGENTS.md §2.8 rules 5, 8). Expensive judgment, cheap execution.
7. **Seed `docs/STATE-OF-THE-PROJECT.md`** §1 (what the project is, goals in
   priority order) and §7 (how to run things).
8. **Have the planner compile Round 1** into `SPEC.md` from the owner's
   goals, using the milestone format verbatim (AGENTS.md §2.6).
9. **Run one cheap milestone end-to-end** (worker → commit → WORKER_LOG →
   diff reviewer gate → REVIEW_LOG) before trusting the loop with real work.

## 4. Placeholders

| placeholder | meaning | example |
|---|---|---|
| `{{PROJECT}}` | project name | `my-project` |
| `{{ONE_LINER}}` | one-line description | `a research prototype` |
| `{{DATE}}` | last-updated date | `2026-10-18` |
| `{{TEST_CMD}}` | the targeted test command | `bin/tw-test tests/test_x.py -q` |
| `{{SUITE_CMD}}` | the full-suite gate | `bin/tw-suite` |
| `{{OWNER_NAME}}` / `{{OWNER_EMAIL}}` | commit identity | — |
| `{{WORKER_MODEL}}` etc. | per-role model ids | see AGENTS.md §2.8 |

The `tw-` script prefix is arbitrary. Renaming is optional and
must be done in one pass: the `bin/` files plus every reference in
AGENTS.md, `tools/protocol_guards.py`, `tests/test_protocol_guards.py`, and
the role definitions.

## 5. Design rationale (why it is shaped this way)

1. **Channels, not conversations.** Agents coordinate through append-only
   files with stable paths, so each agent's prompt prefix stays cacheable
   across cycles — the measured cost lever in the origin project.
2. **Single owner per file.** Two writers to one file produced a real
   ownership incident; the rule is now absolute.
3. **Diff-only, batched review.** The diff reviewer's cost was 98% input reads at
   a ~950:1 read:output ratio before this rule; it reviews `git diff` +
   acceptance criteria, once per completed milestone batch.
4. **The planner never ingests raw data.** The worker summarizes; the
   planner compiles. A cached planner token cost 42× a worker token.
5. **Compaction on a schedule.** Channels grow by append and are compacted
   (closed rounds → one-line summary entries) at ~50k tokens, witnessed by
   another role and gated by the diff reviewer, so nothing open is ever lost.
6. **Every protocol rule traces to an incident.** Rules without a recorded
   failure mode get ignored; rules with one get followed.
