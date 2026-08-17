# JIG-103: The Timing Pipeline and Its Discontinuity Defect

**Crs:** 3 | **Prerequisite:** JIG-101 | **Phase:** Domain
**Reference impl / anchor:** transcript L1172–L1190 (the easing diagnosis);
upstream `code/HeroDemo.tsx` at commit `70041403`.
**Prerequisite audit (2026-08-17):** JIG-101 supplies the commitment-tracing the exam depends on.

> **Core Principle:** Two symptoms with one root cause are one defect. A plane that snaps forward
> mid-flight and a plane that never reaches the end of its path are the same discontinuous easing
> function observed at two different moments.

## Coverage Declaration
- **Provides:** the ability to reason about an animation timing pipeline and to locate a
  discontinuity defect within it.
- **Requires:** the ability to trace a commitment to shipped code (JIG-101).
- **Generalizes to modes:** Quantitative, Procedural.
- **Capstone stage supplied:** the implementation-fidelity chapter of `THESIS-the-jig-is-back`.

## Learning Objectives
1. Evaluate a piecewise easing function for continuity at its breakpoint.
2. Explain how one discontinuity produces both a mid-flight snap and an unfinished path.
3. Determine from shipped code whether a diagnosed defect was actually removed.

## Curriculum

### Module 1: The function
The easing in both files at the time of the report was
`const e = t < 0.45 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 3) / 6 - 0.165;`
Evaluating both branches at t=0.45 gives different values, so the output jumps at the breakpoint.

### Module 2: Two symptoms, one cause
The jump at t=0.45 advances the plane instantaneously — the snap the human reported twice. The
second branch does not reach 1 at t=1, so the plane stops short of the path end. Both follow from
the single function.

### Module 3: Where the human's diagnosis was wrong, and why that matters
The human reported the symptom as persisting "even after smoothing", implicitly attributing it to
the path or the smoothing pass. The agent's reply opens by rejecting that attribution: "it's not in
the path or the smoothing. It's in my easing function." A correct diagnosis contradicted the
reporter, and the record preserves both.

### Module 4: Verifying removal
The piecewise expression is absent from `HeroDemo.tsx` and `PathEditor.tsx` at the pinned commit.
Searching for the bare string `0.45` is not sufficient evidence: it appears four times in the
shipped code, in `strokeWidth` and `rgba` values entirely unrelated to easing. The check must be
against the expression, not the constant.

## Assignments

**Assignment 3.1** `[JIG-103-A1]` Evaluate both branches at t=0.45 and report the size of the jump.

**Assignment 3.2** `[JIG-103-A2]` Determine whether the defective easing is present at the pinned
commit, and state what was searched for.

## Final Exam: Account for both symptoms and verify the fix

Explain how a single easing function produced both reported symptoms, and establish whether it is
present in the shipped code.

## GRADING RUBRIC FOR JIG-103 FINAL EXAM
*(inherits `protocol/MASTER_RUBRIC.md` in full)*

### Criterion 1: Breakpoint identified
- **Description:** States that the easing function branches at t=0.45.
- **Sources:** transcript L1184.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 2: Discontinuity established by evaluation
- **Description:** States that the two branches evaluate to different values at t=0.45.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 1

### Criterion 3: Snap symptom attributed to the discontinuity
- **Description:** States that the jump in output at the breakpoint advances the plane
  instantaneously.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 2

### Criterion 4: Unfinished-path symptom attributed to the same function
- **Description:** States that the second branch does not reach 1 at t=1.
- **Rationale:** Treating the unfinished path as a separate defect is the error the agent's own
  diagnosis corrected; one function accounts for both reports.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 2

### Criterion 5: Reporter's attribution identified as incorrect
- **Description:** States that the human attributed the persisting symptom to the path or the
  smoothing, and that the cause was in neither.
- **Sources:** transcript L1172, L1178.
- **Weight:** Not primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 6: Absence of the defective easing established
- **Description:** States that the piecewise expression is absent from both `HeroDemo.tsx` and
  `PathEditor.tsx` at commit `70041403`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 7: Constant search rejected as sufficient evidence
- **Description:** States that the literal `0.45` occurs in the shipped code in contexts unrelated
  to easing.
- **Rationale:** Negative constraint N3 in `COVERAGE_PROFILE.md`. A search for the constant returns
  four hits at the pinned commit, none of them the easing function, so a response resting on that
  search has not established the fix.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 6
