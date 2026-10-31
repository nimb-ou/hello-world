#!/usr/bin/env python3
"""Build LORE's 90-day social content calendar (Mon 2 Nov 2026 -> Sat 30 Jan 2027).

Run:  python3 gtm/social-media/tools/build_calendar.py
Out:  gtm/social-media/content-calendar-90d.csv

Every "Secrets of Rome" / "Look up" fact is flagged VERIFY: it must be checked
against the Rome City Pack fact cards (with source) before posting. The bank below
uses well-documented Roman facts, but the Story team has final say.
"""
import csv, datetime as dt, itertools, os

START = dt.date(2026, 11, 2)
DAYS = 90
OUT = os.path.join(os.path.dirname(__file__), "..", "content-calendar-90d.csv")

WAITLIST = "lore.travel"
# (topic, hook, body, source_hint)
SECRETS = [
 ("Aventine Keyhole", "There's a keyhole in Rome where people say you can see three states at once.",
  "On the Aventine Hill, the door of the Knights of Malta's villa has a keyhole. Look through it and St Peter's dome sits perfectly framed at the end of a garden avenue: the Order of Malta's property, Italy, and the Vatican in one view.", "Sovereign Military Order of Malta / Piranesi-designed piazza"),
 ("Colosseum holes", "Why is the Colosseum covered in holes?",
  "Not bullets. Not decay. In the Middle Ages people dug out the iron clamps that held the stone blocks together, and metal was valuable. The holes are the scars.", "Parco archeologico del Colosseo"),
 ("Piazza Navona stadium", "Piazza Navona is shaped like a running track because it was one.",
  "The square follows the outline of the Stadium of Domitian (1st century AD). The buildings sit on its seating. You can visit the ruins underneath.", "Stadio di Domiziano museum"),
 ("Pantheon rain", "Yes, it rains inside the Pantheon.",
  "The oculus is open to the sky, about 9 m across. The floor is slightly convex and has small drain holes so rainwater runs away.", "Pantheon / MiC"),
 ("Monte Testaccio", "This hill in Rome is made of broken pots.",
  "Monte Testaccio is an artificial hill built from millions of discarded amphorae, mostly olive-oil jars, from the ancient river port nearby.", "Sovrintendenza Capitolina"),
 ("Bocca della Verità", "The 'Mouth of Truth' was probably a drain cover.",
  "The famous marble face at Santa Maria in Cosmedin is thought to have been an ancient drain cover or fountain mask. The hand-biting legend came much later.", "Santa Maria in Cosmedin"),
 ("Pasquino", "Rome has a statue that's been posting anonymous insults since the 1500s.",
  "Pasquino, a battered statue near Piazza Navona, is a 'talking statue'. Romans stuck satirical poems on it to mock the powerful. People still do.", "Sovrintendenza Capitolina"),
 ("Nasoni", "Every Roman knows this water-fountain trick. Most tourists don't.",
  "The iron 'nasoni' fountains have a hole on top of the spout. Block the bottom with your finger and the water arcs up for you to drink.", "Acea / Roma Capitale"),
 ("Trevi coins", "Where do the Trevi Fountain coins go?",
  "They're collected and given to charity. Caritas Roma uses them for its programmes. Toss with your right hand over your left shoulder.", "Caritas Roma"),
 ("Acqua Vergine", "The Trevi Fountain still runs on an aqueduct from 19 BC.",
  "The Aqua Virgo, built under Agrippa, still feeds the Trevi and several fountains in the centre.", "Sovrintendenza Capitolina"),
 ("Giordano Bruno", "This statue is staring at the Vatican on purpose.",
  "Campo de' Fiori's hooded statue is Giordano Bruno, burned here for heresy in 1600. The 1889 monument faces the Vatican.", "Roma Capitale"),
 ("Torre Argentina cats", "Julius Caesar was killed about here. Now it's a cat sanctuary.",
  "Largo di Torre Argentina holds remains of the Curia of Pompey, where Caesar was assassinated in 44 BC, and a long-running cat colony.", "Sovrintendenza Capitolina"),
 ("Sant'Ignazio dome", "This dome isn't there.",
  "Inside Sant'Ignazio, the 'dome' is a flat painted canvas by Andrea Pozzo. Stand on the marked disc in the floor and the illusion snaps into place.", "Chiesa di Sant'Ignazio"),
 ("Palazzo Spada", "This 'long' colonnade is under 9 metres.",
  "Borromini's forced-perspective gallery in Palazzo Spada looks about 35 m long. It's actually about 8 m, and the statue at the end is small.", "Galleria Spada / MiC"),
 ("Pyramid of Cestius", "Rome has a pyramid. A real one.",
  "The Pyramid of Cestius, a tomb from around 12 BC, survived because it was built into the Aurelian Walls.", "Sovrintendenza / MiC"),
 ("Ponte Sant'Angelo", "Rome's most beautiful bridge used to be its execution site.",
  "Executions were held near Ponte Sant'Angelo. Beatrice Cenci was beheaded there in 1599, and locals say she returns every 10 September.", "Archivio di Stato di Roma (legend flagged)"),
 ("Quattro Fontane", "Stand here and you can see three obelisks.",
  "At the Quattro Fontane crossroads, four corner fountains face each other, and the long straight streets show obelisks in several directions.", "Roma Capitale"),
 ("Sampietrini", "These cobblestones are named after a saint.",
  "Rome's black basalt cobbles are 'sampietrini', little St Peters, after the square where they were laid.", "Roma Capitale"),
 ("Spanish Steps", "The Spanish Steps were paid for by the French.",
  "Funded by a bequest from French diplomat Étienne Gueffier and finished in 1725, they link the Spanish embassy below to the French church above.", "Trinità dei Monti"),
 ("Marcus Aurelius", "This statue survived because of a case of mistaken identity.",
  "Most ancient bronze statues were melted down. Marcus Aurelius on horseback survived because people thought he was Constantine, the first Christian emperor.", "Musei Capitolini"),
 ("Teatro di Marcello", "People live on top of a 2,000-year-old theatre.",
  "The Theatre of Marcellus became a fortress and then a palazzo. There are still apartments in its upper floors.", "Sovrintendenza Capitolina"),
 ("Tiber Island", "The island in the Tiber is shaped like a ship. On purpose?",
  "Isola Tiberina was faced with travertine to look like a ship's prow and has hosted healing sites for centuries. A hospital still runs there today.", "Sovrintendenza / Ospedale Fatebenefratelli"),
 ("Trajan's Column", "There's a saint on top of an emperor's column.",
  "Trajan's statue on top was lost. In 1588 Pope Sixtus V put St Peter up there instead.", "Mercati di Traiano"),
 ("Obelisks", "Rome has more ancient Egyptian obelisks than Egypt.",
  "There are 13 ancient obelisks in Rome, brought by emperors as trophies and later re-erected by popes.", "Roma Capitale (count to verify)"),
 ("SPQR manholes", "Look down: Rome still signs its drains like an empire.",
  "SPQR, Senatus Populusque Romanus, is stamped on manhole covers, buses and bins across the city.", "Roma Capitale"),
 ("Elephant obelisk", "Bernini's elephant might be mooning a monastery.",
  "Legend says the elephant in Piazza della Minerva turns its backside towards the Dominican friars who criticised the design. Legend, not record.", "Legend (flag as legend)"),
 ("Navona lake", "Piazza Navona used to be flooded on purpose.",
  "From the 17th to the 19th century the square was flooded on August weekends, and carriages splashed through the 'Lake of Piazza Navona'.", "Museo di Roma"),
 ("Via Margutta", "This quiet street is where Gregory Peck 'lived' in Roman Holiday.",
  "Via Margutta has been the artists' street for centuries, and Joe Bradley's apartment in Roman Holiday (1953) was filmed at no. 51.", "Film history"),
 ("Madonnelle", "Rome's first street lights were saints.",
  "Small shrines called 'madonnelle' on street corners often had lamps lit at night, so they doubled as street lighting.", "Roma Capitale (verify)"),
 ("Four Rivers myth", "The most famous Bernini rivalry story is probably false.",
  "The legend: the Nile statue covers its eyes to avoid seeing Borromini's church. But the fountain (1651) was finished before the church façade. Nice story, wrong dates.", "Myth-bust (verify dates)"),
 ("Mamertine", "Rome's oldest prison is under a church.",
  "The Mamertine Prison (Carcer Tullianum) by the Forum held Rome's enemies. Tradition says St Peter was held here.", "Parco archeologico del Colosseo"),
 ("Arancio", "Rome's orange garden smells like the Middle Ages.",
  "The Giardino degli Aranci on the Aventine recalls the orange tree that tradition says St Dominic planted at Santa Sabina.", "Santa Sabina (tradition)"),
 ("Portico d'Ottavia", "A 2,000-year-old portico is the gate of the Jewish Ghetto.",
  "The Porticus Octaviae became a fish market in the Middle Ages. A plaque still claims fish heads above a certain length for the city officials.", "Sovrintendenza Capitolina"),
 ("Cloaca Maxima", "Rome's ancient sewer is still working.",
  "The Cloaca Maxima, begun around the 6th century BC, still carries some of the city's water to the Tiber.", "Sovrintendenza (verify extent)"),
 ("Facchino", "This little fountain-man is complaining about his job.",
  "Il Facchino on Via Lata is one of Rome's six 'talking statues': a porter with a barrel, and probably the city's grumpiest worker.", "Roma Capitale"),
 ("Holy Door", "St Peter's has a door that's bricked up most of the time.",
  "The Holy Door is opened only in Jubilee years. It opened for the 2025 Jubilee and was sealed again in January 2026.", "Vatican"),
]
LOOKUP = [
 ("Sant'Ignazio ceiling", "Look up: this whole ceiling is a lie.", "Andrea Pozzo painted architecture onto a flat vault. Find the floor marker and it 'opens'."),
 ("Pantheon oculus", "Look up: the only light in the Pantheon is a hole.", "About 9 m wide and nearly 1,900 years old, the oculus crowns what is still the world's largest unreinforced concrete dome."),
 ("Palazzo Farnese", "Look up at night: you can see Carracci's ceiling from the street.", "On some evenings the windows of Palazzo Farnese (French Embassy) are lit, and you can glimpse painted ceilings from Piazza Farnese."),
 ("Altane", "Look up: Rome's secret rooftop terraces.", "'Altane' and loggias crown old palazzi. Rome's best views belong to people who hang laundry."),
 ("Trevi details", "Look up above the Trevi: the bees.", "Look for symbols of papal families on Rome's fountains and façades: Barberini bees, Chigi mountains and stars."),
 ("Palazzo Altemps", "Look up: the painted loggia.", "Roman palazzi hide painted loggias you can only see from the courtyard. Look up as soon as you step in."),
 ("Shrines", "Look up at the corner: a Madonna has been watching this street for 300 years.", "Rome has hundreds of corner shrines. Look up at intersections in the centro storico."),
 ("Coats of arms", "Look up: every keystone tells you who paid.", "Papal coats of arms on gates and buildings date the work: keys, tiara, family symbol."),
 ("Domes skyline", "Look up from the Gianicolo: count the domes.", "From the Janiculum terrace you can pick out St Peter's, Sant'Andrea della Valle and the Pantheon."),
 ("Bricked windows", "Look up: why are so many Roman windows painted on?", "Trompe-l'œil windows keep façades symmetrical where real windows couldn't go."),
 ("Pigna", "Look up: a giant bronze pine cone.", "The 'Pigna' in the Vatican's Cortile della Pigna gave its name to a Roman district (Rione Pigna)."),
 ("Clock of Borromini", "Look up: a clock tower with a single hand?", "Old Roman clocks often showed 6 hours, not 12: 'Italian hours' counted from sunset."),
 ("Santa Maria in Trastevere", "Look up at the mosaic: 12th-century gold at night.", "The façade mosaics of Santa Maria in Trastevere are lit after dark and shimmer over the piazza."),
 ("Sundial line", "Look down for once: there's a sun line in this church.", "Santa Maria degli Angeli has a meridian line (1702) where sunlight marks solar noon on the floor."),
 ("Aventine skyline", "Look up from the Giardino degli Aranci at sunset.", "The best free view of Rome's domes, and the light hits the Tiber at golden hour."),
]
SOLO = [
 ("First-night routine", "My first-night routine in any new city (solo).", "1) Walk the route from my stay to the nearest main square in daylight. 2) Save the address offline in the local language. 3) Share live location with one person until I'm in for the night."),
 ("Phone in pocket", "The #1 pickpocket target is the phone in your hand.", "Crowded buses, metro doors and photo spots are where phone snatches happen. Keep your phone away when you don't need it: use a crossbody bag and a strap."),
 ("Fake petition", "If someone hands you a petition at a landmark, say no.", "A common distraction scam in major European cities. Polite, firm 'no, grazie' and keep walking."),
 ("112", "Save this number before you land in Europe: 112.", "112 is the EU-wide emergency number. It works from any phone, free."),
 ("Walk me home", "Ask a friend to 'walk you home' from 1,000 km away.", "Before a late walk, set a check-in time and share live location. If you don't check in, they know to call. (LORE's walk-me-home does this automatically.)"),
 ("Taxi", "How to get a legit taxi in Rome.", "Official white taxis with the Roma Capitale sign at ranks, or use an official app. There are fixed fares from Fiumicino to inside the Aurelian Walls (check the current rate)."),
 ("Look confident", "The trick to not looking lost: stop to check the map in a shop doorway.", "Step aside, check, then walk with purpose. Better still, have directions in your ear."),
 ("Battery", "The real solo-travel emergency is 4% battery.", "Your phone holds your ticket, map, payment and contacts. Protect its battery: offload maps and audio to another device, and carry a power puck."),
 ("Copies", "Do this with your passport before any trip.", "A photo in an offline folder, a copy in your email, and the original in a zipped inside pocket, not in your back pocket."),
 ("Accommodation", "How I pick solo-safe accommodation.", "Recent reviews mentioning 'solo', a staffed 24h desk or an easy self-check-in, a street with evening foot traffic, and less than 10 min to transit."),
 ("Night walks", "Rome after dark: where I love to walk (and how).", "Lit, busy streets: Via del Corso area, Trastevere's main lanes, Piazza Navona. Keep to the people, earbuds at low volume or open-ear."),
 ("Open-ear", "Why I switched to open-ear headphones in cities.", "You still hear scooters, bikes and people. Awareness is a safety feature."),
 ("Roaming", "Roaming is a safety issue, not just a cost.", "No data = no map, no ride app, no translation. Sort data before you land: eSIM or a device with data built in."),
 ("Trust your gut", "Solo-travel rule I never break: leave early.", "If a place feels off, you don't owe anyone an explanation. Walk towards light and people."),
 ("Emergency card", "The tiny card in my wallet on every trip.", "Name, blood type, allergies, emergency contact, accommodation address in the local language."),
]
BUILD = [
 ("Why a device", "Why we're building a device and not just an app.", "Phones are bad at three things travellers need: affordable global data, all-day battery, and staying out of sight in crowds. So: a pebble that clips to your bag."),
 ("Map Vision", "How do you know what's on someone's left without a camera?", "Dual-band GNSS (L1+L5), a 9-axis IMU and compass, step detection, and building footprints. We call it Map Vision."),
 ("Fact cards", "Our AI isn't allowed to invent history. Here's how.", "Every story comes from fact cards our team checks, each with a source. The AI tells the story, and it can't make up the facts."),
 ("Rome pack", "Building the Rome City Pack: [N] places so far.", "Target: 300+ places, 1,000+ fact cards, 100% sourced. Today's progress, plus one card that surprised us."),
 ("Walk test", "We took the prototype on a 3-hour walk in Rome. What broke.", "Honest notes from a walking test: what worked, what didn't (narrow streets!), and what we change next."),
 ("Prototype", "This is what LORE looks like right now (it's a phone).", "Stage 0: a phone-app prototype with simulation mode. The hardware comes in Q1 2027. Building in public means showing the ugly parts."),
 ("Names", "Pebble, Square or Atlas: which one would you carry?", "Pebble clips on, Square has a screen and global data, Atlas is titanium with a camera. Vote below."),
 ("Survey", "We need 500 travellers to tell us what we're getting wrong.", "5-minute survey: lore.travel/survey. Every answer is read."),
 ("Design", "Why our device has a button and not a touchscreen.", "Press to talk. Double-press: what's around me. Long-press: SOS. You can use it without looking."),
 ("Battery", "Designing for 2 days of battery: the trade-offs.", "Screen off by default, low-power GNSS duty cycling, on-device models for short tasks. Every milliwatt matters."),
 ("Quiet", "We taught our prototype to shut up at crossings.", "Map geometry + movement = 'you're crossing a road'. The story pauses. Small feature, huge for safety."),
 ("Waitlist", "Waitlist update: [N] walkers in [N] countries.", "Thank you. The next milestone is a beta in Rome in Feb–Apr 2027. Join at lore.travel."),
 ("Sources", "Show your sources: what a LORE fact card looks like.", "Claim, date, place, source, confidence, reviewer. That's the standard behind every 30-second story."),
 ("Hiring", "We're hiring: firmware lead, ML/voice engineer, content lead.", "Help us make every walk feel like walking with a local friend. Details at lore.travel/jobs."),
 ("Mistake", "We got a fact wrong in testing. Here's what we changed.", "A tester spotted a date error. We traced it to a secondary source, swapped it for a primary one, and added a second reviewer."),
 ("Voice", "Choosing LORE's voice was harder than choosing its shape.", "Warm, curious, calm, never a tour-bus megaphone. We tested [N] voices with walkers."),
 ("Kickstarter", "We're launching on Kickstarter in 2027. Here's why.", "We want our first customers to shape the product, and we want to prove demand before building 5,000 units."),
 ("Offline", "Can an AI guide work with zero signal? Ours has to.", "City Packs bundle maps, routes, stories and a small on-device model, for stone churches, metro tunnels and roaming-free trips."),
]

HASH = {
 "Secrets of Rome": ["#Rome", "#SecretsOfRome", "#RomeTravel", "#HiddenRome", "#TravelTips"],
 "Look up": ["#LookUp", "#Rome", "#Architecture", "#RomeItaly", "#LookUpChallenge"],
 "Solo safe": ["#SoloTravel", "#SoloFemaleTravel", "#TravelSafety", "#SoloTravelTips", "#Rome"],
 "Build in public": ["#BuildInPublic", "#Hardware", "#TravelTech", "#Startup", "#Kickstarter"],
}

# Seasonal / milestone overrides (date -> (pillar, hook, body, cta))
SPECIAL = {
 dt.date(2026,11,2): ("Build in public", "Day 1: We're building LORE, a pocket guide that tells you the story of every street.", "Follow along as we build it in public, starting with Rome. Join the waitlist at lore.travel.", "Join the waitlist"),
 dt.date(2026,11,26): ("Solo safe", "Travelling over Thanksgiving? Three things to sort before you fly.", "Offline maps, data plan, a shared itinerary with one person. Safe travels.", "Save this"),
 dt.date(2026,11,27): ("Build in public", "No Black Friday deal. Just a story.", "We don't have anything to sell yet. Here's a free story about Rome instead. (Waitlist members get the best Kickstarter price.)", "Join the waitlist"),
 dt.date(2026,12,8): ("Secrets of Rome", "Why does a firefighter climb a column in Rome every 8 December?", "On the Feast of the Immaculate Conception, Rome's firefighters place a wreath on the Madonna atop the Column of the Immaculate Conception near Piazza di Spagna, a tradition linked to the column's 1857 erection by firemen.", "Follow for more"),
 dt.date(2026,12,24): ("Look up", "Christmas Eve in Rome: look up at the Piazza San Pietro tree.", "The Vatican's Christmas tree and nativity scene go up in St Peter's Square each December. Buon Natale.", "Share with someone in Rome"),
 dt.date(2026,12,31): ("Secrets of Rome", "Romans used to throw old stuff out of the window at New Year.", "The old Capodanno custom of tossing old things out of windows to start fresh is now mostly retired. Please don't.", "Follow for 2027 stories"),
 dt.date(2027,1,6): ("Secrets of Rome", "On 6 January a witch flies over Piazza Navona.", "La Befana brings sweets (or coal) at Epiphany, and Piazza Navona's Christmas market traditionally celebrates her.", "Save for next year"),
 dt.date(2027,1,17): ("Secrets of Rome", "Today in Rome, priests bless the animals.", "On the feast of Sant'Antonio Abate, pets and farm animals are blessed. In Rome the tradition centres on Sant'Eusebio all'Esquilino.", "Tag a dog lover"),
 dt.date(2027,1,30): ("Build in public", "90 days of building LORE in public: the numbers.", "Followers, waitlist, walk tests, fact cards: the real numbers, good and bad. Next up: 50 prototype units and a beta in Rome.", "Join the waitlist"),
}

# platform schedule by weekday (0=Mon)
SCHED = {
 "TikTok":    {d: ["Narrated POV walk (25-35s)"] for d in range(7)},
 "Instagram": {0:["Reel"],1:["Reel"],2:["Reel"],3:["Reel"],4:["Carousel (7 slides)"],5:["Reel"],6:["Story set (poll + link sticker)"]},
 "YouTube":   {0:["Short"],2:["Short"],4:["Short"],6:["Long-form (12-20 min)"]},
 "X":         {d:["Post / thread"] for d in range(5)},
 "Reddit":    {3:["Text post (value-first)"]},
 "LinkedIn":  {1:["Founder post"],3:["Company post"]},
 "Pinterest": {0:["Idea pin"],2:["Standard pin (1000x1500)"],5:["Standard pin (1000x1500)"]},
}
PILLAR_BY_DAY = {0:"Secrets of Rome",1:"Look up",2:"Secrets of Rome",3:"Solo safe",4:"Build in public",5:"Secrets of Rome",6:None}

banks = {"Secrets of Rome": itertools.cycle(SECRETS), "Look up": itertools.cycle(LOOKUP),
         "Solo safe": itertools.cycle(SOLO), "Build in public": itertools.cycle(BUILD)}
xbank = itertools.cycle(BUILD[3:] + BUILD[:3])
lbank = itertools.cycle(BUILD)
rbank = itertools.cycle(SECRETS[5:] + SECRETS[:5])
pinbank = itertools.cycle(SECRETS[10:] + LOOKUP)
ytlong = itertools.cycle([
 ("One Street, Five Stories: Via Giulia", "A 15-minute walk down Rome's straightest Renaissance street, with five stories most people walk past."),
 ("Rome's Talking Statues: a complete walk", "Pasquino, Madama Lucrezia, Marforio, Abate Luigi, il Facchino, il Babuino: a walking route linking all six."),
 ("How we're building an AI guide that can't lie", "Founder explainer: fact cards, sources and Map Vision, shown with the prototype."),
 ("Look Up, Rome: 12 ceilings in one afternoon", "A route through free-entry churches with jaw-dropping ceilings."),
 ("Solo in Rome: my first 24 hours", "A calm, practical first day: transport, neighbourhoods, staying connected, evening walks."),
 ("The Aventine: keyhole, oranges and the best sunset", "A short loop with the stories of the Aventine Hill."),
 ("Building LORE: 90-day update", "What we learned from walking tests, followers and the waitlist."),
])

CTAS = {
 "Secrets of Rome": ["Follow for a new Rome secret every day", "Save this for your Rome trip", "Send this to whoever you're going to Rome with", "Which street should we do next? Comment below"],
 "Look up": ["Save this for your Rome trip", "Tag us in your #LookUpChallenge", "Follow for more Look Up, Rome"],
 "Solo safe": ["Save this before your next solo trip", "Share with a friend who travels solo", "What's your rule? Comment below"],
 "Build in public": ["Join the waitlist (link in bio)", "Tell us what we're getting wrong", "Follow the build"],
}

def pillar_for(day, idx):
    p = PILLAR_BY_DAY[day.weekday()]
    if p is None:  # Sunday alternates
        p = "Look up" if (idx // 7) % 2 == 0 else "Solo safe"
    return p

def adapt(platform, fmt, pillar, item, day_i):
    topic, hook, body = item[0], item[1], item[2]
    src = item[3] if len(item) > 3 else ""
    cta = CTAS[pillar][day_i % len(CTAS[pillar])]
    tags = HASH[pillar]
    if platform == "TikTok":
        script = f"[0-2s] On-screen text: '{topic}' + VO hook. [2-25s] POV walk; LORE-style narration: {body} [25-30s] Tilt up / reveal. End card: 'Every street has a story.'"
        tags = tags[:4]
    elif platform == "Instagram":
        if fmt.startswith("Carousel"):
            script = f"Slide 1 cover (Fraunces headline): '{hook}'. Slides 2-6: one fact per slide with a photo. Slide 7: source + 'Join the waitlist: {WAITLIST}'. Caption: {body}"
        elif fmt.startswith("Story"):
            script = f"Frame 1 poll: 'Did you know? {hook}' (Yes / No). Frame 2 answer: {body} Frame 3: link sticker to {WAITLIST}."
        else:
            script = f"Reel (native IG edit of the TikTok). Caption: {hook} {body}"
        tags = tags[:5]
    elif platform == "YouTube":
        if fmt.startswith("Long"):
            t, d = next(ytlong)
            hook = t; script = d + " Chapters, sources in description, a waitlist link in the first line."
            topic = t
        else:
            script = f"Short (TikTok repurpose, no watermark). Title: '{hook}'"
        tags = tags[:3]
    elif platform == "X":
        b = next(xbank); topic, hook = b[0], b[1]
        script = f"{hook} {b[2]}"; pillar = "Build in public"; tags = []; cta = "Follow the build"
    elif platform == "Reddit":
        s = next(rbank); topic = s[0]
        hook = f"r/rome or r/solotravel: 'A free walking route: {s[0]} and 4 nearby stories (with sources)'"
        script = f"Value-first text post with route + sources; disclose 'I work on LORE' in the post; no link unless subreddit rules allow. Fact: {s[2]}"
        pillar = "Secrets of Rome"; tags = []; cta = "Ask for feedback; no hard sell"
    elif platform == "LinkedIn":
        b = next(lbank); topic, hook = b[0], b[1]
        script = f"Founder voice, 150-250 words. {b[2]} End with one question for travel-industry readers."
        pillar = "Build in public"; tags = ["#TravelTech", "#Hardware"]; cta = "Comment / DM for Fleet Pilot (hostels, tour operators)"
    elif platform == "Pinterest":
        s = next(pinbank); topic, hook = s[0], s[1]
        script = f"Vertical pin, Bone background, Fraunces title '{s[1]}'. Description: {s[2]} Link: lore.travel/journal"
        pillar = "Secrets of Rome" if s in SECRETS else "Look up"; tags = ["#RomeTravel", "#HiddenRome", "#ItalyTravel"]
        cta = "Save to your Rome board"
    fact = "VERIFY vs Rome City Pack" + (f" (source hint: {src})" if src else "") if pillar in ("Secrets of Rome", "Look up") else ("Legal review (safety copy)" if pillar == "Solo safe" else "Use real numbers only")
    return dict(platform=platform, format=fmt, pillar=pillar, topic=topic, hook=hook, script_caption=script,
                cta=cta, hashtags=" ".join(tags), fact_check=fact)

rows = []
for i in range(DAYS):
    day = START + dt.timedelta(days=i)
    wd = day.weekday()
    pillar = pillar_for(day, i)
    item = next(banks[pillar])
    for platform, sched in SCHED.items():
        for fmt in sched.get(wd, []):
            if day in SPECIAL and platform in ("TikTok", "Instagram"):
                p, hook, body, cta = SPECIAL[day]
                r = dict(platform=platform, format=fmt, pillar=p, topic="Seasonal / milestone", hook=hook,
                         script_caption=body, cta=cta, hashtags=" ".join(HASH[p][:4]),
                         fact_check="VERIFY vs Rome City Pack" if p in ("Secrets of Rome", "Look up") else "Use real numbers only")
            else:
                r = adapt(platform, fmt, pillar, item, i)
            r = {"date": day.isoformat(), "weekday": day.strftime("%a"), **r}
            if platform == "Instagram" or platform == "TikTok":
                r["cta"] = r["cta"] + (" · Waitlist: lore.travel (link in bio)" if "aitlist" not in r["cta"] else "")
            rows.append(r)

fields = ["date","weekday","platform","format","pillar","topic","hook","script_caption","cta","hashtags","fact_check"]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

from collections import Counter
print(f"wrote {len(rows)} rows -> {os.path.normpath(OUT)}")
print(Counter(r["platform"] for r in rows))
print(Counter(r["pillar"] for r in rows if r["platform"] in ("TikTok","Instagram")))
