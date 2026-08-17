#!/usr/bin/env python3
"""governance/spheres.py — propose and inspect spheres over the evidence index.

A **sphere** is a named area of a project's evidence. Chapters are authored per sphere, so a
chapter's Scope declaration names a real subject instead of an arbitrary time window. A chapter
over "everything unreviewed" works for one session and becomes meaningless at fifty.

**A sphere is a query-time view, not a partition.** There is one index. A sphere is a named
filter over it, so nothing is copied, nothing is rebuilt when a sphere changes, and a source may
belong to several spheres at once — a decision spanning licensing and governance should appear
in both.

**Proposed here, confirmed by a human.** Machine-drawn boundaries are a starting hypothesis;
naming an area is a judgment about what the project is. `propose` writes nothing to
spheres.yaml — it prints candidates for a person to accept, rename, merge or reject.

Method:
  1. For every keyword, the set of chunks carrying it.
  2. Drop terms too rare to be an area, and terms so common they describe the whole project
     rather than an area of it.
  3. Score pairs of terms by Jaccard overlap of their chunk sets — terms that appear together
     and rarely apart are one area.
  4. Agglomerate greedily above a threshold.
  5. Report each candidate with its evidence: defining terms, chunk count, how many distinct
     sources it spans, and its date range. **A sphere drawn from a single source is usually a
     topic, not an area** — flagged rather than silently returned.

Usage:
    python3 governance/spheres.py propose
    python3 governance/spheres.py propose --min-chunks 4 --threshold 0.35
    python3 governance/spheres.py list
    python3 governance/spheres.py show licensing
"""
from __future__ import annotations
import argparse
import json
import os
import re
from collections import defaultdict

from pc_config import paths

P = paths()
SPHERES_PATH = os.path.join(P["gov"], "spheres.yaml")


def load_index() -> dict:
    if not os.path.exists(P["index"]):
        raise SystemExit(f"No index at {P['index']} — run build_search_index.py first.")
    return json.load(open(P["index"], encoding="utf-8"))


def load_spheres() -> dict:
    """Deliberately dependency-free parser for the flat shape spheres.yaml uses."""
    if not os.path.exists(SPHERES_PATH):
        return {}
    spheres, cur = {}, None
    for raw in open(SPHERES_PATH, encoding="utf-8"):
        s = raw.rstrip()
        if not s.strip() or s.strip().startswith("#") or s.strip() == "spheres:":
            continue
        m = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*$", s)
        if m:
            cur = m.group(1)
            spheres[cur] = {"terms": [], "categories": [], "tiers": [], "description": ""}
            continue
        if cur is None:
            continue
        m = re.match(r"^\s{4}(terms|categories|tiers|description):\s*(.*)$", s)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if key == "description":
                spheres[cur]["description"] = val.strip('"')
            elif val.startswith("["):
                spheres[cur][key] = [t.strip().strip('"')
                                     for t in val.strip("[]").split(",") if t.strip()]
    return spheres


# Function words and structural tokens survive the index's own stopword list because that
# list is tuned for retrieval, where a rare co-occurrence still helps. Sphere derivation has
# the opposite need: a term carried by most chunks describes the corpus, not an area of it,
# and proposing it produces a "sphere" that is just the project.
STRUCTURAL = {
    "to", "at", "in", "is", "of", "on", "it", "as", "by", "or", "if", "we", "you", "an",
    "be", "do", "so", "no", "up", "out", "not", "can", "all", "any", "how", "why", "who",
    "one", "two", "new", "get", "set", "may", "per", "its", "was", "are", "has", "had",
    "const", "let", "var", "function", "return", "import", "export", "true", "false",
    "null", "none", "self", "this", "that", "from", "with", "into", "html", "div", "span",
}


def _keyword_sets(index, min_chunks, max_ratio):
    total = len(index["chunks"])
    kw = defaultdict(set)
    for c in index["chunks"]:
        for k in c["keywords"]:
            if len(k) < 3 or k in STRUCTURAL or k.isdigit():
                continue
            kw[k].add(c["id"])
    ceiling = max(min_chunks, int(total * max_ratio))
    return {k: v for k, v in kw.items() if min_chunks <= len(v) <= ceiling}, total


def _jaccard(a, b):
    inter = len(a & b)
    return inter / len(a | b) if inter else 0.0


def propose(min_chunks, threshold, limit):
    index = load_index()
    kw, total = _keyword_sets(index, min_chunks, 0.25)
    if not kw:
        print(f"No terms qualified (index has {total} chunks). Lower --min-chunks, or the "
              f"corpus is too small for spheres — which is a normal early state, not an error.")
        return 0

    terms = sorted(kw, key=lambda k: -len(kw[k]))[:400]
    parent = {t: t for t in terms}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, a in enumerate(terms):
        for b in terms[i + 1:]:
            if _jaccard(kw[a], kw[b]) >= threshold:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[rb] = ra

    groups = defaultdict(list)
    for t in terms:
        groups[find(t)].append(t)

    by_id = {c["id"]: c for c in index["chunks"]}
    meta = {s["path"]: s for s in index["sources"]}

    candidates = []
    for root, members in groups.items():
        if len(members) < 2:
            continue
        chunks = set().union(*(kw[m] for m in members))
        paths_ = {by_id[c]["path"] for c in chunks}
        cats = {by_id[c]["category"] for c in chunks}
        members.sort(key=lambda m: -len(kw[m]))
        candidates.append({"terms": members[:8], "chunks": len(chunks),
                           "sources": len(paths_), "categories": sorted(cats),
                           "paths": sorted(paths_)[:3]})
    candidates.sort(key=lambda c: (-c["sources"], -c["chunks"]))

    if not candidates:
        print(f"No multi-term candidates at threshold {threshold} over {total} chunks. "
              f"Try --threshold 0.25, or accept that this corpus has no distinct areas yet.")
        return 0

    print(f"Candidate spheres over {total} chunks "
          f"(min-chunks={min_chunks}, threshold={threshold})\n")
    for i, c in enumerate(candidates[:limit], 1):
        single = c["sources"] == 1
        print(f"{i}. terms:      {', '.join(c['terms'])}")
        print(f"   chunks:     {c['chunks']}   sources: {c['sources']}   "
              f"categories: {', '.join(c['categories'])}")
        print(f"   seen in:    {', '.join(c['paths'])}")
        if single:
            print("   ⚠ single source — this is probably a topic within one document, "
                  "not an area of the project")
        print()

    print("Nothing was written. To adopt one, add it to governance/spheres.yaml:\n")
    print("spheres:")
    print("  <your-name-for-it>:")
    print(f"    terms: [{', '.join(candidates[0]['terms'][:4])}]")
    print('    description: "what this area is, in your words"')
    print("\nThen scope a chapter to it:  ice_chapter.py new --label <name> --sphere <name>")
    return 0


def cmd_list():
    spheres = load_spheres()
    if not spheres:
        print(f"No spheres defined at {SPHERES_PATH}.")
        print("Run 'spheres.py propose' for candidates, then write the ones you accept.")
        return 0
    for name, spec in spheres.items():
        print(f"  {name}")
        if spec["description"]:
            print(f"    {spec['description']}")
        for key in ("terms", "categories", "tiers"):
            if spec[key]:
                print(f"    {key}: {', '.join(spec[key])}")
    return 0


def cmd_show(name):
    spheres = load_spheres()
    if name not in spheres:
        print(f"Unknown sphere '{name}'. Defined: {', '.join(spheres) or '(none)'}")
        return 1
    spec, index = spheres[name], load_index()
    terms = set(spec["terms"])
    hits = [c for c in index["chunks"]
            if (not terms or terms & set(c["keywords"]))
            and (not spec["categories"] or c["category"] in spec["categories"])]
    print(f"Sphere '{name}': {len(hits)} chunks across "
          f"{len({h['path'] for h in hits})} sources")
    for h in hits[:10]:
        sp = f" [{h['speaker']}]" if h.get("speaker") else ""
        print(f"  {h['origin']}/{h['category']}{sp}  {h['path']}:L{h['line_start']}")
    if len(hits) > 10:
        print(f"  … {len(hits) - 10} more")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("propose")
    pr.add_argument("--min-chunks", type=int, default=3)
    pr.add_argument("--threshold", type=float, default=0.30)
    pr.add_argument("--limit", type=int, default=12)
    sub.add_parser("list")
    sh = sub.add_parser("show")
    sh.add_argument("name")
    a = ap.parse_args()
    if a.cmd == "propose":
        return propose(a.min_chunks, a.threshold, a.limit)
    return cmd_list() if a.cmd == "list" else cmd_show(a.name)


if __name__ == "__main__":
    raise SystemExit(main())
