# Changelog

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
