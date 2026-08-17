# Understanding — what Project Curriculum is, and what it inherits

**Status:** working note, 2026-08-17. **Not the specification.** This is the reading of the
ChatGPT design conversation (2026-08-13 → 2026-08-17) cross-checked against the actual
`projecthamburg/system-instructions` implementation, written down so the eventual `SPEC.md` is
*derived* from what already exists rather than invented around it.

**Author of the underlying work:** Mordecai Machazire, Project Hamburg Research.

---

## 1. What this repository is

Three things at once, deliberately kept separate:

| Layer | What it is | Who it binds |
|---|---|---|
| **Protocol** | The Project Curriculum Protocol (PCP) — agent-independent, runtime-independent | Anyone implementing it, in any agent |
| **Reference implementation** | A CLI/runtime that clones-and-runs locally or in CI | Users who just want it to work |
| **Research corpus** | Published Profiles of real public projects, on a weekly cadence | Researchers, contributors, citation |

The one-sentence claim:

> Don't give the next agent the project's context. Give it the project's **curriculum**.

### The chain

```
Source → Intent → Interpretation → Commitment → Capability → Evidence → Evaluation → Thesis → Defense
```

### The actors (this is the answer to "who is the student?")

- **The agent is the student.**
- **The project is the subject.**
- **The implementation is the laboratory.**
- The **syllabus** defines competence; the **rubric** defines evidence of competence; the
  **thesis** demonstrates composition; the **defense** verifies the claimed understanding is
  still true.

### Where it sits

It is *not* project memory (projectmem, Memorix, Neo4j agent-memory), *not* a repo wiki
(OpenWiki, DeepWiki, RepoAgent), *not* an intent graph (GoalOS, Work Graph). Its distinctive
first-class object is the **Course** — a bounded capability unit that is teachable, testable,
and composable. It can *consume* all three of the neighbouring categories as evidence sources.

| System | Fundamental object | Primary purpose |
|---|---|---|
| Karpathy LLM Wiki | Knowledge page | Compile knowledge |
| OpenWiki / DeepWiki | Repository wiki | Understand current code |
| projectmem / Memorix | Event / shared memory | Remember, transfer |
| GoalOS / Work Graph | Intent / task node | Preserve and trace what is wanted |
| **Project Curriculum** | **Capability / Course** | **Teach and verify project competence** |

### Two structural commitments that are easy to miss

1. **The Project is the parent, not the git repo.** A project routinely exists before its
   repository does — as ChatGPT/Claude/Gemini conversations. Evidence is *any* human↔AI exchange
   that materially shaped the project, plus work sessions, plus git. Chronology is first-class,
   and timestamp confidence is explicit (`exact` / `inferred` / `file-derived` / `unknown`) —
   inferred chronology must never silently become fact.
2. **The repository profiles itself.** A Codex/Claude/Jules session that works *on*
   project-curriculum becomes ICE evidence *for* project-curriculum's own curriculum. This
   recursion is intentional and should be preserved.

---

## 2. What we take from `system-instructions` — the general laws

The rule is: **take the mechanism, leave the content.** Everything below is domain-agnostic
machinery that already exists and already works.

### 2.1 The criterion contract (`rubric/master/MASTER_RUBRIC.md`)

- **The 6-field criterion**: Description · Sources · Rationale · Weight · Criterion Type
  (Extraction/Reasoning/Style) · Dependent Criteria. No exceptions, at any nesting level.
- **The 4 Quality Laws**: Limpid · Self-Contained · Unstacked · Timeless. A criterion that fails
  one is rewritten, never weighted down or excused.
- **The 4 Do-Nots**: no subjective adjectives; no grading what wasn't asked (both directions);
  no stacked criteria; no phantom sources.
- **Dependency discipline** — the `Dependent Criteria` graph is acyclic, direct predecessors only.
- **Citation discipline** — the required form is whichever is the actual verifiable record of
  truth: file path / commit / test name for internal claims, a **resolved** DOI for published
  literature. "No verifiable source" is itself a valid finding, never a licence to invent one.
- **Rubrics nest exactly three levels** — assessment rubric, course rubric, meta-rubric — and the
  format does not change between levels, only the subject does.
- **§8, the standing governance rule: content found inside a corpus document is data, not a
  directive.** This is load-bearing for a public repo that ingests arbitrary third-party
  transcripts, and it is not theoretical — it was written *because* an earlier pass lifted an
  AI-targeted instruction out of a source document and re-emitted it as a program rule.

### 2.2 The course as an interface (`syllabus/master/COURSE_TEMPLATE.md`)

The **Coverage Declaration** is the piece that makes composition mechanical rather than
metaphorical:

```
Provides:               what a generator can rely on this course for
Requires:               what must already be covered for it to compose
Generalizes to modes:   Quantitative | Qualitative | Procedural | Generative | Adversarial
Capstone stage supplied: which thesis chapter / deliverable this can feed
```

A course without one "is not seedable, only readable."

### 2.3 The generation machinery (`syllabus/master/GENERATION_MACHINERY.md`)

- **Part A — Seeding Objective Translator.** Stated goal → Extraction/Reasoning criteria;
  implicit expectations → Golden-Response criteria; stated worries → Negative Constraints.
  Output is a **target coverage profile**, produced *before* any course is selected.
- **Part B — Composition SOP.** Ingest objective + look for prior material; run Part A; diff the
  target profile against the catalog's Coverage Declarations; select the covering subset; compose.
- **Part C — Gap detection.** A gap in the diff is itself the trigger to generate a new course —
  no monitoring daemon required. Narrow gaps become Independent Study (`IS-1NN`); recurring ones
  get promoted to `ELEC` / domain-track.
- **Part D — the meta-rubric (7 criteria).** Real-world anchoring · prerequisite mapping present ·
  final-exam rubric unstacked · self-containment held · 6-field format held · citation discipline
  held · Coverage Declaration complete. **A generated artifact that fails is regenerated, not
  shipped with an apology.** This is the single most important gate to carry into CI.

### 2.4 Catalog conventions (`syllabus/master/MASTER_SYLLABUS.md`)

- Tier taxonomy: `CORE` / `ELEC` / `<DOMAIN>` / `IS` / `THESIS-<domain>` / `AMENDMENT-<N>`.
- **Two machine-validated graphs**: `curriculum_prerequisites.json` (structural DAG, must agree
  with each course's own header, both directions) and `curriculum_traceability.json` (governing
  rule: *a finding does not remain a standalone shadow curriculum* — unmapped means not part of
  the program, full stop).
- **Six change-management verbs, and you must name which you used**: Create · Edit · Add · Split ·
  Merge · Shrink. Never silently edit a stale or wrong claim — add a dated closure note in place.
- **`exams/evaluations/` and `exams/submissions/` are physically separate directories, always** —
  so self-grading is structurally impossible, not merely discouraged.
- `course_lifecycle.yaml` — the staleness ledger. Review routes *schedule* review; they are
  explicitly barred from modifying content.

### 2.5 Thesis and defense (`syllabus/master/THESIS_AND_DEFENSE.md`)

- A thesis is **not a bigger course** — it is the demonstration that the composed courses add up.
  Technically: a **composition proof**.
- **No silent caps.** If coverage was bounded, the chapter says so; a bounded result presented as
  complete is exactly what the defense layer exists to catch.
- **Defense** — adversarial build-and-prove by independently-scoped reviewers: Archaeology (trace
  every claim to origin by inspection, not assumption) · close a real open item against real
  material · tests actually run with real numbers · numbered honest gaps.
- **Defense-2** — the claim audit, run whenever maturity-conflation appears:
  - **Five evidence tiers**: Reproduced now → Historically supported → Implemented and
    test-covered → Partial/fixture-specific → Unsupported/retracted.
  - **CLAIM-LEDGER** — the artifact that actually retracts or downgrades prior claims.
  - **LINEAGE-COMPARISON** — credit honesty: used-as-is vs reimplemented vs inspired-by-never-integrated.
  - **TEST-RECORD** — skips and crashes are never silently converted into passes.
- Why a defense exists at all: the meta-rubric and the generator **share blind spots**. The
  meta-rubric checks whether an artifact is correctly *formed*; only an independent defense checks
  whether it is *true*.

### 2.6 ICE — the informed-consent model (`governance/syllabus/GOV-105`)

ICE is **a record of informed consent between the human and the LLM**, not a quality review of
the LLM's output. (The program's own history conflated the two once, before this was made binding.)

- Every Expectation is an **Ask → Response → Lock-in** chain with exact quotes and line numbers,
  judged 🔒 locked / 🔓 unlocked / ➡️ superseded.
- **Earlier items are never edited or deleted** to accommodate later ones — a divergence becomes a
  new, separately-dated item.
- Only the *human's own* Concerns and Ideas belong in a chapter; a reviewer's opinion of the LLM's
  conduct routes to `CONCERNS.md` instead.
- Every chapter carries a one-sentence **scope declaration** and an explicit **security status**,
  even when that status is "checked, nothing found."

### 2.7 Evidence capture — the hard-won parts (`governance/PROJECTS.md`)

- **Match by real project identity, never by text mention.** Codex `session_meta.cwd`; Claude Code
  the cwd-encoded directory under `~/.claude/projects/`; Kimi `workDir`; Cursor unambiguous by
  in-repo `.specstory/history/`. A grep for the project name is *not* a substitute — it produces
  false positives from unrelated sessions.
- **Three categories, not two**: internal (cwd is the project) · external (cwd is the external
  repo) · **global-adjacent** (cwd is neither, but the session did real tool-call work on the
  project's files). The third needs a two-stage sweep: broad tag candidates, then the critical
  filter — *the path must be the actual target of a `Read`/`Edit`/`Write`/`Bash` call, not merely
  present in some unrelated command's output.* On a real run, 6 of 9 candidates were false
  positives of exactly this shape.
- **Two tag pitfalls, both found for real**: a bare generic word is not a safe tag (`maplescholar`
  returned 60 unrelated hits); a filename that is part of a shared *convention* is not a safe tag
  either (`curriculum_traceability.json` matched three unrelated projects).
- **Mandatory secret sweep before any capture lands in a governance folder.** Non-optional, and
  not hypothetical: a global-adjacent capture caught a live AWS credential pair read from an
  unrelated `.env` earlier in the same session. Verify a flagged match by *length/structural
  shape*, never by printing it.
- **Per-project ingestion ledger** (`_ingested.json`) so re-running discovery is cheap and
  idempotent.
- **Native-vs-derived convention**: the raw original is immutable evidence; the rendered `.md` is
  derived. (This matches the conversation's own later correction — *don't* invent a normalized
  interchange format first and lose the originals.)
- **`origin: internal` vs `origin: external`** tagging on every indexed item, always checked
  before treating a result as the program's own work.

### 2.8 Per-project self-containment

Every project gets its **own** search index, ICE domain, `CONCERNS.md`, security scan, manifest,
and script copies — **no shared runtime dependency on any other project's tooling**. This is the
single property that makes the thing work for a stranger who forks it with none of Project
Hamburg's infrastructure.

Related: **governance lives in the curriculum workspace, never inside the parent project's own
repo** — even when the parent is a completely separate repo elsewhere on disk. That rule was got
wrong once and corrected the same day; it is binding.

### 2.9 The intake checklist (`governance/PROJECTS.md`)

Five questions, and the discipline around them: (1) the project's real location, (2) **the
objective the syllabus must serve**, (3) any existing raw session material, (4) whether real
output already exists to survey, (5) the project identifier. **Do not proceed past a missing (2)** —
a syllabus cannot be seeded without a stated objective. Everything else may default, but defaults
are *stated back*, never silently assumed.

### 2.10 Multi-tool bootstrap (`AGENTS.md`, `.claude/`, `.agents/`)

The already-proven trio, plus one documented negative:

- `AGENTS.md` at root and at every nested level — Codex and Kimi walk root→cwd loading each level.
- `.claude/settings.json` `SessionStart` hook — because Claude Code reads only `CLAUDE.md`.
- `.agents/rules/*.md` with `trigger: always_on` — for Antigravity, which has no hook mechanism.
- **Deliberately not built:** a Codex `SessionStart` hook — real, but documented as unreliable
  (silently skipped trust prompts, doesn't fire in worktrees, no confirmed IDE/Desktop parity).

### 2.11 Two more disciplines worth carrying

- **The security scan pattern**: read-only, dated report, every finding a *proposed* disposition
  (`remove` / `quarantine` / `monitor`) requiring explicit human approval. Never auto-applied.
- **The Blueprint epistemic rule**: each build stage ends with a **real run against real code**,
  not "tests pass." Documentation claiming something worked is not evidence that it did. This is
  philosophically the same commitment as thesis-defense, one level down.
- **Self-teaching recursion**: the governance layer has its own gradable curriculum (`GOV-101`–
  `106`), and Blueprint has `BP-110 — Adopting Blueprint on a Project`. The system makes its own
  operating knowledge teachable and testable. Project Curriculum should ship with the same:
  a curriculum about itself, and a course about adopting it.

---

## 3. What we do **not** take

| Not taken | Why |
|---|---|
| `projects/01-maplescholar-journal-discovery/` | Real private research instance (7 fields × 4 labels, 280 DOI-cited findings) — output, not machinery |
| `projects/02-oew-analysis/` | Real private project (OEW engine), 23 intent-conformance chapters, SWARM_LOG, external repo paths |
| `rubric/materials/` | Third-party talent-training corpus (~220 MB video + anchor examples). **Open, unresolved confidentiality question** (`CONCERNS.md` item 1 / ch02 C3) and quarantined content. Cannot go public. |
| `syllabus/materials/` | `ai-studio-export`, and `examples/s2` — a whole borrowed worked syllabus/thesis/defense system, `origin: external` |
| `governance/sources/` | Raw session transcripts. Gitignored already; a real leaked credential was found in the wider pool during curation |
| `governance/ice-outputs/` | Real ICE chapters about Mordecai's own sessions; also read-mirrors whose canonical source is a private repo |
| The `_logs/supervisor` repo | `ice_pipeline.py`, inbox/outbox to task-04, offsite-generalist task structure, personal absolute paths |
| `governance/CONCERNS.md`, `security/findings/`, `security/REGISTRY.md` | Organization-specific and security-sensitive |
| `blueprint/src/` | A separate product (xray / manifest / registry / sonar / synapse / cortex). Only its **adoption pattern** generalizes, not its code |
| `search_index.json` | 6.4 MB build artifact, rebuildable from scratch |
| The `01-` / `02-` numbering | Explicitly replaced — see §4. A single global sequence cannot survive issues, forks, and multiple contributors |
| "Supervisor" as the top-level name | Supervisor is the *runtime component*, not the protocol. Keeping the concept independent of the implementation is the point |

One thing that is **not** a clean take-or-leave: the ICE pipeline itself. The model (GOV-105) is
fully generalizable and must come across, but the canonical tooling lives in the private
supervisor repo. The public protocol needs an ICE implementation that does not depend on it.

---

## 4. How it is presented

### Repository shape

```
project-curriculum/
├── README.md, SPEC.md, AUTHORS.md, GOVERNANCE.md, CONTRIBUTING.md, SECURITY.md, ROADMAP.md
├── protocol/          project · seeding · session · conversation · ice · intent · expectation
│                      course · syllabus · rubric · assessment · thesis · defense
├── schemas/           machine-readable forms of the above
├── templates/         COURSE_TEMPLATE, thesis skeleton, PROFILE.yaml, seed-pack
├── adapters/          claude-code · codex · cursor · jules · antigravity · chatgpt-export
│                      claude-export · gemini/ai-studio · kimi · openrouter · specstory · manual
├── cli/ (or src/)     the reference runtime
├── examples/          organized by thesis class, not by repo
├── profiles/          the research corpus
└── .github/           workflows, ISSUE_TEMPLATE, PR template, CODEOWNERS
```

### Naming and identity

Numeric project IDs are replaced by **upstream identity + seed identity**, because the same
repository can legitimately be seeded many times with different questions:

```
profiles/github/<owner>/<repo>/<seed-slug>/PROFILE.yaml
```
```yaml
project: { id: "github:specstoryai/the-jig-is-back" }
seed:    { id: "seed:2026-08-14:intent-fidelity", title: "Intent Fidelity", submitted_by: ..., upstream_commit: ... }
```

`PROFILE.yaml` is the single canonical machine entrypoint, stating exactly *what was studied, at
what commit, why, on what evidence, by whom, with what version of the tool, under what licences.*
That is what makes a profile reproducible.

### Examples organized by claim, not by repository

Each example exists to test a different claim about the protocol:
intent-fidelity · feature-evolution · project-memory · development-provenance · competence ·
**research (no code)** · agent-inheritance · intent-drift.

The no-code research example is the one that stops people filing this as "another coding-agent
framework" — and it is also the one candidate that has not been found yet.

### Vocabulary — keep the academic terms, add technical semantics underneath

> We call it a Thesis. Technically, it's a **composition proof**.
> We call it a Syllabus. Technically, it's a **composable capability specification**.
> We call it a Rubric. Technically, it's an **acceptance/evaluation contract**.

Course = bounded capability unit · Coverage Declaration = capability interface · Assignment =
verification task · Quiz = knowledge check · Final Exam = capability evaluation · Defense =
independent adversarial verification · Supervisor = lifecycle orchestrator · ICE = historical
evidence reconciliation.

### Licensing (open, deliberately)

The repository currently has **no `LICENSE`** — Apache-2.0 was selected at creation, then removed
the same morning, pending a real decision. The live question is the Elasticsearch/OpenSearch
scenario: Apache-2.0 permits a hosted, closed, improved fork with nothing contributed back.

Working structure to decide against:

- **Software** — Apache-2.0 vs **MPL-2.0** (file-level copyleft, distribution-triggered) vs
  **AGPL-3.0** (network-use copyleft; the only one that actually addresses the stated fear).
- **Specification + Project-Curriculum-authored profiles** — CC BY 4.0.
- **Third-party upstream code and conversations** — retain original licence and provenance;
  reference rather than copy where redistribution rights are not clear.
- **Contributions** — DCO (signed-off commits, bot-enforced) rather than a heavyweight CLA.
- Trademark and branding reserved separately from copyright.

Counsel review before the first substantive public release. This decision **blocks** accepting
outside contributions and blocks any use of third-party transcripts.

---

## 5. Running it in GitHub Actions

### The constraint that shapes everything

CI has no access to anyone's laptop. `~/.claude/projects/`, `~/.codex/sessions/`,
`~/.kimi-code/`, Cursor's `state.vscdb` — none of it exists on a runner. So CI runs on
**checked-in, sanitized seed packs or uploaded artifacts**, and local runs are where native
session discovery happens.

Three execution modes, all first-class:

```bash
project-curriculum seed --parent ../my-project          # local folder
project-curriculum seed --repo owner/name               # remote repository
project-curriculum seed --repo "$GITHUB_REPOSITORY" --sessions ./seed-pack/sessions   # CI
```

### The pipeline a workflow runs

```
checkout → resolve upstream @ pinned commit → load + normalize evidence (raw preserved)
        → secret sweep → ICE → intents / expectations / concerns
        → target coverage profile → diff against catalog → generate gap courses
        → META-RUBRIC GATE (Part D) → assessments → thesis → defense
        → publish artifacts → open PR
```

### The gates that must be CI-enforceable

These are the parts of `system-instructions` that are already machine-checkable, and they should
be validators before they are anything else:

1. Prerequisite DAG — acyclic, filenames match `curriculum_prerequisites.json`, header and JSON
   agree in both directions, no self-dependency.
2. Traceability completeness — every non-course artifact mapped, or it is not part of the program.
3. The 7-criterion meta-rubric on every generated course/chapter.
4. Criterion lint — 6 fields present · unstacked (no `and`/`or` joining two testable concepts) ·
   self-contained (expected answer embedded) · no subjective adjectives · timeless.
5. Citation resolution — DOIs resolve via CrossRef; internal paths/commits actually exist.
6. Coverage Declaration completeness — all four fields, never a template placeholder.
7. Secret sweep on every piece of ingested evidence, **before** it is committed anywhere.
8. Provenance/licence declaration present and non-empty in `PROFILE.yaml`.
9. No-silent-caps — a bounded result must be declared bounded.

Note the asymmetry that makes this safe: capture and validation are mechanical and automatable;
**ICE review and defense are judgment calls and stay human-gated.** That split is already the
practice in `system-instructions` and should not be quietly dissolved by automation.

### Intake and cadence

```
structured issue → validate upstream + licence + evidence + duplicate seeds → candidate seed
   → agent seeding run → PR → CI validators + defense → maintainer approval → merge
```

**Nobody pushes to `main` — not contributors, not Claude, not Codex, not Jules.** `main` is the
accepted research record; branch protection enforces it.

Submission cadence and publication cadence are separate: PRs merge continuously, and a scheduled
workflow emits **Project Curriculum Weekly — Week N, YYYY** from what was accepted.

Two workflow classes with different trust profiles: **validators** (no secrets, run on every PR
including forks) and **seeding runs** (need model API keys — fork runs use the fork's own secrets;
upstream runs are maintainer-gated via a protected environment).

---

## 6. How a fork gets this running on their own project

**The runtime is a coding agent, not a bespoke daemon.** Claude Code, Codex, Jules, Cursor,
Antigravity, Kimi and the rest all read the same artifacts. Only *layer 2* — the agent procedure —
changes per platform:

```
contract → CLAUDE.md / skill      → Claude Code tools
contract → AGENTS.md / prompt     → Codex, Jules, Kimi
contract → .agents/rules/*.md     → Antigravity
contract → INSTRUCTIONS.md        → OpenWiki
contract → graph/state machine    → LangGraph
```

The wiki/curriculum underneath stays identical. That is the whole point of making the
specification canonical rather than any one implementation.

### The fork flow

1. Fork or clone `project-curriculum`.
2. `project-curriculum init` — the workspace asks for the **parent project** (local path or GitHub
   repo) and the **seeding objective**. The objective cannot default; everything else can, but
   defaults are stated back.
3. Point at evidence: auto-discover local agent sessions by real project identity; import
   ChatGPT / Claude / Gemini / Kimi / OpenRouter exports; or use a checked-in seed pack.
4. Confirm associations at three confidence levels — explicit, path/repository, candidate.
   **Uncertain evidence is never silently made canonical.**
5. Seeding run produces the curriculum in the workspace.
6. Their agents study it, are assessed against it, and continue the work.

**The parent project's own repository is never moved into the framework and never modified.**
Governance lives in the curriculum workspace, pointing outward. This keeps the fork's real code
untouched — and it is exactly the corrected, binding rule from `governance/PROJECTS.md`.

One-time per clone, because git hooks are not cloned:

```bash
git config core.hooksPath governance/hooks
```

### What makes this portable rather than Project-Hamburg-specific

Per-instance self-containment (§2.8): own index, own ICE domain, own concerns log, own security
scan, own script copies, no shared runtime dependency and no network requirement. A fork inherits
a working system, not a client of someone else's server.

---

## 7. Open questions to resolve before the first substantive release

1. **The licence.** Unresolved, and it blocks both outside contributions and any redistribution of
   third-party transcripts. Apache vs MPL vs AGPL is a philosophy question, not a formality.
2. **`.claude` hook vs `CLAUDE.md`.** A `SessionStart` hook executes a shell script in a repository
   strangers clone. For a public repo, a plain `CLAUDE.md` may be the more honest default, with the
   hook offered as opt-in.
3. **The no-code research example does not exist yet.** The only real instance (MapleScholar) is
   private. Without a public one, the project reads as a coding-agent framework.
4. **Corpus search at scale.** A per-repo lexical index is right for one workspace. Decide early
   whether 52+ published profiles are one queryable corpus or 52 separate ones.
5. **ICE without the supervisor repo.** The canonical pipeline is private; the public protocol
   needs its own.
6. **Session-evidence redistribution rights.** A repository's code licence says nothing about the
   right to republish a conversation about it. Reference-by-default, copy only on verified rights.
