# ch01 — paper-plane-path-editor

**Domain:** the-jig-is-back
**Chapter:** ch01
**Authored:** 2026-08-17
**Reviewer:** Claude Code, acting as the reviewing agent for this seeding run

## Scope

This chapter covers the whole of the single captured SpecStory session of 2026-05-05
(16:46Z–17:11Z), which is the only conversation evidence the upstream repository publishes.

**Sources reviewed (1):**
- `sources/2026-05-05_specstory_transcript.md` — derived rendering of upstream
  `transcript.md` at commit `70041403`, 5 human turns / 69 agent turns, per-turn timestamps
  recorded in the export (`timestamp_confidence: exact`)

**Bound on this chapter, stated rather than implied:** the upstream repository was committed
**2026-06-12**, five weeks after this session ended. Work done in that gap is not captured
anywhere in the public evidence. Every divergence recorded below is therefore a divergence
between *what was committed to in this session* and *what shipped* — **not** proof that a
commitment was broken. The evidence cannot distinguish an abandoned commitment from a later,
deliberate, unrecorded revision, and this chapter does not pretend otherwise.

## Security status

Checked, nothing found. The imported transcript was swept at capture time by
`import_chat_logs.py`; zero redaction patterns fired. The upstream code was scanned as part
of this project's own `security_scan.py` run; no secret-shaped findings.

## Expectations

### E1 — A better way to author the flight path
- **Ask** (L12): "the plane path is so rough. whats a better way to help draw a path out for
  you?"
- **Response** (L19): three ranked options — draw it in a vector editor and hand over the
  SVG `d` string; annotate a screenshot; or add a live debug overlay.
- **Lock-in:** 🔓 unlocked. No approval was recorded, and the human did not take any of the
  three. E2 asks for something adjacent but different.

*This is the turn that explains the whole repository.* The agent's own framing of option 1 —
"You're not translating intent through me — you're handing me the finished curve" — names the
failure the project exists to solve: intent transfer through prose was not converging.

### E2 — Build the editor
- **Ask** (L44): "can you code a tool that allows me to edit and view the path live in the
  localhost hero and then copy something fro you to see?"
- **Response** (L51): "Yes — let me build that. A live editor on the page itself,
  drag-and-drop waypoints, copy the path string out."
- **Lock-in:** 🔒 locked — by delivery and subsequent use. The human proceeds to exercise the
  tool in E3 and E4 rather than re-litigating the ask.
- **Satisfied by:** `code/PathEditor.tsx` (930 lines), reached via `?editPath=1`, with the
  copy-out textarea and an import field for round-tripping.

### E3 — The plane jumps between points
- **Ask** (L771): "there are some odd bugs where its jumping acorss points instead of
  smoothly traveling through them"
- **Response** (L777): diagnosed as tangent kinks at anchors — "positionally continuous but
  direction-discontinuous" — with **four** committed fixes: auto-mirror controls with Alt to
  break symmetry; drag anchors together with both flanking controls; a smooth-all pass; and
  centered-difference tangent estimation in the production flight loop.
- **Lock-in:** 🔓 unlocked at the time — E4 reports the symptom persisting.
- **Satisfied by:** all four are present in the shipped code (`altKey` in `PathEditor.tsx`;
  flanking-control drag; a smooth-all pass; centered-difference tangent in `HeroDemo.tsx`).

### E4 — Still snapping, and the path does not finish
- **Ask** (L1172): "still snapping ahead even after smoothing. aslo it doesnt go to the end
  of the path"

  Two distinct defects in one turn. Recorded as one Expectation because the human raised them
  as one, and resolved by a single root cause below.
- **Response** (L1178): "You found a real bug — and it's not in the path or the smoothing.
  It's in my easing function." The easing was
  `const e = t < 0.45 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 3) / 6 - 0.165;` — discontinuous
  at t=0.45, which produces both the forward snap and the unfinished path.
- **Lock-in:** 🔒 locked. E5 opens with "ok lets use this for now."
- **Satisfied by:** the piecewise easing is **absent** from both `HeroDemo.tsx` and
  `PathEditor.tsx` at the pinned commit. Verified by direct search, not inferred. ✅

### E5 — Accept, adopt the hand-drawn path, and slow it down
- **Ask** (L1293): "ok lets use this for now", followed by a pasted 15-segment path beginning
  `M 746 83 C 829 74, 1176 64, 884 -214 …`, followed by "lets slow the plane down though"

  Three acts in one turn: an acceptance, an artifact, and a new request.
- **Response** (L1299): "Wiring it in. Two changes: **1.** Replace `buildPath()` with your
  hardcoded path, but translate it at runtime so its M point (746, 83) aligns with the live
  button position … **2.** Bump `FLIGHT_MS` from 4500 → 7000ms for a slower, more graceful
  glide."
- **Lock-in:** 🔒 locked — "ok lets use this for now" is the session's only explicit
  acceptance.
- **Satisfied by:** ➡️ **neither commitment holds at the pinned commit.** See C1 and C2.

## Concerns

*(The human stated no concerns in their own words. The two below are the reviewer's, and are
recorded here because they are findings about the evidence rather than assessments of the
agent's conduct — anything of the latter kind belongs in `CONCERNS.md`.)*

### C1 — The committed flight duration is not what shipped, and moves the wrong way
- **Committed** (L1299): `FLIGHT_MS` 4500 → **7000**, in answer to "lets slow the plane down".
- **Shipped** (`code/HeroDemo.tsx:42`): `const FLIGHT_MS = 4100;`
- 4100 is not merely short of the committed 7000 — it is **faster than the 4500 the human was
  asking to slow down from.** The line above it reads "Pacing — slow and deliberate."
- Within the captured evidence, this is unexplained. Per the scope bound above, the five-week
  gap is the likely explanation and the evidence does not confirm it.

### C2 — The human's hand-drawn path is not the shipped path
- **Committed** (L1299): replace `buildPath()` with the pasted path, preserving its
  `M 746 83` origin and translating at runtime.
- **Shipped** (`code/HeroDemo.tsx:47–50`): `FLIGHT_PATH` begins `M 716 77 …`, with
  `FLIGHT_PATH_ORIGIN_X = 716` / `..._Y = 77`. The string `746` does not appear anywhere in
  `code/`.
- The *mechanism* the agent committed to — a hardcoded path translated at runtime from its own
  origin constants — is exactly what shipped. The *artifact* is a different curve. The most
  probable reading is that the editor was used again later and a new path drawn, which would
  make this the tool working as intended rather than a broken commitment. **The captured
  evidence does not establish this**, and it is recorded as unresolved rather than assumed.

## Ideas

### I1 — Build the instrument, not the artifact
- **Stated** (L44): rather than accept better-guessed Beziers, the human asked for a tool to
  draw the curve directly and hand the result back.

The idea is a general one and it is the repository's whole thesis: when intent will not
transfer through description, build the instrument that removes description from the loop.

### I2 — Same physics in the preview as in production
- **Stated implicitly** (L44): "edit and view the path live in the localhost hero".

Upstream's README states the editor's live preview uses the same RAF logic and physics
constants as production — "what you see in the editor is what you'll get live." A preview that
approximates production would have reintroduced the guessing the tool exists to remove.

## Open, unresolved

1. **C1 and C2 cannot be closed from public evidence.** Only the upstream authors know whether
   the flight duration and the flight path were deliberately revised after 2026-05-05. This is
   the kind of question the architecture exists to raise, and it is exactly where an
   evidence-bounded answer must stop.
2. **The trail-reveal supersession is real but was never explicitly asked for.** Upstream's
   README records that a mask-based reveal was abandoned for arc-length-sampled dots because
   masks cannot handle a self-intersecting path. Verified in code
   (`HeroDemo.tsx:202`; the remaining `mask` usages are `chromeMask`, an unrelated element).
   No human turn in the captured session requests this. It originates in the gap, or in
   agent-side judgment that was never surfaced as a commitment — either way, **a real design
   decision with no recorded intent behind it.**
