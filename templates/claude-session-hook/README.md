# Opt-in: a Claude Code SessionStart hook

**You almost certainly do not need this.** `CLAUDE.md` at the repository root is auto-loaded
by Claude Code with no script execution and no trust prompt, and it covers every case where
the context is static text — which is nearly all of them.

This template exists for the one case where it isn't: when a session should open with
**computed** state rather than a fixed pointer — a live project count, the current ICE
backlog, whether the index is stale.

## Why it is not the default here

A `SessionStart` hook asks every person who clones this repository to execute a shell script
they have not read. For a private repository that is a non-issue — it is your own script on
your own machine. For a public one that strangers clone, asking for script execution in
order to deliver text a file could deliver is the wrong default.

So: `CLAUDE.md` ships enabled, and this ships as something you turn on deliberately.

## Installing it

Copy both files into your own clone:

```bash
cp templates/claude-session-hook/settings.json .claude/settings.json
cp templates/claude-session-hook/hooks/session-start.sh .claude/hooks/
chmod +x .claude/hooks/session-start.sh
```

`.claude/settings.json` is **not** committed by this repository, deliberately — enabling a
hook is a decision each clone makes for itself, not one inherited from upstream.

## What the script must and must not do

**Must:** be fast, be read-only, and print to stdout. Its output is injected straight into
the session's context.

**Must not:** run the reindex. That already happens on commit and push; doing it again on
every session start makes every new session slow for no benefit.
