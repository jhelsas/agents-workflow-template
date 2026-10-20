---
name: planner
description: Pointer to the canonical planner definition (roles/planner.md).
---

# Planner — host adapter (goose)

> **This file is a pointer, not a definition.** The canonical planner
> definition lives at [`roles/planner.md`](../../roles/planner.md) — read
> AGENTS.md first, then that file, then `docs/STATE-OF-THE-PROJECT.md`,
> then the compile inputs.
>
> This adapter exists only because the goose host discovers custom agents
> from `.agents/agents/` (project-level; global agents live at
> `~/.agents/agents/`). goose reads `AGENTS.md` itself as a context file
> (`CONTEXT_FILE_NAMES` defaults to `["AGENTS.md", ".goosehints"]`),
> so only the canonical role file needs this pointer. It is gitignored
> host state; it never duplicates the
> canonical content (single-sourcing — the duplicated-default hazard class,
> AGENTS.md §2.4 Hazard 1). If `roles/planner.md` and anything here ever
> disagree, the canonical file wins.
