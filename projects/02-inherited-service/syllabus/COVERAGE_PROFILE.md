# Coverage profile — seed:2026-08-17:pathway-b-inheritance

**Produced by:** `protocol/GENERATION_MACHINERY.md` Part A, run against the objective and the
codebase index. **Pathway B** — determined by `governance/intake.py`, recorded in
`governance/reports/intake_inherited-service.json`.

> **No intent record exists for this project.** Every statement below about *why* the code is
> as it is would be inference from the artifact, so no such statement is made. What follows is
> built from structure, behaviour, and one Tier 3 note that carries Concerns and an Idea but
> — being a monologue — no Expectation.

---

## Part A — translation

### 1. Stated goal → Extraction / Reasoning criteria

The objective asks for two checkable things: what the service does, and where its components
disagree with each other and with its documentation.

| Needed capability | Because |
|---|---|
| Read the read path and the write path and state each one's format contract | "what this inherited service does" |
| Demonstrate a disagreement by execution, not by reading | "where its own components disagree" |
| Compare a documentation claim against observed behaviour | "and with its documentation" |
| Distinguish an absent intent record from an inferred one | Pathway B's governing rule |

### 2. Implicit expectations → Golden-response criteria

- **A disagreement is shown by running it**, with the actual input and the actual output. A
  reading of two functions is an argument; a round trip is evidence.
- **A quantitative claim states the number.** "The field count changes" is not an answer; "two
  fields written, three fields read" is.
- **Absence of intent is stated, never filled in.** "The quoting was added later" is a story
  the evidence does not support, however plausible.

### 3. Stated worries → Negative constraints

Derived from the objective's risk surface and from the note's own C2/C3:

- **N1.** The answer does not assert which of the two behaviours was intended.
- **N2.** The answer does not treat the README as ground truth about the code.
- **N3.** The answer does not treat the Tier 3 note as an Expectation, or as evidence of what
  anyone agreed.
- **N4.** The answer does not recommend a fix as though the choice were technical. Both sides
  are internally coherent; only together are they not.

---

## Target coverage profile

| # | Provides | Modes |
|---|---|---|
| P1 | State the format contract each side of the pipeline implements | Qualitative, Procedural |
| P2 | Demonstrate a component disagreement by execution | Quantitative, Adversarial |
| P3 | Test a documentation claim against observed behaviour | Adversarial |
| P4 | Work correctly under an absent intent record | Qualitative |

## Part B step 3 — catalog diff

**Courses in catalog: 0.** All four are gaps; Part C fires for each.

**Bootstrap exception invoked once** (`INH-101`), per `protocol/MASTER_SYLLABUS.md`. The other
three require it.

| ID | Provides | Closes |
|---|---|---|
| `INH-101` | The two format contracts, read from the code | P1 |
| `INH-102` | The disagreement, demonstrated by execution | P2 |
| `INH-103` | Documentation and test coverage against behaviour | P3 |
| `INH-104` | Working under an absent intent record | P4 |

## Bounds on this run — stated, not implied

- **No intent record exists.** No Ask → Response → Lock-in chain is possible, so no
  intent-fidelity course is generated and none should be expected.
- **The parent has no git history of its own**, so even change-order evidence is unavailable.
  This is the barest Pathway B case: code, docs, and one note.
- **One Tier 3 note is the entire human-side record**, and it carries Concerns and an Idea only.
- **No CORE tier exists**, so these four courses carry method knowledge that belongs in shared
  courses.
- **No assessment has been taken.**
