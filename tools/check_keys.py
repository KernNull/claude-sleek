#!/usr/bin/env python3
"""Check that every theme defines the same set of keys.

Run from the repo root:  python tools/check_keys.py
Exits with status 1 if a theme is missing a key the others have (or has an extra one),
so a color added to one theme cannot be forgotten in another.

High Contrast themes are the only ones that may (and must) define the contrast border keys.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HC_TYPES = ("hc", "hcLight")
HC_ONLY = {"contrastBorder", "contrastActiveBorder"}
VALID_TYPES = {"dark", "light", "hc", "hcLight"}


def main():
    themes = {}
    for path in sorted((ROOT / "themes").glob("*.json")):
        themes[path.name] = json.loads(path.read_text(encoding="utf-8"))

    problems = []
    names = [t["name"] for t in themes.values()]
    for n in sorted({n for n in names if names.count(n) > 1}):
        problems.append(f"duplicate theme name: {n}")

    # the union of UI keys across the normal themes is the reference set
    normal = [t for t in themes.values() if t["type"] not in HC_TYPES]
    reference = set().union(*(set(t["colors"]) for t in normal)) - HC_ONLY
    sem_reference = set().union(*(set(t["semanticTokenColors"]) for t in themes.values()))
    scopes_reference = set().union(*(
        {tuple(tok["scope"]) for tok in t["tokenColors"]} for t in themes.values()))

    for fname, t in themes.items():
        hc = t["type"] in HC_TYPES
        label = t["name"]
        if t["type"] not in VALID_TYPES:
            problems.append(f"{label}: invalid type {t['type']!r}")
        expected = reference | (HC_ONLY if hc else set())
        have = set(t["colors"])
        for k in sorted(expected - have):
            problems.append(f"{label}: missing UI key {k}")
        for k in sorted(have - expected):
            problems.append(f"{label}: unexpected UI key {k}")
        for k in sorted(sem_reference - set(t["semanticTokenColors"])):
            problems.append(f"{label}: missing semantic token {k}")
        have_scopes = {tuple(tok["scope"]) for tok in t["tokenColors"]}
        for s in sorted(scopes_reference - have_scopes):
            problems.append(f"{label}: missing token rule {list(s)[:2]}")

    for p in problems:
        print("FAIL", p)
    print(f"\nAll {len(themes)} themes define the same keys." if not problems
          else f"\n{len(problems)} problem(s) found.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
