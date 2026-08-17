# THESIS-inherited-service: What an Artifact Can Prove About Itself

**Tier:** Thesis | **Prerequisites:** INH-101, INH-102, INH-103, INH-104
**Candidate's standing question:** *With no record of what anyone wanted, how much can be
established about this service — and where exactly does that stop?*
**Citation discipline in effect:** internal record of truth (file and line in the parent, plus
executed output). No published-literature claim is made, so no DOI applies.

> **Core Principle:** This thesis proves a disagreement and refuses a diagnosis. Both are
> results. **No intent record exists for this project**, so the second half is not a gap in the
> work — it is the finding.

> **Revision 2026-08-17.** As first authored this thesis described the project as having no
> Expectations at all. That was wrong: Expectations also arise from the artifact, and this
> project has three — one ⚡ contradicted, one ❌ violated, one ⚠️ untested — now recorded in
> `ch01`. What it lacks is *negotiated* Expectations. The findings below are unchanged; their
> classification is corrected. See `protocol/ICE.md` §"What an Expectation is".

## Thesis Statement

The four courses compose into a complete account of what this artifact can demonstrate about
itself, and a precise boundary where that ends. The service's read path and write path
implement incompatible format contracts; the incompatibility is demonstrated by execution, not
argued from source; the README's round-trip claim is false as written; and the reason for any
of it is unrecoverable.

| Deliverable | Made real by | Evidence |
|---|---|---|
| Both format contracts, read from code | INH-101 | `src/app.py`, `src/export.py` |
| The disagreement, executed | INH-102 | two fields written, three read |
| A false documentation claim | INH-103 | `README.md` vs the executed round trip |
| The boundary of what evidence supports | INH-104 | empty Expectations, by rule |

## Chapter Plan

### Chapter 1 — Contracts
- **Stands on:** INH-101
- **Already real:** `parse` splits on every comma and never unquotes. `format_field` quotes a
  field containing a comma. Each is internally coherent. They differ only where a field contains
  a delimiter — precisely the class quoting was added for.
- **OPEN:** Nothing. Both contracts are fully readable from the code.

### Chapter 2 — Demonstration
- **Stands on:** INH-102
- **Already real:** `format_record(["hello,world", "active"])` writes `"hello,world",active`;
  `parse` reads it back as `['"hello', 'world"', 'active']`. **Two fields written, three read**,
  with the quote characters surviving as content. Executed, not predicted.
- **OPEN:** Nothing.

### Chapter 3 — Documentation
- **Stands on:** INH-103
- **Already real:** the README states the format round-trips cleanly. Unqualified, so one
  counterexample falsifies it. It remains true for every record with no delimiter in a field,
  which is why it survived.
- **OPEN:** Whether the README predates the quoting is not recoverable.

### Chapter 4 — Pathway
- **Stands on:** INH-104, and all three prior chapters
- **Already real:** Pathway B, determined by probe before any file was written. One Tier 3 note
  is the whole human-side record; it carries three Concerns and one Idea and **no negotiated
  Expectation**, because a monologue has an Ask and no Response. The artifact itself carries
  three **encoded** Expectations, judged by conformance in `ch01`.
- **OPEN, and permanently:** which contract was sanctioned. Both are coherent alone. Nothing in
  the artifact ranks them.

## The Thesis Defense

### Part A — Archaeology

Every claim traced to the parent by direct inspection, and the central claim by execution rather
than inspection. The Tier 3 note asserts the disagreement; the note was **not** taken as the
source of that finding. The finding rests on running the round trip, and the note is recorded
separately as a Concern the human stated.

That ordering matters here: the note happens to be right, and a run that accepted it would have
been right by luck. Tier 3 material is admissible as a Concern and inadmissible as proof.

### Part B — Closing an open item

Chapter 3's claim was closed by execution: the README's round-trip statement is false for the
delimiter-containing class and true otherwise. Both halves reported.

### Tests actually run

| Check | Result |
|---|---|
| Round trip on a delimiter-containing field | 2 fields written, 3 read |
| Quote characters in returned values | present — `'"hello'`, `'world"'` |
| Round trip on a delimiter-free record | unchanged |
| Existing test suite covers the failing class | **no** — no test input has a delimiter in a field |
| Tier 3 note establishes a negotiated Expectation | **no** — no counterparty exists |
| Artifact carries encoded Expectations | **yes** — 3: one contradicted, one violated, one untested |
| Secret sweep of captured evidence | 0 patterns fired |

### Honest gaps

1. **No assessment has been taken.** Four exams are defined; zero submission/evaluation pairs
   exist. No course here is passed.
2. **The parent has no git history of its own**, so change order is unavailable — the barest
   Pathway B case: code, docs, one note.
3. **No intent record exists**, so no intent-fidelity course was generated and none should be
   expected.
4. **The fix is deliberately not recommended.** Fixing the reader and fixing the writer are both
   coherent and produce different formats. That is the owner's decision.
5. **This parent is a synthetic fixture** authored for this repository, not a found project. It
   demonstrates the pathway mechanically; it does not demonstrate that the pathway survives a
   large real codebase.
6. **No CORE tier exists**, so these four courses carry method knowledge belonging in shared
   courses.

## Evidence tiers for every claim

| Claim | Tier |
|---|---|
| `parse` splits on every comma | **Reproduced now** — read at `src/app.py` |
| `format_field` quotes on delimiter | **Reproduced now** — read at `src/export.py` |
| Round trip returns three fields | **Reproduced now** — executed |
| README's claim is false as written | **Reproduced now** — executed against the claim |
| No test covers the failing class | **Reproduced now** — read at `tests/test_app.py` |
| The mismatch was unintentional | **Unsupported** — no evidence either way, and none exists |
| The quoting was added after the reader | **Unsupported** — plausible, unevidenced |

## GRADING RUBRIC FOR THESIS-inherited-service

### Criterion 1: Composition demonstrated, not asserted
- **Description:** Each chapter names the course IDs it stands on and cites at least one artifact
  produced under them.
- **Weight:** Primary objective | **Type:** Style | **Dependent Criteria:** none

### Criterion 2: The central finding rests on execution
- **Description:** States that the three-field read-back was obtained by running the round trip.
- **Rationale:** The Tier 3 note asserts the same conclusion. A thesis resting on the note would
  be correct by luck and would have promoted a monologue to proof.
- **Weight:** Primary objective | **Type:** Procedural | **Dependent Criteria:** 1

### Criterion 3: Absent intent declared, not filled
- **Description:** States that no intent record exists for this project.
- **Rationale:** Gate G9. A Pathway B curriculum that omits this reads as one that simply found
  no intent worth reporting.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** none

### Criterion 4: The unrankable decision left unranked
- **Description:** Does not recommend fixing the reader rather than the writer.
- **Rationale:** Negative constraint N4. Both are internally coherent, so a recommendation would
  be a preference presented as a finding.
- **Weight:** Primary objective | **Type:** Adversarial | **Dependent Criteria:** none

### Criterion 5: Fixture status disclosed
- **Description:** States that the parent is a synthetic fixture authored for this repository.
- **Rationale:** No silent caps. A reader assuming this was a found project would overrate what
  the run demonstrates about real codebases.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** none

### Criterion 6: No assessment claimed as passed
- **Description:** States that zero submission/evaluation pairs exist for the four defined exams.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** none
