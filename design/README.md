# LORE design

Everything the Design team makes for LORE Pebble (P1), Square (S1) and Atlas (A1): industrial design, the device UI and the companion app. Rev **EVT-0**, 2026-10-31.

Brand inputs (logo, palette, type) live in [`../brand/`](../brand/). The design copies used by the pages here are in [`assets/`](assets/):
- `assets/brand/`: logo SVGs
- `assets/fonts/` and `assets/fonts.css`: Fraunces, Inter and JetBrains Mono, OFL
- `assets/vendor/three/`: Three.js for the 3D pages

## Start here (to see the work)

| What | File |
|---|---|
| Device screens, all 15 | [`ux/device-screens/contact-sheet.png`](ux/device-screens/contact-sheet.png) |
| Device screens in the product | [`ux/device-screens/on-device-mockup.png`](ux/device-screens/on-device-mockup.png) |
| Companion app, all 12 | [`ux/app-screens/contact-sheet.png`](ux/app-screens/contact-sheet.png) |
| Companion app in phones | [`ux/app-screens/phone-mockup.png`](ux/app-screens/phone-mockup.png) |
| Product line hero | [`industrial/renders/lineup.png`](industrial/renders/lineup.png) |

---

## Industrial design: `industrial/`

The other designer owns this folder and is still producing some of it. Paths marked *(expected)* may not exist yet.

| Area | Path | Notes |
|---|---|---|
| ID spec | [`industrial/id-spec.md`](industrial/id-spec.md) | Dimensions, controls, CMF, sealing, drop design |
| Master parameters | [`industrial/params.json`](industrial/params.json) | Single source of truth for models, drawings and mass budget |
| Mass budget | [`industrial/mass-budget.md`](industrial/mass-budget.md), `mass-budget.json` | Built by `scripts/mass_budget.py` |
| Accessories spec | [`industrial/accessories.md`](industrial/accessories.md) | Clip, lanyard, wrist strap, dock, rugged case, buds, power puck |
| Accessory drawings | `industrial/accessories/` *(expected)* | |
| Renders | `industrial/renders/*.png` | Full list in `scripts/jobs-all.json`, by group below |
| Drawings | `industrial/drawings/{pebble,square,atlas}.{svg,png}` | Dimensioned orthographic drawings |
| 3D models | `industrial/models/lore-{pebble-p1-bone,square-s1-ink,atlas-a1-titanium}.{glb,stl}` | Plus `export-report.json` |
| Viewer | `industrial/viewer.html` *(expected)* | Interactive 3D viewer for `models/*.glb` |
| Render / export pages | `industrial/render.html`, `industrial/export.html` | Code: `lib/lore-geometry.js`, `lib/materials.js`, `lib/studio.js` |

Render groups:

| Group | Files |
|---|---|
| Hero | `hero-pebble`, `hero-square`, `hero-square-upright`, `hero-atlas` |
| Range | `lineup`, `colourways`, `scale-reference` |
| In use | `in-hand-pebble`, `in-hand-square`, `on-lanyard`, `on-clip` |
| Accessories | `acc-clip`, `acc-lanyard`, `acc-wrist-strap`, `acc-dock`, `acc-rugged-case`, `acc-buds`, `acc-power-puck`, `acc-family` (currently saved as `acc-kit-family.png`) |
| Engineering | `ortho-{pebble,square,atlas}`, `exploded-{pebble,square,atlas}` |
| Finishes | `finish-pebble-{bone,ink,terracotta}`, `finish-square-sq-{ink,sand}`, `finish-atlas-at-{ti,dlc}` |

## UX / UI: `ux/`

| Area | Path | Notes |
|---|---|---|
| UX spec | [`ux/ux-spec.md`](ux/ux-spec.md) | Covers input grammar, voice, story format, earcons, LED states, SOS, Walk Me Home, screen inventory (§8, §9), offline and battery |
| User journeys | [`ux/user-journeys.md`](ux/user-journeys.md) | Maya in Rome. Refers to device screens as D-NN and app screens as A-NN |
| Device screens source | [`ux/device-screens/screens.html`](ux/device-screens/screens.html) | One file holds all screens, the drawn device frame, the contact sheet and the mockup |
| Device screens (PNG) | `ux/device-screens/png/NN-*.png` | 466 × 466 px, 1.6" round-corner AMOLED (Square and Atlas) |
| Device contact sheet | `ux/device-screens/contact-sheet.png` | Labelled 5 × 3 grid |
| Device mockup | `ux/device-screens/on-device-mockup.png` | 4 key screens in the drawn Ink Square (true 54 mm proportions, crown + Terracotta Talk key) on Bone |
| App screens source | [`ux/app-screens/screens.html`](ux/app-screens/screens.html) | One file holds all screens, the contact sheet and the phone mockup |
| App screens (PNG) | `ux/app-screens/png/NN-*.png` | 390 × 844 pt, rendered @2x (780 × 1688) |
| App contact sheet | `ux/app-screens/contact-sheet.png` | Labelled 6 × 2 grid |
| App mockup | `ux/app-screens/phone-mockup.png` | Screens 05, 06 and 07 in phone frames on Bone |
| Render scripts | `ux/scripts/render-device-screens.mjs`, `ux/scripts/render-app-screens.mjs` | |

**Device screens (D-NN):**

| # | Screen | # | Screen | # | Screen |
|---|---|---|---|---|---|
| 01 | home-compass | 06 | answer | 11 | city-pack-download |
| 02 | now-narrating | 07 | dinner | 12 | battery-low-power |
| 03 | nearby | 08 | sos-countdown | 13 | settings-narrator-persona |
| 04 | navigation | 09 | sos-live | 14 | offline-mode |
| 05 | listening | 10 | walk-me-home | 15 | nightstand |

**App screens (A-NN):**

| # | Screen | # | Screen | # | Screen |
|---|---|---|---|---|---|
| 01 | welcome | 05 | rome-pack-detail | 09 | lore-pass |
| 02 | pair | 06 | live-walk-map | 10 | device-settings |
| 03 | interests-persona | 07 | day-recap | 11 | story-detail |
| 04 | city-pack-store | 08 | safety | 12 | dinner-booking |

The app uses Bone (light) for most screens, Ink for the brand moment and evening, and Night for safety. Terracotta appears once per screen, usually as the primary action. The map in A-06 is a stylised vector drawing of Rome's Centro Storico, not real map tiles. Restaurant names in D-07 and A-12 are illustrative.

---

## How to re-render

All rendering goes through one harness, [`tools/render.mjs`](tools/render.mjs). It serves `design/` over HTTP and drives headless Chromium through Playwright, which is installed in `design/node_modules`. Run these from `design/`:

```bash
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers

# UX: device screens: 15 PNGs, contact sheet and on-device mockup (~10 s)
node ux/scripts/render-device-screens.mjs            # optional filter, e.g. "mockup" or "10-walk"

# UX: companion app: 12 PNGs @2x, contact sheet and phone mockup (~15 s)
node ux/scripts/render-app-screens.mjs               # optional filter, e.g. "06-live"

# Industrial: WebGL renders (slow, minutes per shot; uses SwiftShader)
node tools/render.mjs industrial/scripts/jobs-all.json            # or jobs-core.json / jobs-fix.json
node tools/render.mjs industrial/scripts/jobs-all.json hero-square   # filter by output name
python3 industrial/scripts/mass_budget.py                         # mass-budget.md / .json from params.json
```

You can also open any screen in a browser while working on it. Serve `design/` first, for example with `python3 -m http.server` run from `design/`. Then open:
- `ux/device-screens/screens.html?s=10-walk-me-home`
- `ux/device-screens/screens.html?frame=1&s=02-now-narrating` (the screen inside the device)
- `ux/device-screens/screens.html?view=mockup`
- `ux/app-screens/screens.html?s=06-live-walk-map`
- `ux/app-screens/screens.html?view=mockup`

With no query string, each file shows its contact sheet.

**Editing rules:**
- Screen IDs are the keys of the `S` object in each `screens.html`. If you add or rename a screen, add it to the `ids` list in the matching render script as well, and update the tables in `ux/ux-spec.md` §8/§9.
- Device screens are 466 px square with 92 px corners, on pure black. Terracotta marks the single active element, Brass is used for navigation and Walk Me Home, and Signal red is for SOS only.
