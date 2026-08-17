# PROJECTS — the registry, the intake checklist, and the per-project pattern

One workspace holds many projects. This file is the pattern every one of them follows,
whether its content is nested here or lives entirely elsewhere on disk.

**Machine source of truth:** `governance/registry.json`. A folder name is not the record —
`new_project.py` assigns the number in the registry and derives the folder from it, never
the other way round. A folder like `03-my-app` happens to be readable, but an external
project has no such prefix on its own directory, so the registry is what actually decides.

---

## How to create a new project — the intake checklist

**Step 0: probe before you ask.** `governance/intake.py` determines by looking everything that
can be determined by looking, asks only for what cannot be, and reports the pathway and the
capability declaration before a single file is written.

```bash
python3 governance/intake.py --parent ../my-app --exports ~/Downloads/chat-exports
```

Asking a human to report what the filesystem already knows produces wrong answers, so the
questionnaire deliberately asks as little as possible. What it cannot probe — the objective
above all — it asks for, and refuses to continue without.

Its most important output is the list of what the curriculum **will not** be able to claim.
That list is never empty: even a project with Tier 1 sessions and full git history lacks
pre-repository conversation and human-side material, and both are stated.

The five items below are what that probe resolves, kept here because an agent working without
the script still needs them.

| # | What | Default? |
|---|---|---|
| 1 | **The project's real location.** A path. Nested here, or a fully external directory (possibly its own git repository). | Yes — surveyed from the path given |
| 2 | **The objective the curriculum must serve.** | **No. Required.** |
| 3 | **Any existing conversation or session material** — chat exports, prior terminal sessions, research notes — that should seed ICE review or the curriculum itself. | Yes — assume none if nothing is found, and say so |
| 4 | **Whether the project already has real output to fold in**, or is a from-scratch build. A partially-existing project needs a read-only survey pass before deciding what its content means for the curriculum. | Yes — but don't assume a blank slate just because governance hasn't been built |
| 5 | **The project number.** | Yes — next in the registry |

> **Do not proceed past a missing (2).** A curriculum cannot be seeded without a stated
> objective; there is nothing to seed it *for*. `new_project.py` enforces this.

(1), (3), (4) and (5) may default — but every default is **stated back**, never silently
assumed, so it can be corrected before real files exist. `new_project.py` prints an intake
summary and supports `--dry-run` for exactly that.

```bash
python3 governance/new_project.py --parent ../my-app \
    --objective "Understand and verify the authentication system" --dry-run
```

---

## Governance folder location — binding

> **Every project's governance folder lives at `projects/<NN>-<slug>/governance/` in this
> workspace. Always. Unconditionally.** Whether the project's real content is nested here
> or lives in a completely separate repository elsewhere on disk.
>
> **It is never placed inside an external project's own directory.**

This is stated first and plainly because the predecessor system got it wrong once, built it
the other way for a real project, and corrected it the same day. A later project should
never have to re-derive it from an ambiguous precedent.

The external repository is **read, never written to**. Its own git history, hooks and
tooling are entirely its own concern, untouched by this pattern.

**What actually differs for an external project** — everything else is identical:

- The manifest's `path:` entries resolve against the **external** root, not the governance
  folder. That is what `external_root` in `config.json` is for.
- `discover_sessions.py` matches sessions against **both** roots.

---

## What every project gets

```
projects/<NN>-<slug>/
├── AGENTS.md                        nests under the workspace root AGENTS.md
├── governance/
│   ├── config.json                  the only file that differs between copies
│   ├── <portable scripts>           byte-identical copies — see governance/README.md
│   ├── sources/                     captures + _ingested.json ledger
│   │   └── <NN>-project-files-manifest.yaml
│   ├── ice-outputs/                 chapters + _watermark.json
│   ├── reports/                     dated update reports
│   ├── security/findings/           dated scan reports
│   ├── CONCERNS.md                  not optional, exists from the start
│   └── PROVENANCE.md
└── syllabus/
    ├── curriculum_prerequisites.json
    ├── curriculum_traceability.json
    └── course_lifecycle.yaml
```

Three of these are worth calling out:

**`CONCERNS.md` is not optional.** Every project gets one from the start, even empty. It is
where security and conduct findings land as they are found — not something added later once
something has already gone wrong.

**Its own ICE domain.** Not a chapter inside a shared one. This isn't symmetry: each
project's `ice_chapter.py` needs its own chapter-number watermark to allocate from, or two
projects running at once collide on the same number.

**Its own everything else.** Own index, own scripts, own security scan. **No shared runtime
dependency on the workspace or on any other project.** That independence is what makes a
fork work with none of the original infrastructure.

---

## The cycle, once a project exists

1. **Capture.** `discover_sessions.py` finds work sessions on this machine, matched by real
   cwd/workDir. `import_chat_logs.py` imports exported conversations from providers with no
   local store. Both diff against the project's own ingestion ledger, so re-running is cheap
   and idempotent.
2. **Review.** `ice_chapter.py new --label <name>` scaffolds a chapter; a human or agent
   reads the sources and authors it. **This step stays manual, deliberately** — capture is
   mechanical and safe to automate; review is a judgment call and isn't.
3. **Reindex.** `update.py --real` rebuilds the project's own index, after capture, so
   anything new is included.
4. **Seed and maintain.** Reviewed chapters plus the project's own content feed curriculum
   generation (`protocol/GENERATION_MACHINERY.md` Part A). Keeping the curriculum current is
   a judgment call each time, not itself automated.

---

## Session discovery — what it does and does not do

**Matches by real project identity, never by text mention.** Codex `session_meta.cwd`;
Claude Code the cwd-encoded directory name under `~/.claude/projects/`; Kimi `workDir`
(**not** `cwd` — a naive scan checking `cwd` there finds nothing at all); Cursor unambiguous
by in-repo `.specstory/history/`; Claude Desktop `cwd`/`originCwd`.

**A grep for the project's name is not a substitute.** It reliably produces false positives
from unrelated sessions that merely mention it.

### The third category — global-adjacent

`discover_sessions.py` finds sessions whose own recorded cwd **is** the project. That leaves
a real gap: a session whose cwd is neither the project nor its external repo, but which did
genuine, deliberate work on the project's files anyway.

Finding those takes a two-stage sweep, and it is **not yet implemented here** — stated
plainly rather than left for someone to discover missing:

- **Stage 1 — broad candidate sweep**, no cwd filter, across every tool's session storage,
  looking for the literal path roots *and* distinctive project-specific identifiers.
- **Stage 2 — the critical filter.** A path appearing anywhere in a session file is not
  evidence. It must appear as the actual **target of a real tool call** — a `Read`/`Edit`/
  `Write` `file_path`, or a `Bash` command operating on it — not merely inside the *output*
  of some unrelated, much broader command. In the predecessor system, 6 of 9 raw candidates
  were false positives of exactly this shape: recursive search dumps from an unrelated
  working directory that happened to sweep past a matching file.

**Two tag pitfalls, both found the hard way:**

- **A bare generic word is not a safe tag.** One single-word project tag returned 60 hits,
  every one of them an unrelated, coincidentally-named reference. Prefer the full
  distinctive path or a genuinely unique compound identifier.
- **A filename that is part of a shared naming *convention* is not a safe tag either.**
  `curriculum_traceability.json` matched three unrelated projects, because every project
  built on this method has one. A shared-convention filename is only safe when paired with
  something that disambiguates it.

**Security requirement, non-optional:** sweep every capture for secrets **before** it is
left in a governance-tracked folder. Never assume clean on the precedent of earlier captures
being clean — a global-adjacent session by definition did *other* work too. In the
predecessor system this caught a live credential pair read from an unrelated file earlier in
the same session and captured verbatim. Verify a flagged match by its **length and
structural shape, never by printing it.**
