# LORE industrial design (design/industrial/)

ID package for **LORE Pebble (P1) · Square (S1) · Atlas (A1)** and the LORE Kit accessories.
Rev EVT-0 / ID-A3, 2026-10-31. Everything here is generated from **[`params.json`](params.json)**. Edit the params, then re-run the scripts below; never hand-edit generated files.

## Index

| Path | What it is |
|---|---|
| [id-spec.md](id-spec.md) | **The ID specification** for each SKU: dimensions, radii and walls; mass budget per part; control, port, mic and speaker placement; charging, attach points and IP; CMF; ergonomics; drop. Also the packaging fit check and the hardware alignment register |
| [accessories.md](accessories.md) | LORE Kit: spec, material, target price, COGS (E) and GM for each accessory, plus in-box contents |
| [mass-budget.md](mass-budget.md) / `mass-budget.json` | Generated mass budget (estimates). The JSON feeds the render captions and the viewer |
| [params.json](params.json) | Master parameters (mm): the single source of truth |
| [drawings/](drawings/) | `pebble/square/atlas.svg` (+ `.png` previews): A3, 2:1, third-angle general-arrangement drawings with front, top, bottom, left, right and back views, CTF dimensions, numbered callouts and a title block |
| [models/](models/) | `lore-*-*.glb` (metres, PBR, textures embedded) and `.stl` (mm, binary, visual mesh) for the three devices; `export-report.json` holds bounding boxes and triangle counts |
| [viewer.html](viewer.html) | Interactive 3D viewer: orbit the family or one SKU, switch finishes, toggle screen and LED, show the back. Built live from the same geometry as the renders |
| [renders/](renders/) | 19 product renders (heroes, lineup, colourways, exploded, scale, in-hand, in-use, 7 accessories, kit flat-lay) and [`contact-sheet.png`](renders/contact-sheet.png) |
| `render.html` | Shot library for the renders (`?shot=<name>`) |
| `export.html` | GLB/STL exporter (GLTFExporter + STLExporter in headless Chromium) |
| `lib/` | `lore-geometry.js` (parametric three.js geometry), `materials.js` (CMF finishes), `studio.js` (render studio) |
| `scripts/` | `mass_budget.py`, `drawings.py`, `fit_check.py`, `contact_sheet.py`, and the render job files `jobs-*.json` |

## Re-generate

From `design/`. The renders need Playwright's Chromium at `/opt/pw-browsers`, and the Python scripts need `pip install cairosvg pillow`.

```
python3 industrial/scripts/mass_budget.py                        # mass-budget.md/.json, id-spec §7 tables
python3 industrial/scripts/drawings.py                           # drawings/*.svg + .png
python3 industrial/scripts/fit_check.py                          # packaging fit table (id-spec §11)
node tools/render.mjs industrial/scripts/jobs-core.json          # heroes, lineup, colourways, exploded
node tools/render.mjs industrial/scripts/jobs-all.json           # every shot (slow: about 1 min per shot)
node tools/render.mjs industrial/scripts/jobs-accessories.json   # rugged case, buds, power puck, kit family, clip
node tools/render.mjs industrial/scripts/jobs-export.json        # models/*.glb + *.stl
python3 industrial/scripts/contact_sheet.py                      # renders/contact-sheet.png
```

**Viewer.** Run `python3 -m http.server -d design 8000`, then open `http://localhost:8000/industrial/viewer.html`. ES modules do not load from `file://`.

## Status and caveats

- All masses, COGS and battery figures marked **(E)** are estimates. All renders are visualisations of parametric EVT-0 models, not photographs of hardware.
- The 3D models show the SOS pocket and the Mount recess as flush decals, without a boolean cut. **The drawings govern.**
- Open ID↔hardware items, most importantly **H8: the Pebble cell and PCB do not fit the housing**, are listed in id-spec §12.
