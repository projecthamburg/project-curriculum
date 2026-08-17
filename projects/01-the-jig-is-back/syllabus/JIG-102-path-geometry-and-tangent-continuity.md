# JIG-102: Path Geometry and Tangent Continuity

**Crs:** 2 | **Prerequisite:** JIG-101 | **Phase:** Domain
**Reference impl / anchor:** upstream `code/PathEditor.tsx` at commit `70041403`;
transcript L771–L790 (the tangent-kink diagnosis and its four committed fixes).
**Prerequisite audit (2026-08-17):** JIG-101 supplies the commitment-tracing this course's exam
depends on; no other course exists to require.

> **Core Principle:** A path can be positionally continuous and direction-discontinuous at the same
> time. The eye reads the second as the object "jumping", which is why a defect described as
> jumping between points is a defect in tangents, not in positions.

## Coverage Declaration
- **Provides:** the ability to reason about cubic-Bezier anchors and control points, and about
  tangent continuity across a shared anchor.
- **Requires:** the ability to trace a commitment to shipped code (JIG-101).
- **Generalizes to modes:** Quantitative, Qualitative.
- **Capstone stage supplied:** the implementation-fidelity chapter of `THESIS-the-jig-is-back`.

## Learning Objectives
1. Decompose an SVG `d` string into anchors and control points.
2. Explain why collinearity of the two controls flanking an anchor produces a smooth tangent.
3. Identify the four fixes committed for the tangent-kink defect and locate each in the code.

## Curriculum

### Module 1: The decomposition
The first point is the `M` anchor; each subsequent cubic adds `[control1, control2, anchor]`. The
editor renders anchors as circles and controls as squares with dashed tangent lines to the anchor
that owns them.

### Module 2: Why kinks read as jumps
At an anchor shared by two cubics, the incoming and outgoing tangents are set by the flanking
control points. If those two controls are not collinear with the anchor, direction changes
instantaneously. The plane's rotation is derived from the tangent, so the rotation snaps — read by
the eye as a jump, though position is continuous throughout.

### Module 3: The four fixes, and where each lives
Committed at L777 and all four present at the pinned commit: auto-mirroring a control's partner
across the shared anchor, with `altKey` to break symmetry for an intentional corner; dragging an
anchor together with both flanking controls so local shape survives; a smooth-all pass; and
centered-difference tangent estimation in the production flight loop, which averages a small
window so residual kinks do not snap visibly.

### Module 4: Why the editor was not enough on its own
Fixes 1–3 act on authoring; fix 4 acts on playback. The defect survived the first three because
the production loop derived rotation from an instantaneous tangent. A defect can be real in the
artifact and also real in the renderer.

## Assignments

**Assignment 2.1** `[JIG-102-A1]` Decompose the shipped `FLIGHT_PATH` into anchors and controls and
report the count of each.

**Assignment 2.2** `[JIG-102-A2]` Locate each of the four committed fixes in the shipped code, with
file and line.

## Final Exam: Explain the kink and its fixes

Explain why the reported symptom "jumping across points" is a tangent defect rather than a position
defect, and account for all four committed fixes against the shipped code.

## GRADING RUBRIC FOR JIG-102 FINAL EXAM
*(inherits `protocol/MASTER_RUBRIC.md` in full)*

### Criterion 1: Continuity classes distinguished
- **Description:** States that the path is positionally continuous at the anchors where the symptom
  occurs.
- **Sources:** transcript L777.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 2: Direction discontinuity named as the cause
- **Description:** States that the cause is a direction discontinuity produced by control points
  that are not collinear across the shared anchor.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 1

### Criterion 3: Rotation derivation connected to the symptom
- **Description:** States that the plane's rotation is derived from the path tangent.
- **Rationale:** Without this link the diagnosis is a geometry fact with no connection to what the
  human actually saw on screen.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 2

### Criterion 4: Alt-to-break-symmetry identified
- **Description:** States that holding Alt breaks the auto-mirroring so a sharp corner can be
  authored deliberately.
- **Sources:** transcript L777; `code/PathEditor.tsx` (`altKey`).
- **Weight:** Not primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 5: Playback-side fix distinguished from authoring-side fixes
- **Description:** States that centered-difference tangent estimation acts in the production flight
  loop rather than in the editor.
- **Rationale:** Three of the four fixes change what can be authored; only this one changes what is
  rendered from an already-authored path. A response treating all four as editor features has not
  understood why the defect survived the first attempt.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 4

### Criterion 6: All four fixes located in shipped code
- **Description:** Cites a file for each of the four committed fixes.
- **Sources:** `code/PathEditor.tsx`, `code/HeroDemo.tsx` at commit `70041403`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none
