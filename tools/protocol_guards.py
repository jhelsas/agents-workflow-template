#!/usr/bin/env python3
"""Runtime protocol guards for agent-workflow (AGENTS.md §2.8, §2.10, §2.13).

CLI:  python3 tools/protocol_guards.py --guard <name> [options]

Exit codes: 0 = pass (including not-applicable / inert contexts), 2 = detected
protocol violation (prints a concrete, actionable remediation message).

SCOPE -- READ THIS FIRST. These guards are WRAPPER-LEVEL ACCIDENT DETECTION.
They catch honest mistakes (a forgotten trailer, a deleted channel line, an
`--lf` with no recorded failure) at the `bin/tw-*` boundary. They are NOT
authorization, identity verification, or model-access control: the caller
self-declares its role, so a guard cannot prove who typed a commit, and a
deliberate bypass (editing a wrapper, invoking git directly, setting the
hatch) is out of scope and always will be (Hazard 2 -- no overclaiming).

Allowed guard names (CLOSED SET, pinned by the M150 planner plan): ping,
commit-trailer, append-only, review-diff, lf, packet-hash. An unknown name
exits 2 (Hazard 8 -- a typo must not silently pass). A guard invoked in a
context it does not govern is INERT -- exit 0, never exit 2; exit 2 is
reserved for detected violations.

Escape hatch (documented, validated, logged whenever used):
TW_GUARDS_BYPASS=<comma-separated guard names>. Unknown/empty/malformed
items are REJECTED (exit 2) -- a hatch that fails open is a dead guard.
Compaction exemption (§2.13): TW_COMPACTION=1 exempts the append-only check;
TW_COMPACTION_REASON carries the reason (empty reason exits 2) and the
exemption is recorded to .tw_guards.log at the repo root.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys

OK, VIOLATION = 0, 2

# The ten stable channels (AGENTS.md §2.8 rule 2). Append-only, one owner each.
CHANNELS = (
    "SPEC.md",
    "ADVISOR_NOTES.md",
    "docs/REVIEW_LOG.md",
    "docs/WORKER_LOG.md",
    "docs/STATE-OF-THE-PROJECT.md",
    "docs/IDEAS-REVIEWER.md",
    "docs/IDEAS-ADVISOR.md",
    "docs/BACKLOG.md",
    "docs/MATH-REFEREE.md",
    "math/MATH-REVIEW.md",
)

ROLE_RE = re.compile(r"^Role:\s*([A-Za-z0-9_.\-]+)\(([^)]+)\)\s*$", re.M)
COAUTHOR_RE = re.compile(
    r"^Co-authored-by:\s*goose\s+([A-Za-z0-9_.\-]+)\(([^)]+)\)\s*$", re.M
)
PACKET_MARKER = "# review-diff packaging (diff reviewer input)"
PACKET_DIFF_HEADER = "## git diff"

BYPASS_ENV = "TW_GUARDS_BYPASS"
LF_MARKER = ".tw_last_failure"
GUARDS_LOG = ".tw_guards.log"


def _fail(guard: str, msg: str) -> int:
    print(f"[guards] VIOLATION '{guard}': {msg}", file=sys.stderr)
    return VIOLATION


def _pass(guard: str, msg: str = "") -> int:
    print(f"[guards] ok '{guard}'" + (f": {msg}" if msg else ""))
    return OK


def _bypass_names() -> tuple[set[str], str | None]:
    """Parse TW_GUARDS_BYPASS. Returns (names, error_message_or_None).

    Strict (Hazard 8, fail-closed): only the closed set of guard names is
    accepted; unset -> inert; malformed (empty items, unknown names) -> error.
    """
    raw = os.environ.get(BYPASS_ENV, "")
    if raw == "":
        return set(), None
    names: set[str] = set()
    for item in raw.split(","):
        name = item.strip()
        if not name:
            return set(), (
                f"{BYPASS_ENV} has an empty/malformed item ({raw!r}); "
                "supply a comma-separated list of guard names, or unset it"
            )
        if name not in GUARDS:
            return set(), (
                f"{BYPASS_ENV} names unknown guard {name!r}; allowed: "
                f"{', '.join(sorted(GUARDS))}"
            )
        names.add(name)
    return names, None


def guard_ping(args) -> int:
    """Wiring smoke test: proves the module is reachable from bin/*."""
    return _pass("ping", "wiring smoke")


def guard_commit_trailer(args) -> int:
    """Trailer parser (AGENTS.md §2.5, §2.10 rule 5).

    Requires exactly ONE 'Role: <role>(<model>)' line in the message body and
    the 'Co-authored-by: goose <role>(<model>)' trailer; if --role is given, the
    declared role must match. Duplicate/ambiguous Role lines exit 2. This is
    accident-detection (see module docstring), not authorization.
    """
    if args.message and args.message_file:
        return _fail(
            "commit-trailer",
            "--message and --message-file are both set -- refusing to guess "
            "precedence (Hazard 11: a silent override is a documented flag "
            "that never takes effect); pass exactly one",  # M151.2
        )
    msg = args.message or ""
    if args.message_file:
        try:
            with open(args.message_file, encoding="utf-8") as fh:
                msg = fh.read()
        except OSError as exc:
            return _fail(
                "commit-trailer", f"cannot read --message-file: {exc}"
            )
    if not msg:
        return _fail("commit-trailer", "no commit message supplied")
    role_lines = [
        ln for ln in msg.splitlines()
        if ln.startswith("Role:") and ROLE_RE.match(ln)
    ]
    if not role_lines:
        return _fail(
            "commit-trailer",
            "missing 'Role: <role>(<model>)' line -- add it (§2.10 rule 5)",
        )
    if len(role_lines) > 1:
        return _fail(
            "commit-trailer",
            "ambiguous: multiple Role lines found ("
            + "; ".join(repr(ln) for ln in role_lines)
            + ") -- keep exactly one (§2.10 rule 5)",
        )
    roles = ROLE_RE.findall(msg)
    role, model = roles[0]
    coa = COAUTHOR_RE.findall(msg)
    if not coa:
        return _fail(
            "commit-trailer",
            "missing 'Co-authored-by: goose <role>(<model>)' trailer -- "
            "commit via bin/tw-commit (§2.5)",
        )
    if coa[0] != (role, model):
        return _fail(
            "commit-trailer",
            f"Role line '{role}({model})' disagrees with trailer "
            f"'{coa[0][0]}({coa[0][1]})' -- both must name the same role(model)",
        )
    if args.role:
        declared = args.role.strip()
        if f"{role}({model})" != declared:
            return _fail(
                "commit-trailer",
                f"Role line says '{role}({model})' but bin/tw-commit role is "
                f"'{declared}'",
            )
    return _pass("commit-trailer", f"role={role}({model})")


def _staged_channel_deletions(repo: str) -> list[tuple[str, str]]:
    out = []
    for ch in CHANNELS:
        proc = subprocess.run(
            ["git", "diff", "--cached", "--numstat", "--", ch],
            cwd=repo, capture_output=True, text=True,
        )
        for line in proc.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            added, deleted, path = parts[0], parts[1], parts[2]
            if deleted not in ("0", "-"):
                out.append((path, deleted))
    return out


def guard_append_only(args) -> int:
    """Channels are append-only (§2.8 rule 2); §2.13 compaction is exempt.

    TW_COMPACTION=1 is a CALLER ASSERTION, not a permission grant -- the guard
    does not verify the compaction was witnessed. When set, the exemption and
    the touched paths are recorded to .tw_guards.log with the caller-supplied
    reason (TW_COMPACTION_REASON; an empty reason exits 2, Hazard 8).
    """
    if os.environ.get("TW_COMPACTION") == "1":
        reason = os.environ.get("TW_COMPACTION_REASON", "").strip()
        if not reason:
            return _fail(
                "append-only",
                "TW_COMPACTION=1 set but TW_COMPACTION_REASON is empty -- "
                "a §2.13 exemption must record its reason (Hazard 8)",
            )
        touched = ",".join(
            p for p, _ in _staged_channel_deletions(args.repo)
        ) or "(no deletions)"
        stamp = _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        line = f"{stamp} | TW_COMPACTION=1 | {touched} | {reason}\n"
        with open(os.path.join(args.repo, GUARDS_LOG), "a", encoding="utf-8") as fh:
            fh.write(line)
        return _pass("append-only", "exempt (TW_COMPACTION=1, §2.13; logged)")
    bad = _staged_channel_deletions(args.repo)
    if bad:
        listing = ", ".join(f"{p} (-{d})" for p, d in bad)
        return _fail(
            "append-only",
            f"{listing}: channel lines deleted/rewritten -- channels are "
            "append-only (§2.8 rule 2); use TW_COMPACTION=1 with "
            "TW_COMPACTION_REASON for a witnessed §2.13 compaction",
        )
    return _pass("append-only", "no deletions in staged channels")


def guard_review_diff(args) -> int:
    """Enforce the diff-only boundary at the PACKAGING level.

    The only place the invariant is enforceable: the diff reviewer LLM's own file
    tools cannot be constrained at runtime (a packaging-time bound, not a runtime one).
    Validates that the input is a packet produced by bin/tw-review-diff
    (diff + criteria only) -- no content sniffing, only the packet header.
    """
    if not args.review_input:
        return _fail("review-diff", "--review-input <file> required")
    with open(args.review_input, encoding="utf-8") as fh:
        text = fh.read()
    if PACKET_MARKER not in text or PACKET_DIFF_HEADER not in text:
        return _fail(
            "review-diff",
            "input is not a packaged review (diff + criteria only) -- do not "
            "hand the diff reviewer a codebase dump; produce it with "
            "bin/tw-review-diff",
        )
    return _pass("review-diff", "diff + criteria only")


def guard_lf(args) -> int:
    """Gate pytest --lf on a recorded failure (AGENTS.md Part 1 step 4).

    INERT (exit 0) when the invocation does not request --lf. When --lf is
    requested, a recorded failure marker (.tw_last_failure, written by
    bin/tw-test on a failing run, cleared on a passing run) must be present.

    SCOPE (OPEN OWNER INPUT, compile-blocking per advisor Finding 78): this
    implementation uses the PRESENCE-ONLY reduced scope. Repo/node binding of
    the marker is the owner's ruling; the guard does not fork at runtime.
    """
    invocation = args.invocation or ""
    tokens = invocation.split()
    if "--lf" not in tokens and "--last-failed" not in tokens:
        return _pass("lf", "inert (no --lf in invocation)")
    repo = args.repo
    if not os.path.exists(os.path.join(repo, LF_MARKER)):
        return _fail(
            "lf",
            f"'--lf' requested but no recorded failure ({LF_MARKER} absent) "
            "-- establish a baseline failure first (Part 1 step 2), or set "
            f"{BYPASS_ENV}=lf to override",
        )
    return _pass("lf", "recorded failure present")


def guard_packet_hash(args) -> int:
    """Verify a frozen packet's recorded hashes; INERT when no manifest set.

    Manifest contract (pinned): path from TW_PACKET_MANIFEST (repo-relative;
    unset = inert); schema = JSON array of {path, hash}; path repo-relative;
    hash = sha256 hex digest over the STAGED/INDEX content (`git show
    :<path>`), not the working-tree file -- the commit records what is staged.
    Missing path / hash mismatch / malformed manifest exit 2 (Hazard 8).
    """
    manifest = os.environ.get("TW_PACKET_MANIFEST")
    if not manifest:
        return _pass("packet-hash", "inert (no TW_PACKET_MANIFEST)")
    path = manifest if os.path.isabs(manifest) else os.path.join(args.repo, manifest)
    try:
        with open(path, encoding="utf-8") as fh:
            entries = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return _fail("packet-hash", f"manifest not parseable: {exc}")
    if not isinstance(entries, list):
        return _fail("packet-hash", "manifest must be a JSON array of {path, hash}")
    bad = []
    for i, entry in enumerate(entries):
        if (not isinstance(entry, dict) or set(entry) != {"path", "hash"}
                or not isinstance(entry["path"], str)
                or not isinstance(entry["hash"], str)):
            return _fail(
                "packet-hash",
                f"entry {i} must be exactly {{path, hash}} with string values",
            )
        rel = entry["path"]
        want = entry["hash"]
        if not re.fullmatch(r"[0-9a-f]{64}", want):
            return _fail("packet-hash", f"entry {i} ({rel}) hash is not sha256 hex")
        proc = subprocess.run(
            ["git", "show", f":{rel}"], cwd=args.repo,
            capture_output=True,
        )
        if proc.returncode != 0:
            bad.append(f"{rel} (not in index)")
            continue
        got = hashlib.sha256(proc.stdout).hexdigest()
        if got != want:
            bad.append(f"{rel} (hash mismatch)")
    if bad:
        return _fail("packet-hash", "frozen-packet check failed: " + "; ".join(bad))
    return _pass("packet-hash", f"{len(entries)} entry(s) verified against the index")


# NOTE: a 'planner_no_execute' guard (proposed in the origin project, 2026-10-19)
# is DROPPED: asserting a substring of the planner's output proves nothing
# about execution and risks blocking legitimate output formats (Hazard 11;
# diff reviewer 20261019_3, critique 3).
GUARDS = {
    "ping": guard_ping,
    "commit-trailer": guard_commit_trailer,
    "append-only": guard_append_only,
    "review-diff": guard_review_diff,
    "lf": guard_lf,
    "packet-hash": guard_packet_hash,
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="agent-workflow runtime protocol guards")
    ap.add_argument("--guard", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--role", default="")
    ap.add_argument("--message", default=None)
    ap.add_argument("--message-file", default=None)
    ap.add_argument("--review-input", default=None)
    ap.add_argument("--invocation", default=None)
    args, _ = ap.parse_known_args(argv)

    if args.guard not in GUARDS:
        return _fail(
            args.guard,
            f"unknown guard name {args.guard!r}; allowed: "
            f"{', '.join(sorted(GUARDS))}",
        )

    names, err = _bypass_names()
    if err is not None:
        return _fail(args.guard, err)
    if args.guard in names:
        print(
            f"[guards] BYPASS: guard '{args.guard}' skipped via {BYPASS_ENV}",
            file=sys.stderr,
        )
        return OK

    return GUARDS[args.guard](args)


if __name__ == "__main__":
    sys.exit(main())
