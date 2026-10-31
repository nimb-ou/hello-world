# Software Roadmap and Hiring Plan (v0.1)

Aligned with the timeline in `COMPANY.md`. Dates are targets; headcount is contingent on funding (pre-seed $1.5M now, seed $6M after Kickstarter).

## Roadmap

| Quarter | Milestone | Software deliverables | Exit criteria |
|---|---|---|---|
| **Q4 2026** | Phone-app prototype + Rome pack | **Done in this repo:** core engine (geo, heading fusion, story engine, narration + guard), Rome seed (86 POIs, 215 facts), pack builder (JSON + SQLite, OSM/Wikipedia fetchers), PWA with simulation mode, backend (`/narrate` Claude + mock, `/nearby`, `/search`, `/hotels`, `/safety`), walk simulation. **Remaining:** run `verify` online plus editorial review of all 215 facts; 10 real walks in Rome with the PWA; field-measure heading accuracy | 100% of facts reviewed; real-walk direction accuracy ≥85%; 0 quiet-moment violations |
| **Q4 2026 (field)** | Mumbai real-walk tests | Mumbai pack (62 POIs, 144 facts) and simulated Gateway-to-CSMT route are built. Founder walks it with the PWA, logs GNSS/heading, and coordinates and facts are corrected | Field-corrected Mumbai coordinates; direction accuracy ≥85% on real walks |
| **Q1 2027 (pack)** | Hampi offline stress-test pack | Pack for the Hampi UNESCO site (weak or no signal) with an offline-only test protocol: zero cloud calls, on-device voice, pre-downloaded routing, queued sync | A full day on site offline with no degraded stories |
| **Q1 2027** | 50 EVT units, beta | Port `lore-core` to Rust with JNI/Zephyr bindings; AOSP-lite bring-up on EVT; sensor hub firmware (step detection, step direction); on-device ASR/TTS/3B LLM via QNN; pack v1.1 with footprints and Valhalla routing; companion app (React Native) with the BLE GATT spec; OTA pipeline; beta telemetry | EVT battery ≥1.5 days on Square profile; on-device first story <1.5 s; crash-free sessions ≥99% |
| **Q2 2027** | Kickstarter | Demo-grade build; 2 more cities (Lisbon, Paris) through the editorial pipeline; persona voices; walk-me-home + SOS end-to-end with E2E sharing; security review/pentest | External pentest with no high-severity findings; 3 city packs |
| **Q3 2027** | DVT/PVT | Power optimisation (island-based engine), factory provisioning (keys, eFuses, test station software), certification support (Bluetooth SIG, carrier/eSIM), localisation (IT/ES/FR/DE) | Meets battery targets; certified BT/LTE stacks |
| **Q4 2027** | First 5k units shipped | Production OTA with staged rollout; support tooling; London/Barcelona packs; Atlas Glance camera beta | 30-day return rate due to software <3% |
| **2028** | Retail + 20 cities | Pack pipeline scaled (editor tooling, translation review); B2B fleet management (hostels/tour operators); accessibility mode (blind/low-vision: richer orientation cues, crossings guidance) | 20 cities, fleet console GA |

## Engineering principles
1. **No unverified claims are spoken.** Every change to narration has to pass the guard test-suite and the walk simulation gates in CI.
2. **Offline is the default path**, not a fallback. Cloud makes LORE better but is never required for a story.
3. **Measure on the street.** Every release gets real Rome walks and logged metrics (privacy-preserving).
4. **One core, many shells.** The PWA, device, companion app and backend share `lore-core`.

## Hiring plan (software)

| # | Role | When | Why | Est. cost (fully loaded, EU/US blend) |
|---|---|---|---|---|
| 1 | Founding Engineer, Embedded/Android platform (AOSP, BSP, power) | Now (pre-seed) | EVT bring-up in Q1 2027 is the critical path | $170–220k |
| 2 | Founding Engineer, Sensor fusion / Map Vision (GNSS, IMU, map matching) | Now (pre-seed) | Left/right accuracy is the product | $160–210k |
| 3 | ML Engineer, on-device speech & LLM (QNN/llama.cpp, ASR/TTS, wake word) | Q1 2027 | On-device latency and quality | $170–220k |
| 4 | Full-stack Engineer, backend + companion app (TypeScript, React Native, BLE) | Q1 2027 | App, pairing, safety, OTA backend | $140–180k |
| 5 | Data/Content Engineer + editorial lead (contract historians per city) | Q1 2027 | Pack pipeline and fact review; contractors ~$4–8k per city **(est.)** | $120–150k + contractors |
| 6 | Firmware Engineer, MCU/Zephyr (Pebble, sensor hub, MCUboot) | Q2 2027 (seed) | Pebble line and low-power island | $150–190k |
| 7 | Security Engineer (part-time/contract until seed) | Q2 2027 | Secure boot, provisioning, pentest coordination | contract ~$40k |
| 8 | QA/Field test engineer (Rome-based) | Q3 2027 | Street testing, regression walks | $70–90k |
| 9 | SRE/DevOps | Q4 2027 | Production OTA, observability, on-call | $150–180k |

Pre-seed budget allows roles 1–2 plus contractors. Roles 3–5 start when the seed closes or Kickstarter succeeds. Finance owns the budget model; these are planning ranges, not offers.

## Key risks
| Risk | Mitigation |
|---|---|
| Heading accuracy in urban canyons (magnetic disturbance, GNSS multipath) | Bias-learning Kalman filter (implemented), step-direction input, map matching to street geometry, "nearby" phrasing when confidence is low (implemented) |
| On-device LLM too slow or power-hungry | Template path is always available; LLM only rephrases; 1B fallback; cloud when online |
| Fact errors erode trust | Sourced fact cards, editorial review, guard validator, user "report a fact" flow (Q1 2027) |
| AOSP power overhead | Island-based engine; Yocto spike as contingency |
| LE Audio interoperability with users' earphones | A2DP fallback, compatibility matrix from beta |
