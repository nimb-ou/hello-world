# Pricing & margin sensitivity

*There are two layers.*
- *The **live grid** in `LORE_Financial_Model.xlsx` → `Unit Economics` (below the SKU table) shows DTC hardware GM by price × change in landed cost for each SKU. Grid costs use the **launch** quote.*
- *The **whole-model reruns** come from `scripts/sensitivity.py`. It rebuilds the workbook with one input changed, recalculates it in LibreOffice and writes `sensitivity_results.json`.*

*Base case: Research prices, hardware COGS, D10-D13, and the D11 Square cost-down to $185 ex-NRE from Jul-2028. All figures are estimates. The equity-need figures below were run with the earlier $35M Series B. The Series B size affects only cash, not burn, so they still hold.*

## 1. Whole-model sensitivities

| Case | FY28 rev | FY31 rev | FY28 GM | FY31 GM | FY30 EBITDA | FY31 EBITDA | Peak cumulative burn* | First EBITDA+ FY |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **Base** | $10.1M | $111.3M | 26.8% | 41.0% | −$5.4M | **+$0.8M** | **$32.8M** | **2031** |
| Square at $329 (D11 fallback) | $10.5M | $115.2M | 29.4% | 42.9% | −$3.2M | +$4.4M | $25.8M | 2031 |
| Square hits the D11 target ($168 ex-NRE, ≤ $240 incl. NRE) | $10.1M | $111.3M | 28.5% | 43.0% | −$4.1M | +$3.0M | $27.9M | 2031 |
| **Square cost-down fails (stays at $227)** | $10.1M | $111.3M | 22.3% | 32.9% | −$10.7M | **−$8.3M** | **$51.7M** | after FY31 |
| Cost-down fails + Square at $329 | $10.5M | $115.2M | 25.0% | 35.0% | −$8.4M | −$4.7M | $44.3M | after FY31 |
| Atlas back to $549 | $9.9M | $109.0M | 25.3% | 39.8% | −$6.8M | −$1.4M | $37.4M | after FY31 |
| **China assembly, +20% of FOB tariff** | $10.1M | $111.3M | 14.9% | 31.9% | −$12.0M | **−$9.3M** | **$56.5M** | after FY31 |
| Explorer attach −25% | $10.0M | $108.8M | 26.5% | 40.2% | −$6.4M | −$1.1M | $36.2M | after FY31 |
| Churn 8%/mo (vs 6%) | $10.1M | $109.8M | 26.8% | 40.5% | −$6.0M | −$0.3M | $34.7M | after FY31 |
| Churn 4%/mo | $10.1M | $113.4M | 26.9% | 41.7% | −$4.8M | +$2.4M | $30.3M | 2031 |
| eSIM data at $3.00/GB (vs $1.60) | $10.1M | $111.3M | 26.0% | 40.0% | −$6.1M | −$0.3M | $35.2M | after FY31 |
| Retailer margin 45% (vs 38%) | $10.0M | $108.7M | 25.8% | 39.7% | −$6.9M | −$1.5M | $37.2M | after FY31 |
| DTC promotions 12% (vs 6%) | $9.6M | $107.2M | 23.5% | 39.0% | −$7.9M | −$3.1M | $41.2M | after FY31 |
| Kickstarter at half of base (2,300 backers) | $9.8M | $111.3M | 26.9% | 41.0% | −$5.5M | +$0.8M | $33.0M | 2031 |

*Peak cumulative operating + investing cash outflow is the minimum equity needed before any cash buffer.

**Scenario toggles** (sheet `Scenarios`; multipliers on volume, price, attach, churn, COGS and CAC):

| | FY28 rev | FY31 rev | FY31 EBITDA | FY31 cash (with planned $55.5M of rounds) |
|---|---:|---:|---:|---:|
| Bear: 0.55× volume, −7% price, 0.7× attach, 1.3× churn, +10% COGS, 1.35× CAC | $5.1M | $56.2M | −$22.3M | **−$16.6M → needs ≈ $72M of equity** |
| **Base** | $10.1M | $111.3M | +$0.8M | $22.1M |
| Bull: 1.45× volume, 1.25× attach, 0.8× churn, −5% COGS, 0.85× CAC | $14.8M | $166.1M | +$24.4M | $56.1M (EBITDA+ from FY2030) |

![Revenue by scenario](charts/scenarios_revenue.png)

## 2. Price-point view (DTC hardware GM, launch cost vs H2-2028 cost)

| SKU | Price | Landed at launch | DTC HW GM at launch | Landed H2-28 | DTC HW GM H2-28 |
|---|---:|---:|---:|---:|---:|
| Pebble | $129 | $62.65 | 31% | $59.52 | 34% |
| Pebble | **$149** | $62.65 | 40% | $59.52 | **42%** |
| Square | **$299** | $227.16 | **7%** | $184.00 | **23%** |
| Square | $329 | $227.16 | 15% | $184.00 | 29% |
| Square | $349 | $227.16 | 19% | $184.00 | 33% |
| Atlas | $549 | $317.39 | 29% | $301.52 | 32% |
| Atlas | **$599** | $317.39 | 34% | $301.52 | **37%** |
| Atlas | $649 | $317.39 | 39% | $301.52 | 41% |

DTC HW GM = (MSRP × 0.94 × 0.96 − landed − $11 fulfilment − 2.9% − $0.30 − 2% warranty) ÷ (MSRP × 0.94 × 0.96).

## 3. CFO recommendations

1. **The D11 Square cost-down is the most valuable engineering milestone in the plan**, worth ≈$9M a year of EBITDA by FY2031. Set a hard DVT gate (Sep-2027): if the projected landed cost is above $205 ex-NRE, switch to $329 before regular DTC sales open (Kickstarter prices are already locked).
2. **Keep assembly in VN/MY (D13).** China assembly is the largest single downside (−$10M EBITDA a year).
3. **Hold Atlas at $599** and keep promotions under 8% blended. Each extra 6 points of discount costs ≈$4M of FY2031 EBITDA.
4. **Sell Square in retail only after the cost-down.** Lead retail with Pebble and Atlas.
5. **Protect churn.** Moving from 6% to 4% a month is worth +$1.6M of FY2031 EBITDA. Annual plans ($79/yr) and Trip Pass upsell are the tools.
