# Investor FAQ: the 25 hardest questions

*LORE Labs, pre-seed, November 2026. These answers are as honest as we can make them. Numbers come from the team folders (cited) and are estimates unless stated. Simulated means model output, not measured data.*

---

## A. Why this, why a device

**1. Why isn't this just an app? Google Maps + Gemini on a phone already does most of this.**
It might be, and we have built the test for it. Decision D1 says that if Gate G0 shows the phone app alone delivers ≥80% of the value, we ship the app first and keep the device as a later premium model. Our view is that phones fail travellers in three ways a device fixes:
- **Phone-independent data and SOS.** The global eSIM on Square and Atlas keeps working when the phone is stolen or flat.
- **A separate battery** of 2+ days (simulated), so the phone's battery is left for photos, tickets and payments.
- **Eyes up, phone hidden**, with physical buttons for talk, "what's around me" and SOS.

The phone PWA is our prototype and stays the companion app, so the software is not wasted either way.

**2. Humane and Rabbit burned hundreds of millions on AI gadgets. Why are you different?**
They sold general-purpose assistants with no daily job:
- **Humane:** ~$230M raised, ~10k units, assets sold to HP for $116M.
- **Rabbit:** ~130k units sold, ~5% daily use.

We differ in four ways:
- **One narrow job.** LORE tells you the stories of the street you are on, during the trips where you need it. Plaud (>1M devices) shows a narrow job, a clip-on and a subscription can work.
- **Lower prices.** We start at $149, against Humane's $699 + $24/mo.
- **No pre-PMF mega-round.** We are raising $1.75M against gates.
- **Retention built in.** An annual plan, a free tier that stays useful, home-city "Weekend Walks", and retention KPIs reported to investors (`research/README.md`, `finance/valuation.md`).

**3. People travel 2–3 times a year. Won't the device sit in a drawer between trips?**
Yes, this is the main structural risk. Our answers:
- Trip Pass pricing ($29 / $49) that matches episodic use.
- An annual Explorer plan at $79.
- Home-city "Weekend Walks".
- B2B fleet rental for hostels and tour operators, which keeps devices in use.

The model assumes 6% monthly churn and only 28–55% paid attach after the trial (`finance/unit-economics.md`). Gate G3 needs churn <6% and attach >55% before we scale.

**4. Isn't "verified facts" just a marketing line? LLMs hallucinate.**
It is how the system is built (D4). Every story comes from fact cards, and each card carries a source URL. The prompt allows only the selected facts. A validator (`software/packages/core/src/narration.ts`) rejects any output that strays, and in that case LORE falls back to a deterministic template. The current limitation: the 215 Rome cards are curated with Wikipedia citations but still need an online verify pass and human editorial review before customers hear them. That is why the Content Editor-in-Chief is hire #6.

## B. Big Tech and competition

**5. Google/Samsung Gemini glasses ship in fall 2026 and Meta sold ~7M Ray-Bans in 2025. Aren't you roadkill?**
This is our #1 threat (`research/competitors.md`). Google owns the POI graph and Gemini Live. We will not out-platform them. Our plan:
- **Out-curate them** on verified, travel-specific stories.
- **Win on directionality** with Map Vision.
- **Win on the trip itself:** offline packs, a 2–3 day battery, a phone-independent eSIM and SOS, and price ($149 vs $799 for Ray-Ban Display).
- **Interoperate** with any earphones and, later, glasses, so LORE is the travel brain whatever the output device.

If glasses win the form-factor war, the City Packs and story engine remain the asset.

**6. What stops Google or Apple from copying the story feature?**
Nothing technical stops them in the short term. Our defences are focus and trust:
- A fact-checked editorial process per city.
- Patents planned on Map Vision (P1) and quiet-moment behaviour (P2), with provisionals due by 15 Jan 2027.
- A premium travel brand.

Big platforms tend to optimise for breadth, not sourced storytelling. We do not claim a hard moat at pre-seed.

**7. Why not license the story engine to Big Tech or OTAs instead of building hardware?**
It is a real option and we keep it open. B2B and licensing sit in the plan (fleet rental, strategics in `finance/fundraising-plan.md`). But without our own device we would give up the global eSIM, battery and safety features that justify the purchase, the higher margin (D1), and the brand.

## C. Hardware economics (the hard part)

**8. Your own hardware team said Pebble and Square had zero or negative margins. Is this business viable?**
At first, no. At 10k units with 2026 DRAM prices and NRE included, landed COGS were Pebble $157 (−5% margin at $149), Square $299 (0%) and Atlas $413 (`hardware/README.md`). We changed the product rather than hide it:
- **D10, Pebble becomes "Lite":** AI runs on the phone over Bluetooth and offline stories are pre-generated. Landed cost is ~$90, giving a 39% margin.
- **D11, Square moves to LTE Cat-1bis:** it stays at $299. The cost-down target is ≤$240 landed by unit 10k, and the price moves to $329 if DVT misses by >10%.
- **D8, Atlas rises to $599.** It becomes the margin engine at 37% DTC hardware GM.
- **D15, retail leads with Pebble and Atlas.** Square stays DTC-only until it is ≤$200 landed.

DTC hardware GM at H2-2028 cost is 42% / 23% / 37%, and lifetime contribution after $60 CAC is $42 / $57 / $211 (`finance/unit-economics.md`).

**9. What if the Square cost-down fails?**
It is the single biggest swing factor in the model. If Square stays at $227 landed, FY2031 EBITDA is **−$8.3M instead of +$0.8M**, and the equity need rises by ≈$19M. Moving the price to $329 recovers about half of that. We will set a hard DVT gate in Sep 2027: if the projected landed cost is above $205 ex-NRE, the price moves to $329 before regular DTC sales open (`finance/pricing-margin-sensitivity.md`). Kickstarter prices are locked, so the first ~2k Square units carry thin margins (7%).

**10. Doesn't Pebble "Lite" make it just a Bluetooth accessory for the phone?**
Partly, and on purpose. Pebble was always conceived as the tethered entry model. It keeps the eyes-up experience, the physical buttons, the clip-on form and a 1.5-day battery, and offline it still plays pre-generated stories. It loses offline Q&A. The kill criterion in D10 is that beta users strongly want offline Q&A on the cheapest model.

**11. Tariffs and the DRAM shortage?**
- **Tariffs:** China final assembly would put Square at $343 landed. That is why D13 moves assembly to Vietnam/Malaysia, and the model assumes 0% duty. China assembly at +20% FOB is the worst single sensitivity: about −$10M of EBITDA a year.
- **DRAM:** this is the most volatile BOM line. At a normalised $3/GB, Square ex-NRE would fall to ~$206. Mitigations are a DRAM buy-ahead and Pebble Lite, which carries no on-device LLM memory (`hardware/README.md`).

**12. Battery claims: you marketed "3 days" for Atlas.**
We no longer do. In simulation the Atlas reached 2.4 days (new cell, optimised firmware), short of the 3-day target, so D12 changed the claim to "2+ days". With baseline firmware all three models only reach 1.2–1.65 days, so firmware power work is critical. Gate G1 needs ≥1.5 days measured on EVT units.

**13. Map Vision accuracy is all simulated. What if it doesn't work on real streets?**
Correct, all of it is simulated today:
- Hardware simulation: 99.9% left/right with EKF + map-matching + L1/L5.
- Software walk: 100% direction accuracy and 4.3° mean heading error on synthetic sensors.

Real-world risks are urban-canyon GNSS multipath, magnetic disturbance and metal enclosures. Gate G1 requires ≥90% on real test walks, and D3's kill line is <85%. Below that we would need a camera (Atlas only) or a different interaction model. Rome walk tests start with G0.

**14. Certification and LTE look expensive and slow for a pre-seed company.**
They are. Certification is ≈$485k for Square and ≈$640k for Atlas; carrier acceptance and India are the longest items. The finance model books $1.29M of certification across the three SKUs, funded by the seed, not the pre-seed. Pebble has no cellular, which keeps the entry SKU simple. The cellular range of a metal-bodied device is estimated at 0.72–0.77× a phone, so OTA chamber work starts at EVT.

## D. Market and demand

**15. Is the $10.7B TAM real or stitched together?**
It is a top-down sum of today's spend on the jobs LORE does: eSIM $3.4B, audio guides $3.2B, the travel slice of safety wearables $1.2B, the AI-companion slice $1.4B, and self-guided tours $1.5B. Each part is cited in `research/market-sizing.md`. The number we underwrite is the bottom-up SAM: 8.7M solo or independent travellers, ≈$1.44B/yr. Research's 2030 SOM is $93M at list price. Finance nets it to $67M after discounts, retail margin and churn.

**16. Where is the evidence that anyone wants this?**
We have none from customers yet, and we do not claim any. The validation plan (`research/customer-survey.md`, `company/operating-plan.md`) runs before Kickstarter:
- An n≥500–600 survey, 20 interviews, 20 Rome walk tests and 200 remote simulation users.
- **G0:** ≥40% of testers "very disappointed" without LORE, and ≥25% would pay $149 or more.
- **Pre-Kickstarter:** ≥25k emails and 2.5k deposits.
- **G2:** ≥$1M pledged from ≥3,000 backers.

If we miss, we stop or pivot before the expensive hardware spend.

**17. Your Kickstarter projection is $1.04M. Hardware campaigns often miss.**
The $1.04M is GTM's base case, not a result: 4,600 backers × $225 at ≈$50 cost per backer on $230k of marketing. The conservative case is $554k, which misses the $1M gate, and an escalation playbook is ready for it. The public goal is $250k. At half the base case the seed still closes in our plan but FY2028 revenue falls. Below 3,000 backers we delay Atlas and DVT spend (`finance/kickstarter-economics.md`).

**18. Why Rome first?**
It has the most history per square metre, very high tourism, rich open data, and it is reachable for walk tests. In Research's 15-city scoring Rome won narrowly at 8.65, against London 8.60 and Paris 8.40 (`research/launch-markets.md`). London runs in parallel as the dev and beta city (best open data, English-language press), and Florence is "City 1.5" (D9). Rome is also the Kickstarter story.

**19. City Packs sound labour-intensive. How does this scale to 20 cities in 2028?**
The pipeline is semi-automated. The builder fetches from OSM and Wikipedia (`software/city-pack/`), and humans review and edit the facts. We cap expansion at one new city per month until City Pack quality scores are measured. The seed plan has 3 content editors covering several cities each, plus licensed storytellers at €40–€150 per story. Cost and speed per city are unproven, and that is a real unknown.

## E. Financials and the round

**20. You need $55.5M to reach break-even. That is a lot of dilution for a consumer hardware company.**
It is (D16). The base case reaches EBITDA break-even in FY2031 on $111M revenue. The peak cumulative outflow is $33.4M, and the rest is a buffer for inventory and the bear case. The founder holds ≈35% after the Series B. The bull case breaks even in FY2030, and the bear case needs ≈$72M. Blended gross margin peaks at around 41%, which is GoPro territory, not Oura or Whoop, because recurring revenue reaches only ~13% of the mix. Valuation upside depends on lifting subscription attach (`finance/valuation.md`).

**21. Why $1.75M at a $12M post-money cap? Why did the round change?**
At $1.5M the model's cash bottomed at ≈$278k in Jun-27, one month before the Kickstarter payout. A one-month slip would have meant emergency cuts. D14 adds a $250k top-up on the same cap, which lifts the low point to ≈$0.5M. Investors get ≈14.6% post-money at conversion. For reference, Carta-reported 2025 medians were a $16M pre-money for all-sector seed rounds and $19M for hardware seed rounds. This is a pre-seed with no customer data, so we priced below those.

**22. What exactly does the pre-seed buy?**
Gates G0, G1 and G2. The money goes to:
- **Founding engineering team** (firmware, ML/story engine, mobile/backend): ~$500k.
- **Kickstarter, brand and community:** ~$322k.
- **ID, ODM NRE and 50 EVT units:** ~$210k.
- **G&A, legal, IP and insurance:** ~$168k.
- **City Pack content:** ~$40k.
- **Buffer through the Kickstarter:** ~$510k.

The $6M seed in Aug 2027 then funds DVT/PVT, certification and the first 5k units (`finance/budget-12-months.md`, `finance/fundraising-plan.md`).

**23. Kickstarter money is pre-sales. Are you counting it as revenue or using it to fund operations?**
It is deferred revenue: a liability to backers until shipment (Nov-27 to Apr-28). The payout (≈$0.86M net in Jul-27) does fund DVT tooling and the first ODM deposits. That is normal for hardware crowdfunding, but it means a delivery slip is a reputational and cash risk at the same time. Warranty reserves, 3PL and fulfilment terms are planned in `legal-ops/supply-chain-ops.md`.

## F. Team, legal and execution

**24. It's a solo founder with AI agents. Who will actually build this?**
Today the founder runs every function through AI-agent teams and signs off each output. That is how this much documentation, code and modelling exists before any hiring. It does not replace a team that has shipped hardware, and we do not pretend it does. The first pre-seed hires (`legal-ops/hr-hiring.md`) are:
1. Founding Firmware Lead (Nov 2026).
2. ML/Story-Engine Engineer (Nov 2026).
3. Mobile + Backend Engineer (Dec 2026).
4. Hardware/EE Lead, starting on contract (Jan 2027).
5. Sensor-Fusion Engineer (Jan 2027).
6. Content Editor-in-Chief (Jan 2027).
7. Growth/Kickstarter Lead (Feb 2027).

We also plan contract-first ID, RF and ODM programme management. Execution risk is concentrated in the founder until these hires land. Investors should weigh that.

**25. What legal or IP landmines should we know about?**
- **Trademark:** "LORE" has potential conflicts (Epic Games, Pixite, YLORE filings, and the "Lore" podcast in class 41). We will not file in class 41, and full clearance is due Dec 2026 (D2's kill criterion is a blocking conflict, which would mean a compound mark or a rename).
- **Founder residency:** Indian FEMA/ODI rules on founder residency need an opinion before incorporation.
- **EU rules:** the battery-removability rules (Feb 2027) and Cyber Resilience Act obligations (Dec 2027) affect device design.
- **Location data** is sensitive under GDPR. A DPIA is drafted.

All legal documents are drafts or templates pending counsel (`legal-ops/README.md`).

---
*See also: `investor/data-room-index.md` for the evidence behind each answer.*
