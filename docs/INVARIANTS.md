# INVARIANTS — the contract register

> **Purpose.** Each entry is a contract the implementation is *supposed*
> to satisfy, with an executable witness that asserts the contract (not the
> current behaviour). This file is the reference the diff reviewer gates against
> and the worker implements toward. It exists because prose contracts with
> no executable witness drift silently.
>
> **The two binding rules.**
> 1. **Contracts, not behaviour.** The contract field states the *intended*
>    semantics, never what the code currently does. A witness that asserts
>    current behaviour is the pin-defect class (a pin that blesses the bug).
> 2. **Scope is enumerated, never implied.** "All modes" must list the
>    modes. An entry whose scope was not checked is a deadness claim
>    without scope.
>
> **Lifecycle.** The owner approves every entry before its witness is
> implemented. A red witness is the driver for its fix milestone, not a
> tolerated failure. Entries grow by incident; they are never dropped
> without a stated reason recorded in `docs/REVIEW_LOG.md`.

---

## Entry format

```markdown
### INV-00{{n}}: {{the contract, as a one-line law}}

**Contract:** {{the intended semantics, precisely — an equation or an
input/output property, not prose about the code}}
**Scope:** {{every mode / module / path it governs — enumerated}}
**Witness:** `tests/test_invariants.py::{{test_name}}` — {{what the test
constructs and asserts; a red witness is expected while the contract is
unimplemented}}
**Status:** {{unimplemented (at: file:line) | implemented (mode list) |
partially implemented (which modes deviate)}}
**Evidence:** {{the incident or report that created the entry; corrections
carry their own dated annotation}}
```

<!-- Example entries from the origin project (paraphrased):
     INV "the trust region governs every update" — the interpolation weight
     is chosen by bisection so the KL to the old distribution stays under
     the configured bound, in EVERY sampling mode; the first witness sweep
     found two modes silently interpolating at a constant instead.
     The witness, not the prose, caught it. -->
