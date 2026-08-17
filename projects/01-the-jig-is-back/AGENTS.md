# 01-the-jig-is-back — project context for agents

**Parent project:** `/home/user/upstream-the-jig-is-back`
**Kind:** external
**Registered:** 2026-08-17 as project 01 in `governance/registry.json`

This file nests under the workspace root `AGENTS.md` — Codex, Jules and Kimi load both,
walking from the git root to the working directory. Everything in the root file still
applies here.

## Objective

Reconstruct the design intent, behavioural expectations, and implementation decisions behind the paper-plane hero animation and its in-page path editor, and determine whether the current code satisfies them — including the three defects the human reported and the one approach abandoned mid-build.

## What this folder is

The **governance and curriculum** for the parent project named above. The parent project's real content lives at `/home/user/upstream-the-jig-is-back` — a separate directory that this layer reads and **never writes to**. Governance lives here, not there.

- `governance/` — this project's own independent layer: its own search index, its own ICE
  domain, its own concerns log, its own security scan. No shared runtime dependency on the
  workspace or on any other project.
- `syllabus/` — the curriculum generated for the objective above: courses, the two
  dependency graphs, and the staleness ledger.

## Before searching files by hand

```
python3 governance/query.py "your question"
python3 governance/query.py "your question" --origin internal
python3 governance/query.py "what did I ask about X" --speaker user
```

Keyword index, not a vector database — no embeddings, no live search. Every result is
tagged `origin: internal` (this project's own material) or `origin: external` (borrowed
reference material). Check which before treating a result as this project's own work.

## The cycle

```
python3 governance/update.py --real       # capture sessions, rebuild the index
python3 governance/ice_chapter.py status   # what is awaiting review
python3 governance/ice_chapter.py new --label <name>
```

Capture is automated. **Review is not** — read the sources and author the chapter.
