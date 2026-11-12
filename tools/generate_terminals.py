#!/usr/bin/env python3
"""Generate the Windows Terminal color schemes from the theme palettes.

Run from the repo root:  python tools/generate_terminals.py
Check only (for CI):     python tools/generate_terminals.py --check

The schemes use the same palettes as tools/generate_themes.py, so a color changed there
shows up here after regenerating. One scheme is written per distinct palette; the No Italics
themes are skipped because italics do not exist in a terminal color scheme.
Output: terminals/windows-terminal/claude-sleek.json
"""
import json
import sys
from pathlib import Path

from generate_themes import THEMES

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "terminals" / "windows-terminal" / "claude-sleek.json"

# the same translucent selection the editor terminal uses (accent at 0x38 alpha)
SELECTION_ALPHA = 0x38 / 255

COLOR_NAMES = ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]


def over(fg, bg, alpha):
    """Blend fg over a solid bg. Windows Terminal ignores alpha in schemes, so we pre-blend."""
    f = [int(fg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(bg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(x * alpha + y * (1 - alpha)) for x, y in zip(f, b))


def scheme(label, p):
    s = {
        "name": label,
        "background": p["bg"],
        "foreground": p["fg"],
        "cursorColor": p["accent"],
        "selectionBackground": over(p["accent"], p["bg"], SELECTION_ALPHA),
    }
    for name, color in zip(COLOR_NAMES, p["ansi"]):
        s[name] = color
    for name, color in zip(COLOR_NAMES, p["ansiB"]):
        s["bright" + name.capitalize()] = color
    return s


def build():
    schemes = [scheme(label, pal) for stem, label, _t, pal, _i in THEMES
               if not stem.endswith("-no-italics")]
    return json.dumps({"schemes": schemes}, indent=2) + "\n"


def main():
    text = build()
    if "--check" in sys.argv[1:]:
        current = OUT.read_bytes().replace(b"\r\n", b"\n") if OUT.exists() else None
        if current != text.encode("utf-8"):
            print("out of date:", OUT.relative_to(ROOT))
            print("\nRun: python tools/generate_terminals.py")
            sys.exit(1)
        print("Windows Terminal schemes are up to date.")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
