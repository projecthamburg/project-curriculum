# PROVENANCE — project-curriculum

Maps every file in `sources/` to what it actually is, and where the true original lives.

**Raw is immutable; renderings are derived.** A native `.jsonl`, an exported `.json`, or an
as-supplied `.md` is evidence and is never edited. Anything this layer produced from it is a
derived artifact and is regenerable from the original.

The index reads `sources/*.md` only, so a raw `.json` sitting alongside is a real, present
source without being pulled into the index. Each capture's `.meta.json` sidecar records its
category, provider, association confidence, and timestamp confidence.

## Current captures

| File in `sources/` | Indexed? | Kind | True original |
|---|---|---|---|
| _(none yet)_ | | | |

Nothing has been captured into this repository's own governance layer yet. When it is, every
entry states plainly whether it is a native original or a derived rendering, and where the
untouched original lives.

## A note on this repository's own history

This repository's design conversation exists and is real evidence, but it has not been
captured here: it contains a third party's messages, which fall under `CONCERNS.md` item 2.
Recorded as a known, deliberate omission rather than left as an unexplained gap.
