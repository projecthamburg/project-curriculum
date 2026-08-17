#!/usr/bin/env python3
"""governance/index_codebase.py — build the codebase and documentation index.

**Deliberately separate from the evidence index.** Both feed curriculum generation, and they
are kept apart because their chunk shapes and their trust semantics differ. Merging them makes
a query unable to distinguish *"someone said the system does X"* from *"the system does X"* —
and that distinction is most of the value.

| | evidence index | this index |
|---|---|---|
| over | Tier 1/2/3 captures | source, docs, config, tests |
| chunked by | speaker turn | symbol and section |
| answers | what was said, asked, decided | what exists and how it behaves |

This is the **only** index Pathway B has (protocol/EVIDENCE_AND_PATHWAYS.md). A project with no
conversation history still gets a real curriculum from it — with intent recorded as absent
rather than inferred.

Chunking:
  - **code** — split at top-level symbol boundaries (def/class/function/const/type/impl…) so a
    chunk is a unit someone can reason about, not an arbitrary window. Each chunk records the
    symbol it starts at.
  - **docs** — split at markdown headings.
  - **everything else** — fixed windows.

Deliberately NOT done: no AST parsing, no call graphs, no dead-code or complexity analysis.
That is a different tool's job and it is out of scope here. This index answers "where is X and
what is near it", nothing more, and says so rather than implying depth it does not have.

Usage:
    python3 governance/index_codebase.py
    python3 governance/index_codebase.py --root /path/to/repo
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
import re
from collections import Counter, defaultdict

from pc_config import paths
from build_search_index import STOPWORDS, tokenize, top_keywords, chunk_generic

P = paths()

CODE_EXT = {
    ".py": "python", ".js": "javascript", ".jsx": "javascript", ".ts": "typescript",
    ".tsx": "typescript", ".go": "go", ".rs": "rust", ".java": "java", ".rb": "ruby",
    ".php": "php", ".c": "c", ".h": "c", ".cpp": "cpp", ".hpp": "cpp", ".cs": "csharp",
    ".swift": "swift", ".kt": "kotlin", ".sh": "shell", ".sql": "sql", ".scala": "scala",
}
DOC_EXT = {".md": "markdown", ".rst": "rst", ".txt": "text", ".adoc": "asciidoc"}
CONFIG_EXT = {".json": "json", ".yaml": "yaml", ".yml": "yaml", ".toml": "toml",
              ".ini": "ini", ".cfg": "ini"}

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
             ".next", "target", "vendor", ".pytest_cache", "coverage", ".mypy_cache"}

SYMBOL_RE = re.compile(
    r"^(?:export\s+)?(?:default\s+)?(?:async\s+)?"
    r"(?:def|class|function|const|let|var|type|interface|enum|struct|impl|trait|fn|"
    r"public|private|protected|func)\s+([A-Za-z_$][\w$]*)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
TEST_HINT = re.compile(r"(^|/)(tests?|__tests__|spec)(/|$)|(_test|\.test|\.spec)\.", re.I)


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def classify(path: str) -> tuple:
    ext = os.path.splitext(path)[1].lower()
    if TEST_HINT.search(path):
        return "test", CODE_EXT.get(ext, DOC_EXT.get(ext, "unknown"))
    if ext in CODE_EXT:
        return "code", CODE_EXT[ext]
    if ext in DOC_EXT:
        return "docs", DOC_EXT[ext]
    if ext in CONFIG_EXT:
        return "config", CONFIG_EXT[ext]
    return "", ""


def chunk_code(lines: list, max_lines: int = 160) -> list:
    """Split at top-level symbol boundaries. A symbol at column 0 starts a new chunk; an
    over-long symbol is split further, keeping its name."""
    starts = [(i, m.group(1)) for i, line in enumerate(lines, start=1)
              if not line[:1].isspace() and (m := SYMBOL_RE.match(line.strip()))]
    if not starts:
        return [(s, e, None) for s, e, _ in chunk_generic(lines, max_lines)]
    segments = []
    if starts[0][0] > 1:
        segments.append((1, starts[0][0] - 1, "<module>"))
    for idx, (start, name) in enumerate(starts):
        end = starts[idx + 1][0] - 1 if idx + 1 < len(starts) else len(lines)
        if end - start + 1 > max_lines:
            sub = start
            while sub <= end:
                sub_end = min(sub + max_lines - 1, end)
                segments.append((sub, sub_end, name))
                sub = sub_end + 1
        else:
            segments.append((start, end, name))
    return segments


def chunk_docs(lines: list) -> list:
    heads = [(i, HEADING_RE.match(line).group(2).strip())
             for i, line in enumerate(lines, start=1) if HEADING_RE.match(line)]
    if not heads:
        return [(s, e, None) for s, e, _ in chunk_generic(lines)]
    segments = []
    if heads[0][0] > 1:
        segments.append((1, heads[0][0] - 1, None))
    for idx, (start, title) in enumerate(heads):
        end = heads[idx + 1][0] - 1 if idx + 1 < len(heads) else len(lines)
        segments.append((start, end, title))
    return segments


def walk(root: str) -> list:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            kind, lang = classify(path)
            if not kind:
                continue
            try:
                if os.path.getsize(path) > 2_000_000:
                    print(f"  skipped (over 2 MB): {os.path.relpath(path, root)}")
                    continue
            except OSError:
                continue
            files.append((path, kind, lang))
    return sorted(files)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None,
                    help="defaults to external_root when set, else content_root")
    args = ap.parse_args()

    root = os.path.abspath(args.root) if args.root else P["manifest_root"]
    if not os.path.isdir(root):
        print(f"No such root: {root}")
        return 1

    out_path = os.path.join(P["gov"], "codebase_index.json")
    files = walk(root)
    chunks, sources, cid = [], [], 1

    for path, kind, lang in files:
        rel = os.path.relpath(path, root)
        try:
            lines = open(path, encoding="utf-8", errors="ignore").read().splitlines()
        except OSError:
            continue
        segs = (chunk_code(lines) if kind in ("code", "test")
                else chunk_docs(lines) if kind == "docs"
                else [(s, e, None) for s, e, _ in chunk_generic(lines)])
        n = 0
        for start, end, symbol in segs:
            text = "\n".join(lines[start - 1:end]).strip()
            if not text:
                continue
            chunks.append({
                "id": f"cb_{cid:06d}", "path": rel, "kind": kind, "language": lang,
                "symbol": symbol, "line_start": start, "line_end": end,
                "keywords": top_keywords(text[:15000]),
                "preview": text[:260] + ("..." if len(text) > 260 else ""),
            })
            cid += 1
            n += 1
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        sources.append({"path": rel, "kind": kind, "language": lang,
                        "lines": len(lines), "sha256": h, "chunk_count": n})

    keyword_index, path_index = defaultdict(list), defaultdict(list)
    kind_index, symbol_index = defaultdict(list), defaultdict(list)
    for c in chunks:
        for k in c["keywords"]:
            keyword_index[k].append(c["id"])
        path_index[c["path"]].append(c["id"])
        kind_index[c["kind"]].append(c["id"])
        if c["symbol"]:
            symbol_index[c["symbol"]].append(c["id"])

    by_kind = Counter(s["kind"] for s in sources)
    index = {
        "metadata": {
            "generated_at": iso_now(), "root": root,
            "project_id": P["config"]["project_id"],
            "index_kind": "keyword-lexical", "embeddings": False,
            "analysis_depth": "lexical only — no AST, no call graph, no complexity analysis",
            "file_count": len(sources), "chunk_count": len(chunks),
            "total_lines": sum(s["lines"] for s in sources),
            "by_kind": dict(by_kind),
            "languages": dict(Counter(s["language"] for s in sources if s["language"])),
        },
        "sources": sources, "chunks": chunks,
        "indices": {"keyword_index": dict(keyword_index), "path_index": dict(path_index),
                    "kind_index": dict(kind_index), "symbol_index": dict(symbol_index)},
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    m = index["metadata"]
    print(f"Built codebase index at {out_path}")
    print(f"Root: {root}")
    print(f"Files: {m['file_count']} ({', '.join(f'{k} {v}' for k, v in sorted(by_kind.items()))})"
          f" | lines: {m['total_lines']} | chunks: {m['chunk_count']}")
    print(f"Languages: {', '.join(sorted(m['languages'])) or '(none detected)'}")
    if not files:
        print("  Nothing indexed — no recognized source, doc or config files under this root.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
