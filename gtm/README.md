# LORE: Go-To-Market (gtm/)

Owner: CMO / Head of Growth & Sales · v1.0 · 31 Oct 2026. Product facts come from `/COMPANY.md`; gates come from `company/operating-plan.md`.

## GTM summary
- **Positioning:** the "AI travel companion" that tells the *true* story of every street through your own earphones. The phone stays in your pocket, there's global data and offline packs, and it has a 2–3 day battery. Messaging pillars: **Look up · True stories · Go anywhere, safely**.
- **Primary buyer:** solo travellers aged 22–45 (2+ international trips a year). Secondary: culture retirees, business travellers, students. B2B fleets later.
- **Phases:** waitlist (Nov 26–Jan 27, 5k) → beta in Rome (Feb–Apr 27) → pre-launch (20k list, 2k $1 VIPs) → **Kickstarter Tue 25 May – Thu 24 Jun 2027, $250k goal** → late pledges → DTC (Q4 27) → retail/airport (2028, after returns <5%) → B2B fleet pilots (Q4 27→).
- **Kickstarter base case:** 4,600 backers × $225 average pledge ≈ **$1.04M**, on **$230k** of marketing → **CPB ≈ $50**. This meets Gate G2 (≥$1M, ≥3,000 backers, CPB <$60). Conservative case: $554k (misses $1M), with an escalation playbook ready.
- **Channels:** TikTok/IG organic ("Secrets of Rome") → paid lead gen ($2.75 CPL target) → creators (≤$45 CPB) → PR (15+ tier-1/2 articles) → email (8% list conversion). DTC blended CAC ceiling: $70.
- **Trust is the moat:** every story is sourced, and we make no safety guarantees. No partners or customers are claimed; all named companies are targets.

## Index
| Path | What |
|---|---|
| [gtm-strategy.md](gtm-strategy.md) | Positioning, messaging house, persona value props, launch phases, channel budget & CAC, funnel model, benchmarks (cited) |
| [kickstarter/](kickstarter/README.md) | Campaign plan, reward tiers (+CSV), stretch goals, 30-day timeline, pre-launch plan, full page copy, 2:30 video script + shot list, updates & community |
| [social-media/](social-media/README.md) | Platform strategy, pillars, 90-day calendar CSV (374 posts), 30 captions, 10 video scripts, **14 rendered covers + contact sheet** |
| [creator-pr/](creator-pr/README.md) | Creator programme, PR plan, press release, press kit outline, Rome launch event |
| [sales/](sales/README.md) | DTC sitemap + home/product copy, retail strategy, B2B playbook, affiliate/partnerships, CRM pipeline |
| [website/](website/) | `index.html`: responsive landing page with a client-side-validated waitlist form; `screenshots/` (desktop, mobile, form states); `screenshot.mjs` re-renders them |
| [email/](email/) | Waitlist welcome sequence (6 emails) + Kickstarter launch sequence (16 sends) |
| [community.md](community.md) | LORE Locals ambassadors, referral scheme, storyteller marketplace |
| [metrics.md](metrics.md) | KPI dictionary, targets, 5 dashboard definitions, attribution rules |
| `assets/` | Brand logos (copied from `brand/logo/svg`) and OFL fonts used by the renders |
| `tools/` | npm package for Playwright + fonts (`npm install` here before rendering) |

## Re-render
```bash
cd gtm/tools && npm install && cd ../..
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node gtm/social-media/visuals/src/build.mjs
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node gtm/website/screenshot.mjs
python3 gtm/social-media/tools/build_calendar.py
```

## Open dependencies on other teams
Finance: sign off prices, tiers and the $230k budget · Hardware: battery, accuracy and delivery dates for page copy · Story team: verify every Rome fact in content · Legal: safety, privacy and influencer-disclosure copy, and handle availability · Research: validate the personas and price sensitivity (survey linked from welcome email E3).
