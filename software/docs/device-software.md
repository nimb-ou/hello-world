# LORE Device Software Plan (v0.1)

Scope: firmware and OS for **Pebble** (MCU + phone), **Square** and **Atlas** (AOSP-lite). Hardware part numbers are owned by `hardware/`. This document states what software needs and assumes. Values marked **(est.)** are targets to be measured on EVT units (Q1 2027).

## 1. Platform summary

| | Pebble | Square | Atlas |
|---|---|---|---|
| Main compute | BLE SoC (nRF54H20-class), Zephyr RTOS | Application SoC with NPU + LTE modem, AOSP-lite (Android 15 base) | Same as Square + camera ISP |
| Low-power island | Same MCU | Sensor DSP / companion MCU (sensor hub, wake word) | Same |
| AI | Phone/cloud; on-device keyword spotting only | On-device 3B LLM, ASR, TTS | 3–4B multimodal LLM |
| Storage | 16–64 MB flash (no packs; the phone holds them) | ≥32 GB UFS | ≥64 GB UFS |
| Audio out | BT LE Audio (LC3) / Classic A2DP via the phone, small speaker | LE Audio + A2DP direct, speaker | Same |

## 2. Boot sequence (Square/Atlas)
1. **ROM → primary bootloader:** SoC secure boot. The vendor ROM verifies the PBL/XBL signature with an OEM key hash fused in eFuses (fuses are blown at the factory station).
2. **Bootloader (ABL):** verifies `vbmeta` (Android Verified Boot 2.0, rollback index), selects the A/B slot and loads the kernel.
3. **Kernel + init:** dm-verity on `system`, `vendor` and `models`. File-based encryption keys are unlocked with the TEE/KeyMint (no user PIN by default; device-bound keys).
4. **LORE system services:** Sensor Hub bridge, Map Vision, Story Engine, Voice, Safety, Sync. A custom headless launcher with no app drawer.
5. **Ready chime.** Target cold boot under 15 s **(est.)**. Normal use resumes from suspend in under 300 ms.

Safety exception: the SOS long-press is handled by the low-power island and the modem path. It works even if the application processor (AP) is booting or has crashed.

## 3. Power management states

| State | AP | Island/DSP | GNSS | LTE | Audio | Typical trigger | Target draw (est.) |
|---|---|---|---|---|---|---|---|
| **Off/ship** | off | off | off | off | off | factory / long-hold | <20 µA |
| **Standby** (in pocket, not walking) | suspend | step detect + wake word | off | eDRX/PSM | off | no steps 3 min | 3–5 mW |
| **Walk-listening** (walking, no story) | suspend, wakes 1 Hz | sensor fusion | L1+L5 1 Hz (duty-cycled tracking) | PSM / idle | off | steps detected | 40–70 mW |
| **Narrating** | active (little cores) | fusion | 1 Hz | idle | TTS + LE Audio LC3 | engine decision | 150–250 mW |
| **Thinking** (on-device LLM/ASR) | big cores + NPU | – | 1 Hz | – | – | voice query | 1.5–3 W, bursts of 1–4 s |
| **Online conversation** | active | – | 1 Hz | connected | duplex | press-to-talk | 600–900 mW |
| **SOS** | active | – | continuous | connected (NTN on Atlas) | speaker | long press | max |

Policies:
- The Story Engine is evaluated on the island, using a pre-filtered candidate list of the nearest 20 POIs pushed every 30 s. The AP wakes only when a candidate crosses the score threshold.
- GNSS is duty-cycled and enters 5 s intervals when standing still.
- Packs are memory-mapped from SQLite. There is no network while offline-capable.

Battery math for Square with a 2-day target is owned by `hardware/`. Software provides the duty-cycle profile above.

## 4. Wake word and controls
- **Physical controls** (from COMPANY.md): press = talk, double-press = "What's around me", long-press 2 s = SOS with a 5 s cancel window and haptic countdown.
- **Wake word "Hey Lore":**
  - 2-stage detector: an always-on tiny keyword model on the DSP (≤100 kB, ~1 mW), then a confirmation model on the AP.
  - Targets **(est.):** under 1 false accept per 24 h of street audio, and over 95% true accept at 1 m in 70 dB(A) traffic.
  - Training data: in-house recordings from 300+ speakers plus augmentation with Rome street noise. Recordings are consented; tracked in legal-ops.
- **VAD** runs whenever the mic is active. "User talking" feeds the Story Engine quiet policy. The mic is off in Standby unless the wake word is enabled (user setting, default on).

## 5. Offline packaging and City Pack storage

```
/data/lore/
  packs/rome/1.0.3/
     manifest.json        # city, version, bbox, sha256 of every file, signature (Ed25519)
     pack.sqlite          # schema in city-pack/lore_citypack/sqlite_writer.py (pois, facts, fact_sources, poi_tags, footprints, poi_rtree)
     routing/             # Valhalla tiles (pedestrian), ~25-40 MB central Rome (est.)
     audio/               # optional pre-rendered premium-voice narrations (opus 24 kbps)
  models/                 # separate signed partition, mounted read-only (dm-verity)
     llm-3b-w4/ asr/ tts-<voice>/ kws/
  state/engine.json       # spoken fact IDs, profile (encrypted at rest via FBE)
```

- **Pack sizes (est.):** Rome stories pack is 2–5 MB SQLite (86 POIs now; ~3,000 POIs at launch). Routing adds 25–40 MB, and optional pre-rendered audio ~120 MB. Maps for the Square screen use vector tiles (PMTiles), ~60 MB.
- **Download:** over Wi-Fi or LTE through the CDN, resumable (HTTP range). The manifest is verified before activation and the switch is atomic via a symlink.
- **Updates:** deltas are row-level SQLite changesets (`sqldiff`-style) signed per version.
- **Free tier:** 3 cities. Packs are not DRM-encrypted (the content is facts with public sources); premium audio is licensed per account.

## 6. OTA
- **OS:** AOSP A/B `update_engine` payloads, signed with the OTA key (HSM-held). Staged rollout is 1% → 10% → 50% → 100% with automatic halt on crash-rate or boot-failure regression. Rollback protection comes from the AVB rollback index.
- **Models:** an independent A/B partition so a model update doesn't need an OS release. Each model has its own version and is tested against the narration guard suite.
- **MCU** (Pebble and the companion MCU): MCUboot with signed images and swap-with-revert. Delivered via the phone app (BLE DFU) or the AP.
- **Policy:** updates install only when charging, or above 50% battery and idle. They are never applied during an active walk-me-home timer.

## 7. Security
- **Secure boot:** an OEM key is fused at the factory. AVB 2.0 with dm-verity covers all read-only partitions. Debug ports (JTAG/SWD) are fused off on production units.
- **Encrypted storage:** AOSP file-based encryption (AES-256-XTS) with keys bound to KeyMint/TEE. Pebble uses nRF PSA Crypto with key storage in KMU.
- **Device identity:** a per-device key pair generated in the TEE at manufacturing, with a certificate signed by the LORE device CA. It is used for mTLS to the backend and for attestation.
- **E2E location sharing:** the device generates the share key and seals each location update (XChaCha20-Poly1305). The server only ever sees ciphertext (see `backend/src/safety.ts`).
- **App ↔ device:** BLE LE Secure Connections pairing (numeric comparison on Square/Atlas; Pebble uses Just Works plus an app-level ECDH bound to the account). All GATT payloads after pairing are additionally encrypted at the application layer with a session key derived from that ECDH.
- **Supply chain:** SBOM per build, reproducible builds for the LORE services, signed artifacts, and vendor blobs tracked with versions and CVE monitoring.

## 8. App ↔ device protocol (BLE GATT)
Messages are protobuf (`lore.proto`) framed with a 2-byte length, chunked to the negotiated MTU (target 247). Base UUID: `4C4F5245-xxxx-4C61-6273-2D4C4F524500` (ASCII "LORE…Labs-LORE"); `xxxx` is the 16-bit ID below.

| Service / characteristic | ID | Properties | Payload | Notes |
|---|---|---|---|---|
| **LORE Control Service** | 0x1000 | – | – | Primary service |
| Command | 0x1001 | Write w/ response | `Command{more, around, quiet(duration), resume, set_persona, set_interests, speak_text}` | App buttons mirror the device controls |
| Event | 0x1002 | Notify | `Event{narration_started(poi_id, fact_ids, direction, tier), narration_ended, quiet_reason, button(type)}` | Drives the app's "Now" card |
| Settings | 0x1003 | Read/Write | `Settings{persona, interests, wake_word_on, volume, units, language}` | Versioned |
| **Location & Heading Service** | 0x2000 | – | – | Used by Pebble, which has no GNSS |
| Phone Location | 0x2001 | Write w/o response | `Fix{t, lat_e7, lng_e7, acc_cm, speed_cms, course_cdeg}` at 1 Hz | Phone → device |
| Heading | 0x2002 | Notify | `Heading{t, deg_x100, sigma_x100, confidence}` at 2 Hz | Device fused heading → app |
| **City Pack Service** | 0x3000 | – | – | Square/Atlas usually download over Wi-Fi/LTE themselves |
| Pack Manifest | 0x3001 | Read | `PackList{city, version, size, installed}` | |
| Pack Transfer | 0x3002 | Write w/o response + Notify | `Chunk{file_id, offset, bytes}` / `Ack{offset}` | Pebble stories pack via BLE (~2–5 MB) |
| **Safety Service** | 0x4000 | – | – | |
| SOS | 0x4001 | Notify + Write | `Sos{state, t, cancel}` | Device → app pushes SOS to contacts if the device has no LTE |
| Walk-me-home | 0x4002 | Read/Write/Notify | `Timer{id, due_at, status}` | Mirrors `/safety/walk-home` |
| Share Key | 0x4003 | Write (encrypted only) | `ShareKey{share_id, key32}` | Lets the phone show the same live share |
| **Device Info / OTA** | 0x5000 | – | – | Plus standard 0x180A Device Information and 0x180F Battery |
| OTA Control | 0x5001 | Write/Notify | `Ota{begin(image, size, sha256), status}` | MCUboot DFU (SMP) on Pebble |
| Diagnostics | 0x5002 | Read | counters (see architecture §10) | Opt-in |

Audio does not go over this GATT link. It is LE Audio (BAP unicast, LC3 32 kHz) or Classic A2DP straight to the user's earphones; the phone is not involved.

## 9. Open questions (owners)
- AOSP vs Yocto power delta on the chosen SoC: Software + Hardware, decide by the EVT power test (Feb 2027).
- Whether the Pebble needs its own GNSS (the phone-only fix degrades heading/side-of-street when the phone is in a bag): Hardware.
- Wake-word data licensing and consent: Legal-ops.
