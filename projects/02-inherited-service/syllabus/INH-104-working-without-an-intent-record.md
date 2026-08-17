# INH-104: Working Without an Intent Record

**Crs:** 4 | **Prerequisite:** INH-101 | **Phase:** Domain
**Reference impl / anchor:** `governance/ice-outputs/ch01_2026-08-17_record-format-inconsistency_ICE.md`,
whose Expectations section is empty by rule; `governance/reports/intake_inherited-service.json`.
**Prerequisite audit (2026-08-17):** INH-101 supplies the contracts whose origin this course
establishes as unrecoverable.

> **Core Principle:** The honest answer to "why is it like this" is sometimes "no record
> survives". A curriculum that supplies a plausible reason instead has manufactured the thing it
> exists to preserve. Saying so is the competence this course tests.

## Coverage Declaration
- **Provides:** the ability to work correctly on a project with no intent record — separating
  what the artifact shows from what someone wanted, and declining to fill the gap.
- **Requires:** the two format contracts (INH-101).
- **Generalizes to modes:** Qualitative.
- **Capstone stage supplied:** the pathway chapter of `THESIS-inherited-service`.

## Learning Objectives
1. State what Pathway B makes unavailable, and why.
2. Explain why a Tier 3 note cannot carry an Expectation.
3. Route a decision that the evidence cannot settle to the person who can settle it.

## Curriculum

### Module 1: What is missing, precisely
No conversation history exists for this project — no agent sessions, no LLM logs, and the parent
carries no git history of its own. The intake probe recorded this before any file was written.
So there is no Ask, no Response, and no lock-in anywhere: intent-fidelity courses are not
generated here because there is nothing for them to be about.

### Module 2: Why the note is not a substitute
`notes/thoughts.txt` is one voice. It says the reader and the writer disagree, that nobody
remembers whether the mismatch was intended, and that a CSV reader would be better. Those are
Concerns and an Idea. **None of them is an Expectation**, because an Expectation needs a
counterparty who responded and a lock-in judgment about whether the human accepted it. Writing
one from a monologue invents the other party.

### Module 3: What the artifact can and cannot tell you
Docstrings and a README are evidence of what someone believed at writing time. Both docstrings
here are internally coherent and mutually incompatible, which tells you they were written
against different assumptions — and tells you nothing about which assumption was sanctioned.

### Module 4: Routing what cannot be settled
Whether to fix the reader or the writer is not a technical question here. Both sides are
coherent alone. Choosing between them changes what the format *is*, and the evidence contains
no basis for the choice. The correct output is a stated decision point addressed to the owner,
not a recommendation dressed as an inference.

## Assignments

**Assignment 4.1** `[INH-104-A1]` List the course types this project cannot generate, and why.

**Assignment 4.2** `[INH-104-A2]` State the decision the evidence cannot settle, and who must.

## Final Exam: Account for the absent record

State what this project's evidence cannot establish, why the Tier 3 note does not close the gap,
and what follows for the format decision.

## GRADING RUBRIC FOR INH-104 FINAL EXAM
*(inherits `protocol/MASTER_RUBRIC.md` in full)*

### Criterion 1: Pathway stated
- **Description:** States that this project is on Pathway B because no conversation history
  exists for it.
- **Sources:** `governance/reports/intake_inherited-service.json`.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 2: Tier of the note stated
- **Description:** States that `notes/thoughts.txt` is Tier 3 evidence.
- **Weight:** Primary objective | **Type:** Extraction | **Dependent Criteria:** none

### Criterion 3: Reason the note carries no Expectation
- **Description:** States that the note has no counterparty and therefore no Response to pair
  with its Ask.
- **Rationale:** The tier label alone is a rule invoked. This criterion tests whether the reason
  behind it is understood, which is what stops the rule being applied where it does not fit.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 2

### Criterion 4: Empty Expectations section identified as structural
- **Description:** States that the chapter's Expectations section is empty by rule.
- **Sources:** `governance/ice-outputs/ch01_2026-08-17_record-format-inconsistency_ICE.md`.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** 3

### Criterion 5: Docstrings not promoted to intent
- **Description:** Does not state that either docstring records what the format was required to
  do.
- **Rationale:** Negative constraint N1. Two coherent, incompatible docstrings are evidence of
  two assumptions, not of one sanctioned requirement.
- **Weight:** Primary objective | **Type:** Reasoning | **Dependent Criteria:** none

### Criterion 6: Format decision routed to the owner
- **Description:** States that choosing between fixing the reader and fixing the writer is the
  project owner's decision.
- **Rationale:** Negative constraint N4. Both sides are internally coherent, so a recommendation
  here would be a preference presented as a finding.
- **Weight:** Primary objective | **Type:** Adversarial | **Dependent Criteria:** none
