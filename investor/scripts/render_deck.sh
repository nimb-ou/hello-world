#!/usr/bin/env bash
# Render LORE_Pitch_Deck.pptx -> investor/render/slide-NN.png via LibreOffice + pdftoppm.
set -euo pipefail
INV="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$INV/render"
soffice --headless --convert-to pdf --outdir "$INV/render" "$INV/LORE_Pitch_Deck.pptx" >/dev/null
pdftoppm -r 90 -png "$INV/render/LORE_Pitch_Deck.pdf" "$INV/render/slide"
ls "$INV/render"
