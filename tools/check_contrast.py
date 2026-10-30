#!/usr/bin/env python3
"""Check every theme for valid colors and readable contrast.

Run from the repo root:  python tools/check_contrast.py
Exits with status 1 if anything fails, so it can run in CI.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEX = re.compile(r"^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$")


def lum(h):
    h = h.lstrip("#")[:6]
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main():
    failures = 0
    for path in sorted((ROOT / "themes").glob("*.json")):
        theme = json.loads(path.read_text(encoding="utf-8"))
        c = theme["colors"]
        bg = c["editor.background"]
        problems = []

        # 1. every color must be a valid hex value
        for k, v in c.items():
            if not HEX.match(v):
                problems.append(f"invalid color {k} = {v}")
        for tok in theme["tokenColors"]:
            fg = tok["settings"].get("foreground")
            if fg and not HEX.match(fg):
                problems.append(f"invalid token color {fg}")

        # 2. syntax colors against the editor background (4.5:1)
        for tok in theme["tokenColors"]:
            fg = tok["settings"].get("foreground")
            if fg and ratio(fg, bg) < 4.5:
                problems.append(f"syntax {fg} ({tok.get('name') or tok['scope'][0]}) = {ratio(fg, bg):.2f}")

        # 3. UI pairs: (label, foreground key, background key or color, minimum)
        pairs = [
            ("line numbers", "editorLineNumber.foreground", "editor.background", 3.0),
            ("inactive tab", "tab.inactiveForeground", "tab.inactiveBackground", 4.5),
            ("inactive activity icon", "activityBar.inactiveForeground", "activityBar.background", 3.0),
            ("sidebar text", "sideBar.foreground", "sideBar.background", 4.5),
            ("status bar text", "statusBar.foreground", "statusBar.background", 4.5),
            ("breadcrumb", "breadcrumb.foreground", "editor.background", 4.5),
            ("button text", "button.foreground", "button.background", 4.5),
            ("button hover text", "button.foreground", "button.hoverBackground", 4.5),
            ("badge text", "badge.foreground", "badge.background", 4.5),
            ("warning badge", "statusBarItem.warningForeground", "statusBarItem.warningBackground", 4.5),
            ("remote badge", "statusBarItem.remoteForeground", "statusBarItem.remoteBackground", 4.5),
            ("link", "textLink.foreground", "editor.background", 4.5),
            ("placeholder", "input.placeholderForeground", "input.background", 4.5),
            ("inlay hint", "editorInlayHint.foreground", "editorInlayHint.background", 4.5),
            ("active indent guide", "editorIndentGuide.activeBackground1", "editor.background", 3.0),
            ("ANSI white", "terminal.ansiWhite", "terminal.background", 3.0),
            ("ANSI bright black", "terminal.ansiBrightBlack", "terminal.background", 3.0),
        ]
        for label, fg_key, bg_key, minimum in pairs:
            r = ratio(c[fg_key], c[bg_key])
            if r < minimum:
                problems.append(f"{label}: {r:.2f} < {minimum}")

        status = "FAIL" if problems else "ok"
        print(f"{status:4} {theme['name']}")
        for p in problems:
            print("       -", p)
        failures += len(problems)

    print("\nAll themes pass." if not failures else f"\n{failures} problem(s) found.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
