# JIG-101: The Intent Record — Ask, Commitment, Shipped Artifact

**Crs:** 1 | **Prerequisite:** none (bootstrap) | **Phase:** Core
**Reference impl / anchor:** `governance/ice-outputs/ch01_2026-08-17_paper-plane-path-editor_ICE.md`;
upstream `transcript.md` at commit `70041403`; `code/HeroDemo.tsx` at the same commit.
**Prerequisite audit (2026-08-17):** the catalog was empty at generation time; this is the run's
single use of the bootstrap exception, logged in `COVERAGE_PROFILE.md`.

> **Core Principle:** A commitment and its implementation are two different records, and the gap
> between them is information rather than error. This course teaches an agent to trace one to the
> other and to classify what it finds — satisfied, superseded, or unexplained — without collapsing
> the third case into the first.

## Coverage Declaration
- **Provides:** the ability to trace an intent from ask → interpretation → commitment → shipped
  artifact, and to classify the outcome against a stated evidence bound.
- **Requires:** the ability to read a session transcript closely and quote it with line numbers.
- **Generalizes to modes:** Qualitative, Adversarial.
- **Capstone stage supplied:** the intent-fidelity chapter of `THESIS-the-jig-is-back`.

## Learning Objectives
1. Extract an Ask → Response → Lock-in chain from a transcript, with quotes and line numbers.
2. Classify a lock-in as locked, unlocked, or superseded, using only what the record supports.
3. Resolve a commitment against the shipped code at a pinned commit, citing file and line.
4. State the evidence bound that limits a divergence claim, before making the claim.

## Curriculum

### Module 1: Five turns and what they carry
The captured session has 5 human turns against 69 agent turns. Turn count is a poor proxy for
intent density: E5 alone carries an acceptance, a pasted artifact, and a new request. The
extraction unit is the *act*, not the message.

### Module 2: Lock-in is evidence, not judgment
E2 is locked by delivery and subsequent use — the human exercised the tool rather than
re-litigating the ask. E3 is unlocked because E4 reports the symptom persisting. E4 is locked by
E5's opening words. Each judgment is made from the record; none is inferred from whether the work
looked good.

### Module 3: Resolving a commitment against code
The agent committed at L1299 to `FLIGHT_MS` 4500 → 7000. `code/HeroDemo.tsx:42` reads
`const FLIGHT_MS = 4100;`. Both are checkable facts. The conclusion "the commitment was broken"
is not, because the pinned commit postdates the session by five weeks.

### Module 4: The bound comes first
Upstream's session ran 2026-05-05; the pinned commit is 2026-06-12. Any divergence found is a
divergence between *what was committed to in the session* and *what shipped* — never proof that a
commitment was abandoned. State the bound before the finding, so the finding cannot be read
without it.

## Assignments

**Assignment 1.1** `[JIG-101-A1]` Produce the Ask → Response → Lock-in chain for all five human
turns, with line numbers, and a lock-in marker for each.

**Assignment 1.2** `[JIG-101-A2]` For each of the two commitments in E5, resolve it against the
pinned commit and classify the outcome with its evidence bound attached.

## Final Exam: Resolve E5's two commitments

Given the transcript and the code at commit `70041403`, report for each of the two commitments in
the agent's L1299 response: the committed value or artifact, the shipped value or artifact with a
file and line citation, and the classification.

## GRADING RUBRIC FOR JIG-101 FINAL EXAM
*(inherits `protocol/MASTER_RUBRIC.md` in full)*

### Criterion 1: Committed duration identified
- **Description:** States that the agent committed to changing `FLIGHT_MS` from 4500 to 7000.
- **Sources:** `sources/2026-05-05_specstory_transcript.md` L1299.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 2: Shipped duration identified
- **Description:** States that `code/HeroDemo.tsx` line 42 defines `FLIGHT_MS` as 4100.
- **Sources:** upstream `code/HeroDemo.tsx:42` at commit `70041403`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 3: Direction of the divergence stated
- **Description:** States that 4100 is faster than the 4500 the human asked to slow down from.
- **Rationale:** The gap is not merely "short of 7000". A response that reports only the distance
  from the committed value misses that the change moved opposite to the request.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 1, 2

### Criterion 4: Evidence bound attached to the divergence claim
- **Description:** States that the pinned commit is dated 2026-06-12 and the session 2026-05-05,
  and that the five-week gap is uncaptured.
- **Rationale:** `protocol/THESIS_AND_DEFENSE.md` treats a bounded result presented as complete as
  the defect the defense layer exists to catch.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 3

### Criterion 5: Divergence not asserted as a broken commitment
- **Description:** Does not state that the agent failed to honour, abandoned, or broke the
  duration commitment.
- **Rationale:** Negative constraint N1 in `COVERAGE_PROFILE.md`. A later deliberate revision is
  equally consistent with the evidence, and nothing in the record distinguishes the two.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 4

### Criterion 6: Path origin divergence identified
- **Description:** States that the human's pasted path begins `M 746 83` while the shipped
  `FLIGHT_PATH` begins `M 716 77`.
- **Sources:** transcript L1293; `code/HeroDemo.tsx:47–50`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 7: Mechanism distinguished from artifact
- **Description:** States that the runtime-translation mechanism the agent committed to is present
  in the shipped code while the specific curve is not.
- **Rationale:** `FLIGHT_PATH_ORIGIN_X`/`_Y` exist and hold the shipped path's own origin, which is
  exactly the committed mechanism operating on a different curve. Conflating the two produces a
  finding that the code contradicts.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 6
