#!/usr/bin/env python3
"""governance/discover_sessions.py — find and capture agent work sessions for this instance.

Scans known native session-storage locations on THIS machine and matches **only by a real
cwd/workDir check — never a raw text-mention grep.** That distinction is not stylistic: a
grep for a project's name or an IP address reliably hits unrelated sessions that merely
mention it. Identity matching is the only method that produces a defensible capture set.

Match roots come from governance/config.json: `content_root`, plus `external_root` when this
layer governs a separate repository. A session whose recorded cwd is at or under either root
is a capture candidate.

FIVE providers:
  - Codex CLI          ~/.codex/sessions/**/*.jsonl        matched by session_meta.cwd
                       (read from the first line only, not a full parse)
  - Claude Code CLI    ~/.claude/projects/<cwd-encoded>/*.jsonl
                       matched by directory-name encoding, prefix-aware so a subdirectory
                       session is still caught
  - Kimi Code CLI      ~/.kimi-code/session_index.jsonl    matched by `workDir`, NOT `cwd`.
                       A real documented gotcha: checking `cwd` here finds nothing at all.
  - Cursor (in-repo)   <root>/.specstory/history/*.md      unambiguous by construction
  - Claude Desktop     ~/Library/Application Support/Claude/claude-code-sessions/**/local_*.json
                       matched by cwd/originCwd. A SEPARATE, lighter metadata index the
                       desktop app keeps alongside — not instead of — the CLI transcript.
                       Its real value is as a FALLBACK: it can survive after the CLI's own
                       .jsonl has been removed by cleanup, preserving the session's title,
                       true activity window, and referenced paths. When both exist, prefer
                       the CLI capture; when the CLI transcript is gone, this is what is
                       left to record honestly.

KNOWN GAPS — not implemented, listed so nobody rediscovers the absence:
  - Kimi sessions are DETECTED but not auto-converted; its on-disk turn format has not been
    schema-verified against a real match, and a wrong converter is worse than a manual note.
  - Cursor's native workspace SQLite store (state.vscdb / cursorDiskKV) is deliberately not
    scanned — too heavy for a routine per-commit check. Treat as an occasional manual audit.
  - Gemini Code Assist inside Cursor (a SQLite blob), Cursor's separate background-agent
    transcripts, Antigravity (protobuf payloads in a .db), and Kimi Desktop: no reader here.
  - ChatGPT / Claude.ai / Gemini web and desktop: **no programmatic reader exists.** Manual
    export is the only workflow — that is what import_chat_logs.py is for, and why it is a
    first-class path rather than a convenience.
  - Another machine's native stores are NOT scanned. This script reads the local machine only.

Usage:
    python3 governance/discover_sessions.py           # dry-run: report what is new
    python3 governance/discover_sessions.py --real     # convert, redact, and file them
"""
from __future__ import annotations
import argparse
import datetime
import glob
import json
import os
import re

from pc_config import paths
from redact_util import redact

P = paths()
HOME = os.path.expanduser("~")
MATCH_ROOTS = [r for r in (P["content_root"], P["external_root"]) if r]


def _cwd_matches(cwd: str) -> bool:
    if not cwd:
        return False
    return any(cwd == r or cwd.startswith(r + "/") for r in MATCH_ROOTS)


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_ledger() -> dict:
    if not os.path.exists(P["ledger"]):
        return {"ingested": []}
    return json.load(open(P["ledger"], encoding="utf-8"))


def save_ledger(ledger: dict) -> None:
    os.makedirs(P["sources"], exist_ok=True)
    with open(P["ledger"], "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def already_known(ledger, tool, session_id) -> bool:
    return any(e["tool"] == tool and e["session_id"] == session_id for e in ledger["ingested"])


def trunc(s, n=3000) -> str:
    s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False)
    return s if len(s) <= n else (
        s[:n] + f"\n...[truncated, {len(s)} chars total — full text in the companion .json]")


def write_redacted(path, text) -> None:
    """Redaction happens in memory before either rendering reaches disk. Matched values are
    never printed — only pattern labels and counts."""
    safe, counts = redact(text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(safe)
    if counts:
        print(f"       redacted {os.path.basename(path)}: {counts}")


def write_sidecar(stem, candidate, timestamp_confidence) -> None:
    """Records what this capture is, so the index chunks it correctly and a reader can see
    the provenance without re-deriving it. Timestamp confidence is explicit per
    protocol/ICE.md — an inferred time must never be indistinguishable from a recorded one."""
    with open(os.path.join(P["sources"], f"{stem}.meta.json"), "w", encoding="utf-8") as f:
        json.dump({
            "category": "ice-session",
            "tier": "1",                     # an agent that could act; tool calls in record
            "can_establish_expectation": True,
            "source_tool": candidate["tool"],
            "session_id": candidate["session_id"],
            "native_path": candidate["native_path"],
            "association": "path",
            "timestamp": candidate.get("timestamp"),
            "timestamp_confidence": timestamp_confidence,
            "captured_at": _now_iso(),
            "raw_is_immutable": True,
        }, f, indent=2)


# ------------------------------------------------------------------ scanners ----

def scan_codex() -> list:
    found = []
    for path in glob.glob(os.path.join(HOME, ".codex", "sessions", "**", "*.jsonl"),
                          recursive=True):
        try:
            with open(path, encoding="utf-8") as f:
                first = json.loads(f.readline())
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            continue
        if first.get("type") != "session_meta":
            continue
        meta = first.get("payload", {})
        if _cwd_matches(meta.get("cwd") or ""):
            found.append({"tool": "codex", "session_id": meta.get("id"),
                          "native_path": path, "timestamp": meta.get("timestamp")})
    return found


def scan_claude_code() -> list:
    base = os.path.join(HOME, ".claude", "projects")
    if not os.path.isdir(base):
        return []
    found = []
    for root in MATCH_ROOTS:
        encoded = root.replace("/", "-").replace("_", "-")
        for name in os.listdir(base):
            if not (name == encoded or name.startswith(encoded + "-")):
                continue
            for path in glob.glob(os.path.join(base, name, "*.jsonl")):
                found.append({"tool": "claude-code",
                              "session_id": os.path.splitext(os.path.basename(path))[0],
                              "native_path": path, "timestamp": None})
    return found


def scan_kimi() -> list:
    index_path = os.path.join(HOME, ".kimi-code", "session_index.jsonl")
    if not os.path.exists(index_path):
        return []
    found = []
    for line in open(index_path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if _cwd_matches(d.get("workDir") or ""):   # NOT "cwd" — see module docstring
            found.append({"tool": "kimi", "session_id": d.get("sessionId"),
                          "native_path": d.get("sessionDir"), "timestamp": None})
    return found


def scan_cursor_inrepo() -> list:
    found = []
    for root in MATCH_ROOTS:
        hist = os.path.join(root, ".specstory", "history")
        if not os.path.isdir(hist):
            continue
        for path in sorted(glob.glob(os.path.join(hist, "*.md"))):
            found.append({"tool": "cursor", "session_id": os.path.basename(path),
                          "native_path": path, "timestamp": None})
    return found


def scan_claude_desktop() -> list:
    base = os.path.join(HOME, "Library", "Application Support", "Claude",
                        "claude-code-sessions")
    if not os.path.isdir(base):
        return []
    found = []
    for path in glob.glob(os.path.join(base, "**", "local_*.json"), recursive=True):
        try:
            d = json.load(open(path, encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            continue
        if _cwd_matches(d.get("cwd") or d.get("originCwd") or ""):
            found.append({"tool": "claude-desktop",
                          "session_id": d.get("sessionId") or os.path.basename(path),
                          "native_path": path, "timestamp": d.get("createdAt"),
                          "cli_session_id": d.get("cliSessionId")})
    return found


def claude_cli_transcript_exists(session_id) -> bool:
    """Does a real CLI transcript for this exact session ID exist anywhere under
    ~/.claude/projects/, regardless of cwd match? A linked session may be filed under a
    slightly different project-folder encoding."""
    base = os.path.join(HOME, ".claude", "projects")
    if not os.path.isdir(base) or not session_id:
        return False
    return bool(glob.glob(os.path.join(base, "*", f"{session_id}.jsonl")))


# ---------------------------------------------------------------- converters ----

SPECSTORY_META_RE = re.compile(r"<!--\s*\w+ Session ([\w-]+) \(([^)]+)\)\s*-->")
SPECSTORY_TURN_RE = re.compile(r"^_\*\*(User|Agent)\s*(?:\(([^)]*)\))?\*\*_\s*$", re.MULTILINE)


def convert_cursor_inrepo(c, stem) -> list:
    text = open(c["native_path"], encoding="utf-8", errors="ignore").read()
    m = SPECSTORY_META_RE.search(text)
    markers = list(SPECSTORY_TURN_RE.finditer(text))
    turns = []
    for i, mm in enumerate(markers):
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        body = text[mm.end():end].strip()
        if body.endswith("---"):
            body = body[:-3].strip()
        turns.append({"turn": i + 1, "speaker": mm.group(1).lower(),
                      "meta": mm.group(2), "text": body})
    write_redacted(os.path.join(P["sources"], f"{stem}.md"), text)
    write_redacted(os.path.join(P["sources"], f"{stem}.json"), json.dumps(
        {"source_tool": "cursor", "capture_mechanism": "specstory",
         "session_id": m.group(1) if m else None,
         "session_timestamp_utc": m.group(2) if m else None,
         "turn_count": len(turns), "turns": turns}, indent=2, ensure_ascii=False))
    write_sidecar(stem, c, "exact" if m else "file-derived")
    return [f"{stem}.md", f"{stem}.json"]


def _read_jsonl(path) -> list:
    records = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def convert_codex(c, stem) -> list:
    records = _read_jsonl(c["native_path"])
    compact = os.path.getsize(c["native_path"]) > 10_000_000
    json_text = (json.dumps(records, ensure_ascii=False, separators=(",", ":")) if compact
                 else json.dumps(records, indent=2, ensure_ascii=False))

    meta = next((r["payload"] for r in records if r.get("type") == "session_meta"), None)
    lines = [f"<!-- Rendered from Codex rollout JSONL — {c['native_path']} -->"]
    if meta:
        git = meta.get("git") or {}
        lines += [f"<!-- codex session {meta.get('id')} ({meta.get('timestamp')}) -->",
                  f"# {stem}", "", f"- **Session ID:** {meta.get('id')}",
                  f"- **Started:** {meta.get('timestamp')}",
                  f"- **cwd:** {meta.get('cwd')}",
                  f"- **Originator:** {meta.get('originator')} (cli {meta.get('cli_version')})"]
        if git:
            lines.append(f"- **Git:** {git.get('branch')} @ {git.get('commit_hash')}")
        lines += ["", "---", ""]

    for r in records:
        ts, typ, p = r.get("timestamp", ""), r.get("type"), r.get("payload") or {}
        if typ in ("session_meta", "turn_context"):
            continue
        if typ == "compacted":
            lines += ["### System", f"*({ts})*", "", "_[context compacted by Codex]_",
                      "", "---", ""]
        elif typ == "event_msg":
            pt = p.get("type")
            if pt == "user_message":
                lines += ["### User", f"*({ts})*", "", trunc(p.get("message", "")),
                          "", "---", ""]
            elif pt == "agent_message":
                lines += ["### Assistant", f"*({ts})*", "", trunc(p.get("message", "")),
                          "", "---", ""]
            elif pt == "agent_reasoning":
                lines += [f"> _Reasoning ({ts}):_ {trunc(p.get('text', ''), 800)}", ""]
            elif pt in ("turn_aborted", "context_compacted"):
                lines += ["### System", f"*({ts})*", "", f"_[{pt}]_", "", "---", ""]
            elif pt != "token_count":
                lines += [f"_[event_msg:{pt} @ {ts}]_", ""]
        elif typ == "response_item":
            pt = p.get("type")
            if pt in ("function_call", "custom_tool_call"):
                name = p.get("name") or p.get("tool_name") or "?"
                args = p.get("arguments") or p.get("input") or ""
                lines += ["### Tool", f"*(call, {ts})* `{name}`", "", "```",
                          trunc(args, 2000), "```", ""]
            elif pt in ("function_call_output", "custom_tool_call_output"):
                out = p.get("output") or p.get("result") or ""
                lines += ["### Tool", f"*(output, {ts})*", "", "```",
                          trunc(out, 2000), "```", "", "---", ""]
            elif pt not in ("ghost_snapshot", "message", "reasoning"):
                lines += [f"_[response_item:{pt} @ {ts}]_", ""]

    write_redacted(os.path.join(P["sources"], f"{stem}.json"), json_text)
    write_redacted(os.path.join(P["sources"], f"{stem}.md"), "\n".join(lines) + "\n")
    write_sidecar(stem, c, "exact" if meta and meta.get("timestamp") else "file-derived")
    return [f"{stem}.md", f"{stem}.json"]


def _flatten_cc_content(content):
    if isinstance(content, str):
        return content, []
    text_parts, tool_parts = [], []
    for block in content or []:
        bt = block.get("type")
        if bt == "text":
            text_parts.append(block.get("text", ""))
        elif bt == "tool_use":
            tool_parts.append(("call", block.get("name"), block.get("input")))
        elif bt == "tool_result":
            tool_parts.append(("output", None, block.get("content")))
    return "\n".join(text_parts), tool_parts


def convert_claude_code(c, stem) -> list:
    records = _read_jsonl(c["native_path"])
    cwd = next((r.get("cwd") for r in records
                if r.get("type") == "system" and r.get("cwd")), None)
    lines = [f"<!-- Rendered from Claude Code session JSONL — {c['native_path']} -->",
             f"# {stem}", "", f"- **Session ID:** {c['session_id']}",
             f"- **cwd:** {cwd}", "", "---", ""]

    normal_user_texts = {
        r["message"]["content"] for r in records
        if r.get("type") == "user" and isinstance((r.get("message") or {}).get("content"), str)
    }

    for r in records:
        ts, typ = r.get("timestamp", ""), r.get("type")
        if typ in ("user", "assistant"):
            text, tool_parts = _flatten_cc_content((r.get("message") or {}).get("content"))
            if text.strip():
                lines += ["### User" if typ == "user" else "### Assistant",
                          f"*({ts})*", "", trunc(text), "", "---", ""]
            for kind, name, payload in tool_parts:
                if kind == "call":
                    lines += ["### Tool", f"*(call, {ts})* `{name}`", "", "```",
                              trunc(payload, 2000), "```", ""]
                else:
                    lines += ["### Tool", f"*(output, {ts})*", "", "```",
                              trunc(payload, 2000), "```", "", "---", ""]
        elif typ == "attachment":
            # A prompt queued while the assistant was busy, then removed from the queue
            # without ever being submitted, is still something the human asked for. It is
            # recoverable only from the raw JSONL, and it is real Expectation evidence.
            att = r.get("attachment") or {}
            prompt = att.get("prompt")
            if (att.get("type") == "queued_command"
                    and (att.get("origin") or {}).get("kind") == "human"
                    and prompt and prompt not in normal_user_texts):
                lines += ["### User",
                          f"*({att.get('timestamp') or ts})* _(queued while the assistant was "
                          f"busy; later removed from the queue without being submitted as a "
                          f"normal turn — recovered from the raw session JSONL)_",
                          "", trunc(prompt), "", "---", ""]

    write_redacted(os.path.join(P["sources"], f"{stem}.json"),
                   json.dumps(records, indent=2, ensure_ascii=False))
    write_redacted(os.path.join(P["sources"], f"{stem}.md"), "\n".join(lines) + "\n")
    write_sidecar(stem, c, "exact" if records else "file-derived")
    return [f"{stem}.md", f"{stem}.json"]


def convert_claude_desktop(c, stem) -> list:
    """Metadata-only, deliberately. The desktop app's local_*.json holds session-level
    metadata, never turn content. Render exactly what is real — and say plainly when this
    file is the only surviving record of a session whose transcript is gone."""
    d = json.load(open(c["native_path"], encoding="utf-8"))
    cli_id = d.get("cliSessionId")
    has_cli = claude_cli_transcript_exists(cli_id)

    lines = [f"<!-- Rendered from Claude Desktop session-index metadata — "
             f"{c['native_path']} -->", f"# {stem}", "",
             f"- **Session ID:** {c['session_id']}",
             f"- **Linked CLI session ID:** {cli_id}",
             f"- **cwd:** {d.get('cwd')}", f"- **Title:** {d.get('title')}",
             f"- **Created:** {d.get('createdAt')}  ·  "
             f"**Last activity:** {d.get('lastActivityAt')}", ""]
    if has_cli:
        lines.append(f"The linked Claude Code CLI transcript for session `{cli_id}` is also "
                     f"present on this machine and captured separately. This file exists only "
                     f"as the desktop app's own metadata record, not a duplicate transcript.")
    else:
        lines.append("**No Claude Code CLI transcript exists for the linked session ID on this "
                     "machine.** This metadata file is the only surviving record that this "
                     "session happened — turns and tool calls are not recoverable from it.")

    write_redacted(os.path.join(P["sources"], f"{stem}.json"),
                   json.dumps(d, indent=2, ensure_ascii=False))
    write_redacted(os.path.join(P["sources"], f"{stem}.md"), "\n".join(lines) + "\n")
    write_sidecar(stem, c, "exact" if d.get("createdAt") else "unknown")
    return [f"{stem}.md", f"{stem}.json"]


CONVERTERS = {
    "cursor": convert_cursor_inrepo,
    "codex": convert_codex,
    "claude-code": convert_claude_code,
    "claude-desktop": convert_claude_desktop,
}


def slug_for(c) -> str:
    date = (c.get("timestamp") or _now_iso())[:10]
    sid = c["session_id"] or "unknown"
    short = re.sub(r"[^a-z0-9]+", "-", str(sid).lower()).strip("-")[:24]
    return f"{date}_{c['tool']}_{short}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--real", action="store_true",
                    help="convert, redact, and file any newly found sessions")
    args = ap.parse_args()

    if not MATCH_ROOTS:
        print("No match roots configured — check governance/config.json.")
        return 1
    print(f"Match roots: {', '.join(MATCH_ROOTS)}")

    ledger = load_ledger()
    all_found = (scan_codex() + scan_claude_code() + scan_kimi()
                 + scan_cursor_inrepo() + scan_claude_desktop())
    new = [c for c in all_found if not already_known(ledger, c["tool"], c["session_id"])]

    print(f"Scanned: {len(all_found)} matching sessions across "
          f"codex / claude-code / kimi / cursor(in-repo) / claude-desktop")
    print(f"Already known: {len(all_found) - len(new)} | New: {len(new)}")

    os.makedirs(P["sources"], exist_ok=True)
    for c in new:
        print(f"  NEW  [{c['tool']}]  {c['session_id']}  ({c.get('native_path')})")
        if c["tool"] == "kimi":
            print("       -> detected only; the Kimi converter is not implemented "
                  "(format unverified) — handle manually")
            continue
        if not args.real:
            continue
        stem = slug_for(c)
        files = CONVERTERS[c["tool"]](c, stem)
        ledger["ingested"].append({
            "session_id": c["session_id"], "tool": c["tool"],
            "native_path": c["native_path"], "sources_files": files,
            "captured_at": _now_iso(),
        })
        print(f"       -> captured: {files}")

    if new and args.real:
        save_ledger(ledger)
        print("Ledger updated.")
    elif new:
        print("Dry-run only — pass --real to convert and file these.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
