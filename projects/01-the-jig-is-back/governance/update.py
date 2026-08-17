#!/usr/bin/env python3
"""governance/update.py — this instance's own update cycle. No external dependency.

Runs the mechanical half of the loop and stops there:

    1. discover work sessions on this machine (identity-matched, never text-grep)
    2. rebuild the local search index
    3. report what is now awaiting ICE review
    4. write a dated report

**Step 4 does not author anything.** Capture is mechanical and safe to automate; review is
a judgment call and is not (protocol/ICE.md). This script tells you what is waiting; a
human or an agent then reads the sources and writes the chapter with ice_chapter.py.

Unlike its predecessor there is no coordinating repository, no inbox/outbox channel, and no
network call. Everything this instance needs is in this folder, which is what makes a fork
work with none of the original infrastructure.

Usage:
    python3 governance/update.py            # dry-run: report what would happen
    python3 governance/update.py --real      # capture + reindex for real
"""
from __future__ import annotations
import argparse
import datetime
import os
import subprocess
import sys

from pc_config import paths

P = paths()


def run(script: str, extra=None) -> tuple:
    cmd = [sys.executable, os.path.join(P["gov"], script)] + (extra or [])
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=P["gov"])
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--real", action="store_true",
                    help="capture new sessions and rebuild the index for real")
    ap.add_argument("--skip-discovery", action="store_true",
                    help="reindex only; do not scan for new sessions")
    args = ap.parse_args()

    now = datetime.datetime.now(datetime.timezone.utc)
    sections = [f"# Update report — {now.strftime('%Y-%m-%d %H:%M:%SZ')}", "",
                f"**Instance:** {P['config']['project_id']}",
                f"**Mode:** {'real' if args.real else 'dry-run'}", ""]
    failed = False

    if not args.skip_discovery:
        print("== 1. session discovery ==")
        rc, out = run("discover_sessions.py", ["--real"] if args.real else [])
        print(out.rstrip())
        failed |= rc != 0
        sections += ["## 1. Session discovery", "", "```", out.strip(), "```", ""]
    else:
        sections += ["## 1. Session discovery", "", "Skipped (--skip-discovery).", ""]

    print("\n== 2. search index ==")
    if args.real:
        rc, out = run("build_search_index.py")
        print(out.rstrip())
        failed |= rc != 0
    else:
        out = "Dry-run — index not rebuilt."
        print(f"  {out}")
    sections += ["## 2. Search index", "", "```", out.strip(), "```", ""]

    print("\n== 3. awaiting ICE review ==")
    rc, out = run("ice_chapter.py", ["status"])
    print(out.rstrip())
    failed |= rc != 0
    sections += ["## 3. Awaiting ICE review", "", "```", out.strip(), "```", "",
                 "Review is deliberately not automated. Read the sources and author the "
                 "chapter with `ice_chapter.py new --label <name>`.", ""]

    os.makedirs(P["reports"], exist_ok=True)
    report = os.path.join(P["reports"], f"{now.strftime('%Y-%m-%dT%H-%M-%SZ')}_update.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write("\n".join(sections))
    print(f"\nReport: {report}")

    if not args.real:
        print("Dry-run only — pass --real to capture and reindex.")
    if failed:
        print("One or more steps reported a failure — see the report.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
