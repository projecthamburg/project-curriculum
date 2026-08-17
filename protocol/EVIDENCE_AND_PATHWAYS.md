# EVIDENCE AND PATHWAYS — what a curriculum can be built from

**Status:** v0.1-draft · Project Curriculum Protocol
**Feeds:** [`GENERATION_MACHINERY.md`](GENERATION_MACHINERY.md) Part A · consumed by
[`ICE.md`](ICE.md)

Two pathways produce a curriculum. They are not variants of one process — they answer different
questions, and one of them **cannot answer the question the other exists for.** Saying which
pathway produced a curriculum is not metadata; it bounds every claim the curriculum can make.

---

## Pathway A — ICE + codebase and documentation

**Available when:** the project has recoverable human↔AI conversation history.

```
conversations + work sessions        codebase + documentation
            │                                   │
       ICE review                        codebase index
            │                                   │
   Ideas · Concerns · Expectations       structure · behaviour
            └───────────────┬───────────────────┘
                            ▼
                    coverage profile
                            ▼
                       curriculum
```

**What only this pathway can answer:** *did the implementation do what was asked?* That requires
a record of the asking. Intent fidelity, commitment tracing, supersession, and drift are all
Pathway A capabilities.

---

## Pathway B — codebase and documentation only

**Available when:** no conversation history exists, or none is recoverable — a repository
inherited without its history, a project built before capture was in place, or one whose
sessions were never preserved.

```
codebase + documentation + git history
                  │
           codebase index
                  │
        structure · behaviour · change
                  ▼
          coverage profile
                  ▼
             curriculum
```

**What this pathway must declare, in the curriculum itself:**

> No intent record exists for this project. Every statement about *why* something is the way it
> is, is inference from the artifact, not evidence of a decision.

That declaration bounds *why*, and only *why*. It does not bound *what the artifact promised* —
that is readable directly, and reading it is most of the work here.

### The hard rule for Pathway B

**Absent intent is stated as absent. It is never inferred and presented as recovered.**

A commit message, a code comment, and a README are all real evidence of *what was believed at
writing time* — and none of them is a record of what was asked for. A Pathway B curriculum may
say "the code does X, and the comment says X was chosen for reason Y". It may not say "the
intent was Y".

Concretely, a Pathway B curriculum:

| May contain | May not contain |
|---|---|
| Structural and behavioural courses | Ask → Response → Lock-in chains |
| **Encoded Expectations, and their conformance judgments** | **Negotiated** Expectations |
| Courses grounded in code, tests, docs, git history | Courses grounded in what someone asked for |
| A thesis proving the courses compose | A thesis claiming the implementation satisfies its *negotiated* intent |
| Findings about internal inconsistency and self-contradiction | Findings about drift from what was wanted |

> **Pathway B is not a pathway without Expectations.** It is a pathway without *negotiated* ones.
> The artifact states what it holds itself to — in docstrings, config documentation, tests,
> schemas, validation, defaults and error messages — and every one of those is an Expectation that
> can be checked. See `ICE.md` §"What an Expectation is". Pathway B projects routinely produce
> **more** Expectation findings than Pathway A ones, because nobody has been reconciling the
> artifact's promises against its behaviour.

Git history is the strongest evidence Pathway B has, and it is still evidence of *change*, not
of *intent*. A curriculum that quietly upgrades it is doing the thing this protocol exists to
prevent.

### Pathway B is not a lesser pathway

It is the correct pathway for most projects that exist. Almost no repository has its
conversation history. A protocol that only works for projects captured from day one would be
useless for the inheritance problem it was built to solve.

### Promotion

A project can move from B to A when history is found — an old export surfaces, a machine is
recovered. Promotion is **additive**: existing courses stay, ICE chapters are authored over the
newly available evidence, and intent-fidelity courses are generated on top. The curriculum
records the date it was promoted, and which of its courses predate the intent record.

---

## Evidence tiers

Tier is a property of the **source**, recorded in each capture's `.meta.json` sidecar. It
determines what a chapter may claim from that source — not how much the source is worth.

### Tier 1 — Agent work sessions

Claude Code, Codex, Cursor, Kimi, Jules, Antigravity, desktop agent apps, and SpecStory
captures of any of them.

- **Distinguishing property:** the agent could *act*. Tool calls, file edits, and commands are
  in the record alongside the dialogue.
- **Carries:** per-turn timestamps, a working directory, often a git ref.
- **Association:** `path` by default — the session's own recorded cwd establishes it.
- **Can establish:** a full Ask → Response → Lock-in chain, and a commitment traceable to a
  specific edit.

### Tier 2 — LLM conversation logs

ChatGPT, Claude.ai, Gemini and AI Studio, Kimi, OpenRouter frontends, self-hosted models.
Exported by hand as `.md`, `.txt`, `.json`, or `.html`.

- **Distinguishing property:** dialogue without action. This is where a project is *thought
  about* — often long before a repository exists.
- **Carries:** turn structure and usually dates. **No tool calls, no working directory.**
- **Association:** `explicit` when a human points at the file; `candidate` in a bulk sweep.
  Never `path` — there is no path in the record to match on.
- **Can establish:** an Ask → Response → Lock-in chain. **Cannot** establish that any
  commitment reached the codebase — a Tier 2 commitment must be resolved against Tier 1 or
  against the code itself before it is treated as implemented.

Tier 2 is where the pre-repository history lives. A project frequently exists for months in
Tier 2 before its first commit, and that period is invisible to every repository-centric tool.

### Tier 3 — Human-side material

Notes, thoughts, scratch `.txt` files, screenshots, whiteboard photos, voice-note transcripts,
emails to oneself, design sketches.

- **Distinguishing property:** **one voice.** There is no response and no counterparty.
- **Carries:** frequently no date, no structure, no ordering.
- **Association:** `candidate` by default, always.
- **Can establish:** Ideas, and Concerns. **Cannot establish a *negotiated* Expectation** — that
  requires an Ask *and* a Response *and* a lock-in judgment, and a note has only the first.

> **This is the tier rule that matters most.** A monologue cannot produce an Ask → Response →
> Lock-in chain. A chapter that manufactures one from a note has fabricated the other party.
>
> It says nothing about **encoded** Expectations, which come from the artifact rather than from
> any source tier. A project whose only human-side evidence is a Tier 3 note still has every
> Expectation its code, config, tests and docs state about themselves.

Tier 3 material is often the earliest and most candid record of what someone actually wanted.
It is admissible, valuable, and constrained.

### What tier does and does not do

| Tier does | Tier does not |
|---|---|
| Bound what a chapter may claim from a source | Rank sources by importance |
| Set the default association confidence | Determine whether a source is included |
| Determine the chunking strategy | Override an explicit human association |

A Tier 3 screenshot can carry the single most important requirement in a project. It still
cannot carry a lock-in.

---

## Spheres — scoping a chapter to an area

A chapter over "everything not yet reviewed" works for one session. It fails at fifty: the scope
declaration becomes meaningless, and the Expectations in one chapter have nothing to do with
each other.

A **sphere** is a named area of a project's evidence. Chapters are authored **per sphere**, so
a chapter's scope is a real subject rather than an arbitrary time window.

### Spheres are a query-time view, not a partition

There is **one index**. A sphere is a named filter over it — categories, keyword rules, path
globs, tiers, date ranges. Nothing is copied, nothing is rebuilt when a sphere changes, and a
source may belong to several spheres at once. A decision that spans licensing *and* governance
should appear in both.

### Deriving spheres

Proposed by the tooling, confirmed by a human. Never adopted silently.

1. **Co-occurrence.** For every keyword in the index, the set of chunks carrying it. Keywords
   appearing together across many chunks and rarely apart are one area.
2. **Score and rank.** Prefer terms that are frequent within a candidate sphere and infrequent
   outside it — a term appearing everywhere describes the project, not an area of it.
3. **Propose with evidence.** Each candidate sphere is proposed with its defining terms, its
   chunk count, its source spread, and its date range. A sphere drawn from one source is
   usually a topic, not an area.
4. **A human confirms, names, and edits.** Machine-proposed boundaries are a starting
   hypothesis. Naming an area is a judgment about what the project *is*.
5. **Chapters are then authored per sphere**, each with a real scope declaration.

### What spheres are not

Not clusters that replace human judgment; not a partitioned index; and not permanent — a
project's areas change, and a sphere definition is edited in place with a dated note like any
other claim.

---

## Two indexes, one curriculum

The evidence index and the codebase index are **separate, and deliberately so.**

| | Evidence index | Codebase index |
|---|---|---|
| Over | Tier 1/2/3 captures | source, docs, config, tests |
| Chunked by | speaker turn | symbol and section |
| Answers | what was said, asked, decided | what exists and how it behaves |
| Tagged | tier, speaker, association, timestamp confidence | language, kind, path |

They are kept apart because their chunk shapes and their trust semantics differ, and merging
them makes a query unable to distinguish "someone said the system does X" from "the system does
X". Part A consumes both:

```
evidence index ──┐
                 ├──> coverage profile ──> courses ──> thesis
codebase index ──┘
```

Pathway B has only the second. That is the whole difference between the pathways, expressed
mechanically.
