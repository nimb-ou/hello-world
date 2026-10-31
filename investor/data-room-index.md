# LORE Labs: Data Room Index

*Pre-seed, November 2026. All paths are relative to the repo root. **Status:** ✅ = exists; 🟡 = draft or template (needs counsel or real data); ❌ = not yet available (gap, with the date we expect it). Everything marked (E) or SIMULATED in the source files is an estimate or a model output, not measured data.*

## 1. Company and corporate

| Diligence item | File(s) | Status |
|---|---|---|
| Company overview / single source of truth | `COMPANY.md` | ✅ |
| Decisions log (D1–D16) | `company/decisions-log.md` | ✅ |
| 18-month operating plan and stage gates G0–G3 | `company/operating-plan.md` | ✅ |
| OKRs, operating cadence | `company/okrs.md`, `company/operating-cadence.md` | ✅ |
| Org chart (today, pre-seed, seed) | `company/org-chart.md` | ✅ |
| Incorporation plan (Delaware C-corp, 83(b), EIN, bank, QSBS, Indian-residency ODI warning) | `legal-ops/incorporation.md` | 🟡 company not yet incorporated |
| Certificate of incorporation, bylaws, board consents | — | ❌ at formation (Nov 2026) |
| Founder stock agreement + IP assignment | `legal-ops/templates/founder-agreement.md`, `legal-ops/templates/ciiaa.md` | 🟡 templates |
| Board cadence, insurance, tax calendar, risk register (top 25) | `legal-ops/admin-ops.md` | ✅ |

## 2. Financing and cap table

| Diligence item | File(s) | Status |
|---|---|---|
| Round terms: $1.75M SAFE at a $12M post-money cap (D14) | `company/decisions-log.md` D14, `legal-ops/templates/safe-summary-note.md` | 🟡 SAFE summary is a template |
| Fundraising plan, rounds through Series B, target investor types | `finance/fundraising-plan.md` | ✅ (no investor has committed) |
| Cap table (formation → Series B) | `finance/LORE_Financial_Model.xlsx` (sheet `Cap Table`), `finance/fundraising-plan.md` §5 | ✅ modelled (pre-D14 $1.5M basis) |
| Valuation rationale and comparables | `finance/valuation.md` | ✅ |
| Pitch deck, one-pager, executive summary, FAQ | `investor/LORE_Pitch_Deck.pptx`, `investor/one-pager.pdf`, `investor/executive-summary.md`, `investor/investor-faq.md` | ✅ |

## 3. Financials

| Diligence item | File(s) | Status |
|---|---|---|
| 3-statement model (live formulas, 20 sheets, 8 automated checks) | `finance/LORE_Financial_Model.xlsx`, `finance/scripts/run_all.py` | ✅ |
| CFO summary and reconciliation with other teams | `finance/README.md` | ✅ |
| Machine-readable model outputs | `finance/model_summary.json`, `finance/sensitivity_results.json` | ✅ |
| 12-month budget (Nov-26 → Oct-27) | `finance/budget-12-months.md` | ✅ (generated on the $1.5M basis; D14 adds $250k) |
| Unit economics per SKU, cloud cost stack | `finance/unit-economics.md` | ✅ |
| Pricing and margin sensitivities (14 cases) | `finance/pricing-margin-sensitivity.md` | ✅ |
| Kickstarter economics and cash timing | `finance/kickstarter-economics.md` | ✅ |
| KPI definitions and targets | `finance/kpis.md`, `gtm/metrics.md` | ✅ |
| Charts | `finance/charts/*.png` | ✅ |
| Historical financial statements / bank statements | — | ❌ pre-incorporation, no history |

## 4. Market and customers

| Diligence item | File(s) | Status |
|---|---|---|
| TAM/SAM/SOM with full math | `research/market-sizing.md`, `research/scripts/sizing_model.py` | ✅ |
| Competitive landscape (30 products) and threat ranking | `research/competitors.md`, `research/charts/positioning-map.png` | ✅ |
| Pricing research, Van Westendorp plan, regional prices | `research/pricing-research.md` | ✅ (hypotheses until the survey runs) |
| Personas and jobs to be done | `research/personas.md` | 🟡 hypotheses |
| Customer survey and interview script, go/kill thresholds | `research/customer-survey.md` | 🟡 ready to run (Nov 2026 – Jan 2027) |
| Survey results, interview notes, Sean Ellis (G0) results | — | ❌ expected Jan 2027 |
| Trends and launch-city scoring | `research/trends.md`, `research/launch-markets.md`, `research/launch-scoring.csv` | ✅ |

## 5. Product and technology

| Diligence item | File(s) | Status |
|---|---|---|
| Software overview and run instructions | `software/README.md` | ✅ |
| System architecture, model strategy, privacy, cost per user | `software/docs/architecture.md` | ✅ |
| Device software / OS plan, BLE GATT spec | `software/docs/device-software.md` | ✅ |
| Engineering roadmap and software hiring | `software/docs/roadmap.md` | ✅ |
| Core code (story engine, Map Vision geometry, heading fusion, narration guard) | `software/packages/core/src/` | ✅ |
| Rome City Pack (86 POIs, 215 sourced fact cards) | `software/city-pack/data/rome_seed.json`, `software/city-pack/output/` | 🟡 facts need an online verify pass + editorial review |
| Prototype app and screenshots | `software/apps/prototype/`, `software/apps/prototype/screenshots/` | ✅ |
| Walk simulation transcript and metrics | `software/simulations/output/rome-walk-transcript.md`, `rome-walk-metrics.json` | ✅ SIMULATED |
| Test suite (61 vitest + 16 pytest) | `software/` (`npm run test:all`) | ✅ |
| Real-world field-test data (Map Vision accuracy, battery) | — | ❌ G0 walks (Jan 2027), EVT (Q1 2027) |

## 6. Hardware and manufacturing

| Diligence item | File(s) | Status |
|---|---|---|
| Hardware overview, headline results, top risks | `hardware/README.md` | ✅ |
| System architecture, SoC trade study, ECRs | `hardware/system-architecture.md` | ✅ |
| BOMs and landed COGS roll-up (incl. Pebble Lite) | `hardware/bom/BOM.md`, `hardware/bom/bom_*.csv`, `hardware/bom/cogs_summary.csv` | ✅ (E) estimates, pre-RFQ |
| Schematics (Square reference sheets), pin map, PCB stack-up | `hardware/schematics/` | ✅ reference design |
| Block diagrams | `hardware/block-diagrams/` | ✅ |
| Power, heading-fusion, thermal, RF simulations | `hardware/simulations/results.md` (+ scripts and JSON) | ✅ SIMULATED |
| Certification plan and costs | `hardware/certification.md`, `legal-ops/compliance-matrix.md` | ✅ |
| DFM, EVT/DVT/PVT plan, yields, MOQs | `hardware/dfm-manufacturing.md` | ✅ |
| Firmware interfaces | `hardware/firmware-interfaces.md` | ✅ |
| Supply chain, ODM selection, logistics, RMA, warranty | `legal-ops/supply-chain-ops.md` | ✅ |
| ODM term sheet | `legal-ops/templates/odm-supply-agreement-term-sheet.md` | 🟡 template; ODM selection due 31 Jan 2027 |
| Supplier quotes (RFQs) | — | ❌ Q1 2027 |

## 7. Design and brand

| Diligence item | File(s) | Status |
|---|---|---|
| Industrial-design renders (lineup, heroes, exploded, colourways) | `design/industrial/renders/*.png` | ✅ concept renders |
| Design parameters and mass budget | `design/industrial/params.json`, `design/industrial/mass-budget.md` | ✅ |
| Design README, 3D models, drawings, UX screens | `design/README.md`, `design/industrial/models/`, `design/industrial/drawings/`, `design/ux/` | ❌ folders empty at time of writing |
| Brand guidelines, voice and tone, packaging | `brand/brand-guidelines.md`, `brand/voice-and-tone.md`, `brand/packaging.md` | ✅ |
| Logos, palette, fonts | `brand/logo/`, `brand/palette/`, `brand/typography/` | ✅ |

## 8. Go-to-market

| Diligence item | File(s) | Status |
|---|---|---|
| GTM strategy, channels, CAC, funnel | `gtm/README.md`, `gtm/gtm-strategy.md` | ✅ plan |
| Kickstarter plan, tiers, page copy, video script | `gtm/kickstarter/` | ✅ plan. Note: the campaign page shows Atlas at $549; it must be updated to $599 (D8) |
| Social, creator and PR plans | `gtm/social-media/`, `gtm/creator-pr/` | ✅ |
| Sales: DTC, retail, B2B, affiliate, CRM | `gtm/sales/` | ✅ (retail per D15: Pebble + Atlas first) |
| Waitlist site | `gtm/website/` | ✅ (not yet live) |
| Waitlist count, CAC actuals | — | ❌ from Nov 2026 |

## 9. Legal, IP, privacy and compliance

| Diligence item | File(s) | Status |
|---|---|---|
| Legal and ops index and master setup checklist | `legal-ops/README.md` | ✅ |
| Trademark strategy and risks (LORE vs Epic, Pixite, YLORE, the Lore podcast) | `legal-ops/ip-strategy.md`, `brand/naming-trademark.md` | 🟡 clearance search due Dec 2026 |
| Patent plan (P1 Map Vision, P2 quiet-moment) | `legal-ops/ip-strategy.md` | 🟡 provisionals due by 15 Jan 2027 |
| Open-source and data licences (OSM ODbL, Wikipedia CC BY-SA, model licences) | `legal-ops/ip-strategy.md` | ✅ analysis |
| Privacy programme, DPIA (location data), EU AI Act assessment | `legal-ops/privacy-security.md`, `legal-ops/policies/dpia-location-data.md`, `legal-ops/policies/eu-ai-act-assessment.md` | 🟡 drafts |
| Customer policies (privacy, ToS, subscription, warranty, AUP, safety disclaimers) | `legal-ops/policies/` | 🟡 drafts for counsel |
| Compliance matrix (radio, safety, batteries, EPR, duties, origin) | `legal-ops/compliance-matrix.md` | ✅ |
| Contract templates (NDA, contractor, advisor, offer, content licence, affiliate) | `legal-ops/templates/` | 🟡 templates |
| Material contracts signed | — | ❌ none yet |
| Litigation | — | none |

## 10. Team and HR

| Diligence item | File(s) | Status |
|---|---|---|
| First 12 hires, salary and equity bands, process, payroll/EOR | `legal-ops/hr-hiring.md` | ✅ plan |
| Headcount plan in the model | `finance/LORE_Financial_Model.xlsx` (`Headcount`, `Headcount Plan`) | ✅ |
| Founder background / references | — | ❌ provided on request by the founder |
| Employment agreements | — | ❌ no employees yet |

## Known gaps and inconsistencies to fix before close
1. Finance's cap table and 12-month budget are on the $1.5M basis; D14 raised the round to $1.75M (≈14.6% to SAFE holders instead of 12.5%).
2. The design folder has no README; 3D models, drawings and UX screens are not yet in the repo. The `lineup.png` render caption still shows Atlas at $549 (cropped out of the deck).
3. `company/operating-plan.md` mentions "3 Shenzhen manufacturers"; D13 moved assembly to Vietnam/Malaysia.
4. `hardware/README.md` listed the Atlas at $549 (fixed 2026-10-31) and Square on Cat-4 (EG25-G); D8 and D11 supersede both.
5. All customer evidence (survey, interviews, field tests) is still to come; see G0.
