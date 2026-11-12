#!/usr/bin/env python3
"""Check that everything that mentions the version or the theme list agrees.

Run from the repo root:  python tools/check_release.py
Optional:                python tools/check_release.py --tag v2.0.0
Exits with status 1 on any mismatch, so a release cannot ship with a stale README or demo file.

Checks: package.json version is semver; the newest CHANGELOG entry, the README VSIX filename and
demo/showcase.json carry the same version; every contributed theme file exists and is named in the
README; (with --tag) the git tag matches the version.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def main():
    problems = []
    pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    version = pkg["version"]
    if not SEMVER.match(version):
        problems.append(f"package.json version {version!r} is not MAJOR.MINOR.PATCH")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    heads = re.findall(r"^## (\S+)", changelog, re.M)
    if not heads or heads[0] != version:
        problems.append(f"newest CHANGELOG entry is {heads[0] if heads else 'missing'}, expected {version}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if f"claude-sleek-{version}.vsix" not in readme:
        problems.append(f"README does not mention claude-sleek-{version}.vsix")

    showcase = json.loads((ROOT / "demo" / "showcase.json").read_text(encoding="utf-8"))
    if showcase.get("version") != version:
        problems.append(f"demo/showcase.json version is {showcase.get('version')}, expected {version}")

    for theme in pkg["contributes"]["themes"]:
        if not (ROOT / theme["path"]).exists():
            problems.append(f"missing theme file {theme['path']}")
        if f"**{theme['label']}**" not in readme:
            problems.append(f"README does not list **{theme['label']}**")

    if "--tag" in sys.argv:
        tag = sys.argv[sys.argv.index("--tag") + 1]
        if tag.lstrip("v") != version:
            problems.append(f"git tag {tag} does not match package.json version {version}")

    for p in problems:
        print("FAIL", p)
    print(f"\nRelease files agree on {version}." if not problems else f"\n{len(problems)} problem(s) found.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
