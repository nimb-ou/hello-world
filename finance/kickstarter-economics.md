# Kickstarter economics

*Inputs come from GTM's plan (`gtm/kickstarter/campaign-plan.md`, `reward-tiers.csv`, `prelaunch-plan.md`), with hardware landed costs (`hardware/bom/`, founder decisions D10-D13) and Research prices. Model sheets: `Assumptions` (Kickstarter block), `Pricing & Mix`, `Working Capital` (deferred revenue), `OpEx` (campaign marketing & fees). All figures are estimates.*

## 1. Campaign at a glance (GTM base case)

| Item | Value | Source |
|---|---|---|
| Dates | Tue 25 May to Thu 24 Jun 2027 (30 days) | GTM |
| Public goal | **$250,000** (enough to fund on day 1; covers Pebble tooling plus a first MOQ) | GTM |
| Internal gate G2 | ≥ $1.0M pledged, ≥ 3,000 backers, cost per backer < $60 | GTM |
| Base-case forecast | **$1.04M gross from ~4,600 backers**; average pledge ≈ $226 incl. kits/add-ons | GTM |
| Pre-launch + campaign marketing | **$230k** (12-week list build to 20k emails + 2k $1 VIP reservations; 8% list→backer) | GTM, modelled Feb-Jun 2027 |
| Cost per backer | ≈ $50 | $230k / 4,600 |
| Kickstarter payout | ≈ 14 days after close → **Jul-2027** | Kickstarter practice |
| Late pledges (BackerKit / website) | 700 devices, Aug-Oct 2027 at $129 / $259 / $499 | CFO estimate (~15% of campaign) |

## 2. Fees and net proceeds

| | $ |
|---|---:|
| Gross pledges (GTM base) | 1,040,000 |
| Kickstarter platform fee 5% | −52,000 |
| Payment processing 3% + $0.20/pledge | −32,120 |
| Failed / dropped pledges (~3%) | −31,200 |
| **Net to LORE** | **≈ 924,700** |
| Less campaign marketing | −230,000 |
| **Net cash after marketing (before fulfilment)** | **≈ 694,700** |

Fees: 5% platform + 3% + $0.20 processing (https://www.launchboom.com/crowdfunding-tips/how-much-does-kickstarter-charge/ ; https://www.pledgebox.com/post/how-much-does-kickstarter-take). The model books device pledges only (4,600 devices at blended tier prices, ≈$0.93M), and kit/add-on pledges fall into accessories, so its $1.10M of pre-order cash (KS plus late pledges) reconciles to GTM's $1.04M.

## 3. Tiers and per-device fulfilment economics (launch cost, before Square cost-down)

| SKU | KS tiers (GTM) | Blended pledge | Landed cost at launch (ex-NRE) | Fulfilment net of shipping charged | Fees 8% + warranty 2% | **Contribution / device** | Margin |
|---|---|---:|---:|---:|---:|---:|---:|
| Pebble (Lite, D10) | $99 (750) / $115 (2,000) / $125 | $113 | $62.65 | $6 | $11.30 | **+$33** | 29% |
| Square (Cat-1bis, D11) | $199 (750) / $229 (2,000) / $249 | $226 | $227.16 | $6 | $22.60 | **−$30** | −13% |
| Atlas Founders (500 numbered, Apr-2028) | $399 + later tiers | $405 | $317.39 | $6 | $40.50 | **+$41** | 10% |
| **Weighted (45/40/15 mix)** | | $202 | | | | **≈ +$9** | ≈ 4% |

**Reading:** the campaign is roughly **break-even on product and a ~$190k loss after marketing.** That is the normal price of buying 4,600 founding users, launch PR and the demand evidence the Seed needs. Square backers are fulfilled before the D11 cost-down lands, which is why every Square backer costs about $30. Two mitigations: (1) cap Square Super-Early-Bird at 750 units (GTM already does); (2) push the Square Traveller Kit ($299 with Buds, case and puck), whose accessories run at about 62% GM.

GTM gives backers **6 months of Explorer** (3 extra months). Extra cloud cost ≈ 4,600 × 3 × $2.02 ≈ **$28k**, and the first paid conversion moves 3 months later. Affordable; included in the S&M narrative, not in the model's trial row.

Shipping is charged separately via the pledge manager ($12-18 US/EU/UK, DDP for EU/UK). The model assumes a residual $6/unit subsidy (3PL, packaging, DDP leakage).

## 4. Cash timing (the reason the campaign matters to finance)

| Month | Event | Cash effect (model, base) |
|---|---|---|
| Feb-Jun 2027 | List build, video, ads | −$230k marketing |
| **Jun-2027** | Campaign live; no payout yet | **cash low point ≈ $278k** |
| **Jul-2027** | Kickstarter payout (net of fees) | ≈ +$0.86M |
| Aug-Oct 2027 | Late pledges; Seed $6M closes Aug | +$0.16M; +$6.0M |
| Aug-Oct 2027 | 30% ODM deposits (3 months before ship), tooling $705k | − |
| Oct-Dec 2027 | 70% ODM balances (1 month before ship), certification $1.29M | − |
| Nov-27 to Jan-28 | Pebble/Square ship (30% / 45% / 25%) | deferred revenue released to revenue |
| Apr-2028 | Atlas Founders ship | last deferred revenue released |

Pledges are a **liability (deferred revenue)** until devices ship. The balance sheet carries it at ~$1.0M in Oct-2027. Because the money arrives 4-9 months before shipment, it finances DVT tooling and the first ODM deposits. That is the main financial value of the campaign.

## 5. Risks & controls

- **Pre-seed cash is thin before the payout (~$278k in Jun-27).** Recommend a $250k SAFE top-up or holding $100k of ID/Atlas spend until the campaign is funded.
- **Under-performance:** at half the base (2,300 backers) the Seed still closes in our plan, but FY2028 revenue falls (see `pricing-margin-sensitivity.md`). Below 3,000 backers (Gate G2 failure), delay Atlas and DVT spend.
- **Delivery risk:** Kickstarter hardware is notorious for slips. Each month of slip keeps ~$1M as a liability and delays the first retail sell-in.
- **Refund liability:** budget 2-3% of pledges for refunds and chargebacks before shipping.
