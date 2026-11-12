# Changelog

## 2.1.1

This release folds the planned 2.0.1 follow-up and the planned 2.1.0 feature work into one upload. Neither 2.0.1 nor 2.1.0 was ever published. The follow-up had no code changes to ship on its own (see Notes), and the one new feature is additive, so two uploads would have been churn. It is numbered 2.1.1 to mark it as the release that covers both of those plans.

No theme colors changed. The extension itself is unchanged apart from its version, README and CHANGELOG, so the VSIX behaves exactly like 2.0.0.

### Added
- **Windows Terminal color schemes**: `terminals/windows-terminal/claude-sleek.json` holds five schemes (Claude Ember, Claude Ember Black, Claude Parchment, Claude Ember High Contrast, Claude Parchment High Contrast). They use the same ANSI palettes the editor terminal uses, so the contrast already checked for the VS Code themes applies to them.
- `tools/generate_terminals.py`: generates that file from the palettes in `tools/generate_themes.py`, with a `--check` mode. Windows Terminal ignores alpha in schemes, so the translucent selection color is pre-blended over the background.
- A CI and release step that fails if the committed Windows Terminal file differs from the generator output.
- README: a Windows Terminal section and the new development commands.

### Changed
- `.vscodeignore` excludes `terminals/`, so the Windows Terminal files live in the GitHub repository and are not bundled into the VSIX.

### Notes
- The No Italics themes have no Windows Terminal scheme, because they use identical colors and a terminal color scheme has no italics. That is five schemes for eight themes.
- The newer interface keys from 2.0.0 are still unchecked against the editor's own schema validation. This release does not change that.
- Not included on purpose: more language syntax rules and a colorblind-safety check. They need testing in a real editor, and guessing at scope names is how themes get subtly wrong.

## 2.0.0

The biggest release so far: two High Contrast themes, much wider language and interface coverage, and CI that keeps releases honest.

**Nothing was renamed.** All six existing themes keep their names, so any `workbench.colorCustomizations` or `workbench.colorTheme` setting keeps working. Syntax and UI colors are unchanged except where listed under Changed.

### Added
- **Claude Ember High Contrast** and **Claude Parchment High Contrast**: brighter text and syntax (7:1 contrast, up from 4.5:1), brighter terminal colors, and outlined widgets through `contrastBorder` / `contrastActiveBorder`. They contain no italics.
- Syntax colors for more languages: TypeScript primitive types and type operators, Python keyword arguments and string prefixes, Rust attributes and std functions, Go packages, C/C++ preprocessor directives and built-in types, Java/Kotlin imports and generics, PHP, Ruby symbols and instance variables, shell options and positional parameters, TOML and INI sections, SQL table and database names, Dockerfile instructions, XML namespaces, diff file headers, and regular expression quantifiers, anchors and classes.
- Semantic token colors for built-in functions and methods (`function.defaultLibrary`, `method.defaultLibrary`) and for rust-analyzer tokens (lifetimes, attributes, derives, built-in types, `self`, format specifiers).
- Interface coverage for newer VS Code features: source control graph and history, merge editor, inline chat, multi-cursor, light bulbs, Unicode highlights, inlay hint kinds, problems icons, debug console, debug icons and token values, tab selection, toolbars, banners, ports, search editor, comments widget, list filter matches, tree tables, and drop targets.
- `demo/` sample files for TypeScript, Rust, Go, C++, Java, PHP, Ruby, shell, SQL, TOML, INI, XML, Dockerfile and diff.
- `.github/workflows/ci.yml`: runs every check on each push and pull request.
- `.github/workflows/release.yml`: on a `v*` tag, runs every check, builds the VSIX and creates a GitHub release. It publishes to Open VSX and the VS Code Marketplace only if the `OVSX_PAT` / `VSCE_PAT` repository secrets exist.
- `tools/check_keys.py`: every theme must define the same UI keys, semantic tokens and syntax rules.
- `tools/check_release.py`: `package.json`, the newest CHANGELOG entry, the README VSIX filename, `demo/showcase.json` and the README theme list must agree (and the git tag, in the release workflow).

### Changed
- Terminal ANSI black in Ember and Ember Black is now a visible warm gray (`#6d675c`, 3:1). It was about 1.2:1 on Ember and 1.5:1 on Ember Black, so text printed in black was nearly invisible. Parchment is unchanged.
- Built-in functions and methods that a language server marks as such (`print`, `len`, `console.log`) now use the teal built-in color instead of the function color, matching what Python's syntax rules already did.
- `engines.vscode` is now `^1.65.0`, the first version with a High Contrast Light theme type.
- `tools/check_contrast.py` checks ANSI black and the new interface colors, and holds High Contrast themes to 7:1 for text.
- `tools/check_parity.py` skips High Contrast themes and verifies they contain no italics.
- README: High Contrast themes, accent presets, release steps, updated palette and development commands.

### Notes
- The newer interface keys come from the VS Code theme color reference as I know it. VS Code ignores keys it does not recognize, and an editor with JSON schema validation underlines any it does not know.

## 1.1.4

### Fixed
- CHANGELOG: the 1.1.3 entry said `--check` "exists" without regenerating. It should say "exits". The vague "typo" line now says what was fixed.
- `demo/showcase.json` still reported version 1.1.0. It now matches the package version.
- `demo/showcase.css`: the `@import` rule now comes first, as CSS requires. It followed the `:root` block before, so editors could flag it.
- `.gitignore` now ignores `commit-message.txt`, which `.vscodeignore` already excluded from the package.
- README: the accent customization example only applies to Claude Ember. It now explains that each variant needs its own key.

No theme colors changed in this release.

## 1.1.3

### Fixed
- `tools/generate_themes.py --check` no longer crashes on out-of-date files, and now exits without regenerating when everything is current
- The generator wrote the theme list to a misspelled `contrributes` key, leaving a duplicate block in `package.json`. The stray block is removed.
- README: the accent customization example used a misspelled setting name (`colorCutomizations`) and silently did nothing. The VSIX filename is also updated.
- CHANGELOG: corrected "exists" to "exits" in the `--check` entry above.

No theme colors changed in this release.

## 1.1.2

### Fixed
- Ember and Parchment: the matched-text highlight in the suggest list is now readable on the selected row (it was 4.1:1 in Ember and 3.7:1 in Parchment).

### Changed
- The contrast checker now also covers bracket pair colors, chart colors, text on selection, find match, line highlight and diff backgrounds, tab hover, secondary buttons, input validation text, and menu, quick input and suggest selections.
- New `tools/check_parity.py` verifies each No Italics theme differs from its parent only in italics.
- `tools/generate_themes.py --check` verifies the committed theme files and the `package.json` theme list match the generator output.
- README: development commands, accent customization snippet, raised surface palette row.

## 1.1.1

### Fixed
- Parchment: darkened the sidebar git status tints (added, deleted, untracked, conflicting) and list error/warning text, which sat just under 4.5:1 contrast.
- Unused code (such as an unused import) now renders at the same opacity in every theme. It was very faint in Parchment.

### Changed
- The contrast checker now covers git decorations, list errors and warnings, status badges, terminal ANSI colors, symbol and test icons, and text on hover and selection backgrounds.
- The tools write LF line endings on Windows.
- README: the No Italics variants also remove italics from Markdown emphasis and quotes.

## 1.1.0

### Added
- **Claude Ember Black**: the Ember colors on true black, for OLED screens.
- **No Italics variants** of Ember, Ember Black and Parchment.
- Tuned syntax colors for Markdown, JSON, YAML, HTML and CSS/SCSS (headings, code fences, link text and URLs, YAML anchors and list markers, HTML tag brackets and entities, CSS selectors, custom properties, at-rules and values).
- Styling for sticky scroll, symbol icons (outline, breadcrumbs), notebooks, tests, the settings editor, the command center, terminal command markers and the chat panel.
- `demo/` sample files for Markdown, JSON, YAML, HTML and CSS.
- `tools/generate_themes.py` and `tools/check_contrast.py` to rebuild the themes and check contrast.

### Changed
- Updated the README with 1.1.0 screenshots (editor, interface and terminal for Ember, Ember Black and Parchment) and descriptions of every theme.
- Softened the active bracket-pair guide (it was a loud terracotta box in Ember).
- HTML tag brackets are now muted so tag names stand out.

### Fixed
- Parchment: darkened comments, punctuation, keywords, constants, function color and the accent (links, Markdown headings, buttons, badges, status items) so all text clears 4.5:1 contrast on the cream background.
- Both themes: raised dim UI text (inactive tabs, breadcrumbs, placeholders, inlay hints) to at least 4.5:1. Line numbers, inactive activity bar icons and active indent guides use a separate gutter gray (3:1 or better).
- Ember: raised comment contrast from 3.8:1 to 4.6:1, and terminal bright black (dim text) from 3.1:1 to 4.6:1.
- Parchment terminal: darkened ANSI yellow and the bright ANSI colors, and made ANSI white a readable warm gray (it was nearly invisible on cream).

## 1.0.0
- Initial release: Claude Ember (dark) and Claude Parchment (light).
