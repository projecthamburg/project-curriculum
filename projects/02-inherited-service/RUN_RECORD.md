# Run record — seed:2026-08-17:pathway-b-inheritance

The first **Pathway B** seeding run: a curriculum built with no conversation history at all.

**Parent:** `examples/inherited-service/` — a **synthetic fixture authored for this
repository**, committed here so the run is reproducible. Stated up front because a reader who
assumed it was a found project would overrate what this demonstrates.

## What ran

| # | Step | Result |
|---|---|---|
| 1 | `intake.py` | **Pathway B** determined by probe, before any file was written |
| 2 | `new_project.py` | `projects/02-inherited-service/`, own governance layer |
| 3 | `import_chat_logs.py` | 1 file → **Tier 3**, `can_establish_expectation: false` |
| 4 | `build_search_index.py` | 2 sources, 3 chunks (evidence — deliberately thin) |
| 5 | `index_codebase.py` | 5 files, 75 lines, 14 chunks (**the load-bearing index here**) |
| 6 | `ice_chapter.py` + authoring | ch01: 3 Concerns, 1 Idea, **0 Expectations** |
| 7 | Part A → courses | `INH-101`–`104` + thesis |
| 8 | `validate_curriculum.py` | **9 of 9 gates pass**, 28 criteria, 29 citations resolved |

## What the run established about the parent

The read path and the write path implement **incompatible format contracts**. `parse` splits on
every comma and never unquotes; `format_field` wraps a field in `"` when it contains a comma.
Each is coherent alone.

Demonstrated by execution, not argued from source:

```
format_record(["hello,world", "active"])  ->  "hello,world",active
parse('"hello,world",active')             ->  ['"hello', 'world"', 'active']
```

**Two fields written, three read**, with the quote characters surviving as content. The
README's claim that the format "round-trips cleanly" is therefore false as written — and true
for every record without a delimiter in a field, which is why it survived. No test covers the
failing class.

## What the run refused to establish

**Which contract was sanctioned.** Both are internally coherent; nothing in the artifact ranks
them. The fix is deliberately not recommended — choosing between them changes what the format
*is*, and that is the owner's decision, not an inference.

Three explanations the evidence does not distinguish between: that the quoting was added later,
that the reader was meant to be updated alongside it, or that the README simply predates both.
All plausible. None evidenced.

## The discipline this run tested

The Tier 3 note **asserts the same disagreement the thesis proves.** It would have been trivial
to cite the note and be right.

The run did not. The finding rests on executing the round trip; the note is recorded separately
as a Concern the human stated. That ordering is the point — Tier 3 material is admissible as a
Concern and inadmissible as proof, and a run that accepted it would have been **right by luck**.

The chapter's Expectations section is empty **by rule**: a monologue has an Ask and no Response,
so writing a lock-in chain from it would invent the counterparty.

## A gate bug this run exposed before it ran

G9 classified pathway by the *presence* of an ICE chapter file. This project has a real ICE
chapter — carrying Concerns and an Idea — and **no Expectations**. Under the old gate it would
have read as Pathway A and skipped the absent-intent declaration check entirely: precisely the
hole G9 exists to close, in the gate itself.

Fixed before the run: G9 now tests whether any chapter establishes an Expectation, evidenced by
a lock-in marker. Seed 01 still passes as Pathway A; this one correctly reports
*"Pathway B — 1 chapter(s), none establishing an Expectation"*.

Found by constructing the case the design implied, rather than by re-reading the gate.

## Honest gaps

1. **No assessment has been taken.** Four exams defined, zero taken.
2. **The parent is synthetic.** This demonstrates the pathway mechanically. It does **not**
   demonstrate that Pathway B survives a large real codebase — 75 lines is not a test of scale.
3. **The parent has no git history of its own**, so even change-order evidence is unavailable.
   This is the barest Pathway B case.
4. **No CORE tier exists**, so these four courses carry method knowledge belonging in shared
   courses.
5. **The bootstrap exception was used once** (`INH-101`).

## Reproducing

```bash
python3 governance/intake.py --parent examples/inherited-service \
    --exports examples/inherited-service/notes --objective "<see COVERAGE_PROFILE.md>"
python3 governance/new_project.py --parent examples/inherited-service --slug inherited-service \
    --objective "<same>"
python3 projects/02-inherited-service/governance/import_chat_logs.py \
    examples/inherited-service/notes --real
python3 projects/02-inherited-service/governance/index_codebase.py
python3 governance/validate_curriculum.py
```

Steps 6–7 are agent work, not a script — the honest state of the implementation today.
