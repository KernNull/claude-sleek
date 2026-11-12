#!/usr/bin/env bash
# Build and publish helper, used to show off shell colors.
set -euo pipefail

VERSION="${1:-2.0.0}"
OUT_DIR="$(dirname "$0")/../dist"

log() { printf '[%s] %s\n' "$(date +%T)" "$*"; }

if [[ ! -d "$OUT_DIR" ]]; then
  mkdir -p "$OUT_DIR"
fi

for check in generate_themes check_contrast check_parity; do
  log "running $check"
  python "tools/${check}.py" || { log "failed: $check"; exit 1; }
done

npx --yes @vscode/vsce package --out "$OUT_DIR/claude-sleek-${VERSION}.vsix"
ls -l "$OUT_DIR" | grep -c vsix
