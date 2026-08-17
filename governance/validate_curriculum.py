#!/usr/bin/env python3
"""governance/validate_curriculum.py — enforce the protocol contracts mechanically.

Until this existed, the Part D meta-rubric was applied by hand, which means it was applied
inconsistently. These are the checks that can be made deterministic. **They are not the whole
of Part D** — Criterion 1 (real-world anchoring) and Criterion 6 (citation discipline) require
judgment about whether a cited artifact actually supports the claim, and this validator only
checks that the citation *resolves*. Those two remain a reviewer's job, and the report says so
rather than implying full coverage.

Gates, each traceable to a protocol document:

  G1  prerequisite DAG          acyclic; files exist; header agrees with JSON, both directions
  G2  traceability completeness every artifact mapped, or it is not part of the program
  G3  coverage declarations     all four fields, never a placeholder
  G4  criterion structure       6 fields present on every criterion
  G5  unstacked                 no "and"/"or" joining two testable concepts
  G6  self-containment          an expected value is embedded, not deferred to
  G7  no subjective adjectives  the four do-nots
  G8  citation resolution       cited internal paths and line ranges exist
  G9  pathway declaration       a Pathway B curriculum declares absent intent

Exit code is non-zero if any gate fails, so CI can depend on it.

Usage:
    python3 governance/validate_curriculum.py
    python3 governance/validate_curriculum.py --project projects/01-the-jig-is-back
    python3 governance/validate_curriculum.py --project <p> --json
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys

SUBJECTIVE = ["adequate", "thorough", "creative", "strong", "sufficient", "relevant",
              "appropriate", "reasonable", "good", "proper", "clear", "robust"]

# Only conjunctions joining two *testable* concepts stack a criterion. A conjunction inside a
# quoted string, a file list, or an enumeration of one concept's parts does not.
STACK_RE = re.compile(r"\b(?:and|or)\b", re.I)
DEFERRED = re.compile(r"\b(the (correct|expected|right) (answer|value|fix|result))\b", re.I)
VALUE_RE = re.compile(r"\b\d|`[^`]+`|\bM \d|\bnone\b|\bzero\b|\babsent\b|\bpresent\b", re.I)
CITE_PATH_RE = re.compile(r"`([\w./-]+\.(?:md|py|tsx?|jsx?|json|yaml|yml))(?::L?(\d+))?`")


class Report:
    def __init__(self):
        self.gates: dict = {}

    def add(self, gate, ok, detail, findings=None):
        self.gates[gate] = {"pass": ok, "detail": detail, "findings": findings or []}

    @property
    def failed(self):
        return [g for g, r in self.gates.items() if not r["pass"]]


def read(path):
    return open(path, encoding="utf-8", errors="ignore").read()


def find_syllabus(project_root):
    d = os.path.join(project_root, "syllabus")
    return d if os.path.isdir(d) else None


def parse_criteria(text):
    """Return [(title, body)] for every '### Criterion N: …' block."""
    blocks = re.split(r"^### Criterion\s+", text, flags=re.M)[1:]
    out = []
    for b in blocks:
        title = b.splitlines()[0].strip()
        body = b.split("\n### ")[0]
        out.append((title, body))
    return out


def g1_dag(syl, rep):
    pj = os.path.join(syl, "curriculum_prerequisites.json")
    if not os.path.exists(pj):
        return rep.add("G1", False, "curriculum_prerequisites.json missing")
    graph = json.load(open(pj))["courses"]
    findings, ids = [], {}
    for c in graph:
        p = os.path.join(syl, c["file"])
        if not os.path.exists(p):
            findings.append(f"{c['file']}: listed in JSON, absent on disk")
            continue
        ids[c["file"].split("-")[0] if not c["file"].startswith("THESIS")
            else "THESIS"] = c["file"]
    known = set(ids)
    for c in graph:
        for pre in c["prerequisites"]:
            if pre.split("-")[0] not in {k.split("-")[0] for k in known} and pre not in known:
                if not any(f.startswith(pre) for f in (x["file"] for x in graph)):
                    findings.append(f"{c['file']}: prerequisite {pre} resolves to no course")
        p = os.path.join(syl, c["file"])
        if os.path.exists(p):
            m = re.search(r"\*\*Prerequisite[s]?:\*\*\s*(.+)", read(p))
            hdr = m.group(1) if m else ""
            for pre in c["prerequisites"]:
                if pre not in hdr and "ALL" not in hdr:
                    findings.append(f"{c['file']}: JSON lists {pre}, header does not")
            if not c["prerequisites"] and "bootstrap" not in hdr.lower() and \
                    not c["file"].startswith("THESIS"):
                findings.append(f"{c['file']}: no prerequisites and no bootstrap declaration")
    # cycle detection
    adj = {c["file"]: c["prerequisites"] for c in graph}
    name_of = {f.split("-")[0]: f for f in adj if not f.startswith("THESIS")}
    state = {}

    def visit(f):
        if state.get(f) == 1:
            findings.append(f"cycle through {f}")
            return
        if state.get(f) == 2:
            return
        state[f] = 1
        for pre in adj.get(f, []):
            nxt = name_of.get(pre)
            if nxt:
                visit(nxt)
        state[f] = 2

    for f in adj:
        visit(f)
    rep.add("G1", not findings, f"{len(graph)} nodes", findings)


def g2_traceability(syl, rep):
    tj = os.path.join(syl, "curriculum_traceability.json")
    if not os.path.exists(tj):
        return rep.add("G2", False, "curriculum_traceability.json missing")
    arts = json.load(open(tj))["artifacts"]
    findings = [f"{a['path']}: no disposition" for a in arts if not a.get("disposition")]
    rep.add("G2", not findings, f"{len(arts)} artifacts mapped", findings)


def g3_coverage(syl, rep, course_files):
    required = ["**Provides:**", "**Requires:**", "**Generalizes to modes:**",
                "**Capstone stage supplied:**"]
    findings = []
    for f in course_files:
        t = read(os.path.join(syl, f))
        for field in required:
            if field not in t:
                findings.append(f"{f}: missing {field}")
            else:
                val = t.split(field, 1)[1].split("\n", 1)[0].strip()
                if not val or val.startswith("<"):
                    findings.append(f"{f}: {field} is a placeholder")
    rep.add("G3", not findings, f"{len(course_files)} courses", findings)


def g4_g7_criteria(syl, rep, all_files):
    g4, g5, g6, g7 = [], [], [], []
    total = 0
    for f in all_files:
        t = read(os.path.join(syl, f))
        for title, body in parse_criteria(t):
            total += 1
            ref = f"{f} · Criterion {title}"
            desc_m = re.search(r"\*\*Description:\*\*\s*(.+?)(?=\n- \*\*|\Z)", body, re.S)
            if not desc_m:
                g4.append(f"{ref}: no Description")
                continue
            desc = " ".join(desc_m.group(1).split())
            for field in ("**Weight:**", "**Type:**", "**Dependent Criteria:**"):
                if field not in body:
                    g4.append(f"{ref}: missing {field}")
            # G5 — stacking. Two testable concepts joined by a conjunction. A conjunction
            # inside a quoted string or joining a list of one concept's parts is not stacking,
            # so require a verb-like clause on both sides before flagging.
            for m in STACK_RE.finditer(desc):
                left, right = desc[:m.start()], desc[m.end():]
                if re.search(r"\b(states|identifies|cites|reports|explains|does not)\b", left,
                             re.I) and re.search(
                        r"\b(states|identifies|cites|reports|explains|does not)\b", right, re.I):
                    g5.append(f"{ref}: '{m.group(0)}' joins two testable concepts")
                    break
            # G6 — self-containment
            if DEFERRED.search(desc):
                g6.append(f"{ref}: defers to an unstated expected value")
            elif not VALUE_RE.search(desc) and len(desc.split()) > 25:
                g6.append(f"{ref}: long description with no embedded value or named artifact")
            # G7 — subjective adjectives
            for adj in SUBJECTIVE:
                if re.search(rf"\b{adj}\b", desc, re.I):
                    g7.append(f"{ref}: subjective adjective '{adj}'")
    rep.add("G4", not g4, f"{total} criteria", g4)
    rep.add("G5", not g5, f"{total} criteria", g5)
    rep.add("G6", not g6, f"{total} criteria", g6)
    rep.add("G7", not g7, f"{total} criteria", g7)


def g8_citations(project_root, syl, rep, all_files):
    """Resolve cited internal paths. An unresolvable citation is a phantom source
    (MASTER_RUBRIC do-not 4). Upstream paths are checked only when the clone is present —
    absence is reported as unchecked, never as a pass."""
    ext_root = None
    cfg = os.path.join(project_root, "governance", "config.json")
    if os.path.exists(cfg):
        ext_root = json.load(open(cfg)).get("external_root")
    findings, checked, unchecked = [], 0, 0
    for f in all_files:
        for m in CITE_PATH_RE.finditer(read(os.path.join(syl, f))):
            rel, line = m.group(1), m.group(2)
            # A citation is written the way a reader would look it up, not as a path
            # relative to one fixed base. Resolve against every base a reader would try:
            # the syllabus, the project, its governance folder, the workspace root, and the
            # upstream clone — plus a basename match under the upstream tree, since upstream
            # files are cited by filename (`HeroDemo.tsx`), not by their path inside it.
            workspace = os.path.dirname(os.path.dirname(os.path.abspath(project_root)))
            bases = [syl, project_root,
                     os.path.join(project_root, "governance"),
                     os.path.dirname(project_root), workspace, ext_root]
            hit = None
            for base in bases:
                if base and os.path.exists(os.path.join(base, rel)):
                    hit = os.path.join(base, rel)
                    break
            if hit is None and ext_root and os.path.isdir(ext_root) and "/" not in rel:
                for dirpath, dirnames, filenames in os.walk(ext_root):
                    dirnames[:] = [d for d in dirnames if not d.startswith(".")]
                    if rel in filenames:
                        hit = os.path.join(dirpath, rel)
                        break
            if hit is None:
                if not (ext_root and os.path.isdir(ext_root)) and (
                        rel.startswith("code/") or "/" not in rel):
                    unchecked += 1
                    continue
                findings.append(f"{f}: cited path does not resolve: {rel}")
                continue
            checked += 1
            if line and int(line) > len(read(hit).splitlines()):
                findings.append(f"{f}: {rel} cited at L{line}, file has fewer lines")
    detail = f"{checked} citations resolved"
    if unchecked:
        detail += f"; {unchecked} upstream citations NOT checked (clone absent)"
    rep.add("G8", not findings, detail, findings)


def g9_pathway(project_root, syl, rep):
    """Pathway A means an intent RECORD exists — not merely that chapter files exist.

    A Tier 3 corpus produces real ICE chapters carrying Ideas and Concerns while carrying no
    Expectations at all, because a monologue has an Ask and no Response. Classifying by the
    presence of a chapter file would read such a project as Pathway A and skip the declaration
    check entirely, which is the exact hole this gate exists to close. So the test is whether
    any chapter establishes an Expectation, evidenced by a lock-in marker."""
    ice = os.path.join(project_root, "governance", "ice-outputs")
    chapters = ([os.path.join(ice, f) for f in os.listdir(ice) if f.endswith("_ICE.md")]
                if os.path.isdir(ice) else [])
    LOCKIN = ("🔒", "🔓", "➡️")
    with_expectations = [c for c in chapters
                         if any(m in read(c) for m in LOCKIN)]
    corpus = " ".join(read(os.path.join(syl, f)) for f in os.listdir(syl)
                      if f.endswith(".md"))
    declares = bool(re.search(r"no intent record exists", corpus, re.I))

    if with_expectations:
        return rep.add("G9", True,
                       f"Pathway A — {len(with_expectations)} chapter(s) establish Expectations")
    detail = (f"Pathway B — {len(chapters)} chapter(s), none establishing an Expectation"
              if chapters else "Pathway B — no ICE chapters")
    rep.add("G9", declares, detail,
            [] if declares else ["Pathway B curriculum does not declare that no intent record "
                                 "exists (protocol/EVIDENCE_AND_PATHWAYS.md). Chapters carrying "
                                 "only Ideas and Concerns do not make this Pathway A."])


def validate(project_root, as_json):
    syl = find_syllabus(project_root)
    if not syl:
        print(f"No syllabus/ under {project_root} — nothing to validate.")
        return 0
    files = sorted(f for f in os.listdir(syl) if f.endswith(".md")
                   and f != "COVERAGE_PROFILE.md")
    courses = [f for f in files if not f.startswith("THESIS")]

    rep = Report()
    g1_dag(syl, rep)
    g2_traceability(syl, rep)
    g3_coverage(syl, rep, courses)
    g4_g7_criteria(syl, rep, files)
    g8_citations(project_root, syl, rep, files)
    g9_pathway(project_root, syl, rep)

    if as_json:
        print(json.dumps(rep.gates, indent=2))
    else:
        names = {"G1": "prerequisite DAG", "G2": "traceability", "G3": "coverage declarations",
                 "G4": "criterion structure", "G5": "unstacked", "G6": "self-containment",
                 "G7": "no subjective adjectives", "G8": "citation resolution",
                 "G9": "pathway declaration"}
        print(f"Validating {project_root}\n")
        for g in sorted(rep.gates):
            r = rep.gates[g]
            print(f"  [{'PASS' if r['pass'] else 'FAIL'}]  {g}  {names[g]:28s} {r['detail']}")
            for f in r["findings"][:10]:
                print(f"          - {f}")
            if len(r["findings"]) > 10:
                print(f"          … {len(r['findings']) - 10} more")
        print()
        print("NOT covered mechanically, and still a reviewer's job: Part D Criterion 1 "
              "(does the cited artifact actually anchor the course) and Criterion 6 "
              "(does a resolved citation actually support the claim).")
    return 1 if rep.failed else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=None,
                    help="project root; defaults to every projects/* found")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.project:
        return validate(os.path.abspath(args.project), args.json)

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    roots = [os.path.join(here, "projects", d)
             for d in sorted(os.listdir(os.path.join(here, "projects")))
             if os.path.isdir(os.path.join(here, "projects", d))] \
        if os.path.isdir(os.path.join(here, "projects")) else []
    if not roots:
        print("No projects to validate.")
        return 0
    rc = 0
    for r in roots:
        rc |= validate(r, args.json)
    return rc


if __name__ == "__main__":
    sys.exit(main())
