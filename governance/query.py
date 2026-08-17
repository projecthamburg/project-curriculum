#!/usr/bin/env python3
"""governance/query.py — search this instance's local index.

Reads governance/search_index.json (built by build_search_index.py) and scores chunks by
keyword and path overlap. No network, no embeddings, no live search — it finds what has
already been written down and indexed, nothing else.

Use it before searching files by hand. Every result carries an `origin` tag:
`internal` = this instance's own authored material, `external` = borrowed or third-party
reference material. **Check which before treating a result as this instance's own work.**

Usage:
    python3 governance/query.py "some question"
    python3 governance/query.py "some question" --origin internal
    python3 governance/query.py "some question" --category protocol --limit 3
    python3 governance/query.py "what did I ask about licensing" --speaker user
    python3 governance/query.py "some question" --json
"""
from __future__ import annotations
import argparse
import json
import os
import re

from pc_config import paths

P = paths()

STOPWORDS = {
    "the", "and", "for", "that", "with", "this", "from", "have", "were", "what",
    "when", "where", "your", "into", "will", "would", "about", "there", "their",
    "them", "they", "then", "than", "because", "which", "while", "also", "been",
    "being", "just", "like", "some", "only", "more", "most", "using", "used",
    "need", "needs", "onto", "over", "under", "after", "before", "does", "doing",
    "done", "each", "other", "others", "unto", "both", "same", "very", "make",
    "made", "much", "many", "ours", "ourselves", "these", "those", "such", "still", "here",
}


def normalize_token(token: str) -> str:
    token = token.strip().lower().strip("`'\"[]{}()<>,;!?")
    return token.replace("’", "'").strip(".")


def expand_token_parts(token: str) -> list:
    parts = [normalize_token(token)]
    for piece in re.split(r"[/:._#-]+", token):
        piece = normalize_token(piece)
        if piece:
            parts.append(piece)
    deduped, seen = [], set()
    for piece in parts:
        if not piece or (len(piece) == 1 and not piece.isdigit()):
            continue
        if piece.isdigit() and len(piece) < 4:
            continue
        if piece.isalpha() and piece in STOPWORDS:
            continue
        if piece not in seen:
            seen.add(piece)
            deduped.append(piece)
    return deduped


def normalize_query(query: str) -> list:
    terms = []
    for raw in query.split():
        terms.extend(expand_token_parts(raw))
    return sorted(set(terms))


def fetch_excerpt(chunk: dict, roots: dict) -> str:
    root = roots.get(chunk["path"])
    if not root:
        return "(source root unknown — rebuild the index)"
    path = os.path.join(root, chunk["path"])
    if not os.path.exists(path):
        return "(source file no longer at this path — rebuild the index)"
    lines = open(path, encoding="utf-8", errors="ignore").read().splitlines()
    return "\n".join(lines[max(0, chunk["line_start"] - 1):min(len(lines), chunk["line_end"])])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--origin", choices=["internal", "external"])
    ap.add_argument("--category")
    ap.add_argument("--speaker", choices=["user", "assistant", "system", "tool"],
                    help="Session chunks only — e.g. --speaker user to find what was asked, "
                         "not what was answered.")
    ap.add_argument("--list-categories", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(P["index"]):
        print(f"No search index at {P['index']} — run "
              f"'python3 governance/build_search_index.py' first.")
        return 1

    index = json.load(open(P["index"], encoding="utf-8"))
    indices = index["indices"]

    if args.list_categories:
        for cat, ids in sorted(indices["category_index"].items()):
            print(f"  {cat:32s} {len(ids)} chunks")
        return 0

    if not args.query:
        ap.error("a query is required unless --list-categories is given")

    chunks_by_id = {c["id"]: c for c in index["chunks"]}
    roots = {s["path"]: s.get("root", P["content_root"]) for s in index["sources"]}
    terms = normalize_query(args.query)
    lowered = args.query.lower()

    scores: dict = {}

    def add(cid, pts):
        scores[cid] = scores.get(cid, 0.0) + pts

    for term in terms:
        for cid in indices["keyword_index"].get(term, []):
            add(cid, 3.0)

    for cid, chunk in chunks_by_id.items():
        path_l = chunk["path"].lower()
        if lowered in chunk["preview"].lower():
            add(cid, 2.5)
        if lowered in path_l:
            add(cid, 4.5)
        overlap = [t for t in terms if t in set(normalize_query(path_l))]
        if overlap:
            add(cid, min(len(overlap) * 1.2, 6.0))

    if not scores:
        print("No matching chunks found.")
        return 0

    results = []
    for cid, score in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0])):
        chunk = chunks_by_id[cid]
        if args.origin and chunk["origin"] != args.origin:
            continue
        if args.category and chunk["category"] != args.category:
            continue
        if args.speaker and chunk.get("speaker") != args.speaker:
            continue
        results.append((cid, score, chunk))
        if len(results) >= args.limit:
            break

    if not results:
        print("No matches remained after filters.")
        return 0

    if args.json:
        print(json.dumps([{"chunk_id": cid, "score": score, "chunk": chunk,
                           "excerpt": fetch_excerpt(chunk, roots)}
                          for cid, score, chunk in results], indent=2))
        return 0

    for cid, score, chunk in results:
        speaker = f" [{chunk['speaker']}]" if chunk.get("speaker") else ""
        print(f"  [{score:.1f}]  {chunk['origin']}/{chunk['category']}{speaker}  "
              f"{chunk['path']}:L{chunk['line_start']}-{chunk['line_end']}")
        print(f"    {chunk['preview']}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
