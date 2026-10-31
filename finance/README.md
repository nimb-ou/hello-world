# finance/ (LORE Labs CFO office)

*Prepared 31 Oct 2026. All projections are **estimates** (base scenario unless stated). The model is reconciled to **Research final prices and units** (`research/`), **Hardware landed COGS and NRE** (`hardware/bom/`, `hardware/README.md`), **founder decisions D10-D13** (`company/decisions-log.md`) and the **GTM Kickstarter plan** (`gtm/kickstarter/`).*

## CFO summary

| $M (FY = calendar year) | FY2027 | FY2028 | FY2029 | FY2030 | FY2031 |
|---|---:|---:|---:|---:|---:|
| Units shipped | 3.4k | 39.9k | 120k | 250k | 400k |
| **Revenue** | **0.6** | **10.1** | **31.6** | **67.1** | **111.3** |
| of which hardware (net) | 0.5 | 9.1 | 26.9 | 54.9 | 87.9 |
| of which subscriptions (Explorer + Trip Pass) | 0.0 | 0.4 | 2.3 | 6.2 | 12.3 |
| of which accessories / affiliate / B2B fleet | 0.0 | 0.6 | 2.5 | 5.9 | 11.1 |
| **Gross margin** | 11% | 27% | 33% | 38% | **41%** |
| Hardware gross margin | 8% | 25% | 29% | 32% | 34% |
| EBITDA | −4.2 | −4.3 | −7.2 | −5.4 | **+0.8** |
| Net burn (operating + investing cash) | 4.7 | 6.9 | 7.8 | 9.8 | 3.9 |
| Ending cash | 2.6 | 23.6 | 15.8 | 26.0 | 22.1 |
| Paid subscribers (end) / ARR | – | 7.7k / $0.8M | 32k / $3.3M | 74k / $7.6M | 132k / $13.6M |
| Headcount (end) | 14 | 30 | 61 | 92 | 121 |

*FY2026 (Nov-Dec stub): −$0.2M EBITDA. 2027 units are 3.4k because the 5.3k pre-orders ship Nov-27 to Apr-28 (Atlas Founders in Apr-28), so ~1.9k fall into FY2028.*

- **Funding need:** **$55.5M** of equity in total: $1.5M pre-seed SAFE ($12M post cap), **$6M Seed** (Aug-27, $22M pre), **$3M Seed-2 extension** (Mar-28; CFO addition, could be inventory finance instead), **$25M Series A** (Sep-28, $80M pre / $105M post) and **$20M Series B** (2030). The peak cumulative operating + investing outflow is **$33.4M**. The rest is a buffer that leaves ≥ $15M of cash at each year-end after the Seed.
- **Peak burn:** **$1.1M in a single month (Oct-27)**: certification for three SKUs, tooling and the first ODM deposits. The steady-state peak is FY2030 at ≈ $0.8M/month.
- **Runway risk:** the pre-seed bottoms at **≈ $278k in Jun-27**, before the Kickstarter payout in Jul-27. Recommendation: a $250k SAFE top-up or a gate on Atlas/ID spend.
- **Break-even:** **EBITDA turns positive in FY2031** (+$0.8M; ≈ Q4-2031 run-rate). Operating + investing cash flow is still −$3.9M in FY2031 because of inventory growth, and turns positive in FY2032 on trend. **Bull case: EBITDA-positive in FY2030. Bear case: not before FY2032, with ≈ $72M of equity needed.**
- **Biggest swing factors** (FY2031 EBITDA): the Square D11 cost-down failing (−$9.1M), China assembly tariff (−$10.1M), Square at $329 (+$3.6M), D11 target fully met (+$2.2M). See `pricing-margin-sensitivity.md`.
- **Unit economics (DTC, H2-2028 cost):** Pebble 42% hardware GM / $42 lifetime contribution per device; Square 23% / $57; Atlas 37% / $211. Square sold through retail is margin-negative until the cost-down.

## Reconciliation with other teams (differences documented)

| Topic | Other team | Finance model | Note |
|---|---|---|---|
| Prices | Research: $149 / $299 / $599; Explorer $9.99 or $79/yr; Trip Pass $29 / $49 | Same. Realised ARPU 86% of list; Trip Pass blended $32 | GTM's campaign page still shows Atlas at $549 retail. **GTM should update it to $599** |
| Net device price | Research: ≈ 80-85% of list | DTC 90% (6% promo + 4% returns), retail 60%; blended 83% (FY28) → 80% (FY31) | Within range |
| Units | Research: 5k / 40k / 120k / 250k (2027-30), 400k 2031 | Same totals (5.3k pre-orders; 2027 shipments 3.4k due to timing) | Our bear case = 0.55x, bull = 1.45x (≈ Research bull 1.6x) |
| Mix | 45 / 40 / 15 | Same; Atlas regular sales from Apr-28 | |
| Revenue | Research SOM 2030 ≈ $93M at list price | **$67M** | Research is at list price and uses 35% attach × $90/yr. We net retail margin, discounts and returns, and use 6%/mo churn |
| Landed COGS | Hardware incl. NRE @10k: Pebble ≈ $90, Square ≈ $299 (target ≤ $240), Atlas ≈ $413 | Ex-NRE unit COGS $63 / $227 → **$184 (Jul-28)** / $317; NRE booked separately (cert $1.29M opex, tooling $0.7M capex) | Square base assumes the D11 target is **missed by ~10%** ($185 vs $168 ex-NRE). Conservative |
| Duties | D13: VN/MY assembly, 0% | 1% freight, 0% duty; China +20% as a scenario | |
| Kickstarter | GTM: $250k goal, $1.04M base, 4,600 backers, $230k marketing, campaign May 25-Jun 24 2027 | 4,600 KS devices + 700 late pledges; payout Jul-27; $230k marketing | Backers get 6 months of Explorer (GTM) ≈ +$28k cloud cost, not in the model's trial row |
| Salaries | Legal-ops: offer-letter template only | CFO salary estimates + 25% burden (`Headcount` sheet) | Replace when legal-ops publishes bands |

## Index

| File | What it is |
|---|---|
| [LORE_Financial_Model.xlsx](LORE_Financial_Model.xlsx) | 20-sheet model with **live formulas** and cached values (recalculated in LibreOffice). Sheets: Dashboard, Assumptions (blue inputs), Scenarios (bear/base/bull toggle + snapshot), Pricing & Mix, Unit Economics (+ price × COGS grid), Subscription Cohorts, Revenue Build (monthly 2027-28, annual 2029-31), Hardware COGS, Cloud & AI COGS, Headcount (roles), Headcount Plan, OpEx (R&D incl. NRE/cert, S&M, Ops, G&A), Working Capital (ODM 30/70 deposits, inventory, retail AR, Kickstarter deferred revenue, capex), P&L, Cash Flow, Balance Sheet, Funding & Runway, Runway, Cap Table, Timeline |
| [unit-economics.md](unit-economics.md) | Per-SKU price → COGS → GM → CAC → subscription LTV → lifetime contribution, payback; cloud cost stack |
| [pricing-margin-sensitivity.md](pricing-margin-sensitivity.md) | 14 whole-model sensitivities, scenario table, price-point margin table, recommendations |
| [kickstarter-economics.md](kickstarter-economics.md) | Goal, tiers, fees, per-device fulfilment margin, cash timing |
| [budget-12-months.md](budget-12-months.md) | Month-by-month pre-seed/Seed budget Nov-26 → Oct-27 (generated) |
| [fundraising-plan.md](fundraising-plan.md) | Rounds, use of funds, milestones, investor target list by type, cap table |
| [valuation.md](valuation.md) | Path to a $100M valuation; comparables (GoPro, Oura, Whoop, Garmin, Nothing, Teenage Engineering, Rabbit, Humane) with sources |
| [kpis.md](kpis.md) | KPI definitions, owners, targets |
| [charts/](charts/) | `revenue_by_stream.png`, `gross_margin.png`, `cash_runway.png`, `headcount.png`, `unit_economics_waterfall.png`, `scenarios_revenue.png` |
| `model_summary.json`, `sensitivity_results.json` | Machine-readable outputs for investor/ and company/ |
| [scripts/](scripts/) | `build_model.py` (writes the workbook with formulas), `lo_recalc.py` (LibreOffice UNO recalculation), `run_all.py` (build → scenario recalcs → verification → summary → charts), `make_charts.py`, `make_budget_md.py`, `sensitivity.py` |

## Rebuild & verification

```bash
sudo apt-get install -y libreoffice-calc     # once; headless recalculation engine
python3 finance/scripts/run_all.py           # rebuild + recalc + 8 checks + charts
python3 finance/scripts/make_budget_md.py    # regenerate the 12-month budget
python3 finance/scripts/sensitivity.py       # optional, ~5 min
```

`run_all.py` checks (all **PASS** on 31 Oct 2026): the balance sheet balances in every period; cash-flow ending cash equals balance-sheet cash; no formula errors; **independent Python recomputation** of net hardware revenue (all periods) and the monthly paid-subscriber roll-forward matches the Excel formulas; revenue streams sum to total; the cap table sums to 100% at every stage; annual summaries equal the sum of periods.

## Key benchmark sources (details in each doc)

GoPro GM ≈ 34-36% (https://www.alphaquery.com/stock/GPRO/fundamentals/annual/gross-margin) · Kickstarter fees (https://www.launchboom.com/crowdfunding-tips/how-much-does-kickstarter-charge/) · subscription churn patterns (https://www.revenuecat.com/state-of-subscription-apps-2025) · Gemini Flash pricing (https://www.morphllm.com/gemini-api-pricing) · TTS pricing (https://developer.puter.com/tutorials/elevenlabs-api-pricing/) · eSIM wholesale (https://simology.io/blog/wholesale-pricing-forecasting-volume-tiers-commitments-and-margins) · consumer-electronics CAC (https://tenten.co/shopify/d2c-cac-benchmarks-2026/) · ODM 30/70 terms (https://harris-sliwoski.com/chinalawblog/china-manufacturing-payment-terms/) · Carta seed medians (https://carta.com/data/linkedin-hottest-startup-sectors-seed-2025/). Some benchmark sources are secondary aggregators, so treat them as indicative.
