# projects/

One folder per project this workspace maintains a curriculum for.

Nothing here yet. Create one with:

```bash
python3 governance/new_project.py --parent ../my-app \
    --objective "what this curriculum must serve" --dry-run
```

The intake checklist, the registry rules, and the per-project pattern are in
[`governance/PROJECTS.md`](../governance/PROJECTS.md). Two things worth knowing before you
start:

- **An objective is required.** Everything else can default, but a curriculum cannot be
  seeded without a stated objective — there is nothing to seed it *for*.
- **A project's content can live anywhere.** Governance lives here; the parent project's own
  repository is read and never written to.
