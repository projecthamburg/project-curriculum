# INH-101: The Two Format Contracts

**Crs:** 1 | **Prerequisite:** none (bootstrap) | **Phase:** Core
**Reference impl / anchor:** `src/app.py` and `src/export.py` at the fixture's committed state.
**Prerequisite audit (2026-08-17):** the catalog was empty at generation time; this is the run's
single use of the bootstrap exception, logged in `COVERAGE_PROFILE.md`.

> **Core Principle:** A pipeline with a reader and a writer has two format contracts, not one.
> They are usually assumed to be the same contract. Reading each one on its own terms, before
> comparing them, is what makes the difference visible.

## Coverage Declaration
- **Provides:** the ability to state the format contract each side of a pipeline implements,
  read from the code rather than from its documentation.
- **Requires:** the ability to read a small Python module.
- **Generalizes to modes:** Qualitative, Procedural.
- **Capstone stage supplied:** the contracts chapter of `THESIS-inherited-service`.

## Learning Objectives
1. State the read contract implemented by `parse`.
2. State the write contract implemented by `format_field`.
3. Identify the input class on which the two contracts differ.

## Curriculum

### Module 1: The read contract
`src/app.py` splits a line on every comma with no escaping and no unquoting. Its own docstring
states the assumption: the v1 wire format is comma-separated with no escaping. On that
contract, a quote character is an ordinary character.

### Module 2: The write contract
`src/export.py` wraps a field in `"` when the field contains `DELIM`. Its docstring gives the
reason: so the row stays unambiguous. On that contract, a quote character is a delimiter of a
field, not content.

### Module 3: Where the contracts diverge
For any record whose fields contain no comma, both contracts agree and the pipeline round-trips.
The contracts differ only on the input class where a field contains a delimiter — which is
exactly the class the writer added quoting for.

## Assignments

**Assignment 1.1** `[INH-101-A1]` State each contract in one sentence, citing the function.

**Assignment 1.2** `[INH-101-A2]` Give the smallest input class on which they differ.

## Final Exam: State both contracts and their divergence

Read both modules and report the read contract, the write contract, and the input class on
which they disagree.

## GRADING RUBRIC FOR INH-101 FINAL EXAM
*(inherits `protocol/MASTER_RUBRIC.md` in full)*

### Criterion 1: Read contract stated
- **Description:** States that `parse` splits on every comma and performs no unquoting.
- **Sources:** `src/app.py`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 2: Write contract stated
- **Description:** States that `format_field` wraps a field in a double-quote character when the
  field contains a comma.
- **Sources:** `src/export.py`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 3: Divergence class identified
- **Description:** States that the two contracts differ only on records where a field contains a
  comma.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 2

### Criterion 4: Agreement class identified
- **Description:** States that records whose fields contain no comma round-trip unchanged.
- **Rationale:** A response reporting only the failure implies the pipeline is broken for all
  input. It is correct for most input, which is why the defect survived.
- **Weight:** Not primary objective | **Type:** Reasoning | **Dependent Criteria:** 3

### Criterion 5: No intent attributed to either contract
- **Description:** Does not state which contract was intended, planned, or original.
- **Rationale:** Negative constraint N1. No intent record exists for this project, and both
  docstrings are evidence of what was believed at writing time rather than of what was asked for.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** none
