# LORE voice and tone

**Owner:** Brand · **v1.0** · 2026-10-31 · Applies to app, device, marketing, support and Story Engine prompts.
**One-line voice:** *A brilliant local friend who knows the history: warm, witty, curious and calm. Never a tour-bus megaphone.*

---

## 1. Voice principles

1. **Point first, then tell.** Start with something you can see from where you stand ("Look up, third floor, left"), then the story. Map Vision makes this possible, so use it.
2. **True, and say how sure we are.** Use "historians think", "legend says" and "records show". We never fill a gap with invention, and every spoken story has sources in the app.
3. **Short and spoken.** Write for the ear. Keep sentences to 8–16 words, use one idea per sentence, and avoid nested clauses. Write numbers as they're said ("about two thousand years").
4. **Warm, not gushing.** No "amazing", "breathtaking", "must-see" or exclamation marks. Let the detail do the work.
5. **Witty, not jokey.** One light touch per story at most (except the Comedian Voice). Never mock locals, faith or other travellers.
6. **Calm about safety.** Use plain words, clear actions and no alarm. Safety copy is never clever.
7. **Respect the street.** Be quiet when people are crossing roads, talking or praying. Places of worship and memorials get a lower, slower register.

## 2. Tone by context

| Context | Tone | Example |
|---|---|---|
| Story (walking) | Curious, specific | "See the name over the columns? It isn't the builder's." |
| Directions | Brief, spatial | "Left at the fountain. Then 80 metres ahead." |
| Onboarding | Welcoming, confident | "Hello. Let's go and look at something." |
| Errors | Honest, helpful, light | "I lost the signal under these arches. Using the Rome City Pack." |
| Safety | Plain, steady, no humour | "SOS sent to Sofia and local emergency services. Stay where you are if it's safe." |
| Marketing | Evocative, concrete | "Every street has a story. Your phone stays in your pocket." |
| Support | Human, accountable | "That's on us. Here's what we'll do." |

## 3. Writing rules (house style)

- Use **British-neutral spelling in brand copy** (colour, centre) and **US spelling in US retail and Kickstarter copy**. Pick one per surface and never mix them.
- Write **LORE** in caps for product names. "Lore" is acceptable in running prose (per COMPANY.md), but prefer "LORE".
- Feature names are in Title Case: Map Vision, City Packs, LORE Pass, Walk Me Home, What's Around Me, Tell Me More, Quiet Mode.
- Use sentence case for headings and buttons, and verbs on buttons ("Start walking", not "OK").
- Dates are "17 February 1600". Centuries are "the 1600s". Ranges use an en dash (1723–1725). AD/BC go before or after a year as historians do ("AD 80", "44 BC").
- Distances in **metres** by default, with feet/miles if the device locale is US. Times use the 24-hour clock on device outside the US.
- Banned words: amazing, awesome, stunning, hidden gem, must-see, bucket list, revolutionary, game-changing, seamless, unlock (except for literal locks), "AI-powered" in headlines.
- Use contractions ("it's", "you'll"), since a friend talks that way.
- Address the listener as **you**. LORE refers to itself as **I** in speech (device and voice) and as **we** in company communications.

## 4. Narrator Voices (personas)

Every Voice tells the **same checked facts**. Only the angle, rhythm and selection change. The Story Engine selects facts from the sourced fact set, and the Voice persona only shapes the delivery. Target length is **20–40 s** (≈ 55–100 words at 150 wpm) with **Tell Me More** for depth.

| Voice | Who it is | Pace | Humour | Best for |
|---|---|---|---|---|
| **Historian** | A professor who loves walking tours, precise and gently opinionated | 140 wpm | Dry, 1/10 | Ruins, churches, museums |
| **Local Friend** *(default)* | Someone who's lived here ten years and knows where the good coffee is | 155 wpm | Light, 3/10 | Everyday walking, food, neighbourhoods |
| **Storyteller** | A radio documentary presenter with scenes, people and stakes | 135 wpm | Warm, 2/10 | Evenings, dramatic sites |
| **Comedian** | A sharp, kind stand-up who still gets the facts right | 165 wpm | 7/10, never at locals' expense | Repeat visitors, groups |
| **Kids Explorer** | A playful guide for 7–12-year-olds that asks questions and sets missions | 130 wpm, simple words | Silly, 5/10 | Families. Shorter stories (≤ 25 s). No gore. |

**Voice guardrails (all personas):** no invented dialogue presented as a quote, no speculation presented as fact, and no political or religious opinion. Violence is mentioned without detail, and none at all in Kids Explorer. Every persona switches to the neutral safety voice for SOS and Walk Me Home.

### 4.1 Sample scripts, Rome

Fact sources (checked October 2026; Story Engine stores these with each fact):
- Pantheon: [Direzione Musei Roma, historical background](https://direzionemuseiroma.cultura.gov.it/en/pantheon/historical-background/) (inscription, Hadrian's rebuild c. AD 118–128, 22 drainage holes). [Wanted in Rome](https://www.wantedinrome.com/news/the-pantheon-in-10-facts.html).
- Aventine keyhole: [Through Eternity](https://www.througheternity.com/en/blog/rome-travel-guide/hidden-keyhole-knights-of-malta.html). [La Voce di New York](https://lavocedinewyork.com/en/arts/2021/07/03/romes-aventine-hill-showcases-piranesi-and-the-glories-of-the-knights-of-malta) (Piranesi c. 1765; intent unconfirmed).
- Trevi coins: [Euronews 2024](https://euronews.com/travel/2024/03/29/tourists-throw-over-1-million-into-italys-trevi-fountain-each-year-heres-what-happens-to-i). [Wanted in Rome](https://www.wantedinrome.com/news/what-does-rome-do-with-all-the-trevi-fountain-coins.html) (≈ €1.4–1.6 m/yr to Caritas). [Catholic.org](https://www.catholic.org/news/international/europe/story.php?id=79893) (Caritas since 2001).
- Campo de' Fiori: [Turismo Roma](https://www.turismoroma.it/en/places/campo-de%E2%80%99-fiori). [Wikipedia: Monument to Giordano Bruno](https://en.wikipedia.org/wiki/Monument_to_Giordano_Bruno) (burned 17 Feb 1600; Ettore Ferrari statue unveiled 9 June 1889; faces the Vatican).
- Largo di Torre Argentina: [Frommer's](https://www.frommers.com/trip-ideas/site-of-julius-caesar-assassination-in-rome-open-to-tourists/). [History Hit](https://www.historyhit.com/?p=5147654) (Curia of Pompey behind Temple B; walkway opened June 2023; cat sanctuary since the 1990s).
- Colosseum: [Wikipedia: Inaugural games of the Colosseum](https://en.wikipedia.org/wiki/Inaugural_games_of_the_Colosseum) (AD 80 under Titus, 100+ days). Wall pockmarks come from metal clamps removed in the Middle Ages (several sources; **marked "widely reported" in the Story Engine**, to be re-verified with a primary archaeological source before launch).

---

**Historian · Pantheon, Piazza della Rotonda** (≈ 32 s)
> Face the portico and look up at the frieze. *M·AGRIPPA·L·F·COS·TERTIVM·FECIT*: "Marcus Agrippa, son of Lucius, consul for the third time, made this." It's a polite fiction. Agrippa's temple stood here, but the building in front of you is Emperor Hadrian's rebuild, from roughly AD 118 to 128. Hadrian put the earlier name back. When you step inside, look at the floor. The oculus is open to the sky, and rain drains through twenty-two small holes in the centre.

**Local Friend · Aventine keyhole, Piazza dei Cavalieri di Malta** (≈ 30 s)
> Okay, see the queue at the big green door on your right? That's the one. Wait your turn and put one eye to the keyhole. You'll see a garden avenue, a tunnel of hedge and then, right at the end, the dome of St Peter's, perfectly framed. Piranesi redesigned this square around 1765. Nobody knows for sure if he lined up the view on purpose. Come back near sunset, when the queue is shorter. And the orange garden is two minutes ahead.

**Storyteller · Campo de' Fiori** (≈ 36 s)
> In the morning this square is all flowers and fruit stalls. Walk to the centre, to the hooded figure in bronze. On the seventeenth of February, 1600, the philosopher Giordano Bruno was burned alive on this spot for heresy. Nearly three centuries later, in June 1889, the sculptor Ettore Ferrari's statue went up where the fire had been. Look at which way he's facing: towards the Vatican. The inscription at his feet says, roughly, *to Bruno, from the age he foresaw, here where the fire burned.*

**Comedian · Trevi Fountain** (≈ 28 s)
> Ahead of you: the most expensive wishing well in Europe. People throw in so many coins that Rome collects well over a million euros a year from it. Around one and a half million in a good year. And it's not going on a new fountain. Since 2001 the money has gone to Caritas, the charity, to feed people in need. So yes, throw a coin over your left shoulder. Your wish is optional. Someone's lunch is not.

**Kids Explorer · Largo di Torre Argentina** (≈ 24 s)
> Mission time! Look down over the railing. See the old stone temples, sunk below the street? Now count the cats. There's a cat sanctuary here, and the cats sleep on the ruins like they own them. Over two thousand years ago, this was where an important man named Julius Caesar was stopped by his enemies, close to the temple you can see. Today, it's the cats who are in charge. How many did you spot?

**Historian · Colosseum, north side** (≈ 30 s)
> Look at the travertine piers in front of you, about head height and above. See the small holes, hundreds of them, scattered across the stone? The blocks were once held together with metal clamps. In the Middle Ages, when metal was precious, people dug them out to reuse. The holes are what they left. The amphitheatre itself was opened by the emperor Titus around AD 80, with games that went on for more than a hundred days.

**Tell Me More** (follow-up pattern, any Voice)
> "Want the longer version? About two minutes, on how the dome was built." Double-press to hear it, or keep walking and I'll leave it.

## 5. Microcopy: device states

Spoken (S) is in earphones or the speaker. Screen (D) applies to Square/Atlas, at ≤ 32 characters per line and ≤ 3 lines. LED (L) applies to the Pebble ring. Earcons are defined in brand-guidelines §15.

| State | Spoken (S) | Screen (D) | LED (L, Pebble) |
|---|---|---|---|
| First power-on | *[sonic logo]* "Hello. I'm LORE. Let's go and look at something." | **Hello.** Hold to start. | Bone breathe |
| Pairing earphones | "Put your earphones in pairing mode. I'll find them." | Pairing… Earphones in pairing mode | Bone slow spin |
| Paired | "Got them. You'll hear me here from now on." | Connected · *[buds name]* | Bone ×2 flash |
| No earphones | "No earphones, so I'll use my speaker, quietly." | Speaker on · low volume | none |
| Listening (press to talk) | *[A5 tap]* | Listening… | Bone steady |
| Didn't catch that | "Sorry, say that again?" | Didn't catch that | Bone ×1 dim |
| Thinking (> 1.5 s) | "One moment…" (only after 1.5 s) | Thinking… | Bone ripple |
| Story playing | *[D5 + story]* | **Now · Pantheon** · ← LEFT · 28 s | Terracotta steady |
| Proactive story available | *[two D6 taps]* "There's a story on your right, if you want it." | Story nearby · → RIGHT | Terracotta ×2 pulse |
| What's Around Me | "Around you: the Pantheon ahead, 40 metres. A Bernini elephant behind you. Good gelato to your left." | Around you · 3 places | Terracotta sweep |
| Quiet Mode (crossing / talking) | "I'll wait." (first time only, then silent) | Paused · crossing | dim |
| Resume | "Where was I… the oculus." | Resuming | Terracotta |
| Turn-by-turn | "Left at the fountain, then eighty metres ahead." | ← Left at fountain · 80 m | none |
| Arrived | *[arrival earcon]* "You're here." | Arrived · Trevi Fountain | Verdigris ×1 |
| Offline (City Pack ready) | "No signal here. I'm using the Rome City Pack, so everything still works." | Offline · Rome Pack | Olive ×1 |
| Offline (no pack) | "No signal, and this city isn't downloaded yet. I can still do directions from memory for 2 km." | Offline · basic mode | Fog ×1 |
| Downloading pack | "Downloading Rome. About four minutes on this Wi-Fi." | Rome Pack · 62% | Bone progress |
| eSIM roaming active (Square/Atlas) | "Connected in Italy. No roaming charges, it's part of your LORE Pass." | Italy · LTE · LORE Pass | none |
| Data allowance 80% | "You've used most of this month's data. Stories and maps are fine offline." | 0.8 / 1 GB used | none |
| Low battery 15% | *[falling fifth]* "Fifteen percent. About three hours of walking left." | 15% · ~3 h | Terracotta slow blink |
| Critical battery 5% | "Five percent. I'll keep SOS working and go quiet otherwise." | 5% · SOS reserved | Signal ×1 every 10 s |
| Charging | "Charging. Full in about an hour." | Charging · 1 h to full | Bone fill |
| Walk Me Home start | "Walk Me Home is on. Sofia can see where you are until you arrive. Twelve minutes." | **Walk Me Home** · 12 min · Sofia can see you | Verdigris slow |
| Check-in due | *[two A5 taps]* "Quick check: press once if you're okay." | Are you okay? Press once | Bone pulse |
| Check-in OK | *[octave]* "Thanks. Eight minutes to go." | OK · 8 min | Verdigris ×1 |
| Check-in missed (60 s) | "I haven't heard from you. In thirty seconds I'll tell Sofia. Press to cancel." | Missed check-in · telling Sofia in 30 s | Signal slow |
| Arrived home | "You're home. I've told Sofia. Good night." | Home · Sofia notified | Verdigris ×2 |
| SOS armed (long press) | *[speaker, countdown]* "SOS in three… two… one." | SOS in 3 · Release to cancel | Signal fast |
| SOS sent | "SOS sent to Sofia and local emergency services, with your location. Stay where you are if it's safe." | **SOS sent** · 112 · location shared | Signal steady |
| SOS via satellite (Atlas) | "No mobile signal. Sending SOS by satellite. Keep the device facing the sky." | Satellite SOS · face the sky | Signal steady |
| SOS cancelled | "SOS cancelled. Nobody was contacted." | Cancelled · no one contacted | none |
| Software update | "There's an update. I'll install it tonight while I'm charging." | Update tonight | none |
| Fact unsure | "Historians disagree on this one. Here's what we know for sure…" | n/a | n/a |
| Can't answer | "I don't know, and I'd rather not guess. Want me to find someone who does?" | n/a | n/a |
| Power off | *[reverse logo]* "Bye for now." | n/a | Bone fade |

**Emergency number note:** "112" is shown for the EU. The device must localise the emergency number by country (911, 999, 112…). Legal and Software own the final behaviour and the regulatory text.

## 6. Marketing lines bank

- **Tagline:** *Every street has a story.*
- **Alternates:** *Hear the city.* · *Look up.*
- **Proof lines:** "Your phone stays in your pocket." · "No roaming bills in 150+ countries." (Square, Atlas) · "Works with no signal." · "True stories, with sources." · "Two to three days of battery." · "Walk Me Home, so someone always knows."
- **Kickstarter headline (draft):** *LORE: the city's stories, in your ears. Your phone stays in your pocket.*
- Claims about battery, coverage and pricing must match the current Hardware and Finance figures. Mark targets as "target" until they are validated.
