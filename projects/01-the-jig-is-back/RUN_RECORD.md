# Run record — seed:2026-08-17:intent-fidelity

The first end-to-end seeding run. Recorded so the claim "the machinery works" cashes out
against something checkable rather than resting on the fact that files exist.

**Upstream:** `github:specstoryai/the-jig-is-back` @ `70041403`, resolved from `seed.yaml`.
**Nothing upstream is committed here.** No licence is stated upstream, so redistribution is
`reference-only`; the working clone is re-fetchable from the pointer.

## What ran, in order

| # | Step | Command | Result |
|---|---|---|---|
| 1 | Intake | `new_project.py --parent … --objective …` | `projects/01-the-jig-is-back/` created; external kind; own governance layer |
| 2 | Capture | `import_chat_logs.py transcript.md --real` | 1 file, format `specstory` auto-detected, 65 non-empty turns, date `2026-05-05` at `exact` confidence |
| 3 | Index | `build_search_index.py` | 15 sources (9 internal, 6 external), 103 chunks |
| 4 | Review | `ice_chapter.py new --label paper-plane-path-editor` → authored | `ch01`, watermark advanced to `ch02` |
| 5 | Translate | Part A → coverage profile | 4 target capabilities, all gaps against an empty catalog |
| 6 | Generate | Part B/C | `JIG-101`–`JIG-104` + `THESIS-the-jig-is-back` |
| 7 | Validate | DAG, headers, coverage declarations, adjective lint | pass |
| 8 | Scan | `security_scan.py` | 26 tracked files, 0 secret-shaped, 0 injection-shaped |

## Checks that could have failed and did not

| Check | Result |
|---|---|
| All 5 human turns survive import and are retrievable by `--speaker user` | 5 of 5 |
| Secret sweep of captured evidence | 0 patterns fired |
| Prerequisite DAG acyclic, filenames match, headers agree with JSON | pass |
| Every course's Coverage Declaration has all 4 fields | 4 of 4 |
| Subjective adjectives in criterion descriptions | 0 |
| Criteria written | 28 across 4 courses + 5 thesis criteria |
| Bootstrap exception uses | 1 (`JIG-101`), logged in `COVERAGE_PROFILE.md` |

## Findings about the upstream project

Three of five recorded expectations are satisfied by the shipped code. Two commitments are not,
and the evidence cannot say why.

| Finding | Status |
|---|---|
| Four committed tangent-kink fixes | all present at the pinned commit |
| Defective piecewise easing (`t < 0.45 ? …`) | absent from both files — fix landed |
| `FLIGHT_MS` committed 4500 → 7000 | shipped **4100**, faster than the value the human asked to slow down from |
| Human's pasted path `M 746 83` | shipped path begins `M 716 77`; the committed *mechanism* is present, the *artifact* differs |
| Trail-reveal mask → arc-length dots | real and correctly motivated, with **no requesting turn anywhere in the captured session** |

**Evidence bound, stated before the findings are used:** the session is 2026-05-05; the pinned
commit is 2026-06-12. Five uncaptured weeks sit between them. The two divergences are recorded
as *unexplained*, not as broken commitments — a later deliberate revision is equally consistent
with the evidence.

## Two things this run got wrong, and what fixed them

**A false finding, caught by reading.** A search for `mask` in the shipped code appeared to
contradict upstream's statement that the mask-based trail reveal was removed. Reading the
surrounding code resolved it: those are `chromeMask`, an unrelated element. The grep produced a
finding; only reading removed it. This is the run's own negative constraint N3 catching a real
error inside the run.

**A real bug in the tooling, caught by running it.** With `external_root` set, every manifest
path resolved against upstream, so a project could not index its own authored syllabus and ICE
chapters — the index reported 7 sources where it should have reported 15. The original design
this was generalized from needed two roots and this port had collapsed them to one. Fixed by a
per-entry `root: content | external` field; re-run gives 15 sources across 8 categories.

Both are recorded rather than quietly corrected, because a run that reports only what worked
hides its own error rate.

## Honest gaps

1. **No assessment has been taken.** Four exams are defined; zero submission/evaluation pairs
   exist. No course in this run is passed, and this run could not have graded itself in any
   case — an exam-taker and its evaluator must never be the same pass.
2. **The seeding translation was performed by an agent, not by code.** Parts A–C of
   `GENERATION_MACHINERY.md` were executed as reasoning against the protocol documents. **The
   Part D meta-rubric was applied by hand, not by a validator** — the seven criteria were
   checked manually. The CI validators do not exist yet.
3. **Session discovery was not exercised.** This run captured evidence from a committed file.
   `discover_sessions.py`'s five providers require a real developer machine; this container has
   no Codex or Kimi store. That half remains unproven.
4. **One session is the entire conversational corpus**, and no CORE tier exists, so these four
   courses carry method knowledge that belongs in shared courses.

## Reproducing this run

```bash
git clone https://github.com/specstoryai/the-jig-is-back /tmp/jig
git -C /tmp/jig checkout 70041403230a109ab17ccfbef718665fb4901553
python3 governance/new_project.py --parent /tmp/jig --slug the-jig-is-back --objective "<seed.yaml objective>"
python3 projects/01-the-jig-is-back/governance/import_chat_logs.py /tmp/jig/transcript.md --real
python3 projects/01-the-jig-is-back/governance/update.py --real
```

Steps 4–6 are agent work, not a script. That is the honest state of the implementation today.
