# LORE Kit: accessories ID specification

**Rev:** EVT-0 · 2026-10-31. Every accessory uses the **LORE Mount** (id-spec §2): a male puck Ø23.6 × 2.4 with 3 bayonet lugs, an N52 magnet catch and 2 spring pogo pins.
Prices are **targets for Finance and Research to validate**. COGS figures are design-team estimates **(E)**.
Renders are in `renders/acc-*.png`; the kit family shot is `renders/acc-family.png`. In-use shots are `renders/on-clip.png` and `renders/on-lanyard.png`.

| Accessory | Render | Key dimensions | Materials / process | Target price | COGS (E) |
|---|---|---|---|---|---|
| **LORE Clip** | acc-clip.png, on-clip.png | Puck Ø23.6 + spring tongue 16 wide × 1.0 thick × ~44 long. Opens to 6 mm webbing. 8 g | 17-7PH stainless, heat-treated CH900, bead-blast. Silicone grip pad (Shore 50A) | Included with Pebble; $19 spare | $2.10 |
| **Leather Lanyard** | acc-lanyard.png, on-lanyard.png | 10 mm strap, 2.2 thick, 900 mm loop (adjustable 600–900). Brass slider 12 × 8. Mount yoke 10 × 18 | Vegetable-tanned leather (Tuscan tannery, LWG-certified supplier), edges hand-burnished and waxed. Solid brass C360, lacquered. **80 N breakaway yoke** (safety) | $49 | $9.80 |
| **Wrist Strap** | acc-wrist-strap.png | 8 mm loop, 200 mm circumference. Brass keeper 13 × 7 | Same leather as the lanyard. Brass keeper | $29 | $5.40 |
| **Magnetic Dock** | acc-dock.png | 72 × 60 × 12 base plus a cradle leaning 22° from vertical. Square/Atlas shows nightstand mode. Silicone foot. 140 g so it does not tip | 6063 Al CNC, bead-blast + anodise (Ink/Sand to match). LORE Mount pad + pogo. Status LED. USB-C in (5 V/2 A) | $59 | $14.50 |
| **Rugged Case** | acc-rugged-case.png | Adds 2.0 per side and 1.4 at the back (58 × 58 × 13.4 with Square). Corners carry an extra 1.6 bumper. Raised 0.6 lip protects the glass | TPU 85A over a PC back plate. LORE Mount pass-through (Ø24 cut-out), integrated lanyard eyelet. Olive / Ink. Rated 2 m drop (MIL-STD-810H 516.8 procedure IV, as a design target) | $35 | $3.90 |
| **LORE Buds** | acc-buds.png | Ti memory-alloy band, Ø3.4 silicone over a Ø1.2 Ti wire. Transducer pods 14 × 22 × 6.5. 29 g (E) | Open-ear bone-conduction. BT 5.4 LE Audio (LC3) + A2DP. IP55. Brass-tone accent ring (ZrN). 8 h playback | $129 | $34 |
| **Power Puck** | acc-power-puck.png | 64 × 64 × 16 squircle. 5,000 mAh / 19.3 Wh (airline-OK, under 100 Wh). 4 status LEDs. 118 g (E) | 6063 Al shell + silicone top pad with a LORE Mount puck (charges any LORE at 5 W). USB-C PD 20 W in/out | $69 | $16.20 |
| **City bundles** | — | e.g. "Rome Kit" = lanyard in Terracotta leather + Trip Pass + printed map card | Packaging per brand/packaging.md | $79 | n/a |

## Design notes

- **One interface.** The Clip, Lanyard yoke, Wrist strap, Dock and Puck all carry the same male puck. Moving a device from one to another takes one twist.
- **Safety.** The lanyard yoke uses a magnet-held breakaway insert that releases at 80 N ±10 %. That protects against strangulation and bag snatches: the device drops and the strap stays. The device then sounds the "detached" earcon (ux-spec §4) and flags a possible snatch if it moves away quickly.
- **Leather.** The leather is undyed vegetable-tanned. It ages from tan to a deep caramel; we tell customers this up front as a feature (brand story).
- **Buds.** Bone conduction leaves the ear canal open, which serves the safety story ("hear the traffic and the story"). Latency target: < 120 ms over LE Audio LC3 for earcon sync.
- **Dock nightstand mode.** When docked, Square and Atlas show a clock plus tomorrow's first walk (see device screen `12-nightstand`).

## Open issues

1. The breakaway force needs a usability check with 10 users (pulls from a backpack zip, etc.).
2. Rugged case plus Dock: the 1.4 mm case back weakens the magnet catch by about 35 % (E). A case-on dock insert may be needed.
3. Puck: confirm with Hardware that pogo 5 W is adequate. Square takes about 1 h 15 min to reach 80 % (E).
