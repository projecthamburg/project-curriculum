# Coverage profile — seed:2026-08-17:intent-fidelity

**Produced by:** `protocol/GENERATION_MACHINERY.md` Part A, run against the objective in
`seed.yaml` and the reviewed evidence in `governance/ice-outputs/ch01`.
**Produced before any course was selected or written**, which is the point of Part A.

---

## Part A — translation

### 1. Stated goal → Extraction / Reasoning criteria

The objective asks for three things that can be checked: reconstruct the intent, reconstruct
the implementation decisions, and determine whether the code satisfies them.

| Needed capability | Because |
|---|---|
| Trace a recorded commitment to the shipped artifact that should satisfy it | The objective's verb is "determine whether the current code satisfies them" |
| Read a cubic-Bezier path as anchors and control points, and reason about tangent continuity across an anchor | E3's defect and its four fixes are entirely about this |
| Reason about an animation timing pipeline: easing, duration, and arc-length sampling | E4's root cause and E5's duration request are both here |
| Explain why the tool exists, not merely what it does | E1 and I1 — the repository's reason for existing is an intent-transfer failure |

### 2. Implicit expectations → Golden-response criteria

Never written down by the human, but a competent answer satisfies them:

- **A divergence is reported with its evidence bound attached.** The upstream commit postdates
  the session by five weeks. An answer that reports "the commitment was broken" without that
  caveat is wrong, not merely incomplete.
- **A claim about the code cites a file and line, resolved against the pinned commit.**
- **A quantitative claim states the number.** "The duration differs" is not an answer; "4100
  where 7000 was committed" is.
- **A supersession is distinguished from a defect.** The trail-reveal change was correct
  engineering; the shipped flight duration is unexplained. Same surface shape, different kind.

### 3. Stated worries → Negative constraints

The human stated no worries in their own words. These are derived from the objective's own
risk surface, and are checks that something did *not* happen:

- **N1.** The answer does not claim a commitment was broken where a later deliberate revision
  is equally consistent with the evidence.
- **N2.** The answer does not treat upstream's README as ground truth about the code. It is one
  input; the code is the record.
- **N3.** The answer does not report a `grep` hit as a finding without reading the surrounding
  code. (The `mask` case would have produced a false positive exactly this way.)
- **N4.** No upstream content is redistributed. `seed.yaml` declares `reference-only`.

---

## Target coverage profile

What the run needs, before looking at any catalog:

| # | Provides | Modes |
|---|---|---|
| P1 | Trace an intent from ask → interpretation → commitment → shipped artifact, and classify the outcome | Qualitative, Adversarial |
| P2 | Reason about cubic-Bezier path geometry and tangent continuity across anchors | Quantitative, Qualitative |
| P3 | Reason about an animation timing pipeline and locate a discontinuity defect in it | Quantitative, Procedural |
| P4 | Explain and evaluate a purpose-built authoring instrument, including preview/production parity | Qualitative, Procedural |

---

## Part B step 3 — catalog diff

**Catalog consulted:** `syllabus/curriculum_prerequisites.json`.
**Courses in catalog: 0.** This workspace has no CORE tier yet.

| Target | Covered by | Action |
|---|---|---|
| P1 | — | **gap** → generate |
| P2 | — | **gap** → generate |
| P3 | — | **gap** → generate |
| P4 | — | **gap** → generate |

All four are gaps. Part C fires for each.

**Bootstrap exception invoked.** Per `protocol/MASTER_SYLLABUS.md` §Bootstrap exception, the
first course into an empty catalog may declare `Requires: none (bootstrap)`. **JIG-101 is the
only course in this run that uses it**; JIG-102, 103 and 104 all require JIG-101 and therefore
satisfy Part D Criterion 2 normally. Recorded here as the run's log of that use.

---

## Generated courses

| ID | Provides | Closes |
|---|---|---|
| `JIG-101` | The intent record: ask → commitment → shipped artifact | P1 |
| `JIG-102` | Path geometry and tangent continuity | P2 |
| `JIG-103` | The timing pipeline and its discontinuity class of defect | P3 |
| `JIG-104` | The instrument: why the editor exists and what parity it must hold | P4 |

## Bounds on this run — stated, not implied

- **One session is the entire conversational record.** 5 human turns. Whatever intent was
  formed before or after it is not recoverable from public evidence.
- **A five-week gap sits between the session and the pinned commit**, and nothing documents it.
- **No CORE tier exists**, so these four courses carry method knowledge that would normally
  live in shared courses. They will need splitting once a CORE tier exists.
- **No assessment has been taken.** The courses define exams; no submission or evaluation pair
  exists yet, so no course is "passed" in this run.
