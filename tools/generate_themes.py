#!/usr/bin/env python3
"""Generate the Claude Sleek theme files.

Run from the repo root:  python tools/generate_themes.py
Edit the palettes below, regenerate, then run tools/check_contrast.py.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / "themes"

# ----------------------------------------------------------------------------
# Palettes
# ----------------------------------------------------------------------------
DARK = dict(
    bg="#1c1b19", deep="#161513", raised="#24221f", hover="#2b2926", border="#2e2b27",
    fg="#ebe6dd", dim="#a8a196", faint="#8f887b", gutter="#7d766a", comment="#8a8376", punct="#9b9488",
    accent="#d97757", accentHi="#e8896a", onAccent="#1a1816", shadow="#00000066",
    kw="#e48a6c", str="#abc58c", num="#c8a5ea", fn="#efca8e", type="#8fbde3",
    prop="#d9c3ac", param="#ecb99d", op="#c2b8a8",
    red="#ef7a7d", green="#a6c987", gold="#e8c27a", blue="#7fb0dc", violet="#c3a1e8",
    teal="#7ccfc0", rose="#ec8fa5",
    ansi=["#2e2b27", "#ef7a7d", "#a6c987", "#e8c27a", "#7fb0dc", "#c3a1e8", "#7ccfc0", "#cfc8bb"],
    ansiB=["#8a8376", "#f59a9c", "#bddca1", "#f3d596", "#a0c6ea", "#d5baf0", "#9ce0d3", "#f4efe6"],
)

# True-black variant for OLED screens: same syntax colors, darker surfaces.
BLACK = {**DARK, **dict(
    bg="#000000", deep="#0a0908", raised="#141211", hover="#1d1b19", border="#242220",
    shadow="#000000aa",
)}

LIGHT = dict(
    bg="#faf9f5", deep="#f2f0e8", raised="#f5f3ec", hover="#ebe8dd", border="#e2ded1",
    fg="#2b2926", dim="#5a554c", faint="#716b61", gutter="#8c867a", comment="#766f64", punct="#716b61",
    accent="#b84d30", accentHi="#a8442a", onAccent="#fffdf8", shadow="#2b292622",
    kw="#b84d2d", str="#4a7a2e", num="#7d47b0", fn="#8a5800", type="#1d6ba5",
    prop="#6b5441", param="#a3512f", op="#6f685d",
    red="#c93a45", green="#4a7a2e", gold="#9c6600", blue="#1d6ba5", violet="#7d47b0",
    teal="#127f72", rose="#b8386a",
    ansi=["#2b2926", "#c93a45", "#4a7a2e", "#9c6600", "#1d6ba5", "#7d47b0", "#127f72", "#6f695f"],
    ansiB=["#6a645a", "#cf5059", "#5a8641", "#a37112", "#3d80b2", "#8f61bb", "#25897d", "#8a8478"],
    # slightly darker status tints so file names stay at 4.5:1 on the sidebar
    gitAdded="#46742c", gitDeleted="#bd3741", gitUntracked="#11766a", gitConflict="#905e00",
    # the matched-text highlight in the suggest list needs a darker tone on its selected row
    suggestHi="#a04024",
)

# (file stem, label, base type, palette, italics?)
THEMES = [
    ("claude-ember", "Claude Ember", "dark", DARK, True),
    ("claude-ember-black", "Claude Ember Black", "dark", BLACK, True),
    ("claude-parchment", "Claude Parchment", "light", LIGHT, True),
    ("claude-ember-no-italics", "Claude Ember (No Italics)", "dark", DARK, False),
    ("claude-ember-black-no-italics", "Claude Ember Black (No Italics)", "dark", BLACK, False),
    ("claude-parchment-no-italics", "Claude Parchment (No Italics)", "light", LIGHT, False),
]


# ----------------------------------------------------------------------------
# Workbench (UI) colors
# ----------------------------------------------------------------------------
def workbench_colors(p):
    a = p["accent"]
    ui = {
        # base
        "focusBorder": a + "66",
        "foreground": p["fg"],
        "descriptionForeground": p["dim"],
        "errorForeground": p["red"],
        "icon.foreground": p["dim"],
        "selection.background": a + "55",
        "widget.shadow": p["shadow"],
        "textLink.foreground": a,
        "textLink.activeForeground": p["accentHi"],
        "textCodeBlock.background": p["raised"],
        "textBlockQuote.background": p["raised"],
        "textBlockQuote.border": a,
        "textSeparator.foreground": p["border"],
        "sash.hoverBorder": a,

        # editor
        "editor.background": p["bg"],
        "editor.foreground": p["fg"],
        "editorLineNumber.foreground": p["gutter"],
        "editorLineNumber.activeForeground": a,
        "editorCursor.foreground": a,
        "editor.selectionBackground": a + "38",
        "editor.inactiveSelectionBackground": a + "20",
        "editor.selectionHighlightBackground": a + "22",
        "editor.wordHighlightBackground": p["blue"] + "22",
        "editor.wordHighlightStrongBackground": a + "30",
        "editor.findMatchBackground": p["gold"] + "55",
        "editor.findMatchHighlightBackground": p["gold"] + "28",
        "editor.findRangeHighlightBackground": a + "14",
        "editor.hoverHighlightBackground": a + "18",
        "editor.lineHighlightBackground": p["hover"] + "99",
        "editor.lineHighlightBorder": "#00000000",
        "editor.rangeHighlightBackground": a + "14",
        "editor.foldBackground": a + "14",
        "editor.snippetTabstopHighlightBackground": a + "26",
        "editor.snippetFinalTabstopHighlightBorder": a + "88",
        "editorLink.activeForeground": a,
        "editorUnnecessaryCode.opacity": "#000000b0",
        "editorWhitespace.foreground": p["border"],
        "editorIndentGuide.background1": p["border"],
        "editorIndentGuide.activeBackground1": p["gutter"],
        "editorRuler.foreground": p["border"],
        "editorCodeLens.foreground": p["faint"],
        "editorInlayHint.foreground": p["faint"],
        "editorInlayHint.background": p["raised"],
        "editorGhostText.foreground": p["gutter"],
        "editorBracketMatch.background": a + "30",
        "editorBracketMatch.border": "#00000000",
        "editorBracketHighlight.unexpectedBracket.foreground": p["red"],
        "editorOverviewRuler.border": "#00000000",
        "editorOverviewRuler.errorForeground": p["red"],
        "editorOverviewRuler.warningForeground": p["gold"],
        "editorOverviewRuler.infoForeground": p["blue"],
        "editorOverviewRuler.findMatchForeground": p["gold"] + "99",
        "editorOverviewRuler.modifiedForeground": p["blue"] + "99",
        "editorOverviewRuler.addedForeground": p["green"] + "99",
        "editorOverviewRuler.deletedForeground": p["red"] + "99",
        "editorError.foreground": p["red"],
        "editorWarning.foreground": p["gold"],
        "editorInfo.foreground": p["blue"],
        "editorHint.foreground": p["teal"],
        "editorGutter.background": p["bg"],
        "editorGutter.modifiedBackground": p["blue"],
        "editorGutter.addedBackground": p["green"],
        "editorGutter.deletedBackground": p["red"],
        "editorGutter.foldingControlForeground": p["dim"],
        "editorGroup.border": p["border"],
        "editorGroup.dropBackground": a + "22",
        "editorGroupHeader.tabsBackground": p["deep"],
        "editorGroupHeader.tabsBorder": "#00000000",
        "editorGroupHeader.noTabsBackground": p["bg"],

        # sticky scroll
        "editorStickyScroll.background": p["raised"],
        "editorStickyScrollHover.background": p["hover"],
        "editorStickyScroll.border": p["border"],
        "editorStickyScroll.shadow": p["shadow"],
        "sideBarStickyScroll.background": p["deep"],
        "sideBarStickyScroll.border": p["border"],
        "panelStickyScroll.background": p["bg"],
        "panelStickyScroll.border": p["border"],

        # widgets
        "editorWidget.background": p["raised"],
        "editorWidget.foreground": p["fg"],
        "editorWidget.border": p["border"],
        "editorWidget.resizeBorder": a,
        "editorSuggestWidget.background": p["raised"],
        "editorSuggestWidget.border": p["border"],
        "editorSuggestWidget.foreground": p["fg"],
        "editorSuggestWidget.selectedBackground": a + "26",
        "editorSuggestWidget.highlightForeground": p.get("suggestHi", p["accentHi"]),
        "editorHoverWidget.background": p["raised"],
        "editorHoverWidget.border": p["border"],
        "editorHoverWidget.statusBarBackground": p["hover"],
        "editorActionList.background": p["raised"],
        "editorActionList.foreground": p["fg"],
        "editorActionList.focusBackground": a + "26",
        "peekView.border": a,
        "peekViewEditor.background": p["deep"],
        "peekViewEditor.matchHighlightBackground": p["gold"] + "44",
        "peekViewResult.background": p["raised"],
        "peekViewResult.selectionBackground": a + "26",
        "peekViewResult.matchHighlightBackground": p["gold"] + "44",
        "peekViewTitle.background": p["raised"],
        "peekViewTitleLabel.foreground": p["fg"],
        "peekViewTitleDescription.foreground": p["dim"],

        # diff / merge
        "diffEditor.insertedTextBackground": p["green"] + "22",
        "diffEditor.removedTextBackground": p["red"] + "22",
        "diffEditor.insertedLineBackground": p["green"] + "14",
        "diffEditor.removedLineBackground": p["red"] + "14",
        "diffEditor.diagonalFill": p["border"],
        "diffEditorGutter.insertedLineBackground": p["green"] + "33",
        "diffEditorGutter.removedLineBackground": p["red"] + "33",
        "merge.currentHeaderBackground": p["blue"] + "55",
        "merge.incomingHeaderBackground": p["green"] + "55",
        "merge.currentContentBackground": p["blue"] + "1e",
        "merge.incomingContentBackground": p["green"] + "1e",

        # activity bar / side bar
        "activityBar.background": p["deep"],
        "activityBar.foreground": p["fg"],
        "activityBar.inactiveForeground": p["gutter"],
        "activityBar.border": "#00000000",
        "activityBar.activeBorder": a,
        "activityBar.activeBackground": "#00000000",
        "activityBarBadge.background": a,
        "activityBarBadge.foreground": p["onAccent"],
        "sideBar.background": p["deep"],
        "sideBar.foreground": p["dim"],
        "sideBar.border": "#00000000",
        "sideBarTitle.foreground": p["fg"],
        "sideBarSectionHeader.background": "#00000000",
        "sideBarSectionHeader.foreground": p["dim"],
        "sideBarSectionHeader.border": p["border"],

        # lists / trees
        "list.activeSelectionBackground": a + "26",
        "list.activeSelectionForeground": p["fg"],
        "list.inactiveSelectionBackground": p["hover"],
        "list.inactiveSelectionForeground": p["fg"],
        "list.hoverBackground": p["hover"] + "aa",
        "list.hoverForeground": p["fg"],
        "list.focusBackground": a + "26",
        "list.focusOutline": "#00000000",
        "list.highlightForeground": a,
        "list.errorForeground": p.get("gitDeleted", p["red"]),
        "list.warningForeground": p.get("gitConflict", p["gold"]),
        "list.dropBackground": a + "22",
        "tree.indentGuidesStroke": p["border"],

        # tabs / breadcrumbs
        "tab.activeBackground": p["bg"],
        "tab.activeForeground": p["fg"],
        "tab.activeBorderTop": a,
        "tab.activeBorder": "#00000000",
        "tab.inactiveBackground": p["deep"],
        "tab.inactiveForeground": p["faint"],
        "tab.hoverBackground": p["hover"],
        "tab.hoverForeground": p["fg"],
        "tab.unfocusedActiveBackground": p["bg"],
        "tab.unfocusedActiveForeground": p["dim"],
        "tab.unfocusedInactiveBackground": p["deep"],
        "tab.border": p["deep"],
        "tab.lastPinnedBorder": p["border"],
        "tab.activeModifiedBorder": p["gold"],
        "tab.inactiveModifiedBorder": p["gold"] + "88",
        "breadcrumb.foreground": p["faint"],
        "breadcrumb.focusForeground": p["fg"],
        "breadcrumb.activeSelectionForeground": a,
        "breadcrumbPicker.background": p["raised"],

        # title bar / menus / command center
        "titleBar.activeBackground": p["deep"],
        "titleBar.activeForeground": p["dim"],
        "titleBar.inactiveBackground": p["deep"],
        "titleBar.inactiveForeground": p["faint"],
        "titleBar.border": "#00000000",
        "commandCenter.background": p["raised"],
        "commandCenter.foreground": p["dim"],
        "commandCenter.border": p["border"],
        "commandCenter.activeBackground": p["hover"],
        "commandCenter.activeForeground": p["fg"],
        "menubar.selectionBackground": p["hover"],
        "menubar.selectionForeground": p["fg"],
        "menu.background": p["raised"],
        "menu.foreground": p["fg"],
        "menu.selectionBackground": a + "26",
        "menu.selectionForeground": p["fg"],
        "menu.separatorBackground": p["border"],
        "menu.border": p["border"],

        # status bar
        "statusBar.background": p["deep"],
        "statusBar.foreground": p["dim"],
        "statusBar.border": "#00000000",
        "statusBar.noFolderBackground": p["deep"],
        "statusBar.debuggingBackground": a,
        "statusBar.debuggingForeground": p["onAccent"],
        "statusBarItem.hoverBackground": p["hover"],
        "statusBarItem.remoteBackground": a,
        "statusBarItem.remoteForeground": p["onAccent"],
        "statusBarItem.prominentBackground": p["hover"],
        "statusBarItem.errorBackground": p["red"],
        "statusBarItem.errorForeground": p["onAccent"],
        "statusBarItem.warningBackground": p["gold"],
        "statusBarItem.warningForeground": p["onAccent"],

        # panel
        "panel.background": p["bg"],
        "panel.border": p["border"],
        "panelTitle.activeForeground": p["fg"],
        "panelTitle.inactiveForeground": p["faint"],
        "panelTitle.activeBorder": a,
        "panelSectionHeader.background": p["deep"],
        "panelInput.border": p["border"],

        # inputs / buttons
        "input.background": p["raised"],
        "input.foreground": p["fg"],
        "input.border": p["border"],
        "input.placeholderForeground": p["faint"],
        "inputOption.activeBackground": a + "33",
        "inputOption.activeBorder": a,
        "inputOption.activeForeground": p["fg"],
        "inputValidation.errorBackground": p["red"] + "22",
        "inputValidation.errorBorder": p["red"],
        "inputValidation.warningBackground": p["gold"] + "22",
        "inputValidation.warningBorder": p["gold"],
        "inputValidation.infoBackground": p["blue"] + "22",
        "inputValidation.infoBorder": p["blue"],
        "dropdown.background": p["raised"],
        "dropdown.foreground": p["fg"],
        "dropdown.border": p["border"],
        "button.background": a,
        "button.foreground": p["onAccent"],
        "button.hoverBackground": p["accentHi"],
        "button.secondaryBackground": p["hover"],
        "button.secondaryForeground": p["fg"],
        "button.secondaryHoverBackground": p["border"],
        "checkbox.background": p["raised"],
        "checkbox.border": p["border"],
        "badge.background": a,
        "badge.foreground": p["onAccent"],
        "progressBar.background": a,
        "keybindingLabel.background": p["hover"],
        "keybindingLabel.foreground": p["fg"],
        "keybindingLabel.border": p["border"],
        "keybindingLabel.bottomBorder": p["border"],
        "quickInput.background": p["raised"],
        "quickInput.foreground": p["fg"],
        "quickInputList.focusBackground": a + "26",
        "quickInputList.focusForeground": p["fg"],
        "quickInputTitle.background": p["hover"],
        "pickerGroup.foreground": a,
        "pickerGroup.border": p["border"],

        # notifications
        "notifications.background": p["raised"],
        "notifications.foreground": p["fg"],
        "notifications.border": p["border"],
        "notificationCenterHeader.background": p["hover"],
        "notificationLink.foreground": a,
        "notificationsErrorIcon.foreground": p["red"],
        "notificationsWarningIcon.foreground": p["gold"],
        "notificationsInfoIcon.foreground": p["blue"],

        # scrollbars / minimap
        "scrollbar.shadow": "#00000000",
        "scrollbarSlider.background": p["gutter"] + "33",
        "scrollbarSlider.hoverBackground": p["gutter"] + "66",
        "scrollbarSlider.activeBackground": a + "88",
        "minimap.background": p["bg"],
        "minimap.selectionHighlight": a + "88",
        "minimap.findMatchHighlight": p["gold"] + "99",
        "minimap.errorHighlight": p["red"],
        "minimap.warningHighlight": p["gold"],
        "minimapSlider.background": p["gutter"] + "22",
        "minimapSlider.hoverBackground": p["gutter"] + "44",
        "minimapSlider.activeBackground": a + "55",
        "minimapGutter.addedBackground": p["green"],
        "minimapGutter.modifiedBackground": p["blue"],
        "minimapGutter.deletedBackground": p["red"],

        # git
        "gitDecoration.addedResourceForeground": p.get("gitAdded", p["green"]),
        "gitDecoration.modifiedResourceForeground": p["blue"],
        "gitDecoration.deletedResourceForeground": p.get("gitDeleted", p["red"]),
        "gitDecoration.untrackedResourceForeground": p.get("gitUntracked", p["teal"]),
        "gitDecoration.ignoredResourceForeground": p["faint"],
        "gitDecoration.conflictingResourceForeground": p.get("gitConflict", p["gold"]),
        "gitDecoration.stageModifiedResourceForeground": p["blue"],
        "gitDecoration.stageDeletedResourceForeground": p.get("gitDeleted", p["red"]),

        # debug
        "debugToolBar.background": p["raised"],
        "debugIcon.breakpointForeground": p["red"],
        "debugIcon.startForeground": p["green"],
        "editor.stackFrameHighlightBackground": p["gold"] + "28",
        "editor.focusedStackFrameHighlightBackground": p["green"] + "28",

        # terminal
        "terminal.background": p["bg"],
        "terminal.foreground": p["fg"],
        "terminal.selectionBackground": a + "38",
        "terminal.inactiveSelectionBackground": a + "20",
        "terminal.findMatchBackground": p["gold"] + "55",
        "terminal.hoverHighlightBackground": a + "18",
        "terminalCursor.foreground": a,
        "terminal.tab.activeBorder": a,
        "terminalCommandDecoration.defaultBackground": p["gutter"],
        "terminalCommandDecoration.successBackground": p["green"],
        "terminalCommandDecoration.errorBackground": p["red"],
        "terminalOverviewRuler.cursorForeground": a + "99",
        "terminalOverviewRuler.findMatchForeground": p["gold"] + "99",

        # settings editor
        "settings.headerForeground": p["fg"],
        "settings.modifiedItemIndicator": a,
        "settings.dropdownBackground": p["raised"],
        "settings.dropdownForeground": p["fg"],
        "settings.dropdownBorder": p["border"],
        "settings.dropdownListBorder": p["border"],
        "settings.textInputBackground": p["raised"],
        "settings.textInputForeground": p["fg"],
        "settings.textInputBorder": p["border"],
        "settings.numberInputBackground": p["raised"],
        "settings.numberInputForeground": p["fg"],
        "settings.numberInputBorder": p["border"],
        "settings.checkboxBackground": p["raised"],
        "settings.checkboxForeground": p["fg"],
        "settings.checkboxBorder": p["border"],
        "settings.focusedRowBackground": a + "14",
        "settings.focusedRowBorder": a + "55",
        "settings.rowHoverBackground": p["hover"] + "88",
        "settings.settingsHeaderHoverForeground": a,

        # notebooks
        "notebook.editorBackground": p["bg"],
        "notebook.cellBorderColor": p["border"],
        "notebook.cellEditorBackground": p["raised"],
        "notebook.cellHoverBackground": p["raised"],
        "notebook.focusedCellBorder": a,
        "notebook.focusedEditorBorder": a,
        "notebook.selectedCellBorder": p["gutter"],
        "notebook.selectedCellBackground": p["hover"] + "88",
        "notebook.inactiveSelectedCellBorder": p["border"],
        "notebook.cellInsertionIndicator": a,
        "notebook.cellToolbarSeparator": p["border"],
        "notebook.outputContainerBackgroundColor": p["raised"],
        "notebookStatusRunningIcon.foreground": a,
        "notebookStatusSuccessIcon.foreground": p["green"],
        "notebookStatusErrorIcon.foreground": p["red"],
        "notebookScrollbarSlider.background": p["gutter"] + "33",
        "notebookScrollbarSlider.hoverBackground": p["gutter"] + "66",
        "notebookScrollbarSlider.activeBackground": a + "88",

        # testing
        "testing.iconPassed": p["green"],
        "testing.iconFailed": p["red"],
        "testing.iconErrored": p["red"],
        "testing.iconQueued": p["gold"],
        "testing.iconUnset": p["dim"],
        "testing.iconSkipped": p["faint"],
        "testing.runAction": p["green"],
        "testing.peekBorder": p["red"],
        "testing.peekHeaderBackground": p["raised"],

        # chat panel
        "chat.requestBackground": p["raised"],
        "chat.requestBorder": p["border"],
        "chat.requestBubbleBackground": p["raised"],
        "chat.requestBubbleHoverBackground": p["hover"],
        "chat.slashCommandBackground": a + "22",
        "chat.slashCommandForeground": a,
        "chat.avatarBackground": p["hover"],
        "chat.avatarForeground": p["fg"],
        "chat.linesAddedForeground": p["green"],
        "chat.linesRemovedForeground": p["red"],
        "chat.editedFileForeground": p["gold"],

        # misc
        "extensionButton.prominentBackground": a,
        "extensionButton.prominentForeground": p["onAccent"],
        "extensionButton.prominentHoverBackground": p["accentHi"],
        "extensionIcon.starForeground": p["gold"],
        "extensionIcon.verifiedForeground": p["teal"],
        "welcomePage.tileBackground": p["raised"],
        "welcomePage.tileHoverBackground": p["hover"],
        "walkThrough.embeddedEditorBackground": p["raised"],
        "charts.orange": a, "charts.red": p["red"], "charts.green": p["green"],
        "charts.blue": p["blue"], "charts.yellow": p["gold"], "charts.purple": p["violet"],
    }

    # bracket pair colors + softened guides (the active guide used to be loud)
    brackets = [a, p["gold"], p["blue"], p["green"], p["violet"], p["teal"]]
    for i, col in enumerate(brackets, 1):
        ui[f"editorBracketHighlight.foreground{i}"] = col
        ui[f"editorBracketPairGuide.background{i}"] = col + "22"
        ui[f"editorBracketPairGuide.activeBackground{i}"] = col + "66"

    # symbol icons (outline, breadcrumbs, quick open)
    sym = {
        "array": p["gold"], "boolean": p["num"], "class": p["type"], "color": p["teal"],
        "constant": p["gold"], "constructor": p["fn"], "enumerator": p["type"],
        "enumeratorMember": p["gold"], "event": p["rose"], "field": p["prop"],
        "file": p["dim"], "folder": p["dim"], "function": p["fn"], "interface": p["type"],
        "key": p["prop"], "keyword": p["kw"], "method": p["fn"], "module": p["teal"],
        "namespace": p["type"], "null": p["num"], "number": p["num"], "object": p["gold"],
        "operator": p["op"], "package": p["teal"], "property": p["prop"],
        "reference": p["blue"], "snippet": p["violet"], "string": p["str"],
        "struct": p["type"], "text": p["dim"], "typeParameter": p["type"],
        "unit": p["num"], "variable": p["fg"],
    }
    for name, col in sym.items():
        ui[f"symbolIcon.{name}Foreground"] = col

    # terminal ANSI palette
    names = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
    for n, c in zip(names, p["ansi"]):
        ui[f"terminal.ansi{n}"] = c
    for n, c in zip(names, p["ansiB"]):
        ui[f"terminal.ansiBright{n}"] = c
    return ui


# ----------------------------------------------------------------------------
# Syntax (TextMate) colors
# ----------------------------------------------------------------------------
def token_colors(p):
    def t(scope, fg=None, style=None, name=None):
        s = {}
        if fg:
            s["foreground"] = fg
        if style is not None:
            s["fontStyle"] = style
        d = {"scope": scope, "settings": s}
        if name:
            d["name"] = name
        return d

    kw, st, num, fn, ty, var, prop, par, op, cm = (p[k] for k in
        ("kw", "str", "num", "fn", "type", "fg", "prop", "param", "op", "comment"))
    punct, teal, gold, rose, blue, acc = p["punct"], p["teal"], p["gold"], p["rose"], p["blue"], p["accent"]

    return [
        # ---- general ----
        t(["comment", "punctuation.definition.comment"], cm, "italic", "Comments"),
        t(["comment.block.documentation", "comment.block.javadoc"], cm, "italic"),
        t(["keyword", "keyword.control", "storage.type", "storage.modifier"], kw, "", "Keywords"),
        t(["keyword.operator", "keyword.operator.assignment", "keyword.operator.arithmetic"], op, "", "Operators"),
        t(["keyword.operator.new", "keyword.operator.expression", "keyword.operator.logical.python", "keyword.operator.word"], kw, ""),
        t(["storage.type.function", "storage.type.class", "storage.type.js"], kw, "italic"),
        t(["string", "string.quoted", "string.template"], st, "", "Strings"),
        t(["punctuation.definition.string"], st, ""),
        t(["constant.character.escape", "string.regexp", "constant.other.character-class.regexp"], teal, "", "Escapes & regex"),
        t(["punctuation.definition.template-expression", "punctuation.section.embedded"], kw, ""),
        t(["constant.numeric", "constant.language", "constant.character", "support.constant"], num, "", "Numbers & constants"),
        t(["constant.other", "variable.other.constant", "variable.other.enummember"], gold, ""),
        t(["entity.name.function", "support.function", "meta.function-call entity.name.function", "variable.function"], fn, "", "Functions"),
        t(["meta.function-call.generic", "meta.method-call"], fn, ""),
        t(["entity.name.type", "entity.name.class", "entity.name.namespace", "support.class", "support.type", "entity.other.inherited-class"], ty, "", "Types & classes"),
        t(["variable", "variable.other", "variable.other.readwrite"], var, "", "Variables"),
        t(["variable.parameter", "meta.parameters variable"], par, "italic", "Parameters"),
        t(["variable.language", "variable.language.this", "variable.language.self", "variable.language.super"], rose, "italic", "this / self"),
        t(["variable.other.property", "variable.other.object.property", "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], prop, "", "Properties"),
        t(["punctuation", "meta.brace", "punctuation.separator", "punctuation.terminator", "punctuation.accessor"], punct, "", "Punctuation"),
        t(["entity.name.tag"], kw, "", "Tags"),
        t(["entity.other.attribute-name", "entity.other.attribute-name.html"], fn, "italic", "Attributes"),
        t(["support.class.component", "entity.name.tag.tsx", "entity.name.tag.jsx"], ty, ""),
        t(["meta.decorator", "entity.name.function.decorator", "punctuation.decorator", "meta.annotation", "storage.type.annotation"], teal, "", "Decorators"),
        t(["entity.name.type.module", "support.module", "meta.import variable.other.readwrite", "entity.name.import"], var, ""),
        t(["keyword.control.import", "keyword.control.export", "keyword.control.from", "keyword.control.default"], kw, "italic"),
        t(["invalid", "invalid.illegal"], p["red"], "underline"),
        t(["invalid.deprecated"], gold, "strikethrough"),
        t(["keyword.other.special-method", "support.function.builtin", "support.function.magic.python", "support.variable.magic.python"], teal, ""),
        t(["entity.name.function.macro", "entity.name.lifetime.rust", "storage.modifier.lifetime.rust"], teal, ""),
        t(["variable.other.env", "variable.other.normal.shell", "punctuation.definition.variable.shell"], gold, ""),
        t(["markup.inserted"], p["green"], ""),
        t(["markup.deleted"], p["red"], ""),
        t(["markup.changed"], blue, ""),
        t(["meta.diff.header", "meta.diff.range"], p["violet"], ""),

        # ---- Markdown ----
        t(["markup.heading", "entity.name.section.markdown", "punctuation.definition.heading.markdown"], acc, "bold", "Markdown headings"),
        t(["markup.bold"], gold, "bold"),
        t(["markup.italic"], rose, "italic"),
        t(["markup.strikethrough"], cm, "strikethrough"),
        t(["markup.inline.raw", "markup.fenced_code.block", "markup.raw", "markup.inline.raw.string.markdown"], st, ""),
        t(["fenced_code.block.language", "fenced_code.block.language.markdown"], teal, "", "Markdown code fence language"),
        t(["punctuation.definition.markdown", "punctuation.definition.raw.markdown", "punctuation.definition.fenced.markdown", "punctuation.definition.bold.markdown", "punctuation.definition.italic.markdown"], punct, ""),
        t(["markup.underline.link", "string.other.link"], blue, "underline"),
        t(["string.other.link.title.markdown", "string.other.link.description.markdown", "constant.other.reference.link.markdown"], blue, "", "Markdown link text"),
        t(["markup.underline.link.markdown", "markup.underline.link.image.markdown"], p["faint"], "underline", "Markdown link URL"),
        t(["markup.quote", "markup.quote.markdown"], cm, "italic"),
        t(["punctuation.definition.quote.begin.markdown"], acc, ""),
        t(["markup.list punctuation.definition.list.begin", "beginning.punctuation.definition.list.markdown", "punctuation.definition.list.begin.markdown"], acc, ""),
        t(["meta.separator.markdown"], p["faint"], "bold"),

        # ---- JSON ----
        t(["support.type.property-name.json", "punctuation.support.type.property-name.begin.json", "punctuation.support.type.property-name.end.json"], prop, "", "JSON keys"),
        t(["punctuation.definition.dictionary", "punctuation.definition.array", "punctuation.separator.dictionary", "punctuation.separator.array"], punct, ""),

        # ---- YAML ----
        t(["entity.name.type.anchor.yaml", "variable.other.alias.yaml", "punctuation.definition.anchor.yaml", "punctuation.definition.alias.yaml"], teal, "", "YAML anchors"),
        t(["punctuation.definition.block.sequence.item.yaml"], acc, ""),
        t(["punctuation.separator.key-value.mapping.yaml"], punct, ""),
        t(["keyword.control.flow.block-scalar.literal.yaml", "keyword.control.flow.block-scalar.folded.yaml", "storage.modifier.chomping-indicator.yaml"], kw, ""),
        t(["entity.other.document.begin.yaml", "entity.other.document.end.yaml"], p["faint"], ""),

        # ---- HTML ----
        t(["punctuation.definition.tag", "punctuation.definition.tag.begin.html", "punctuation.definition.tag.end.html"], punct, "", "Tag brackets"),
        t(["punctuation.separator.key-value.html"], punct, ""),
        t(["meta.tag.metadata.doctype.html", "meta.tag.metadata.doctype.html entity.name.tag", "meta.tag.metadata.doctype.html punctuation.definition.tag"], p["faint"], "", "DOCTYPE"),
        t(["constant.character.entity.html", "punctuation.definition.entity.html"], teal, "", "HTML entities"),

        # ---- CSS / SCSS / Less ----
        t(["entity.name.tag.css", "entity.name.tag.scss", "entity.name.tag.less"], kw, "", "CSS element selectors"),
        t(["entity.other.attribute-name.class.css", "entity.other.attribute-name.class.scss", "entity.other.attribute-name.class.less"], fn, "", "CSS class selectors"),
        t(["entity.other.attribute-name.id.css", "entity.other.attribute-name.id.scss", "entity.other.attribute-name.id.less"], gold, "", "CSS id selectors"),
        t(["punctuation.definition.entity.css", "punctuation.definition.entity.scss"], punct, ""),
        t(["entity.other.attribute-name.pseudo-class.css", "entity.other.attribute-name.pseudo-element.css"], kw, "italic", "CSS pseudo selectors"),
        t(["support.type.property-name.css", "support.type.vendored.property-name.css", "support.type.property-name.scss"], prop, "", "CSS properties"),
        t(["support.constant.property-value.css", "support.constant.font-name.css", "support.constant.color.w3c-standard-color-name.css", "support.constant.property-value.scss"], ty, "", "CSS value keywords"),
        t(["constant.numeric.css", "constant.numeric.scss", "keyword.other.unit.css", "keyword.other.unit.scss", "constant.other.color.rgb-value.hex.css", "punctuation.definition.constant.css"], num, "", "CSS numbers & colors"),
        t(["support.function.misc.css", "support.function.url.css", "support.function.gradient.css", "support.function.transform.css", "support.function.calc.css", "support.function.misc.scss"], fn, "", "CSS functions"),
        t(["variable.css", "variable.argument.css", "variable.scss", "variable.other.less", "variable.parameter.url.css"], teal, "", "CSS variables"),
        t(["keyword.control.at-rule", "punctuation.definition.keyword.css", "punctuation.definition.keyword.scss"], kw, "italic", "CSS at-rules"),
        t(["keyword.other.important.css"], rose, ""),
    ]


def semantic_colors(p):
    ty, fn, prop, par = p["type"], p["fn"], p["prop"], p["param"]
    return {
        "class": ty, "interface": ty, "enum": ty, "struct": ty, "typeParameter": ty,
        "type": ty, "namespace": ty,
        "function": fn, "method": fn, "macro": p["teal"],
        "parameter": {"foreground": par, "italic": True},
        "variable": p["fg"],
        "variable.readonly": p["gold"],
        "variable.defaultLibrary": p["teal"],
        "property": prop,
        "enumMember": p["gold"],
        "decorator": p["teal"],
        "selfParameter": {"foreground": p["rose"], "italic": True},
        "*.deprecated": {"strikethrough": True},
    }


def strip_italics(tokens, semantic):
    for tok in tokens:
        fs = tok["settings"].get("fontStyle")
        if fs:
            tok["settings"]["fontStyle"] = fs.replace("italic", "").strip()
    for k, v in semantic.items():
        if isinstance(v, dict) and v.get("italic"):
            v["italic"] = False


def build(label, ttype, p, italics):
    tokens = token_colors(p)
    semantic = semantic_colors(p)
    if not italics:
        strip_italics(tokens, semantic)
    return {
        "$schema": "vscode://schemas/color-theme",
        "name": label,
        "type": ttype,
        "semanticHighlighting": True,
        "semanticTokenColors": semantic,
        "colors": workbench_colors(p),
        "tokenColors": tokens,
    }

def render(obj):
    return json.dumps(obj, indent=2) + "\n"

def main():
    check = "--check" in sys.argv[1:]
    expected = {}
    contributes = []
    for stem, label, ttype, pal, italics in THEMES:
        expected[THEMES_DIR / f"{stem}.json"] = render(build(label, ttype, pal, italics))
        contributes.append({
            "label": label,
            "uiTheme": "vs-dark" if ttype == "dark" else "vs",
            "path": f"./themes/{stem}.json",
        })
    pkg_path = ROOT / "package.json"
    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))

    if check:
        stale = []
        for path, text in expected.items():
            if not path.exists() or path.read_bytes().replace(b"\r\n", b"\n") != text.encode("utf-8"):
                stale.append(path.relative_to(ROOT))
        for path in sorted(THEMES_DIR.glob("*.json")):
            if path not in expected:
                stale.append(path.relative_to(ROOT)) # a theme file the script doesn't produce
        if pkg.get("contributes", {}).get("themes") != contributes:
            stale.append(pkg_path.relative_to(ROOT))
        for p in stale:
            print("out of date:", p)
        print("\nGenerated files are up to date." if not stale else
                "\nRun: python tools/generate_themes.py")
        sys.exit(1 if stale else 0)

    THEMES_DIR.mkdir(exist_ok=True)
    for path, text in expected.items():
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print("wrote", path.relative_to(ROOT))
    pkg.setdefault("contributes", {}) ["themes"] = contributes
    with open(pkg_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render(pkg))
    print("updated package.json themes list")

if __name__ == "__main__":
    main()
