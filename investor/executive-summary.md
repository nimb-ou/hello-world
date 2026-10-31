# LORE Labs: Executive Summary

*Pre-seed, November 2026. Confidential. All projections are estimates from `finance/LORE_Financial_Model.xlsx` (base case). Simulated results are labelled as simulated. No customers, partners or investors are claimed.*

## 1. The opportunity
Travel is at record volume: 1.52B international arrivals in 2025, and arrivals in the top-100 cities grew 8%. Between 35% and 48% of travellers now plan or take solo trips. Yet the traveller's whole trip still runs on one phone, which has to be guide, map, wallet, camera and lifeline at once. By late afternoon its battery is gone. Held out on a street in Rome it marks you as a target (33,455 pickpocketing incidents in Greater Rome in 2024, +68% vs 2019). And reading Wikipedia in front of a monument means you miss the monument.

**LORE is a pocket-sized AI travel companion that tells you the stories of the city around you through your own earphones.** It works online and offline, and it keeps the phone in your pocket. Our tagline is *"Every street has a story."*

## 2. Product
- **Map Vision** works out what is on your **left, right, ahead, behind** and when to **look up**, without a camera. It fuses multi-band GNSS (L1+L5), a 9-axis IMU and compass, step direction and map geometry (building footprints, street sides). In hardware simulations, left/right accuracy reaches 99.9% with EKF + map-matching + L1/L5. Real-world accuracy is still to be measured; our gate is ≥90% and our kill line is <85% (D3).
- **Verified stories.** Every story is built from fact cards that each carry a source. The language model narrates but is not allowed to invent history: a validator falls back to a deterministic template if it tries (D4). Stories last 20–40 s, with "tell me more" chaining. LORE stays quiet while you cross a road or talk to someone.
- **Why a device:** a global eSIM (Square/Atlas) so it works when the phone is stolen or flat; offline City Packs; a 2+ day battery (simulated 2.1–2.4 days with optimised firmware); and physical buttons for talk, "what's around me" and SOS.

| | **Pebble $149** | **Square $299** | **Atlas $599** |
|---|---|---|---|
| Form | Clip-on, LED ring | 54 mm aluminium, 1.6" AMOLED | Titanium + sapphire, 13.5 mm |
| Brain | Phone + cloud ("Lite", D10) | On-device 3B model + cloud | On-device 3–4B + vision + cloud |
| Connectivity | BLE to phone + Wi-Fi | LTE Cat-1bis global eSIM (D11) | LTE + eSIM + satellite SOS |

**LORE Pass:** Explorer $9.99/mo ($79/yr); Trip Pass $29 for 14 days with 5 GB, or $49 for 30 days with 10 GB; a free tier with 3 cities. Each device includes 3 months of Explorer. Other revenue comes from accessories (LORE Kit, LORE Buds $129), booking affiliate fees and B2B fleet rental for hostels and tour operators.

## 3. Where we are (October 2026)
- **Working software:** a phone PWA prototype running the real story engine, Kalman heading fusion and fact-grounded narration. The Rome City Pack holds 86 POIs and 215 fact cards, each with a source URL. In a simulated 1.93 km walk from the Pantheon to Trevi it made 17 narrations, repeated no facts, met 100% of quiet moments, and had a fused heading error of 4.3° mean (12.7° p95). 61 vitest and 16 pytest tests pass.
- **Hardware:** architecture v0.9 on MediaTek Genio 520/720, with costed BOMs, schematics, and power, RF, thermal and fusion simulations, plus a certification plan (≈$485k for Square and ≈$640k for Atlas).
- **Brand, GTM and legal:** a complete identity system; a Kickstarter plan (25 May to 24 Jun 2027, $250k goal); and draft company formation, IP, privacy and compliance documents.
- **Not yet done:** no real-user walk tests, no EVT units, no revenue, no hires. The founder currently runs each function with AI-agent teams and signs off every output.

## 4. Market
- **TAM:** ≈$10.7B/yr top-down (2027 spend on the jobs LORE does: eSIM, audio guides, travel safety, AI companions, self-guided tours), or ≈$24.0B bottom-up (145M frequent international travellers × $165).
- **SAM:** 8.7M solo or independent travellers in the US, CA, UK, EU and AU/NZ who make 2+ trips a year and will pay $150 or more, ≈$1.44B/yr.
- **SOM (Research, 2030):** ≈$93M of revenue and 250k units (bear case $46M, bull case $148M). Finance nets this down to $67M in FY2030, after retail margin, discounts and churn.

## 5. Competition
The **standalone × travel-specialised** quadrant is empty. The top threats are (1) Google/Samsung Gemini glasses with Google Maps (fall 2026), (2) Meta Ray-Ban/Display (~7M glasses sold in 2025), and (3) a phone running an AI-guide app with an eSIM. We position LORE as the "travel brain" that works with any earphones or glasses, and we compete on verified content, directionality, offline use, battery and safety. Humane (~10k units) and Rabbit (~5% daily use) show what happens when an AI gadget has no daily job. Plaud (>1M devices) shows that one narrow job, a clip-on and a subscription can work.

## 6. Business model and unit economics
Unit economics are for DTC sales at H2-2028 cost (`finance/unit-economics.md`):

| | Pebble | Square | Atlas |
|---|---:|---:|---:|
| Hardware gross margin | 42% | 23% (7% at launch cost) | 37% |
| Lifetime contribution per device, after $60 CAC | $42 | $57 | $211 |

LORE Pass gross margin is ≈69%, rising to ≈75% (cloud + data ≈ $2.02 per paid user-month). **We found the hardware margin problem early and changed the product:**
- **D10:** Pebble moves to a phone-tethered "Lite" design ($157 → ~$90 landed).
- **D11:** Square moves to LTE Cat-1bis, with a cost-down target of ≤$240 landed (fallback price $329).
- **D13:** assembly in Vietnam/Malaysia avoids a China-tariff case of $343 landed for Square.
- **D15:** retail leads with Pebble and Atlas, and Square stays DTC-only until its landed cost is ≤$200.

## 7. Go-to-market
1. **Waitlist** (Nov 2026 to Jan 2027, 5k sign-ups).
2. **Rome beta** with 50 EVT units (Feb to Apr 2027).
3. **Pre-launch** to a 20k email list and 2k $1 VIPs.
4. **Kickstarter**, 25 May to 24 Jun 2027. The base case is **$1.04M** from 4,600 backers at a cost per backer of ≈$50, on $230k of marketing.
5. **DTC** in Q4 2027.
6. **Retail and airports** in 2028, once returns are below 5%.

Channels are short-form social ("Secrets of Rome"), creators, PR and email. We lead with the experience and use safety to justify the purchase.

## 8. Plan, gates and financials
Each stage has a gate that must pass before we spend on the next (`company/operating-plan.md`):

| Gate | Timing | Must be true |
|---|---|---|
| **G0** | Jan 2027 | ≥40% of testers "very disappointed" without LORE; ≥60% finish a 30-minute walk; ≥25% would pay $149 or more |
| **G1** | May 2027 | EVT battery ≥1.5 days; left/right ≥90%; beta users use it ≥3 days a week |
| **G2** | Aug 2027 | ≥$1M pledged; ≥3,000 backers; cost per backer <$60 |
| **G3** | Apr 2028 | Returns <5%; attach >55%; churn <6%/month; NPS >50 |

| Base case | FY27 | FY28 | FY29 | FY30 | FY31 |
|---|---:|---:|---:|---:|---:|
| Units | 3.4k | 39.9k | 120k | 250k | 400k |
| Revenue | $0.6M | $10.1M | $31.6M | $67.1M | $111.3M |
| Gross margin | 11% | 27% | 33% | 38% | 41% |
| EBITDA | −$4.2M | −$4.3M | −$7.2M | −$5.4M | +$0.8M |

EBITDA break-even comes in FY2031. We plan **$55.5M** of total equity to get there (D16): this pre-seed, a $6M seed in Aug 2027, a $3M seed extension, a $25M Series A and a $20M Series B. The bull case breaks even in FY2030. The bear case needs ≈$72M.

## 9. The ask
**$1.75M pre-seed SAFE at a $12M post-money cap**, which gives investors ≈14.6%. This is $1.5M plus a $250k top-up (D14), because at $1.5M cash would have fallen to ≈$278k in Jun-27, one month before the Kickstarter payout.

| Use of funds | Amount |
|---|---:|
| Founding engineering team (firmware, ML/story engine, mobile/backend) | ~$500k |
| Kickstarter, brand and community | ~$322k |
| Hardware: ID/ME, ODM NRE, 50 EVT units | ~$210k |
| G&A, legal, IP, insurance | ~$168k |
| City Pack content | ~$40k |
| Cash buffer through Kickstarter | ~$510k |

The round funds gates G0 to G2 and positions us for the $6M seed.

**Contact:** Nimit Jain, Founder & CEO, LORE Labs, Inc. · nimitjain.248@gmail.com. The data room is indexed at `investor/data-room-index.md`.
