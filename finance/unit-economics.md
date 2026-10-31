# Unit economics per SKU

*Source: `LORE_Financial_Model.xlsx` → sheet **Unit Economics** (live formulas), base scenario. The cost basis is H2-2028 steady state, after the D11 Square cost-down and DRAM normalisation. All figures are estimates. Landed costs are **reconciled to `hardware/bom/cogs_summary.csv` and founder decisions D10-D13**. Prices are **Research final**: Pebble $149, Square $299, Atlas $599.*

![Unit economics waterfall](charts/unit_economics_waterfall.png)

## 1. Reconciliation to Hardware

Hardware quotes landed cost **including** amortised certification and tooling. The model books certification ($165k / $485k / $640k) as R&D opex and tooling + fixtures ($140k / $235k / $330k) as capex. Unit COGS is therefore **ex-NRE**, so nothing is counted twice.

| SKU | Hardware: landed incl. NRE @10k | NRE per unit @10k | **Model unit COGS ex-NRE (launch)** | Model H2-2028 | Model FY2031 | Hardware @100k incl. NRE |
|---|---:|---:|---:|---:|---:|---:|
| Pebble (Lite design, D10) | ≈ $90 | ≈ $27-30 | $62.65 | $59.52 | $49.49 | ≈ $53 |
| Square (Cat-1bis, D11) | ≈ $299 today; target ≤ $240 | ≈ $72 | $227.16 | **$184.00** (assumes the target is missed by ~10%) | $170.37 | ≈ $190 |
| Atlas | ≈ $413 | ≈ $97 | $317.39 | $301.52 | $250.74 | ≈ $263 |

Assembly is in Vietnam/Malaysia with 0% US duty (D13). The China-assembly +20% case is in `pricing-margin-sensitivity.md`.

## 2. Per-device economics, DTC channel ($ per unit)

| Line | Pebble $149 | Square $299 | Atlas $599 |
|---|---:|---:|---:|
| DTC promo discount (6%) | −8.94 | −17.94 | −35.94 |
| Returns allowance (4%) | −5.60 | −11.24 | −22.52 |
| **Net revenue** | **134.46** | **269.82** | **540.54** |
| Landed COGS ex-NRE | −59.52 | −184.00 | −301.52 |
| Fulfilment (3PL + outbound) | −11.00 | −11.00 | −11.00 |
| Card processing (2.9% + $0.30) | −4.36 | −8.45 | −16.63 |
| Warranty reserve (2%) | −2.80 | −5.62 | −11.26 |
| **Hardware gross profit (margin)** | **56.78 (42%)** | **60.75 (23%)** | **200.12 (37%)** |
| Paid CAC (FY2028) | −60.00 | −60.00 | −60.00 |
| Hardware contribution after CAC | −3.22 | +0.75 | +140.12 |
| Accessories GP (30% attach × $45 AOV × 62%) | +8.37 | +8.37 | +8.37 |
| Free 3-month Explorer trial (cloud cost) | −6.05 | −6.05 | −6.05 |
| Paid attach after trial | 28% | 40% | 55% |
| Subscription GP per paid month ($8.59 ARPU − 8% billing − $2.02 cloud/data) | 5.89 | 5.89 | 5.89 |
| Expected paid life (1 ÷ 6% churn) | 16.7 mo | 16.7 mo | 16.7 mo |
| Subscription LTV (GP, undiscounted) | +27.48 | +39.25 | +53.97 |
| Affiliate GP over device life ($0.30/mo ÷ 2% dormancy) | +15.00 | +15.00 | +15.00 |
| **Lifetime contribution per device** | **$42** | **$57** | **$211** |
| Lifetime contribution before CAC ÷ CAC | 1.7x | 2.0x | 4.5x |
| CAC payback | at sale | at sale | at sale |

**Retail channel** (38% retailer margin): hardware GP is Pebble $23 (26%), **Square −$14 (−8%)** and Atlas $44 (12%). Lifetime contribution is $63 / $32 / $93 because co-op (6%) replaces paid CAC.

**At launch, before the cost-down** (the Kickstarter units and H1-2028), Square at $227 landed makes only $18 of hardware GP (7%) DTC and loses $57 per unit in retail. See `kickstarter-economics.md`.

## 3. Subscription & cloud COGS per paid user-month (2027-28 prices)

| Component | $/user-mo | Basis |
|---|---:|---|
| LLM inference (~150 live queries/mo: ~300k in / 45k out tokens on a Flash-class model) | 0.30 | $0.30/M in, $2.50/M out (https://www.morphllm.com/gemini-api-pricing) |
| Speech-to-text (~25 min) | 0.15 | ~$0.006/min (estimate) |
| Neural TTS for live answers (stories are pre-rendered & cached per POI) | 0.70 | ~$0.016/1k chars standard neural. Premium voices cost $0.04-0.10/1k (https://developer.puter.com/tutorials/elevenlabs-api-pricing/) |
| Infra, maps/places APIs | 0.25 | estimate |
| eSIM data (0.7 GB × $1.60/GB × 55% eSIM share) | 0.62 | wholesale ~€2.5/GB at small volume; $1.85/GB illustrative (https://simology.io/blog/wholesale-pricing-forecasting-volume-tiers-commitments-and-margins) |
| **Total** | **2.02** | plus 8% billing (web checkout + app stores) |

Explorer gross margin is ≈69% in 2028 and ≈75% by 2031 (AI deflation 20%/yr, data 8%/yr). Trip Pass ($32 blended: $29/14 days/5 GB, $49/30 days/10 GB) costs ≈$7.30 per pass, a ≈77% GM.

## 4. Takeaways

1. **Atlas carries the hardware economics**, and the $599 price is worth ≈$2.2M of FY2031 EBITDA compared with $549.
2. **Square is only viable if the D11 cost-down lands.** If it stays at $227, FY2031 EBITDA is −$8.3M and the equity need rises by ≈$19M. Moving the price to $329 recovers roughly half of that.
3. **Pebble as "Lite" (D10)** is a solid entry SKU: 42% hardware GM DTC, and the hardware margin alone pays for CAC.
4. **Retail suits Pebble and Atlas.** Square in retail destroys margin until Square is below ≈$165 landed.
5. **The subscription is the lever for lifetime value**, not the main source of gross profit. Recurring revenue reaches 13% of revenue in FY2031, so blended GM peaks around 41%, in GoPro territory (≈34-36% GAAP GM; https://www.alphaquery.com/stock/GPRO/fundamentals/annual/gross-margin) rather than Oura or Whoop.
