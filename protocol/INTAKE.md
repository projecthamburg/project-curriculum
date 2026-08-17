# INTAKE — the questions asked before anything is written

**Status:** v0.1-draft · Project Curriculum Protocol
**Implemented by:** `governance/intake.py`

When someone clones this and points it at a project, the agent asks a fixed set of questions in
a fixed order, records the answers, and links them to what it found by looking. The output is a
**wiring record**: who is doing the work, what they can reach, where every source lives, how it
gets there, and who validates the result.

Two standing rules govern the whole set:

1. **Never ask what can be probed.** Asking a human to report what the filesystem already knows
   produces wrong answers. Everything determinable by looking is looked at first.
2. **Order matters.** Each section narrows the next. Asking where the chat logs are before
   knowing whether the run happens on the laptop or in CI wastes the answer, because the same
   logs are reachable in one and invisible in the other.

---

## Section 1 — Runtime: who is doing this work, and where

**Asked first, because it determines what is reachable at all.**

| # | Question | Options |
|---|---|---|
| 1.1 | Which agent runs this? | Claude Code · Codex · Jules · Cursor · Antigravity · Kimi · Hermes · OpenClaw · other · **none (algorithmic only)** |
| 1.2 | Where does it run? | this machine · remote container (Claude Code on the web, Jules) · CI (GitHub Actions) · over SSH to another box |
| 1.3 | If SSH: which host, and reachable how? | host + credential mechanism |

**What 1.2 determines, and it is the single most consequential answer in the questionnaire:**

| Runtime | Native session stores reachable? |
|---|---|
| This machine | **Yes** — `~/.claude`, `~/.codex`, `~/.kimi-code`, desktop app stores |
| Remote container | **No.** A fresh container has none of them |
| CI | **No**, and no home directory worth scanning |
| SSH | Only the *remote* box's stores, not the local ones |

A run in CI or a cloud container can only see evidence that was **committed or uploaded**. That
is not a limitation to work around; it is the reason `import_chat_logs.py` exists as a
first-class path rather than a convenience.

### 1.1 = none — the algorithmic path

No agent, no model calls. Everything deterministic still runs:

| Runs | Does not run |
|---|---|
| Chat-log import from committed evidence | ICE chapter authoring |
| Both indexes | Part A objective translation |
| Secret sweep and security scan | Course and thesis generation |
| All nine contract gates | Any conformance judgment |
| The capability declaration | |

The output is a fully prepared workspace plus **a list of what awaits an author**. That is a
real deliverable — a fork can run it on every push, keep its indexes current, and hold the
judgment work for whenever an agent or a human arrives.

---

## Section 2 — The parent project

| # | Question | Notes |
|---|---|---|
| 2.1 | Where is the parent? | local path · git URL · **needs uploading** (not reachable from the runtime) |
| 2.2 | Public or private? | decides 2.3 and the redistribution question in §7 |
| 2.3 | If private, how is access granted? | already cloned locally · SSH key · token/PAT · GitHub App installed · **permission still needed from the owner** |
| 2.4 | Pin to a ref? | commit · tag · branch. **A profile without a pinned ref is not reproducible** |
| 2.5 | Scope | whole repository, or named subtrees; paths excluded |
| 2.6 | More than one repository? | a service plus its client, a repo plus a separate docs repo, a monorepo subdirectory |

**2.3 answered "permission still needed" stops the run** and produces the access request instead
of a half-built project. A curriculum seeded from a partial clone silently under-reports.

---

## Section 3 — Chat-log and conversation sources

Asked **per tier**, because each tier is reachable differently. Every question has the same
shape: *does it exist, where does it live, how do we get to it, and does it need uploading?*

### 3.1 Tier 1 — agent work sessions

| Question | Options |
|---|---|
| Which tools produced sessions for this project? | Claude Code · Codex · Cursor · Kimi · Jules · Antigravity · desktop apps · none |
| For each, where are they? | native store on the runtime machine · in-repo `.specstory/history/` · **SpecStory cloud or API** (endpoint + credential + project identifier) · already exported to files · on a different machine |
| If on a different machine | can it be reached, or must the sessions be exported and uploaded? |

### 3.2 Tier 2 — LLM conversation logs

| Question | Options |
|---|---|
| Which products were used? | ChatGPT · Claude.ai · Gemini / AI Studio · Kimi · OpenRouter · self-hosted · none |
| Where are the exports? | local directory · **need exporting first** · uploaded · in a private repo (needs permission) · in a public repo (needs path + ref) · behind an API (endpoint + credential) |

**None of these has a programmatic reader.** Manual export is the only workflow, so "need
exporting first" is a common and legitimate answer that pauses the run rather than failing it.

### 3.3 Tier 3 — human-side material

| Question | Options |
|---|---|
| Notes, scratch files, screenshots, voice transcripts? | local directory · uploaded · in the repo · none |
| Anything not text? | screenshots and images need a transcription pass before indexing; say so rather than silently skipping them |

### 3.4 Reachability, asked once across all three

> For every source named above that is **not reachable from the runtime chosen in §1**: does it
> need uploading, and to where?

This is the question that makes a CI or cloud run honest. A source named but unreachable is
recorded as **declared-but-unreachable**, and the capability declaration says so.

---

## Section 4 — Codebase and documentation sources

**Deliberately the same shape as §3.** Code and docs are sources with the same reachability
problem as conversations, and asking about them differently is how a repo-centric tool ends up
assuming the code is always local and the conversations never are.

| # | Question | Options |
|---|---|---|
| 4.1 | Where is the code? | the parent from §2 · additional repositories · needs uploading |
| 4.2 | Where is the documentation? | in the repo · a separate docs repository · an external wiki, site or knowledge base (URL + access) · none |
| 4.3 | External docs reachable from the runtime? | if not: export, or reference-only |
| 4.4 | What is excluded? | vendored dependencies, generated code, build output, fixtures |

**4.4 matters more than it looks.** A codebase index that swallows `node_modules` or generated
clients produces a curriculum about someone else's library.

---

## Section 5 — Validation

Three layers, per `VALIDATION.md`. This section decides which are available.

| # | Question | Options |
|---|---|---|
| 5.1 | Is an external validator available? | yes — who, and how is it reached · no |
| 5.2 | If no, use an agent panel? | yes — how many members, which lenses, which models · no |
| 5.3 | Confirm gates-only? | the mechanical baseline, always available, no secrets, no model calls |

**A panel is the documented weaker substitute for an external validator**, not an equivalent —
agents from one family share priors, and a shared prior is what an external validator exists to
break. If 5.1 is "no", the curriculum records that no external validation occurred. That is a
finding about its standing, not a blank.

---

## Section 6 — Adjacent agents and tools

| # | Question | Options |
|---|---|---|
| 6.1 | Is there a supervisor-adjacent agent? | yes — where it lives, what it owns, how this workspace reaches it · no |
| 6.2 | MCP tools to attach? | names and configuration location — e.g. a supervisor server, a code-health server |
| 6.3 | Anything deliberately excluded? | recorded with the reason, so a later reader does not treat the absence as an oversight |

**6.1 exists because the predecessor system had one**, and its canonical ICE tooling lived
there. A workspace that depends on an adjacent agent must say so, or a fork will find a hole
where a pipeline should be.

**6.3 is not a formality.** "We are not using the code-health tool yet" is a decision. Recorded,
it stays a decision; unrecorded, it becomes a mystery.

---

## Section 7 — Writing, boundaries and cadence

| # | Question | Default |
|---|---|---|
| 7.1 | Where does governance live? | **this workspace, never the parent.** The parent is read, never written to |
| 7.2 | May evidence be committed, or reference-only? | reference-only unless rights are established. See `EVIDENCE_AND_PATHWAYS.md` |
| 7.3 | Cadence | one-shot · on every push · scheduled |

---

## The output

A single record linking answers to probe results:

```
runtime      agent, location, what it can reach
parent       location, access, pinned ref, scope
sources      per tier: where, how reached, reachable yes/no, needs upload
codebase     same shape
validation   which layers are available
adjacent     supervisor, MCP tools, exclusions
boundaries   governance location, redistribution, cadence
             ↓
pathway + capability declaration
             ↓
what this curriculum will NOT be able to claim
```

That last line is the point of the whole exercise. Every unreachable source, every absent tier,
every validation layer that could not run **narrows what the curriculum may claim**, and the
declaration says so before a single course is written.
