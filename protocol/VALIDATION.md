# VALIDATION — who checks the curriculum, and what they can actually check

**Status:** v0.1-draft · Project Curriculum Protocol
**Implements:** [`GENERATION_MACHINERY.md`](GENERATION_MACHINERY.md) Part D ·
[`THESIS_AND_DEFENSE.md`](THESIS_AND_DEFENSE.md)

Three layers, in increasing cost and decreasing determinism. **Each catches a class the one
before it structurally cannot**, which is why none of them replaces another.

| Layer | Catches | Deterministic? | Cost |
|---|---|---|---|
| 1. Mechanical gates | Malformed artifacts | Yes | Free, every commit |
| 2. External validator | Wrong artifacts | No | An outside party |
| 3. Adversarial panel | Plausible-but-false artifacts | No | Several agents |

---

## Layer 1 — mechanical gates

`governance/validate_curriculum.py`. Nine gates, non-zero exit on failure, no secrets and no
network, so it runs on a fork's pull request exactly as it runs upstream.

| Gate | Checks | From |
|---|---|---|
| G1 | Prerequisite DAG: acyclic, files exist, header and JSON agree **both ways** | `MASTER_SYLLABUS.md` |
| G2 | Traceability: every artifact mapped, or it is not part of the program | `MASTER_SYLLABUS.md` |
| G3 | Coverage Declarations: four fields, never a placeholder | Part D C7 |
| G4 | Criterion structure: six fields present | Part D C5 |
| G5 | Unstacked: no conjunction joining two testable concepts | Part D C3 |
| G6 | Self-containment: an expected value embedded, not deferred to | Part D C4 |
| G7 | No subjective adjectives | `MASTER_RUBRIC.md` do-not 1 |
| G8 | Citation resolution: cited paths and line ranges exist | do-not 4 |
| G9 | Pathway declaration: a Pathway B curriculum declares absent intent | `EVIDENCE_AND_PATHWAYS.md` |

### What Layer 1 cannot do, stated in its own output

Part D's Criterion 1 (real-world anchoring) and Criterion 6 (citation discipline) are **not
fully mechanizable.** G8 checks that a cited path resolves. It cannot check that the file
actually supports the claim. A criterion citing a real file that says the opposite passes every
gate.

The validator prints this limit on every run rather than reporting a clean sweep and letting a
reader infer coverage it does not have.

---

## Layer 2 — the external validator

**Preferred when available.** An external validator is a party that did not generate the
curriculum and does not share the generator's context: a different organization, a domain
expert, a maintainer of the upstream project being profiled, or a separately-operated service.

Its value is exactly its independence. It is the only layer that can catch an error the
generator and its checkers share — a misread source document, a wrong assumption held
consistently throughout.

**Interface.** A validator receives the curriculum, the seed, and the evidence pointers, and
returns findings in the same shape Layer 3 produces (below). It needs no access to the
generating agent and no knowledge of this protocol beyond the seed's objective.

**When absent, say so.** A curriculum validated only by Layers 1 and 3 records that no external
validation occurred. "No external validator was available" is a finding about the curriculum's
standing, not a blank to leave empty.

---

## Layer 3 — the adversarial panel

When no external validator exists, a panel of independently-scoped agents substitutes for one.
It is a **weaker** substitute — agents drawn from the same family share priors, and a shared
prior is exactly what an external validator exists to break. Recorded as such, never as
equivalent.

### The shape that makes it work

**Each member gets a distinct lens, not the same prompt repeated.** Redundancy catches noise;
diversity catches failure modes. For a curriculum, the lenses that have earned their place:

| Lens | Asks |
|---|---|
| **Evidence** | Does every cited artifact actually say what the criterion claims? |
| **Overclaim** | Is any claim tiered higher than its evidence supports? |
| **Fabrication** | Is any quote, line number, DOI or file path invented? |
| **Coverage** | What does the objective require that no course covers? |
| **Bound** | Is any bounded result presented as complete? |

**Each member is prompted to refute, not to confirm**, and defaults to *refuted* under
uncertainty. A panel asked "is this good?" produces agreement; a panel asked "show me this is
wrong" produces findings.

**A finding survives on majority refutation**, and the vote is recorded with it. A finding that
two of five members raised is a different object from one that five of five raised, and
flattening them loses the signal.

### Composition rule

The panel is not a swarm of clones. If every member is the same model with the same prompt at
the same temperature, the panel has one opinion expressed five times, and its agreement means
nothing. Vary the lens first, and the model where possible.

---

## What each layer is allowed to do

**Nothing in any layer edits the curriculum.** All three produce findings with proposed
dispositions. Application is a separate, human-approved step — the same rule as the security
scan, for the same reason: a checker that silently rewrites what it checks destroys the record
it exists to protect.

```
generate ─> L1 gates ─> L2 external (if any) ─> L3 panel ─> findings
                                                              │
                                                     proposed dispositions
                                                              │
                                                     human approval ─> applied
```

---

## Where each layer runs

| Layer | Where | Why |
|---|---|---|
| L1 | GitHub Actions, every pull request | No secrets, no network — runs on fork PRs unchanged |
| L2 | Wherever the validator is | Out of this repository's control by definition |
| L3 | Manually, or a gated workflow | Needs model API keys, so fork runs use the fork's own secrets and upstream runs are maintainer-gated |

That split is not incidental. **Putting model calls in the same workflow as the gates would
mean the gates could not run on a fork's pull request at all**, and the cheapest, most
deterministic layer is the one that most needs to run everywhere.
