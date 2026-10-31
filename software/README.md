# LORE Software

Working code for LORE's Q4 2026 milestone ("Phone-app prototype + Rome pack", see `../COMPANY.md`), plus a Mumbai pack for the founder's first real walk tests in India: the story engine, Map Vision geometry and heading fusion, the Rome City Pack builder, a phone-browser PWA prototype with a simulation mode, the cloud backend, a headless walk simulation, and the device/OS architecture docs.

Everything here runs offline. Cloud features switch to mock mode when no API key or network is available.

## Index

| Path | What it is |
|---|---|
| `packages/core/` | TypeScript core, shared by the PWA, backend, simulation and (later) the device app. |
| `packages/core/src/geo.ts` | Haversine, bearing, relative bearing, ahead/left/right/behind classification and "look up", side of street, path interpolation. |
| `packages/core/src/heading-fusion.ts` | Two-state Kalman filter (heading + compass bias) that fuses compass, GNSS course, step direction and gyro. Rejects magnetic disturbance. Also a complementary filter. |
| `packages/core/src/story-engine.ts` | Chooses what to narrate and when. Handles interest scoring, distance, heading and visibility, novelty (never repeats), the interest profile, cooldowns, quiet moments, 20 s / 40 s / deep tiers, "tell me more" chaining, "what's around me" and live-info merge. |
| `packages/core/src/narration.ts` | Builds the script from fact cards. Includes four personas, the LLM prompt template, an anti-hallucination validator and a deterministic offline template fallback. |
| `packages/core/src/routes.ts` | Demo routes with crossings, talking windows, stops and magnetic-disturbance zones. Rome runs Pantheon to Navona to Campo de' Fiori to Largo Argentina to Trevi. Mumbai runs Gateway of India to Regal Circle to Kala Ghoda to Flora Fountain to Horniman Circle to CSMT. |
| `city-pack/` | Python City Pack builder (stdlib only). It has real fetch code for Overpass and the Wikipedia REST API, and falls back to curated seed data. |
| `city-pack/data/rome_seed.json` | Curated Rome seed: **86 POIs and 215 fact cards**, each with a source URL. |
| `city-pack/data/mumbai_seed.json` | Curated Mumbai seed for the founder's first real walk tests: **62 POIs and 144 fact cards** in the Fort, Kala Ghoda, Colaba and Churchgate heritage area, which covers the UNESCO Victorian Gothic and Art Deco Ensembles (2018) and CSMT (2004), plus a few landmarks further north. |
| `city-pack/output/{rome,mumbai}.pack.json`, `.sqlite` | Built City Packs. Rome is the commercial launch pack; Mumbai is the field-test pack. |
| `apps/prototype/` | Vite PWA: Geolocation, DeviceOrientation, the story engine and Web Speech TTS, plus simulation mode and a city switcher (Rome / Mumbai). |
| `apps/prototype/screenshots/` | Playwright screenshots of simulation mode (phone viewport). Rome: `01`–`08`, light and dark. Mumbai: `mumbai-01`–`03`. |
| `backend/` | Node/TypeScript HTTP API with `/narrate` (Claude tool calling, guarded to fact cards, mock without a key), `/nearby`, `/search`, `/hotels` and `/safety`. |
| `simulations/walk-sim.ts` | Headless walk with simulated sensors. Outputs a transcript and metrics. |
| `simulations/output/{rome,mumbai}-walk-transcript.md`, `-metrics.json` | Latest transcripts and metrics (simulated). |
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
npm run pack:build              # build the Rome + Mumbai packs (seed; add --online in city-pack to enrich from OSM/Wikipedia)
npm run app:dev                 # http://localhost:5173/?sim=1             (Rome simulation starts automatically)
                                # http://localhost:5173/?city=mumbai&sim=1 (Mumbai simulation)
# On a phone on the same Wi-Fi, open http://<laptop-ip>:5173 and tap "Use my location" (needs HTTPS for
# DeviceOrientation on iOS; use `npm run app:build && npx vite preview` behind an HTTPS tunnel).
```

URL parameters: `city=rome|mumbai` picks the City Pack (the header has a switcher too). `sim=1` starts the simulated walk. `speed=1|5|10|30` sets the simulation speed; at 1x the app speaks through speechSynthesis. `mute=1` silences speech. `persona=historian|storyteller|minimalist|local-friend` picks the voice. `backend=http://localhost:8787` sets the backend URL used by the "Cloud narration" toggle.

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
npm run sim                     # Rome + Mumbai: simulations/output/{city}-walk-transcript.md + metrics json
npx tsx simulations/walk-sim.ts --city mumbai --seed 7 --persona historian
npm run app:build && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers npm run app:screenshots          # both cities
node apps/prototype/scripts/screenshots.mjs mumbai                                              # Mumbai only
```

## Tests

```bash
npm run typecheck               # tsc --noEmit over all TS
npm test                        # vitest: core (geo, fusion, engine, narration), backend, simulation
npm run pack:test               # pytest: seed validation, builder, OSM/Wikipedia parsing (mocked network), SQLite
npm run test:all                # all of the above + the simulation
```

Current status: 66 vitest tests and 21 pytest tests, all passing.

## City packs

| Pack | Status | POIs / facts | Simulated walk (seed 42) |
|---|---|---|---|
| **Rome** | Commercial launch pack (v1) | 86 / 215 | 1.93 km: 17 stories (8.8/km), 0 % repeats, 100 % quiet-moment compliance, 100 % direction accuracy |
| **Mumbai** | Founder's first real walk tests (India) | 62 / 144 | 2.32 km: 16 stories (6.9/km), 0 % repeats, 100 % quiet-moment compliance, 93.8 % direction accuracy, heading error mean 2.8° / p95 5.4° |
| **Hampi** (planned next) | Offline-mode stress test | – | – |

**Mumbai field-test checklist:**
- The seed coordinates come from memory and are approximate (about 30–60 m). On the first walk, log GNSS against each POI and correct the seed before trusting left/right calls.
- Run `python -m lore_citypack verify --seed data/mumbai_seed.json` with network access, then do an editorial review.
- Watch heading quality near CSMT and D. N. Road. Buses, trains and steel structures are likely to disturb the compass, so the simulation models a disturbance zone there.

**Hampi (next pack).** The Group of Monuments at Hampi is a large UNESCO World Heritage Site (https://whc.unesco.org/en/list/241) with weak or no mobile signal across much of the site. It is planned as the stress test for offline mode:
- packs, routing, on-device ASR/LLM/TTS and walk-me-home all have to work with no network;
- POIs are spread out, so long walks and bike rides will test GNSS-only heading and the battery;
- the pack has to be downloaded fully before arrival, and so does the queued sync of engine state and safety check-ins.

Success criteria: a full day on site with zero cloud calls, no degraded stories, and walk-me-home SMS escalation using the device's own LTE/SMS path when there is any signal.

## Honesty notes
- **Seed facts** are curated from well-established knowledge, and each one cites its Wikipedia article. They are marked `review_status: "curated"`. The sandbox could not reach Wikipedia, so `python -m lore_citypack verify` still has to be run with network access, followed by an editorial review, before customers see them. Auto-extracted facts are held back unless `--include-unreviewed` is set.
- **Simulation output** comes from synthetic sensors and is labelled as simulated.
- **Mock adapters** (search, hotels, notifier) return data labelled `[MOCK]` or `[SIMULATED]`.
- The web fonts (Fraunces, Inter) load from Google Fonts. The screenshots used fallback fonts because the sandbox blocks that host.
