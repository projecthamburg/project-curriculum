#!/usr/bin/env python3
"""governance/build_search_index.py — build this instance's local search index.

A keyword/lexical index: chunking + inverted index + scored retrieval. **Not a vector
database** — no embeddings, nothing computes similarity, and it does no live web or paper
search. It finds only what is already written down in the files it was pointed at.
Saying so plainly matters: a tool named like a vector DB that isn't one causes people to
over-trust its recall.

Fully local. No network, no shared infrastructure, no service to keep in sync. One JSON
file, rebuildable from scratch at any time — which is why it is gitignored rather than
committed (every rebuild rewrites the whole blob).

Two source families, each origin-labeled so results self-identify:

  1. governance/sources/*.md — captured session transcripts and imported chat logs.
     Chunked by speaker turn. Category comes from the sidecar (see _sidecar_category).
  2. Every `enabled: true` entry in the manifest — protocol docs, courses, rubrics,
     exams, whatever this instance wants searchable. Chunked by paragraph/section.
     origin per entry: `internal` = this instance's own authored material,
     `external` = borrowed or third-party reference material.

Always check a result's origin before treating it as this instance's own work.

Usage:
    python3 governance/build_search_index.py
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from functools import lru_cache

from pc_config import paths

P = paths()

SESSION_CATEGORIES = {"ice-session", "chat-log", "global-adjacent-session"}

SPEAKER_RE = re.compile(r"^#{1,6}\s+(User|Assistant|System|Tool)\s*$")
TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/#-]*")

STOPWORDS = {
    "the", "and", "for", "that", "with", "this", "from", "have", "were", "what",
    "when", "where", "your", "into", "will", "would", "about", "there", "their",
    "them", "they", "then", "than", "because", "which", "while", "also", "been",
    "being", "just", "like", "some", "only", "more", "most", "using", "used",
    "need", "needs", "onto", "over", "under", "after", "before", "does", "doing",
    "done", "each", "other", "others", "unto", "both", "same", "very", "make",
    "made", "much", "many", "ours", "ourselves", "these", "those", "such", "still", "here",
}


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


@lru_cache(maxsize=200000)
def normalize_token(token: str) -> str:
    token = token.strip().lower().strip("`'\"[]{}()<>,;!?")
    return token.replace("’", "'").strip(".")


@lru_cache(maxsize=200000)
def expand_token_parts(token: str) -> tuple:
    """A path or dotted identifier is searchable whole AND by its parts, so a query for
    `thesis` finds `protocol/THESIS_AND_DEFENSE.md`."""
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
    return tuple(deduped)


def tokenize(text: str) -> list:
    terms = []
    for raw in TOKEN_RE.findall(text):
        terms.extend(expand_token_parts(raw))
    return terms


def top_keywords(text: str, limit: int = 25) -> list:
    counts = Counter(tokenize(text))
    return [t for t, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------ manifest ----

def parse_manifest(path: str) -> list:
    """Minimal parser for the manifest's fixed shape — deliberately dependency-free so a
    fresh clone needs nothing installed. Expects:

        files:
          - path: protocol/MASTER_RUBRIC.md
            enabled: true
            category: protocol
            origin: internal
            note: "optional"
    """
    entries, cur = [], None
    if not os.path.exists(path):
        return entries
    for raw in open(path, encoding="utf-8"):
        s = raw.strip()
        if not s or s.startswith("#") or s == "files:":
            continue
        if s.startswith("- path:"):
            if cur:
                entries.append(cur)
            cur = {"path": s.split("- path:", 1)[1].strip().strip('"'),
                   "enabled": True, "category": "", "origin": "internal",
                   "note": "", "root": ""}
        elif cur is not None:
            for key in ("enabled", "category", "origin", "note", "root"):
                if s.startswith(key + ":"):
                    val = s.split(":", 1)[1].strip().strip('"')
                    cur[key] = (val == "true") if key == "enabled" else val
                    break
    if cur:
        entries.append(cur)
    return entries


def _sidecar_category(md_path: str) -> str:
    """A captured source's category is recorded by whatever captured it, in a `.meta.json`
    sidecar. Defaults to ice-session so a hand-dropped transcript still chunks correctly."""
    side = md_path[:-3] + ".meta.json" if md_path.endswith(".md") else md_path + ".meta.json"
    if os.path.exists(side):
        try:
            return json.load(open(side, encoding="utf-8")).get("category", "ice-session")
        except (json.JSONDecodeError, OSError):
            pass
    return "ice-session"


# ------------------------------------------------------------------ chunking ----

def chunk_session_transcript(lines: list) -> list:
    """Speaker-turn chunking. A turn keeps its speaker label so a query can tell what the
    human asked from what the model answered — which is the whole point for ICE."""
    markers = [(i, m.group(1).lower())
               for i, line in enumerate(lines, start=1)
               if (m := SPEAKER_RE.match(line.strip()))]
    if not markers:
        return chunk_generic(lines)
    segments = []
    for idx, (start, speaker) in enumerate(markers):
        end = markers[idx + 1][0] - 1 if idx + 1 < len(markers) else len(lines)
        if end - start + 1 > 200:
            # A very long turn splits further, keeping the same speaker label.
            sub = start
            while sub <= end:
                sub_end = min(sub + 199, end)
                segments.append((sub, sub_end, speaker))
                sub = sub_end + 1
        else:
            segments.append((start, end, speaker))
    return segments


def chunk_generic(lines: list, max_lines: int = 120) -> list:
    """Paragraph-aware chunking for prose documents — cuts on a blank line where possible
    so a chunk boundary doesn't land mid-sentence."""
    segments, start, last_blank = [], 1, None
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            last_blank = i
        if i - start + 1 > max_lines:
            cut = last_blank if last_blank and last_blank > start else i - 1
            segments.append((start, cut, None))
            start, last_blank = cut + 1, None
    if start <= len(lines):
        segments.append((start, len(lines), None))
    return segments or [(1, max(len(lines), 1), None)]


def build_chunks(rel_path, abs_path, origin, category, cid_start):
    lines = open(abs_path, encoding="utf-8", errors="ignore").read().splitlines()
    segments = (chunk_session_transcript(lines) if category in SESSION_CATEGORIES
                else chunk_generic(lines))
    chunks, cid = [], cid_start
    for start, end, speaker in segments:
        seg = "\n".join(lines[start - 1:end]).strip()
        if not seg:
            continue
        chunks.append({
            "id": f"chk_{cid:06d}", "path": rel_path, "origin": origin,
            "category": category, "speaker": speaker,
            "line_start": start, "line_end": end,
            "keywords": top_keywords(seg[:15000]),
            "preview": seg[:260] + ("..." if len(seg) > 260 else ""),
        })
        cid += 1
    return chunks, cid


# ---------------------------------------------------------------------- main ----

def collect_sources() -> list:
    sources = []

    # Family 1 — captured sessions and imported chat logs.
    if os.path.isdir(P["sources"]):
        for fn in sorted(os.listdir(P["sources"])):
            if not fn.endswith(".md"):
                continue
            abs_path = os.path.join(P["sources"], fn)
            sources.append({"path": f"sources/{fn}", "abs_path": abs_path,
                            "root": P["gov"], "origin": "internal",
                            "category": _sidecar_category(abs_path)})

    # Family 2 — manifest-driven files. TWO roots, not one: an external project's
    # governance layer must index both the upstream content it studies AND its own
    # authored material (syllabus, ICE chapters). A per-entry `root:` selects which.
    #   root: content   -> this project's own folder
    #   root: external  -> the upstream repository (external_root)
    # Default is manifest_root: external_root when set, else content_root — so a
    # nested project's manifest needs no root: field at all.
    for e in parse_manifest(P["manifest"]):
        if not e["enabled"]:
            continue
        if e.get("root") == "content":
            root = P["content_root"]
        elif e.get("root") == "external":
            if not P["external_root"]:
                print(f"  entry declares root: external but no external_root is "
                      f"configured, skipped: {e['path']}")
                continue
            root = P["external_root"]
        else:
            root = P["manifest_root"]
        abs_path = os.path.join(root, e["path"])
        if not os.path.exists(abs_path):
            print(f"  manifest entry missing on disk, skipped: {e['path']}")
            continue
        sources.append({"path": e["path"], "abs_path": abs_path,
                        "root": root, "origin": e["origin"],
                        "category": e["category"] or "uncategorized"})
    return sources


def main() -> int:
    sources = collect_sources()
    all_chunks, source_records, cid = [], [], 1

    for src in sources:
        chunks, cid = build_chunks(src["path"], src["abs_path"], src["origin"],
                                   src["category"], cid)
        all_chunks.extend(chunks)
        source_records.append({
            "path": src["path"], "root": src["root"], "origin": src["origin"],
            "category": src["category"], "sha256": sha256_file(src["abs_path"]),
            "mtime": dt.datetime.fromtimestamp(
                os.path.getmtime(src["abs_path"]), tz=dt.timezone.utc).isoformat(),
            "chunk_count": len(chunks),
        })

    keyword_index, path_index = defaultdict(list), defaultdict(list)
    category_index, origin_index = defaultdict(list), defaultdict(list)
    for c in all_chunks:
        for kw in c["keywords"]:
            keyword_index[kw].append(c["id"])
        path_index[c["path"]].append(c["id"])
        category_index[c["category"]].append(c["id"])
        origin_index[c["origin"]].append(c["id"])

    index = {
        "metadata": {
            "generated_at": iso_now(),
            "project_id": P["config"]["project_id"],
            "content_root": P["content_root"],
            "manifest_root": P["manifest_root"],
            "index_kind": "keyword-lexical",
            "embeddings": False,
            "source_count": len(sources),
            "chunk_count": len(all_chunks),
            "internal_sources": sum(1 for s in source_records if s["origin"] == "internal"),
            "external_sources": sum(1 for s in source_records if s["origin"] == "external"),
        },
        "sources": source_records,
        "chunks": all_chunks,
        "indices": {
            "keyword_index": dict(keyword_index), "path_index": dict(path_index),
            "category_index": dict(category_index), "origin_index": dict(origin_index),
        },
    }

    with open(P["index"], "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    m = index["metadata"]
    print(f"Built search index at {P['index']}")
    print(f"Sources: {m['source_count']} ({m['internal_sources']} internal, "
          f"{m['external_sources']} external) | Chunks: {m['chunk_count']}")
    if not sources:
        print("  Nothing indexed — no sources/*.md and no reachable manifest entries yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
