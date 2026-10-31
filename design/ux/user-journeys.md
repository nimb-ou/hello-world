# LORE user journeys

**Rev:** EVT-0 · 2026-10-31. These are illustrative design scenarios: the persona is composite (built from the research/ persona brief) and the times are **design targets**, not measurements. Screen references point to `device-screens/png/NN-*.png` (D-NN) and `app-screens/png/NN-*.png` (A-NN).

**Persona: Maya, 31**, product designer from Toronto. Solo trip to Rome for 5 days, LORE Square (Sand) with Explorer trial. She uses her own AirPods Pro (LE Audio capable via phone, A2DP direct to LORE).

---

## J1. Unboxing → first walk in Rome

| # | Time | Moment | Maya does / feels | LORE does | Touchpoints |
|---|---|---|---|---|---|
| 1 | Day −3, 19:00 | Box opened at home | Lifts the device out of the box; it is warm grey, cool metal | Wakes on lift (IMU), plays the signature motif quietly through the speaker, screen shows *"Hi. I'm Lore."* + QR | Packaging (brand/), D-01 variant |
| 2 | +0:40 | App install | Scans the QR | App opens on **Welcome** (A-01) | A-01 |
| 3 | +1:30 | Pairing | Taps "Pair", holds Talk when asked | BLE bond, eSIM activates silently, firmware is current | A-02 |
| 4 | +2:30 | Interests | Picks *Architecture, Food, Dark history, Art*; depth slider "Curious" | Builds the story-ranking profile | A-03 |
| 5 | +3:10 | Safety | Adds her sister as a safety contact | Saves; Walk Me Home defaults to "after 22:00, suggest" | A-04 |
| 6 | +3:40 | First story | Connects AirPods; taps "Try it" | Plays a 25 s "here at home" demo story, then *"Want the Rome pack? It's 1.2 GB, best on Wi-Fi."* | A-05/A-06, D-13 |
| 7 | Day 1, 10:05 | Lands at FCO | Phone in airplane mode; turns LORE on | eSIM attaches (TIM/Vodafone roaming profile). D-01 shows Rome time and weather. *"Benvenuta. The train to Termini is 32 minutes. Want me to tell you about the aqueduct you'll pass?"* | D-01 |
| 8 | 12:40 | First walk: Via dei Coronari | Clips LORE to her bag strap, walks, phone in pocket | Quiet-moments score rises near Piazza Navona; `story-start` earcon. *"On your left, the fountain's river god is covering his eyes. Legend says Bernini made him flinch at Borromini's church. It's a great story, and it's false: the fountain was finished first. Look up at the church's twin towers."* | D-02 (L indicator) |
| 9 | 12:42 | Depth | Says "Source?" | *"Two sources: the Fountain's 1651 completion record, and the church's 1653 start. Both are in the Rome pack."* | D-02 source chip |
| 10 | 12:50 | Around | Double-presses Talk | Sweep: *"Left, 60 m: Palazzo Pamphilj. Ahead, 180 m: the Pantheon. Right, 90 m: a 1938 gelateria locals argue about."* | D-03 |
| 11 | 13:05 | Navigate | "Take me to the Pantheon" | Brass arrow, `turn-right` earcon panned right at 30 m | D-04 |
| 12 | 18:30 | Evening | Opens the app | Day recap: 6.4 km, 11 stories, 3 saved places | A-07, A-08, A-09 |

**Success criteria:**
- First story in **under 4 min** from opening the box.
- Zero phone unlocks during the walk.
- Any story at most 40 s unless Maya asks for more.

**Pain points designed out:** roaming bill (eSIM included), phone theft risk (phone stays pocketed), looking down (L/R spatial language).

## J2. Lost signal (Trastevere backstreets → Janiculum)

| # | Moment | LORE behaviour |
|---|---|---|
| 1 | LTE drops in a narrow medieval street (multipath, basement-level sidewalk) | No interruption. The current story is from the pack. Fog "OFFLINE · ROME PACK" chip appears on D-15; the `offline` earcon plays once. **Nothing is said aloud** unless Maya asks for something that needs the network |
| 2 | GNSS degrades (urban canyon, HDOP > 5) | Map Vision switches to PDR (step + heading) snapped to the pack's street graph. If confidence drops below 70 %, stories switch to landmark-relative wording ("the doorway with the marble lion") |
| 3 | Maya asks "Is Da Enzo open now?" | *"Going by the Rome pack's 28 October hours, yes until 23:00. I'll check live hours when we're back online and tell you if that's changed."* (stale-data date is shown on D-07) |
| 4 | She asks a deep question outside the pack ("What did Garibaldi think of the Pope?") | Square/Atlas answer briefly with the on-device model, using pack facts only, then: *"I can go deeper online. Want me to save the question?"* The question is queued |
| 5 | Signal returns at the Janiculum terrace | `online` earcon. Queued answer: *"You asked about Garibaldi earlier: here's the longer version."* Only if the quiet-moments score allows |

**Principle:** offline is a mode, not an error. The word "error" is never spoken.

## J3. Late-night walk home (Monti → hotel near Termini, 23:40)

| # | Moment | LORE behaviour |
|---|---|---|
| 1 | Maya leaves a bar, slightly lost, battery 24 % | Time is after 22:00, she is alone (no recent conversation detected), and moving toward the saved hotel, so LORE offers once: *"Want me to walk you home? I'll keep Sara posted."* |
| 2 | Says "Yes" | D-10. Route goes via Via Nazionale (lit, open venues), not the shorter dark Via Panisperna side street. The ETA (14 min) is texted to Sara with a live link. A Brass heartbeat shows on the status bar |
| 3 | Companion mode | Every ~5 min a short, reassuring line: *"Two minutes to the main road. The pharmacy on the corner is open till 1."* The battery goes to Saver automatically (24 % → at least 6 h) |
| 4 | She stops at a shop for 6 min, off-route | `checkin` earcon + haptic: *"All good?"* She presses Talk; the timer resets |
| 5 | Someone follows her and she feels unsafe | Holds the SOS key 2 s → D-08 countdown (5 s) → D-09. Local 112 is dialled; Sara and a second contact get an SMS with live location. The narrator stays silent; the speaker stays off (discreet) |
| 6 | Alternative: she arrives normally | Within 30 m of the hotel, `arrive` plays and Sara gets "Maya arrived safely, 23:56". Sharing stops automatically |

**Design notes:**
- Check-ins use the earphones and haptics, never the speaker, so they stay discreet.
- The battery's safety reserve (last 3 %) guarantees SOS.
- On Atlas without LTE, SOS goes over satellite NTN, with "face-up, clear sky" coaching.

## J4. Finding dinner and booking (Day 2, 19:30, near Campo de' Fiori)

| # | Moment | LORE behaviour | Touchpoints |
|---|---|---|---|
| 1 | "Somewhere good for dinner. Not touristy, cacio e pepe, not too far." | Ranks venues by distance, open-now, cuisine, and a local-signal score (review language mix, menu prices, no photo menus). Excludes places she flagged | D-07 |
| 2 | Hears three picks | *"Three good ones. Closest: a trattoria 6 minutes left, around €16 for cacio e pepe, mostly Roman reviewers. Second: …"* | D-07 |
| 3 | "Book the first one for 8:15, one person" | Online only: books via a partner API (TheFork/OpenTable-class). Confirms by voice and puts a card on the phone. **Affiliate disclosure:** "LORE may earn a small fee" is shown in-app (A-10). Ranking is never affected by fees (editorial rule) | A-10 |
| 4 | Booking not possible (no partner) | *"They only take phone bookings. Want me to show the number on your phone, or call through your phone?"* | A-10 |
| 5 | Walk there | Navigation (D-04) with one optional story on the way (cooldown respected) | D-04, D-02 |
| 6 | At the table | Quiet: the device detects a stationary state indoors plus speech, so no stories. "How do I say *the bill, please*?" → *"Il conto, per favore."* spoken slowly, then at normal speed | — |

**Revenue touchpoint:** booking affiliate fees. The fairness rule is stated in the app and the ToS: ranking is computed before affiliate status is known.

---

## Cross-journey metrics (targets for EVT beta)

| Metric | Target |
|---|---|
| Time to first story | < 4 min |
| Phone unlocks per walking hour | < 1 |
| Stories skipped within 5 s | < 15 % |
| False SOS per 1,000 device-days | < 1 |
| "LORE talked at a bad moment" reports | < 1 per 5 walking hours |
