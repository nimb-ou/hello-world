# LORE System Architecture (v0.1, Oct 2026)

Owner: Software (CTO). Status: proposed baseline. Numbers marked **(est.)** are engineering estimates and need validation by Hardware/Finance.

## 1. Goals and constraints
- **Offline first.** Stories, maps, routing and basic voice must work with no signal (City Packs + on-device AI).
- **No invented history.** Narration may only use fact cards that are verified and sourced. Every spoken claim traces to a `fact_id`.
- **Eyes up, safe.** LORE is silent while crossing roads, while the user talks, and at speed. SOS and walk-me-home work without the phone.
- **Battery.** 1.5 to 3 days (Pebble to Atlas). The radios and the SoC's big cores are the budget, so we duty-cycle hard.
- **Privacy.** Location stays on the device by default. Shared location is end-to-end encrypted.

## 2. Device OS decision: Android AOSP-lite vs Linux/Yocto

| Criterion | AOSP (headless, trimmed) | Linux (Yocto, custom) |
|---|---|---|
| LTE/eSIM/IMS modem stack | Mature RIL, vendor-supported on Qualcomm/MediaTek | Usually ModemManager + vendor libs; more integration work |
| BT LE Audio (LC3, BAP, CAP) | Present since Android 13 with vendor offload | BlueZ LE Audio still maturing; LC3 offload is DIY |
| NPU access (QNN/NeuroPilot) | First-class SDKs | Available, but fewer samples |
| Boot time / RAM floor | ~12–20 s, ~1.2 GB (est.) | ~3–6 s, ~150 MB (est.) |
| Power control | Doze/AlarmManager; less control at kernel level | Full control (cpuidle, runtime PM, custom governor) |
| Certification (GMS not needed) | AOSP without GMS is fine | Fine |
| Team hiring pool | Large | Smaller (embedded Linux) |

**Decision:**
- **Pebble** runs an MCU (nRF54H20-class) with Zephyr RTOS plus a phone companion. There is no OS decision for it; all heavy work happens on the phone or in the cloud.
- **Square/Atlas** run **AOSP-lite (Android 15 base, headless with a custom launcher, no GMS)** on a Qualcomm QCS/QCM-class or MediaTek Genio-class SoC with LTE Cat-4. The reasons are the modem/eSIM/LE Audio stacks and the NPU toolchains; those are where schedule risk lives.
- **We keep the core portable.** The story engine and fusion are TypeScript today and will be ported to Rust (`lore-core`) with C ABI bindings for Android (JNI), Zephyr and iOS/Android companion apps. A Yocto build stays as a fallback spike (Q1 2027) in case AOSP power numbers miss the targets.

Hardware part selection is owned by `hardware/`. This document only fixes the software requirements: an NPU of at least 10 TOPS INT8 for the 3B model on Square and 3–4B plus vision on Atlas, at least 4 GB LPDDR4X (Square) or 6 GB (Atlas), at least 32 GB UFS, and a dedicated low-power island (Hexagon sensor DSP or companion MCU) for wake word, step detection and the sensor hub.

## 3. Services (on device)
Each service is a process (Android service / Zephyr thread) that communicates over a local message bus (Binder AIDL on AOSP; a protobuf schema shared with BLE).

| Service | Responsibilities | Key code |
|---|---|---|
| **Sensor Hub** (low-power island) | IMU at 100 Hz, magnetometer at 50 Hz, step detection, step direction (PCA of horizontal acceleration), magnetic anomaly flag, wake-word front end | firmware |
| **Map Vision** | GNSS L1+L5 fixes plus map matching to the pedestrian graph; heading fusion (`HeadingKalman`); classifying POIs as ahead/left/right/behind and "look up" using footprints and heights; side of street | `geo.ts`, `heading-fusion.ts` |
| **Story Engine** | Candidate scoring, novelty, cooldowns, tiers, "tell me more", "what's around me", live-info merge | `story-engine.ts` |
| **Narration** | Prompt building, on-device or cloud LLM, guard, template fallback, personas | `narration.ts` |
| **Voice** | Wake word, VAD, ASR, intent routing, TTS, audio focus/ducking | see §4 |
| **Navigation** | Valhalla pedestrian routing on pack tiles, turn cues blended with stories, crossing detection (`highway=crossing` nodes and GNSS speed/trajectory) | Q1 2027 |
| **Safety** | SOS (long press), walk-me-home timers, E2E location sharing, fall/inactivity heuristics, emergency numbers per country (112 in the EU) | `backend/src/safety.ts` (server half) |
| **Sync** | City Pack download and delta updates, engine state (spoken fact IDs), profile, settings; CRDT-free last-writer-wins per key | Q1 2027 |

### Quiet-moment policy (implemented in `StoryEngine.quietReason`)
In priority order:
1. Crossing a road, plus 4 s afterwards.
2. User talking (VAD), plus 3 s afterwards.
3. Speed above 2.3 m/s (jogging, scooter, vehicle).
4. LORE already speaking.
5. A 20 s minimum gap between stories.
6. GNSS accuracy worse than 35 m.

An explicit "tell me more" overrides LORE's own speech and the manual "Quiet" setting, but never a safety quiet moment; it is deferred until the moment ends. The simulation (`npm run sim`) measures compliance: 0 story starts during 177 s of simulated quiet moments.

## 4. Voice pipeline

```
mic ─► AEC/NS (DSP) ─► wake word ("Hey Lore"; or the press-to-talk button) ─► VAD
     ─► ASR ─► intent router ──┬─ local intents (more / around / quiet / SOS / directions) ─► engine
                               └─ open question ─► LLM (on-device if offline, cloud if online) with tools
     ◄─ TTS ◄─ narration script (guarded) ◄─────────────────────────────────────────────┘
```

| Stage | On device | Cloud (when online) |
|---|---|---|
| Wake word | microWakeWord / openWakeWord-style 50–100 kB keyword model on the DSP, at under 1 mW (est.) | – |
| VAD | Silero VAD (ONNX, ~2 MB) | – |
| ASR | Moonshine Base / Whisper-small INT8 for EN, IT, ES, FR, DE (~100–250 MB) | Streaming ASR for long questions and accents |
| LLM | Llama 3.2 3B Instruct or Qwen2.5-3B (Square), 1B-class (Pebble via phone), Gemma-class 4B multimodal (Atlas) | Claude (`claude-sonnet-5-5` default for narration/tool use; `claude-haiku-5-5` for cheap routing) or a realtime speech-to-speech provider for conversational mode |
| TTS | Piper / Kokoro-82M-class neural TTS (~80–150 MB per voice) | Premium neural voices (persona voices) |

Latency budget for a press-to-talk question online, measured from end of speech to first audio: ASR final 250 ms, LLM first token 600 ms, TTS first chunk 200 ms, giving under 1.2 s. Offline on Square: ASR 400 ms, a 3B model at Q4 doing ~12–18 tok/s (est.), so the first sentence arrives in about 1.5 s.

## 5. On-device models and packaging

| Model | Use | Quantization | Runtime | Size on disk (est.) |
|---|---|---|---|---|
| Llama 3.2 1B Instruct | Pebble companion (phone) / Square fallback | Q4_K_M GGUF | llama.cpp (CPU/GPU) | ~0.8 GB |
| Llama 3.2 3B Instruct or Qwen2.5-3B | Square narration rephrasing and Q&A | W4A16 (QNN) / Q4_K_M | QNN on Hexagon NPU, llama.cpp fallback | ~2.0 GB |
| Gemma 3 4B (multimodal) | Atlas "Glance" camera Q&A | W4A16 | QNN / MLC-LLM | ~2.6 GB |
| Whisper-small / Moonshine | ASR | INT8 | ONNX Runtime + NPU EP | 0.1–0.25 GB |
| Piper/Kokoro voice | TTS | FP16/INT8 | ONNX Runtime | 0.08–0.15 GB per voice |

Rules:
- The on-device LLM uses exactly the same `buildNarrationPrompt()` and `validateNarration()` as the cloud. A guard failure falls back to the template, so the worst case is a plainer story, never a wrong one.
- Model licences (Llama Community License, Gemma Terms, Qwen Apache-2.0) need Legal review before shipping; this is tracked in `legal-ops/`.
- Models ship as a separate signed A/B "model partition" image so they can be updated independently of the OS (see device-software.md).

## 6. Cloud
Services run in containers on a managed platform (Cloud Run / ECS Fargate), in an EU region first for GDPR and then US.

| Service | Purpose | Implementation |
|---|---|---|
| Gateway | Auth (device certificate mTLS plus user JWT), rate limits | Envoy / API GW |
| Narration (`/narrate`) | Claude tool calling, restricted to fact cards (`get_fact_cards`, `get_live_info`), validator, template fallback | `backend/src/narrate.ts` |
| Tools for the conversational agent | `places_nearby` (City Pack + Overture/Foursquare), `web_search` (Claude server tool or Brave), `hotels` (Booking/Expedia affiliate), `directions` (Valhalla), `weather` (Open-Meteo), `events` (Ticketmaster Discovery / local feeds) | adapter interfaces in `backend/src/adapters/` |
| Safety | Walk-me-home timers, share links, escalation (SMS via Twilio) | `backend/src/safety.ts` |
| Pack CDN | Signed City Pack bundles plus deltas | object storage + CDN |
| Pack pipeline | Nightly OSM/Wikipedia/Wikidata ingest, editor review queue | `city-pack/` |

**Tool-calling contract:** search, events and weather results are *live info*. They are spoken with "right now" and a source, and they never become fact cards. Only the editorial pipeline creates fact cards.

## 7. Data pipeline (City Packs)

```
OSM (Overpass/planet extract) ─┐
Wikipedia REST + Wikidata ─────┼─► candidates ─► match/dedupe ─► candidate facts (needs_review)
Curated seed (editors) ────────┘                                   │
                                  editor review UI ◄────────────────┘ (support score from source text)
                                         │ approve
                                         ▼
          interest scoring ─► pack build (JSON + SQLite + routing tiles + footprints) ─► sign ─► CDN
```

- **Today:** `python -m lore_citypack build` produces `rome.pack.json` and `rome.pack.sqlite` (86 POIs, 215 facts, 83 distinct sources). With `--online` it runs real Overpass and Wikipedia REST fetches, and on failure falls back to the seed. That fallback is exercised in this sandbox.
- **Next:**
  - building footprints (OSM `building=*` ways joined to POIs; the `footprints` table exists);
  - Valhalla pedestrian tiles;
  - Wikipedia pageviews in the interest score;
  - multilingual fact cards (translation is reviewed, not generated live).

## 8. Privacy and security
- **On-device first.** Raw GNSS traces never leave the device by default. Cloud narration sends only `poi_id`, `fact_ids`, persona and tier, not coordinates. `/nearby` is used only by the phone companion and can be served from the pack locally.
- **E2E location sharing.** A per-share 256-bit key is generated on the device. Location updates are sealed with XChaCha20-Poly1305. The key travels only in the share URL fragment (`#k=`), which browsers never send to servers. The server stores ciphertext (it enforces base64url and rejects plaintext-looking bodies; this is tested).
- **Data minimisation and GDPR.** Engine state holds spoken fact IDs only. Telemetry is aggregated (§10). Users can export and delete their data, and retention is 30 days for crash logs.
- **Device security.** Secure boot, verified boot, file-based encryption and attestation are covered in `device-software.md` §7.
- **LLM safety.** Tools are scoped to the requested POI (the tool loop rejects other IDs). The validator blocks unknown citations, numbers and proper nouns that are not in the facts. Refusals and failures go to the template.

## 9. OTA updates
- **OS:** A/B seamless updates (AOSP `update_engine`), signed, with staged rollout (1% → 10% → 50% → 100%) and automatic rollback on boot failure.
- **Models:** a separate signed partition with delta updates.
- **City Packs:** content-addressed bundles with deltas, downloaded on Wi-Fi or charge by default (see device-software.md §5).
- **Firmware** (MCU, BT, modem): vendor tools, but gated by the same staged rollout.

## 10. Observability
- OpenTelemetry traces in the backend: `/narrate` spans carry model, tokens, guard result and fallback reason.
- On-device counters, privacy-preserving and aggregated daily, uploaded only with consent:
  - narrations per km;
  - guard rejection rate;
  - quiet-moment violations (target 0);
  - heading confidence distribution;
  - battery per hour by state;
  - TTS underruns;
  - wake-word false accepts per hour.
- **Quality gates in CI:** the walk simulation must keep repeat rate at 0, quiet compliance at 100%, direction accuracy at or above 85%, and narrations per km between 4 and 16 (`simulations/test/walk-sim.test.ts`).

## 11. Scaling
- Narration is stateless and horizontally scaled. Prompt caching covers the system prompt and tool schemas, which form a stable prefix.
- Expected load **(est.):** 5k devices in Q4 2027 at 30% daily active, 2 h of walking per active day, and ~30% of narrations going to the cloud. That is ~25 narration requests per active hour per device, or about 75k requests/day, with peaks of ~10 RPS. A few small containers can handle it.
- City Pack downloads (~150–400 MB per city with routing and models excluded) are CDN egress, about $0.01–0.03 per download **(est.)**.

## 12. Cost per user per month (est.)
Assumptions for a **heavy month**, meaning a traveller actually on a trip: 10 walking days × 3 h, ~9 narrations/km at 4 km/h, giving ~1,080 narrations. 30% go to the cloud LLM and the rest use the on-device template or LLM. There are 40 voice questions, and 20 min of realtime conversational voice.

| Item | Unit price (source) | Usage | $/month |
|---|---|---|---|
| Cloud narration, Claude Sonnet 5.5 | $2 / MTok in, $10 / MTok out (Anthropic pricing, Oct 2026) | 324 calls × (~2.5k in + ~250 out, 2 turns) | ~$3.30 |
| Voice Q&A with tools, Claude Sonnet 5.5 | same | 40 × (~6k in, ~400 out) | ~$0.65 |
| Prompt caching saving | cache reads ~10% of input price | ~60% of input tokens cached | −$1.30 |
| Realtime speech-to-speech mode | ~$0.05–0.10/min **(est., vendor-dependent)** | 20 min | ~$1.50 |
| Cloud ASR (fallback) | ~$0.006/min **(est.)** | 30 min | ~$0.20 |
| Cloud TTS premium voice | ~$15 per 1M chars **(est.)** | 20% of narrations × 600 chars | ~$2.00 |
| Places/live data APIs | ~$0.005–0.02/call **(est.)**, heavily cached | 100 calls | ~$1.00 |
| Maps/routing | self-hosted OSM/Valhalla | – | ~$0.05 |
| Infra (compute, CDN, DB, observability) | – | – | ~$0.40 |
| **Total, heavy month (excl. cellular data)** | | | **~$7.80** |
| **Blended per subscriber** (~35% of subscriber-months are trip months; the rest are near-idle at about $0.30) | | | **~$3.00** |

Cellular data (eSIM wholesale, ~$1–4 per GB **(est.)**) is modelled by Finance. Levers if margins are tight:
- default to on-device TTS;
- use `claude-haiku-5-5` ($0.10/$0.50 per MTok) for routing and short rephrasing;
- push more narration to the on-device 3B model.

Explorer is $9.99/mo, so even a heavy month leaves gross margin before data.
