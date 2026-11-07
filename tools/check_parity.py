#!/usr/bin/env python3
"""Check that each No Italics theme differs from its parent only in italics.

Run from the repo root:  python tools/check_parity.py
Exits with status 1 if a variant has drifted, so it can run in CI.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"
SUFFIX = "-no-italics"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def strip(style):
    return (style or "").replace("italic", "").strip()


def compare(parent, variant):
    problems = []

    if parent["type"] != variant["type"]:
        problems.append(f"type differs: {parent['type']} vs {variant['type']}")
    if parent["colors"] != variant["colors"]:
        keys = sorted(set(parent["colors"]) | set(variant["colors"]))
        for k in keys:
            if parent["colors"].get(k) != variant["colors"].get(k):
                problems.append(f"UI color {k}: {parent['colors'].get(k)} vs {variant['colors'].get(k)}")

    # syntax tokens: same scopes, names and colors; italics removed from font styles
    pt, vt = parent["tokenColors"], variant["tokenColors"]
    if len(pt) != len(vt):
        problems.append(f"token rule count differs: {len(pt)} vs {len(vt)}")
    for i, (a, b) in enumerate(zip(pt, vt)):
        label = a.get("name") or a["scope"][0]
        if a["scope"] != b["scope"] or a.get("name") != b.get("name"):
            problems.append(f"token rule {i} ({label}): scope or name differs")
            continue
        sa, sb = dict(a["settings"]), dict(b["settings"])
        if "fontStyle" in sa:
            sa["fontStyle"] = strip(sa["fontStyle"])
        if sa != sb:
            problems.append(f"token rule {i} ({label}): {a['settings']} vs {b['settings']}")
        if "italic" in sb.get("fontStyle", ""):
            problems.append(f"token rule {i} ({label}): still italic in the variant")

    # semantic tokens: same keys and colors; italic switched off
    ps, vs = parent["semanticTokenColors"], variant["semanticTokenColors"]
    if set(ps) != set(vs):
        problems.append(f"semantic token keys differ: {sorted(set(ps) ^ set(vs))}")
    for k in ps.keys() & vs.keys():
        a, b = ps[k], vs[k]
        if isinstance(a, dict):
            a = {**a, **({"italic": False} if a.get("italic") else {})}
        if a != b:
            problems.append(f"semantic token {k}: {ps[k]} vs {vs[k]}")
        if isinstance(b, dict) and b.get("italic"):
            problems.append(f"semantic token {k}: still italic in the variant")

    return problems


def main():
    failures = 0
    variants = sorted(THEMES.glob(f"*{SUFFIX}.json"))
    parents = {p.stem for p in THEMES.glob("*.json") if not p.stem.endswith(SUFFIX)}

    for v in variants:
        parent_stem = v.stem[: -len(SUFFIX)]
        parent = THEMES / f"{parent_stem}.json"
        if not parent.exists():
            print(f"FAIL {v.name}: no parent theme {parent.name}")
            failures += 1
            continue
        problems = compare(load(parent), load(v))
        print(f"{'FAIL' if problems else 'ok':4} {load(v)['name']}")
        for p in problems:
            print("       -", p)
        failures += len(problems)
        parents.discard(parent_stem)

    for stem in sorted(parents):
        print(f"FAIL {stem}.json: no No Italics variant")
        failures += 1

    print("\nAll variants match their parents." if not failures else f"\n{failures} problem(s) found.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
