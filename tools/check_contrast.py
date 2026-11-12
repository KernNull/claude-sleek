#!/usr/bin/env python3
"""Check every theme for valid colors and readable contrast.

Run from the repo root:  python tools/check_contrast.py
Exits with status 1 if anything fails, so it can run in CI.

Targets: 4.5:1 for text, 3:1 for icons, charts, line numbers and ANSI black, 4:1 for bright ANSI colors.
High contrast themes (type "hc" / "hcLight") must clear a stricter bar: 7:1, 4.5:1 and 6:1 respectively.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEX = re.compile(r"^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$")

HC_TYPES = ("hc", "hcLight")
HC_SCALE = {4.5: 7.0, 4.0: 6.0, 3.0: 4.5}


def need(minimum, hc):
    """The minimum ratio for a check, raised for high contrast themes."""
    return HC_SCALE.get(minimum, minimum) if hc else minimum


def lum(h):
    h = h.lstrip("#")[:6]
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def over(fg, bg):
    """Composite an 8-digit hex color (with alpha) over a solid background."""
    fg = fg.lstrip("#")
    alpha = int(fg[6:8], 16) / 255 if len(fg) == 8 else 1.0
    f = [int(fg[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(bg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(x * alpha + y * (1 - alpha)) for x, y in zip(f, b))


def extra_pairs(c):
    """Yield (label, foreground, background, minimum ratio): the 1.1.2 additions."""
    editor = c["editor.background"]
    fg = c["editor.foreground"]

    # bracket pair colors are text, so they get the text threshold
    for i in range(1, 7):
        yield f"bracket color {i}", c[f"editorBracketHighlight.foreground{i}"], editor, 4.5
    yield "unexpected bracket", c["editorBracketHighlight.unexpectedBracket.foreground"], editor, 4.5

    # chart colors are graphical, so 3:1
    for n in ["orange", "red", "green", "blue", "yellow", "purple"]:
        yield f"charts.{n}", c[f"charts.{n}"], editor, 3.0

    # editor text on translucent highlights
    yield "text on selection", fg, over(c["editor.selectionBackground"], editor), 4.5
    yield "text on find match", fg, over(c["editor.findMatchBackground"], editor), 4.5
    yield "text on line highlight", fg, over(c["editor.lineHighlightBackground"], editor), 4.5
    yield "text on inserted diff", fg, over(c["diffEditor.insertedTextBackground"], over(c["diffEditor.insertedLineBackground"], editor)), 4.5
    yield "text on removed diff", fg, over(c["diffEditor.removedTextBackground"], over(c["diffEditor.removedLineBackground"], editor)), 4.5
    yield "terminal text on selection", c["terminal.foreground"], over(c["terminal.selectionBackground"], c["terminal.background"]), 4.5

    # tabs and buttons
    yield "tab hover", c["tab.hoverForeground"], c["tab.hoverBackground"], 4.5
    yield "secondary button", c["button.secondaryForeground"], c["button.secondaryBackground"], 4.5
    yield "secondary button hover", c["button.secondaryForeground"], c["button.secondaryHoverBackground"], 4.5

    # input text on validation tints
    inp = c["input.background"]
    for kind in ("error", "warning", "info"):
        yield f"input {kind} text", c["input.foreground"], over(c[f"inputValidation.{kind}Background"], inp), 4.5

    # menus, quick input and suggest widget selections
    yield "menu selection", c["menu.selectionForeground"], over(c["menu.selectionBackground"], c["menu.background"]), 4.5
    yield "quick input focus", c["quickInputList.focusForeground"], over(c["quickInputList.focusBackground"], c["quickInput.background"]), 4.5
    yield "suggest selection", c["editorSuggestWidget.foreground"], over(c["editorSuggestWidget.selectedBackground"], c["editorSuggestWidget.background"]), 4.5
    yield "suggest highlight on selection", c["editorSuggestWidget.highlightForeground"], over(c["editorSuggestWidget.selectedBackground"], c["editorSuggestWidget.background"]), 4.5


def v2_pairs(c):
    """Yield (label, foreground, background, minimum ratio): the 2.0.0 additions."""
    editor = c["editor.background"]
    side = c["sideBar.background"]
    panel = c["panel.background"]

    # problems icons are graphical
    for kind in ("Error", "Warning", "Info"):
        yield f"problems {kind.lower()} icon", c[f"problems{kind}Icon.foreground"], panel, 3.0

    # debug console text sits on the panel
    for kind in ("error", "warning", "info", "source"):
        yield f"debug console {kind}", c[f"debugConsole.{kind}Foreground"], panel, 4.5

    # source control text on the sidebar
    for k in ("scm.historyItemAdditionsForeground", "scm.historyItemDeletionsForeground",
              "gitDecoration.submoduleResourceForeground"):
        yield k, c[k], side, 4.5

    yield "terminal hint", c["terminal.initialHintForeground"], c["terminal.background"], 4.5
    yield "preformatted text", c["textPreformat.foreground"], c["textPreformat.background"], 4.5
    yield "banner text", c["banner.foreground"], c["banner.background"], 4.5
    yield "ANSI black", c["terminal.ansiBlack"], c["terminal.background"], 3.0
    yield "light bulb", c["editorLightBulb.foreground"], editor, 3.0


def pairs_for(c):
    """Yield (label, foreground, background, minimum ratio) for one theme."""
    editor = c["editor.background"]
    side = c["sideBar.background"]
    raised = c["editorWidget.background"]
    term = c["terminal.background"]

    # (label, foreground key, background key, minimum)
    keyed = [
        ("line numbers", "editorLineNumber.foreground", "editor.background", 3.0),
        ("active line number", "editorLineNumber.activeForeground", "editor.background", 4.5),
        ("inactive tab", "tab.inactiveForeground", "tab.inactiveBackground", 4.5),
        ("unfocused active tab", "tab.unfocusedActiveForeground", "tab.unfocusedActiveBackground", 4.5),
        ("inactive activity icon", "activityBar.inactiveForeground", "activityBar.background", 3.0),
        ("sidebar text", "sideBar.foreground", "sideBar.background", 4.5),
        ("status bar text", "statusBar.foreground", "statusBar.background", 4.5),
        ("breadcrumb", "breadcrumb.foreground", "editor.background", 4.5),
        ("description text", "descriptionForeground", "editor.background", 4.5),
        ("error text", "errorForeground", "editor.background", 4.5),
        ("button text", "button.foreground", "button.background", 4.5),
        ("button hover text", "button.foreground", "button.hoverBackground", 4.5),
        ("badge text", "badge.foreground", "badge.background", 4.5),
        ("warning badge", "statusBarItem.warningForeground", "statusBarItem.warningBackground", 4.5),
        ("error badge", "statusBarItem.errorForeground", "statusBarItem.errorBackground", 4.5),
        ("remote badge", "statusBarItem.remoteForeground", "statusBarItem.remoteBackground", 4.5),
        ("link", "textLink.foreground", "editor.background", 4.5),
        ("link hover", "textLink.activeForeground", "editor.background", 4.5),
        ("placeholder", "input.placeholderForeground", "input.background", 4.5),
        ("inlay hint", "editorInlayHint.foreground", "editorInlayHint.background", 4.5),
        ("active indent guide", "editorIndentGuide.activeBackground1", "editor.background", 3.0),
        ("editor error", "editorError.foreground", "editor.background", 4.5),
        ("editor warning", "editorWarning.foreground", "editor.background", 4.5),
        ("editor info", "editorInfo.foreground", "editor.background", 4.5),
        ("list error", "list.errorForeground", "sideBar.background", 4.5),
        ("list warning", "list.warningForeground", "sideBar.background", 4.5),
        ("picker group", "pickerGroup.foreground", "editorWidget.background", 4.5),
        ("suggest highlight", "editorSuggestWidget.highlightForeground", "editorWidget.background", 4.5),
        ("notification link", "notificationLink.foreground", "notifications.background", 4.5),
        ("ANSI white", "terminal.ansiWhite", "terminal.background", 3.0),
        ("ANSI bright black", "terminal.ansiBrightBlack", "terminal.background", 3.0),
    ]
    for label, fk, bk, minimum in keyed:
        yield label, c[fk], c[bk], minimum

    for k in c:
        if k.startswith("gitDecoration.") and k.endswith("Foreground"):
            yield k, c[k], side, 4.5
        if k.startswith("symbolIcon.") and k.endswith("Foreground"):
            yield k, c[k], raised, 3.0
        if k.startswith(("testing.icon", "notebookStatus")) and k.endswith(("Passed", "Failed", "Errored", "Queued", "Unset", "Skipped", "Foreground")):
            yield k, c[k], editor, 3.0
    for n in ["Red", "Green", "Yellow", "Blue", "Magenta", "Cyan"]:
        yield f"ANSI {n}", c[f"terminal.ansi{n}"], term, 4.5
        yield f"ANSI bright {n}", c[f"terminal.ansiBright{n}"], term, 4.0

    # text on translucent hover / selection backgrounds
    yield "status bar hover", c["statusBar.foreground"], over(c["statusBarItem.hoverBackground"], c["statusBar.background"]), 4.5
    yield "list hover", c["list.hoverForeground"], over(c["list.hoverBackground"], side), 4.5
    yield "list selection", c["list.activeSelectionForeground"], over(c["list.activeSelectionBackground"], side), 4.5
    yield "sidebar text on selection", c["sideBar.foreground"], over(c["list.activeSelectionBackground"], side), 4.5


def main():
    failures = 0
    for path in sorted((ROOT / "themes").glob("*.json")):
        theme = json.loads(path.read_text(encoding="utf-8"))
        c = theme["colors"]
        bg = c["editor.background"]
        hc = theme["type"] in HC_TYPES
        problems = []

        # 1. every color must be a valid hex value
        for k, v in c.items():
            if not HEX.match(v):
                problems.append(f"invalid color {k} = {v}")
        for tok in theme["tokenColors"]:
            fg = tok["settings"].get("foreground")
            if fg and not HEX.match(fg):
                problems.append(f"invalid token color {fg}")

        # 2. syntax colors against the editor background (4.5:1, or 7:1 for high contrast)
        for tok in theme["tokenColors"]:
            fg = tok["settings"].get("foreground")
            if fg and ratio(fg, bg) < need(4.5, hc):
                problems.append(f"syntax {fg} ({tok.get('name') or tok['scope'][0]}) = {ratio(fg, bg):.2f}")

        # 3. UI pairs
        for label, fg, back, minimum in list(pairs_for(c)) + list(extra_pairs(c)) + list(v2_pairs(c)):
            r = ratio(fg[:7], back[:7])
            if r < need(minimum, hc):
                problems.append(f"{label}: {r:.2f} < {need(minimum, hc)}")

        status = "FAIL" if problems else "ok"
        print(f"{status:4} {theme['name']}")
        for p in problems:
            print("       -", p)
        failures += len(problems)

    print("\nAll themes pass." if not failures else f"\n{failures} problem(s) found.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
