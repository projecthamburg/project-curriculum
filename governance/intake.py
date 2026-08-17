#!/usr/bin/env python3
"""governance/intake.py — probe what evidence exists, ask for what cannot be probed,
and determine the pathway before a single file is written.

Two halves, and the split is the point:

  SEES     Everything determinable by looking. Parent contents, language mix, git history,
           Tier 1 sessions on this machine matching the parent, and any Tier 2/3 exports in
           a directory you point at. Never asked, because asking a human to report what the
           filesystem already knows produces wrong answers.

  REQUESTS Only what looking cannot answer. The objective above all — it cannot be probed,
           cannot be defaulted, and the run stops without it. Then where exports live, if
           the probe found none where it looked.

It ends with a **capability declaration**: which pathway this project is on, which evidence
tiers are present, and — stated plainly — what this curriculum will therefore NOT be able to
claim. That last part is the output that matters. A curriculum that quietly lacks an intent
record and does not say so is the failure this whole protocol exists to prevent.

Nothing is written except the intake record itself. Feed it to new_project.py.

Usage:
    python3 governance/intake.py --parent ../my-app                      # interactive
    python3 governance/intake.py --parent ../my-app --exports ~/Downloads/chats
    python3 governance/intake.py --parent ../my-app --objective "..." --non-interactive
    python3 governance/intake.py --parent ../my-app --objective "..." --json
"""
from __future__ import annotations
import argparse
import datetime
import glob
import json
import os
import subprocess
import sys

from pc_config import paths

P = paths()
HOME = os.path.expanduser("~")

CODE_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".rb", ".php",
            ".c", ".h", ".cpp", ".cs", ".swift", ".kt", ".sh", ".sql", ".scala"}
DOC_EXT = {".md", ".rst", ".txt", ".adoc"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
             ".next", "target", "vendor"}


# ────────────────────────────────────────────────────────────────── SEES ──────

def probe_parent(parent: str) -> dict:
    code = docs = other = 0
    langs, doc_names = set(), []
    for dirpath, dirnames, filenames in os.walk(parent):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in CODE_EXT:
                code += 1
                langs.add(ext.lstrip("."))
            elif ext in DOC_EXT:
                docs += 1
                if len(doc_names) < 6:
                    doc_names.append(os.path.relpath(os.path.join(dirpath, fn), parent))
            else:
                other += 1
    return {"code_files": code, "doc_files": docs, "other_files": other,
            "languages": sorted(langs), "doc_examples": doc_names}


def probe_git(parent: str) -> dict:
    def run(*a):
        try:
            return subprocess.run(["git", "-C", parent, *a], capture_output=True,
                                  text=True, check=True).stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""
    if not os.path.isdir(os.path.join(parent, ".git")):
        return {"is_repo": False}
    count = run("rev-list", "--count", "HEAD")
    return {"is_repo": True,
            "commits": int(count) if count.isdigit() else 0,
            "first": run("log", "--reverse", "--format=%ad", "--date=short", "-1"),
            "last": run("log", "-1", "--format=%ad", "--date=short"),
            "head": run("rev-parse", "HEAD")[:12],
            "remote": run("config", "--get", "remote.origin.url")}


def probe_tier1(parent: str) -> dict:
    """Sessions on THIS machine whose own recorded working directory is the parent. Identity
    matching only — a text grep for the project's name is not a substitute and never has been."""
    found = {}
    enc = parent.replace("/", "-").replace("_", "-")
    base = os.path.join(HOME, ".claude", "projects")
    if os.path.isdir(base):
        n = sum(len(glob.glob(os.path.join(base, d, "*.jsonl")))
                for d in os.listdir(base) if d == enc or d.startswith(enc + "-"))
        if n:
            found["claude-code"] = n
    n = 0
    for p in glob.glob(os.path.join(HOME, ".codex", "sessions", "**", "*.jsonl"),
                       recursive=True):
        try:
            with open(p, encoding="utf-8") as f:
                first = json.loads(f.readline())
            cwd = (first.get("payload") or {}).get("cwd") or ""
            if cwd == parent or cwd.startswith(parent + "/"):
                n += 1
        except Exception:
            continue
    if n:
        found["codex"] = n
    ki = os.path.join(HOME, ".kimi-code", "session_index.jsonl")
    if os.path.exists(ki):
        n = 0
        for line in open(ki, encoding="utf-8"):
            try:
                wd = json.loads(line).get("workDir") or ""
            except Exception:
                continue
            if wd == parent or wd.startswith(parent + "/"):
                n += 1
        if n:
            found["kimi"] = n
    n = len(glob.glob(os.path.join(parent, ".specstory", "history", "*.md")))
    if n:
        found["cursor-specstory"] = n
    base = os.path.join(HOME, "Library", "Application Support", "Claude",
                        "claude-code-sessions")
    if os.path.isdir(base):
        n = 0
        for p in glob.glob(os.path.join(base, "**", "local_*.json"), recursive=True):
            try:
                d = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            cwd = d.get("cwd") or d.get("originCwd") or ""
            if cwd == parent or cwd.startswith(parent + "/"):
                n += 1
        if n:
            found["claude-desktop"] = n
    # In-repo committed transcripts — how a public example ships its evidence.
    inrepo = [os.path.relpath(p, parent) for p in
              glob.glob(os.path.join(parent, "**", "transcript*.md"), recursive=True)]
    return {"providers": found, "total": sum(found.values()), "in_repo_transcripts": inrepo}


def probe_exports(d: str) -> dict:
    """Tier 2 vs Tier 3 by structure, not by filename. Two voices is a conversation; one
    voice is a note, and a note cannot carry an Expectation."""
    sys.path.insert(0, P["gov"])
    from import_chat_logs import parse_turns, detect_provider
    t2, t3, unparsed = [], [], []
    files = []
    for ext in ("md", "txt"):
        files += glob.glob(os.path.join(d, "**", f"*.{ext}"), recursive=True)
    for f in sorted(files):
        try:
            text = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if not text.strip():
            continue
        turns, fmt = parse_turns(text)
        rel = os.path.relpath(f, d)
        speakers = {t["speaker"] for t in turns}
        if fmt == "unparsed":
            unparsed.append(rel)
            t3.append(rel)
        elif speakers >= {"user", "assistant"}:
            t2.append({"file": rel, "provider": detect_provider(text, rel),
                       "format": fmt, "turns": len(turns)})
        else:
            t3.append(rel)
    return {"dir": d, "tier2": t2, "tier3": t3, "unparsed": unparsed,
            "scanned": len(files)}


# ─────────────────────────────────────────────────────────────── REQUESTS ─────

QUESTIONNAIRE = [
    # (section, key, prompt, options, default, required)
    ("1 runtime", "agent", "Which agent runs this",
     "claude-code|codex|jules|cursor|antigravity|kimi|hermes|openclaw|other|none", "claude-code", True),
    ("1 runtime", "location", "Where does it run",
     "this-machine|remote-container|ci|ssh", "this-machine", True),
    ("1 runtime", "ssh_host", "  SSH host and how it is reached", "", "", False),

    ("2 parent", "parent_access", "Parent reachability",
     "local|git-url|needs-upload", "local", True),
    ("2 parent", "visibility", "Parent visibility", "public|private", "public", True),
    ("2 parent", "access_grant", "  If private, how is access granted",
     "already-cloned|ssh-key|token|github-app|permission-needed", "already-cloned", False),
    ("2 parent", "pinned_ref", "Pin to which ref (commit/tag/branch)", "", "", False),
    ("2 parent", "scope", "Scope — whole repo, or subtrees", "", "whole-repo", False),
    ("2 parent", "extra_repos", "Additional repositories, if any", "", "", False),

    ("3 chat sources", "t1_tools", "Tier 1 — which agent tools produced sessions",
     "claude-code,codex,cursor,kimi,jules,antigravity,desktop,none", "", False),
    ("3 chat sources", "t1_where", "  Where are they",
     "native-store|in-repo-specstory|specstory-api|exported-files|other-machine|none",
     "native-store", False),
    ("3 chat sources", "specstory_endpoint", "  SpecStory API endpoint + project id, if used",
     "", "", False),
    ("3 chat sources", "t2_products", "Tier 2 — which LLM products were used",
     "chatgpt,claude-ai,gemini,kimi,openrouter,self-hosted,none", "", False),
    ("3 chat sources", "t2_where", "  Where are the exports",
     "local-dir|need-exporting|uploaded|private-repo|public-repo|api|none", "local-dir", False),
    ("3 chat sources", "t3_where", "Tier 3 — notes, screenshots, scratch files",
     "local-dir|uploaded|in-repo|none", "none", False),
    ("3 chat sources", "unreachable", "Any source NOT reachable from the chosen runtime",
     "", "", False),

    ("4 code + docs", "code_where", "Where is the code",
     "parent|additional-repos|needs-upload", "parent", True),
    ("4 code + docs", "docs_where", "Where is the documentation",
     "in-repo|separate-repo|external-site|none", "in-repo", False),
    ("4 code + docs", "docs_url", "  External docs URL and access, if any", "", "", False),
    ("4 code + docs", "excluded_paths", "Paths to exclude (vendored, generated, build output)",
     "", "", False),

    ("5 validation", "external_validator", "Is an external validator available",
     "yes|no", "no", True),
    ("5 validation", "validator_reach", "  If yes, who and how reached", "", "", False),
    ("5 validation", "panel", "If no external validator, use an adversarial agent panel",
     "yes|no", "no", False),
    ("5 validation", "panel_config", "  Panel size, lenses, models", "", "", False),

    ("6 adjacent", "supervisor", "Is there a supervisor-adjacent agent",
     "yes|no", "no", False),
    ("6 adjacent", "supervisor_where", "  Where it lives and what it owns", "", "", False),
    ("6 adjacent", "mcp_tools", "MCP tools to attach (names)", "", "", False),
    ("6 adjacent", "excluded_tools", "Anything deliberately excluded, and why", "", "", False),

    ("7 boundaries", "redistribution", "May captured evidence be committed",
     "reference-only|committable", "reference-only", True),
    ("7 boundaries", "cadence", "Cadence", "one-shot|on-push|scheduled", "one-shot", False),
]

# Answers that change what the run can do at all.
RUNTIME_BLIND = {"remote-container", "ci"}


def wiring_findings(a: dict) -> list:
    """Consequences of the answers, stated as limits rather than left implied."""
    out = []
    if a.get("agent") == "none":
        out.append("No agent: indexes, sweeps and all nine gates run; ICE authoring, objective "
                   "translation, course and thesis generation do not. The workspace is prepared "
                   "and the judgment work is held for an author.")
    if a.get("location") in RUNTIME_BLIND:
        out.append(f"Runtime is `{a['location']}`: no native session store exists here, so Tier 1 "
                   f"capture is impossible regardless of what sessions exist elsewhere. Only "
                   f"committed or uploaded evidence is reachable.")
    if a.get("location") == "ssh":
        out.append("Runtime is over SSH: the REMOTE box's session stores are reachable, the "
                   "local machine's are not. Say which set the evidence is in.")
    if a.get("access_grant") == "permission-needed":
        out.append("BLOCKING — parent access is not yet granted. A curriculum seeded from a "
                   "partial clone under-reports silently. Resolve access before seeding.")
    if not a.get("pinned_ref"):
        out.append("No pinned ref: this profile will not be reproducible. A later run may read a "
                   "different tree and reach different conclusions.")
    if a.get("t2_where") == "need-exporting":
        out.append("Tier 2 exports do not exist yet. No programmatic reader exists for any of "
                   "these products, so this pauses the run rather than failing it.")
    if a.get("unreachable"):
        out.append(f"Declared-but-unreachable: {a['unreachable']}. Named in the record, absent "
                   f"from the index, and excluded from every claim.")
    if a.get("external_validator") != "yes":
        out.append("No external validator. A panel, if used, is the weaker substitute — agents "
                   "from one family share priors, which is what an external validator breaks. "
                   "The curriculum records that no external validation occurred.")
    if a.get("t3_where") not in (None, "", "none"):
        out.append("Tier 3 present: carries Ideas and Concerns, and NEVER a negotiated "
                   "Expectation. Encoded Expectations still come from the artifact.")
    if not a.get("excluded_paths"):
        out.append("No exclusions given. A codebase index that swallows vendored or generated "
                   "code produces a curriculum about someone else's library.")
    return out


def run_questionnaire(interactive: bool, preset: dict) -> dict:
    """Fixed order, because each section narrows the next. Section 1 first: asking where the
    chat logs are before knowing whether this runs on a laptop or in CI wastes the answer."""
    answers, section = dict(preset), None
    for sec, key, prompt, options, default, required in QUESTIONNAIRE:
        if key in answers:
            continue
        if not interactive:
            answers[key] = default
            continue
        if sec != section:
            section = sec
            print(f"\n  ── {sec} ──")
        opt = f"  ({options})" if options else ""
        answers[key] = ask(f"  {prompt}{opt}", default or None, required)
    return answers


def ask(prompt, default=None, required=False):
    suffix = f" [{default}]" if default else ""
    while True:
        try:
            v = input(f"{prompt}{suffix}: ").strip()
        except EOFError:
            v = ""
        if v:
            return v
        if default is not None:
            return default
        if not required:
            return ""
        print("  Required — this one cannot be defaulted.")


# ───────────────────────────────────────────────────────── DETERMINATION ──────

def determine(tier1, exports) -> dict:
    """Pathway is decided by whether an intent RECORD exists, and the capability list is
    decided by which tiers back it. Tier 3 alone does not make Pathway A: a monologue has an
    Ask and no Response, so no commitment can be traced from it."""
    has_t1 = tier1["total"] > 0 or bool(tier1["in_repo_transcripts"])
    has_t2 = bool(exports and exports["tier2"])
    has_t3 = bool(exports and exports["tier3"])
    pathway = "A" if (has_t1 or has_t2) else "B"

    enabled, disabled = [], []
    if has_t1:
        enabled.append("Commitment tracing to a specific edit — Tier 1 records tool calls")
    else:
        disabled.append("Commitment tracing to a specific edit — no Tier 1 session evidence; "
                        "a commitment can be found but not followed into the code by session")
    if has_t1 or has_t2:
        enabled.append("NEGOTIATED Expectations — Ask → Response → Lock-in chains, and therefore "
                       "intent-fidelity courses")
    else:
        disabled.append("NEGOTIATED Expectations — no two-voice evidence exists, so no Ask → "
                        "Response → Lock-in chain can be established and no intent-fidelity "
                        "course can be generated")
    # Encoded Expectations come from the artifact, not from any source tier, so they are
    # available on every pathway. Omitting them was the error corrected 2026-08-17.
    enabled.append("ENCODED Expectations — what the code, config, tests and docs state about "
                   "themselves, judged honoured / violated / untested / contradicted")
    if has_t3:
        enabled.append("Ideas and Concerns from human-side material (Tier 3)")
        disabled.append("NEGOTIATED Expectations from Tier 3 — a monologue has an Ask and no "
                        "Response; manufacturing one fabricates the other party. Encoded "
                        "Expectations are unaffected: they come from the artifact")
    if pathway == "B":
        disabled.append("Any claim about WHY the code is as it is. Comments, commit messages "
                        "and READMEs are evidence of what was believed at writing time, not a "
                        "record of what was asked for")
    # Absence of a tier is a limit even when the pathway is otherwise complete. A project
    # with Tier 1 only still has holes, and printing an empty limits list would read as
    # "no limitations" — the exact silent overclaim this protocol exists to prevent.
    if not has_t2:
        disabled.append("Pre-repository intent history — no Tier 2 conversation logs. A "
                        "project usually exists in conversation before its first commit, and "
                        "that period is invisible here")
    if not has_t3:
        disabled.append("Human-side material — no Tier 3 notes, sketches or screenshots. What "
                        "was thought but never said to an agent is not recoverable")
    enabled.append("Structural and behavioural courses from the codebase index")
    return {"pathway": pathway,
            "tiers_present": [t for t, present in
                              (("1", has_t1), ("2", has_t2), ("3", has_t3)) if present],
            "enabled": enabled, "disabled": disabled}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parent", required=True)
    ap.add_argument("--exports", default=None,
                    help="directory of exported chat logs / notes to probe")
    ap.add_argument("--objective", default=None)
    ap.add_argument("--non-interactive", action="store_true",
                    help="ask nothing; take every questionnaire default (for CI)")
    ap.add_argument("--answers", default=None,
                    help="JSON file of questionnaire answers, to skip asking")
    ap.add_argument("--skip-questionnaire", action="store_true",
                    help="probe and determine the pathway only")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default=None, help="write the intake record here")
    args = ap.parse_args()

    parent = os.path.abspath(os.path.expanduser(args.parent))
    if not os.path.isdir(parent):
        print(f"No such parent project: {parent}")
        return 1

    # ── SEES ──
    contents = probe_parent(parent)
    git = probe_git(parent)
    tier1 = probe_tier1(parent)
    exports = probe_exports(os.path.abspath(os.path.expanduser(args.exports))) \
        if args.exports else None

    if not args.json:
        print(f"\n═══ PROBED — determined by looking, not asked ═══\n")
        print(f"  Parent            {parent}")
        print(f"  Contents          {contents['code_files']} code, {contents['doc_files']} docs"
              f"{', ' + ', '.join(contents['languages']) if contents['languages'] else ''}")
        if git["is_repo"]:
            print(f"  Git               {git['commits']} commits, "
                  f"{git['first']} → {git['last']}, HEAD {git['head']}")
            if git["remote"]:
                print(f"  Remote            {git['remote']}")
        else:
            print("  Git               not a repository")
        if tier1["providers"]:
            print(f"  Tier 1 sessions   " + ", ".join(
                f"{k} {v}" for k, v in sorted(tier1["providers"].items())))
        else:
            print("  Tier 1 sessions   none on this machine matching this parent")
        if tier1["in_repo_transcripts"]:
            print(f"  In-repo transcript {', '.join(tier1['in_repo_transcripts'][:3])}")
        if exports:
            print(f"  Exports scanned   {exports['scanned']} files in {exports['dir']}")
            print(f"    Tier 2 (two voices)  {len(exports['tier2'])}")
            for e in exports["tier2"][:4]:
                print(f"      {e['file']}  [{e['provider']}/{e['format']}, {e['turns']} turns]")
            print(f"    Tier 3 (one voice)   {len(exports['tier3'])}")
            if exports["unparsed"]:
                print(f"      of which unrecognized structure: {len(exports['unparsed'])}")
        else:
            print("  Exports           not probed — pass --exports <dir> if you have any")

    # ── REQUESTS ──
    objective = args.objective
    if not objective and not args.non_interactive:
        print(f"\n═══ ASKED — only what probing cannot answer ═══\n")
        if not exports:
            d = ask("  Directory of exported chat logs or notes, if any (blank to skip)")
            if d and os.path.isdir(os.path.expanduser(d)):
                exports = probe_exports(os.path.abspath(os.path.expanduser(d)))
                print(f"    -> Tier 2: {len(exports['tier2'])}, Tier 3: {len(exports['tier3'])}")
            elif d:
                print("    -> no such directory; skipped")
        objective = ask("\n  The objective this curriculum must serve", required=True)
    if not objective:
        print("\nRefusing to proceed: an objective is required and cannot be probed or "
              "defaulted. A curriculum cannot be seeded without one — there is nothing to "
              "seed it for.")
        return 1

    preset = json.load(open(args.answers, encoding="utf-8")) if args.answers else {}
    answers, wiring = {}, []
    if not args.skip_questionnaire:
        if not args.json and not args.non_interactive:
            print("\n═══ WIRING — who does this work, what can they reach ═══")
        answers = run_questionnaire(not args.non_interactive and not args.json, preset)
        wiring = wiring_findings(answers)

    verdict = determine(tier1, exports)
    record = {
        "probed_at": datetime.datetime.now(datetime.timezone.utc)
                             .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "parent": parent, "objective": objective.strip(),
        "contents": contents, "git": git, "tier1": tier1,
        "exports": exports, "wiring": answers, "wiring_findings": wiring,
        "determination": verdict,
    }

    if any(w.startswith("BLOCKING") for w in wiring):
        out = args.out or os.path.join(P["gov"], "reports",
                                       f"intake_{os.path.basename(parent)}.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
        print("\n  ⛔ BLOCKED — nothing further should be created until this is resolved:")
        for w in wiring:
            if w.startswith("BLOCKING"):
                print(f"     {w[len('BLOCKING — '):]}")
        print(f"\n  Intake record: {out}")
        return 2

    if args.json:
        print(json.dumps(record, indent=2))
    else:
        print(f"\n═══ DETERMINATION ═══\n")
        print(f"  Pathway           {verdict['pathway']}"
              f"  ({'ICE + codebase' if verdict['pathway'] == 'A' else 'codebase only'})")
        print(f"  Tiers present     {', '.join(verdict['tiers_present']) or 'none'}")
        print("\n  This curriculum WILL be able to:")
        for e in verdict["enabled"]:
            print(f"    ✓ {e}")
        if wiring:
            print("\n  Consequences of the wiring — stated, not implied:")
            for w in wiring:
                mark = "⛔" if w.startswith("BLOCKING") else "•"
                print(f"    {mark} {w}")
        print("\n  This curriculum will NOT be able to:")
        for d in verdict["disabled"]:
            print(f"    ✗ {d}")
        if not verdict["disabled"]:
            print("    (nothing — all three tiers present. Rare; check the probe is right "
                  "before trusting it.)")
        if verdict["pathway"] == "B":
            print("\n  Pathway B is not a lesser pathway — almost no repository has its\n"
                  "  conversation history. But the curriculum must DECLARE that no intent\n"
                  "  record exists rather than infer intent from the artifact. Gate G9\n"
                  "  enforces that declaration.")
        print(f"\n  Next:  python3 governance/new_project.py --parent {parent} \\\n"
              f"           --objective \"{objective.strip()[:60]}...\"")

    out = args.out or os.path.join(P["gov"], "reports",
                                   f"intake_{os.path.basename(parent)}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    if not args.json:
        print(f"\n  Intake record: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
