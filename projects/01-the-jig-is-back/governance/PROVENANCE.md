# PROVENANCE — the-jig-is-back

Maps every file in `sources/` to what it actually is, and where the true original lives.

**Raw is immutable; renderings are derived.** A native `.jsonl`, an exported `.json`, or an
as-supplied `.md` is evidence and is never edited. Anything this layer produced from it is
a derived artifact and is regenerable.

The index reads `sources/*.md` only, so a raw `.json` sitting alongside is a real, present
source without being pulled into the index. Each capture's `.meta.json` sidecar records its
category, provider, association confidence, and timestamp confidence.

| File in `sources/` | Indexed? | Kind | True original |
|---|---|---|---|
| _(none captured yet)_ | | | |
