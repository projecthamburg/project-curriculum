# JIG-104: The Instrument — Why the Editor Exists and What Parity It Must Hold

**Crs:** 4 | **Prerequisite:** JIG-101 | **Phase:** Domain
**Reference impl / anchor:** transcript L12–L58 (the problem and the build commitment);
upstream `README.md` and `code/PathEditor.tsx` at commit `70041403`.
**Prerequisite audit (2026-08-17):** JIG-101 supplies the intent record this course reasons over.

> **Core Principle:** The editor is not a feature of the animation. It exists because describing a
> curve in prose was not converging, and its whole value rests on one property: what the preview
> shows must be what production renders. A preview that only approximates production reintroduces
> the guessing the instrument was built to remove.

## Coverage Declaration
- **Provides:** the ability to explain and evaluate a purpose-built authoring instrument, including
  the preview/production parity that determines whether it works.
- **Requires:** the ability to trace an intent record (JIG-101).
- **Generalizes to modes:** Qualitative, Procedural.
- **Capstone stage supplied:** the composition chapter of `THESIS-the-jig-is-back`.

## Learning Objectives
1. State the failure mode that caused the instrument to be built, from the record.
2. Explain why preview/production parity is the property the instrument's value depends on.
3. Explain why arc-length-sampled dots replaced a mask-based trail reveal.

## Curriculum

### Module 1: The failure that produced the tool
At L12 the human asks for "a better way to help draw a path out for you". The agent's first option
names the failure directly: hand-typing Bezier control points blind, and the human "translating
intent through me" instead of handing over the finished curve. The tool exists to delete that
translation step.

### Module 2: What was actually asked for
L44 asks for three things: edit live in the real hero, view it live, and copy something back out.
The commitment at L51 answers all three. `?editPath=1` swaps the production demo for the editor
inside the same page, which is what makes "in the real hero" true rather than approximately true.

### Module 3: Parity is the whole product
Upstream states the live preview uses the same RAF logic and physics constants as production. This
is the property that makes the instrument trustworthy: an approximate preview would return the
human to guessing, one level removed. Round-tripping — copy the `d` string out, import it back —
is what makes the tool usable across sessions.

### Module 4: A design decision with no recorded intent
The trail was originally revealed with an SVG mask. A mask cannot reveal a self-intersecting path
correctly, because the same screen region belongs to two different parametric positions. The
replacement samples N circles at fixed arc-length intervals, each storing its own `t` and revealing
when the plane passes it. `code/HeroDemo.tsx:202` records the reason. **No human turn in the
captured session requests this change** — it is real engineering with no intent record behind it,
which is itself a finding about the limits of a single-session evidence corpus.

## Assignments

**Assignment 4.1** `[JIG-104-A1]` State, quoting the transcript, the failure mode that caused the
instrument to be built.

**Assignment 4.2** `[JIG-104-A2]` Explain why a mask cannot correctly reveal a self-intersecting
path, and what the dots approach does instead.

## Final Exam: Evaluate the instrument

Explain why the editor exists, what property its value depends on, and why the trail-reveal
mechanism was replaced.

## GRADING RUBRIC FOR JIG-104 FINAL EXAM
*(inherits `protocol/MASTER_RUBRIC.md` in full)*

### Criterion 1: Originating failure identified
- **Description:** States that Bezier control points were being hand-typed without visual feedback.
- **Sources:** transcript L19.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 2: Intent-translation framed as the cost being removed
- **Description:** States that the tool removes the step of translating the desired curve through a
  prose description.
- **Rationale:** A response treating the editor as a convenience has missed why it was built; the
  agent's own words at L19 name the translation step as the problem.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 1

### Criterion 3: In-page activation identified
- **Description:** States that the editor is reached by the `editPath=1` URL parameter and renders
  in place of the production demo.
- **Sources:** `code/HeroDemo.tsx`, `code/PathEditor.tsx` at commit `70041403`.
- **Weight:** Not primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 4: Parity named as the load-bearing property
- **Description:** States that the preview uses the same flight logic and physics constants as
  production.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 5: Consequence of losing parity stated
- **Description:** States that an approximate preview would require the author to guess at the
  difference between preview and production.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 4

### Criterion 6: Mask failure attributed to self-intersection
- **Description:** States that a mask cannot reveal a self-intersecting path correctly because one
  screen region corresponds to more than one parametric position on the path.
- **Sources:** `code/HeroDemo.tsx:202`.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** none

### Criterion 7: Replacement mechanism described
- **Description:** States that the trail is drawn as circles sampled at fixed arc-length intervals,
  each revealing when the plane passes its own parametric position.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** 6

### Criterion 8: Absence of a recorded request acknowledged
- **Description:** States that no human turn in the captured session requests the trail-reveal
  change.
- **Rationale:** The change is real and correct, and no intent record exists for it. A response
  that supplies a plausible-sounding request for it has fabricated evidence.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 6
