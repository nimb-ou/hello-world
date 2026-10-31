# LORE Labs: Market Research

*Owner: Head of Market Research. Prepared 30 Oct 2026 for founders, Finance, GTM and investors.*
*Every market fact is cited with a URL inside the linked documents. **[EST]** marks a LORE Research estimate. Personas and WTP figures are hypotheses until the survey runs (Nov 2026 – Jan 2027).*

## Index

| File | Contents |
|---|---|
| [market-sizing.md](market-sizing.md) | TAM/SAM/SOM, top-down and bottom-up, with full math; adjacent markets (solo travel, audio guides, travel tech, travel eSIM, personal safety, AI wearables); SOM scenarios |
| [competitors.md](competitors.md) | 30-product feature matrix, pricing, funding, strengths/weaknesses, threat ranking, LORE positioning |
| [pricing-research.md](pricing-research.md) | Comparable prices, Van Westendorp framework, WTP hypotheses, recommended prices (devices, subscription, accessories), regional pricing (US/EU/UK/JP/IN), Kickstarter tiers |
| [personas.md](personas.md) | 6 personas with JTBD, pains, trip behaviour, triggers, objections |
| [customer-survey.md](customer-survey.md) | Ready-to-run 25-question survey, 20-interview script, validation plan with go/kill thresholds |
| [trends.md](trends.md) | 10 travel trends 2025–2027 with sources and implications |
| [launch-markets.md](launch-markets.md) | 15-city scoring matrix; Rome confirmed as City #1 (narrowly) |
| [launch-scoring.csv](launch-scoring.csv) | Machine-readable city scores |
| [scripts/sizing_model.py](scripts/sizing_model.py) | Market-sizing model; prints every step |
| [scripts/make_charts.py](scripts/make_charts.py) | Generates all charts and the CSV (`python3 research/scripts/make_charts.py`) |
| [charts/market-size-waterfall.png](charts/market-size-waterfall.png) | People funnel + TAM/SAM/SOM $ |
| [charts/competitor-price-positioning.png](charts/competitor-price-positioning.png) | Device price ladder vs LORE |
| [charts/positioning-map.png](charts/positioning-map.png) | Standalone × travel-specialised map |
| [charts/launch-city-scores.png](charts/launch-city-scores.png) | Weighted city scores |

**Regenerate everything:** `python3 research/scripts/sizing_model.py && python3 research/scripts/make_charts.py` (requires matplotlib).

---

## Executive summary (1 page)

### The market is large, growing, and has an empty quadrant
- **Travel is at record volume:** 1.52B international arrivals in 2025 (+4%), with UN Tourism forecasting +3–4% for 2026. Top-100 city arrivals grew **+8%** to 702M, so city breaks (LORE's use case) are growing about twice as fast as travel overall.
- **Solo travel is mainstream:** 35–48% of travellers plan or take solo trips (Skyscanner, Global Rescue, IMG). The solo share of Hostelworld bookings is 63%. Solo-travel spend is estimated at ~$482B (2024) rising to ~$1.07T (2030).
- **Adjacent categories are growing fast:** travel eSIM **$1.8B (2025, +85%) → $8.7B (2030)**; AI wearables $36B+ (2025); smart personal safety devices $12.2B (2024, 16% CAGR); travel experiences heading to $342B (2029).

| | Value | Definition |
|---|---|---|
| **TAM (top-down, 2027)** | **≈ $10.7B / yr** | Current spend on the jobs LORE does: eSIM $3.4B + audio guides $3.2B + safety-wearable travel slice $1.2B + AI-companion slice $1.4B + self-guided tours $1.5B |
| **TAM (bottom-up)** | **≈ $24.0B / yr** | 145M frequent international travellers × $165 ARPU |
| **SAM** | **≈ 8.7M people ≈ $1.44B / yr** | Solo/independent, 2+ trips a year, Phase-1 markets (US, CA, UK, EU, AU/NZ), will pay $150+ |
| **SOM (2030 base case)** | **≈ $93M revenue; 250k units in 2030; 415k cumulative (4.7% of SAM)** | Bear ~$46M / Bull ~$148M |

### Competition: everything exists, but not together
- **No product combines** location-triggered *verified* stories + directional "Map Vision" + offline + its own data + SOS in a standalone, eyes-up device. The **standalone × travel-specialised** quadrant is empty (see the positioning map).
- **Top 3 threats:** (1) **Google/Samsung Gemini glasses + Google Maps** (fall 2026); (2) **Meta Ray-Ban / Display** (~7M glasses sold in 2025, camera vision); (3) **"phone + AI-guide app + eSIM"** (Audiala $4.99/mo + Airalo ~$20–37 + free Apple SOS). OpenAI's io device (H2 2026–2027) is the narrative threat.
- **Cautionary tales:** Humane (~10k units, dead; assets sold to HP for $116M); Rabbit (~130k sold, ~5% daily use); Detour (premium audio walks, shut down 2018). **Success template:** Plaud (>1M devices, ~$250M run-rate) shows that one narrow job + clip-on + subscription works.

### Pricing recommendation

| | Pebble | Square | Atlas | Explorer | Trip Pass |
|---|---|---|---|---|---|
| **Recommended (US)** | **$149** (hold) | **$299** (hold) | **$599** (raise from $549; A/B test) | **$9.99/mo** + **new $79/yr annual** | **$29** / 14 d / 5 GB + new **$49** / 30 d / 10 GB |
| Kickstarter super early bird | $99 | $199 | $399 | 6–12 months included | |
| EU / UK / JP | €159 / £149 / ¥24,800 | €329 / £299 / ¥49,800 | €649 / £599 / ¥98,800 | | |

Anchors: Plaud NotePin S $179 and Shokz $180 (Pebble); Pocketalk Plus $299.95 with data (Square); Garmin inReach Mini 3 Plus $499, Apple Watch Ultra 3 and Meta Ray-Ban Display $799 (Atlas). LORE Buds: **$129** (vs Shokz OpenRun Pro 2 $179.95).

### Launch city
**Rome is confirmed as City #1 (8.65/10)**, narrowly ahead of London (8.60) and Paris (8.40). Recommendation: Rome for City Pack v1 and the Kickstarter story; **London as the parallel dev/beta city** (best open data, English, press); **Florence as City 1.5** (reuses the Italian pipeline). Move Istanbul and Kyoto to Wave 3 (regulation and language).

### Recommendations
1. **Lead with experience, justify with safety.** Stories are the daily delight; safety (phone-independent location share, walk-me-home, discreet SOS) is the purchase justifier for women, parents and retirees. Don't headline "data"; it is a commodity at $2–4/GB.
2. **Make "verified facts with sources" the brand moat.** AI-guide apps are commoditising LLM narration, and trust is the gap.
3. **Design against the idle-device risk:** annual Explorer at $79, a free tier that is useful forever, home-city "Weekend Walks," and retention KPIs in the investor deck (the Rabbit lesson).
4. **Interoperate with glasses and earbuds** rather than fight Big Tech. LORE is the travel brain; any audio output works.
5. **Partner, don't fight,** on eSIM (Airalo/1GLOBAL wholesale) and content (license VoiceMap/SmartGuide tours as Premium Walks).
6. **Run the validation plan before Kickstarter:** n = 600 survey, 20 interviews, 50-unit beta. Go only if concept T2B ≥ 35%, "device over app" ≥ 25% and calibrated purchase intent for Square at $299 ≥ 8%; pre-launch target ≥ 25k emails / 2.5k deposits.

### Known data gaps (to close next)
Full-year 2025 international-visitor figures for Barcelona, Amsterdam, Tokyo, Florence and Madrid; Holafly and Saily audited financials; wholesale eSIM data cost per GB (Hardware/Finance); Italy-specific pricing elasticity. Several hosts (euromonitor.com, timeout.com, axios.com) were blocked for direct fetching in this environment, so figures from them are taken from search-result summaries and syndicated coverage.
