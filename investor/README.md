# investor/: LORE Labs Investor Relations

Owner: Head of Investor Relations · v1.0 · 31 Oct 2026. **COMPANY.md wins on any conflict.**

**Round:** $1.75M pre-seed SAFE at a $12M post-money cap (D14: the original $1.5M plus a $250k top-up). The $6M seed follows Kickstarter (Aug 2027). The total plan to break-even is $55.5M of equity (D16).

## Deliverables

| File | What it is |
|---|---|
| [LORE_Pitch_Deck.pptx](LORE_Pitch_Deck.pptx) | 16-slide 16:9 deck in brand fonts and palette. Slides: title, problem, solution, why a device, product family, Map Vision, demo, market, competition, business model, unit economics, GTM/Kickstarter, roadmap and gates, team, financials, ask + use of funds + contact |
| [render/](render/) | `slide-01.png` … `slide-16.png` (LibreOffice render used for the visual check), `LORE_Pitch_Deck.pdf`, `one-pager.png` |
| [one-pager.md](one-pager.md) → [one-pager.pdf](one-pager.pdf) | One-page teaser (Letter). [one-pager.html](one-pager.html) is the intermediate page |
| [executive-summary.md](executive-summary.md) | Two-page executive summary |
| [investor-faq.md](investor-faq.md) | The 25 hardest investor questions with honest answers, covering hardware margins and D10–D13, Big Tech, Humane/Rabbit, idle-device risk, dilution and the solo-founder risk |
| [data-room-index.md](data-room-index.md) | Every diligence item mapped to repo files, with a status for each and a list of known gaps |
| `assets/` | Cropped renders and screenshots used by the deck (generated) |

## Rebuild

```bash
pip install python-pptx pillow markdown playwright
python3 investor/scripts/build_deck.py        # deck; reads finance/model_summary.json live
investor/scripts/render_deck.sh               # needs LibreOffice Impress (apt-get install libreoffice-impress)
python3 investor/scripts/build_onepager.py    # one-pager HTML + PDF via Playwright (Chromium from /opt/pw-browsers)
```

| Script | Purpose |
|---|---|
| `scripts/build_deck.py` | Builds the deck with python-pptx. It crops the design renders and prototype screenshots into `assets/` and embeds the brand logos, research charts and finance charts. Financial-slide numbers come from `finance/model_summary.json`; if that file is missing, the slide shows marked placeholders built on the Research SOM |
| `scripts/fin_inputs.py` | Finance-derived inputs not in the JSON: use of funds (grouped from `finance/budget-12-months.md` Nov-26 to Jun-27, plus the D14 buffer) and the unit-economics text |
| `scripts/render_deck.sh` | PPTX → PDF → PNG per slide |
| `scripts/build_onepager.py` | Markdown → branded HTML → PDF, with fonts embedded from `brand/typography/fonts` |

**Fonts:** the deck specifies Fraunces (display) and Inter (body). On machines without them, PowerPoint substitutes a default serif or sans font. For the render check, static TTF instances were generated from the brand WOFF2 files into `~/.fonts`.

## Sources and honesty rules
- Every number comes from a team folder: `research/`, `hardware/`, `software/`, `gtm/`, `finance/`, `legal-ops/`, `company/`. Each slide's footer names its source files.
- **No traction, quotes, customers, partners or investors are claimed.** The Pantheon quote on slide 3 is real output from the prototype's simulated walk. Simulated metrics are labelled SIMULATED.
- Finance was final at build time (`finance/README.md`, 31 Oct 2026).

## Open items / inconsistencies flagged to other teams
1. **Finance:** the cap table and 12-month budget are still on the $1.5M basis. Update them for D14 ($1.75M; ≈14.6% to SAFE holders).
2. **Design:** there is no `design/README.md`, and the models, drawings and UX folders are empty. The caption on `lineup.png` previously said Atlas $549 (the deck crops it out).
3. **Hardware:** `hardware/README.md` showed Atlas $549 (fixed 2026-10-31: now $599, with a D8–D13 banner) and the Cat-4 EG25-G modem for Square (superseded by D8 and D11).
4. **GTM:** the Kickstarter page copy showed Atlas at $549 (fixed 2026-10-31: $599 everywhere in gtm/).
5. **Company:** `operating-plan.md` says "3 Shenzhen manufacturers", but D13 moved assembly to Vietnam/Malaysia.
6. **Contact:** the founder's email and the domain (`lore.travel`, unverified) are placeholders on the last slide and must be filled in before sending.
