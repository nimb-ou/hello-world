# legal-ops/: Legal, Admin, IP, Privacy, Compliance, Supply Chain, Support and HR

> **IMPORTANT: everything in this folder is a DRAFT or TEMPLATE, NOT LEGAL, TAX OR REGULATORY ADVICE.** A **qualified lawyer** (and, where relevant, a tax adviser, patent/trademark attorney, or accredited test lab) in the relevant jurisdiction must review each document before it is signed, filed, published or relied on. Facts marked **[S]** were checked by web search on 30 Oct 2026 (sources listed in each file). Items marked **[V]/[verify]/(e)** come from working knowledge or estimates, because the session's search budget ran out, and **must be verified**. Founder decisions **D10–D13** (`company/decisions-log.md`, 31 Oct 2026) are reflected.

Owner: COO / Head of Legal, Admin & Operations.

## Index
| File | What it covers |
|---|---|
| [incorporation.md](incorporation.md) | Delaware C-corp via Stripe Atlas / Clerky / law firm; cap table; founder stock, vesting, **83(b) (Form 15620 online)**; EIN; bank; registered agent; franchise tax; QSBS (OBBBA); **Indian-residency ODI warning**; later India/EU subsidiaries |
| [ip-strategy.md](ip-strategy.md) | "LORE" trademark plan (classes 9/38/39/42; **no class 41**: the Lore podcast conflict; Epic Games/Pixite/YLORE filings), USPTO/EUIPO/Madrid/CN; patents (Map Vision, quiet-moment, fact-grounding) + provisional plan; trade secrets; OSM ODbL, Wikipedia CC BY-SA, Llama/Gemma/Qwen licences |
| [privacy-security.md](privacy-security.md) | Data inventory, GDPR/UK GDPR/DUAA/CCPA/DPDP/APPI map, DPO and representatives, transfers, security programme, breach timelines (incl. CRA), budget |
| [compliance-matrix.md](compliance-matrix.md) | US/EU/UK/IN/JP: radio, safety, batteries (EU removability Feb 2027), e-waste/EPR, HS codes and duties, de minimis, **VN/MY origin (D13)**, eSIM/telecom, consumer law, certification timeline |
| [supply-chain-ops.md](supply-chain-ops.md) | NPI stages, ODM selection, logistics (Flexport/ShipBob/crowdfunding 3PLs), Kickstarter fulfilment, inventory, RMA, warranty reserve, support tiers/SLAs/tools, help centre outline, **top 30 FAQs** |
| [hr-hiring.md](hr-hiring.md) | Org by stage, first 12 hires, salary benchmarks (US/EU/IN), equity bands, hiring process, values, remote policy, payroll/EOR |
| [admin-ops.md](admin-ops.md) | Tool stack and monthly SaaS budget, insurance programme, tax calendar, board cadence, **top-25 risk register** |
| **templates/** | [founder-agreement](templates/founder-agreement.md) · [ciiaa](templates/ciiaa.md) · [mutual-nda](templates/mutual-nda.md) · [contractor-agreement](templates/contractor-agreement.md) · [advisor-agreement-fast](templates/advisor-agreement-fast.md) · [safe-summary-note](templates/safe-summary-note.md) · [offer-letter](templates/offer-letter.md) · [odm-supply-agreement-term-sheet](templates/odm-supply-agreement-term-sheet.md) · [content-licensing-agreement](templates/content-licensing-agreement.md) · [affiliate-partner-agreement-outline](templates/affiliate-partner-agreement-outline.md) |
| **policies/** | [privacy-policy](policies/privacy-policy.md) · [terms-of-service](policies/terms-of-service.md) · [subscription-terms](policies/subscription-terms.md) · [warranty-returns-policy](policies/warranty-returns-policy.md) · [acceptable-use-policy](policies/acceptable-use-policy.md) · [dpa-outline](policies/dpa-outline.md) · [dpia-location-data](policies/dpia-location-data.md) · [childrens-data-stance](policies/childrens-data-stance.md) · [eu-ai-act-assessment](policies/eu-ai-act-assessment.md) · [safety-disclaimers](policies/safety-disclaimers.md) |

## Master company-setup checklist

Costs are estimates unless sourced in the linked file. Owners: **CEO** (Nimit Jain), **COO**, **FIN**, **HW**, **SW**, **GTM**, **Counsel** (external).

### Phase 0: Formation (Nov 2026)
| ✓ | Task | Owner | Timing | Cost (est.) |
|---|---|---|---|---|
| ☐ | Indian FEMA/tax opinion on founder residency (ODI; step-down subsidiary restriction) | COO + Indian counsel | **Before incorporating** | $600–$2.5k |
| ☐ | Choose Clerky ($819 lifetime) / Stripe Atlas ($500) / law firm | CEO | Week 0 | $500–$819 (+ Delaware fees, revised 1 Aug 2026) |
| ☐ | File the Certificate of Incorporation (10M shares, low par); bylaws; board consent | Counsel | Week 0 | incl. |
| ☐ | Founder RSPA (4-yr/1-yr cliff, double trigger) + IP assignment + CIIAA | CEO | Week 0–1 | incl. |
| ☐ | **83(b) within 30 days** (Form 15620 online); keep proof | CEO | **≤ day 10** | $0 |
| ☐ | EIN (SS-4 if no SSN) | COO | Week 1–6 | $0 |
| ☐ | Mercury bank + treasury; Wise/Airwallex for FX | FIN | Week 1–6 | $0 |
| ☐ | Registered agent; foreign qualification where operating | COO | Week 2 | $50–$300/yr |
| ☐ | Cap table on Carta/Pulley; equity plan adopted (12% pool) | COO | Week 2–4 | $0–$280/yr |
| ☐ | Google Workspace, Notion, Linear, Slack, GitHub, 1Password, MDM | COO | Week 1 | ~$1.6k/mo at 6 people |

### Phase 1: Raise and protect (Nov 2026–Jan 2027)
| ✓ | Task | Owner | Timing | Cost |
|---|---|---|---|---|
| ☐ | Pre-seed SAFEs (YC post-money, $12M cap); Form D ≤15 days; state notices | CEO + Counsel | Nov–Dec 2026 | $1k–$3k |
| ☐ | D&O + GL/cyber + E&O insurance | COO | At close | ~$13k–$20k/yr |
| ☐ | **Full trademark clearance** (LORE vs Epic, Pixite, YLORE, **Lore podcast**); decide on compound mark/rename | COO + TM attorney | **By Dec 2026** | $1.5k–$4k |
| ☐ | File US TM (9/38/39/42), then EUIPO + Madrid (UK/IN/JP) + China | COO | Dec 2026 → ≤6 months | ~$10k–$15k over 12 months |
| ☐ | Invention disclosures → **US provisionals P1 (Map Vision) + P2 (quiet-moment)** before any public demo | SW + patent attorney | **By 15 Jan 2027** | $8k–$20k |
| ☐ | NDAs/NNN with ODM shortlist (VN/MY per D13) | COO | Nov 2026 | $1.5k–$3k (NNN) |
| ☐ | 409A before first option grant | FIN | Dec 2026 | $1k–$3.5k |
| ☐ | First hires (firmware lead, ML engineer, mobile/backend): offers + CIIAA, Deel EOR | CEO/COO | Nov 2026–Jan 2027 | EOR ~$499–$699/employee/month |
| ☐ | Privacy policy, ToS, AUP, AI disclosure published for the app prototype | COO + privacy counsel | Dec 2026 | $8k–$20k (review) |
| ☐ | Open-source/data licence register; OSM/Wikipedia attribution in the app | SW | Dec 2026 | internal |

### Phase 2: EVT beta and Kickstarter prep (Q1–Q2 2027)
| ✓ | Task | Owner | Timing | Cost |
|---|---|---|---|---|
| ☐ | ODM selected (VN/MY assembly), term sheet → supply agreement; tooling owned by LORE | COO/HW | **31 Jan 2027** | NRE $80k–$250k; tooling $40k–$150k |
| ☐ | **Battery removability design decision (EU Feb 2027)**; EN 18031 / CRA design | HW | Dec 2026–Jan 2027 | — |
| ☐ | EU/UK Art. 27 representatives; DPIA v1 signed; DPAs with processors | COO | Before beta (Q1 2027) | €1.5k–€4k/yr |
| ☐ | Beta agreements + "not authorised / not for sale" labels | COO | Q1 2027 | — |
| ☐ | Product liability insurance in force before beta units ship | COO | Q1 2027 | ~$7k–$14k/yr |
| ☐ | Connectivity partner (SGP.32, local profiles) MSA + DPA | COO | Q1 2027 | per GB |
| ☐ | Kickstarter: claims review (FCC 2.803 disclosure, SOS disclaimers, "2+ days" Atlas battery per D12), 3PL chosen, DDP shipping pricing, refund policy | GTM/COO | Mar–Apr 2027 | fees 8–10% of funds |
| ☐ | Content licences for the Rome storytellers | Content/COO | Q1 2027 | €40–€150/story |
| ☐ | Vulnerability disclosure policy + published support period (PSTI) | SW | Q2 2027 | — |

### Phase 3: Certification and mass production (Q2–Q4 2027)
| ✓ | Task | Owner | Timing | Cost |
|---|---|---|---|---|
| ☐ | FCC, RED/CE, UKCA, SAR, IEC 62368-1, UN38.3, PTCRB + carriers, Giteki | HW | DVT–PVT (Q2–Q3 2027) | **$150k–$350k total** |
| ☐ | CBP binding origin ruling (VN/MY) + classification; EORI; EU fiscal rep; OSS/IOSS VAT | COO | Q3 2027 | $2k–$10k |
| ☐ | GPSR responsible person; WEEE/battery/packaging EPR registrations (DE, FR, IT, ES, NL…) | COO | Q3 2027 | $1k–$5k/yr per rep + fees |
| ☐ | Recall + cargo insurance; product liability limit raised | COO | Before MP | $5k–$15k/yr |
| ☐ | Warranty reserve 3.5% of hardware revenue; RMA process live | FIN/COO | MP | — |
| ☐ | Support: Intercom + Fin, help centre, BPO overflow | COO | Sep 2027 | $1k–$3k/mo |
| ☐ | **CRA readiness** (SBOM, PSIRT, reporting) for units placed on the EU market from 11 Dec 2027 | SW | By Dec 2027 | pen-tests $30k–$75k |
| ☐ | External DPO; CCPA readiness review | COO | Q2–Q4 2027 | €4k–€12k/yr |
| ☐ | PCT + US non-provisional (12 months from the first provisional) | COO | ~Jan 2028 | $15k–$30k |
| ☐ | Delaware franchise tax (1 Mar), Form 1120 + 5472 (15 Apr), 1099s (31 Jan) | FIN | Annual | ~$450–$900 + CPA $1k–$3k |

### Indicative legal/admin/compliance budget
| Year | Total (est.) |
|---|---|
| Q4 2026 (formation + IP + policies) | **$35k–$75k** |
| 2027 (certification-heavy) | **$300k–$650k** (certification $150k–$350k, insurance $30k–$55k, IP $25k–$50k, privacy/security $55k–$135k, EPR/reps $10k–$25k, legal fees) |
