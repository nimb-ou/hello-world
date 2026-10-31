# LORE Kit: accessories ID specification

**Rev:** EVT-0 / ID-A3 · 2026-10-31.

**Interface.** Every accessory uses the **LORE Mount** (id-spec §2): a male puck Ø23.6 × 2.4 with 3 bayonet lugs, an N52 magnet catch and **4 spring pogo pins** (V+ · D · ID · GND). Each accessory identifies itself by a resistor on the ID pin.

**Prices and costs.**
- Prices are **targets for Finance and Research to validate**.
- COGS figures are design-team estimates **(E)** at 10k units, ex-works Vietnam/Malaysia (D13), excluding packaging and freight.
- Gross margin (GM) is shown before channel and payment fees.

**Renders.**
- One per accessory: `renders/acc-*.png`.
- Kit family flat-lay: `renders/acc-kit-family.png`.
- In use: `renders/on-clip.png`, `renders/on-lanyard.png`.

| Accessory | Render | Key dimensions and spec | Materials / process | Target price | COGS (E) | GM |
|---|---|---|---|---|---|---|
| **LORE Clip** | acc-clip.png, on-clip.png | Puck Ø23.6, plus a spring tongue 16 wide × 1.0 thick × ~44 long. Opens to 6 mm webbing; holds on straps up to 38 mm wide. 8 g | 17-7PH stainless, heat-treated to CH900, bead-blast. Silicone grip pad (Shore 50A) | In the box with Pebble; $19 spare | $2.10 | 89 % |
| **Leather Lanyard** | acc-lanyard.png, on-lanyard.png | 10 mm strap, 2.2 thick, 900 mm loop (adjustable 600–900). Brass slider 12 × 8. Mount yoke 10 × 18. 24 g | Vegetable-tanned leather from a Tuscan tannery (LWG-certified supplier); edges hand-burnished and waxed. Solid brass C360, lacquered. **80 N breakaway yoke** (safety) | $49 | $9.80 | 80 % |
| **Wrist Strap** | acc-wrist-strap.png | 8 mm loop, 200 mm circumference. Brass keeper 13 × 7. 9 g | Same leather as the lanyard. Brass keeper | $29 | $5.40 | 81 % |
| **Magnetic Dock** | acc-dock.png | Base 72 × 60 × 12. The cradle leans 22° from vertical (68° from the desk). 140 g, so it does not tip. In nightstand mode Square and Atlas show a clock | 6063 Al CNC, bead-blast + anodise (Ink / Sand to match). LORE Mount pad + 4-pin pogo. Status LED. USB-C in (5 V / 2 A). Silicone foot | $59 | $14.50 | 75 % |
| **Rugged Case** (Square) | acc-rugged-case.png | Adds 2.0 per side and 1.4 at the back. A 0.6 lip stands above the glass. 58 × 58 × 14.0 with Square fitted. Corners carry an extra 1.6 bumper. 11 g | TPU 85A over a PC back plate. Ø24 LORE Mount pass-through, integrated lanyard eyelet. Olive / Ink. Design target: 2 m drop (MIL-STD-810H Method 516.8, Procedure IV) | $35 | $3.90 | 89 % |
| **Rugged Case** (Atlas) | as above | Same, but 1.5 deeper for the 13.5 mm body (D12): 58 × 58 × 15.5 fitted. A separate SKU, because a Square case will not close on Atlas | as above. Ink / Olive | $39 | $4.00 | 90 % |
| **LORE Buds** | acc-buds.png | Ti memory-alloy neckband: Ø3.4 silicone over a Ø1.2 Ti wire. Transducer pods 14 × 22 × 6.5. 29 g (E) | Open-ear bone conduction. BT 5.4 LE Audio (LC3) + A2DP. IP55. Brass-tone ZrN accent ring. 8 h playback (E). Magnetic 2-pin charge port on the right battery pod; cable included | $129 | $34.00 | 74 % |
| **Power Puck** | acc-power-puck.png | 64 × 64 × 16 squircle. 5,000 mAh / 19.3 Wh, well under the 100 Wh airline cabin limit. 4 status LEDs. 118 g (E) | 6063 Al shell, plus a silicone top pad with a LORE Mount puck that charges any LORE at 5 W. USB-C PD 20 W in/out | $69 | $16.20 | 77 % |
| **Mount Charging Cable** | — | 1.0 m USB-C to a Ø23.6 magnetic LORE Mount puck. Twist-free: the magnet alone holds it for charging | TPE jacket, 316L puck, 4 pogo pins. Proposed as the **Pebble in-box charger** (id-spec §12 H3) | In the box (Pebble); $15 spare | $1.60 | 89 % |
| **City bundles** | — | e.g. "Rome Kit": Terracotta leather lanyard + Trip Pass + printed map card | Packaging per brand/packaging.md | $79 | n/a | — |

## In the box (aligned with the hardware BOMs)

| SKU | In the box | Source |
|---|---|---|
| Pebble | LORE Clip (MEC7) · silicone lanyard loop (ACC2) · charging: **ID proposes the Mount Charging Cable in place of ACC1's C-to-C cable** (Pebble has no USB-C port; see id-spec §12 H3) | bom_pebble_lite.csv |
| Square | Leather-look lanyard + quick-release clip (ACC2) · USB-C to C cable (ACC1) | bom_square.csv |
| Atlas | Full-grain leather lanyard + Ti quick-release + polishing cloth (ACC2) · USB-C to C cable (ACC1) | bom_atlas.csv |

## Design notes

- **One interface.** The Clip, Lanyard yoke, Wrist strap, Dock, Puck and Charging Cable all carry the same male puck. Moving a device from one to another takes one twist.
- **Safety.** The lanyard yoke uses a magnet-held breakaway insert that releases at 80 N ±10 %. That protects against strangulation and bag snatches: the device drops and the strap stays. The device then sounds the "detached" earcon (ux-spec §4), and if it moves away quickly it flags a possible snatch.
- **Leather.** The leather is undyed vegetable-tanned. It ages from tan to a deep caramel, and we tell customers this up front as a feature (brand story).
- **Buds.** Bone conduction leaves the ear canal open, which serves the safety story ("hear the traffic and the story"). Latency target: < 120 ms over LE Audio LC3, for earcon sync.
- **Dock nightstand mode.** Docked Square and Atlas show a clock plus tomorrow's first walk (device screen `12-nightstand`).

## Open issues

1. The 80 N breakaway force needs a usability check with 10 users, e.g. pulls from a backpack zip.
2. With the Rugged Case on, the 1.4 mm case back weakens the Dock's magnet catch by about 35 % (E). A case-on dock insert may be needed.
3. Puck: confirm with Hardware that 5 W pogo charging is adequate. Square takes about 1 h 15 min to reach 80 % (E).
4. The Atlas case is a separate SKU because of D12. Retail planning needs the extra SKU count.
5. Pebble in-box charger: the Mount Charging Cable depends on the H3 decision (delete J1 USB-C on Pebble Lite).
