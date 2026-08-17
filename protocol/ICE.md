# ICE — Ideas, Concerns, Expectations

**Status:** v0.1-draft · Project Curriculum Protocol

> **Revision 2026-08-17 — Expectations were defined too narrowly.** The first draft treated an
> Expectation as arising only from dialogue: something the human asked for, or something the
> agent committed to. That omitted the third and often largest source — **Expectations encoded in
> the artifact itself**. The correction is in §"What an Expectation is" below. The earlier
> framing is not deleted; it turns out to describe one of three provenances accurately, and is
> retained as the *negotiated* case.
**Produces:** the reviewed evidence that `GENERATION_MACHINERY.md` seeds a curriculum from.
**Independent of** the other protocol documents — this one can be read and implemented first.

---

## What ICE is

> **ICE is the record of what this project holds itself to, and whether it does.**

Two halves, and both are required:

- **Informed consent between the human and the LLM** — what the human asked and expected, what the
  model formally responded, and whether the human agreed to it. This half needs conversation
  evidence and is unavailable on Pathway B.
- **Conformance of the artifact to what it states about itself** — what the code, config, tests and
  documentation claim, and whether they hold. This half needs no conversation at all, and is the
  whole of ICE on Pathway B.

**Neither half is a general quality review of the model's output**, even though the two are extremely easy
to conflate. The predecessor system conflated them once before this model was written down as
binding, which is why the distinction is stated first rather than assumed.

The two things and where each goes:

| Finding | Belongs in |
|---|---|
| What the human asked, expected, proposed, worried about | **An ICE chapter** |
| What the artifact states about itself, and whether it holds | **An ICE chapter** — an encoded Expectation |
| A reviewer's assessment of how well the model behaved | **`CONCERNS.md`**, never the chapter |

That routing rule is load-bearing. A chapter that has drifted into grading the model has stopped
being an evidence record and become an opinion, and a curriculum seeded from opinions inherits them.

---

## Domain → chapter → `ICE.md`

- A **domain** is a class of source — usually one project.
- A **chapter** is one review run over a defined window or file set within a domain.
- **`ICE.md`** is that chapter's deliverable.

**Every domain keeps its own chapter-number sequence.** This is not symmetry for its own sake: two
projects reindexing concurrently against a shared sequence will collide on the same chapter number the
moment both run at once. The sequence is per-domain, and the watermark is stored with the domain.

**Every chapter carries a one-sentence scope declaration** stating exactly what window or file set it
covers. Without one, a later reader cannot tell whether something absent from the chapter was absent
from the sessions or merely out of scope.

**Every chapter states a security status explicitly** — including "checked, nothing found." Required
even when the chapter's own source material never mentions security, because the absence of a
statement is indistinguishable from the absence of a check.

---

## What an Expectation is

> **An Expectation is a statement of what must be true for the work to count as satisfied.**

It has **three provenances**, and a chapter that recognizes only the first two will miss most of
them on most projects.

| Provenance | Where it lives | Example |
|---|---|---|
| **Asked** | the human said it | "don't modify existing records unless the user chooses overwrite" |
| **Committed** | the agent said it would do it | "I'll bump the duration from 4500 to 7000ms" |
| **Encoded** | **the artifact asserts it** | a config documenting `"beam" = Faster`; a docstring saying `Dynamic programming based wave search`; a test asserting an output; a schema, a type constraint, a validation check, an error message, a default |

**Asked and Committed are negotiated.** They need two voices and they carry a lock-in judgment,
because someone either agreed or did not.

**Encoded is not negotiated.** The artifact states, alone, what it holds itself to. Nobody has to
have agreed to it, and usually nobody discussed it at all. It is still an Expectation, because it
is still a claim about what counts as working — and because the artifact can be checked against it.

### Why this matters more than it looks

A config file documenting three search strategies — `dp = Dynamic Programming (Optimal)`,
`csp`, `beam = Faster` — where all three dispatch to the same function is a **violated encoded
Expectation.** No conversation is needed to find it. The artifact promised three behaviours and
delivers one. A function whose docstring says it performs a search, whose body performs no
search, has broken a promise it made to itself.

This is the class of finding a Pathway B project produces in quantity, and the reason **Pathway B
is not a pathway without Expectations.** It is a pathway without *negotiated* ones.

---

## Judging an Expectation

Two provenances, two kinds of judgment. Using the wrong one is the common error.

### Negotiated — the Ask → Response → Lock-in chain

Each negotiated Expectation states three things:

1. **The ask** — what the human asked, quoted, with a line number.
2. **The response** — the model's formal reply, quoted, with a line number.
3. **A lock-in judgment:**

| Marker | Meaning |
|---|---|
| 🔒 **locked** | Explicit approval on the record — a "yes", a "great job", or the human's own addition building on it |
| 🔓 **unlocked** | Asked and answered, with no recorded approval |
| ➡️ **superseded** | A later, separately-dated item changed direction |

> **An earlier item is never edited or deleted to make room for a later one.**

When execution diverges from the original ask, that divergence becomes a **new, separately-dated
item** documenting where things went differently — not a retroactive edit of the original. The
original stays 🔒 locked if it was locked, because it *was* locked at the time, and the record of
what was agreed is distinct from the record of what happened.

This is what makes ICE evidence rather than narrative. A smoothed history reading as though the
right decision was made all along has destroyed the exact information a future agent needs.

### Encoded — the conformance judgment

An encoded Expectation has no lock-in, because nothing was agreed. It is judged against the
artifact itself:

| Marker | Meaning |
|---|---|
| ✅ **honoured** | the artifact does what it states |
| ❌ **violated** | the artifact contradicts its own statement |
| ⚠️ **untested** | stated, and nothing exercises it |
| ⚡ **contradicted** | two encoded Expectations disagree with each other |

**⚡ contradicted is its own marker and not a variant of violated.** When a reader and a writer
each hold a coherent format contract and the two contracts are incompatible, neither one is
individually wrong. Recording it as a violation of one of them silently picks a winner — which
is a decision the evidence does not support and the owner has not made.

Each encoded item states: **where the Expectation is stated** (file and line), **what it claims**,
**what the artifact actually does**, and **how that was established** — read, or executed. An
encoded Expectation demonstrated by execution outranks one argued from source, for the same
reason a real run outranks "the tests pass".


---

## Extracting Concerns and Ideas

**Concerns** — the human's own stated worries, in their own words. Not the reviewer's assessment of
risk, and not the model's self-criticism.

**Ideas** — concepts, changes, problems, and directions the human introduced.

For both: quote, with a line number. If a finding is genuinely the reviewer's own judgment rather than
the human's, it is real and worth keeping — it just goes to `CONCERNS.md` instead.

---

## Recognizing drift in an existing chapter

A chapter has drifted when its Concerns or Ideas are actually about the model's conduct rather than
the human's stated position.

**Correct it without deleting the underlying finding.** Move the finding to `CONCERNS.md`, note the
move and its date in the chapter, and leave the trail visible. A silently corrected chapter and a
never-wrong chapter are indistinguishable to a later reader, which defeats the purpose.

---

## Evidence handling

**Raw is immutable; renderings are derived.** The native original — a `.jsonl` session file, an
exported `.json`, an as-supplied `.md` — is evidence and is never edited. Human-readable renderings
are derived artifacts, regenerable, and clearly labelled as such.

**Timestamp confidence is explicit**, never inferred silently:

| Value | Meaning |
|---|---|
| `exact` | Recorded in the source |
| `inferred` | Derived from surrounding context |
| `file-derived` | Taken from filesystem metadata |
| `unknown` | Not determinable — say so |

An inferred chronology that becomes indistinguishable from a recorded one will eventually be reasoned
over as fact, and ICE's whole value is chronological.

**Association confidence is explicit too:**

| Level | Basis |
|---|---|
| **Explicit** | The human said this conversation belongs to this project |
| **Path** | The session's own recorded working directory is the project |
| **Candidate** | Content suggests a relationship — terminology, filenames, URLs |

**Uncertain evidence is never silently made canonical.** A candidate association is proposed for
confirmation, not adopted.

**Secret sweep before anything lands.** Any capture is swept for credentials *before* it is written
into a tracked folder — non-optional, and not hypothetical: a real credential pair was found in
exactly this position in the predecessor system, read from an unrelated file earlier in the same
session and captured verbatim. Verify a flagged match by its **length and structural shape, never by
printing the matched content.**

---

## The capture/review split

**Capture is mechanical and safe to automate. Review is a judgment call and is not.**

Discovering sessions, converting formats, filing them, and diffing against an ingestion ledger can all
run unattended on every commit. Authoring a chapter — deciding what was asked, what was agreed, what
was superseded — stays deliberate.

An implementation that automates the second half has produced generated prose about conversations, not
a record of informed consent.

---

## What ICE feeds

```
conversations + work sessions
          ↓
        ICE chapters               ← reviewed, quoted, dated, scoped
          ↓
Ideas · Concerns · Expectations
          ↓
   seeding objective + evidence     → GENERATION_MACHINERY.md Part A
          ↓
       curriculum
```

A curriculum seeded from unreviewed transcripts is a curriculum seeded from noise. ICE is the step
that makes the evidence citable.
