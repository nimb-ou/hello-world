# LORE UX specification: device, voice and companion app

**Rev:** EVT-0 · 2026-10-31 · Owner: Head of Design (UX/UI)
Applies to: **Pebble (P1, "Lite", phone-tethered per D10)**, **Square (S1)** and **Atlas (A1)**, plus the companion app (iOS and Android).
Related documents: `design/industrial/id-spec.md` (controls hardware), `design/ux/user-journeys.md`, screen mockups in `design/ux/device-screens/` and `design/ux/app-screens/`.

---

## 0. Principles

1. **Ears first, eyes second, hands last.** Audio carries the experience. The screen confirms and the buttons interrupt. A user can complete a full day without looking at the device.
2. **A friend, not a guide.** Narration is opt-out by silence, never pushy. At most one unsolicited story every 4 minutes by default (§7).
3. **Never at the wrong moment.** When crossing a road, talking, paying, or with traffic detected, LORE is quiet (§7).
4. **Trust is visible.** Every story carries a source ("say *source?*"). The camera has a hardware LED. Location sharing shows a persistent indicator.
5. **Offline is not an error.** It is a mode, with its own colour and wording (§10).

## 1. Input grammar

### 1.1 Pebble (top dish = Talk, side rocker = volume)

| Gesture | Action | Feedback |
|---|---|---|
| **Press** (< 400 ms) | Pause or resume the current story. When idle: "What's this?" (story for the nearest point of interest in the facing direction) | Earcon `tick` + ring quarter-arc flash |
| **Press and hold** (≥ 400 ms, keep holding) | Push-to-talk. Release to send | Earcon `listen-open` / `listen-close`. Ring "breathing" Terracotta |
| **Double press** | **"What's around me"**: 3 nearest items in a clockwise sweep (left, ahead, right) | Earcon `sweep`. Ring segments light in sweep order |
| **Triple press** | Repeat the last sentence | `tick-tick` |
| **Hold 3 s** (keep holding past PTT) | **SOS countdown** (§6). Phone confirms | Rising haptic every 1 s, ring turns red |
| Rocker + / − | Volume. Hold − for 2 s = mute narration ("Quiet") | Volume earcon at the new level |
| Rocker + and − together for 2 s | Bluetooth pairing mode | Ring spins blue |

### 1.2 Square and Atlas (crown · Talk key · SOS key · touch)

| Control | Gesture | Action |
|---|---|---|
| **Talk key** | Press | Pause / resume. When idle: "What's this?" |
| | Hold | Push-to-talk (release to send) |
| | Double press | **What's around me** (screen shows the Nearby list) |
| | Triple press | Repeat the last sentence |
| **Crown** | Rotate | Scroll lists. On the Now Narrating screen it scrubs ±10 s. On the compass it rotates the "look" target |
| | Press | Back / Home |
| | Double press | Last app (toggles Map ↔ Now Narrating) |
| | Hold 2 s | Quick settings (Quiet, brightness, battery modes) |
| **SOS key** (recessed) | Hold 2 s | **SOS countdown** (§6) |
| | 5 quick presses | SOS countdown (alternative, ISO-style emergency pattern) |
| **Talk + crown** | Hold together 2 s | Screenshot (debug builds) / share current place to phone (retail) |
| **Touch** | Tap / swipe | Standard. Swipe down = notifications. Swipe up = Nearby. Swipe left/right = cards. **Touch is disabled while walking above 1.2 m/s unless the device is raised** (IMU "glance" pose), to prevent false taps through a pocket |
| **Wrist-raise / glance** | Lift to ~45° and hold for 300 ms | Screen wakes (always-on-display level → full) |

*Left-handed mode:* rotating 180° mirrors the crown/Talk side. All gestures are unchanged.

## 2. Voice

Wake is press-to-talk by default. An optional hands-free wake word, "Hey Lore", runs in the always-on hub, is off by default, and is shown in the privacy dashboard. Speech is understood on-device (Square/Atlas) or via the phone (Pebble). Answers longer than 20 words go to the screen as well (Square/Atlas).

| Intent | Example utterances | Offline? |
|---|---|---|
| Story here | "What's this?", "What am I looking at?", "Tell me about that church" | ✓ (City Pack) |
| Deeper | "Tell me more", "Why?", "Who built it?" | ✓ partial / ✓ online |
| Source | "Source?", "How do you know that?" | ✓ (citations ship in the pack) |
| Around | "What's around me?", "Anything interesting nearby?" | ✓ |
| Navigation | "Take me to the Pantheon", "Walk me to my hotel", "How far?" | ✓ (offline routing) |
| Food | "Somewhere good for dinner", "Cacio e pepe near here, not touristy", "Open now?" | ✓ list / ✓ online for live hours + booking |
| Booking | "Book a table for two at 8" | online only (partner API) |
| Practical | "Nearest pharmacy / toilet / ATM / water fountain" | ✓ |
| Language | "How do I say *the bill, please*?" (spoken in Italian, slowly then normally) | ✓ (pack phrasebook) |
| Safety | "Walk me home", "Share my location with Sam", "I feel unsafe" | ✓ partial (SMS fallback) |
| Control | "Quieter", "Shorter stories", "Only history", "Stop for 30 minutes", "Battery?" | ✓ |
| Memory | "Save this", "What was that fountain earlier?" | ✓ |

**Voice persona:** warm, mid-tempo (165 wpm), British-neutral English at launch, with Italian, Spanish, French and German voices at City Pack v2. Tone rules come from `brand/voice-and-tone.md`. Every factual claim must exist in the pack's source table; the generator may rephrase but never add facts (see software/ story engine).

## 3. Story format

- **Length:** 20–40 s (≈ 55–110 words). "Tell me more" chains up to three deeper layers of 45–60 s each.
- **Structure:** spatial anchor ("On your right…") → hook → one concrete detail to look at → optional prompt ("Want the gory version?").
- **Spatial words:** *left / right / ahead / behind / look up / look down*. They are computed from the heading (IMU and compass fused with walking direction) and the building footprint. If heading confidence is below 70 %, LORE falls back to landmark-relative wording ("the building with the green shutters").
- **Ducking:** a story pauses automatically on a cross-street (map), on a speech pair (the user or someone else speaking within 1.5 m, detected on-device by VAD with no recording), on a phone call, or when the user stops and turns away for 8 s.

## 4. Earcon map

All earcons are under 600 ms, mixed −18 LUFS, built from a shared "struck brass + felt" palette (Sound brief: Brand). They play through the earphones, or the speaker when no earphones are connected. Each one also has a distinct haptic on Square/Atlas.

| ID | Meaning | Sound (descriptor) | Haptic (S/A) |
|---|---|---|---|
| `tick` | Acknowledged | single soft felt-mallet tap, 1.2 kHz | 1 × 10 ms |
| `listen-open` / `listen-close` | Mic on / off | rising / falling two-note brass, a fifth apart | 1 × 15 ms |
| `story-start` | A story is starting (unprompted) | three-note ascending motif (LORE "signature") | none |
| `look` | "Look up / look here" moment within a story | high bell shimmer | 2 × 10 ms |
| `sweep` | What's around me | short pan left→right whoosh with three pips | 3 pulses |
| `turn-left` / `turn-right` | Navigation turn in 30 m | two-note motif panned L or R | L: long-short, R: short-long |
| `arrive` | Arrived | resolved chord | 1 × 40 ms |
| `offline` / `online` | Connectivity change | muted single note / brighter single note | none |
| `pack-ready` | City Pack installed | signature motif + chord | 1 × 30 ms |
| `battery-low` | ≤ 15 % | descending two notes | 2 × 20 ms |
| `checkin` | Walk Me Home check-in due | gentle repeating knock ×2 | 2 × 30 ms |
| `sos-count` | SOS countdown tick | sharp wood block, every second | 1 × 80 ms |
| `sos-sent` | SOS delivered | three firm tones | 3 × 80 ms |
| `detached` | Device fell or was pulled from its mount | two quick high notes | 2 × 15 ms |
| `error` | Did not understand / cannot do that | soft low thud | 1 × 25 ms |

## 5. LED ring (Pebble) and status light (Square/Atlas screen-off)

The ring has 8 RGB segments behind frosted PMMA. Brightness is capped at 40 cd/m² at night (ALS) and 120 outdoors.

| State | Pattern | Colour |
|---|---|---|
| Idle, connected | off (dark by default). A tap shows 1 s of the battery arc | — |
| Listening | slow breathing, 1.2 s cycle | Terracotta `#C4623A` |
| Thinking | single segment orbiting, 0.8 s/rev | Bone white |
| Narrating | very low glow on 1 segment pointing to the subject's side (left/right/ahead) | warm white 10 % |
| Navigation turn | 3 segments on the turn side pulse twice | Brass `#B8935A` |
| Offline | one segment on the south side dimly lit for 2 s on change | Fog `#9AA0A6` |
| Charging | fill arc proportional to %, breathing at the tip | Olive `#5E6B4E` |
| Battery low | 2 segments blink ×3 every 60 s | Amber |
| Pairing | full ring spin | Blue (only use of blue) |
| Walk Me Home active | 1 segment slow heartbeat every 5 s (visible to the user, discreet to others) | Brass |
| **SOS countdown** | full ring, flashing at 2 Hz | Signal red `#D2392B` (brand token) |
| SOS sent / live | full ring solid 1 s every 5 s | Red |
| Error / not understood | 2 segments flicker once | Fog |

## 6. Safety flows

### 6.1 SOS

1. **Trigger:** SOS key hold 2 s, or 5 quick presses (Square/Atlas). On Pebble: Talk hold for 3 s, or "Hey Lore, emergency".
2. **Countdown: 5 s.** The screen goes full red with a countdown and *Release + press crown to cancel*, plus `sos-count` haptics and the red ring. Audio in the earphones says: "Calling for help in 5. Press the crown to cancel."
3. **Send**, in order of availability:
   - Local emergency number via LTE voice. The device supports 112/911 dialling; the number is set by MCC.
   - Plus an SMS/data alert to up to 5 safety contacts with a live location link (updates every 30 s for 60 min).
   - On Atlas, with no LTE: **satellite NTN message** via Skylo with lat/long and a medical note. The user is coached to "Hold the device face-up, with a clear view of the sky".
   - On Pebble: the phone performs the call and SMS. If the phone is unreachable, the Pebble shouts "Help, call 112" on the speaker at 85 dB (optional, off by default).
4. **Live:** red status bar. The location keeps sharing. The narrator falls silent. The screen shows contacts notified and an ETA if responders confirm.
5. **End:** hold SOS for 2 s, then confirm with the crown (prevents an attacker cancelling with one press). Contacts get an "I'm safe" message.

**False-alarm handling.** The 5 s countdown plus the requirement to release-and-confirm to cancel. In Settings: a "practice SOS" mode that never dials.

### 6.2 Walk Me Home

1. Start by voice ("Walk me home"), from the app, or from the Square/Atlas Quick Settings.
2. LORE asks for the destination (default: the saved hotel), shows the safest route (well-lit, open venues, main streets, weighted from OSM `lit=yes` and footfall), and lets the user choose contacts. The ETA is shared.
3. **While walking:** a quiet Brass heartbeat on the ring or status bar. Stories switch to "companion mode": short, every 5–8 min, about the walk itself ("2 minutes to the river, the bridge is well lit"), so the user is audibly accompanied.
4. **Check-ins:** a `checkin` earcon plays if the user (a) stops for more than 4 min off-route, (b) deviates by more than 150 m, or (c) the ETA is exceeded by 10 min. The user then has 60 s to press Talk (or say "I'm fine"). Otherwise the contacts are alerted with the live location. Escalation to SOS is offered, not automatic.
5. **Arrive:** within 30 m of the destination, an `arrive` earcon plays and the contacts get "Arrived safely" automatically.

## 7. "Quiet moments" logic (when LORE speaks)

LORE computes a **talk score** every 2 s. An unprompted story plays only when the score is above 0.6 *and* the cooldown has elapsed (default 4 min; adjustable 2–15 min or "only when asked").

| Signal | Effect |
|---|---|
| Road crossing ahead (map + < 15 m) or crossing in progress (heading over a carriageway) | **hard block** |
| Speech detected nearby (VAD, not recorded) | hard block + pause the current story |
| Phone call / media from the phone | hard block |
| Speed above 2.2 m/s (running or cycling) | block, except for navigation |
| Stationary below 0.2 m/s for more than 20 s in a POI-dense spot | +0.3 ("you've stopped, here's something") |
| Facing a POI with story score ≥ 4/5 within 40 m | +0.4 |
| Inside a venue (Wi-Fi fingerprint / GNSS loss) | −0.4 |
| Night (after 22:00 local) and alone | −0.2 for history; +0.2 for safety info |
| User has dismissed 2 stories in a row | cooldown ×2 |
| Do-not-disturb windows / "Quiet" | hard block (navigation and safety still speak) |

Notification rules:

- **Phone notifications are never read aloud by default.** An allow-list is opt-in (e.g., Uber "driver arriving", calls from favourites).
- Live info (closures, rain in 20 min, last-entry times) is interrupt-eligible only if it changes the plan, and at most 1 per 30 min.
- Priority order: **Safety > Navigation > Live info > Requested story > Unprompted story.**

## 8. Screen UI (Square/Atlas: 1.6" 466 × 466 AMOLED)

Mockups are in `device-screens/png/`; the contact sheet is `device-screens/contact-sheet.png`.

- **Grid:** 466 px square with R ≈ 90 px display corners. 24 px safe margin, 8 px base unit.
- **Type:**
  - Fraunces 300 for the time and big numerals (72–96 px).
  - Inter 500/600 for UI (17–28 px; minimum 17 px ≈ 7 pt at 412 ppi, readable at 35 cm).
  - JetBrains Mono for distances and coordinates.
- **Colour:** pure black background (AMOLED power). Bone `#F3EEE6` primary text, Fog secondary, Terracotta for the single active element, Brass for navigation, red for SOS only. Offline mode adds a Fog "OFFLINE · ROME PACK" chip; the palette is otherwise unchanged.
- **Always-on display:** time plus heading tick only, 1 Hz, about 2 % of pixels lit, no Terracotta.
- **Motion:** 180–240 ms ease-out. The compass rotates with heading at 30 fps and is damped (critically damped, τ = 120 ms).

| # | Screen | Purpose |
|---|---|---|
| 01 | Home / compass | Time, street name, heading ring with POI ticks, next interesting thing |
| 02 | Now narrating | Title, L/R/ahead indicator, progress, source chip |
| 03 | Nearby | Sweep list sorted clockwise with direction arrows and distance |
| 04 | Navigation | Big arrow, distance to turn, street, ETA |
| 05 | Listening | Push-to-talk waveform + transcript |
| 06 | Answer card | Short answer + "tell me more" |
| 07 | Dinner picks | 3 restaurants, open-now, walk minutes, book |
| 08 | SOS countdown | Full red, 5-4-3-2-1, cancel hint |
| 09 | SOS live | Contacts notified, sharing, satellite state (Atlas) |
| 10 | Walk Me Home | Route progress, ETA shared, next check-in |
| 11 | Battery & modes | %, time-left estimate, Normal / Saver / Ultra |
| 12 | Nightstand | Docked clock + tomorrow |
| 13 | City Pack download | Progress, size, Wi-Fi only |
| 14 | Settings | Quiet, voice, story length, interests, rotate 180° |
| 15 | Offline state | Home with an offline chip and capability list |

## 9. Companion app (iOS/Android, 390 × 844 pt reference)

Screens are in `app-screens/png/`; the contact sheet is `app-screens/contact-sheet.png`. Navigation has 4 tabs: **Today · Map · Packs · You**.

| # | Screen |
|---|---|
| 01 | Welcome (brand moment) |
| 02 | Pairing (device found, hold Talk to confirm) |
| 03 | Interests profile (tap chips + depth slider) |
| 04 | Safety contacts + Walk Me Home defaults |
| 05 | City Pack store |
| 06 | City Pack detail (Rome) |
| 07 | Today / day recap (timeline of stories, distance, saved places) |
| 08 | Story detail (transcript + sources + "listen again") |
| 09 | Map (walked route, story pins, offline area outline) |
| 10 | Dinner / booking flow |
| 11 | Subscription (LORE Pass: Free / Explorer / Trip Pass) |
| 12 | Device settings and battery |

The onboarding target is **first story heard in under 4 min from box open** (§11).

## 10. Online / offline states

| Capability | Online (LTE/Wi-Fi/phone) | Offline with City Pack | Offline, no pack |
|---|---|---|---|
| Stories | full + live LLM depth | full pack stories (pre-verified) + on-device "tell me more" from pack facts (Square/Atlas). Pebble plays pre-generated stories only (D10) | "Basic narration": street and landmark names only from OSM-lite base map |
| Q&A | cloud + on-device | on-device model over pack facts. Out-of-scope questions are queued ("I'll answer when we're back online") | queued |
| Navigation | live (closures, transit) | full offline routing (pack graph) | compass + straight-line distance to saved places |
| Food | live hours, reviews, booking | pack list with hours as of the pack date (shown) | none |
| Safety | full | SOS via voice/SMS on any network. Atlas satellite. Walk Me Home with check-ins (SMS) | same |
| UI cue | none | Fog "OFFLINE" chip, `offline` earcon once | chip + one spoken line on the first offline minute |

Transitions are announced at most once per 10 min. LORE never says "error", "failed" or "no connection" aloud; it says "I'm working from the Rome pack for a bit".

## 11. Onboarding flow (unbox → first story)

1. Open the box: the device is already at 60 % and wakes when lifted (IMU). The ring says hello (signature motif, slow Terracotta sweep).
2. The screen or the voice says "Hi, I'm Lore. Get the app at lore.travel/start". A QR code shows on Square/Atlas; the card in the box carries it for Pebble.
3. App: create account (Apple/Google/email) → pair (BLE, "hold Talk to confirm") → choose up to 5 interests → add 1 safety contact (skippable, re-prompted on the first night walk) → connect earphones (the device lists bonded BT devices) → download the Rome pack on Wi-Fi (1.2 GB, about 3 min at 50 Mbps).
4. Tutorial walk (60 s): "Press the button once." → "Now double-press to see what's around." → a first story about the nearest landmark, even at home ("You're 2,400 km from the Colosseum, so here's the opening line of its story").
5. Explorer trial: 3 months are activated. eSIM activation is silent on Square/Atlas.

## 12. Battery-saving modes

| Mode | What changes | Est. impact (from hardware/ simulation) |
|---|---|---|
| **Normal** | GNSS L1+L5 with duty-cycling + PDR, AOD on, cloud depth on | Square ~2 days, Atlas ~2.4 days (simulated, D12) |
| **Saver** (auto at 20 %) | AOD off, L1 only, screen max 300 nits, story cooldown ×1.5, LTE PSM between requests | +30 % (E) |
| **Ultra** (auto at 8 %, or manual) | Screen shows the clock only, no unprompted stories, nav + safety only, GNSS every 10 s with PDR | +3× remaining (E) |
| **Safety reserve** | The last 3 % is reserved for SOS + Walk Me Home. The device turns off other features rather than dying | — |

## 13. Accessibility

- **Blind and low-vision (2028 accessibility version, partly in v1):**
  - Every screen element has a spoken equivalent ("Battery?", "Where am I?").
  - Haptic turn patterns on navigation.
  - "Detailed mode" describes crossings, kerbs and entrances from map data.
  - **No safety-critical guidance depends on the screen.**
- **Hearing:**
  - Captions on the screen and in the app for every story.
  - Haptic earcon equivalents.
  - Hearing-aid streaming via LE Audio / ASHA (Android) and MFi (iOS, via phone).
- **Motor:**
  - Talk is large (Pebble dish ~23 mm; Square key 11 mm).
  - Press timings are adjustable (×1.5 / ×2).
  - The 5-press SOS alternative helps users who cannot sustain a hold.
- **Cognitive:** "Simple mode" with one button only: press = story, hold = talk. Shorter stories.
- **Contrast:** text contrast ≥ 7:1 on black (Bone on black ≈ 18:1); Fog on black ≈ 7.6:1 is the minimum used for text.
- **Languages:** UI in EN at launch, then IT, ES, FR, DE, JA.

## 14. Privacy UX

- Microphone: push-to-talk by default. The VAD for "quiet moments" runs on-device and stores no audio.
- Camera (Atlas): only on explicit "What is this?" with a raised device. Privacy LED. Frames are processed on-device and discarded; the app log shows "1 photo analysed, not stored".
- Location history stays on the device and the phone. The day recap is end-to-end encrypted when synced. "Forget today" is one tap.
