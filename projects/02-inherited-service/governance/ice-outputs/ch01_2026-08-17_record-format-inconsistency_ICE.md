# ch01 — record-format-inconsistency

**Domain:** inherited-service
**Chapter:** ch01
**Authored:** 2026-08-17
**Reviewer:** Claude Code, acting as the reviewing agent for this seeding run

## Scope

This chapter covers the single Tier 3 note at `notes/thoughts.txt`, which is the entire
human-side record available for this project.

**Sources reviewed (1):**
- `sources/2026-08-17_unknown_thoughts.md` — Tier 3, one voice, no recognized turn structure,
  date `file-derived` (the note carries none of its own)

## This chapter has no NEGOTIATED Expectations

**Tier 3 material cannot establish a negotiated Expectation.** That needs an Ask *and* a
Response *and* a lock-in judgment. This source has only the first: it is a monologue, with no
counterparty and no reply. Writing an Ask → Response → Lock-in chain from it would invent a
party to a conversation that never happened.

It has **encoded** Expectations, recorded below. See `protocol/ICE.md` §"What an Expectation is".

> **Correction, 2026-08-17.** As first authored, this chapter stated it had *no Expectations at
> all* and that the emptiness was structural. That was wrong, and the error was in the protocol
> before it was in this chapter: Expectations were defined as arising only from dialogue.
>
> They also arise from the artifact. This project has at least three, and two of them contradict
> each other — which is the central finding of the whole run and was recorded here as a Concern
> instead. The original Concerns are left in place below rather than moved, because they are
> genuinely also the human's own stated worries; the encoded Expectations are added as their own
> section with conformance judgments. Nothing has been deleted.

## Security status

Checked, nothing found. The note was swept at capture time by `import_chat_logs.py`; zero
redaction patterns fired. The parent's own files were scanned by `security_scan.py`; no
secret-shaped findings.

## Expectations — negotiated

**None, and none can exist from this evidence.** See the section above.

## Expectations — encoded

Judged by conformance against the artifact, not by lock-in. Each states where the Expectation
is stated, what it claims, what the artifact does, and how that was established.

### E1 ⚡ contradicted — the wire format has two incompatible definitions
- **Stated at** `src/app.py:6-8`: the v1 wire format is comma-separated **with no escaping**.
- **Stated at** `src/export.py:8`: a field containing the delimiter is quoted **so the row stays
  unambiguous**.
- **Artifact does:** both, in the same pipeline. Each contract is internally coherent; together
  they are incompatible on exactly the input class quoting was added for.
- **Established by:** execution. `format_record(["hello,world","active"])` writes two fields;
  `parse` reads that back as three.
- **Marked ⚡ contradicted, not ❌ violated, deliberately.** Neither side is individually wrong.
  Recording this as a violation of one of them would silently pick a winner, and choosing which
  contract the format *has* is the owner's decision, not a finding.

### E2 ❌ violated — the documented round trip does not hold
- **Stated at** `README.md:8-9`: the format round-trips cleanly, so an exported file can be fed
  straight back in.
- **Artifact does:** round-trips every record whose fields contain no comma, and corrupts any
  record whose field contains one.
- **Established by:** execution, as above. The claim is unqualified, so one counterexample
  falsifies it as written.

### E3 ⚠️ untested — the quoting behaviour has no test
- **Stated at** `src/export.py:8`: quoting exists so a row stays unambiguous. That is a claim
  about a behaviour, and a behaviour claim is testable.
- **Artifact does:** nothing exercises it. `tests/test_app.py` asserts on `"a,b,active"` and a
  filter case; no input in the suite contains a delimiter inside a field.
- **Established by:** reading `tests/test_app.py` in full.
- **Consequence:** the suite passes while E1 and E2 both hold. A green suite is evidence about
  what was tested, not about what works.

## Concerns

### C1 — The reader and the writer disagree about quoting
- **Stated** (L5–L9): "The reader splits on every comma. The writer wraps a field in quotes
  when the field contains a comma. Those two do not agree with each other. If a field ever
  contains a comma, we write it quoted and then read it back as two fields, one of which
  starts with a quote character."

Independently confirmed against the code rather than taken on the note's word:
`src/export.py:9` quotes a field containing `DELIM`; `src/app.py:9` splits unconditionally on
`,` with no unquoting. Executing the round trip on `["hello,world", "active"]` returns
`['"hello', 'world"', 'active']` — three fields where two were written.

### C2 — Nobody knows whether the mismatch was intended
- **Stated** (L11–L12): "Nobody remembers whether the quoting was added later or whether the
  reader was supposed to be updated at the same time. There is no ticket and no discussion I
  can find."

This is the Pathway B condition stated by the project's own author. It is recorded as a
Concern — the human's own worry — and **not** treated as evidence of what was intended, which
it explicitly is not.

### C3 — Changing it may break unknown dependents
- **Stated** (L15): "Worried about what depends on the current behaviour though."

## Ideas

### I1 — Replace the hand-rolled format with a real CSV reader
- **Stated** (L14): "Should probably move to a real CSV reader."

An Idea, not an Expectation: nothing responded to it, nothing committed to it, and nothing in
the code reflects it. Recorded so a later agent inherits the proposal without inheriting a
false impression that it was agreed.

## Open, unresolved

1. **Whether the quoting in `export.py` or the splitting in `app.py` is the correct
   behaviour** cannot be determined from any available evidence. Both are internally coherent;
   they are only incoherent together. Choosing between them is a decision the project's owner
   must make, and this pipeline cannot make it for them.
2. **The README claims the format "round-trips cleanly."** That claim is false for any field
   containing a delimiter, demonstrated above. Whether the README was written before the
   quoting was added, or was simply wrong, is not recoverable.
3. **No test covers a field containing a delimiter.** `tests/test_app.py` exercises only
   unquoted input, so the defect is invisible to the suite. Whether that gap was deliberate is
   not recoverable either.
