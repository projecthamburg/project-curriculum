# Project Curriculum

**An open protocol, reference implementation, and public research corpus for determining what an
agent must learn — and demonstrate — to work competently on a project.**

Created by **Mordecai Machazire**, Lead Research, **Project Hamburg Research** (501(c)(3)
nonprofit, [projecthamburg.org](https://www.projecthamburg.org)). First public work: August 2026.

---

## The idea

A codebase tells you what exists. It doesn't tell you what someone was trying to build, how that
intent changed, what an agent understood it to mean, what was tried and abandoned, or whether what
was built still satisfies what was asked for. That knowledge lives in conversations — across
ChatGPT, Claude, Gemini, Codex, Cursor, and every other tool a project passed through — and it is
routinely lost.

Handing the next agent a transcript doesn't solve it either. A transcript is not understanding.

Project Curriculum takes a different position:

> **Don't give the next agent the project's context. Give it the project's curriculum.**

A project has things that must be learned. Organize them as **courses**. Define what competence
means with a **rubric**. Test comprehension with **quizzes**, demonstration with **assignments**,
and whole capabilities with **exams**. Prove the capabilities compose with a **thesis**, and then
**defend** that thesis against the implementation rather than trusting it because a model wrote it.

### Who is the student?

**The agent is the student. The project is the subject. The implementation is the laboratory.**

The syllabus defines competence. The rubric defines evidence of competence. The thesis demonstrates
composition. The defense verifies the claimed understanding is still true.

### The chain

```
Source → Intent → Interpretation → Commitment → Capability → Evidence → Evaluation → Thesis → Defense
```

---

## Where this sits

| System | Fundamental object | Primary question |
|---|---|---|
| Karpathy's LLM Wiki | Knowledge page | What have we learned? |
| OpenWiki / DeepWiki | Repository wiki | How does this code work? |
| projectmem / Memorix | Event, shared memory | What happened before? |
| GoalOS / Work Graph | Intent, task node | What are we trying to do? |
| **Project Curriculum** | **Capability / Course** | **What must an agent understand and demonstrate to work competently here — and can we prove it has?** |

These are not competitors. Project Curriculum can consume all of them as evidence sources. A repo
wiki answers "what does the code do"; project memory answers "what happened"; an intent graph
answers "what was wanted". This project asks what competence over all of that looks like, and how
you would verify someone — or something — has it.

Two commitments that follow from this and are easy to miss:

- **The project is the parent, not the git repository.** Projects routinely exist before their
  repos do, as conversations. Evidence is any human↔AI exchange that materially shaped the work,
  plus work sessions, plus git. Chronology is first-class, and timestamp confidence is explicit —
  inferred order must never quietly become fact.
- **The repository profiles itself.** A session that works *on* Project Curriculum is evidence
  *for* Project Curriculum's own curriculum. That recursion is intentional.

---

## Status — early, and honest about it

This repository is at the beginning. What exists today is the derived understanding of the
architecture and the decisions behind it, in [`docs/UNDERSTANDING.md`](docs/UNDERSTANDING.md).

Being built, in order:

1. The reusable machinery — rubric contract, course template with Coverage Declarations,
   generation machinery, thesis and defense.
2. Evidence capture across agent CLIs, IDEs, desktop apps, and exported conversations from
   providers with no local store.
3. ICE — the informed-consent review that turns raw sessions into reviewed chapters.
4. One real end-to-end seeding run against a real project.
5. `SPEC.md`, derived from what that run actually did — not written ahead of it.

The specification is deliberately being derived from a working implementation rather than invented
around one. That is also the rule this project applies to itself: **claims cash out against
observable reality.** Each stage ends with a real run against real material, not "the tests pass."

---

## Licence — none yet, deliberately

**There is currently no `LICENSE` file, and that is intentional.** Public visibility on GitHub is
not a licence. Until one is added, no rights to copy, modify, or redistribute this work are
granted, and no outside contributions are being accepted.

The licensing structure is under review because this repository will eventually hold four legally
distinct classes of material — the software, the specification, generated research profiles, and
third-party evidence that must retain its own provenance. Getting that boundary right at v0.1 is
much easier than unwinding it later.

Nothing about this is a move away from openness. The intent is a genuinely open protocol that
Claude, Codex, Jules, Hermes, LangGraph, OpenWiki or anything else can implement.

## Provenance and scope

This work was derived from an experimental system used internally at Project Hamburg Research.
**Private project histories, real session archives, and organizational data are not part of this
repository and will not be.**

Third-party material — upstream repositories and conversations authored by others — retains its own
licence and provenance. It is referenced, not absorbed.
