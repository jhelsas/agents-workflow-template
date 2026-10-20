# AGENTS.md — Guidance for future models

**Project:** {{PROJECT}} — {{ONE_LINER}}
**Last updated:** {{DATE}}

Read [docs/STATE-OF-THE-PROJECT.md](docs/STATE-OF-THE-PROJECT.md) first for
structure, achievements, outstanding goals, and known shortcomings. This file
is the *operating manual*; that file is the *situation report*.

---

## Part 1 — Execution protocol

The following is the mandated execution loop for milestone-driven work in
this repository. Follow it exactly.

> You are an autonomous engineer executing a test-driven development loop.
> Your only goal is to complete the milestones outlined in `SPEC.md`.
>
> **CRITICAL RULES OF EXECUTION:**
> 1. **No Unscoped Context:** Unscoped repository-wide reading for task
>    execution is forbidden — but **bounded invariant sweeps are REQUIRED**
>    at milestone boundaries (§2.8 rule 9) over the milestone's module set.
> 2. **JIT File Reading:** You may only read files explicitly assigned to
>    your current milestone in `SPEC.md`, or files specifically named in a
>    stack trace.
> 3. **Targeted Testing Only:** When verifying code, run only the exact test
>    command specified in the current milestone (e.g. `bin/tw-test
>    tests/test_<module>.py -q`). DO NOT run a global test command.
> 4. **The Last-Failed Loop:** If a test fails, switch your test command to
>    `bin/tw-test --lf --tb=short <target>`. Execute only that targeted
>    command until the specific failing test passes. `--lf` requires a
>    **recorded** failure — the wrapper writes `.tw_last_failure` on a
>    failing run and clears it on a passing one — so the loop cannot skip
>    the baseline run (§2.15).
> 5. **No Hallucinated Scope:** If a test passes, the milestone is complete.
>    Immediately move to the next milestone in `SPEC.md`. Do not refactor
>    passing code or expand your scope.
>
> **Workflow:**
> 1. Read `SPEC.md` to identify the current uncompleted milestone.
> 2. Run the specified targeted test command to establish the baseline
>    failure.
> 3. Parse the traceback.
> 4. Read *only* the specific file and line number mentioned in the traceback.
> 5. Implement the fix and rerun the last-failed command.
> 6. Repeat until the milestone passes, then log the completion.

---

## Part 2 — Project-specific adaptations

The protocol above is the default. The following are **required adaptations**
where the protocol as written would produce wrong results in this
repository. They are not optional.

### 2.0 The role definition files

Each role has a dedicated **canonical** definition file under
`roles/<role>.md` — `worker`, `reviewer`, `advisor`, `planner`,
`math-reviewer`, `math-referee` — mirroring this protocol with the role's
read order, writes, wrappers, and discipline. **If you are running as one
of these roles, read your definition file FIRST**, immediately after this
file; it is prefix-stable and cacheable. The canonical files are
version-controlled and travel with the clone — the workflow does not
assume any particular agent host.

**Host adapters.** An agent host that auto-loads role files from its own
private directory (Kilo: `.kilo/agent/<role>.md`) gets a **thin pointer
adapter** there — a pointer to the canonical file, never a copy. Adapter
directories are gitignored host state, like the rest of the host's local
configuration. The same pattern applies to any other host (a system prompt
snippet, a launcher, a `CLAUDE.md`-style entry point): point at
`roles/<role>.md`; do not duplicate it. Three things stay true and must
not be "cleaned up":

- **This file (AGENTS.md) remains the authoritative protocol.** Any rule
  that exists only in a definition file or adapter is a convenience
  restatement, not the rule.
- **The role definitions do not grant anything.** Scope, standing, and
  authorization live in the rules below (§2.8 rules 3–6b) and in the active
  SPEC round — no definition file or adapter ever widens its role's write
  scope or standing.
- **One source per role.** If a host requires its own file, it points at
  the canonical one; content is never duplicated. A drifted copy is worse
  than no definition at all (the duplicated-default hazard class, §2.4
  Hazard 1).

### 2.1 `SPEC.md` exists — read it first

`SPEC.md` at the repo root holds the current milestone list. Read it before
starting any milestone-driven run. If it is absent, either create it (see
§2.6 for the required format) or — if the task is exploratory rather than
milestone-driven — **do not use the Part 1 protocol**; use the research
workflow in §2.7 instead.

Do not invent milestones. If `SPEC.md` is absent and the task is not
milestone-shaped, say so and stop.

**SPEC.md is compacted on a schedule (§2.13):** closed rounds live in its
summary block (one line per milestone, with commits); the active rounds are
verbatim. Full historical text: `git log SPEC.md`. The current state is in
[docs/STATE-OF-THE-PROJECT.md](docs/STATE-OF-THE-PROJECT.md) — read that
first, not old round text.

### 2.2 Environment — every command needs the wrapper

The protocol's bare test commands will fail or lie without the environment
set up (thread pinning for reproducibility, import paths, bytecode/cache
isolation). **Never retype the prefix by hand** — use `bin/tw-test` and
`bin/tw-suite`, which bake it in. Adapt the wrappers in `bin/` once, at
adoption time, to your project's requirements.

### 2.3 The "no global test run" rule has one exception

Rule 3 forbids a global test run inside the milestone loop. That is correct
for the inner loop. But **before committing any change that touches code**
(or tests, tooling, or build config), run the full suite once via
`bin/tw-suite`.

**The code-touch scope:** the full-suite gate applies to changes that touch
code. **An agent that does not modify code does not need to re-run the test
suite** — documentation-only commits commit without it. The targeted test
commands still apply when a documentation change asserts test behaviour, and
the suite still gates every release boundary regardless of what changed in
between. The current baseline count lives in STATE §7 (the figure moves; the
state report is the source of truth). A change that breaks an unrelated test
is a regression, and the targeted loop will not catch it.

### 2.4 Known hazards — read before touching code

These are real failure classes, each first observed as an actual incident.
The register grows by incident; an entry is never deleted, only corrected by
a dated annotation. **When you create a new hazard entry, name the file, the
location, the failure, and the fix.** Grep for the parameter, never trust a
table — including this one.

<!-- Seed the register with your project's first incidents. The classes
     below generalize; expect to instantiate each within your first weeks. -->

**Hazard 1 — duplicated constants/defaults across call sites.**
A default duplicated in N places drifts in the N+1th. Single-source every
constant that more than one module references; grep for the name before and
after any change.

**Hazard 2 — result staleness and provenance.**
Benchmark/computed results are only valid for the code revision that
produced them. Before quoting any number: compare the commit time of the
relevant change against the result file's mtime, and re-derive headline
numbers from committed files rather than quoting memory or old reports.

**Hazard 2b — "this fix is not binding" must be verified, not argued.**
Reasoning from the call graph is not evidence that a change cannot affect a
result. To claim inertness, re-run a matched subset and compare. Corollary:
a fix can be inert for the headline but not for the gaps.

**Hazard 2c — reproduce with the *recorded* configuration.**
Verification runs must read the config recorded in the result artifact, not
the code defaults. And some components are not bitwise reproducible (GPU
nondeterminism, solver warm starts): compare those at an appropriate
relative tolerance, and compare the *pre-change* code the same way before
declaring a regression.

**Hazard 3 — silent numeric floors and clamps.**
Every floor, clip, tolerance, and default cap is a binding constraint until
measured otherwise; paired constants that must agree (e.g. a covariance floor
and its stopping threshold) must be changed together or not at all. A comment
claiming two values are "identical" is true only until another masked
constraint changes.

**Hazard 4 — misdiagnosed ceilings.**
A performance plateau can be a true fixed point of the mechanism, an
artefact of a Hazard-3 floor, or a different limit entirely (e.g. direction
finding vs conditioning). Do not "fix" a ceiling without first identifying
which one it is; the fixes are orthogonal.

**Hazard 5 — execution-blocking configurations.**
Configurations that pass constructor validation and then crash (stale
kwargs, rank-deficient linear algebra needing `pinv`, duplicated clamps
between caller and callee). Zero-coverage classes are where these live.

**Hazard 6 — direction-dependent logic.**
Any comparison, sort, or penalty that assumes minimization silently inverts
for `maximize=True`. Whenever you touch one, check whether it needs to
branch on the direction flag. The minimizer path is the default everywhere,
so these bugs are invisible until the maximizing path is tested.

**Hazard 7 — mirrored vector/scalar implementations.**
When a vectorized path mirrors a scalar reference, the two disagree at
boundary conditions (clamping just below a ceiling vs unconditionally).
Test them against each other at the boundary, not just in the interior.

**Hazard 8 — silently dead parameters.**
`reg = max(1e-8, requested)` makes `requested=0` a no-op; a documented
parameter that cannot take effect is a bug, not a default. Verify the
parameter actually reaches the output.

**Hazard 9 — telemetry dropped at return sites.**
A field omitted from a return object silently defaults; per-run counters
reset in `__init__` instead of at the top of the run method accumulate
across runs. When you add a result field, grep **every** return site.

**Hazard 10 — checks that only look at one element.**
Indexing `[0]` of a per-item list tests item 0 only (e.g. one constraint of
many). Ask whether the check should span all items.

**Hazard 11 — documented flags that are never read.**
A stored-and-documented option that never changes behaviour is the same bug
class as Hazard 8. Grep for the flag's uses before assuming it works.

<!-- Append your project's specific hazards below this line, numbered onward.
     Format: what happened, where (file:line), why, the fix, the lesson. -->

### 2.5 Git

Commits require a repo-local identity workaround and the role trailers. Use
the wrapper — never hand-assemble the identity flags:

```bash
bin/tw-commit "<message>" "<role>(<model>)"
```

The wrapper's **role argument is required** — a roleless invocation fails
closed before anything is committed (§2.15; the old `unspecified` fallback
could never satisfy the trailer guard, and its failure misreported the
cause — Hazard 8/11).

Every commit message carries **both** trailers (the owner's convention):

- a `Role: <role>(<model>)` line in the message body — the machine-readable
  role attribution, so *who produced* each commit is recoverable from
  `git log` alone;
- a final `Co-authored-by: Kilo <role>(<model>)` trailer — the signature,
  recording the agent and the model that did the work.

The two must **agree** (same role, same model): the `commit-trailer` guard
(§2.15) cross-checks the wrapper's role argument against the message's
`Role:` line at commit time. Angle brackets above are placeholder notation;
the real trailer carries no brackets and no host suffix.

### 2.6 Required `SPEC.md` format

If you create `SPEC.md`, each milestone must name its files and its exact
test command, or the Part 1 protocol cannot be followed:

```markdown
## Milestone 3 — Fix the low-rank floor

**Files:** {{package}}/optimizers/base.py
**Test:** bin/tw-test tests/test_cross_entropy.py -q
**Done when:** the low-rank floor matches the full-covariance floor and the
targeted test passes.
**Status:** pending
```

**The step-by-step norm.** The milestone header above is the *minimum*. For
any milestone that implements, wires, or measures a change — not for pure
documentation or triage items — the planner MUST also provide a **task
decomposition**: ordered sub-tasks (Task N.1, N.2, ...), each in the same
Files / Test / Done when / Status format, each gating the next. The purpose
is to **minimize the worker's room for error**: the worker executes; the
planner has already made the sequencing decisions. Each sub-task must
carry, where applicable:

- **Controls** — the pins and invariants that prove the change is wired and
  inert when it must be (bit-identity patterns; flag-reachability checks).
- **Tests** — the exact targeted command, and what its pass/fail means (a
  red pin that turns green; a bit-identity assertion; a dry-run assertion —
  never "inspection alone").
- **Markers to observe** — the intermediate quantities that say the task is
  on track, and the values that would falsify the approach (veto floors).
- **Hazard callouts** — the named hazard classes the task touches.
- **Provenance requirements** — what the report must record (script,
  revision, CLI, config, result files) so the log-completeness gate holds.

A milestone compiled without the decomposition, where the norm applies, is
an incomplete compile — the reviewer may gate it back to the planner on that
basis alone.

### 2.7 When *not* to use the Part 1 protocol

The Part 1 protocol is designed for **fixing known failures against a
spec**. It is actively harmful for the other mode of work: **empirical
research** — running experiments, comparing implementations, interpreting
results. In research mode:

- Reading broadly *is* required — you cannot interpret a result without
  knowing which code produced it (Hazard 2).
- There is no "passing test" that means "done". The deliverable is a report
  with honest caveats, not a green checkmark.
- Negative results are results. Record them.

If the task is "run this comparison and tell me what happened", use the
research workflow, not the TDD loop.

### 2.8 Agent cost protocol

This project runs a multi-role workflow (owner / planner / worker /
reviewer / advisor, plus the optional math pair). The measured cost levers,
from the origin project's usage audit:

- **Rate asymmetry:** a cached planner token can cost 40× a cached worker
  token; a reviewer token ~12×. Prompt trimming and input discipline on the
  judgment roles is the highest-leverage cost work.
- **Reasoning runaways:** unbounded reasoning under a "max" default effort
  burned the single largest worker cost line. Pin reasoning effort
  explicitly for every role (rule 8) and route runaway-prone work to
  non-reasoning models.
- **Review read overhead:** a reviewer fed the codebase spent 98% of its
  cost on input reads at a ~950:1 read:output ratio. Diff-only ingestion
  (rule 3) is the fix.

Rules for all agents:

1. **Use the wrapper scripts.** The worker MUST invoke `bin/tw-test`
   (targeted tests), `bin/tw-suite` (the full-suite pre-commit gate), and
   `bin/tw-commit` (identity + trailers). Inside a milestone prefer
   `bin/tw-test <node>`; reserve `bin/tw-suite` for the pre-commit gate.
   The wrappers are also where the executable protocol guards are wired
   (§2.15) — the high-frequency rules are executed, not just documented,
   and the wiring is pinned by a hermetic test suite.

2. **Stable, append-only inter-agent files.** **Each inter-agent file has
   exactly ONE owner and can only be written by its owner.** A role may own
   more than one file; a file never has two owners. The channels:

   | channel | owner | purpose |
   |---|---|---|
   | `SPEC.md` | planner | the milestone register (planner → worker) |
   | `docs/STATE-OF-THE-PROJECT.md` | planner | the situation report |
   | `docs/BACKLOG.md` | planner | deferred items + write-offs |
   | `docs/REVIEW_LOG.md` | reviewer | reviewer → planner (gate verdicts) |
   | `docs/WORKER_LOG.md` | worker | worker → reviewer (handoffs) |
   | `ADVISOR_NOTES.md` | advisor | advisor → planner/reviewer (findings) |
   | `docs/IDEAS-REVIEWER.md` | reviewer | reviewer's untested ideas |
   | `docs/IDEAS-ADVISOR.md` | advisor | advisor's untested ideas |
   | `docs/INVARIANTS.md` | owner-approved | the contract register |
   | `math/MATH-REVIEW.md` (opt.) | math reviewer | the formal math channel |
   | `docs/MATH-REFEREE.md` (opt.) | math referee | the low-cost math screen |

   All keep stable paths and grow by **append** so each agent's prompt
   prefix stays cacheable across cycles. Dated `docs/reports/YYYY-MM-DD-*.md`
   names are for one-off artefacts (snapshots, single analyses) and are
   referenced from the stable files, never edited. When a channel exceeds
   ~50k tokens, compact it (§2.13).

3. **Reviewer: diff-only ingestion, batched gates.** The reviewer must NOT
   be fed the full codebase, broad file trees, or large test logs — only
   the `git diff` + the milestone's acceptance criteria, returning a binary
   PASS/FAIL with line-level critiques. Trigger **once per completed
   milestone**, batched (never mid-milestone, never casual Q&A). Gates
   committed diffs only (§2.10); commits only its own REVIEW_LOG entries.

4. **Planner: offline compiler, minimal input context.** NEVER feed it raw
   codebase dumps, test logs, or large data files — the worker summarizes.
   It compiles the multi-milestone `SPEC.md` and terminates; it is NOT
   polled while the worker executes (re-invoke at batch closes or on an
   escalated blocker; never for interactive chat). It owns SPEC, STATE, and
   BACKLOG. The phantom-hash-prevention duty (verify `git cat-file -t`
   before citing a commit) is the planner's.

5. **Worker: output and loop containment.** The execution loop (TDD,
   implementation, test running, data crunching) — read your role definition
   first. The wrappers, JIT reading, bounded reasoning, chunked large
   writes with tail verification, either-verdict honesty, and the
   WORKER_LOG entry per milestone.

6. **Interactive Advisor: dedicated low-cost Q&A role.** For short
   questions, sanity checks, hypothesis exploration, and data checks. It
   answers and verifies; it does NOT compile SPEC.md, run PASS/FAIL gates,
   or execute the TDD loop — and it obeys the provenance rules. Do NOT
   route interactive Q&A to the planner or reviewer.

6a. **Math Reviewer (optional; math-heavy projects): the formal math gate.**
    Pre-execution checks of every SPEC compile carrying a formula,
    derivation, numeric freeze, floor, tolerance, or update rule;
    back-verification of shipped math; the derivation queue. Writes only
    its own workspace; everything else reaches the tree as *proposals*.
    Casual math Q&A goes to the advisor, not the math reviewer.

6b. **Math Referee (optional): the low-cost math screen.** A screening
    layer in front of the math reviewer: pre-screens math-bearing diffs,
    returns PASS / FAIL / ESCALATE with risk class, cited equations, and a
    falsifiable witness — **advisory only**; it never authorizes execution
    and never downgrades a mandatory escalation. Formal gate authority
    stays with the math reviewer unless the owner rules otherwise.

7. **Prefix stability for KV cache reuse.** Keep static context at the top
   of the prompt (`AGENTS.md` → `SPEC.md` → `STATE` → active task). Avoid
   inserting dynamic volatile strings (timestamps) before static content.

8. **Pin `reasoning_effort` explicitly for every role.** Models that default
   to `max` reasoning make runaway reasoning the dominant cost line. Every
   role's session configuration must set it explicitly — `low`/`medium` for
   routine execution (worker, advisor), `high` for judgment roles
   (planner, reviewer, math pair) — and never rely on the provider default.

9. **Model routing is scoped by diff, not by project.** The routing
   decision is made on the `git diff` under review:
   - **Default:** all roles keep their assigned models.
   - **Escalate the oracle, not the kernel:** when a milestone's red-pin
     tests or verification probes cover numerical behaviour (floors,
     tolerances, precision targets), the *test authorship and probe
     verification* may be routed to the strongest available model.
     Generation stays on the worker.
   - **Escalate review of core-math diffs:** if a diff touches
     update-rule/numerical-core code, the math reviewer supplies the second
     pass on that diff alone — diff-only, so the cost stays bounded.
   - **Diff classification heuristic (the cheap routing signal).** A ~50-line
     check on the diff decides escalation: (a) edits under the numerical
     core; (b) adds/edits a float literal, tolerance, floor, or clip; (c)
     touches a comparison, sort, or penalty branch (Hazard 6); (d) adds/edits
     a constructor default (Hazard 1/8). No escalation for docs, harness, or
     data changes.
   - **Measure before making binding:** any routing change is validated
     against usage logs (cost per successful task) before it becomes a
     standing rule.

### 2.9 Line-by-line itemization protocol

When the owner requests a **line-by-line itemization** (or an equivalent
deep-read deliverable), the planner does **not** perform the deep read
(§2.8 rule 4) and the reviewer is **not** fed the codebase (§2.8 rule 3).
Instead:

1. **Planner emits the instruction set, not the itemization** — what to
   examine, how to verify each item (probe, red-pin test, grep — never trust
   a table), and the output format, without line numbers or content claims
   it has not been handed.
2. **The worker performs the deep read and produces the itemization**,
   resolving exact locations and running the verification probes with
   empirical evidence per item.
3. **The reviewer gates the findings, diff-only** — the worker's report +
   triage table + committed pins, not the codebase.

This keeps the expensive roles on judgment, not ingestion.

### 2.10 Commit ownership and handoff discipline

1. **Each role commits its own deliverables.** A role never commits another
   role's uncommitted work.
2. **Handoff is a state, not an action.** A role's turn ends with either
   (a) all deliverables committed and a handoff note recorded in its
   channel, or (b) an explicit "work in progress, do not touch `<paths>`"
   reservation. Downstream roles must check `git status` and the latest
   handoff note before acting on another role's files.
3. **The reviewer gates on committed diffs only.** If the material to gate
   is uncommitted, the reviewer waits for the worker's handoff note; it
   does not commit on the worker's behalf to make the diff exist.
4. **One deliverable, one commit, one owner.** Edits to a deliverable are
   returned to the author role to commit, not committed by the editor.
5. **Role attribution in commit messages** — the `Role:` body line and the
   `Co-authored-by` trailer, per §2.5.

### 2.11 Output truncation is a hazard — treat it as one

Agent sessions may run under a hard completion cap (the origin host set
`max_output_tokens: 8192` while the model advertised 524,288 — real, not a
no-op). A truncated response is not always obviously truncated, in
descending severity:

1. **A truncated file write** — the tool may report success on a file cut
   mid-statement. **After any large write, verify the tail of the file**
   before running tests. A file that ends mid-statement is the signature.
2. **A truncated code block in a reply** — prose reads complete, code stops
   early. Never copy a block into a file without checking where it ends.
3. **A truncated tool-call argument** — long edit payloads are the most
   likely to be cut. Prefer several small edits over one large one.
4. **A truncated channel append** — a document that ends mid-table or
   mid-sentence. Check the tail after appending to any stable channel.

**Rules:** budget output, not just reasoning (the cap is shared); chunk
writes over ~150 lines into successive calls; verify after writing, before
testing; if a response looks like it ended early, say so and re-emit the
remainder — a silently-truncated deliverable that gets committed is worse
than a re-run. The cap is a *session/host setting, not a repository
property*; the rules are cheap enough to follow unconditionally.

### 2.12 Check the *before* distribution, not just the after

When a containment or a metric change "works", verify it constrained the
thing you meant to constrain. (Origin incident: the output cap bounded
visible output, while reasoning tokens were a separate budget — the runaway
class it targeted was unaffected; the maximum visible completion had
exceeded the cap exactly once, ever.) A metric that *looks* like it moved
can be unrelated to the mechanism you tried to contain.

### 2.13 Channel compaction schedule

The append-only rule (§2.8 rule 2) would grow channels without bound;
compaction is **scheduled, not only triggered**:

1. **Cadence: daily during active rounds; weekly minimum during quiet
   periods.** At each boundary the planner checks channel sizes and
   compacts any past ~50k tokens (compaction is cheapest done early).
2. **Ownership and witnessing:** the owning role compacts its own channel;
   the planner compacts SPEC.md, refreshes STATE, and owns all BACKLOG
   writes. **A compaction is an authored write and is never unwitnessed:**
   another role witnesses the summary block against the record (every claim
   cites a commit that exists; superseded content marked, never deleted; no
   open milestone or pending decision lost; statuses match the artifacts),
   and the reviewer gates the witness verdict.
3. **What compacts:** closed milestones/rounds collapse into a summary
   block (one line per milestone: number, status, commit, one-line
   outcome); **open milestones, pending decisions, and the active round
   stay verbatim.** Dated report files never compact — they are immutable
   snapshots; full text is always recoverable from git history.
4. **STATE refreshes on the same cadence:** re-dated and re-pointed at each
   compaction checkpoint so a cold-starting agent reads current state.

A compaction legitimately rewrites channel lines, which the `append-only`
guard would otherwise flag: exempt it at the wrapper with `TW_COMPACTION=1`
and `TW_COMPACTION_REASON=<one line>` — an empty reason exits 2, and the
exemption is recorded to `.tw_guards.log` (§2.15).

### 2.14 Extended-work scheduling

When the owner announces an absence and asks for **extended work**, the
reviewer dimensions the queued milestone set to the stated duration and
hands the planner a compile input; the planner compiles it into `SPEC.md`
as one round. The queue runs **quickest-first**, so a partial run leaves a
closed, committable deliverable at every stop. Each milestone is
independently committable and independently gated; the worker proceeds
autonomously through the ladder and **stops at the owner's return**. The
reviewer batches the gates at batch close.

### 2.15 Executable protocol guards (wrapper-level accident detection)

The high-frequency protocol rules are **executed, not just documented**:
`tools/protocol_guards.py` is wired into the `bin/tw-*` wrappers, and
`tests/test_protocol_guards.py` (hermetic — throwaway git fixtures under
`tmp_path`, no network, no project state) pins both the guards and their
wiring. The closed guard set:

| guard | wire site | catches |
|---|---|---|
| `ping` | CLI/tests only | wiring smoke — the module imports and answers |
| `commit-trailer` | `bin/tw-commit` | missing/duplicated/disagreeing `Role:` vs `Co-authored-by:` trailers; `--role` vs message cross-check; `--message`/`--message-file` conflict |
| `append-only` | `bin/tw-commit` | deletion of channel lines (§2.8 rule 2) in the staged diff |
| `review-diff` | `bin/tw-review-diff` | a reviewer packet that is not diff + acceptance criteria (§2.8 rule 3) |
| `lf` | `bin/tw-test` | `--lf` with no recorded failure (Part 1 step 4) |
| `packet-hash` | `bin/tw-commit` | a frozen reviewer packet that drifted from its recorded hash (`TW_PACKET_MANIFEST`) |

**Scope — read before trusting the guards.** They are wrapper-level
**accident detection**, not authorization: the caller self-declares its
role, so a guard cannot prove who typed a commit, and a deliberate bypass
(editing a wrapper, invoking git directly) is out of scope by design. Exit
codes: `0` = pass, or an inert context (a guard invoked where it does not
govern); `2` = detected violation, with a concrete remediation message. An
unknown guard name exits `2` — a typo must not pass silently (Hazard 8).

**Escape hatches are documented, validated, and logged:**

- `TW_GUARDS_BYPASS=<comma-separated guard names>` bypasses named guards;
  unknown/empty/malformed items are **rejected** (exit 2) — a hatch that
  fails open is a dead guard.
- `TW_COMPACTION=1` exempts `append-only` for a §2.13 compaction;
  `TW_COMPACTION_REASON` carries the reason (empty exits 2) and the
  exemption is appended to `.tw_guards.log` at the repo root (gitignored).

**Adoption.** Keep `tests/test_protocol_guards.py` green — its wiring tests
read the `bin/*` files and assert the guards are actually invoked (Hazard
11: a documented guard that is never wired is dead code). Adapt `CHANNELS`
in `tools/protocol_guards.py` if your channel set differs from the ten in
§2.8 rule 2, and add `.tw_last_failure` / `.tw_guards.log` to `.gitignore`
(the shipped one already has them).

---

## Part 3 — Standing rules for this repository

1. **Never quote a number without checking its provenance.** See Hazard 2.
   This is the single most common way to be wrong here.
2. **Report negative results.** A fix that does not work is a finding. Do
   not quietly drop it.
3. **Do not make external claims from a convenience benchmark.** State the
   benchmark's limits (seeds, families, rotations) wherever a result is
   quoted; external validity is a separate argument.
4. **Change one thing at a time.** Two parameters changed together
   produced a misattributed conclusion in the origin project; isolating
   them reversed it.
5. **Verify before committing.** Full test suite plus a check that the
   change does what you claim, measured.
6. **Clean up temp files** at the end of a task.
7. **Long runs need explicit monitoring.** Redirect output to a file and
   poll the file; never rely on interactive reads of a live process.

---

## Part 4 — Quick reference

```bash
bin/tw-suite                       # the full-suite pre-commit gate (baseline: STATE §7)
bin/tw-test <node>                 # targeted tests, env prefix baked in; --lf is guarded
bin/tw-commit "<message>" "<role(model)>"   # identity + trailers + guards (role REQUIRED)
bin/tw-review-diff <rev-range> [crit.md]   # the reviewer packet: diff + criteria ONLY

python3 tools/protocol_guards.py --guard ping   # wiring smoke (guard set: §2.15)

# the read order for any cold start:
#   1. AGENTS.md                     (this file — the protocol)
#   2. docs/STATE-OF-THE-PROJECT.md  (the situation report)
#   3. SPEC.md, active round         (the work)
#   4. roles/<your-role>.md            (your role definition, if running as a role)
```

**Key documents:**

| document | purpose |
|---|---|
| [STATE-OF-THE-PROJECT.md](docs/STATE-OF-THE-PROJECT.md) | situation report — read first; current baseline |
| [SPEC.md](SPEC.md) | active rounds + closed-round summary |
| [INVARIANTS.md](docs/INVARIANTS.md) | the invariant register |
| [BACKLOG.md](docs/BACKLOG.md) | the deferred register + the written-off list |
| [REVIEW_LOG.md](docs/REVIEW_LOG.md) / [WORKER_LOG.md](docs/WORKER_LOG.md) | the gate/handoff channels |
| [ADVISOR_NOTES.md](ADVISOR_NOTES.md) | the advisor's findings |
| [IDEAS-REVIEWER.md](docs/IDEAS-REVIEWER.md) / [IDEAS-ADVISOR.md](docs/IDEAS-ADVISOR.md) | the untested-idea channels |
