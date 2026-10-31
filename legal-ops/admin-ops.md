# Admin and Operations: Tools, Budget, Insurance, Calendar, Governance, Risk Register

> Planning document, not legal, tax or insurance advice. Prices are third-party-reported list prices (web search, Oct 2026) or **estimates (e)**. Insurance figures are broker-published medians or ranges and must be replaced with **broker quotes**. A CPA must confirm the tax calendar.

Owner: COO.

---

## 1. Tool stack

| Function | Tool | Plan | Why |
|---|---|---|---|
| Email, docs, calendar, SSO | **Google Workspace** | Business Standard **$14/user/mo** annual ($16.80 flexible) ([EmailVendorSelection](https://www.emailvendorselection.com/google-workspace-pricing/)) | SSO for everything; Drive data room |
| Wiki / docs / handbook | **Notion** | Business ~**$20/user/mo** annual (sources conflict: $18–$20) ([Tinycommand](https://tinycommand.com/blogs/notion-pricing-2026)) | Includes Notion AI on Business |
| Issue tracking | **Linear** | Basic **$10**, Business **$16/user/mo** ([Automation Atlas](https://automationatlas.io/answers/linear-pricing-2026/)) | Engineering + hardware ECNs |
| Chat | **Slack** | Pro **$7.25/user/mo** annual ([Vendr](https://www.vendr.com/blog/slack-cost-per-user-real-pricing-by-plan-in-2026)) | Slack Connect with ODM/partners |
| Design | **Figma** | Professional ~$16–$20/editor/mo (e) [verify] | UX/UI, packaging |
| Code | **GitHub** | Team ~$4/user/mo; + Advanced Security later (e) [verify] | Monorepo, Actions CI, SBOM |
| Banking | **Mercury** (primary) + **Brex/Ramp** cards | $0 base | Treasury, cards |
| Accounting | **QuickBooks Online** (US CPA familiarity) or **Xero** (multi-currency, EU/India friendly) | QBO Plus ~$99/mo; Xero Established ~$80/mo (e) [verify] | **Choose Xero** if subsidiaries come by 2028; QBO otherwise. Outsourced bookkeeping (Pilot, Kruze, Bench-alternative) $500–$1,500/mo (e) |
| Cap table | **Carta** Launch (third parties say free/≈$280/yr ≤25 stakeholders) **or Pulley** ([CostBench](https://www.costbench.com/software/equity-management/carta/)) | 409A $1k–$5k ([Vendr](https://www.vendr.com/marketplace/carta)) | Investor standard |
| Payroll/EOR | Gusto/Justworks (US), **Deel** (international) | see `hr-hiring.md` | |
| E-sign | DocuSign / Dropbox Sign / Clerky | $10–$25/user/mo (e) | |
| Password mgmt | 1Password Business | ~$8/user/mo (e) | |
| MDM | Kandji / Fleet / Jamf Now | $4–$10/device/mo (e) | Security baseline |
| E-commerce | **Shopify** (+ Shopify Tax / Avalara) | $39–$399/mo + payments (e) | Store, pre-orders post-Kickstarter |
| Payments / subscriptions | **Stripe** Billing + Tax | 2.9% + 30¢ + Billing 0.7% (e) [verify] | LORE Pass |
| Support | **Intercom + Fin** | see `supply-chain-ops.md` | |
| Email marketing | Klaviyo | usage-based ($45–$400/mo) (e) | |
| Compliance automation | Vanta / Drata (2028) | $10k–$25k/yr (e) | SOC 2 |
| Legal docs / contract mgmt | Notion database → Ironclad/Juro later | | Contract register |
| Expense / travel | Ramp / Brex + Navan | $0–$15/user | |

### 1.1 Monthly SaaS budget (estimate)

| Item | 6 people (Q1 2027) | 15 people (Q4 2027) |
|---|---|---|
| Google Workspace | $84 | $210 |
| Notion Business | $120 | $300 |
| Linear Business | $96 | $240 |
| Slack Pro | $44 | $109 |
| Figma (2/4 editors) | $40 | $80 |
| GitHub Team | $24 | $60 |
| 1Password | $48 | $120 |
| MDM | $50 | $120 |
| Carta/Pulley | $25 | $100 |
| QBO/Xero + bookkeeping | $600 | $1,200 |
| Deel/EOR platform (excl. per-employee EOR fees) | $150 (contractors) | $300 |
| DocuSign | $45 | $75 |
| Shopify + apps | $0 (pre-launch) | $500 |
| Intercom + Fin | $0 | $600–$1,500 (volume) |
| Klaviyo | $100 | $400 |
| Cloud (AWS/GCP) + LLM APIs | $1,000–$3,000 | $4,000–$10,000 |
| Misc (Loom, Zoom, domain, status page, Sentry) | $200 | $500 |
| **Total (excl. cloud)** | **~$1,600/mo** | **~$5,000–$6,000/mo** |
| **Total incl. cloud** | **~$2.6k–$4.6k/mo** | **~$9k–$16k/mo** |

Rules: annual billing once headcount is stable; founder approves new tools > $100/mo; quarterly seat audit; every tool SSO-enabled and on the sub-processor register if it touches personal data.

---

## 2. Insurance programme

| Policy | Why | When | Limit (proposal) | Indicative premium (broker medians, not quotes) |
|---|---|---|---|---|
| **General liability (GL)** | Premises/third-party injury, events | Now | $1M / $2M agg | ~$180–$1,200/yr ([Vouch](https://www.vouch.us/blog/start-up-insurance-costs-how-much-to-pay)) |
| **Product liability** (often in GL; hardware-specific endorsements) | Battery fire, injury from device; **required by retailers, Kickstarter 3PLs and ODM contracts** | **Before beta units reach users (Q1 2027)**; scale limits at MP | $2M–$5M per occurrence (retail usually requires ≥$2M, plus vendor endorsements) | Vouch hardware range **~$7.2k–$13.9k/yr** ([Vouch](https://www.vouch.us/insurance101/hardware-company-product-liability-insurance)); rises with revenue (~$0.25 per $100 revenue for low-risk products per one source) |
| **Product recall** | Cost of a recall (logistics, replacement, notification) | Before MP (Q3 2027) | $1M–$2M | Quote needed (e: $5k–$15k/yr) |
| **Tech E&O (professional liability)** | AI narration errors, service failure, SOS failure claims (subject to exclusions) | Before Kickstarter | $1M–$3M | Median ~$3.7k/yr ([Vouch](https://www.vouch.us/blog/start-up-insurance-costs-how-much-to-pay)) |
| **Cyber** (first + third party: breach response, ransomware, regulatory fines where insurable) | Location data; CRA/GDPR | Before beta | $1M–$3M | Median ~$2.9k/yr ([Vouch](https://www.vouch.us/blog/start-up-insurance-costs-how-much-to-pay)) |
| **D&O** | Investor/board claims; seed investors expect it | At pre-seed close (now) | $1M → $2–3M at seed | Median ~$6.3k/yr; range $4k–$10k ([Vouch](https://www.vouch.us/blog/start-up-insurance-costs-how-much-to-pay), [Corgi](https://corgi.insure/blog/startup-insurance-cost-by-stage)) |
| **EPLI** | Employment claims | At first hires | $1M | $1k–$3k/yr (e) |
| Workers' comp | US employees (mandatory by state) | First US hire | statutory | via payroll |
| **Marine cargo / stock throughput** | Inventory in transit/at 3PL (5k units ≈ $0.7M–$1M cost) | Before the first MP shipment | Per-shipment value up to $1M | 0.1–0.3% of insured value (e) |
| Crime / social engineering | Wire fraud | Seed | $250k–$1M | $1k–$2k (e) |
| International (foreign GL/products, EU) | EU sales, events | 2027 | | Via the same carrier (e.g., Hiscox, Chubb, AXA XL) |

**Brokers to approach:** Vouch, Embroker, Founder Shield, Newfront, Woodruff Sawyer (hardware experience). **Budget 2027: ~$30k–$55k total premiums (e).** Key wording points: no exclusion for **lithium batteries**, AI/algorithmic outputs, or **bodily injury arising from technology failure** (critical for SOS); worldwide territory including US suits; vendor endorsements for retailers.

---

## 3. Accounting and tax calendar (US parent; calendar fiscal year)

| Date | Item |
|---|---|
| Monthly, by business day 10 | Month-end close (bank recs, accruals, inventory, deferred revenue for LORE Pass/Kickstarter); investor update |
| 15th monthly | US payroll tax deposits (per schedule); EU/UK VAT returns per registration cadence (OSS: quarterly, by the end of the month after the quarter) |
| **31 Jan** | 1099-NEC to contractors and IRS; W-2s; Q4 Form 941; **BIS encryption self-classification report (if applicable, Feb 1)** [verify] |
| **1 Mar** | **Delaware franchise tax + annual report** (Assumed Par Value method) |
| **15 Mar** | (if an S-corp or partnership; n/a) |
| **15 Apr** | **Form 1120** (or Form 7004 extension to 15 Oct) + **Form 5472** if 25% foreign-owned; Q1 estimated tax; California franchise tax (if qualified) |
| 30 Apr / 31 Jul / 31 Oct | Form 941 quarterly |
| 15 Jun / 15 Sep / 15 Dec | Federal estimated tax (once profitable) |
| **31 Jul (India FY)** | (Indian sub, later) ITR; TDS returns quarterly; GST monthly (GSTR-1/3B); **30 Sep tax audit**; transfer-pricing Form 3CEB |
| Annual | **Form D amendments** (annually if the offering continues >12 months); R&D credit study (Form 6765 with the 1120); **409A refresh** (12 months or after a material event, e.g., Kickstarter/seed); Sales-tax nexus review (economic nexus thresholds: $100k sales / 200 transactions in many states); DPF re-certification; ICO fee; trademark/patent deadlines (in the IP docket) |
| Kickstarter tax note | Funds are generally **taxable income when earned** (on delivery of rewards, under accrual accounting, as deferred revenue until shipped). Plan with the CPA: large pledge receipts in Q2 2027 with costs in Q3–Q4 2027 straddle the same fiscal year, which is good |

---

## 4. Board and governance cadence

| Stage | Board | Cadence | Content |
|---|---|---|---|
| Now (pre-seed) | 1 director (founder); **written consents** for equity grants, SAFE, policies | Monthly investor update (email); consents as needed (at least quarterly batch for option grants) | KPIs, cash runway, milestones, asks |
| Post-seed (late 2027) | 3 seats: founder (CEO) + 1 lead seed investor + 1 independent (hardware/consumer operator), or 2+1 | **Quarterly board meeting** (90–120 min) + monthly KPI email | Board pack 5 days ahead: CEO letter, financials vs budget, cash runway, hiring, product/hardware gate status, Kickstarter delivery, risk register top 10, legal/compliance update, approvals (options, budget) |
| Annual | Stockholder consent/meeting; approve budget (Dec); 409A; D&O review; auditor (if required by investors at Series A) | | |

**Governance hygiene:** minute book in the data room; option grants only by board approval at 409A FMV; conflicts of interest policy; related-party transactions disclosed; delegation-of-authority matrix (spend >$25k = CEO + COO; >$100k = board-approved budget; ODM POs within the approved build plan).

**Policies to adopt by Q1 2027:** Code of conduct; anti-bribery (FCPA/UKBA, given gifts/facilitation risks with factories); sanctions/export; whistleblower; information security; privacy; travel and expense; delegation of authority; document retention; insider trading (later).

---

## 5. Risk register: top 25

L = likelihood, I = impact (1–5). Score = L×I. Owners: CEO, COO, HW (Hardware lead), SW (Software lead), FIN, GTM.

| # | Risk | L | I | Score | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | **Trademark conflict on "LORE"** (Epic Games, Pixite, Sunbird, YLORE filings) forces a rename after packaging/Kickstarter | 4 | 4 | **16** | Full clearance by Dec 2026; compound mark (e.g., LORE TRAVEL); CN filing; contingency name | COO |
| 2 | **Hardware schedule slip** (EVT→MP) delays Kickstarter delivery beyond Q4 2027 | 4 | 5 | **20** | Pre-certified modules; experienced ODM; buffer in promised dates (promise Q1 2028 for Atlas); honest updates | HW |
| 3 | **Certification failure/re-test** (SAR, RED cyber EN 18031, carrier PTCRB) | 3 | 4 | 12 | Pre-scans at EVT; antenna margin; NB early engagement; 20% budget contingency | HW |
| 4 | **EU battery removability (Feb 2027)** non-compliance for sealed designs | 3 | 4 | 12 | ID decision by Dec 2026; derogation analysis; replaceable battery design | HW/COO |
| 5 | **US tariff changes** (Section 301/122/232; origin rules) raise landed cost 10–30% | 4 | 3 | 12 | Non-China assembly option; price buffer; CBP ruling; DDP pricing reviews | COO/FIN |
| 6 | **Cash runway** shortfall before seed (pre-seed $1.5M covers ~12–15 months at plan) | 3 | 5 | 15 | Monthly runway review; milestone-based hiring; Kickstarter target sized to fund MP; bridge SAFE option | CEO/FIN |
| 7 | **Kickstarter underfunds** (target not met or lower volume than MOQs) | 3 | 4 | 12 | Pre-launch list ≥20–30k emails; deposit reservations; realistic goal; MOQ negotiation | GTM |
| 8 | **ODM IP leakage / clones** | 3 | 4 | 12 | NNN contract; CN trademarks; split firmware signing; design patents | COO |
| 9 | **Component shortage / LTE module EOL** | 3 | 4 | 12 | LLT buys; second-source module footprint; lifecycle (LTB) clauses | HW |
| 10 | **eSIM partner failure / permanent-roaming blocks / cost overrun on data** | 3 | 4 | 12 | SGP.32 eIM for portability; two partners evaluated; fair-use caps; pricing per zone in LORE Pass economics | COO |
| 11 | **Safety incident** (battery fire, SOS failure leading to harm) → injury, lawsuit, recall | 2 | 5 | 10 | IEC 62133-2/UL cells; BMS; QA; clear SOS disclaimers; product liability + recall insurance; incident response | HW/COO |
| 12 | **AI hallucination/defamation** (false history, false claims about a business) → reputational/legal | 3 | 3 | 9 | Fact-grounding + verifier; editorial review; correction process; E&O insurance | SW |
| 13 | **Privacy breach of location data** | 2 | 5 | 10 | On-device default; encryption; pen-tests; minimal retention; cyber insurance; breach plan | SW/COO |
| 14 | **Misuse for stalking** → press scandal, regulatory scrutiny | 2 | 4 | 8 | Anti-stalking design (LEDs, reminders, auto-expiry, unwanted-tracker alerts) | SW |
| 15 | **Open-source / data licence breach** (ODbL share-alike, CC BY-SA, Llama terms) | 3 | 3 | 9 | Licence register; separate databases; attribution screens; SBOM scans | SW/COO |
| 16 | **Patent assertion by incumbents/NPEs** (location audio, SEPs) | 2 | 4 | 8 | FTO screen; SEP licences via modules; provisional filings for defensive value | COO |
| 17 | **Key-person dependency** (solo founder) | 3 | 5 | 15 | Hire strong founding team; documented decisions; key-person insurance at seed; co-founder search | CEO |
| 18 | **Hiring delays for firmware/RF talent** | 3 | 4 | 12 | India/EU hubs; contractors; competitive equity; recruiter | CEO/COO |
| 19 | **Founder's Indian residency / FEMA ODI issues** block an Indian subsidiary or create penalties | 3 | 3 | 9 | Indian counsel opinion before incorporation; EOR instead of subsidiary | COO |
| 20 | **Regulatory change** (CRA, AI Act, Data Act, PLD) increases compliance cost | 4 | 2 | 8 | Compliance matrix review quarterly; build privacy/security by design | COO |
| 21 | **Fulfilment errors / DG shipping refusals** at peak | 3 | 3 | 9 | DG-trained 3PL; documentation pack; pilot shipments in DVT; buffer weeks | COO |
| 22 | **High returns/warranty claims** (new product) | 3 | 3 | 9 | QA gates; 3.5% reserve; ODM epidemic-failure clause; clear onboarding to reduce "no fault found" returns | HW/COO |
| 23 | **Subscription-law non-compliance** (auto-renew, cancellation) → fines/chargebacks | 2 | 3 | 6 | Checkout checklist; legal review; easy cancel | COO |
| 24 | **Content supply bottleneck** (20 cities by 2028 with checked facts) | 3 | 4 | 12 | Contributor network + licensing template; AI-assisted pipeline with human fact-check; prioritise cities | SW/Content |
| 25 | **FX and payment risk** (USD/CNY/EUR; ODM deposits; Kickstarter payouts) | 2 | 2 | 4 | Wise/Airwallex; hedge large POs; deposit escrow | FIN |

Review: monthly by the COO; top 10 in each board pack; re-score after each hardware gate.

---

## Sources
- Google Workspace: https://www.emailvendorselection.com/google-workspace-pricing/
- Slack: https://www.vendr.com/blog/slack-cost-per-user-real-pricing-by-plan-in-2026
- Notion: https://tinycommand.com/blogs/notion-pricing-2026
- Linear: https://automationatlas.io/answers/linear-pricing-2026/
- Carta: https://www.costbench.com/software/equity-management/carta/ ; https://www.vendr.com/marketplace/carta
- Insurance: https://www.vouch.us/blog/start-up-insurance-costs-how-much-to-pay ; https://www.vouch.us/insurance101/hardware-company-product-liability-insurance ; https://corgi.insure/blog/startup-insurance-cost-by-stage
- Delaware franchise tax: https://bench.co/blog/tax-tips/delaware-franchise-tax
