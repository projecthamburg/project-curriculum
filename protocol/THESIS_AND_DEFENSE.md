# THESIS AND DEFENSE — the capstone and its adversarial audit

**Status:** v0.1-draft · Project Curriculum Protocol
**Depends on:** [`MASTER_RUBRIC.md`](MASTER_RUBRIC.md) (a thesis rubric is the same 6-field
contract) · [`COURSE_TEMPLATE.md`](COURSE_TEMPLATE.md) (a thesis's prerequisites are literally every
course its domain track composed).

## What a thesis is

**Not a bigger course.** A thesis is the demonstration that the composed courses actually add up to
something. Technically: a **composition proof**.

One thesis per domain track per seeding run. Its prerequisites are every CORE, ELEC, domain-track and
Independent Study course the seeding translator selected for that objective.

> A course teaches one capability. A thesis demonstrates that the prerequisite courses **function
> together** against the seeded objective.

---

## Thesis skeleton

```
# THESIS-<domain>: <Title>

**Tier:** Thesis | **Prerequisites:** ALL courses this run's seeding translator selected for <domain>
**Candidate's standing question:** <one italicized research question the whole run answers>
**Citation discipline in effect:** <which mode from MASTER_RUBRIC.md §5 — internal record, DOI, or both>

> **Core Principle:** ...

## Thesis Statement
<one paragraph naming the exact deliverable, then a table:
 Deliverable | Made real by | Evidence
 — each row citing the specific course or study and its own measured numbers>

## Chapter Plan
### Chapter N — <name>
- **Stands on:** <course IDs>
- **Already real:** <what's proven, with real citations per MASTER_RUBRIC.md §5>
- **OPEN:** <what's still missing, with the measured evidence that it's missing — never silently
             dropped from a later revision without a dated closure note>

## Quizzes / Assignments / Final Exam: The Thesis Defense
<same nested-rubric structure as any course — MASTER_RUBRIC.md §7>

## GRADING RUBRIC FOR THESIS-<domain>
(6-field criteria, same contract; criteria may depend on each other, forming their own small
 acyclic graph per MASTER_RUBRIC.md §4)
```

---

## Findings format

For a run whose deliverable is a **set of discrete findings** rather than one integrated artifact:

- Each finding is graded as its own mini-exam submission against the domain track's rubric.
- The thesis chapter for that sub-area reports: how many findings were required, how many passed full
  citation and rubric validation, and **which were discarded and why** — rather than silently
  omitted.

> **No silent caps.** If coverage was bounded — a source that couldn't be reached, a sub-area with
> fewer than the required count of valid findings, a sweep that was truncated — **say so explicitly
> in the chapter.** A bounded result presented as if complete is exactly the overclaim the defense
> layer below exists to catch.

---

## Why a defense layer exists at all

The meta-rubric (`GENERATION_MACHINERY.md` Part D) catches format defects in generated output. **It
does not catch overclaiming**, because the generator and the meta-rubric share the same blind spots.
Neither is independently checking "is this actually true" — only "is this correctly shaped."

The predecessor system's own history is the proof: its first defense passed cleanly, and a *second*
defense was required specifically because that pass's own evidence, plus an outside audit, surfaced
conflation between **"implemented", "reproduced once on one fixture", "integrated", and "generic"** —
four different maturity levels that had been used interchangeably.

**Assume the same conflation risk exists in every run from the start.**

---

## Defense — adversarial build-and-prove

Convened with a fixed constraint set and real input material, executed by **independently-scoped
reviewers** (human or agent instances) each assigned one slice, journaling as they go.

Each reviewer's entry has this shape:

- **Part A — Archaeology.** Trace every input and claim to its real origin, **by direct inspection,
  not assumption.**
- **Part B — Close an open item.** Do new real work against real material, not a synthetic stand-in.
- **Tests.** What was actually run, pass/fail, real numbers.
- **Honest gaps.** Numbered, explicit, never silently omitted.

Merge into a single journal: recon and plan, a courses-applied mapping (**every claim cites which
course's specific technique was used, not merely its topic**), the centrepiece finding, and a
synthesis — what discipline held, what capabilities transferred, what gaps remain.

---

## Defense-2 — the adversarial claim audit

Run whenever defense-1's own evidence, or an outside check, reveals maturity conflation.

**Five evidence tiers**, applied to every claim:

| Tier | Meaning |
|---|---|
| **Reproduced now** | Run again, just now, and it worked |
| **Historically supported** | Worked before, with a record; not re-run |
| **Implemented and test-covered** | Code exists and tests cover it; not necessarily exercised end to end |
| **Partial / fixture-specific** | Worked on one fixture or one path only |
| **Unsupported / retracted** | No evidence, or previously claimed and now withdrawn |

**CLAIM-LEDGER** — a table of `Claim | Tier | Evidence, scope, correction | Courses`. This is the
artifact that **actually retracts or downgrades prior claims**. A claim like "all findings passed" is
retracted here as a stale snapshot once a later count shows otherwise.

**Round structure** — each round targets one specific overclaim risk relevant to the domain. For a
findings pipeline: is every claimed DOI resolvable *right now*, not merely at generation time; is
"validated" being used consistently; is one source being treated as ground truth when it is actually
one input among several.

**LINEAGE-COMPARISON** — an honesty check about credit and originality. Distinguish "used a vendored
or external tool as-is" from "studied a reference and reimplemented" from "inspired by, never actually
integrated", so credit is never overclaimed.

**TEST-RECORD** — environment plus focused pass/fail counts. **Skips and crashes are never silently
converted into passes.**

---

## Scope discipline for defenses

Small governance changes after a defense-2 do **not** need a "defense-3" folder. Handle them as dated
in-place revision sections in the thesis itself, plus a new `AMENDMENT` file if the change is
cross-cutting.

**Reserve full defense folders for whole-run audits, not incremental fixes.**

---

## The standing epistemic rule

Everything above is one application of a single commitment, which holds at every level of a
conformant implementation:

> **Knowledge claims must eventually cash out against observable reality.**
> Each build stage ends with a real run against real material — not "the tests pass", and never
> documentation asserting that something worked as evidence that it did.

This rule was learned the hard way in the predecessor system: audits missed real defects because
nobody actually ran the software. Concrete bugs were subsequently found by executing components
against real targets, and prior documentation was corrected where suspected failures did not
reproduce.

The defense layer is that rule applied to a whole composed run. The rule itself applies to every
commit.
