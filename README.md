# agent-workflow-template

A portable multi-agent workflow for **milestone-driven, evidence-gated**
software and research projects. It is distilled from the operating protocol of
the originating project (a long-running CEM research prototype); every rule in
it traces to a measured incident there, not to a hypothetical.

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
| **reviewer** | mid model, high effort | batched PASS/FAIL gates on committed diffs only | reads the whole codebase, commits others' work |
| **advisor** | cheap model | interactive Q&A, sanity checks, data verification | compiles, gates, executes |
| **math reviewer** (opt.) | strongest model | formal math gate: derivations, floors, tolerances, update rules | writes outside its workspace |
| **math referee** (opt.) | cheap model | low-cost math pre-screen (PASS/FAIL/ESCALATE), advisory only | authorizes anything |

**The loop:** owner states goals → planner compiles a round of milestones
into `SPEC.md` (each with exact files + exact test command + task
decomposition) → worker executes milestones one at a time under the TDD
protocol, appending to `WORKER_LOG` and committing each deliverable →
reviewer gates the batched committed diffs at round close → findings go back
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

## 2. Folder map

```
agent-workflow-template/
├── README.md                    ← this guide (do not copy into the project)
├── AGENTS.md                    ← the operating manual (the protocol)
├── SPEC.md                      ← the milestone register (planner-owned)
├── ADVISOR_NOTES.md             ← advisor → planner/reviewer channel
├── bin/
│   ├── tw-test                  ← targeted test wrapper (env prefix baked in)
│   ├── tw-suite                 ← full-suite pre-commit gate
│   └── tw-commit                ← commit wrapper (identity + role trailers)
├── roles/                      ← the six canonical role definitions (host-neutral)
│   ├── worker.md  reviewer.md  advisor.md  planner.md
│   └── math-reviewer.md  math-referee.md  (the optional math pair)
├── .kilo/agent/                ← example host adapters (Kilo) — pointers to roles/
├── docs/
│   ├── STATE-OF-THE-PROJECT.md  ← the situation report (read FIRST)
│   ├── REVIEW_LOG.md            ← reviewer → planner channel
│   ├── WORKER_LOG.md            ← worker → reviewer channel
│   ├── IDEAS-REVIEWER.md        ← reviewer-owned untested ideas
│   ├── IDEAS-ADVISOR.md         ← advisor-owned untested ideas
│   ├── BACKLOG.md               ← deferred register + write-off list
│   ├── INVARIANTS.md            ← the contract register (executable witnesses)
│   └── MATH-REFEREE.md          ← optional: low-cost math screen
└── math/
    └── MATH-REVIEW.md           ← optional: formal math-review channel
```

**Core set** (every project): AGENTS, SPEC, STATE, REVIEW_LOG, WORKER_LOG,
ADVISOR_NOTES, IDEAS-REVIEWER, IDEAS-ADVISOR, BACKLOG, INVARIANTS, the three
`bin/` wrappers, and the four core role definitions under `roles/`.
**Optional** (math-heavy projects only): `docs/MATH-REFEREE.md`,
`math/MATH-REVIEW.md`, and the two math role definitions.

## 3. Adoption checklist

1. **Copy the skeleton.** Everything above except this README into the
   project root. `roles/` is committed and travels with the clone — the
   workflow does not assume any particular agent host. If your host
   auto-loads role files from its own directory (Kilo: `.kilo/agent/`),
   create **thin pointer adapters** there, like the ones in this template,
   and gitignore that directory: adapters point at `roles/<role>.md`, never
   copy them (AGENTS.md §2.0). Not using Kilo? Delete `.kilo/` — for any
   other host (or a human), `roles/<role>.md` is the definition to load.
2. **Fill the placeholders** (see §4 below) across AGENTS.md, SPEC.md,
   STATE, and the `bin/` wrappers.
3. **Adapt `bin/`** to your test runner and environment. The contract is not
   the command — it is that *nobody retypes the environment prefix by hand*
   and nobody runs a bare global test inside a milestone.
4. **Seed the hazard register** (AGENTS.md §2.4). It starts with the generic
   classes already listed there; from then on, every real incident in YOUR
   project becomes a numbered hazard with the file, the line, the failure,
   and the fix. An empty hazard register is a lie of omission — expect the
   first incidents within a week and record them.
5. **Assign models per role** and pin reasoning effort explicitly for each
   (AGENTS.md §2.8 rules 5, 8). Expensive judgment, cheap execution.
6. **Seed `docs/STATE-OF-THE-PROJECT.md`** §1 (what the project is, goals in
   priority order) and §7 (how to run things).
7. **Have the planner compile Round 1** into `SPEC.md` from the owner's
   goals, using the milestone format verbatim (AGENTS.md §2.6).
8. **Run one cheap milestone end-to-end** (worker → commit → WORKER_LOG →
   reviewer gate → REVIEW_LOG) before trusting the loop with real work.

## 4. Placeholders

| placeholder | meaning | example |
|---|---|---|
| `{{PROJECT}}` | project name | `tw-cem` |
| `{{ONE_LINER}}` | one-line description | `CEM optimizer research prototype` |
| `{{DATE}}` | last-updated date | `2026-10-18` |
| `{{TEST_CMD}}` | the targeted test command | `bin/tw-test tests/test_x.py -q` |
| `{{SUITE_CMD}}` | the full-suite gate | `bin/tw-suite` |
| `{{OWNER_NAME}}` / `{{OWNER_EMAIL}}` | commit identity | — |
| `{{WORKER_MODEL}}` etc. | per-role model ids | see AGENTS.md §2.8 |
| `{{HOSTNAME}}` | the machine name in trailers | `haven` |

The `tw-` script prefix is heritage from the originating project. Renaming is
allowed but must be done in one pass: the three `bin/` files plus every
reference in AGENTS.md and the role definitions.

## 5. Design rationale (why it is shaped this way)

1. **Channels, not conversations.** Agents coordinate through append-only
   files with stable paths, so each agent's prompt prefix stays cacheable
   across cycles — the measured cost lever in the origin project.
2. **Single owner per file.** Two writers to one file produced a real
   ownership incident; the rule is now absolute.
3. **Diff-only, batched review.** The reviewer's cost was 98% input reads at
   a ~950:1 read:output ratio before this rule; it reviews `git diff` +
   acceptance criteria, once per completed milestone batch.
4. **The planner never ingests raw data.** The worker summarizes; the
   planner compiles. A cached planner token cost 42× a worker token.
5. **Compaction on a schedule.** Channels grow by append and are compacted
   (closed rounds → one-line summary entries) at ~50k tokens, witnessed by
   another role and gated by the reviewer, so nothing open is ever lost.
6. **Every protocol rule traces to an incident.** Rules without a recorded
   failure mode get ignored; rules with one get followed.

## 6. Maintenance

This folder is gitignored in the origin repo **by design** (it is workflow
infrastructure, not project code) and is refreshed periodically from the
origin project's lessons. Do not commit it into the origin repository; do
commit the adapted copy into an adopting repository.
