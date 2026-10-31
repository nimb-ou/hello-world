# brand/: LORE brand identity

Owner: Brand Director, LORE Labs · v1.0 · 2026-10-31 · COMPANY.md wins on any conflict.

**Start here:** [`brand-board.png`](brand-board.png) (one-page overview) → [`brand-guidelines.md`](brand-guidelines.md)

## Documents
| File | What it is |
|---|---|
| [brand-guidelines.md](brand-guidelines.md) | Complete brand book: story, mission, values, positioning, pillars, personality, naming system, logo rules, clear space and minimum sizes, colour (HEX/RGB/CMYK/Pantone candidates), type scale, iconography, photography, illustration, motion, sound identity (sonic logo and earcons), merch, do/don't |
| [voice-and-tone.md](voice-and-tone.md) | Writing guide, five narrator Voices with sourced Rome scripts, device-state microcopy table |
| [packaging.md](packaging.md) | Per-SKU structures, dimensions, FSC materials (no plastic), finishes, inserts, opening sequence, inside-lid message, open checks |
| [naming-trademark.md](naming-trademark.md) | Why "LORE", alternates, class 9/38/39/42 (+41/45) risk notes, domains and handles to check (all UNVERIFIED) |
| [brand-board.html](brand-board.html) → [brand-board.png](brand-board.png) | One-page moodboard (1920 px wide) |

## Assets for reuse (Design / GTM)
| Need | Path |
|---|---|
| Primary logo (horizontal, Ink + Terracotta) | `logo/svg/lore-lockup-horizontal-ink.svg` |
| Reverse logo (on dark) | `logo/svg/lore-lockup-horizontal-bone.svg` |
| Mono logo | `logo/svg/lore-lockup-horizontal-ink-mono.svg`, `…-terracotta.svg` |
| Stacked (± tagline) | `logo/svg/lore-lockup-stacked-*.svg`, `logo/svg/lore-lockup-stacked-tagline-*.svg` |
| Wordmark only | `logo/svg/lore-wordmark-{ink,bone,terracotta}.svg` |
| Symbol, "The Keyhole" | `logo/svg/lore-symbol-{ink,bone,terracotta}.svg`; positive glyph `logo/svg/lore-keyhole-glyph-*.svg` |
| App icon | `logo/svg/lore-app-icon-1024.svg`, `logo/png/lore-app-icon-1024.png` (+ `-dark`, `-tinted-mask`, `app-icon-{180,120,87,58}.png`) |
| Favicon | `logo/favicon.svg`, `logo/favicon.ico`, `logo/png/favicon-{16,32,48,180,192,512}.png` |
| PNG renders | `logo/png/*` (transparent, 1600 px wide lockups / 512 px symbols) |
| Logo sheets | `logo/concepts.svg` (3 routes, Keyhole selected), `logo/construction.svg`, `logo/clearspace.svg`, `logo/misuse.svg`, `logo/logo-overview.svg` (+ PNGs in `logo/png/`) |
| Colour tokens | `palette/tokens.json`, `palette/lore-colors.css`, `palette/palette.csv` |
| Swatch sheets | `palette/palette.svg/.png`, `palette/contrast-matrix.svg/.png` |
| Fonts (OFL, WOFF2) + CSS | `typography/fonts/`, `typography/lore-fonts.css` |
| Type specimen | `typography/specimen.html/.png` |
| Dielines (1:1 mm) | `packaging/dieline-{pebble,square,atlas}.svg` (+ `packaging/png/`) |
| Box art | `packaging/box-art.svg`, `packaging/png/box-art.png` |
| Stationery | `stationery/business-card-{front,back}.svg`, `stationery/letterhead-a4.svg`, `stationery/envelope-dl.svg`, `stationery/stationery-mockup.svg` |
| Merch concepts | `stationery/merch-concepts.svg` (+ `stationery/png/`) |

## Rebuild
All SVG logos are pure outlines (no live fonts). The wordmark is outlined from Fraunces (OFL) by script.
```bash
cd brand/scripts
pip install fonttools brotli pillow
npm install            # playwright-core + @fontsource-variable fonts (node_modules is git-ignored)
./build_all.sh         # regenerates logo/, palette/, packaging/, stationery/, specimen + brand-board PNGs
```
Rendering uses headless Chromium at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` (override with `CHROME=`).

| Script | Output |
|---|---|
| `scripts/glyphs.py` | Font → SVG outline helper (fontTools, applies Fraunces rvrn/WONK substitutions) |
| `scripts/tokens.py` | Colour constants, CMYK conversion, WCAG contrast |
| `scripts/build_logos.py` / `render_logos.py` | Every logo SVG / PNG, favicon.ico |
| `scripts/build_palette.py` | Swatch and contrast sheets, tokens |
| `scripts/build_packaging.py` | Dielines and box art |
| `scripts/build_stationery.py` | Cards, letterhead, envelope, mockup, merch |
| `scripts/render.js` | SVG/HTML → PNG (Playwright) |

## Status and caveats
- Pantone references are **nearest candidates, unverified**. CMYK values are naive conversions, so confirm them with the printer's ICC profile.
- Packaging dimensions and papers are **estimates and candidates** pending EVT units and supplier samples.
- Trademark, domain and handle availability is **unverified**. Legal-ops must clear it.
- Brand-board photo tiles are art-direction placeholders, not photography. The Pebble sleeve street pattern is illustrative, not map data.
- Rome story facts are sourced in `voice-and-tone.md` §4.1. The Colosseum clamp detail is flagged for primary-source re-check.
