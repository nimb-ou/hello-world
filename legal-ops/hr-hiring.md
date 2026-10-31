# HR and Hiring Plan

> Planning document, not legal advice. Employment counsel must review the employment terms in each country. Salary figures are **benchmarks from web sources (Payscale and similar aggregators, Oct 2026)** or Ops **estimates** where marked. Finance must validate them against the operating budget in `finance/`. Equity bands are **market-convention estimates** for a pre-seed/seed hardware startup. Validate with Carta Total Compensation or Pave data once subscribed.

Owner: COO (People). Decision: CEO.

---

## 1. Org design by stage

| Stage | Headcount | Shape |
|---|---|---|
| **Pre-seed (now → Q2 2027)**, $1.5M SAFE | Founder + **5–6** FTE/contractors | Founder (CEO/product) · Firmware/embedded lead · Mobile/backend engineer · ML/story-engine engineer · Hardware/EE lead (contract → FTE) · Content editor (Rome, contract) · Ops/legal via COO/fractional |
| **Kickstarter → seed ($6M, H2 2027)** | **12–16** | + Industrial/product designer · Supply chain & quality manager (Asia) · Growth/community lead · Support lead · Second firmware engineer · QA/test engineer · Map/data engineer |
| **2028 (retail + 20 cities)** | 25–35 | + City content team (editors per region) · B2B sales · Finance lead · Security engineer · Data/analytics · More support (BPO) |

**Location strategy:** remote-first, overlapping hours **CET ±3h** (Rome/Lisbon/London/India IST overlap mornings; US East Coast afternoons). Hubs: **Lisbon (EU)**, **Bangalore (firmware/hardware, cost)**, **Shenzhen (supply chain, 1–2 people via EOR or agent)**, **US (founder/GTM, as needed)**.

---

## 2. First 12 hires

| # | Role | When | Where (proposal) | Mission and responsibilities | Must-haves |
|---|---|---|---|---|---|
| 1 | **Founding Embedded/Firmware Lead** | Nov 2026 | Bangalore or Lisbon | Own device OS (Zephyr/FreeRTOS or Linux), BLE LE Audio, power management, sensor drivers (GNSS L1/L5, IMU), secure boot/OTA | 7+ yrs embedded C/C++, shipped a BLE/LTE consumer device, low-power design |
| 2 | **Founding ML / Story-Engine Engineer** | Nov 2026 | EU / remote | On-device LLM (1–4B) quantisation, RAG over City Packs, fact verifier, TTS/ASR, eval harness | LLM fine-tuning + on-device inference (llama.cpp/ExecuTorch/MLC), evals |
| 3 | **Mobile + Backend Engineer** | Dec 2026 | EU / India | Companion app (React Native/Flutter or native), account/subscription backend, eSIM partner integration, Stripe | Shipped consumer apps; payments; BLE in mobile |
| 4 | **Hardware/Electrical Engineering Lead** | Jan 2027 (contract from Nov) | Bangalore / Shenzhen / Taipei | Schematics, RF/antenna with the ODM, certification strategy, BOM cost | Shipped LTE wearables; FCC/CE experience |
| 5 | **Sensor-Fusion / Map Vision Engineer** | Jan 2027 | EU / India | Heading fusion, PDR, map-matching, street-side detection, field testing in Rome | Kalman/particle filters; GNSS; OSM data |
| 6 | **Content Editor-in-Chief (City Packs)** | Jan 2027 | Rome / Lisbon | Editorial standards, fact-checking, contributor network, story style guide, AI-edit workflow | Journalism/history background; editorial management; Italian + English |
| 7 | **Supply Chain & Quality Manager** | Mar 2027 | Shenzhen (EOR) / HK | ODM management, NPI, AQL, LLT purchasing, logistics, DG shipping | 5+ yrs consumer-electronics NPI in China; Mandarin |
| 8 | **Industrial / Product Designer** | Mar 2027 (contract earlier) | Lisbon / London / Milan | CMF, DFM with the ODM, packaging, accessories | Shipped premium hardware (Leica / Teenage Engineering-level taste) |
| 9 | **Growth & Community Lead (Kickstarter)** | Feb 2027 | US / UK / EU | Kickstarter campaign, community (Discord), creators, email, PR coordination | Ran a $1M+ hardware crowdfunding campaign |
| 10 | **QA & Test Engineer (HW/SW)** | Apr 2027 | India / EU | Test plans, field-testing programme, automated firmware tests, beta management | Device QA, test automation, RF/GNSS field test |
| 11 | **Customer Support Lead** | Jun 2027 | Lisbon / remote | Help centre, Intercom/Fin, BPO management, RMA process, safety escalations | Built support for a hardware launch |
| 12 | **Finance & Operations Manager** | Jul 2027 | US / EU | Accounting close with the outsourced CPA, AP, inventory accounting, sales tax/VAT, payroll/EOR admin, insurance | Startup finance generalist; hardware/inventory exposure |

Contract-first options (de-risk): industrial design studio, RF/antenna house, fractional CFO, fractional General Counsel (~$5k–$10k/month or hourly), patent/trademark attorneys, BPO support.

---

## 3. Salary benchmarks (base, annual)

> Sources: Payscale 2026 city pages (San Francisco, Bangalore, Berlin) and salary blogs for Amsterdam. Many figures are averages, not startup offers. Other cells are **Ops estimates** marked (e). Startups typically pay 10–20% below big tech in cash and make up the gap with equity.

| Role (senior IC unless noted) | US (SF/NYC) | EU (Lisbon) | EU (Berlin/Amsterdam) | India (Bangalore) |
|---|---|---|---|---|
| Firmware/embedded (senior) | **$148k–$190k** (Payscale senior firmware SF range) ([Payscale](https://www.payscale.com/research/US/Job=Senior_Firmware_Engineer/Salary/72862908/San-Francisco-CA)); mid ~$110k–$130k ([Payscale](https://www.payscale.com/research/US/Job=Firmware_Engineer/Salary/9078951e/San-Francisco-CA)) | €50k–€70k (e) | €75k–€95k (e) | **₹20–30 LPA** experienced (Payscale avg experienced senior ₹20.6 LPA; Linux-skilled ~₹27 LPA) ([Payscale](https://www.payscale.com/research/IN/Job=Senior_Embedded_Software_Engineer/Salary/efda3115/Experienced-Bangalore)); founding lead ₹35–50 LPA (e) |
| ML engineer (senior) | $180k–$240k (e) | €55k–€80k (e) | Berlin Payscale avg **€83k–€88k**; blogs €90k–€135k ([Payscale](https://www.payscale.com/research/DE/Job=Senior_Machine_Learning_Engineer/Salary/64d883b4/Berlin), [JobRise](https://jobrise.io/en/blog/ai-engineer-salary-berlin-2026/)); Amsterdam senior €90k–€120k ([CareerCheck](https://www.careercheck.io/blog/ml-engineer-salary-amsterdam-2026)) | ₹30–55 LPA (e) |
| Mobile/backend (senior) | $160k–$200k (e) | €45k–€65k (e) | €70k–€90k (e) | ₹22–40 LPA (e) |
| Hardware/EE lead | $160k–$210k (e) | €55k–€75k (e) | €75k–€95k (e) | ₹30–50 LPA (e) |
| Industrial designer | $130k–$170k (e) | €40k–€60k (e) | €60k–€80k (e) | ₹18–30 LPA (e) |
| Supply chain/quality mgr (Shenzhen) | — | — | — | CN: ¥300k–¥500k RMB (e) |
| Content editor-in-chief | $90k–$120k (e) | €35k–€50k (e); Rome €35k–€50k (e) | €50k–€65k (e) | ₹12–20 LPA (e) |
| Growth/community lead | $130k–$170k (e) | €40k–€60k (e) | €60k–€80k (e) | — |
| Support lead | $70k–$95k (e) | €30k–€40k (e) | €40k–€55k (e) | ₹8–14 LPA (e) |
| Finance & ops manager | $100k–$140k (e) | €40k–€55k (e) | €55k–€75k (e) | ₹15–25 LPA (e) |
| Founder/CEO (post pre-seed) | $90k–$140k (e; pre-seed founder norm) | | | |

**Employer on-costs (planning):** US +20–30% (benefits, payroll tax); Portugal +23.75% social security; Germany ~+21%; Netherlands ~+20–30%; India +12–15% (PF, gratuity, insurance) (e) [verify].

---

## 4. Equity bands (options, % of fully diluted at grant; 4-yr/1-yr cliff)

| Level | Pre-seed hires (#1–5) | Seed hires (#6–16) | Series A+ |
|---|---|---|---|
| Founding engineer / lead | **1.0–2.0%** | 0.5–1.0% | 0.2–0.5% |
| Senior IC | 0.5–1.0% | 0.25–0.6% | 0.1–0.25% |
| Mid IC | 0.25–0.5% | 0.1–0.3% | 0.05–0.15% |
| Manager (supply chain, support lead, finance) | 0.3–0.75% | 0.2–0.5% | 0.1–0.2% |
| Advisors (FAST-style) | 0.15–1.0% | 0.1–0.5% | — |

**Pool:** 12% at incorporation (1.2M shares), refreshed to 10–12% post-seed. **First-12 usage estimate: ~7–9%.**
**Policy:** cash/equity choice offered for senior hires (e.g., −10% cash for +25% equity); **extended exercise window** (5 years post-termination for ≥2 yrs' service) as a talent advantage (converts ISOs to NSOs after 90 days); international grants via EIP sub-plans (India: perquisite tax at exercise; Portugal/Germany: taxed at exercise; UK: unapproved options or CSOP) [verify per country].

---

## 5. Hiring process (target 3–5 weeks)

1. **Intake:** scorecard with outcomes for months 3, 6 and 12; must-haves; level; budget; legal checks (pay-range disclosure requirements: CA, NY, WA, CO, IL; **EU Pay Transparency Directive (EU) 2023/970 transposition by 7 Jun 2026**, which requires a pay range in job ads or before the interview and bans asking about salary history) [verify national status].
2. **Sourcing:** founder network, Wellfound, LinkedIn, Hacker News "Who's hiring", embedded communities (Zephyr, Hackaday), hardware Slack groups, Rome universities (content), Shenzhen sourcing agents. Referral bonus $2k / €2k / ₹1L.
3. **Screen** (30 min, CEO or COO): motivation, logistics, comp range.
4. **Technical deep-dive** (60–90 min) with a real LORE problem (e.g., "Estimate street side from noisy GNSS + IMU", "BLE LE Audio latency budget", "Write a 30-second story about the Pantheon from these 6 facts with sources").
5. **Paid take-home or work trial** (≤4 hrs, paid at a fair rate; or a 1-day paid trial for contractors).
6. **Values interview + founder close.**
7. **References** (2, incl. one manager) + background check where lawful.
8. **Offer** within 48h of the final interview (template: `templates/offer-letter.md`); CIIAA; equity approval at the next board consent.
9. **Onboarding:** day-1 accounts (SSO), hardware kit + a LORE prototype, buddy, 30/60/90 plan, security and privacy training (incl. AI Act Art. 4 AI-literacy record), a Rome field-test trip in the first 90 days for product roles.

**Fairness and compliance:** structured interviews, consistent scorecards, diverse panels, EEO statement (US), accessible process, candidate data retention 6–12 months (GDPR; consent to keep longer).

---

## 6. Culture and values (draft for the Founder; align with `company/` handbook)

1. **Tell the true story.** Facts, sources and honesty, in our product and with each other. No invented history, no invented metrics.
2. **Eyes up.** Design for presence and safety. If a feature makes someone look down at the wrong moment, it's wrong.
3. **Quiet confidence.** Calm craft over hype. Quiet luxury, warm voice.
4. **Walk the streets.** Test in the real world. Every product person field-tests in a city each quarter.
5. **Own it end to end.** From the BOM to the backer's doorstep.
6. **Respect privacy like it's ours.** Location is sacred.
7. **Kind and direct.** Disagree in the doc, commit in the meeting.

Rituals: weekly written update (Notion), Monday planning (Linear), monthly demo + "story of the month", quarterly in-person offsite in a LORE city.

---

## 7. Remote work policy (summary)

- **Remote-first;** core overlap **10:00–14:00 CET**; async by default (Notion docs, Loom).
- **Work location:** employees must work from their contracted country. **Working from another country >30 days/year needs approval** (tax, PE and immigration risk). The EOR checks each request.
- **Equipment:** laptop (MDM-managed) + monitor/peripherals budget $1,000; internet stipend $50/month; co-working allowance up to $250/month on request.
- **Security:** company devices only for company data; FileVault/BitLocker; 1Password; no public-Wi-Fi without VPN for admin access.
- **Travel:** a quarterly offsite; field-testing trips per the travel policy (economy class < 6h flights).
- **Time off:** 25 days + public holidays (minimum, or more where local law requires); **mandatory 2 consecutive weeks/year** encouraged.
- **Right to disconnect:** respect local law (e.g., Portugal's "right to disconnect" rules in Labour Code art. 199-A; France) [verify]. No expectation of replies outside working hours except on-call.
- **On-call:** rota with compensation per local law.

---

## 8. Payroll, EOR and contractors

| Need | Solution | Indicative cost |
|---|---|---|
| US employees | **Gusto / Justworks (PEO) / Rippling** | Gusto ~$49/mo + $6–$12/employee (e) [verify]; PEO ~$60–$120/employee/month (e) |
| Non-US employees (pre-entity) | **EOR: Deel / Remote / Oyster / Multiplier / Remofirst** | **Deel EOR ~$599/employee/month** ($499 billed annually); **Remote EOR ~$699/month (monthly) / $599 annual** ([Gloroots](https://gloroots.com/blog/deel-pricing), [CostBench](https://costbench.com/compare/deel-vs-remote), [CASRAI](https://casrai.org/guides/remote-com-pricing)); Multiplier ~$400, Remofirst from $199 (same sources) |
| Contractors | **Deel Contractor (~$49/contractor/mo)** or Remote (from $29/mo) ([Gloroots](https://gloroots.com/blog/deel-pricing), [Gloroots Remote](https://www.gloroots.com/blog/remote-pricing)) | |
| India team ≥5 FTE | **Indian subsidiary** (see `incorporation.md` §10; subject to the ODI restriction in §9) + local payroll (Keka/Razorpay Payroll) | Breakeven vs EOR at ~5–6 heads (e) |
| Portugal/EU team ≥3 in one country | Local entity + payroll provider | |

**Recommendation:** Deel (single platform for EOR + contractors + equity-tracking integrations) for 2026–27. Negotiate the annual rate (~$499) for ≥3 EOR seats. Remote is a close alternative (IP protections and strong EOR entities). Get quotes from both.

**Compliance musts:** I-9/E-Verify (US, where applicable); workers' comp (US states); payroll tax registrations in each US state with employees; EU social security A1 certificates for cross-border travel; India PF/ESI/PT via the EOR; GDPR employee privacy notice; handbook per country; harassment training (CA, NY, IL mandatory).

---

## Sources
- Payscale (SF firmware): https://www.payscale.com/research/US/Job=Firmware_Engineer/Salary/9078951e/San-Francisco-CA ; https://www.payscale.com/research/US/Job=Senior_Firmware_Engineer/Salary/72862908/San-Francisco-CA
- Payscale (Bangalore embedded): https://www.payscale.com/research/IN/Job=Senior_Embedded_Software_Engineer/Salary/efda3115/Experienced-Bangalore ; https://www.payscale.com/research/IN/Job=Senior_Embedded_Software_Engineer/Salary/2be24b8d/Experienced-Bangalore-Linux
- Berlin/Amsterdam ML: https://www.payscale.com/research/DE/Job=Senior_Machine_Learning_Engineer/Salary/64d883b4/Berlin ; https://jobrise.io/en/blog/ai-engineer-salary-berlin-2026/ ; https://www.careercheck.io/blog/ml-engineer-salary-amsterdam-2026
- EOR pricing: https://gloroots.com/blog/deel-pricing ; https://www.gloroots.com/blog/remote-pricing ; https://costbench.com/compare/deel-vs-remote ; https://casrai.org/guides/remote-com-pricing
- FAST advisor grid: https://fi.co/fast
