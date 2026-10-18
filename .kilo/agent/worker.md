# Worker — host adapter (Kilo)

> **This file is a pointer, not a definition.** The canonical worker
> definition lives at [`roles/worker.md`](../../roles/worker.md) — read
> AGENTS.md first, then that file, then `docs/STATE-OF-THE-PROJECT.md`,
> then the active round in `SPEC.md`.
>
> This adapter exists only because the Kilo host auto-loads role files from
> `.kilo/agent/`. It is gitignored host state; it never duplicates the
> canonical content (single-sourcing — the duplicated-default hazard class,
> AGENTS.md §2.4 Hazard 1). If `roles/worker.md` and anything here ever
> disagree, the canonical file wins.
