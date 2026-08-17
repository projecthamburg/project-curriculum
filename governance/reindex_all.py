#!/usr/bin/env python3
"""governance/reindex_all.py — run this instance's update cycle, then every project's own.

Each project under projects/<NN-slug>/governance/ owns an independent copy of this folder
with its own config.json, its own index, and its own ICE domain. **There is no shared
runtime dependency between them** — this script only invokes each one in turn, so a project
added tomorrow is picked up by the glob with zero edits here.

That independence is the property that makes a fork work with none of the original
infrastructure. Do not centralize the per-project layers to save duplication; the
duplication is the point.

Usage:
    python3 governance/reindex_all.py
    python3 governance/reindex_all.py --real
"""
from __future__ import annotations
import argparse
import glob
import os
import subprocess
import sys

from pc_config import paths

P = paths()


def run_update(gov_dir: str, real: bool) -> int:
    script = os.path.join(gov_dir, "update.py")
    if not os.path.exists(script):
        print(f"  no update.py in {gov_dir} — skipped")
        return 0
    cmd = [sys.executable, script] + (["--real"] if real else [])
    proc = subprocess.run(cmd, cwd=gov_dir)
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--real", action="store_true")
    args = ap.parse_args()

    failures = 0

    print(f"=== {P['config']['project_id']} (this instance) ===")
    failures += bool(run_update(P["gov"], args.real))

    pattern = os.path.join(P["content_root"], "projects", "*", "governance")
    project_govs = sorted(d for d in glob.glob(pattern) if os.path.isdir(d))

    if not project_govs:
        print("\nNo per-project governance layers yet "
              "(create one with governance/new_project.py).")
    for gov in project_govs:
        name = os.path.basename(os.path.dirname(gov))
        print(f"\n=== {name} ===")
        failures += bool(run_update(gov, args.real))

    print(f"\nDone. {len(project_govs) + 1} layer(s) processed, {failures} reported failure.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
