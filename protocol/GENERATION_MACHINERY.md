# GENERATION MACHINERY — seeding, translation, gap detection, self-validation

**Status:** v0.1-draft · Project Curriculum Protocol
**Depends on:** [`COURSE_TEMPLATE.md`](COURSE_TEMPLATE.md) (the Coverage Declaration is what this
operates on) · [`MASTER_RUBRIC.md`](MASTER_RUBRIC.md) (Part D below is just another 6-field rubric).

This is the piece that makes "seeding" a real mechanism rather than a hope. Four parts, in the order
they actually fire.

---

## Part A — the Seeding Objective Translator

Translates **any** seeding objective — a research question, a legal audit domain, a coding project's
failure mode, an organizational process — into the same three buckets, because the underlying move
is identical regardless of domain.

| Input | Becomes |
|---|---|
| **The stated goal** — what the objective explicitly asks to be produced or verified | **Extraction / Reasoning criteria** |
| **Implicit expectations** — what would count as excellent even though nobody wrote it down ("run quietly in the background", "cover the field thoroughly", "don't miss the obvious cases") | **Golden-Response criteria**, turned into hard, timeless, self-contained numbers or checks — the same move `MASTER_RUBRIC.md` §2 demands of any criterion |
| **Stated worries** — what the output must *not* do | **Negative constraints** — checks that something did *not* happen: a forbidden action, a scope violation, a fabricated citation |

**Output of Part A:** a **target coverage profile** — the set of `Provides` and
`Generalizes to modes` values this seeding run actually needs, derived from the objective, **before a
single course is selected.**

That ordering is the whole point. Selecting courses first and rationalizing coverage afterwards
produces a curriculum that describes the catalog rather than the objective.

---

## Part B — the composition SOP

1. **Ingest the objective and its footprint.** What is actually being asked for, and **what prior
   material already exists on this topic** — prior runs, prior conversations, prior partial attempts.
   Check before assuming nothing exists; a findable prior attempt is common, not exceptional.
2. **Run the objective through Part A** to get the target coverage profile.
3. **Diff the target profile against the existing catalog's Coverage Declarations**
   (`curriculum_prerequisites.json` plus each course's own declaration). Select the covering subset.
4. **If the subset doesn't fully cover the objective, trigger Part C** — rather than forcing an
   ill-fitting existing course to stretch to cover something it wasn't written for.
5. **Compose the domain-specific track.** Clone `COURSE_TEMPLATE.md` for whatever the gap analysis
   says is missing. Write its modules **grounded in real material for this objective** — never
   abstract theory disconnected from the actual objective, which is the single most-checked property
   in Part D. Write its rubric inheriting `MASTER_RUBRIC.md` in full.
6. **Self-audit before presenting anything.** Is every course rooted in real material for *this*
   objective rather than generic filler? Does every final-exam rubric have complete 6-field criteria?
   Are dependencies acyclic?

---

## Part C — gap detection

Whenever Part B step 3 finds the catalog doesn't cover the target profile, **that gap is itself the
trigger.** No separate monitoring daemon is required for this to work, though one can be layered on
later for a continuously-running system rather than one-shot seeding runs.

On a gap:

1. **Isolate the point of divergence** — exactly which part of the target coverage profile has no
   covering course.
2. **Classify it** — a missing domain-specific technique, a missing shared cross-cutting course, or
   a missing generalization mode entirely.
3. **Generate the closing course** — an `IS-1NN` Independent Study if it is narrow or one-off;
   promoted to a proper `ELEC` or domain-track course if it is clearly going to be needed again.
   Ground its modules in the objective's real material, per Part B step 5.
4. **The output is gated, not auto-published.** It must pass Part D before a human or any downstream
   process ever sees it.

---

## Part D — the meta-rubric

*Who grades the grader?* This rubric grades any auto-generated course, Independent Study, or thesis
chapter — automatically, before a human sees it. **If a generated artifact fails this rubric, it is
regenerated, not shipped with an apology.**

Same 6-field format as every other rubric here; this is Level 3 of the three-level nesting in
`MASTER_RUBRIC.md` §7.

### Criterion 1 — Real-world anchoring
- **Description:** The generated course or chapter explicitly references at least one actual artifact
  from the objective's own real material — a file, a commit, a session, a prior run's output, a
  specific source document — and not abstract or generic theory.
- **Sources:** the generated file; the objective's real material it should be anchored to.
- **Rationale:** a course anchored to nothing real is a hallucinated generic response dressed as a
  targeted one.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 2 — Prerequisite mapping present
- **Description:** The generated course's Coverage Declaration `Requires` field names at least one
  course ID that exists in `curriculum_prerequisites.json`, or the literal value `none (bootstrap)`
  while the catalog is empty per `MASTER_SYLLABUS.md` §Bootstrap exception.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 3 — Final exam rubric is unstacked
- **Description:** Zero criterion descriptions in the generated final-exam rubric contain a
  coordinating conjunction ("and" / "or" / "while") linking two distinct testable concepts.
- **Weight:** Primary objective | **Type:** Style | **Dependent Criteria:** none

### Criterion 4 — Self-containment held
- **Description:** Every generated criterion embeds the expected answer directly in its own text — a
  number, a named fix, a specific fact — rather than deferring to "the correct answer" or "the
  expected fix" left unstated.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 3

### Criterion 5 — 6-field format held
- **Description:** Every criterion in the generated rubric carries all six fields from
  `MASTER_RUBRIC.md` §1, none omitted, with `Sources` and `Rationale` present wherever a specific one
  exists to state.
- **Weight:** Primary objective | **Type:** Style | **Dependent Criteria:** 3, 4

### Criterion 6 — Citation discipline held
- **Description:** Every criterion whose Rationale asserts a claim about external published
  literature cites a DOI that resolves via CrossRef or the publisher's page; every criterion whose
  Rationale asserts a claim about internal project material cites a real file path, commit hash,
  session identifier, or run identifier that exists.
- **Rationale:** `MASTER_RUBRIC.md` §5 is not optional, and **a generator is exactly where
  fabrication risk is highest** — this criterion is what catches a generator inventing a
  plausible-looking DOI or file path instead of finding a real one.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 7 — Coverage Declaration complete
- **Description:** The generated course's Coverage Declaration has all four fields filled — Provides,
  Requires, Generalizes to modes, and Capstone stage supplied (or an explicit `none` for the last) —
  and never a template placeholder.
- **Rationale:** an incomplete Coverage Declaration is **invisible to the next seeding run that needs
  it**. This criterion is what stops the whole composability mechanism from silently degrading as new
  courses accumulate.
- **Weight:** Primary objective | **Type:** Style | **Dependent Criteria:** none

---

## What passing Part D produces

A course or chapter that passed all seven criteria is:

1. added to `curriculum_prerequisites.json` and `curriculum_traceability.json`,
2. given its `course_lifecycle.yaml` entry, initialized, and
3. **made available to every future seeding run.**

That third step is how the catalog grows without a human hand-authoring every domain track from
scratch — and why Criterion 7 matters more than it looks.

---

## What Part D does not catch

The meta-rubric checks whether an artifact is correctly **formed**. It does not check whether the
artifact is **true**, because the generator and the meta-rubric share the same blind spots — neither
is independently verifying reality.

That gap is exactly what `THESIS_AND_DEFENSE.md`'s defense layer exists to close. Passing Part D is
necessary and nowhere near sufficient.
