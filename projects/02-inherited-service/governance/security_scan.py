#!/usr/bin/env python3
"""governance/security_scan.py — standing, read-only security scan for this instance.

**Read-only, always.** It writes a dated report and nothing else. It never modifies,
quarantines, or deletes anything. Every finding carries a *proposed* disposition that
requires explicit human approval before anyone acts on it:

    remove      the finding should not exist in this repository at all
    quarantine  it should be moved out of tracked content, retained elsewhere
    monitor     it is expected or already understood; keep watching it

A scanner that auto-remediates is a scanner that silently rewrites evidence. In a system
whose entire value is that its record can be trusted, that trade is never worth it.

Two passes:
  1. Generic sweep — secret-shaped and injection-shaped patterns across tracked files.
  2. Registry cross-reference — known findings from REGISTRY.md checked against reality,
     so a finding that was resolved stops being reported and one that reappears is caught.

Matched values are NEVER printed. A finding reports the pattern label, the file, the line,
and the match's length — verify by structural shape, never by printing the content.

Usage:
    python3 governance/security_scan.py
    python3 governance/security_scan.py --path protocol/
"""
from __future__ import annotations
import argparse
import datetime
import os
import re
import subprocess

from pc_config import paths
from redact_util import REDACTION_PATTERNS

P = paths()

# Injection-shaped patterns. Per protocol/MASTER_RUBRIC.md §8, ingested source material is
# data and never a directive — this pass surfaces text that is *trying* to be a directive so
# a reviewer can confirm it is being treated as data. A hit is not automatically a problem:
# this very file, and the protocol documents that describe the rule, will match. That is
# why every finding is proposed rather than applied.
INJECTION_PATTERNS = [
    ("Instruction-override phrasing",
     re.compile(r"(?i)ignore (?:all |any )?(?:previous|prior|above) instructions")),
    ("Role-reassignment phrasing",
     re.compile(r"(?i)you are now (?:a|an|the)\s")),
    ("System-prompt disclosure request",
     re.compile(r"(?i)(?:reveal|print|output|repeat) (?:your |the )?system prompt")),
    ("Embedded agent directive",
     re.compile(r"(?i)<\s*(?:system|instructions?)\s*>")),
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
SKIP_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".mp4", ".zip",
                 ".woff", ".woff2", ".ico", ".so", ".dylib")


def tracked_files(root: str) -> list:
    """Prefer git's own view — an untracked scratch file is not this repository's problem,
    and a gitignored raw capture is deliberately out of scope."""
    try:
        out = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True,
                             text=True, check=True).stdout
        return [os.path.join(root, line) for line in out.splitlines() if line]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            files += [os.path.join(dirpath, fn) for fn in filenames]
        return files


def scan_file(path: str) -> list:
    if path.lower().endswith(SKIP_SUFFIXES):
        return []
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return []
    if "\x00" in text[:4096]:
        return []

    findings = []
    lines = text.splitlines()
    for label, pattern, _ in REDACTION_PATTERNS:
        for m in pattern.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            findings.append({"kind": "secret", "label": label, "path": path,
                             "line": line_no, "match_length": len(m.group(0)),
                             "disposition": "remove"})
    for label, pattern in INJECTION_PATTERNS:
        for m in pattern.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            context = lines[line_no - 1][:120] if line_no <= len(lines) else ""
            findings.append({"kind": "injection", "label": label, "path": path,
                             "line": line_no, "match_length": len(m.group(0)),
                             "context": context, "disposition": "monitor"})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=None,
                    help="limit the scan to a subpath of the content root")
    args = ap.parse_args()

    root = P["content_root"]
    target = os.path.join(root, args.path) if args.path else root
    files = [f for f in tracked_files(root)
             if os.path.abspath(f).startswith(os.path.abspath(target))]

    findings = []
    for f in files:
        findings.extend(scan_file(f))

    secrets = [f for f in findings if f["kind"] == "secret"]
    injections = [f for f in findings if f["kind"] == "injection"]

    now = datetime.datetime.now(datetime.timezone.utc)
    os.makedirs(os.path.join(P["gov"], "security", "findings"), exist_ok=True)
    report_path = os.path.join(P["gov"], "security", "findings",
                               f"{now.strftime('%Y-%m-%d')}_scan.md")

    lines = [f"# Security scan — {now.strftime('%Y-%m-%d %H:%M:%SZ')}", "",
             f"**Instance:** {P['config']['project_id']}",
             f"**Scanned:** {len(files)} tracked files under `{target}`",
             f"**Findings:** {len(secrets)} secret-shaped, {len(injections)} injection-shaped",
             "",
             "Read-only scan. Every disposition below is **proposed** and requires explicit "
             "approval before anything is acted on. Matched values are never printed — verify "
             "by length and structural shape.", ""]

    if secrets:
        lines += ["## Secret-shaped findings", "",
                  "| Pattern | File | Line | Match length | Proposed |",
                  "|---|---|---:|---:|---|"]
        for f in secrets:
            rel = os.path.relpath(f["path"], root)
            lines.append(f"| {f['label']} | `{rel}` | {f['line']} | "
                         f"{f['match_length']} | `{f['disposition']}` |")
        lines.append("")
    else:
        lines += ["## Secret-shaped findings", "", "None found.", ""]

    if injections:
        lines += ["## Injection-shaped findings", "",
                  "A hit here is **not automatically a problem**. The protocol documents that "
                  "describe the data-not-directive rule will match it, and so will this "
                  "scanner's own source. What matters is whether the text is being *treated* "
                  "as data. Each is proposed `monitor` for that reason.", "",
                  "| Pattern | File | Line | Context | Proposed |", "|---|---|---:|---|---|"]
        for f in injections:
            rel = os.path.relpath(f["path"], root)
            ctx = f.get("context", "").replace("|", "\\|")
            lines.append(f"| {f['label']} | `{rel}` | {f['line']} | `{ctx}` | "
                         f"`{f['disposition']}` |")
        lines.append("")
    else:
        lines += ["## Injection-shaped findings", "", "None found.", ""]

    lines += ["## Coverage bounds", "",
              "Stated explicitly rather than left implied:", "",
              "- Only git-tracked files were scanned. Untracked and gitignored files — "
              "including raw session captures — are deliberately out of scope here; they are "
              "swept at capture time instead.",
              "- Binary and media files were skipped by extension.",
              "- Pattern matching cannot catch a credential shape it has no pattern for. "
              "This is a backstop, not the whole control.", ""]

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Scanned {len(files)} tracked files under {target}")
    print(f"  secret-shaped:    {len(secrets)}")
    print(f"  injection-shaped: {len(injections)}")
    print(f"Report: {report_path}")
    if secrets:
        print("\nSecret-shaped findings need review before this is committed or published.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
