# THESIS-the-jig-is-back: Intent Fidelity in a Single-Session Build

**Tier:** Thesis | **Prerequisites:** JIG-101, JIG-102, JIG-103, JIG-104
**Candidate's standing question:** *Does the shipped implementation satisfy the intent recorded in
the only conversation that produced it — and where it does not, can the evidence say why?*
**Citation discipline in effect:** internal record of truth (transcript line numbers; file and line
at the pinned commit `70041403`). No published-literature claim is made, so no DOI applies.

> **Core Principle:** A thesis is not a bigger course. These four courses each teach one capability;
> this document exists to demonstrate that they compose into an answer to the seeded objective — and
> to say plainly where they compose into "the evidence cannot tell us".

## Thesis Statement

The four generated courses compose into a full traversal of one intent record: from the failure that
caused the work to begin, through the two defects reported and fixed, to the shipped artifact. Three
of the five recorded expectations are satisfied by the shipped code. Two commitments are not, and
the captured evidence is insufficient to say whether they were abandoned or deliberately revised.

| Deliverable | Made real by | Evidence |
|---|---|---|
| Intent record for all 5 human turns | JIG-101 | `ch01` E1–E5, each quoted with a line number |
| Tangent-kink defect and its 4 fixes traced to code | JIG-102 | all four located at commit `70041403` |
| Easing defect accounted for and its removal verified | JIG-103 | piecewise expression absent from both files |
| The instrument explained, and one undocumented decision surfaced | JIG-104 | `HeroDemo.tsx:202`; no requesting turn exists |
| Two unexplained divergences, bounded | JIG-101 | `FLIGHT_MS` 4100 vs 7000; `M 716 77` vs `M 746 83` |

## Chapter Plan

### Chapter 1 — Intent fidelity
- **Stands on:** JIG-101
- **Already real:** All five human turns extracted as Ask → Response → Lock-in chains with line
  numbers. E2 and E4 are locked; E1 and E3 are unlocked with the record showing why; E5 is locked
  and carries three separate acts in one turn.
- **OPEN:** E5's two commitments do not hold at the pinned commit. `FLIGHT_MS` is 4100 where 7000
  was committed — and faster than the 4500 the human asked to slow down from. The shipped
  `FLIGHT_PATH` begins `M 716 77`, not the pasted `M 746 83`. Neither is explained by the evidence.

### Chapter 2 — Implementation fidelity
- **Stands on:** JIG-102, JIG-103
- **Already real:** All four committed tangent fixes are present. The defective piecewise easing is
  absent from both files — verified against the expression, not against the constant `0.45`, which
  still occurs four times in unrelated `strokeWidth` and `rgba` values.
- **OPEN:** Nothing. Both defect chains close cleanly, which is the strongest positive result in
  this run.

### Chapter 3 — Composition
- **Stands on:** JIG-104, and all three prior chapters
- **Already real:** The instrument's purpose, its activation path, and its parity requirement are
  established from the record and the code. The trail-reveal supersession is verified as real and
  correctly motivated.
- **OPEN:** The trail-reveal change has **no requesting turn anywhere in the captured session.** It
  is real engineering with no intent record behind it — a genuine limit of a single-session corpus,
  not a defect in the work.

## The Thesis Defense

### Part A — Archaeology

Every claim above was traced to its origin by direct inspection at commit `70041403`, not by
assumption and not from upstream's own description of itself.

One claim did not survive first inspection. A search for `mask` in the shipped code returns hits in
`HeroDemo.tsx`, which appears to contradict upstream's statement that the mask-based trail reveal
was thrown out. Reading the surrounding code resolves it: those hits are `chromeMask`, an unrelated
element that hides the plane behind a chrome strip. **The grep produced a false finding; reading
the code removed it.** This is negative constraint N3 catching a real error inside this very run.

### Part B — Closing an open item

Chapter 1's `FLIGHT_MS` divergence was closed as far as public evidence permits: the committed value
(7000, transcript L1299), the shipped value (4100, `HeroDemo.tsx:42`), the direction of the
discrepancy relative to the request, and the five-week uncaptured gap between session and commit.
The item is closed as **unexplained-and-bounded**, not as a broken commitment.

### Tests actually run

| Check | Result |
|---|---|
| Transcript imported and parsed | 65 non-empty turns; all 5 human turns preserved |
| Human turns retrievable by speaker filter | 5 of 5 |
| Search index built over transcript + upstream code | 7 sources, 93 chunks |
| Secret sweep of captured evidence | 0 patterns fired |
| Security scan of tracked project files | 0 secret-shaped findings |
| Four E3 fixes present in code | 4 of 4 |
| Defective easing present in code | absent from both files |
| `FLIGHT_MS` matches commitment | **no** — 4100 vs 7000 |
| Shipped path matches pasted path | **no** — `M 716 77` vs `M 746 83` |

### Honest gaps

1. **No assessment has been taken.** Four exams are defined; no submission/evaluation pair exists.
   No course in this run is "passed" — and per `protocol/MASTER_SYLLABUS.md`, an exam-taker and its evaluator
   must never be the same pass, so this run could not have graded itself in any case.
2. **One session is the entire conversational corpus.** Intent formed before or after it is not
   recoverable from public evidence.
3. **Five weeks between the session and the pinned commit are undocumented.** Both open items in
   Chapter 1 sit inside that gap.
4. **No CORE tier exists.** These four courses carry method knowledge that belongs in shared
   courses; they will need splitting once a CORE tier exists.
5. **The bootstrap exception was used once** (JIG-101), logged in `COVERAGE_PROFILE.md`.
6. **Upstream states no licence.** Nothing upstream is redistributed here; `seed.yaml` records the
   pointer and the run resolves it at execution time.

## Evidence tiers for every claim in this thesis

Per `protocol/THESIS_AND_DEFENSE.md`, applied to avoid the maturity conflation that layer exists to
catch:

| Claim | Tier |
|---|---|
| All four tangent fixes present | **Reproduced now** — searched at the pinned commit |
| Defective easing absent | **Reproduced now** — searched for the expression in both files |
| `FLIGHT_MS` is 4100 | **Reproduced now** — read at `HeroDemo.tsx:42` |
| Shipped path origin is `M 716 77` | **Reproduced now** — read at `HeroDemo.tsx:47–50` |
| The five Ask → Response → Lock-in chains | **Reproduced now** — quoted with line numbers |
| Preview uses production physics constants | **Historically supported** — upstream's README states it; not independently verified line by line |
| Trail dots replaced a mask reveal | **Implemented and test-covered** — the mechanism and its stated reason are both in the code; the original mask implementation is not in the repository's history to compare against |
| Why `FLIGHT_MS` and the path diverge | **Unsupported** — no evidence either way |

## GRADING RUBRIC FOR THESIS-the-jig-is-back

### Criterion 1: Composition demonstrated, not asserted
- **Description:** Each thesis chapter names the course IDs it stands on and cites at least one
  artifact produced under them.
- **Weight:** Primary objective | **Type:** Style | **Dependent Criteria:** none

### Criterion 2: Both unexplained divergences carry their evidence bound
- **Description:** The `FLIGHT_MS` and flight-path findings each state the 2026-05-05 session date
  and the 2026-06-12 commit date.
- **Rationale:** Negative constraint N1. Without the bound, a bounded finding reads as a proven one.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 1

### Criterion 3: The false finding is disclosed rather than removed
- **Description:** The defense records that the `mask` search produced a finding which reading the
  code removed.
- **Rationale:** A defense that reports only surviving findings hides its own error rate, which is
  the single most useful number it produces.
- **Weight:** Primary objective | **Type:** Adversarial | **Dependent Criteria:** none

### Criterion 4: No assessment claimed as passed
- **Description:** States that zero submission/evaluation pairs exist for the four defined exams.
- **Rationale:** No silent caps. A curriculum that defines exams and reports none taken is honest;
  one that implies competence was demonstrated is the overclaim this layer exists to catch.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** none

### Criterion 5: The undocumented design decision is retained as a finding
- **Description:** States that the trail-reveal change has no requesting turn in the captured
  session.
- **Rationale:** The instinct is to explain it away. Its absence is the finding — it demonstrates
  precisely what a single-session corpus cannot recover.
- **Weight:** Primary objective | **Type:** Adversarial | **Dependent Criteria:** none
