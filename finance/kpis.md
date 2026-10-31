# KPI dashboard: definitions and targets

*Each KPI has an owner and a definition fixed by Finance so that board decks, the data room and the investor deck agree. Targets are the **base-case model values** (`LORE_Financial_Model.xlsx`) and are estimates. The live versions sit on the `Dashboard` sheet.*

## 1. North-star and growth

| KPI | Definition | Cadence | Owner | FY2028 target | FY2029 | FY2031 |
|---|---|---|---|---:|---:|---:|
| **Weekly Active Walkers (north star)** | Devices with ≥1 story or live answer in a 7-day window | weekly | Product | n/a (instrument at launch) | | |
| Units shipped | Devices shipped to customers or retailers (sell-in), net of none | monthly | Ops | 39.9k | 120k | 400k |
| Active devices | Shipped devices with ≥1 session in the trailing 30 days (model: 2%/mo dormancy) | monthly | Product | 39k | 139k | 620k |
| Revenue | GAAP-style: hardware recognised on shipment (pre-orders deferred), subscriptions ratably | monthly | CFO | $10.1M | $31.6M | $111.3M |
| Revenue growth YoY | | annual | CFO | n/m | 213% | 66% |

## 2. Subscription (LORE Pass)

| KPI | Definition | FY2028 | FY2029 | FY2031 |
|---|---|---:|---:|---:|
| Trial-to-paid attach | Paid Explorer subs starting within 30 days of the trial end ÷ devices whose trial ended. Model: Pebble 28%, Square 40%, Atlas 55% | 35% blended | | |
| Paid subscribers (end) | Active paid Explorer subs (monthly + annual) | 7.7k | 32.2k | 132k |
| Subscription ARR | Ending paid subs × realised ARPU × 12 (Trip Pass excluded) | $0.80M | $3.3M | $13.6M |
| Realised ARPU | Explorer revenue ÷ paid sub-months (list $9.99; $79/yr annual) | $8.59 | | |
| Monthly logo churn | Subs cancelled in month ÷ subs at start of month (model 6.0%) | ≤ 6% | ≤ 5.5% | ≤ 5% |
| Paid penetration | Paid subs ÷ active devices | 20% | 23% | 21% |
| Trip Pass attach | Trip Passes sold ÷ non-paying active eSIM device-months (model 3%) | 3% | | |
| Recurring revenue share | (Explorer + Trip Pass + B2B fleet) ÷ revenue | 4% | 9% | 13% |

## 3. Unit economics

| KPI | Definition | Target |
|---|---|---|
| Hardware gross margin | (Net HW revenue − landed COGS − fulfilment − payments − warranty) ÷ net HW revenue | FY28 25% → FY31 34% |
| Blended gross margin | Gross profit ÷ revenue (incl. cloud/AI/data COGS) | FY28 27% → FY31 41% |
| Landed COGS per SKU vs plan | Actual ODM invoice + freight + royalties ÷ units, compared with `Hardware COGS` sheet | Square ≤ $185 ex-NRE by Jul-28 (D11 target $168) |
| Cloud COGS per paid user-month | (LLM + STT + TTS + infra + eSIM data) ÷ paid user-months | ≤ $2.02 in 2028; −15-20%/yr |
| eSIM GB per paid user | Data used ÷ paid eSIM users | ≤ 0.7 GB/mo |
| Paid CAC (DTC) | Paid media + affiliate/referral payouts ÷ new DTC customers | ≤ $60 (2028), ≤ $65 (2029) |
| Blended CAC | All S&M ex-brand ÷ all new customers | track |
| Lifetime contribution / CAC | See `unit-economics.md` | ≥ 1.7x Pebble, ≥ 2x Square, ≥ 4x Atlas |
| CAC payback | Months until HW + accessory GP + subscription GP cover CAC | ≤ 0 months (paid at sale) DTC |
| Return rate | Units returned within 30 days ÷ units shipped | ≤ 4% |
| Warranty claims | RMAs ÷ installed base, monthly | ≤ 0.15%/mo |

## 4. Cash & efficiency

| KPI | Definition | Plan |
|---|---|---|
| Net burn | −(operating + investing cash flow) per month | peak $1.1M (Oct-27, tooling + cert + ODM deposits) |
| Runway | Cash ÷ trailing 3-month average net burn | never < 6 months after the Seed (Jun-27 low ≈ 2 months is the known pre-payout risk) |
| Burn multiple | Net burn ÷ net new revenue (annualised run-rate) | < 2.0x from FY2029 |
| Cash conversion cycle | Inventory days + AR days − AP days (ODM prepaid, so AP = 0) | ≈ 60 + 45 days at scale; negotiate net-30 ODM by 2029 |
| Inventory & ODM prepayments | Balance sheet | ≤ 75 days of COGS |
| Deferred revenue (pre-orders) | Pledges collected and not shipped | peaks ≈ $1.0M Oct-27; must reach 0 by Apr-28 |
| Revenue per employee | Revenue ÷ average headcount | $0.5M (FY29) → $0.9M (FY31) |

## 5. Operating KPIs to instrument at launch

- **Story accuracy**: share of stories with ≥2 sources; corrections per 1,000 stories (target < 1).
- **Map Vision hit rate**: % of "left/right/look up" cues confirmed correct in beta (target ≥ 90%).
- **Battery days delivered** vs claim (Atlas "2+ days", D12).
- **Safety**: SOS false-positive rate; "walk me home" completion.
- **City Pack coverage**: cities live (2028: 20) and POIs per pack.
- **NPS / review score** (Kickstarter and Amazon) ≥ 4.3★.

## 6. Reporting rhythm

Weekly flash (units, cash, burn, KS or pre-order pipeline) → monthly board pack (P&L vs plan, KPI table above, runway) → quarterly re-forecast in the model (`python3 finance/scripts/run_all.py`).
