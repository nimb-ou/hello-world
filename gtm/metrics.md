# Marketing KPIs & Dashboard Definitions

Owner: CMO. Review: weekly growth stand-up (Mon) + monthly board pack. Source systems: GA4 (or Plausible) on lore.travel, Klaviyo, Meta/TikTok/Google Ads, Kickstarter dashboard + referral tags, BackerKit, HubSpot, Shopify (post-launch), app analytics (PostHog), Discord.
**UTM convention:** `utm_source` = platform/partner, `utm_medium` = paid | organic | creator | email | referral | pr, `utm_campaign` = phase_pillar (e.g. `prelaunch_secrets`), `utm_content` = creative ID.

## 1. North-star metrics by phase
| Phase | North star | Target |
|---|---|---|
| P0 Waitlist (Nov 26–Jan 27) | Waitlist sign-ups (double opt-in) | 5,000 + 10k TikTok/IG followers |
| P2 Pre-launch (Mar–May 27) | Email list + VIP reservations | 20,000 / 2,000 |
| P3 Kickstarter (25 May–24 Jun 27) | $ pledged, backers, CPB | ≥$1M, ≥3,000, <$60 |
| P5 DTC (Q4 27→) | Activated customers (first walk within 14 days) | 80% of shipped units |
| Ongoing | Paid LORE Pass subscribers (after the free months) | Attach > 55%, churn < 6%/month |

## 2. KPI dictionary
| KPI | Definition (formula) | Source | Cadence | Target |
|---|---|---|---|---|
| Waitlist sign-ups | Count of confirmed double-opt-in contacts | Klaviyo | Daily | 5k (Jan 27), 20k (24 May 27) |
| LP conversion rate | Confirmed sign-ups ÷ unique LP sessions, by source | GA4 + Klaviyo | Weekly | ≥15% paid cold, ≥30% organic |
| CPL | Paid media spend ÷ paid-attributed confirmed leads | Ads + UTM | Daily | ≤ $2.75 |
| VIP rate | $1 reservations ÷ leads (cohort by week) | Stripe + Klaviyo | Weekly | ≥10% |
| Cost per VIP | Paid spend ÷ paid-attributed VIPs | Ads + Stripe | Weekly | ≤ $20 |
| KS followers | "Notify me" count on the pre-launch page | Kickstarter | Daily | ≥3,000 |
| Referral K-factor | Referred leads ÷ referring leads (period) | Viral Loops | Weekly | ≥0.25 |
| Follower growth | Net new followers per platform | Native | Weekly | +900/week TikTok+IG (Stage 0) |
| 3s view rate | 3s views ÷ impressions (video) | TikTok/Meta | Per post | ≥60% |
| Avg watch % | Avg watch time ÷ duration | Native | Per post | ≥45% |
| Share & save rate | (Shares + saves) ÷ reach | Native | Per post | ≥2% |
| Pledged ($) | Gross pledges | Kickstarter | Hourly (D1), daily | Curve in `kickstarter/campaign-plan.md` §6 |
| Backers | Unique backers | Kickstarter | Daily | ≥3,000 (base 4,600) |
| Avg pledge | Pledged ÷ backers | Kickstarter | Daily | $225 |
| CPB (cost per backer) | Total marketing spend (pre-launch + campaign, incl. creators, PR, production) ÷ backers | Finance + KS | Weekly | < $60 (base $50) |
| Campaign ROAS | KS pledges attributed to paid ads (referral tags/pixel) ÷ campaign ad spend | KS + Ads | Daily | ≥3.0 |
| List conversion | Backers matched to the email list ÷ list size | KS export + Klaviyo | End of campaign | 5–10% (base 8%) |
| Creator CPB | Creator spend ÷ creator-tag backers | KS tags | Weekly | ≤ $45 |
| PR referral pledges | Pledges from press referral tags | KS | Weekly | — |
| Email open / click | Unique opens ÷ delivered (Apple MPP-adjusted) / unique clicks ÷ delivered | Klaviyo | Per send | Flows ≥50%/6%; campaigns ≥40%/2% |
| Unsubscribe rate | Unsubs ÷ delivered | Klaviyo | Per send | <0.3% |
| DTC conversion | Orders ÷ sessions | Shopify | Daily | ≥1.6% |
| Blended CAC | Total S&M spend ÷ new customers | Finance | Monthly | ≤ $70 |
| Paid CAC by channel | Channel spend ÷ channel-attributed first orders (7-day click / 1-day view) | Ads + Shopify | Weekly | Meta $65, TikTok $55, Google $45 |
| Activation | Customers completing a ≥10-min walk within 14 days of delivery ÷ delivered | App | Weekly | ≥80% |
| Pass attach | Paying LORE Pass subscribers ÷ devices past their free period | App/billing | Monthly | >55% |
| Pass churn | Cancelled ÷ active at start of month | Billing | Monthly | <6% |
| Referral share | Orders with a referral code ÷ orders | Shopify | Monthly | 15% |
| NPS | %promoters − %detractors (in-app, 30 days post-activation) | App survey | Monthly | >50 |
| Return rate | Returns ÷ units delivered (30 days) | Shopify/3PL | Monthly | <5% (retail gate) |
| B2B pipeline | Weighted pipeline value (Σ deal value × stage probability) | HubSpot | Weekly | 3× quarterly target |

## 3. Dashboards
**D1: Pre-launch growth (daily, Mar–May 2027).** Tiles: list size vs target line, leads/day by source (stacked), CPL by channel (7-day rolling), LP conversion by source, VIPs (count, rate, cost), KS followers, top 10 creatives (CPL, CTR, thumb-stop), referral K-factor, email health (open/click/unsub).
**D2: Campaign war room (hourly on D1, then daily).** Pledged vs the target curve, backers, avg pledge, tier sell-through (remaining early birds), pledges by referral source (email, ads, creators, PR, KS organic), ROAS by ad set, CPB to date, top countries, comment SLA (% answered in <4h), stretch-goal progress.
**D3: Social & content (weekly).** Followers by platform, reach, 3s view rate, avg watch %, saves/shares, sign-ups per 1k reach by pillar, best posts, fact-check corrections count.
**D4: DTC & lifecycle (weekly, post-launch).** Sessions, CVR, AOV, CAC by channel, activation, Pass attach and churn by cohort, NPS, returns, referral share.
**D5: B2B & partnerships (weekly).** Pipeline by stage, weighted value, pilot health (utilisation, CSAT), affiliate revenue by partner.

## 4. Attribution rules
- Kickstarter: referral tags are the source of truth for pledges; Meta/TikTok pixels via Kickstarter's supported pixel integration where available.
- Pre-launch: last non-direct click (UTM) for leads; self-reported "How did you hear about us?" on the thank-you page as a cross-check.
- Creators: a code or a tag counts, and if both, the code wins.
- Everything simulated or forecast is labelled "forecast" in dashboards; actuals only from source systems.
