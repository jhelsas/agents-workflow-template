---
name: math-referee
description: Pointer to the canonical math-referee definition (roles/math-referee.md).
---

# Math referee — host adapter (goose, optional role)

> **This file is a pointer, not a definition.** The canonical math-referee
> definition lives at
> [`roles/math-referee.md`](../../roles/math-referee.md) — read AGENTS.md
> first, then that file, then `docs/MATH-REFEREE.md` (the channel is the
> spec of record for this role).
>
> This adapter exists only because the goose host discovers custom agents
> from `.agents/agents/` (project-level; global agents live at
> `~/.agents/agents/`). goose reads `AGENTS.md` itself as a context file
> (`CONTEXT_FILE_NAMES` defaults to `["AGENTS.md", ".goosehints"]`),
> so only the canonical role file needs this pointer. It is gitignored
> host state; it never duplicates the
> canonical content (single-sourcing — the duplicated-default hazard class,
> AGENTS.md §2.4 Hazard 1). If the canonical file and anything here ever
> disagree, the canonical file wins.
