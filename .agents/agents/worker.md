---
name: worker
description: Pointer to the canonical worker definition (roles/worker.md).
---

# Worker — host adapter (goose)

> **This file is a pointer, not a definition.** The canonical worker
> definition lives at [`roles/worker.md`](../../roles/worker.md) — read
> AGENTS.md first, then that file, then `docs/STATE-OF-THE-PROJECT.md`,
> then the active round in `SPEC.md`.
>
> This adapter exists only because the goose host discovers custom agents
> from `.agents/agents/` (project-level; global agents live at
> `~/.agents/agents/`). goose reads `AGENTS.md` itself as a context file
> (`CONTEXT_FILE_NAMES` defaults to `["AGENTS.md", ".goosehints"]`),
> so only the canonical role file needs this pointer. It is gitignored
> host state; it never duplicates the
> canonical content (single-sourcing — the duplicated-default hazard class,
> AGENTS.md §2.4 Hazard 1). If `roles/worker.md` and anything here ever
> disagree, the canonical file wins.
