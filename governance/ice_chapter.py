#!/usr/bin/env python3
"""governance/ice_chapter.py — scaffold ICE chapters and track what is still unreviewed.

**This scaffolds; it does not author.** Capture is mechanical and safe to automate. Review
is a judgment call and is not — deciding what was asked, what was agreed, what was
superseded is the work, and a generator that fills these sections in has produced prose
about a conversation rather than a record of informed consent (protocol/ICE.md).

What it does own is the part that must not be done by hand: the **per-domain chapter-number
watermark**. Two projects reindexing at once against a shared sequence collide on the same
chapter number the moment both run. The sequence lives with the domain, in
ice-outputs/_watermark.json, and is allocated here.

Usage:
    python3 governance/ice_chapter.py status
    python3 governance/ice_chapter.py new --label founding-session
    python3 governance/ice_chapter.py new --label licensing --files a.md b.md
"""
from __future__ import annotations
import argparse
import datetime
import json
import os
import re

from pc_config import paths

P = paths()
WATERMARK = os.path.join(P["ice_outputs"], "_watermark.json")

TEMPLATE = """# ch{num:02d} — {label}

**Domain:** {domain}
**Chapter:** ch{num:02d}
**Authored:** {date}
**Reviewer:** <who or what performed this review>

## Scope

<ONE sentence stating exactly which window or file set this chapter covers. Required.
Without it, a later reader cannot tell whether something absent from this chapter was
absent from the sessions or merely out of scope.>

**Sources reviewed ({n_sources}):**
{source_list}

## Security status

<Required, even when the source material never mentions security. State "Checked, nothing
found" if that is the case — the absence of a statement is indistinguishable from the
absence of a check.>

## Expectations

<Each item is an Ask → Response → Lock-in chain. Quote both sides with line numbers.
Lock-in is one of: 🔒 locked (explicit approval on the record) · 🔓 unlocked (asked and
answered, no recorded approval) · ➡️ superseded (a later, separately-dated item changed
direction).

An earlier item is NEVER edited or deleted to make room for a later one. Where execution
diverged from the ask, that is a new dated item, not a retroactive edit.>

### E1 — <title>
- **Ask** (L<n>): "<quote>"
- **Response** (L<n>): "<quote>"
- **Lock-in:** 🔓

## Concerns

<The human's OWN stated worries, quoted, with line numbers. NOT the reviewer's assessment
of how the model behaved — that is real and worth keeping, but it goes to CONCERNS.md
instead. A chapter that has drifted into grading the model has stopped being evidence.>

### C1 — <title>
- **Stated** (L<n>): "<quote>"

## Ideas

<Concepts, changes, problems, and directions the human introduced. Quoted, with line
numbers.>

### I1 — <title>
- **Stated** (L<n>): "<quote>"

## Open, unresolved

<Anything this review surfaced that is the human's own call to make, not something this
process resolves. Say so explicitly rather than leaving it implied.>
"""


def _load_watermark() -> dict:
    if os.path.exists(WATERMARK):
        return json.load(open(WATERMARK, encoding="utf-8"))
    return {"domain": P["config"]["ice_domain"], "next_chapter": 1, "chapters": []}


def _save_watermark(wm) -> None:
    os.makedirs(P["ice_outputs"], exist_ok=True)
    with open(WATERMARK, "w", encoding="utf-8") as f:
        json.dump(wm, f, indent=2)


def _captured_sources() -> list:
    if not os.path.isdir(P["sources"]):
        return []
    return sorted(f for f in os.listdir(P["sources"])
                  if f.endswith(".md") and not f.startswith("_"))


def _reviewed_sources(wm) -> set:
    return {s for ch in wm["chapters"] for s in ch.get("sources", [])}


def cmd_status() -> int:
    wm = _load_watermark()
    captured = _captured_sources()
    reviewed = _reviewed_sources(wm)
    pending = [s for s in captured if s not in reviewed]

    print(f"Domain:          {wm['domain']}")
    print(f"Chapters:        {len(wm['chapters'])} (next: ch{wm['next_chapter']:02d})")
    print(f"Captured sources: {len(captured)}")
    print(f"Reviewed:        {len(captured) - len(pending)}")
    print(f"Awaiting review: {len(pending)}")
    for s in pending:
        print(f"  - {s}")
    if not captured:
        print("\nNothing captured yet — run discover_sessions.py or import_chat_logs.py first.")
    elif pending:
        print(f"\nScaffold a chapter for these:  python3 governance/ice_chapter.py new "
              f"--label <name>")
    return 0


def cmd_new(label, files) -> int:
    wm = _load_watermark()
    captured = _captured_sources()
    reviewed = _reviewed_sources(wm)

    sources = files or [s for s in captured if s not in reviewed]
    if not sources:
        print("No sources to review. Nothing captured, or everything is already in a chapter.")
        return 1

    missing = [s for s in sources if s not in captured]
    if missing:
        print(f"Not found in sources/: {', '.join(missing)}")
        return 1

    num = wm["next_chapter"]
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    fname = f"ch{num:02d}_{date}_{slug}_ICE.md"
    path = os.path.join(P["ice_outputs"], fname)

    if os.path.exists(path):
        print(f"Refusing to overwrite existing chapter: {path}")
        return 1

    os.makedirs(P["ice_outputs"], exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(
            num=num, label=label, domain=wm["domain"], date=date,
            n_sources=len(sources),
            source_list="\n".join(f"- `sources/{s}`" for s in sources)))

    wm["chapters"].append({"chapter": num, "file": fname, "label": label,
                           "authored": date, "sources": sources, "status": "scaffolded"})
    wm["next_chapter"] = num + 1
    _save_watermark(wm)

    print(f"Scaffolded {path}")
    print(f"Covering {len(sources)} source(s):")
    for s in sources:
        print(f"  - {s}")
    print("\nThe scaffold is empty by design. Read the sources and fill in Scope, Security "
          "status, Expectations, Concerns and Ideas — quoting both sides with line numbers.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    new = sub.add_parser("new")
    new.add_argument("--label", required=True, help="short kebab-case name for this chapter")
    new.add_argument("--files", nargs="*", default=None,
                     help="specific sources/*.md filenames; defaults to everything unreviewed")
    args = ap.parse_args()
    return cmd_status() if args.cmd == "status" else cmd_new(args.label, args.files)


if __name__ == "__main__":
    raise SystemExit(main())
