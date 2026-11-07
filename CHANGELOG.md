# Changelog

## 1.1.2

### Fixed
- Ember and Parchment: the matched-text highlight in the suggest list is now readable on the selected row (it was 4.1:1 in Ember and 3.7:1 in Parchment).

### Changed
- The contrast checker now also covers bracket pair colors, chart colors, text on selection, find match, line highlight and diff backgrounds, tab hover, secondary buttons, input validation text, and menu, quick input and suggest selections.
- New `tools/check_parity.py` verifies each No Italics theme differs from its parent only in italics.
- `tools/generate_themes.py --check` verifies the committed theme files and the `package.json` theme list match the generator output.
- README: development commands, accent customization snippet, raised surface pallette row.

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
