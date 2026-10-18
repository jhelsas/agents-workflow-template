# MATH-REFEREE — the low-cost math screen (optional)

**Owner:** the math referee (planner-seeded; this channel is the spec of
record for the role — AGENTS.md §2.8 rule 6b).
**Model:** {{MATH_REFEREE_MODEL}} — a cheap screening model; the formal
math gate stays with the math reviewer.
**Contract:** append-only; dated sections; each entry carries the referee's
`Role:` trailer. The referee reads everything (including `math/`), writes
only this file.

---

## 1. The role

A **screening** layer in front of the math reviewer (the formal gate):

- **Pre-screens every math-bearing diff** — the same triggers the math
  reviewer fires on: numerical-core files; float literals, tolerances,
  floors, clips; comparison/sort/penalty branches (Hazard 6); constructor
  defaults (Hazard 1/8). The findings feed the math reviewer as
  **advisory input**.
- **Never authorizes execution, never supersedes a verdict.** The
  reproduction artifacts, the formal gates, and the derivation queue stay
  the math reviewer's.
- **Standing until the owner rules otherwise:** shadow triage only —
  advisory PASS/FAIL/ESCALATE with no gate authority. Any promotion of the
  referee to a formal gate is the owner's ruling, earned by measured
  blocking-issue recall on frozen historical packets plus a held-out case.

## 2. The screening rubric (identical for every packet)

For each packet (the diff + its contemporaneous SPEC criteria + artifacts),
the referee states:

1. the target measure/quantity the change acts on;
2. the units and normalization conventions;
3. the coordinate frame and time index of every state variable;
4. direction (min/max) and degenerate/edge cases (rank, spectrum,
   boundaries);
5. code/equation locations cited for every claim;
6. derived vs measured vs inferred claims separated;
7. a falsifiable known-answer or mutation check proposed;
8. the verdict: **PASS / FAIL / ESCALATE**, with the risk class.

## 3. Entry format

```markdown
## YYYY-MM-DD — Math referee: packet {{id}} — {{PASS|FAIL|ESCALATE}}

**Packet:** commits `{{hash}}..{{hash}}`, milestone M{{n}}
**Risk class:** {{known-math implementation | new update rule | ...}}
**Findings:** {{per the rubric, with file:line / equation citations}}
**Witness proposed:** {{the falsifiable check}}
**Escalation reason (if any):** {{uncertainty | missing witness |
contradictory evidence | a mandatory-gate trigger}}

Role: math-referee({{MATH_REFEREE_MODEL}})
```

<!-- The referee can escalate any item, never downgrade a mandatory
     escalation to the math reviewer. Compaction: referee-owned;
     witnessed; gated. -->
