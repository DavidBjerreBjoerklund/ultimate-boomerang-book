#!/usr/bin/env bash
set -euo pipefail

pdf_to_ppm="${PDFTOPPM:-}"
if [ -z "$pdf_to_ppm" ]; then
  if command -v pdftoppm >/dev/null 2>&1; then
    pdf_to_ppm="$(command -v pdftoppm)"
  elif [ -x "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/pdftoppm" ]; then
    pdf_to_ppm="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/pdftoppm"
  else
    echo "pdftoppm not found. Install poppler or set PDFTOPPM=/path/to/pdftoppm." >&2
    exit 1
  fi
fi

dpi="${EPUB_IMAGE_DPI:-144}"

find Pictures -name '*-eps-converted-to.pdf' -print0 | while IFS= read -r -d '' pdf; do
  base="${pdf%-eps-converted-to.pdf}"
  png="${base}.png"
  if [ ! -f "$png" ] || [ "$pdf" -nt "$png" ]; then
    "$pdf_to_ppm" -singlefile -png -r "$dpi" "$pdf" "$base"
  fi
done
