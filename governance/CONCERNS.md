# CONCERNS — project-curriculum

This repository's own concerns log. Not optional, and not something added later once
something goes wrong: it exists from the start, even while nearly empty.

**What belongs here:** a reviewer's own assessment of risk, conduct, or exposure —
including assessments of how an agent behaved.

**What does not:** the human's own stated worries. Those are ICE Concerns and belong in an
`ice-outputs/` chapter, quoted with line numbers. See [`protocol/ICE.md`](../protocol/ICE.md).
Getting this routing wrong in the other direction is the documented drift failure — a
chapter that has slid into grading the model has stopped being evidence.

## Open

### 1. No licence — blocks contributions and third-party evidence

With no `LICENSE`, an accepted pull request has no terms, and relicensing later may require
every contributor's agreement. One unreachable contributor can freeze the choice
permanently. Separately, no licence decision means no settled position on redistributing
third-party conversation evidence.

**Disposition:** accept no outside contributions until this is resolved. See `README.md`
and `docs/UNDERSTANDING.md` §7.

### 2. Session-evidence redistribution rights are unsettled

A repository's code licence says nothing about the right to republish a conversation *about*
that code — separate work, separate owner. Until a policy is written, the working rule is
**reference, never copy** for anything a third party authored: store the upstream URL,
pinned commit, and content hash, and read it at execution time.

Riding alongside and mattering more than copyright: personal data inside transcripts, which
is a privacy question independent of licensing.

**Disposition:** monitor. Blocks publishing any seed pack containing third-party material.

### 3. Global-adjacent session discovery is not implemented

`discover_sessions.py` finds sessions whose recorded cwd is the project. It does not find a
session that worked on the project's files from a different working directory. The two-stage
method is documented in `PROJECTS.md`; the code is not written.

**Disposition:** monitor. Stated so nobody assumes capture is complete.

## Closed

_None yet._
