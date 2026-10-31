#!/usr/bin/env bash
# Rebuild every generated brand asset. Requires: python3 + fonttools brotli pillow; node + `npm i` in this folder.
set -e
cd "$(dirname "$0")"
python3 build_logos.py >/dev/null
python3 render_logos.py >/dev/null
python3 build_palette.py >/dev/null
python3 build_packaging.py >/dev/null
python3 build_stationery.py >/dev/null
r() { node render.js "$@" >/dev/null; }
r ../palette/palette.svg ../palette/palette.png
r ../palette/contrast-matrix.svg ../palette/contrast-matrix.png
r ../typography/specimen.html ../typography/specimen.png 1600
mkdir -p ../packaging/png ../stationery/png
for n in dieline-pebble dieline-square dieline-atlas; do r ../packaging/$n.svg ../packaging/png/$n.png 2400 --opaque; done
r ../packaging/box-art.svg ../packaging/png/box-art.png 2560 --opaque
r ../stationery/stationery-mockup.svg ../stationery/png/stationery-mockup.png --opaque
r ../stationery/merch-concepts.svg ../stationery/png/merch-concepts.png --opaque
r ../stationery/business-card-front.svg ../stationery/png/business-card-front.png 1236 --opaque
r ../stationery/business-card-back.svg ../stationery/png/business-card-back.png 1236 --opaque
r ../stationery/letterhead-a4.svg ../stationery/png/letterhead-a4.png 1240 --opaque
r ../brand-board.html ../brand-board.png 1920 --scale=1 || echo "brand board not built yet"
echo "done"
