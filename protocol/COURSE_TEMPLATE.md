# COURSE_TEMPLATE — the clonable course skeleton

**Status:** v0.1-draft · Project Curriculum Protocol
**Depends on:** [`MASTER_RUBRIC.md`](MASTER_RUBRIC.md) — every assessment below inherits it whole.

Every CORE, ELEC, domain-track, and Independent Study course clones this skeleton exactly.

The **Coverage Declaration** is the load-bearing addition. It is what lets a course be recomposed by
a generator for an objective its author never saw. **Do not omit it — a course without one is not
seedable, only readable.**

---

## Skeleton, in order

```
# <ID>: <Title>

**Crs:** <N> | **Prerequisite:** <ID list, or "none (bootstrap)"> | **Phase:** <Core|Elective|Domain|Independent>
**Reference impl / anchor:** <the real file, dataset, session, prior run, or worked example this course is grounded in>
**Prerequisite audit (<YYYY-MM-DD>):** <one line confirming the prerequisite list still holds after the last governance amendment>

> **Core Principle:** <one paragraph — the thesis of this course>

## Coverage Declaration
- **Provides:** <what a generator can rely on this course for — a technique, a mental model, a specific assessment capability>
- **Requires:** <what must already be covered for this to compose correctly — stated as a capability, not just an ID>
- **Generalizes to modes:** <which generalization modes this course serves — see below>
- **Capstone stage supplied:** <which thesis chapter or deliverable this course's output can feed, or `none`>

## Learning Objectives
1. ...
2. ...            (3–5 items, no more)

## Curriculum
### Module 1: <title>
### Module 2: <title>
### Module 3: <title>

(each module: hypothesis → what was actually run or checked → real numbers or real examples
 → finding → any disclosed limitation)

## Assignments
**Assignment N.M:** <task, bracket-tagged `[<ID>-A<N>]` if it needs traceability-graph mapping>

## Final Exam: <Task Name>
<a single, executable task instruction — not a prompt for the student to interpret loosely>

## GRADING RUBRIC FOR <ID> FINAL EXAM
*(inherits MASTER_RUBRIC.md in full — 6 fields, 4 laws, 4 do-nots, dependency discipline)*

### Criterion 1: <title>
- **Description:** <single, self-contained, binary statement — always present>
- **Sources:** <exact filename/commit/citation — omit the line entirely if graded purely against the submission>
- **Rationale:** <the quote/data/reasoning showing why this is correct — omit the line entirely if self-evident>
- **Weight:** <...> | **Type:** <Extraction | Reasoning | Style> | **Dependent Criteria:** <none, or direct predecessors only>

(repeat, numbered, unique within this course)

## Dated Addenda
### <YYYY-MM-DD> <Topic> Addendum
### Quiz N — <title> [<ID>-QN]
### Assignment N — <title> [<ID>-AN]
### Final Exam Extension — <title> [<ID>-FEN]
```

---

## Generalization modes

A first-cut taxonomy — a starting hypothesis to reshape against real domain material, **not a closed
list.** Every course declares which mode(s) it serves, so a seeding translator can match an
unanticipated objective to the right subset of courses **by mode, not just by topic keyword**.

| Mode | What it means |
|---|---|
| **Quantitative** | The deliverable is a number, a calculation chain, or a statistical claim. |
| **Qualitative** | The deliverable is a judgment call, classification, or synthesis experts would converge on without arithmetic. |
| **Procedural** | The deliverable is "did the process get followed correctly" — steps, sequencing, compliance. |
| **Generative** | The deliverable is new content produced to spec (a plan, a design, a report) rather than an analysis of existing material. |
| **Adversarial** | The deliverable is finding where something breaks, overclaims, or fails to hold up. This is the mode the defense apparatus runs in. |

---

## Why the Coverage Declaration is load-bearing, not decorative

Without it, a seeding translator has only prose to search over, and **prose does not compose**. You
get a course that reads beautifully and cannot be programmatically matched to an objective its
author never anticipated.

With it, seeding an unforeseen objective becomes a mechanical sequence:

1. Enumerate what the objective needs (`GENERATION_MACHINERY.md` Part A).
2. Diff that against every course's `Provides` and `Generalizes to modes`.
3. Select the covering subset.
4. Check the subset's `Requires` are mutually satisfied — or trigger gap detection to spin up an
   Independent Study that closes the gap.
5. Compose.

This is the mechanism, not a metaphor for it. In software terms a course is an **interface**:

```
Capability Unit
  PROVIDES:     X
  REQUIRES:     A, B
  GENERALIZES:  modes C, D
  CAPSTONE:     E
```

Composition can then be reasoned about, and a coverage gap becomes a detectable fact rather than
something a human notices late.

---

## Grounding requirement

Every course is **grounded in real material for its own objective** — an actual file, commit,
session, dataset, or run. Abstract theory disconnected from the objective is the single
most-checked defect in the meta-rubric (`GENERATION_MACHINERY.md` Part D, Criterion 1), because a
course anchored to nothing real is a generic response wearing the costume of a targeted one.

If a course genuinely has no real anchor yet, that is a finding to state, not a gap to paper over.
