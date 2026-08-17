# MASTER SYLLABUS — catalog conventions

**Status:** v0.1-draft · Project Curriculum Protocol
**Depends on:** [`MASTER_RUBRIC.md`](MASTER_RUBRIC.md) — every assessment in every course inherits
that contract whole.
**Companion documents:** [`COURSE_TEMPLATE.md`](COURSE_TEMPLATE.md) ·
[`GENERATION_MACHINERY.md`](GENERATION_MACHINERY.md) · [`THESIS_AND_DEFENSE.md`](THESIS_AND_DEFENSE.md)
· [`ICE.md`](ICE.md)

## Cold-start rule

Honour the objective standard: **if a grading criterion requires a human to guess, estimate, or look
something up, the criterion has failed.** Fix it; do not grade around it.

## What a curriculum is and isn't

Not a general writing guide, and not a narrative curriculum meant to be read start to finish. It is
a **generation substrate**: a library of composable course primitives, each declaring what it
provides and requires, that a generator recomposes on demand against **a seeding objective supplied
later, by someone who never wrote any of the courses**.

A course written well for this substrate teaches a human perfectly well too — but that is a side
effect, not the design target. The design target is that a generator can pull exactly the right
subset of courses to cover an objective nobody anticipated, and validate the result automatically
before a human sees it.

---

## Document taxonomy

| Tier | ID pattern | Role |
|---|---|---|
| **CORE** | `CORE-1NN` | Mandatory, universal courses every domain track inherits — the method's own mechanics plus the process a seeded project needs to bootstrap and run. Domain-agnostic by construction. |
| **ELEC** | `ELEC-1NN` | Cross-cutting methodology courses two or more domain tracks share. This is where "blend where domains blend" becomes a structural fact: one shared course listed as a prerequisite by several tracks, **not duplicated prose in each**. |
| **Domain track** | `<DOMAIN>-1NN` | Courses specific to one seeded domain. Sources, schools of thought, and archive priorities differ; the criterion mechanics never do. |
| **Independent Study** | `IS-1NN` | Open-ended studies gap detection spins up when the catalog doesn't cover something a seeding run needs. Unbounded — this tier is expected to grow forever. |
| **Thesis** | `THESIS-<domain>` | The integrative capstone for one seeded objective. One per domain track per run. |
| **Amendment** | `AMENDMENT-<N>-<TITLE>.md` | Cross-cutting governance rule changes, sequential, **always a standalone file** — never inline prose inside one course, which is exactly the drift a new instance should not repeat. |
| **Assessments** | `<COURSE>_<Task>_{Evaluation,Submission}.md` | Kept in **physically separate directories, always** — `exams/submissions/` and `exams/evaluations/`. An exam-taker and its evaluator must never be the same pass, so self-grading is structurally impossible rather than merely discouraged. |
| **Defense** | `defense/`, `defense-2/` | Whole-thesis adversarial audits. See `THESIS_AND_DEFENSE.md`. |

---

## Two dependency graphs — both required, both machine-validated

**1. `curriculum_prerequisites.json` — the structural DAG.**
Every node: `{"file": "<exact filename>", "prerequisites": ["<ID>", ...]}`. It must agree with the
`**Prerequisite:**` line inside the course file's own header. Validate **both directions**: no
missing files, no self-dependency, no cycles, no orphan IDs.

**2. `curriculum_traceability.json` — the artifact map.**
Maps any non-course research artifact onto a `disposition`, a `courses` list, and (for a thesis) a
`thesis_chapters` list.

> **Governing rule: a finding does not remain a standalone shadow curriculum.**
> If a document isn't mapped here, it isn't part of the program. Full stop.

That rule is what stops an implementation from accumulating the exact problem it exists to solve —
an ever-growing pile of disconnected markdown that nothing consumes and nobody maintains.

---

## Naming and cross-referencing

- Course files: `<ID>-<kebab-case-title>.md`. The filename **must exactly match** the `file` field
  in `curriculum_prerequisites.json` — machine-validated, not merely convention.
- Tier numbers are contiguous **within their tier, in creation order** — chronological, not topical.
  A gap at the low end of a tier signals "this continues a shared or parent numbering", not an error.
- Assessment marker IDs: `<COURSE>-Q<N>` (quiz), `<COURSE>-A<N>` (assignment; decimal sub-numbers
  like `A2.5` for closely related follow-ons are fine), `<COURSE>-FE` then `-FE2`, `-FE3` for
  successive held-out generations. **A pass on generation N never implies a pass on N+1** — each
  requires its own submission and evaluation pair before it counts as taken.
- Prose paragraphs end with a bracketed course-ID list, e.g. `[CORE-104; ELEC-101]` — the
  lightweight, human-scannable citation layer sitting on top of the two JSON graphs.
- Timestamps: full offset-aware ISO-8601 in machine-readable files; plain `YYYY-MM-DD` in prose
  revision headers.

---

## Change management — six governance actions, and you must name which you used

When new material arrives that might affect the catalog, the decision is always exactly one of six.
**Any claim that "the catalog was considered" must name which action was taken.**

| Action | When |
|---|---|
| **Create** | Fits no existing course. |
| **Edit** | Fits an existing course's scope exactly, in place. |
| **Add** | Extends a course's scope without breaking its coherence — a new module. |
| **Split** | Content no longer fits its course's stated scope. |
| **Merge** | Two courses are arguing the same topic. |
| **Shrink** | Content is wrong, redundant, or superseded. |

> **Never silently edit a stale or wrong claim.** Add a dated closure note or a dated revision
> section in place, explaining what changed and why. The record of having been wrong is part of the
> evidence, not noise to be cleaned up.

---

## `course_lifecycle.yaml` — the staleness ledger

Three blocks:

- **`policy`** — global rules: a fixed review interval in days, and the standing rule that *a
  matching discussion schedules a review, it never silently edits content.*
- **`courses`** — per-course `created_at` / `last_reviewed_at` / `review_due_at` / `checkpoint`,
  using YAML anchors so unchanged courses inherit shared dates.
- **`review_routes`** — regex pattern → affected courses, auto-flagging review when matching
  material arrives.

**Routing only schedules review. It is explicitly barred from modifying content.** That separation
is what keeps an automated staleness check from quietly becoming an unreviewed editor.

---

## Bootstrap exception

A brand-new catalog has no courses for its first courses to require. The first courses generated
into an empty catalog may declare `Requires: none (bootstrap)`, and the meta-rubric's
prerequisite-mapping criterion (`GENERATION_MACHINERY.md` Part D, Criterion 2) is satisfied by that
literal value.

**This exception applies only while the catalog is empty, and each use is recorded in the run's own
log.** It is not a general escape hatch — a course claiming bootstrap status in a populated catalog
is a defect.
