# LORE — Company Bible (single source of truth)

> Every team reads this first. If something here conflicts with your work, this file wins.
> Change it only through the founder (main session).

## One line
**LORE is a pocket-sized AI travel companion that tells you the stories of the city around you through your own earphones.** It gives you history, hidden facts, live info, directions, places to eat and stay, and safety for solo travellers. It works online and offline.

## Mission
Make every walk in a new city feel like walking with a brilliant local friend who knows its history.

## Who it's for
1. **Primary:** solo travellers aged 22–45 who make 2+ international trips a year: curious, design-conscious, and wary of roaming bills and phone theft.
2. **Secondary:** culture-loving retirees and slow travellers, business travellers with spare evenings, and study-abroad students.
3. **Later:** blind and low-vision walkers (accessibility version), tour operators and hostels (fleet/B2B rental).

## Why a device, not just an app (our "why buy")
1. **Built-in global eSIM data**: works in 150+ countries with no roaming bill (Square and Atlas models).
2. **Offline City Packs**: maps, routing, stories and on-device AI with no signal.
3. **2–3 day battery** that leaves the phone's battery for photos, tickets and payments.
4. **Phone stays in your pocket**: eyes up, safer, more present.
5. **Safety**: SOS button, live location sharing, timed "walk me home" check-ins.
6. **Physical controls**: press to talk, double-press for "what's around me", long-press for SOS.
7. Uses **your own earphones** (Bluetooth LE Audio / Classic A2DP) and has a small speaker as fallback.

## Core experience: "Map Vision"
LORE "sees" without a camera by fusing:
- multi-band GNSS (L1+L5)
- a 9-axis IMU and compass
- step and walking-direction detection
- map geometry (building footprints, street sides, entrances)
- places and live data

From that it says **left / right / ahead / behind / look up**, e.g. *"The building on your right was a plague hospital in 1665 — look up at the bricked-up third-floor windows."*

The story engine uses only **checked facts with sources** (no invented history). Each story is 20–40 seconds, and "tell me more" goes deeper. It stays quiet while you cross roads or talk to someone.

## Product line (working names; prices are targets, validated by Research and Finance)
| | **LORE Pebble** | **LORE Square** | **LORE Atlas** |
|---|---|---|---|
| Form | Clip-on rounded pebble, about 42×42×14 mm, no screen, 1 LED ring | Rounded square, about 54×54×12 mm, 1.6" round-corner AMOLED, crown/button | Same footprint as Square in titanium + sapphire, 1.6" AMOLED, wide-angle "Glance" camera |
| Connectivity | BLE to phone + Wi-Fi; offline packs ("Lite" design: AI runs on the phone and in the cloud, offline pre-generated stories; see D10) | LTE Cat-1bis global eSIM + Wi-Fi + BT 5.4 LE Audio | LTE + eSIM + satellite SOS (NTN) |
| AI | Cloud AI + small on-device model (~1B) | On-device 3B model + cloud | On-device 3–4B model + vision + cloud |
| Battery | 1.5 days | 2 days | 2+ days (13.5 mm body) |
| Target price | **$149** | **$299** | **$599** (raised from $549 per research/pricing-research.md) |

**Subscription "LORE Pass":**
- **Explorer** $9.99/mo: unlimited live AI, 1 GB/mo of data, all City Packs, safety features
- **Trip Pass** $29 for 14 days, including 5 GB of data (also $49 for 30 days with 10 GB; Explorer annual plan $79)
- **Free tier**: offline packs for 3 cities plus basic narration

Every device comes with 3 months of Explorer.

**Accessories line ("LORE Kit"):**
- Clip
- Leather lanyard
- Wrist strap
- Magnetic charging dock
- Rugged case
- LORE Buds (open-ear bone-conduction headphones)
- Travel power puck
- Themed city bundles

**Revenue:** hardware, subscriptions, accessories, and booking affiliate fees (hotels, tours, restaurants), plus B2B fleet rental for hostels and tour operators.

## Brand basics (Brand team will expand; others must use these)
- **Name:** LORE (always all caps in the logo; "Lore" is fine in running text). Domain idea: lore.travel. Tagline: **"Every street has a story."** Alternatives: "Hear the city." / "Look up."
- **Personality:** a knowledgeable local friend. Warm, witty, curious, calm. Never a tour-bus megaphone.
- **Look:** quiet luxury plus warm travel. Think Leica, Teenage Engineering, Aesop and Monocle together.

**Palette:**

| Name | Hex | Notes |
|---|---|---|
| Ink | `#14161A` | |
| Bone | `#F3EEE6` | |
| Terracotta | `#C4623A` | Primary accent |
| Brass | `#B8935A` | |
| Olive | `#5E6B4E` | |
| Fog | `#9AA0A6` | |
| Night | `#0D1B2A` | |

**Fonts** (free and open):
- Display: "Fraunces" (serif, editorial)
- UI/body: "Inter"
- Mono/data: "JetBrains Mono"

**Device finishes (CMF):**
- **Pebble:** Bone, Ink, Terracotta (soft-touch PC + glass-fibre)
- **Square:** Ink anodised aluminium, Sand anodised aluminium
- **Atlas:** Bead-blasted titanium, black DLC titanium; sapphire glass; brass-tone crown accent

## Launch plan basics
- **Launch city / City Pack v1: Rome** (dense history, high tourism, great data). Next: Lisbon, Paris, London, Barcelona, Istanbul, Kyoto, New York.
- **Company:** LORE Labs, Inc. (Delaware C-corp, planned). The founder is Nimit Jain.
- **Timeline:**

  | When | Milestone |
  |---|---|
  | Q4 2026 | Phone-app prototype + Rome pack |
  | Q1 2027 | 50 EVT units, beta |
  | Q2 2027 | Kickstarter |
  | Q4 2027 | First 5k units shipped |
  | 2028 | Retail + 20 cities |

- **Fundraising:** pre-seed $1.75M now (a SAFE, $12M post-money valuation cap; see D14). Seed $6M after Kickstarter.

## Repo layout (each team owns ONLY its folder)
```
COMPANY.md            ← this file (founder only)
company/              ← Founder office: handbook, org chart, OKRs, operating plan, decisions log, HQ dashboard
research/             ← Market research, competitors, pricing, TAM/SAM/SOM, personas, survey
brand/                ← Brand identity: logo SVGs, guidelines, voice, palette, typography, packaging
design/               ← Industrial design (3D models, renders, CMF, drawings) and UX/UI (device UI, app screens)
hardware/             ← Electronics: architecture, component selection, BOM+costing, schematics, power/RF/thermal simulations, certification, DFM
software/             ← Working code: prototype app (PWA), story engine, Map Vision, city-pack builder, backend, device OS architecture, tests, simulations
finance/              ← Financial model (xlsx), unit economics, cap table, fundraising, budget
gtm/                  ← Sales, marketing, social media, Kickstarter, PR, partnerships, community
legal-ops/            ← Legal, admin, IP, privacy, compliance, supply chain, manufacturing ops, support, HR/hiring
investor/             ← Pitch deck, one-pager, exec summary, data room index
```

## Rules for every team
- Write **real, specific, serious** work: numbers, part numbers, sources, assumptions stated. Mark estimates as estimates. Never invent quotes, customers, or fake "real" data. Simulated data must be labelled simulated.
- Cite web sources (URLs) for market facts.
- Use Markdown for docs. Generate files (PNG/SVG/XLSX/PPTX/CSV) with scripts kept in your folder so they can be re-run.
- Start your folder with a `README.md` index of everything in it.
- Do **not** run git commit/push; the founder does that.
- Network: the general web search tool works. Direct HTTP to Wikipedia/OSM is blocked. pip and npm installs work. Headless Chromium is at `/opt/pw-browsers` (use Playwright for rendering screenshots).
