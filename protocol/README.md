# protocol/ — the normative documents

These are the contracts a Project Curriculum implementation obeys. They are **agent-independent and
runtime-independent**: nothing here assumes Claude Code, Codex, Jules, Cursor, Antigravity, or any
particular model or language. An implementation in any of them is conformant if it honours these.

| Document | What it fixes |
|---|---|
| [`MASTER_RUBRIC.md`](MASTER_RUBRIC.md) | The criterion contract — 6 fields, 4 quality laws, 4 do-nots, dependency and citation discipline. Every criterion anywhere obeys this. |
| [`COURSE_TEMPLATE.md`](COURSE_TEMPLATE.md) | The clonable course skeleton, and the **Coverage Declaration** that makes courses composable rather than merely readable. |
| [`MASTER_SYLLABUS.md`](MASTER_SYLLABUS.md) | Catalog conventions — tiers, the two machine-validated graphs, change management, the staleness ledger. |
| [`GENERATION_MACHINERY.md`](GENERATION_MACHINERY.md) | How a seeding objective becomes a curriculum: translation, composition, gap detection, and the meta-rubric that gates generated output. |
| [`THESIS_AND_DEFENSE.md`](THESIS_AND_DEFENSE.md) | The capstone as a composition proof, and the adversarial audit that keeps it honest. |
| [`ICE.md`](ICE.md) | The informed-consent review that turns raw conversation history into reviewed, citable chapters. |
| [`EVIDENCE_AND_PATHWAYS.md`](EVIDENCE_AND_PATHWAYS.md) | The two pathways (with and without conversation history), the three evidence tiers, spheres, and why there are two indexes. |
| [`VALIDATION.md`](VALIDATION.md) | Three validation layers — mechanical gates, an external validator, an adversarial panel — and what each structurally cannot catch. |

## Reading order

Building an implementation: `MASTER_RUBRIC` → `COURSE_TEMPLATE` → `MASTER_SYLLABUS` →
`GENERATION_MACHINERY` → `THESIS_AND_DEFENSE`. `ICE` is independent of the other five and can be
read at any point; it produces the evidence the others consume.

Running a seeding objective for the first time: `EVIDENCE_AND_PATHWAYS` first — it decides which
pathway you are on, and a Pathway B project never reaches `ICE` at all. Then `ICE`, because a
Pathway A curriculum seeded from unreviewed transcripts is a curriculum seeded from noise.

## The layer that changes, and the layers that don't

```
1. KNOWLEDGE CONTRACT      what this curriculum must know, and what counts as evidence
          ↓                                                    ← fixed by protocol/
2. AGENT PROCEDURE         CLAUDE.md · AGENTS.md · .agents/rules · a skill · a graph
          ↓                                                    ← the ONLY layer that varies
3. KNOWLEDGE COMPILER      ingest · reconcile · compose · assess · lint
          ↓                                                    ← fixed by protocol/
4. DURABLE KNOWLEDGE       courses · rubrics · assessments · thesis · defense · provenance
```

Only layer 2 changes between agent platforms. That is the point of keeping the specification
canonical rather than any one implementation.

## Provenance

These documents were derived from an internal predecessor system at Project Hamburg Research and
generalized for public use. **The private corpora that system was itself synthesized from — a
third-party training corpus, a borrowed worked example, and real project material — are not
included here and are not required to implement any of this.** Where a rule exists because
something went wrong once, the failure is described but the private artifact is not cited.

## Status

**v0.1-draft.** These are being derived from a working implementation rather than written ahead of
one. Until an end-to-end seeding run has actually executed against real material, treat every
document here as subject to correction *by that run* — which is the same standard this project
applies to every other claim it makes.
