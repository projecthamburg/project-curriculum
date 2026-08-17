#!/usr/bin/env python3
"""governance/pc_config.py — the one place a governance layer states what it governs.

Every script in this folder reads its roots from here instead of hardcoding them, so a
copy of this folder placed under projects/<NN-slug>/governance/ works **unmodified** —
only its own config.json differs. That is a deliberate improvement over hand-editing a
PROJECT_ROOT constant in five scripts per project: the copies stay byte-identical, so a
fix to one is a fix to all, while each instance remains fully self-contained with no
shared runtime dependency and no network.

config.json (beside this file):

    {
      "project_id":   "project-curriculum",
      "ice_domain":   "project-curriculum",
      "content_root": "..",
      "external_root": null,
      "manifest":     "sources/project-files-manifest.yaml"
    }

  project_id    stable identifier for this instance; used in report filenames.
  ice_domain    the ICE domain name. Its chapter-number sequence is per-domain — see
                protocol/ICE.md for why a shared sequence collides.
  content_root  path to the content this layer governs, relative to the governance
                folder. ".." for a nested project or a repo's own layer.
  external_root absolute path to a separate repository this layer governs, or null.
                When set, manifest entries resolve against it rather than content_root.
                The external repository is never written to.
  manifest      the file manifest, relative to the governance folder.
"""
from __future__ import annotations
import json
import os

GOV = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(GOV, "config.json")

DEFAULTS = {
    "project_id": "unnamed",
    "ice_domain": "unnamed",
    "content_root": "..",
    "external_root": None,
    "manifest": "sources/project-files-manifest.yaml",
}


def load() -> dict:
    cfg = dict(DEFAULTS)
    if os.path.exists(CONFIG_PATH):
        try:
            cfg.update(json.load(open(CONFIG_PATH, encoding="utf-8")))
        except (json.JSONDecodeError, OSError) as exc:
            raise SystemExit(f"governance/config.json is unreadable: {exc}")
    return cfg


def paths() -> dict:
    """Resolved absolute paths every script needs. content_root is where this layer's own
    files live; manifest_root is what manifest `path:` entries resolve against — the same
    directory unless external_root is set."""
    cfg = load()
    content_root = os.path.abspath(os.path.join(GOV, cfg["content_root"]))
    external_root = os.path.abspath(cfg["external_root"]) if cfg["external_root"] else None
    return {
        "config": cfg,
        "gov": GOV,
        "content_root": content_root,
        "external_root": external_root,
        "manifest_root": external_root or content_root,
        "sources": os.path.join(GOV, "sources"),
        "manifest": os.path.join(GOV, cfg["manifest"]),
        "index": os.path.join(GOV, "search_index.json"),
        "ledger": os.path.join(GOV, "sources", "_ingested.json"),
        "ice_outputs": os.path.join(GOV, "ice-outputs"),
        "reports": os.path.join(GOV, "reports"),
    }


if __name__ == "__main__":
    p = paths()
    print(json.dumps({k: v for k, v in p.items() if k != "config"}, indent=2))
    print(json.dumps(p["config"], indent=2))
