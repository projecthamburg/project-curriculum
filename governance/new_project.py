#!/usr/bin/env python3
"""governance/new_project.py — intake for a new project in this workspace.

Implements the intake checklist in PROJECTS.md. The five things an agent should ask for
rather than guess:

  1. The project's real location — a path. Nested here, or a fully external directory
     (possibly its own git repository).
  2. **The objective the curriculum must serve.** REQUIRED — this script refuses without
     it. A curriculum cannot be seeded without a stated objective; there is nothing to
     seed it *for*.
  3. Any existing conversation or session material to review.
  4. Whether the project already has real output worth surveying, or is from scratch.
  5. The project number — assigned in the registry, never guessed from a folder name.

(1), (3), (4) and (5) may reasonably default. This script **states every default back**
rather than silently assuming it, so it can be corrected before real files are created.

What it creates:

    projects/<NN>-<slug>/
      AGENTS.md                    project context, nests under the root AGENTS.md
      governance/                  an independent copy — own config, own index, own ICE
                                   domain, no shared runtime dependency
      syllabus/                    the two dependency graphs and the staleness ledger

**Governance always lives here, never inside an external project's own repository** — even
when that project's real content lives entirely elsewhere on disk. The external repository
is read, never written to.

Usage:
    python3 governance/new_project.py --parent ../my-app --objective "..."
    python3 governance/new_project.py --parent /abs/path/to/repo --objective "..." --dry-run
"""
from __future__ import annotations
import argparse
import datetime
import json
import os
import re
import shutil

from pc_config import paths

P = paths()
REGISTRY = os.path.join(P["gov"], "registry.json")

# Copied into every project's own governance folder. reindex_all.py and new_project.py are
# workspace-level and deliberately not copied.
PORTABLE_SCRIPTS = [
    "pc_config.py", "redact_util.py", "build_search_index.py", "index_codebase.py",
    "query.py", "spheres.py", "discover_sessions.py", "import_chat_logs.py",
    "ice_chapter.py", "intake.py", "security_scan.py", "update.py",
]

AGENTS_MD = """# {number:02d}-{slug} — project context for agents

**Parent project:** `{parent}`
**Kind:** {kind}
**Registered:** {date} as project {number:02d} in `governance/registry.json`

This file nests under the workspace root `AGENTS.md` — Codex, Jules and Kimi load both,
walking from the git root to the working directory. Everything in the root file still
applies here.

## Objective

{objective}

## What this folder is

The **governance and curriculum** for the parent project named above. {content_note}

- `governance/` — this project's own independent layer: its own search index, its own ICE
  domain, its own concerns log, its own security scan. No shared runtime dependency on the
  workspace or on any other project.
- `syllabus/` — the curriculum generated for the objective above: courses, the two
  dependency graphs, and the staleness ledger.

## Before searching files by hand

```
python3 governance/query.py "your question"
python3 governance/query.py "your question" --origin internal
python3 governance/query.py "what did I ask about X" --speaker user
```

Keyword index, not a vector database — no embeddings, no live search. Every result is
tagged `origin: internal` (this project's own material) or `origin: external` (borrowed
reference material). Check which before treating a result as this project's own work.

## The cycle

```
python3 governance/update.py --real       # capture sessions, rebuild the index
python3 governance/ice_chapter.py status   # what is awaiting review
python3 governance/ice_chapter.py new --label <name>
```

Capture is automated. **Review is not** — read the sources and author the chapter.
"""

CONCERNS_MD = """# CONCERNS — {slug}

This project's own concerns log. Not optional, and not something added later once
something goes wrong: it exists from the start, even while empty.

**What belongs here:** a reviewer's own assessment of risk, conduct, or exposure —
including assessments of how an agent behaved.

**What does not:** the human's own stated worries about the project. Those are ICE
Concerns and belong in an `ice-outputs/` chapter, quoted with line numbers. See
`protocol/ICE.md`. Getting this routing wrong in the other direction is the documented
drift failure — a chapter that has slid into grading the model has stopped being evidence.

Security findings land here as they are found.

## Open

_None yet._

## Closed

_None yet._
"""

PROVENANCE_MD = """# PROVENANCE — {slug}

Maps every file in `sources/` to what it actually is, and where the true original lives.

**Raw is immutable; renderings are derived.** A native `.jsonl`, an exported `.json`, or an
as-supplied `.md` is evidence and is never edited. Anything this layer produced from it is
a derived artifact and is regenerable.

The index reads `sources/*.md` only, so a raw `.json` sitting alongside is a real, present
source without being pulled into the index. Each capture's `.meta.json` sidecar records its
category, provider, association confidence, and timestamp confidence.

| File in `sources/` | Indexed? | Kind | True original |
|---|---|---|---|
| _(none captured yet)_ | | | |
"""

MANIFEST_YAML = """# {number:02d}-{slug} — file manifest
#
# Lightweight pointers only. Files are read from their real location and never copied here,
# so the manifest and the original can never disagree.
#
#   path      relative to this project's content root (or to external_root when set)
#   enabled   true to include in the search index
#   category  free-form; used by query.py --category
#   origin    internal = this project's own material
#             external = borrowed or third-party reference material
#
# Always label origin honestly. A borrowed document indexed as internal will eventually be
# cited as this project's own work.

files:
  - path: AGENTS.md
    enabled: true
    category: project-context
    origin: internal
"""

LIFECYCLE_YAML = """# course_lifecycle.yaml — the staleness ledger
#
# Routing SCHEDULES review. It is explicitly barred from modifying content.
# See protocol/MASTER_SYLLABUS.md.

policy:
  review_interval_days: 90
  rule: "A matching discussion schedules a review; it never silently edits content."

courses: {}

review_routes: []
"""


def load_registry() -> dict:
    if os.path.exists(REGISTRY):
        return json.load(open(REGISTRY, encoding="utf-8"))
    return {"projects": []}


def save_registry(reg) -> None:
    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parent", required=True,
                    help="path to the project this curriculum is for (nested or external)")
    ap.add_argument("--objective", required=True,
                    help="REQUIRED. What this project's curriculum must serve.")
    ap.add_argument("--slug", default=None, help="defaults to the parent folder's name")
    ap.add_argument("--number", type=int, default=None,
                    help="defaults to the next number in the registry")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.objective.strip():
        print("Refusing to proceed: an objective is required. A curriculum cannot be "
              "seeded without one — there is nothing to seed it for.")
        return 1

    parent = os.path.abspath(os.path.expanduser(args.parent))
    if not os.path.isdir(parent):
        print(f"Parent project path does not exist: {parent}")
        return 1

    reg = load_registry()
    number = args.number or (max((p["number"] for p in reg["projects"]), default=0) + 1)
    slug = args.slug or re.sub(r"[^a-z0-9]+", "-", os.path.basename(parent).lower()).strip("-")
    folder = f"{number:02d}-{slug}"
    dest = os.path.join(P["content_root"], "projects", folder)

    if any(p["number"] == number for p in reg["projects"]):
        print(f"Project number {number:02d} is already registered.")
        return 1
    if os.path.exists(dest):
        print(f"Refusing to overwrite existing folder: {dest}")
        return 1

    nested = parent.startswith(os.path.join(P["content_root"], "projects"))
    kind = "nested" if nested else "external"
    external_root = None if nested else parent
    content_note = (
        "The parent project's content is nested inside this workspace."
        if nested else
        f"The parent project's real content lives at `{parent}` — a separate directory that "
        f"this layer reads and **never writes to**. Governance lives here, not there.")

    # Every default gets stated back, so it can be corrected before files exist.
    print("Intake summary — correct anything wrong before this runs for real:\n")
    print(f"  1. Parent project : {parent}")
    print(f"     Kind           : {kind}  (derived from the path)")
    print(f"  2. Objective      : {args.objective.strip()}")
    print(f"  3. Prior material : none imported yet — use governance/import_chat_logs.py "
          f"or discover_sessions.py after creation")
    print(f"  4. Existing output: not surveyed — a read-only survey pass is the next step "
          f"if the parent already has real content")
    print(f"  5. Number / slug  : {number:02d} / {slug}"
          f"{'  (both defaulted)' if not args.number and not args.slug else ''}")
    print(f"\n  Creates          : projects/{folder}/")

    if args.dry_run:
        print("\nDry-run — nothing written. Re-run without --dry-run to create.")
        return 0

    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    gov = os.path.join(dest, "governance")
    for sub in ("sources", "ice-outputs", "reports", os.path.join("security", "findings")):
        os.makedirs(os.path.join(gov, sub), exist_ok=True)
    os.makedirs(os.path.join(dest, "syllabus"), exist_ok=True)

    for script in PORTABLE_SCRIPTS:
        shutil.copy2(os.path.join(P["gov"], script), os.path.join(gov, script))

    with open(os.path.join(gov, "config.json"), "w", encoding="utf-8") as f:
        json.dump({"project_id": folder, "ice_domain": slug, "content_root": "..",
                   "external_root": external_root,
                   "manifest": f"sources/{number:02d}-project-files-manifest.yaml"},
                  f, indent=2)

    fmt = {"number": number, "slug": slug, "parent": parent, "kind": kind,
           "date": date, "objective": args.objective.strip(), "content_note": content_note}
    writes = {
        os.path.join(dest, "AGENTS.md"): AGENTS_MD.format(**fmt),
        os.path.join(gov, "CONCERNS.md"): CONCERNS_MD.format(**fmt),
        os.path.join(gov, "PROVENANCE.md"): PROVENANCE_MD.format(**fmt),
        os.path.join(gov, "sources", f"{number:02d}-project-files-manifest.yaml"):
            MANIFEST_YAML.format(**fmt),
        os.path.join(dest, "syllabus", "course_lifecycle.yaml"): LIFECYCLE_YAML,
        os.path.join(dest, "syllabus", "curriculum_prerequisites.json"):
            json.dumps({"courses": []}, indent=2) + "\n",
        os.path.join(dest, "syllabus", "curriculum_traceability.json"):
            json.dumps({"artifacts": []}, indent=2) + "\n",
    }
    for path, content in writes.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    reg["projects"].append({"number": number, "slug": slug, "folder": folder,
                            "parent": parent, "kind": kind, "objective": args.objective.strip(),
                            "ice_domain": slug, "registered": date})
    save_registry(reg)

    print(f"\nCreated projects/{folder}/")
    print("\nNext:")
    print(f"  1. Add real files to governance/sources/{number:02d}-project-files-manifest.yaml")
    print(f"  2. python3 projects/{folder}/governance/discover_sessions.py")
    print(f"  3. python3 projects/{folder}/governance/import_chat_logs.py <export-dir>")
    print(f"  4. python3 projects/{folder}/governance/update.py --real")
    print(f"  5. python3 projects/{folder}/governance/ice_chapter.py new --label <name>")
    print("\nThen seed the curriculum from the reviewed chapters — protocol/"
          "GENERATION_MACHINERY.md Part A.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
