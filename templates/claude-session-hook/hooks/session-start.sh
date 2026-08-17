#!/bin/sh
# Opt-in SessionStart hook. Runs at the start of every Claude Code session (new, resume,
# clear, compact, or fork; identical across CLI, IDE and Desktop). Its stdout is injected
# directly into the new session's context.
#
# Deliberately lightweight: it prints computed state only. It does NOT run the reindex —
# that already happens via git hooks on commit and push, and repeating it here would make
# every new session slow and spam the reports folder.

ROOT="${CLAUDE_PROJECT_DIR:-.}"

PENDING=$(python3 "$ROOT/governance/ice_chapter.py" status 2>/dev/null \
          | awk -F': *' '/Awaiting review/ {print $2}')
PROJECTS=$(python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))['projects']))" \
           "$ROOT/governance/registry.json" 2>/dev/null)

echo "[session-start] project-curriculum"
echo "  Projects registered: ${PROJECTS:-unknown}"
echo "  Sources awaiting ICE review: ${PENDING:-unknown}"
echo "  Search before reading files by hand: python3 governance/query.py \"your question\""
echo "  Full context: AGENTS.md · CLAUDE.md · governance/README.md · protocol/"
