#!/usr/bin/env python3
"""governance/import_chat_logs.py — import exported human↔AI conversations from .md/.txt.

This is the path for every provider that has **no local session store to scan**: ChatGPT web
and desktop, Claude.ai, Gemini and AI Studio, Kimi Desktop, OpenRouter frontends, private or
self-hosted models, and any transcript a person pasted into a file by hand. No programmatic
reader exists for those, so a manual export is the only workflow — which makes this a
first-class capture path, not a convenience.

It is also how a **public example** works. A seeding run in CI cannot reach anyone's laptop,
so a contributed seed pack ships its evidence as committed .md/.txt, and this is what reads it.

What it does:
  - detects the export format and the provider it came from
  - splits the conversation into turns, preserving timestamps where the export has them
  - normalizes into the `### User` / `### Assistant` marker form the index chunks by turn
  - redacts secrets in memory before anything reaches disk
  - records timestamp and association confidence explicitly (protocol/ICE.md), never inferring
    a time silently and never promoting a guess to a fact
  - diffs against the same ingestion ledger discover_sessions.py uses, keyed by content hash
    since these exports carry no stable session ID

What it does NOT do:
  - guess at a conversation's project when none was stated. Default association is `explicit`
    because a human pointed at the file; pass --association candidate for a bulk sweep whose
    membership still needs confirming. Uncertain evidence is never silently made canonical.
  - invent structure. An export it cannot parse is captured whole, marked `unparsed`, and
    reported — not quietly dropped and not force-fitted into a turn shape it doesn't have.

Usage:
    python3 governance/import_chat_logs.py ~/Downloads/exports/
    python3 governance/import_chat_logs.py ~/Downloads/chat.md --real
    python3 governance/import_chat_logs.py examples/seed/evidence/ --real --association candidate
"""
from __future__ import annotations
import argparse
import datetime
import glob
import hashlib
import json
import os
import re

from pc_config import paths
from redact_util import redact

P = paths()

# ---------------------------------------------------------------- detectors ----
# Ordered most-specific first. Each returns a list of {speaker, text, timestamp} turns.

CHATGPT_EXPORTER_TURN = re.compile(
    r"^##\s+(Prompt|Response):\s*$\n(?:^(.+)$\n)?", re.MULTILINE)
SPECSTORY_TURN = re.compile(
    r"^_\*\*(User|Assistant|Agent)\s*(?:\(([^)]*)\))?\*\*_\s*$", re.MULTILINE)
HEADING_TURN = re.compile(
    r"^#{2,4}\s+(User|Human|You|Assistant|Agent|AI|Model|System|Tool)\s*$", re.MULTILINE)
PREFIX_TURN = re.compile(
    r"^(User|Human|You|Assistant|Claude|ChatGPT|Gemini|Model|AI):\s", re.MULTILINE)

SPEAKER_MAP = {
    "prompt": "user", "user": "user", "human": "user", "you": "user",
    "response": "assistant", "assistant": "assistant", "agent": "assistant",
    "ai": "assistant", "model": "assistant", "claude": "assistant",
    "chatgpt": "assistant", "gemini": "assistant",
    "system": "system", "tool": "tool",
}

PROVIDER_HINTS = [
    ("chatgpt", re.compile(r"chatgpt\.com|ChatGPT Exporter|chat\.openai\.com", re.I)),
    ("claude-ai", re.compile(r"claude\.ai", re.I)),
    ("gemini", re.compile(r"gemini\.google\.com|aistudio\.google\.com|AI Studio", re.I)),
    ("kimi", re.compile(r"kimi\.moonshot|kimi\.com", re.I)),
    ("openrouter", re.compile(r"openrouter\.ai", re.I)),
    ("specstory", re.compile(r"specstory", re.I)),
]

ISO_DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
US_DATE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def detect_provider(text: str, filename: str) -> str:
    blob = text[:8000] + "\n" + filename
    for name, pattern in PROVIDER_HINTS:
        if pattern.search(blob):
            return name
    return "unknown"


def _split_on(matches, text, speaker_of, ts_of=None) -> list:
    turns = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end].strip()
        if body.endswith("---"):
            body = body[:-3].strip()
        if not body:
            continue
        turns.append({"speaker": speaker_of(m), "text": body,
                      "timestamp": ts_of(m, body) if ts_of else None})
    return turns


def parse_turns(text: str) -> tuple:
    """Return (turns, format_name). An unrecognized export yields ([], 'unparsed')."""
    m = list(CHATGPT_EXPORTER_TURN.finditer(text))
    if len(m) >= 2:
        def ts_of(_mm, body):
            # This exporter writes the turn's date on the line right after the header.
            first = body.splitlines()[0] if body else ""
            d = ISO_DATE.search(first) or US_DATE.search(first)
            if not d:
                return None
            if d.re is ISO_DATE:
                return d.group(1)
            mo, da, yr = d.groups()
            return f"{yr}-{int(mo):02d}-{int(da):02d}"
        return _split_on(m, text, lambda mm: SPEAKER_MAP[mm.group(1).lower()], ts_of), \
            "chatgpt-exporter"

    m = list(SPECSTORY_TURN.finditer(text))
    if len(m) >= 2:
        return _split_on(m, text, lambda mm: SPEAKER_MAP[mm.group(1).lower()],
                         lambda mm, _b: mm.group(2)), "specstory"

    m = list(HEADING_TURN.finditer(text))
    if len(m) >= 2:
        return _split_on(m, text, lambda mm: SPEAKER_MAP[mm.group(1).lower()]), "headings"

    m = list(PREFIX_TURN.finditer(text))
    if len(m) >= 2:
        return _split_on(m, text, lambda mm: SPEAKER_MAP[mm.group(1).lower()]), "prefixes"

    return [], "unparsed"


def file_date(path: str, text: str) -> tuple:
    """(date, confidence). Prefer a date the export itself states; fall back to the
    filesystem, and label which — never present a guess as a record."""
    head = text[:4000]
    d = ISO_DATE.search(head)
    if d:
        return d.group(1), "exact"
    d = US_DATE.search(head)
    if d:
        mo, da, yr = d.groups()
        return f"{yr}-{int(mo):02d}-{int(da):02d}", "exact"
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path), tz=datetime.timezone.utc)
    return mtime.strftime("%Y-%m-%d"), "file-derived"


def content_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest()[:16]


def load_ledger() -> dict:
    if not os.path.exists(P["ledger"]):
        return {"ingested": []}
    return json.load(open(P["ledger"], encoding="utf-8"))


def save_ledger(ledger) -> None:
    os.makedirs(P["sources"], exist_ok=True)
    with open(P["ledger"], "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def render(turns, meta) -> str:
    lines = [f"<!-- Imported chat log — {meta['origin_file']} -->",
             f"# {meta['stem']}", "",
             f"- **Provider:** {meta['provider']}",
             f"- **Export format:** {meta['format']}",
             f"- **Date:** {meta['date']}  (confidence: {meta['timestamp_confidence']})",
             f"- **Turns:** {len(turns)}",
             f"- **Association:** {meta['association']}",
             f"- **Evidence tier:** {meta['tier']}"
             + ("  — monologue: can establish Ideas and Concerns, NOT Expectations"
                if meta['tier'] == "3" else ""), "", "---", ""]
    if not turns:
        lines += ["### System", "",
                  "_This export's turn structure was not recognized by any known parser, so it "
                  "is captured whole and unsplit rather than force-fitted into a turn shape it "
                  "does not have. Speaker attribution below is unavailable._", "", "---", "",
                  "### User", "", meta["raw_text"], ""]
        return "\n".join(lines) + "\n"
    for t in turns:
        header = {"user": "### User", "assistant": "### Assistant",
                  "system": "### System", "tool": "### Tool"}[t["speaker"]]
        lines += [header]
        if t.get("timestamp"):
            lines.append(f"*({t['timestamp']})*")
        lines += ["", t["text"], "", "---", ""]
    return "\n".join(lines) + "\n"


def gather(target: str) -> list:
    if os.path.isfile(target):
        return [target]
    files = []
    for ext in ("md", "txt"):
        files += glob.glob(os.path.join(target, "**", f"*.{ext}"), recursive=True)
    # Never re-import this instance's own captured sources.
    return sorted(f for f in files if os.path.abspath(f) != P["sources"]
                  and not os.path.abspath(f).startswith(P["sources"] + os.sep))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="a .md/.txt export, or a directory to sweep recursively")
    ap.add_argument("--real", action="store_true", help="write the captures for real")
    ap.add_argument("--tier", choices=["1", "2", "3"], default=None,
                    help="Evidence tier (protocol/EVIDENCE_AND_PATHWAYS.md). Defaults to 2 "
                         "for a detected LLM provider, 3 for an unrecognized monologue. "
                         "Tier 3 cannot establish an Expectation - only Ideas and Concerns.")
    ap.add_argument("--association", choices=["explicit", "path", "candidate"],
                    default="explicit",
                    help="how confidently this evidence belongs to this project "
                         "(protocol/ICE.md). Default explicit: a human pointed at it.")
    args = ap.parse_args()

    if not os.path.exists(args.target):
        print(f"No such path: {args.target}")
        return 1

    files = gather(args.target)
    if not files:
        print(f"No .md or .txt files found under {args.target}")
        return 0

    ledger = load_ledger()
    known = {e.get("content_id") for e in ledger["ingested"] if e.get("content_id")}
    os.makedirs(P["sources"], exist_ok=True)

    imported = skipped = unparsed = 0
    for path in files:
        text = open(path, encoding="utf-8", errors="ignore").read()
        if not text.strip():
            continue
        cid = content_id(text)
        if cid in known:
            skipped += 1
            continue

        provider = detect_provider(text, os.path.basename(path))
        turns, fmt = parse_turns(text)
        # Tier is about what the source CAN establish, not what it is worth. A source
        # with no counterparty is Tier 3 however important its content: a monologue
        # cannot carry an Ask -> Response -> Lock-in chain.
        has_both_voices = {t["speaker"] for t in turns} >= {"user", "assistant"}
        tier = args.tier or ("2" if has_both_voices else "3")
        assoc = args.association
        if tier == "3" and assoc == "path":
            assoc = "candidate"   # Tier 3 has no path in the record to match on
        date, ts_conf = file_date(path, text)
        base = re.sub(r"[^a-z0-9]+", "-",
                      os.path.splitext(os.path.basename(path))[0].lower()).strip("-")[:40]
        stem = f"{date}_{provider}_{base or cid}"

        if fmt == "unparsed":
            unparsed += 1
        print(f"  {'NEW ' if args.real else 'WOULD'} [T{tier} {provider}/{fmt}] "
              f"{os.path.basename(path)} -> {stem}.md  "
              f"({len(turns)} turns, date {date}/{ts_conf}, assoc {assoc})")
        if not args.real:
            continue

        meta = {"stem": stem, "provider": provider, "format": fmt, "date": date,
                "timestamp_confidence": ts_conf, "association": assoc, "tier": tier,
                "origin_file": os.path.abspath(path), "raw_text": text}

        md_text, md_counts = redact(render(turns, meta))
        with open(os.path.join(P["sources"], f"{stem}.md"), "w", encoding="utf-8") as f:
            f.write(md_text)
        json_text, _ = redact(json.dumps(
            {"provider": provider, "format": fmt, "date": date,
             "timestamp_confidence": ts_conf, "turn_count": len(turns), "turns": turns},
            indent=2, ensure_ascii=False))
        with open(os.path.join(P["sources"], f"{stem}.json"), "w", encoding="utf-8") as f:
            f.write(json_text)
        with open(os.path.join(P["sources"], f"{stem}.meta.json"), "w", encoding="utf-8") as f:
            json.dump({"category": "chat-log", "source_tool": provider,
                       "tier": tier,
                       "can_establish_expectation": tier != "3",
                       "export_format": fmt, "session_id": cid,
                       "origin_file": os.path.abspath(path),
                       "association": assoc, "timestamp": date,
                       "timestamp_confidence": ts_conf, "turn_count": len(turns),
                       "captured_at": _now_iso(), "raw_is_immutable": True}, f, indent=2)
        if md_counts:
            print(f"       redacted: {md_counts}")

        ledger["ingested"].append({
            "session_id": cid, "content_id": cid, "tool": f"chat-log:{provider}",
            "native_path": os.path.abspath(path),
            "sources_files": [f"{stem}.md", f"{stem}.json"], "captured_at": _now_iso(),
        })
        imported += 1

    if args.real and imported:
        save_ledger(ledger)

    print(f"\nFiles seen: {len(files)} | imported: {imported} | "
          f"already known: {skipped} | unparsed structure: {unparsed}")
    if unparsed:
        print("  Unparsed exports were captured whole and marked — their turn structure was "
              "not recognized, so speaker attribution is unavailable for those. Stated here "
              "rather than left for a reader to discover.")
    if not args.real:
        print("Dry-run only — pass --real to write these captures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
