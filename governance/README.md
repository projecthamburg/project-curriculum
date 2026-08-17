# governance/ — the runnable layer

This folder is two things at once:

1. **This repository's own governance layer** — its search index, its ICE domain, its
   concerns log, its security scan.
2. **The reference copy** that `new_project.py` clones into every project you create.

Every script here reads its roots from `config.json` via `pc_config.py`, so a copied folder
works **unmodified** — only its own `config.json` differs. That is a deliberate improvement
over hand-editing a path constant in five scripts per project: the copies stay
byte-identical, so fixing one fixes all, while each instance stays fully self-contained with
no shared runtime dependency and no network.

**Do not centralize the per-project layers to remove the duplication. The duplication is the
point** — it is what lets someone fork this and run it with none of the original
infrastructure.

---

## The cycle

```bash
python3 governance/update.py --real          # capture sessions, rebuild the index
python3 governance/ice_chapter.py status      # what is awaiting review
python3 governance/ice_chapter.py new --label founding-session
python3 governance/query.py "some question"
```

Every script defaults to a dry run and needs `--real` to write anything.

## What each script does

| Script | Role |
|---|---|
| `pc_config.py` | The one place roots are declared. Everything else reads from it. |
| `build_search_index.py` | Builds `search_index.json` — a **keyword/lexical** index. No embeddings, no live search. |
| `query.py` | Searches it. `--origin`, `--category`, `--speaker`, `--json`. |
| `discover_sessions.py` | Finds agent work sessions on this machine, matched by real cwd/workDir — **never a text grep**. Five providers. |
| `import_chat_logs.py` | Imports exported `.md`/`.txt` conversations — the path for every provider with no local store, and how a committed seed pack works in CI. |
| `ice_chapter.py` | Scaffolds ICE chapters and owns the **per-domain chapter watermark**. Scaffolds only; it does not author. |
| `security_scan.py` | Read-only sweep. Every finding is a **proposed** disposition needing approval. |
| `update.py` | Runs the mechanical half of the cycle and writes a dated report. |
| `reindex_all.py` | Runs this layer's cycle, then each project's own. |
| `new_project.py` | Intake for a new project. **Refuses without a stated objective.** |
| `redact_util.py` | Shared secret redaction. In-memory, before anything reaches disk. |

---

## Three things that are deliberate, not incidental

**The index is not a vector database.** It scores by keyword and path overlap. Saying so
plainly matters: a tool that sounds like a vector DB but isn't causes people to over-trust
its recall. It finds what has been written down and indexed — nothing else.

**`search_index.json` is gitignored.** It is fully rebuildable from the manifest and
`sources/`, and every rebuild rewrites the whole blob, so committing it means the repository
grows by the full index size on every commit.

**Capture is automated; review is not.** Discovering sessions, converting formats, filing
them and diffing against the ledger all run unattended. Authoring a chapter — deciding what
was asked, what was agreed, what was superseded — stays deliberate. See `protocol/ICE.md`.

---

## Evidence handling

`sources/` holds captures. Each gets three files:

| File | What it is |
|---|---|
| `<stem>.md` | Human-readable rendering, **derived**. Speaker-marked so the index chunks by turn. |
| `<stem>.json` | Structured turns, **derived**. |
| `<stem>.meta.json` | Sidecar: category, provider, association confidence, timestamp confidence, capture time. |

The native original is **evidence and is never edited**. Raw session dumps stay out of git
(see `.gitignore`) — the true original already lives outside this repository, and a raw
capture from a live session only grows.

Two confidences are always explicit, never inferred silently:

- **Timestamp** — `exact` · `inferred` · `file-derived` · `unknown`
- **Association** — `explicit` (a human said so) · `path` (the session's own cwd) ·
  `candidate` (content suggests it)

**A candidate association is proposed, never adopted.** Uncertain evidence is not silently
made canonical.

Everything captured is swept for secrets **in memory, before it reaches disk**. Matched
values are never printed — only pattern labels and counts. Verify a flagged match by its
length and structural shape.

---

## Status

Working and runnable. Not yet built: the CI validators that enforce the protocol contracts
(prerequisite DAG, traceability completeness, the meta-rubric, criterion lint, citation
resolution), and the seeding run itself. See `docs/UNDERSTANDING.md` for where those sit.
