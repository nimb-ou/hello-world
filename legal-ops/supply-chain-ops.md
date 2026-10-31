# Supply Chain, Manufacturing Ops, Fulfilment and Customer Support

> Planning document. Costs are **estimates** unless a source is cited. Third-party price points come from web search on 30 Oct 2026, mostly from secondary review sites, and must be replaced with **written quotes**. Items marked [verify] were not re-checked. Not legal advice. Contract terms are in `templates/odm-supply-agreement-term-sheet.md`.

Owner: COO. Partners: Hardware (BOM, NPI), Finance (cash and inventory), GTM (Kickstarter promises).

---

## 1. Manufacturing operating model

| Stage | Dates (COMPANY.md) | Units | Where | Key ops tasks |
|---|---|---|---|---|
| Proto (works-like / looks-like) | Q4 2026 | 5–20 | In-house + Shenzhen proto shops (JLCPCB/PCBWay PCBA; Protolabs/RapidDirect CNC) | Phone-app prototype + Rome pack is the main Q4 deliverable |
| **EVT** | **Q1 2027** | **50** | ODM short-run | Validate electronics, RF pre-scans, battery, Map Vision accuracy; beta units "not for sale" labels |
| DVT | Q2 2027 | 300 | ODM | Full certification samples; reliability tests (drop 1.2 m × 26, tumble, IP test, thermal cycling −20/+60°C, salt fog for metal, button life 100k presses, UV/sweat on straps); Kickstarter video units |
| PVT | Q3 2027 | 1,000 | ODM MP line | Line yield ≥95% FPY; test-station validation; packaging drop (ISTA 3A); certification samples for retail |
| **MP** | **from Sep 2027; 5k units shipped Q4 2027** | 5,000 → 20k/yr | ODM (+ second source by 2028) | Weekly build reviews; AQL inspection; DG shipping |

**ODM selection process (Nov 2026–Jan 2027):** RFI to 8 → RFQ to 4 → factory audits (2) → selection by **31 Jan 2027**. Scorecard in the term sheet. **Decision D13: final assembly in Vietnam/Malaysia.** Shortlist ODM/EMS partners with VN plants (Bac Ninh/Bac Giang/Hai Phong) or MY plants (Penang/Johor). Many Shenzhen ODMs run VN lines. Do PCBA SMT, final assembly, test and firmware provisioning **in-country** to support substantial transformation (no US Section 301; see `compliance-matrix.md` §4). Plan for longer component lead times (China-sourced parts move to VN/MY) and **+5–10% MVA vs Shenzhen (e) [verify]**. Proto/EVT may still be built in Shenzhen.

**Critical long-lead parts (place orders by DVT):** LTE Cat-1bis module for Square (D11) / Atlas LTE module (16–26 weeks), application SoC/NPU (Square/Atlas only; Pebble Lite has no on-device LLM per D10), 1.6" AMOLED (custom FPC), eUICC, GNSS L1/L5 chip, Li-ion cells (custom size), sapphire (Atlas), titanium bar stock. **Kickstarter cash funds the LLT buys.**

**Quality system:** a lightweight QMS from DVT (Notion + Linear): specifications control, ECN log, FAI reports, AQL plans, 8D for failures, supplier corrective-action requests (SCAR). Hire a **Quality/Supply Chain Manager in China/Taiwan** (or use a sourcing agent at 3–5%) by DVT (see `hr-hiring.md`).

---

## 2. Logistics architecture

```
ODM/EMS (Vietnam or Malaysia, per D13)  ──ocean FCL/LCL (batteries OK as UN3481 under IMDG SP188)──►  US 3PL (CA or NJ/PA)  ──► US/CA backers
          │                                                                         ├─► EU 3PL (NL/DE) ──► EU backers (DDP, OSS VAT)
          │──air freight (UN3481 PI 967 Sec II, ≤30% SoC recommended)──►            ├─► UK 3PL ──► UK backers (DDP)
          └─► APAC 3PL (HK/SG/JP) ──► JP/AU/Asia backers                              
```

| Option | What they do | Fit for LORE | Indicative cost |
|---|---|---|---|
| **Flexport** | Freight forwarding, customs brokerage, DG handling, plus fulfilment network | **Primary forwarder + customs broker** (US/EU entries); also inventory finance | Ocean 40' FCL CN→US West Coast typically $2k–$6k (volatile) [verify]; brokerage ~$100–$250/entry |
| **ShipBob** | DTC fulfilment (US, EU-NL, UK, CA, AU) | Good for **steady-state DTC** + accessories | Receiving ~$25/hr first 2 hrs then $35–45/hr; storage ~$5/bin, $10/shelf, $40/pallet per month; pick fees ~$0.20–0.30/extra item; onboarding ~$500–$1,000 (third-party reviews) ([Fulfyld](https://www.fulfyld.com/reviews/shipbob/), [Simpl](https://simplfulfillment.com/breakdowns/shipbob-pricing)). Must confirm **DG/lithium** acceptance |
| **Crowdfunding specialists**: e.g., **Fulfillrite (US)**, **Easyship** (multi-carrier + crowdfunding), **Floship (HK)**, **ShipMonk**, **Byrd (EU)**, **Weareone/Ekan**, **Zendrop** | Bulk Kickstarter waves, multi-region DDP | **Recommended for the Kickstarter wave** (spiky volume, international DDP) | ~$3–$8/order pick-pack + postage [verify]; quotes needed |
| Regional | EU: **Byrd**, Bigblue, Cubyn; UK: **Huboo**, Zendbox; JP: **Openlogi**; IN: Shiprocket (later) | Local 3PLs with authorised-rep/GPSR services | Quotes |
| Amazon FBA | Retail channel 2028 | Not for Kickstarter | |

**Recommendation:**
1. **Flexport** for international freight and customs (US formal entries, EU/UK import with LORE as importer of record via an indirect representative).
2. **One crowdfunding-specialist 3PL** with **US + EU (NL) + UK** nodes for the Kickstarter wave (Oct–Dec 2027). Shortlist Easyship, Fulfillrite and ShipBob (if DG approved). Choose by **Mar 2027** so shipping costs are right in the Kickstarter reward pricing.
3. Ship **DDP** (duties and VAT paid) to backers in the EU/UK. Backers hate surprise import charges.
4. **Never air-ship the power puck as standalone cargo on passenger aircraft** (UN3480). Ship by sea, or only as a cargo-aircraft DG shipment.

**DG documentation pack per SKU:** UN38.3 test summary (per cell/battery), MSDS/SDS, lithium battery mark, Wh rating on the battery, ≤30% SoC confirmation (recommended for PI 967; mandatory for packed-with PI 966 >2.7 Wh since 1 Jan 2026) ([FAA 2026 guide](https://www.faa.gov/sites/faa.gov/files/Lithium-Battery-Shipping-Guide_508_2026.pdf), [LION](https://www.lion.com/lion-news/december-2025/new-lithium-battery-state-of-charge-limit-in-effect-jan-1)), 1.2 m drop-test-capable packaging, DG-trained staff at the 3PL.

---

## 3. Kickstarter fulfilment plan

| Item | Plan |
|---|---|
| Fees | Kickstarter **5%** + payment processing **~3% + $0.20/pledge** (US; varies by country) ([Kickstarter Help](https://help.kickstarter.com/hc/en-us/articles/115005028634-What-are-the-fees)). Budget **8–10%** of funds raised for platform + processing |
| Pledge manager | **BackerKit** (processing 2.9% + $0.30; pledge-manager fee per plan) ([BackerKit](https://backerkit.com/plans)) or Kickstarter's native Pledge Manager (same fees as campaign) ([Kickstarter Help](https://help.kickstarter.com/hc/en-us/articles/115005028634-What-are-the-fees)). Collect **shipping + VAT/duties** after the campaign, using address locks |
| Shipping charge | Charge shipping in the pledge manager **by region** (US/CA, EU, UK, APAC, RoW). Estimated landed DDP cost per device: US $10–$18, EU $14–$25, UK $14–$22, APAC $15–$30 [estimates] |
| VAT | EU VAT on the pledge value is due at import/sale. Treat the **backer pledge price as VAT-inclusive** for EU backers (set EU pledge prices accordingly). Kickstarter isn't a "deemed supplier" [verify]. OSS registration for EU B2C distance sales from the EU 3PL |
| Wave plan | Wave 1 (Oct 2027): early-bird + US. Wave 2 (Nov): EU/UK. Wave 3 (Dec): RoW + add-ons. Plan holiday cut-offs |
| Communication | Monthly updates (biweekly near shipping); honest delay notices; FAQ; **refund policy before shipping** (refund on request minus processing fees, or full refund at LORE's discretion) |
| Address hygiene | Address validation (Loqate/Smarty), lock date, change fee waived until lock |
| Tracking | Branded tracking (AfterShip / Narvar lite) |
| Lost/damaged | Shipping insurance or 3PL liability; reship within 5 business days |
| Device activation | 3-month Explorer starts on activation (see subscription terms) |
| Cost contingency | **+15%** on logistics budgets (freight volatility; tariff changes) |

---

## 4. Inventory planning

- **Demand plan:** Kickstarter backers (known) + pre-orders + Q4 2027 DTC + retail pilot. **First MP order: 5,000 devices** (per COMPANY.md) split by SKU/colour from backer survey data. Proposal pending Kickstarter mix: Pebble 45% / Square 40% / Atlas 15%.
- **Safety stock:** 10% over committed backer units for DOA/replacements/RMA swaps + 5% for retail samples/marketing.
- **Reorder point (steady state):** ROP = (average weekly demand × lead time in weeks [≈12 incl. transit]) + safety stock (z=1.65 × σ_weekly × √LT).
- **Accessories:** MOQ 500–1,000 each. Prioritise the clip, strap and dock. Defer the rugged case and city bundles until data arrives.
- **Inventory finance:** 30/70 ODM terms. Kickstarter funds cover the first MP. Consider Kickfurther / Flexport Capital / Clearco for the second build.
- **Tools:** Shopify + **Cin7 Core / Katana / inFlow** (MRP-lite) synced to the 3PL. Serial-number capture at the 3PL (needed for warranty and theft-lock).
- **KPIs:** weeks of supply (target 8–12), inventory accuracy ≥99.5%, stock-outs, aged inventory >180 days, shrinkage.

---

## 5. Returns and RMA process

| Step | SLA | System |
|---|---|---|
| 1. Customer opens a request in the app/website (reason codes) | — | Zendesk/Intercom form + Shopify returns app (Loop/AfterShip Returns) |
| 2. **Remote triage**: diagnostics upload, guided reset, firmware update | 24h | Support Tier 1/2 |
| 3. RMA approved → prepaid label (ground for lithium; "damaged/defective" batteries **ground only, special packaging**) | 1 business day | 3PL |
| 4. Advance replacement for Square/Atlas (card hold) | ship in 1 business day | 3PL |
| 5. Receive, grade A/B/C/D, data wipe (NIST 800-88), log the serial | 3 business days | 3PL + RMA log |
| 6. Refund / replacement / repair | refunds ≤ 5 business days after receipt (EU law: 14 days from withdrawal) | Shopify |
| 7. Failure analysis: monthly batch to the ODM; 8D reports | monthly | Hardware QA |
| 8. Refurb → "Certified Renewed" (1-yr warranty) or recycle via a WEEE-compliant recycler | — | 3PL / refurb partner |

**Targets:** DOA <1%; 30-day return rate <8% (consumer electronics norm 5–15% [estimate]); 12-month field failure <3%; RMA turnaround <7 days door-to-door.

---

## 6. Warranty reserve

| Parameter | Year 1 (2027–28) | Steady state |
|---|---|---|
| Expected 24-month failure rate | 4–6% (new product) | 2–3% |
| Average cost per claim (replacement unit cost + 2-way freight + handling) | Pebble ~$45, Square ~$95, Atlas ~$170 (estimates; BOM-dependent) | |
| **Reserve accrual** | **3.5% of hardware revenue** | 2–2.5% |
| ODM recovery | Epidemic-failure + 24-month defect warranty back-to-back | |
| Accounting | ASC 460 (US GAAP) / IAS 37 provision. True up quarterly | |

Example: 5,000 units × blended ASP $260 = $1.3M revenue → **$45.5k reserve** in year 1.

---

## 7. Customer support model

### 7.1 Tiers
| Tier | Who | Handles | Target |
|---|---|---|---|
| **Tier 0: self-service** | Help centre, in-app guides, **AI agent** (Intercom Fin or Zendesk AI) trained on the help centre only | Setup, eSIM activation, City Pack downloads, billing FAQs | **≥50% deflection** by month 6 |
| **Tier 1** | Support agents (outsourced BPO in Lisbon/Manila/India for 24×5 → 24×7 by 2028; or in-house first 2 hires) | Account, orders, returns, basic troubleshooting, Kickstarter backer questions | FRT (first response) chat <5 min, email <8 business hrs; CSAT ≥90% |
| **Tier 2** | In-house product specialists | Device diagnostics, eSIM/connectivity issues with the partner, warranty decisions, RMAs | Resolution <48h |
| **Tier 3** | Engineering on-call (firmware/app/backend) via Linear escalation | Bugs, outages, security reports | Sev1 15 min ack, 4h workaround |
| **Safety escalation** | Trained lead + on-call manager | Any SOS-related report, stalking/misuse report, injury claim, battery incident (swelling/fire) | **Immediate**; product-safety incident log (GPSR/CPSC reporting assessment within 24h) |

**Staffing model:** ~1 agent per 1,500–2,500 active devices at launch (high setup contact rate of ~25–35% of new users), falling to 1 per 5,000 with deflection [estimates]. Q4 2027 (5k devices + backers): **2 in-house + BPO overflow during the shipping waves.**

**Languages at launch:** English, Italian (Rome), Spanish, French, German. AI-assisted translation for others.

### 7.2 Tools
| Tool | Choice | Cost (third-party-reported; verify) |
|---|---|---|
| Help desk | **Intercom** (if chat-first + Fin AI) **or Zendesk Suite** (if email/phone + RMA workflows) | Intercom Essential ~$29–$39/seat/mo + **Fin AI $0.99 per resolution**; Zendesk Suite Team ~$55/agent/mo, AI resolutions ~$1.50–$2 each ([Macha](https://www.getmacha.com/blog/intercom-fin-vs-zendesk-ai-pricing), [CostBench](https://www.costbench.com/compare/intercom-vs-zendesk/)) |
| Recommendation | **Intercom + Fin** for the Kickstarter/launch phase (chat-heavy, small team); revisit Zendesk at >10 agents | |
| Returns | Loop Returns / AfterShip Returns | $100–$300/mo |
| Status page | Instatus / Atlassian Statuspage | $0–$79/mo |
| Community | Discord (backers) → Discourse forum | $0–$100/mo |
| Phone | Aircall / Intercom phone (from 2028) | ~$30–$50/seat |

### 7.3 Help-centre outline
1. **Getting started:** unboxing; charging; pairing with the phone app; connecting earphones (LE Audio/A2DP); first walk; buttons (press / double-press / long-press SOS).
2. **LORE Pass and eSIM:** plans; activation; coverage list; data usage; top-ups; travelling between countries; permanent-roaming notice.
3. **City Packs and offline:** downloading; storage; updates; which cities.
4. **Map Vision and stories:** how directions work; accuracy tips (calibrate compass, carry position); "tell me more"; reporting a wrong fact; quiet moments.
5. **Safety features:** setting up contacts; SOS; live share; walk me home; satellite SOS (Atlas); limitations (disclaimer).
6. **Privacy and security:** what's stored; trip history; deleting data; lost/stolen device lock.
7. **Battery and care:** battery life tips; IP rating; cleaning; travel/airline rules.
8. **Troubleshooting:** won't turn on; no GNSS fix; no data; earphones won't connect; resets.
9. **Orders, shipping and returns:** Kickstarter backers; tracking; customs/DDP; returns; warranty claims.
10. **Accessibility:** VoiceOver/TalkBack in the app; audio-first use; large-text mode.
11. **Legal:** warranty, terms, safety information, regulatory labels (e-label), open-source credits.

### 7.4 Top 30 FAQ answers (draft; Brand to apply voice; Legal approved wording in italics where sensitive)

1. **What is LORE?** A pocket-sized AI travel companion that tells you the stories of the places around you through your own earphones, plus directions, live info and safety features. It works online and offline.
2. **Do I need my phone?** Only for setup and some settings. After that, LORE works on its own. Square and Atlas have their own data. Pebble uses your phone's connection or Wi-Fi, or offline City Packs.
3. **Which earphones work?** Any Bluetooth earphones (Classic A2DP or LE Audio). Open-ear or bone-conduction headphones like LORE Buds let you hear traffic too. There's also a small built-in speaker.
4. **How does LORE know what's on my right?** Map Vision combines precise dual-band GPS, a compass and motion sensors, your walking direction and detailed building maps. No camera needed (except Atlas Glance, which you trigger).
5. **How accurate is it?** Usually within a few metres outdoors. Accuracy drops in very narrow streets, indoors and underground. If LORE isn't sure, it says "nearby" instead of "on your right".
6. **Are the stories true?** *LORE's story engine is built to use checked facts with sources, and legends are flagged as legends. It's AI, so mistakes can happen. Say "that's wrong" and our editors review it.*
7. **Will it talk while I cross the road?** LORE tries to stay quiet at crossings, when you stop to talk to someone, or when you're moving fast. *It can't detect traffic. Always look for yourself.*
8. **How long does the battery last?** Pebble about 1.5 days, Square about 2 days, Atlas **2+ days** (D12) in typical use (targets; final tested figures at launch).
9. **Does it work without signal?** Yes. Download City Packs (maps, routes, stories and on-device AI) before you go. Live info and "ask anything" need data.
10. **Which countries does the data work in?** 150+ countries via our connectivity partner. See lore.travel/coverage.
11. **What does LORE Pass cost?** Free (3 cities offline), Explorer $9.99/month (unlimited live AI, 1 GB data, all City Packs) or Trip Pass $29 for 14 days with 5 GB. New devices include 3 months of Explorer.
12. **Will I be charged automatically after the free 3 months?** Only if you chose to continue when you activated. We'll remind you before it converts. Cancel any time in the app.
13. **How do I cancel?** Settings → LORE Pass → Cancel. It takes effect at the end of the period. EU/UK customers also have a 14-day withdrawal right.
14. **Can I use LORE data for my phone (hotspot)?** No. The data is for the LORE device only.
15. **What happens when I press SOS?** A long-press (with a short countdown to cancel) alerts your chosen contacts with your location by data/SMS (and via satellite on Atlas where available). *SOS isn't an emergency service. In an emergency, call 112/911/999.*
16. **Does LORE call emergency services?** *Not directly.* [If a relay partner is offered: "In supported countries, you can choose a monitoring service that can contact emergency services for you."]
17. **What is "walk me home"?** Set a timer and destination. If you don't check in, LORE alerts your contacts with your location.
18. **Who can see my location?** By default, no one. LORE processes location on the device. It's shared only when you start live share or SOS, with the people you pick, and sharing ends automatically.
19. **Do you sell my data?** No. We don't sell personal data and don't use advertising trackers.
20. **Is LORE always listening?** No. It listens only while you press the button. A tiny on-device detector notices when someone is talking so LORE can pause, and it never records.
21. **Can I delete my data?** Yes: Settings → Privacy → Delete trip history / Delete account. You can also download your data.
22. **I lost my LORE / it was stolen.** Lock it in the app. That blocks data and makes it useless to others. We can help with the police report details (serial/IMEI).
23. **Is it waterproof?** It's splash- and rain-resistant (rating per model, e.g., IP67 tbc). Don't swim with it.
24. **Can I take LORE on a plane?** Yes, in your carry-on. The power puck must go in your carry-on, not checked luggage, and some airlines don't allow power banks to be used during flight.
25. **What's the warranty?** 2 years worldwide, plus your statutory rights (e.g., 2-year EU legal guarantee). Battery holds ≥80% capacity for 2 years.
26. **Can I return it?** Yes, within 30 days of delivery for a full refund (14-day legal minimum in the EU/UK).
27. **Kickstarter: when will mine ship?** Wave dates are in updates and the pledge manager. You'll get tracking by email. EU/UK shipments are duties-paid.
28. **Can I change my Kickstarter address?** Yes, in the pledge manager until the address lock date shown there.
29. **Which languages does LORE speak?** At launch: English, Italian, Spanish, French and German narration, with more coming.
30. **Can hostels or tour companies use LORE?** Yes. LORE for Business offers fleet rental, group features and a fleet dashboard. Contact business@lore.travel.

---

## 8. Ops KPIs dashboard (monthly)
On-time ship %, landed cost/unit vs plan, FPY, DOA, return rate, RMA cycle time, warranty claims %, CSAT, FRT, deflection %, tickets per 100 active devices, inventory weeks of supply, freight cost per order, DG incidents (target 0).

## Sources
- Kickstarter fees: https://help.kickstarter.com/hc/en-us/articles/115005028634-What-are-the-fees ; https://www.pledgebox.com/post/how-much-does-kickstarter-take
- BackerKit plans: https://backerkit.com/plans
- ShipBob pricing (third-party): https://www.fulfyld.com/reviews/shipbob/ ; https://simplfulfillment.com/breakdowns/shipbob-pricing ; https://eightx.co/blog/shipbob-shipmonk-regional-3pl-cost
- Lithium battery shipping: https://www.faa.gov/sites/faa.gov/files/Lithium-Battery-Shipping-Guide_508_2026.pdf ; https://www.lion.com/lion-news/december-2025/new-lithium-battery-state-of-charge-limit-in-effect-jan-1
- Intercom/Zendesk pricing: https://www.getmacha.com/blog/intercom-fin-vs-zendesk-ai-pricing ; https://www.costbench.com/compare/intercom-vs-zendesk/
