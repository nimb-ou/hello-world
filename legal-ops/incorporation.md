# Incorporation Plan: LORE Labs, Inc. (Delaware C-corp)

> **DRAFT. NOT LEGAL OR TAX ADVICE.** LORE Labs Legal & Ops prepared this working plan. No lawyer has reviewed it. A qualified US corporate lawyer, plus a US tax adviser (and Indian FEMA/tax counsel if the founder is resident in India), must review it before anything is filed or signed. We checked fees, thresholds and dates by web search on **30 Oct 2026**. They change often, so check each one against the official source on the day you file.

Owner: COO / Head of Legal, Admin & Ops. Decision-maker: Founder (Nimit Jain).
Target: incorporated, banked and SAFE-ready **before the first pre-seed money arrives (Q4 2026)**.

---

## 1. Why a Delaware C-corp

| Factor | Delaware C-corp | Delaware/other LLC | Indian Pvt Ltd first |
|---|---|---|---|
| US VC / YC SAFE compatibility | Standard. Every US investor expects it | Most VCs cannot invest (fund tax issues, UBTI) | Needs a later "flip", which is costly and taxable in India |
| Stock options (ISOs) and the 409A regime | Yes | No ISOs; profits-interest units are awkward | ESOPs under Companies Act; US hires can't get ISOs |
| QSBS (IRC §1202) gain exclusion for founders and investors | Yes (see §6) | No | No |
| Court of Chancery / settled case law | Yes | Yes | n/a |
| Kickstarter / Stripe / Shopify / Amazon US | All straightforward | Yes | Harder for US payouts |
| Annual cost (min.) | ~$400–$1,000 Delaware tax and report + registered agent | $300–$400 flat tax | ROC filings, audit mandatory |

**Decision:** Delaware C-corp named **"LORE Labs, Inc."** We may add an Indian and/or EU subsidiary later (§10).

> Name availability: check the Delaware Division of Corporations entity-name search before filing. A free name check does not clear the trademark. See `ip-strategy.md`. Plan a backup name such as "Lore Travel Labs, Inc." in case the first is taken.

---

## 2. Three ways to incorporate

| | **Stripe Atlas** | **Clerky** | **Direct with a law firm** (e.g. Cooley GO docs, Gunderson, Orrick, Wilson Sonsini, Goodwin; or a boutique) |
|---|---|---|---|
| Price | **$500 one-off**; reviews say it covers Delaware filing fees, 1st-year registered agent, EIN application, founder stock purchase docs and the 83(b) filing ([Rho review](https://www.rho.co/blog/stripe-atlas-review), [WP Simple Pay](https://wpsimplepay.com/is-stripe-atlas-worth-the-money/)) | **$427** pay-per-use incorporation; **$819** "Company Lifetime Package" incl. post-incorporation setup, stock plan and unlimited standard docs ([Startup Savant](https://startupsavant.com/service-reviews/stripe-atlas-vs-clerky), [Flowjam](https://www.flowjam.com/blog/clerky-review-2026-complete-guide-pricing-alternatives)) | $0 upfront on deferred-fee terms at many startup firms; typically **$3k–$10k** of work billed later or capped (estimate) |
| Registered agent after yr 1 | ~$100/yr (estimate from reviews) | Third-party, ~$50–$300/yr | Firm's provider |
| Non-US founder friendly | Very (EIN without SSN, bank intro) | Good | Good |
| Equity plan / board consents | Basic | Strong. Built by startup lawyers; the paper trail investors like | Strongest, with a human review |
| Best for | Speed; a solo non-US founder | A clean paper trail at low cost | Complex facts (Indian residency, co-founders with prior IP, hardware IP from an employer) |

**Recommendation:** **Clerky Lifetime ($819)** *or* a startup law firm on deferred fees, if counsel will advise on the Indian residency / ODI question (§9). Use Stripe Atlas only if speed matters most and no Indian-resident complications apply. The real costs are a messy cap table and a missing 83(b), not the $300 difference in fees.

---

## 3. The incorporation package (what must exist on day 1)

| # | Document | Notes | Owner |
|---|---|---|---|
| 1 | Certificate of Incorporation | Authorise **10,000,000 shares of Common Stock, par $0.00001** (or $0.0001). Low par plus a high share count keeps the franchise tax low under the Assumed Par Value Capital method. No preferred stock yet; it is created at the seed round. | Counsel / platform |
| 2 | Bylaws | Standard; board of 1 (founder) at start | Counsel |
| 3 | Action of Incorporator | Appoints the first director(s) and adopts the bylaws | Counsel |
| 4 | Initial Board Consent | Officers (CEO/President, Secretary, Treasurer, all Nimit at first), fiscal year (Dec 31), bank authority, founder stock issuance, IP assignment, equity incentive plan, indemnification agreements, EIN, registered agent, foreign qualification | Counsel |
| 5 | Founder Restricted Stock Purchase Agreement (RSPA) | 4-yr vesting / 1-yr cliff, company repurchase right; see §5 and `templates/founder-agreement.md` | Founder + counsel |
| 6 | Technology / IP Assignment from founder | Assigns all pre-incorporation LORE work (code in this repo, Map Vision designs, story engine, brand, domain lore.travel, City Pack data work) | Founder |
| 7 | CIIAA for the founder (as employee/officer) | `templates/ciiaa.md` | Founder |
| 8 | Stockholder consent adopting the Equity Incentive Plan (EIP) | Reserve **1,000,000–1,500,000** shares (10–15% fully diluted) | Board + stockholders |
| 9 | Indemnification Agreement (director/officer) | Investors expect it at seed | Counsel |
| 10 | 83(b) election (filed ≤30 days after stock issuance) + proof of filing | §5 | Founder (critical!) |
| 11 | EIN confirmation letter (CP 575) | §7 | Platform / Founder |
| 12 | Stock ledger / cap table on Carta, Pulley or Clerky | `admin-ops.md` | COO |

### Suggested initial capitalisation (illustrative; counsel to confirm)

| Holder | Shares | % issued | Price | Paid |
|---|---|---|---|---|
| Nimit Jain (founder), Common, vesting | 8,000,000 | 100% | $0.00001/sh (par) | $80 cash (or cash plus the IP assignment as consideration) |
| Equity Incentive Plan, reserved (unissued) | 1,200,000 | — | — | — |
| Authorised but unreserved | 800,000 | — | — | — |
| **Total authorised** | **10,000,000** | | | |

At the $1.5M SAFE on a $12M **post-money** cap, SAFE holders convert to about **12.5%** of the company capitalisation at the priced round (1.5 / 12). The post-money cap includes the pool and the converting SAFEs, so the founder carries that dilution. Finance models this in `finance/`. Pre-seed SAFEs need **no** amendment to the Certificate; they convert into the seed preferred stock.

**If a co-founder joins later:** issue their stock under a separate RSPA, with fresh 4-year vesting and their own 83(b). Re-run `templates/founder-agreement.md`.

---

## 4. Step-by-step timeline and cost

| Week | Step | Detail | Cost (est.) |
|---|---|---|---|
| W0 | Decide platform; collect info | Legal name; founder legal name/address/ID; authorised shares; registered agent; business description ("consumer electronics and software") | — |
| W0 | Delaware filing | Platform files the Certificate of Incorporation. Note: **Delaware raised its filing fees effective 1 Aug 2026 (House Bill 400)**. Secondary sources disagree on the new base incorporation fee (one says $109 plus expedite options, another says some fees rise to $200) ([Delaware fee schedule Aug 2026](https://corpfiles.delaware.gov/Fee_Schedule/AugustFee2026.pdf), [HB 400](https://corpfiles.delaware.gov/2026_Legislation/House_Bill_400.pdf), [InCorp summary](https://www.incorp.com/resources/knowledge-base/delaware-business-filing-fee-increase)). Platforms bundle it. | Included / ~$100–$300 |
| W0–1 | Board consent; founder RSPA; IP assignment; CIIAA | Sign electronically (DocuSign or the platform) | Included |
| **W0–W4 (≤30 days from stock grant)** | **File 83(b)** | Online via IRS **Form 15620** (live since July 2025) or by certified mail. §5 | $0 (+$10 certified mail if paper) |
| W1–W6 | EIN | US-SSN holder: online, same day. Non-US founder without SSN: Form SS-4 by fax/phone, usually 1–6 weeks; Atlas and Clerky can speed this up | $0 |
| W1–W6 | Bank account | Mercury / Brex / SVB (First Citizens); see §8 | $0 |
| W2 | Registered agent confirmed; Delaware "Registered Agent" on file | Required by law; many cheap providers | $50–$300/yr |
| W2–4 | Foreign qualification | Register to do business wherever the company actually operates (founder's state of residence / office). In California this triggers the **$800 minimum CA franchise tax** from year 2. Not needed if no US-state nexus beyond Delaware. | $0–$300 + state tax |
| W2–4 | Cap table platform | Carta Launch / Pulley / Clerky; upload all docs | $0–$280/yr |
| W3–6 | SAFE paperwork | YC post-money SAFE; see `templates/safe-summary-note.md` | Counsel review $1k–$3k (est.) |
| Before first option grant | **409A valuation** | Needed before granting options; $1k–$5k ([Carta 409A cost survey, Vendr](https://www.vendr.com/marketplace/carta), [Eqvista](https://eqvista.com/?p=39499)) | $1k–$3.5k |
| Before 1 Mar 2027 | Delaware Annual Franchise Tax Report | §6 | ~$450–$900 |
| Before 15 Apr 2027 | Federal Form 1120 (+ Form 5472 if 25% foreign-owned) | §6 | CPA $1k–$3k |

**All-in year-1 setup cost (estimate): $1,500–$4,500** (platform + registered agent + 409A + franchise tax + CPA), excluding law-firm review of the SAFE and any Indian ODI compliance work.

---

## 5. Founder stock, vesting and the 83(b) election

### 5.1 Vesting terms (standard, investor-friendly)
- **4 years, 1-year cliff, monthly thereafter** (25% vests at month 12, then 1/48 per month).
- Vesting credit: the founder may get **up to 6–12 months of credit** for pre-incorporation work (since about mid-2026). Investors usually accept up to ~25% credit. Counsel to advise.
- **Acceleration:** **double-trigger** only: 100% (or 50%) of unvested shares accelerate if (a) there is a change of control **and** (b) the founder is terminated without Cause or resigns for Good Reason within 12 months. Avoid single-trigger; it makes acquisitions harder.
- **Repurchase right:** the company may buy back *unvested* shares at the lower of cost or fair market value if the founder leaves.
- Transfer restrictions, a right of first refusal, and a lock-up are in the bylaws and the RSPA.

### 5.2 83(b) election: never miss it
- The founder buys **restricted** stock. Without an 83(b), each vesting tranche is taxed as **ordinary income** at its value on the vesting date. At a $12M post-money cap that is a large tax bill on illiquid shares.
- With the 83(b), the founder elects to be taxed **now** on (FMV − price paid) = **$0** if bought at FMV, and the capital-gains holding period starts now. It also starts the QSBS clock.
- **Deadline: 30 calendar days from the stock issuance date. No extensions, no cure.**
- **How to file (2026):** IRS **Form 15620** may now be filed **online** via an IRS online account, which gives immediate confirmation of receipt. Paper filing by certified mail (return receipt) to the IRS service centre for the taxpayer's region is still allowed ([Morrison Foerster](https://www.mofo.com/resources/insights/250724-say-goodbye-to-paper-cuts-section-83-b), [Goodwin](https://goodwinlaw.com/en/insights/publications/2025/07/alerts-practices-erisa-online-filing-of-section-83b-elections), [Alston & Bird](https://www.alston.com/en/insights/publications/2025/08/irs-online-filing-section-83b-elections)).
  - The online form asks you to confirm you have **not** already mailed an election for the same shares. Don't file twice.
  - Give a **copy to the company**. Keep proof (online confirmation PDF or certified-mail receipt) in the data room: `Data Room/01 Corporate/83(b)`.
- **Non-US-taxpayer founder:** an 83(b) can still be filed with "Foreign" or no SSN on a paper filing. A US tax adviser must confirm. If the founder is an Indian tax resident, see §9: Indian tax treats the shares differently, and the 83(b) is mainly for future US tax residency and QSBS.

### 5.3 Checklist
- [ ] RSPA signed; price paid (wire from the founder's personal account, keep proof)
- [ ] Stock issuance date recorded in the board consent = start of the 30-day clock
- [ ] 83(b) filed on day ≤ 10 (don't wait)
- [ ] Copy to company records; record on cap table
- [ ] Calendar reminder for the 1-year cliff date

---

## 6. Tax and compliance after formation

| Obligation | When | Notes |
|---|---|---|
| **Delaware Annual Franchise Tax + Annual Report** | **1 March** every year (first: 1 Mar 2027 for CY2026) | Use the **Assumed Par Value Capital Method** (minimum $400), not the default Authorised Shares Method (which would bill ~$85k on 10M shares). Annual report fee historically **$50** ([JD Supra](https://jdsupra.com/legalnews/delaware-franchise-tax-for-startups-3219380), [Bench](https://bench.co/blog/tax-tips/delaware-franchise-tax)). Check whether HB 400 changed the report fee for 2027 filings. **Worked example (estimate):** gross assets $1.4M (31 Dec 2026, SAFE cash in bank), issued shares 8M → assumed par $0.175/sh × 10M authorised = $1.75M assumed-par capital → $400 per $1M or part thereof = **$800 tax + report fee**. Late penalty $200 + 1.5%/month interest. |
| Registered agent renewal | Anniversary | $50–$300 |
| Federal corporate return Form 1120 | 15 April (calendar-year) | Even with zero revenue. **Form 5472 + pro forma** if a 25%+ foreign owner (likely, if the founder is non-US). Penalty for not filing 5472: **$25,000** per form |
| State returns | Varies | California $800 minimum if qualified there |
| BOI report (FinCEN CTA) | — | FinCEN's March 2025 interim rule **exempted US-formed companies** from BOI reporting; only foreign companies registered in the US must file. Recheck at formation. |
| QSBS (§1202) tracking | Ongoing | For stock issued **after 4 Jul 2025**, the One Big Beautiful Bill Act gives a tiered exclusion: **50% after 3 yrs, 75% after 4 yrs, 100% after 5 yrs**; per-issuer cap **$15M** (inflation-indexed) or 10× basis; gross-asset limit **$75M** at issuance ([Gibson Dunn](https://www.gibsondunn.com/focus-on-qsbs-provisions-in-the-one-big-beautiful-bill-act/), [Perkins Coie](https://perkinscoie.com/insights/update/significant-changes-one-big-beautiful-bill-act-qualified-small-business-stock), [Crowell](https://crowell.com/en/insights/client-alerts/the-one-big-beautiful-bill-act-expands-favorable-qsbs-treatment)). Keep gross-asset records at each issuance. Only US taxpayers benefit. |
| R&D tax credit (Form 6765) | With 1120 | Up to $500k/yr can offset **payroll** tax for qualified small businesses. Very relevant to hardware/firmware R&D. Use a specialist (e.g., Neo.Tax, MainStreet) |
| 1099-NEC for US contractors | 31 January | Collect W-9s at onboarding; W-8BEN for non-US contractors |
| Sales tax / VAT | From first sale | Handled via Shopify Tax / Stripe Tax / Avalara; Kickstarter VAT note in `supply-chain-ops.md` |

---

## 7. EIN
- **With SSN/ITIN:** apply online at IRS.gov (EIN Assistant), weekdays, instant.
- **Without SSN (non-US founder):** Form **SS-4**, "Responsible party" = founder with "Foreign" in the SSN field. Fax to the IRS international EIN unit or call. Typically **1–6 weeks**. Stripe Atlas / Clerky / Firstbase handle this.
- Keep the **CP 575** letter (banks require it). If it is lost, request a **147C** letter.

---

## 8. Banking and money movement

| Option | Strengths | Watch-outs |
|---|---|---|
| **Mercury** | Fast online onboarding for non-US founders; Treasury sweep; virtual cards; free domestic wires | Restricts some high-risk countries; no cash deposits |
| **Brex** | Corporate card with high limits; expense management bundled | Business-account eligibility depends on funding |
| **SVB (First Citizens)** | Venture debt later; known to VCs | Slower onboarding |
| **Wise Business** | Cheap multi-currency (EUR/INR/GBP) payouts to contractors/suppliers | Not a primary treasury bank |

**Setup:** primary operating account at Mercury (or SVB) plus a treasury/T-bill sweep for SAFE cash above FDIC limits. Use a Wise or Airwallex multi-currency account for paying ODM deposits in USD/CNY and EU/India contractors. Ramp or Brex cards for SaaS. **Two-person approval for wires >$10k** once a second finance person joins (fraud control). See `admin-ops.md`.

---

## 9. Special issue: the founder's residency (India) and cross-border rules

> **Unverified fact:** COMPANY.md does not say where the founder lives. If Nimit Jain is a **resident of India** for FEMA/tax purposes, the points below are **material**. Engage Indian FEMA and tax counsel **before** incorporation (est. ₹50k–₹2L / $600–$2,500).

1. **Overseas Direct Investment (ODI):** an Indian resident individual acquiring founder shares in a foreign company is making an ODI under the **Foreign Exchange Management (Overseas Investment) Rules, 2022**. It goes through an Authorised Dealer bank and must fit within the Liberalised Remittance Scheme limit (USD 250k per financial year). Reporting forms are filed via the AD bank ([RBI OI Rules 2022](https://rbi.org.in/scripts/Bs_viewcontent.aspx?Id=5087)).
2. **Step-down subsidiary restriction:** under the OI Rules, a resident individual may make ODI only in an operating foreign entity that is **not** in financial services **and has no subsidiary or step-down subsidiary in which the resident individual has control**. Commentators note this limits structures where an Indian-resident founder controls a US parent that then sets up an **Indian subsidiary** ([Taxguru FAQ](https://taxguru.in/?p=881584), [SCC Online](https://scconline.com/blog/?p=293155)). **This may affect the "Indian subsidiary later" plan (§10).** Options include the founder becoming non-resident, structuring the India operation as a contractor/EOR arrangement instead of a subsidiary, or a specific legal opinion. **Do not set up an Indian subsidiary without this opinion.**
3. **Income-tax:** report foreign shareholding in **Schedule FA** of the Indian ITR. Indian tax doesn't recognise the US 83(b); the founder's Indian tax treatment depends on residency and the facts. Black Money Act penalties apply for non-disclosure.
4. **Place of Effective Management (POEM):** if the company is effectively managed from India, it can be treated as an Indian tax resident. POEM rules apply above ₹50 crore turnover, so this is not an immediate issue, but keep board meetings and key decisions documented as US/global.
5. **US Form 5472** (above) applies if the founder is foreign.
6. **Permanent establishment:** employees or contractors in India/EU doing core work can create a taxable presence there. Use EOR / contractor agreements with care; see `hr-hiring.md`.

---

## 10. Later: Indian and/or EU subsidiary

### 10.1 When it makes sense
| Trigger | Entity |
|---|---|
| >5 full-time staff in India (firmware, city-pack content, support) and EOR costs > ~$3k/mo | **Indian Pvt Ltd** (wholly owned subsidiary) |
| EU sales start (Kickstarter EU backers ship Q4 2027) and we need an EU importer of record, GPSR "responsible person", WEEE/battery producer registration, VAT OSS/IOSS | Third-party EU authorised-representative / fulfilment partner first. **EU entity** (Netherlands B.V., Irish Ltd, or Portuguese Lda; Lisbon is on our city list) when EU revenue is above ~€1–2M/yr or we hire >3 in one EU country |
| UK sales | UK Ltd only when needed. Companies House incorporation is cheap. Use a UK responsible person for product safety until then |

### 10.2 Indian subsidiary: outline (subject to §9.2)
- **Form:** private limited company, 100% FDI under the **automatic route** (consumer electronics / software is generally automatic, but confirm against the current DPIIT FDI Policy). **Press Note 3 (2020)**: investors from land-border countries (e.g., China) need government approval. Watch this if a Chinese ODM or strategic investor ever takes equity.
- **Requirements:** at least 2 directors, **at least 1 resident in India (≥182 days in the prior calendar year)**; 2 shareholders (parent + nominee); MCA SPICe+ filing; PAN/TAN/GST; FC-GPR reporting to RBI within 30 days of share issuance ([Razorpay Rize](https://razorpay.com/rize/blogs/register-subsidiary-company-india-2026), [Treelife](https://treelife.in/legal/setup-a-foreign-subsidiary-in-india/)).
- **Cost (est.):** setup ₹40k–₹1.5L ($500–$1,800) including professional fees; ongoing compliance (statutory audit, ROC, transfer-pricing study, GST) **₹3–8L/yr ($3.6k–$9.6k)**.
- **Intercompany agreements:** cost-plus R&D services agreement (typically 10–20% markup, safe-harbour rules), with IP **assigned to the US parent**. Transfer-pricing documentation is annual.

### 10.3 EU subsidiary: outline
- Netherlands B.V.: notary incorporation; €0 minimum capital; ~€1.5k–€3k setup; payroll via local provider.
- Ireland Ltd: CRO filing; needs an EEA-resident director or a bond; 12.5% trading tax.
- Portugal Lda: fast ("Empresa na Hora"); low cost; good engineering talent (Lisbon).
- **Intercompany:** a limited-risk distributor (LRD) model for sales, or a cost-plus service company for R&D/support.

---

## 11. Data-room folder structure (corporate)
```
01 Corporate/
   Certificate of Incorporation (stamped)
   Bylaws
   Action of Incorporator; Initial Board Consent
   Board & stockholder consents (chronological)
   Good-standing certificates
   Foreign qualifications
02 Equity/
   Founder RSPA(s) + 83(b) + proof of filing
   Equity Incentive Plan + 409A reports
   Option grants (board approvals, notices)
   SAFEs + side letters
   Cap table export (Carta/Pulley)
03 IP/
   Founder IP assignment; CIIAAs (all staff); contractor IP assignments
   Trademark filings; patent provisionals
   Open-source licence register
04 Commercial/ ...
05 Finance & Tax/ ...
```

---

## Sources
- Stripe Atlas pricing: https://www.rho.co/blog/stripe-atlas-review ; https://wpsimplepay.com/is-stripe-atlas-worth-the-money/
- Clerky pricing: https://startupsavant.com/service-reviews/stripe-atlas-vs-clerky ; https://www.flowjam.com/blog/clerky-review-2026-complete-guide-pricing-alternatives
- Delaware Aug 2026 fee schedule and HB 400: https://corpfiles.delaware.gov/Fee_Schedule/AugustFee2026.pdf ; https://corpfiles.delaware.gov/2026_Legislation/House_Bill_400.pdf ; https://www.incorp.com/resources/knowledge-base/delaware-business-filing-fee-increase
- Delaware franchise tax methods: https://jdsupra.com/legalnews/delaware-franchise-tax-for-startups-3219380 ; https://bench.co/blog/tax-tips/delaware-franchise-tax ; https://corp.delaware.gov/
- 83(b) online filing (Form 15620): https://www.mofo.com/resources/insights/250724-say-goodbye-to-paper-cuts-section-83-b ; https://goodwinlaw.com/en/insights/publications/2025/07/alerts-practices-erisa-online-filing-of-section-83b-elections ; https://www.alston.com/en/insights/publications/2025/08/irs-online-filing-section-83b-elections
- QSBS / OBBBA: https://www.gibsondunn.com/focus-on-qsbs-provisions-in-the-one-big-beautiful-bill-act/ ; https://perkinscoie.com/insights/update/significant-changes-one-big-beautiful-bill-act-qualified-small-business-stock
- 409A cost: https://www.vendr.com/marketplace/carta ; https://eqvista.com/?p=39499
- India OI Rules 2022: https://rbi.org.in/scripts/Bs_viewcontent.aspx?Id=5087 ; https://taxguru.in/?p=881584 ; https://scconline.com/blog/?p=293155
- India subsidiary: https://razorpay.com/rize/blogs/register-subsidiary-company-india-2026 ; https://treelife.in/legal/setup-a-foreign-subsidiary-in-india/
