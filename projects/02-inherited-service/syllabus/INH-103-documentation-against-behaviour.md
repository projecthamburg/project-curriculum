# INH-103: Documentation and Tests Against Observed Behaviour

**Crs:** 3 | **Prerequisite:** INH-101 | **Phase:** Domain
**Reference impl / anchor:** `README.md`'s round-trip claim, checked against the execution in
INH-102.
**Prerequisite audit (2026-08-17):** INH-101 supplies the contracts the documentation is checked
against.

> **Core Principle:** Documentation is evidence of what someone believed when they wrote it. It
> is never evidence that the belief was correct, and on a project with no intent record it is
> the thing most likely to be mistaken for a requirement.

## Coverage Declaration
- **Provides:** the ability to test a documentation claim against observed behaviour and report
  the result without inferring what the documentation was trying to require.
- **Requires:** the two format contracts (INH-101).
- **Generalizes to modes:** Adversarial.
- **Capstone stage supplied:** the documentation chapter of `THESIS-inherited-service`.

## Learning Objectives
1. Extract a checkable claim from prose documentation.
2. Determine whether the claim holds, by execution.
3. State what the falsified claim does and does not tell you.

## Curriculum

### Module 1: The claim
`README.md` states that the format round-trips cleanly, and that an exported file can be fed
straight back in. That is a behavioural claim, and behavioural claims are checkable.

### Module 2: The check
INH-102 established that a record with a delimiter inside a field does not round-trip. The
README's claim is therefore false for that input class and true for every other. "Round-trips
cleanly" is unqualified, so a single counterexample falsifies it as written.

### Module 3: What the falsification does not tell you
It does not tell you the README is out of date. It does not tell you the quoting was added
after the README. It does not tell you anyone intended the format to handle delimiters. All
three are plausible; none is evidenced. The finding is that the claim is false, and that its
origin is unrecoverable.

## Assignments

**Assignment 3.1** `[INH-103-A1]` Quote the README's claim and state the input class that
falsifies it.

**Assignment 3.2** `[INH-103-A2]` List three explanations the evidence does not distinguish
between.

## Final Exam: Check the round-trip claim

Determine whether the README's round-trip claim holds, and state precisely what the result does
and does not establish.

## GRADING RUBRIC FOR INH-103 FINAL EXAM
*(inherits `protocol/MASTER_RUBRIC.md` in full)*

### Criterion 1: Claim located and quoted
- **Description:** Quotes the README's statement that the format round-trips cleanly.
- **Sources:** `README.md`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 2: Claim reported as false
- **Description:** States that the claim does not hold for a record whose field contains a
  comma.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 1

### Criterion 3: Scope of the falsification bounded
- **Description:** States that the claim holds for records whose fields contain no comma.
- **Rationale:** An unqualified report of falsity overstates the defect. The claim is wrong as
  written and right for most real input, and both halves are needed.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 2

### Criterion 4: Documentation not treated as a requirement
- **Description:** Does not state that the README establishes what the format was required to do.
- **Rationale:** Negative constraint N2. On a project with no intent record, a README is the
  artifact most likely to be silently promoted into a specification.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** none

### Criterion 5: Competing explanations left undistinguished
- **Description:** States that the evidence does not establish whether the README predates the
  quoting.
- **Rationale:** The tempting move is to supply the most plausible history. No history is
  recoverable here, and supplying one manufactures the record this pathway exists without.
- **Weight:** Primary objective | **Type:** Adversarial | **Dependent Criteria:** 2
