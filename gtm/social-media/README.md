# Social media: index
| Path | Contents |
|---|---|
| [strategy.md](strategy.md) | Pillars (Secrets of Rome / Look up / Solo safe / Build in public), per-platform strategy (TikTok, IG, YouTube, X, Reddit, LinkedIn, Pinterest), voice, production, KPIs |
| [content-calendar-90d.csv](content-calendar-90d.csv) | 374 posts, Mon 2 Nov 2026 → Sat 30 Jan 2027: date, platform, format, pillar, hook, script/caption, CTA, hashtags, fact-check flag |
| [tools/build_calendar.py](tools/build_calendar.py) | Regenerates the calendar: `python3 gtm/social-media/tools/build_calendar.py` |
| [captions.md](captions.md) | 30 ready-to-post captions |
| [video-scripts.md](video-scripts.md) | 10 short-video scripts |
| [visuals/png/](visuals/png/) | 14 rendered covers: 8 × 1080×1350 (feed), 6 × 1080×1920 (Stories/TikTok) |
| [visuals/contact-sheet.png](visuals/contact-sheet.png) | All covers on one sheet |
| [visuals/src/](visuals/src/) | `designs.mjs` (HTML/CSS designs) + `build.mjs` (Playwright renderer). Run: `(cd gtm/tools && npm install)`, then `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node gtm/social-media/visuals/src/build.mjs` |

Logos come from `brand/logo/svg` (copied to `gtm/assets/brand`); fonts are Fraunces, Inter and JetBrains Mono (OFL, via @fontsource). Every fact on a cover must pass the Rome City Pack check before posting.
