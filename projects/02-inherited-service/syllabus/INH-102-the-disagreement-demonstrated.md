# INH-102: The Disagreement, Demonstrated by Execution

**Crs:** 2 | **Prerequisite:** INH-101 | **Phase:** Domain
**Reference impl / anchor:** the round trip `format_record(["hello,world", "active"])` fed back
through `parse`, executed against the fixture at its committed state.
**Prerequisite audit (2026-08-17):** INH-101 supplies the two contracts this course runs against.

> **Core Principle:** Reading two functions and concluding they disagree is an argument.
> Running the round trip and reporting what came back is evidence. Where a claim can be settled
> by execution, it is settled by execution.

## Coverage Declaration
- **Provides:** the ability to demonstrate a component disagreement by executing it and
  reporting real values, rather than by reasoning about source.
- **Requires:** both format contracts (INH-101).
- **Generalizes to modes:** Quantitative, Adversarial.
- **Capstone stage supplied:** the demonstration chapter of `THESIS-inherited-service`.

## Learning Objectives
1. Construct the smallest input that exercises the divergence.
2. Execute the round trip and report the actual output.
3. Report the field-count change as a number.

## Curriculum

### Module 1: The smallest exercising input
One field containing a delimiter is enough: `["hello,world", "active"]`. Two fields in, one of
which contains the divergence class from INH-101.

### Module 2: The round trip, run
`format_record` produces `"hello,world",active`. Feeding that to `parse` returns
`['"hello', 'world"', 'active']`. Two fields were written; three were read. The quote characters
survive as content, because the reader has no concept of them.

### Module 3: Why the suite does not see it
`tests/test_app.py` asserts `parse("a,b,active") == ["a", "b", "active"]` and a filter case.
Neither input contains a delimiter inside a field, so the suite passes while the defect stands.
A green suite is evidence about what was tested, not about what works.

## Assignments

**Assignment 2.1** `[INH-102-A1]` Execute the round trip and paste the actual returned list.

**Assignment 2.2** `[INH-102-A2]` State why the existing tests pass.

## Final Exam: Demonstrate the disagreement

Execute the round trip on an input whose field contains a delimiter and report what was written,
what was read back, and the change in field count.

## GRADING RUBRIC FOR INH-102 FINAL EXAM
*(inherits `protocol/MASTER_RUBRIC.md` in full)*

### Criterion 1: Written form reported
- **Description:** Reports that `format_record(["hello,world", "active"])` produces the string
  `"hello,world",active`.
- **Sources:** `src/export.py`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 2: Read-back form reported
- **Description:** Reports that parsing that string returns the three-element list
  `['"hello', 'world"', 'active']`.
- **Sources:** `src/app.py`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** 1

### Criterion 3: Field-count change stated as a number
- **Description:** States that two fields were written and three were read.
- **Weight:** Primary objective | **Type:** Quantitative | **Dependent Criteria:** 2

### Criterion 4: Quote characters identified as surviving content
- **Description:** States that the double-quote characters remain inside the returned field
  values.
- **Rationale:** The field count alone understates the corruption; the values are altered too,
  which is what breaks a consumer that counts on the field's content.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 2

### Criterion 5: Execution used rather than inspection
- **Description:** Reports output obtained by running the round trip.
- **Rationale:** Negative constraint. A response deriving the output by reading the source has
  produced a prediction, and this course exists because a prediction is not a demonstration.
- **Weight:** Primary objective | **Type:** Procedural | **Dependent Criteria:** 3

### Criterion 6: Test blindness explained
- **Description:** States that no input in `tests/test_app.py` contains a delimiter inside a
  field.
- **Sources:** `tests/test_app.py`.
- **Weight:** Not primary objective | **Type:** Extraction | **Dependent Criteria:** none
