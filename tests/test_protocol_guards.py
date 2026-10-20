"""Tests for tools/protocol_guards.py (M150, Phase 1).

Every guard is exercised with a RED case (violation -> exit 2) and a GREEN
case (documented legitimate workflow -> exit 0), per the M150 acceptance
criteria, and an INERT case where the plan pins one. Guards are invoked as
subprocesses, exactly as bin/* invokes them. Tests are HERMETIC: every case
that needs git builds a throwaway repo under pytest tmp_path -- no test
touches the real checkout, index, or channel files.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GUARD = REPO / "tools" / "protocol_guards.py"

CLEAR = ("TW_GUARDS_BYPASS", "TW_COMPACTION", "TW_COMPACTION_REASON",
         "TW_PACKET_MANIFEST")


def run_guard(*args, env=None, cwd=None):
    e = dict(os.environ)
    for k in CLEAR:
        e.pop(k, None)
    if env:
        e.update(env)
    return subprocess.run(
        [sys.executable, str(GUARD), *args],
        capture_output=True, text=True, env=e, cwd=str(cwd or REPO),
    )


def _mk_repo(tmp: Path) -> Path:
    tmp.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
    ident = ["-c", "user.email=a@b", "-c", "user.name=a"]
    (tmp / "docs").mkdir(exist_ok=True)
    ch = tmp / "docs" / "REVIEW_LOG.md"
    ch.write_text("line1\nline2\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
    subprocess.run(["git", *ident, "commit", "-q", "-m", "seed"], cwd=tmp, check=True)
    return ch


# --- ping / wiring ---------------------------------------------------------

def test_ping_passes():
    assert run_guard("--guard", "ping").returncode == 0


def test_unknown_guard_name_exits_2():
    assert run_guard("--guard", "typo-guard").returncode == 2


def test_guards_wired_into_bin_commit():
    commit = (REPO / "bin" / "tw-commit").read_text()
    assert "protocol_guards.py" in commit
    assert "--guard commit-trailer" in commit
    assert "--guard append-only" in commit
    assert "--guard packet-hash" in commit


def test_lf_guard_wired_into_bin_test():
    src = (REPO / "bin" / "tw-test").read_text()
    assert "--guard lf" in src
    assert "tw_last_failure" in src


def test_review_diff_helper_exists():
    assert (REPO / "bin" / "tw-review-diff").exists()


def test_review_diff_guard_is_wired_into_helper():
    src = (REPO / "bin" / "tw-review-diff").read_text()
    assert "--guard review-diff" in src


def test_planner_no_execute_is_dropped():
    src = GUARD.read_text()
    assert '"planner_no_execute": ' not in src  # documented, never wired
    assert "DROPPED" in src


# --- commit-trailer (trailer-keyed ownership, accident-detection) ----------

def test_commit_trailer_green_normal():
    msg = ("fix: thing\n\nRole: worker(deepseek-v4.1-flash)\n\n"
           "Co-authored-by: goose worker(deepseek-v4.1-flash)\n")
    p = run_guard("--guard", "commit-trailer", "--role",
                  "worker(deepseek-v4.1-flash)", "--message", msg)
    assert p.returncode == 0


def test_commit_trailer_red_missing_role_line():
    assert run_guard("--guard", "commit-trailer",
                     "--message", "fix: thing\n").returncode == 2


def test_commit_trailer_red_missing_trailer():
    msg = "fix: thing\n\nRole: worker(m)\n"
    assert run_guard("--guard", "commit-trailer", "--message", msg).returncode == 2


def test_commit_trailer_red_role_mismatch():
    msg = "fix\n\nRole: worker(m)\n\nCo-authored-by: goose worker(m)\n"
    p = run_guard("--guard", "commit-trailer", "--role", "planner(m)",
                  "--message", msg)
    assert p.returncode == 2


def test_commit_trailer_red_duplicate_role_lines():
    msg = ("fix\n\nRole: worker(m)\nRole: planner(m)\n\n"
           "Co-authored-by: goose worker(m)\n")
    p = run_guard("--guard", "commit-trailer", "--message", msg)
    assert p.returncode == 2
    assert "multiple Role" in p.stderr


def test_commit_trailer_red_trailer_disagrees_with_role_line():
    msg = ("fix\n\nRole: worker(m)\n\nCo-authored-by: goose planner(m)\n")
    assert run_guard("--guard", "commit-trailer", "--message", msg).returncode == 2


def test_commit_trailer_red_model_mismatch_vs_role_arg():
    msg = ("fix\n\nRole: worker(v2)\n\nCo-authored-by: goose worker(v2)\n")
    p = run_guard("--guard", "commit-trailer", "--role", "worker(v1)",
                  "--message", msg)
    assert p.returncode == 2


# --- bypass hatch (fail-closed) --------------------------------------------

def test_bypass_hatch_valid_is_logged():
    p = run_guard("--guard", "commit-trailer", "--message", "x\n",
                  env={"TW_GUARDS_BYPASS": "commit-trailer"})
    assert p.returncode == 0 and "BYPASS" in p.stderr


def test_bypass_hatch_unknown_name_rejected():
    p = run_guard("--guard", "ping", env={"TW_GUARDS_BYPASS": "nope"})
    assert p.returncode == 2


def test_bypass_hatch_malformed_rejected():
    p = run_guard("--guard", "ping", env={"TW_GUARDS_BYPASS": "ping,,lf"})
    assert p.returncode == 2


# --- append-only channels + §2.13 exemption --------------------------------

def test_append_only_green_pure_append(tmp_path):
    ch = _mk_repo(tmp_path)
    ch.write_text(ch.read_text() + "line3\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    assert run_guard("--guard", "append-only", "--repo", str(tmp_path)).returncode == 0


def test_append_only_red_deletion(tmp_path):
    ch = _mk_repo(tmp_path)
    ch.write_text("line1\n")  # deleted line2
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    assert run_guard("--guard", "append-only", "--repo", str(tmp_path)).returncode == 2


def test_append_only_ignores_non_channels(tmp_path):
    _mk_repo(tmp_path)
    f = tmp_path / "src.py"
    f.write_text("a\nb\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    f.write_text("a\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    assert run_guard("--guard", "append-only", "--repo", str(tmp_path)).returncode == 0


def test_append_only_newline_boundary_is_blocked(tmp_path):
    """Pinned verdict: removing only the EOF newline is a deletion -> exit 2."""
    ch = _mk_repo(tmp_path)
    ch.write_text("line1\nline2")  # drop trailing newline
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    assert run_guard("--guard", "append-only", "--repo", str(tmp_path)).returncode == 2


def test_append_only_compaction_exempt_and_logged(tmp_path):
    ch = _mk_repo(tmp_path)
    ch.write_text("compacted summary\n")  # rewrite == the §2.13 compaction
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    p = run_guard("--guard", "append-only", "--repo", str(tmp_path),
                  env={"TW_COMPACTION": "1",
                       "TW_COMPACTION_REASON": "compaction, reviewer-witnessed"})
    assert p.returncode == 0
    log = (tmp_path / ".tw_guards.log").read_text()
    assert "TW_COMPACTION=1" in log and "compaction, reviewer-witnessed" in log
    assert "docs/REVIEW_LOG.md" in log  # touched-paths field is recorded


def test_append_only_compaction_without_reason_rejected(tmp_path):
    ch = _mk_repo(tmp_path)
    ch.write_text("compacted\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    p = run_guard("--guard", "append-only", "--repo", str(tmp_path),
                  env={"TW_COMPACTION": "1"})
    assert p.returncode == 2


# --- review-diff packaging boundary ----------------------------------------

def test_review_diff_green_real_packet(tmp_path):
    pkt = tmp_path / "packet.md"
    pkt.write_text("# review-diff packaging (diff reviewer input)\n\n"
                   "## git diff HEAD~1\n- x\n")
    assert run_guard("--guard", "review-diff",
                     "--review-input", str(pkt)).returncode == 0


def test_review_diff_red_codebase_dump(tmp_path):
    dump = tmp_path / "dump.md"
    dump.write_text("src/pkg/module.py\n<< the whole codebase >>\n")
    assert run_guard("--guard", "review-diff",
                     "--review-input", str(dump)).returncode == 2


def test_review_diff_helper_refuses_extra_args():
    p = subprocess.run([str(REPO / "bin" / "tw-review-diff"), "HEAD~1",
                        "crit.md", "extra.md"],
                       capture_output=True, text=True, cwd=str(REPO))
    assert p.returncode == 2


def test_review_diff_output_passes_guard(tmp_path):
    p = subprocess.run([str(REPO / "bin" / "tw-review-diff"), "HEAD~1"],
                       capture_output=True, text=True, cwd=str(REPO))
    assert p.returncode == 0
    pkt = tmp_path / "pkt.md"
    pkt.write_text(p.stdout)
    assert run_guard("--guard", "review-diff",
                     "--review-input", str(pkt)).returncode == 0


# --- lf conditional guard ---------------------------------------------------

def test_lf_inert_without_flag(tmp_path):
    _mk_repo(tmp_path)
    p = run_guard("--guard", "lf", "--repo", str(tmp_path),
                  "--invocation", "tests/test_x.py -q")
    assert p.returncode == 0


def test_lf_red_without_recorded_failure(tmp_path):
    _mk_repo(tmp_path)
    p = run_guard("--guard", "lf", "--repo", str(tmp_path),
                  "--invocation", "--lf --tb=short")
    assert p.returncode == 2


def test_lf_green_with_recorded_failure(tmp_path):
    _mk_repo(tmp_path)
    (tmp_path / ".tw_last_failure").write_text("")
    p = run_guard("--guard", "lf", "--repo", str(tmp_path),
                  "--invocation", "--lf --tb=short")
    assert p.returncode == 0


# --- packet-hash frozen-packet guard ---------------------------------------

def test_packet_hash_inert_by_default():
    assert run_guard("--guard", "packet-hash").returncode == 0


def _repo_with_staged(tmp: Path, rel: str, content: bytes):
    _mk_repo(tmp)
    f = tmp / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(content)
    subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
    return f


def test_packet_hash_green(tmp_path):
    _repo_with_staged(tmp_path, "packet/a.txt", b"hello")
    man = tmp_path / "m.json"
    man.write_text(json.dumps(
        [{"path": "packet/a.txt", "hash": hashlib.sha256(b"hello").hexdigest()}]))
    p = run_guard("--guard", "packet-hash", "--repo", str(tmp_path),
                  env={"TW_PACKET_MANIFEST": str(man)})
    assert p.returncode == 0


def test_packet_hash_red_mismatch(tmp_path):
    _repo_with_staged(tmp_path, "packet/a.txt", b"hello")
    man = tmp_path / "m.json"
    man.write_text(json.dumps(
        [{"path": "packet/a.txt", "hash": "0" * 64}]))
    p = run_guard("--guard", "packet-hash", "--repo", str(tmp_path),
                  env={"TW_PACKET_MANIFEST": str(man)})
    assert p.returncode == 2


def test_packet_hash_red_missing_path(tmp_path):
    _mk_repo(tmp_path)
    man = tmp_path / "m.json"
    man.write_text(json.dumps(
        [{"path": "packet/absent.txt", "hash": "0" * 64}]))
    p = run_guard("--guard", "packet-hash", "--repo", str(tmp_path),
                  env={"TW_PACKET_MANIFEST": str(man)})
    assert p.returncode == 2


def test_packet_hash_red_malformed_manifest(tmp_path):
    _mk_repo(tmp_path)
    man = tmp_path / "m.json"
    man.write_text("{not json")
    p = run_guard("--guard", "packet-hash", "--repo", str(tmp_path),
                  env={"TW_PACKET_MANIFEST": str(man)})
    assert p.returncode == 2


# --- M151: the guard's own CLI contract ------------------------------------
# The wrapper (bin/tw-commit) invokes the guard as
#   --guard commit-trailer --role <role> --message-file <tmpfile>
# so the --message-file path is the one that actually runs in production.
# It was untested (diff reviewer 20261019_16 critique 3, diff reviewer 20261020_1).

_OK_MSG = "subject line\n\nbody\n\nRole: worker(deepseek-v4.1-flash)\n"
_OK_FILE = _OK_MSG + "\nCo-authored-by: goose worker(deepseek-v4.1-flash)\n"


def test_commit_trailer_green_via_message_file(tmp_path):
    """GREEN: exactly how bin/tw-commit calls us -- --message-file only."""
    mf = tmp_path / "msg.txt"
    mf.write_text(_OK_FILE)
    p = run_guard("--guard", "commit-trailer", "--role",
                  "worker(deepseek-v4.1-flash)", "--message-file", str(mf))
    assert p.returncode == 0, p.stderr + p.stdout


def test_commit_trailer_red_both_message_args(tmp_path):
    """RED: --message AND --message-file -- no silent precedence (M151.2)."""
    mf = tmp_path / "msg.txt"
    mf.write_text(_OK_FILE)
    p = run_guard("--guard", "commit-trailer", "--role",
                  "worker(deepseek-v4.1-flash)", "--message", _OK_MSG,
                  "--message-file", str(mf))
    assert p.returncode == 2
    assert "both set" in (p.stderr + p.stdout)


def test_commit_trailer_red_unreadable_message_file(tmp_path):
    """RED: a bad --message-file path is a named violation, not a traceback."""
    p = run_guard("--guard", "commit-trailer", "--role",
                  "worker(deepseek-v4.1-flash)", "--message-file",
                  str(tmp_path / "absent.txt"))
    assert p.returncode == 2
    assert "cannot read" in (p.stderr + p.stdout)


def test_commit_trailer_green_message_only():
    """GREEN: --message alone (the other half of the either/or)."""
    p = run_guard("--guard", "commit-trailer", "--role",
                  "worker(deepseek-v4.1-flash)", "--message", _OK_FILE)
    assert p.returncode == 0, p.stderr + p.stdout


def test_tw_commit_requires_role_arg_before_guards():
    """RED (M151.1): a roleless bin/tw-commit exits 2 BEFORE any guard runs,
    naming the missing role arg rather than the guard's generic trailer text.

    Hermetic: runs the real wrapper, which exits at the argument check and so
    never reaches git (nothing is staged or committed)."""
    wrapper = REPO / "bin" / "tw-commit"
    p = subprocess.run(
        [str(wrapper), "some message"], capture_output=True, text=True,
        cwd=str(REPO),
    )
    assert p.returncode == 2
    assert "role argument" in (p.stderr + p.stdout)
    assert "Co-authored-by: goose unspecified" not in (p.stderr + p.stdout)
    # the guard's generic text must NOT be what the user sees (Hazard 2:
    # the error must name the real cause)
    assert "missing 'Role:" not in (p.stderr + p.stdout)
