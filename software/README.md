# LORE Software

Working code for LORE's Q4 2026 milestone ("Phone-app prototype + Rome pack", see `../COMPANY.md`): the story engine, Map Vision geometry and heading fusion, the Rome City Pack builder, a phone-browser PWA prototype with a simulation mode, the cloud backend, a headless walk simulation, and the device/OS architecture docs.

Everything here runs offline. Cloud features switch to mock mode when no API key or network is available.

## Index

| Path | What it is |
|---|---|
| `packages/core/` | TypeScript core, shared by the PWA, backend, simulation and (later) the device app. |
| `packages/core/src/geo.ts` | Haversine, bearing, relative bearing, ahead/left/right/behind classification and "look up", side of street, path interpolation. |
| `packages/core/src/heading-fusion.ts` | Two-state Kalman filter (heading + compass bias) that fuses compass, GNSS course, step direction and gyro. Rejects magnetic disturbance. Also a complementary filter. |
| `packages/core/src/story-engine.ts` | Chooses what to narrate and when. Handles interest scoring, distance, heading and visibility, novelty (never repeats), the interest profile, cooldowns, quiet moments, 20 s / 40 s / deep tiers, "tell me more" chaining, "what's around me" and live-info merge. |
| `packages/core/src/narration.ts` | Builds the script from fact cards. Includes four personas, the LLM prompt template, an anti-hallucination validator and a deterministic offline template fallback. |
| `packages/core/src/routes.ts` | Demo route (Pantheon to Navona to Campo de' Fiori to Largo Argentina to Trevi) with crossings, talking windows and stops. |
| `city-pack/` | Python City Pack builder (stdlib only). It has real fetch code for Overpass and the Wikipedia REST API, and falls back to curated seed data. |
| `city-pack/data/rome_seed.json` | Curated Rome seed: **86 POIs and 215 fact cards**, each with a source URL. |
| `city-pack/output/rome.pack.json`, `rome.pack.sqlite` | Built Rome City Pack. |
| `apps/prototype/` | Vite PWA: Geolocation, DeviceOrientation, the story engine and Web Speech TTS, plus simulation mode. |
| `apps/prototype/screenshots/` | Playwright screenshots of simulation mode (phone viewport, light and dark). |
| `backend/` | Node/TypeScript HTTP API with `/narrate` (Claude tool calling, guarded to fact cards, mock without a key), `/nearby`, `/search`, `/hotels` and `/safety`. |
| `simulations/walk-sim.ts` | Headless walk with simulated sensors. Outputs a transcript and metrics. |
| `simulations/output/rome-walk-transcript.md` | Latest transcript and metrics (simulated). |
| `docs/architecture.md` | Full system architecture, model strategy, cloud, privacy, OTA, observability and cost per user. |
| `docs/device-software.md` | Device firmware/OS plan, power states, wake word, packaging, OTA, security and the BLE GATT spec. |
| `docs/roadmap.md` | Engineering roadmap and software hiring plan. |

## Architecture in one picture

```
 sensors (GNSS L1+L5, IMU, mag) ──► heading-fusion (Kalman) ─┐
                                                             ├─► StoryEngine.update() ──► Decision
 City Pack (SQLite: POIs, fact cards, sources) ──────────────┘        │ (poi, facts, tier, left/right, look up)
 safety context (crossing, VAD "user talking", speed) ───────────────┘
                                                                      ▼
                         narration.ts: on-device LLM or cloud Claude (prompt allows ONLY these facts)
                                       └─► validateNarration() guard ── fail ─► deterministic template
                                                                      ▼
                                                    TTS ─► earphones (LE Audio / A2DP)
```

## Setup

Requirements: Node 20+ (tested on 22) and Python 3.10+ (tested on 3.11).

```bash
cd software
npm install                     # TypeScript, vitest, vite, tsx, playwright, @anthropic-ai/sdk
pip install pytest              # only for the city-pack tests
```

## Run the demo

```bash
npm run pack:build              # build the Rome pack (seed; add --online in city-pack to enrich from OSM/Wikipedia)
npm run app:dev                 # http://localhost:5173/?sim=1   (simulation mode starts automatically)
# On a phone on the same Wi-Fi, open http://<laptop-ip>:5173 and tap "Use my location" (needs HTTPS for
# DeviceOrientation on iOS; use `npm run app:build && npx vite preview` behind an HTTPS tunnel).
```

URL parameters: `sim=1` starts the simulated walk. `speed=1|5|10|30` sets the simulation speed; at 1x the app speaks through speechSynthesis. `mute=1` silences speech. `persona=historian|storyteller|minimalist|local-friend` picks the voice. `backend=http://localhost:8787` sets the backend URL used by the "Cloud narration" toggle.

Backend:

```bash
npm run backend                 # :8787, mock mode
ANTHROPIC_API_KEY=... npm run backend   # live /narrate with claude-sonnet-5-5 (override: LORE_MODEL)
curl -s localhost:8787/nearby?lat=41.8986\&lng=12.4769\&radius=150
curl -s -XPOST localhost:8787/narrate -H 'content-type: application/json' \
  -d '{"poi_id":"rome-pantheon","persona":"storyteller","direction":"right"}'
```

Simulation and screenshots:

```bash
npm run sim                     # writes simulations/output/rome-walk-transcript.md + metrics json
npm run app:build && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers npm run app:screenshots
```

## Tests

```bash
npm run typecheck               # tsc --noEmit over all TS
npm test                        # vitest: core (geo, fusion, engine, narration), backend, simulation
npm run pack:test               # pytest: seed validation, builder, OSM/Wikipedia parsing (mocked network), SQLite
npm run test:all                # all of the above + the simulation
```

Current status: 61 vitest tests and 16 pytest tests, all passing.

## Honesty notes
- **Seed facts** are curated from well-established knowledge, and each one cites its Wikipedia article. They are marked `review_status: "curated"`. The sandbox could not reach Wikipedia, so `python -m lore_citypack verify` still has to be run with network access, followed by an editorial review, before customers see them. Auto-extracted facts are held back unless `--include-unreviewed` is set.
- **Simulation output** comes from synthetic sensors and is labelled as simulated.
- **Mock adapters** (search, hotels, notifier) return data labelled `[MOCK]` or `[SIMULATED]`.
- The web fonts (Fraunces, Inter) load from Google Fonts. The screenshots used fallback fonts because the sandbox blocks that host.
