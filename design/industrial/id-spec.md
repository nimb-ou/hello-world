# LORE industrial design specification: Pebble P1 · Square S1 · Atlas A1

**Rev:** EVT-0 / ID-A3 · 2026-10-31 · Owner: Head of Design · Status: frozen for EVT tooling quotes, open for DVT.

**Sources of truth.**
- Geometry: [`params.json`](params.json). It drives the 3D models, the renders, the drawings and the mass budget.
- Electronics: `hardware/README.md`, `hardware/schematics/pcb-stackup.md` and the BOMs in `hardware/bom/`.
- Product decisions: D10–D13 in `company/decisions-log.md`.

**Units and markings.** All dimensions are in mm. **(E)** marks an estimate that EVT measurement must confirm.

**Package.**

| Deliverable | Where |
|---|---|
| Dimensioned drawings (A3, 2:1, third-angle) | [`drawings/`](drawings/) |
| 3D models | [`models/`](models/) (GLB and STL) |
| Interactive 3D viewer | [`viewer.html`](viewer.html) |
| Renders | [`renders/`](renders/) (overview: `renders/contact-sheet.png`) |
| Accessories spec | [`accessories.md`](accessories.md) |

---

## 1. Design intent

LORE is worn, not held. The phone stays in the pocket, and LORE sits on a strap, a lanyard or a palm. Three rules drove every decision.

1. **Operable blind.** Every primary action can be found by touch alone, and each control has its own texture:
   - Pebble: a concave dish.
   - Square and Atlas: a knurled crown, a smooth pill and a ridged recess.
2. **Quiet object.**
   - There is no visible logo on the front.
   - Front-side colour is limited to one accent: the Terracotta Talk key or the brass-tone crown.
   - The LED ring is the only thing that "speaks".
3. **One interface.** Every SKU and every accessory meets at the **LORE Mount** (§2), so one clip, one dock and one lanyard serve the whole family.

**Reference set:**
- Leica Q3: tactile restraint.
- Teenage Engineering OP-1 field: honest controls.
- Nothing Ear: light as language.
- Apple Watch Ultra: crown guarding and titanium finishing.

## 2. Shared architecture: the LORE Mount

| Item | Spec |
|---|---|
| Female recess (device back) | Ø24.0 × 0.6 deep, 316L stainless insert, bead-blast Ra 0.8 |
| Lock | 3 bayonet lugs, 4.0 wide. A 30° twist locks it, with a spring detent of at least 1.5 N·cm. One lug is 0.5 wider, which keys polarity |
| Magnet | N52 sintered NdFeB ring: OD 22 / ID 14 / 1.0 thick, Ni-Cu-Ni + epoxy, axially magnetised. It self-aligns and holds 0.9 kgf on steel (E) without the twist. It replaces the 2 discrete N52 dock magnets in the hardware BOMs (MEC8) |
| Pogo | **4 pads**, Ø1.6 at 2.5 pitch in a row along device X, Au 0.76 µm over Ni, flush to −0.05. Order: **V+ · D (UART / 1-wire) · ID (accessory resistor) · GND**. This matches hardware J2 `POGO-4P` in all three BOMs. The mating parts are Mill-Max 0906-class spring pins at 1.0 N each |
| Power | 5 V / 1 A (5 W) over pogo. D carries the factory-test and recovery UART |
| Test | 10,000 twist cycles, 50 N straight pull (locked), 1,000 h salt fog on the 316L insert |

Every accessory carries the male puck: Ø23.6 × 2.4, with 3 lugs and 4 spring pins.

## 3. LORE Pebble (P1), the "Lite" tethered design (D10)

| Parameter | Value |
|---|---|
| Envelope | **42.0 × 42.0 × 13.56 max** (COMPANY.md envelope ≤ 14.0). Stack: back dome 0.45 + body 12.6 + top dome. The Talk dish sinks the centre to 13.08 (dish depth 0.45), so the highest point is the LED ring at 13.56. Plan: superellipse, n = 2.6. Drawing: [`drawings/pebble.svg`](drawings/pebble.svg) |
| Edge radii | Top fillet R5.0, bottom fillet R4.2, continuous with the domes (G1 at EVT, G2 target at DVT) |
| Wall | 1.4 nominal, PC + 10 % GF. 1.0 minimum at the speaker grille. 0.8 ribs on a 6 mm pitch |
| Talk control | The **whole top cap is the button**: a floating dish ~22.2 across flats, 0.45 concave, 0.35 travel, 2.4 N metal dome. 0.3 parting gap with a TPE wiper seal |
| LED ring | Frosted PMMA light guide following the plan outline, 22.2–24.2 across flats (~1.0 wide), proud by 0.03. **8 RGB LEDs** on a TI LP5024 (hardware BOM) |
| Volume rocker | East side, centred. 9.0 × 2.6 pill, 0.45 proud at the centre, 0.25 travel |
| Mics | 2 × Ø0.8 on the north edge, 14 apart (beamforming axis points forward when clipped), ePTFE membranes |
| Speaker | 13 × 9 driver behind 9 × Ø0.7 holes at 1.4 pitch on the south edge, with an ePTFE membrane (GORE AE-series class) |
| Charging | Pogo only, through the LORE Mount. **No USB-C**: it saves a seal path, about 3.5 mm of edge height and about $0.42 (J1 at 10k). Dock, Power Puck and the in-box Mount charging cable cover travel. See §12, item H3 |
| Attach points | LORE Mount on the back. Hidden tether tunnel: 2 × Ø2.2 at 5.0 pitch on the back at the NW corner, for a 2 mm cord |
| IP target | **IP67** (1 m, 30 min). There is no open port; the button uses a wiper seal plus an internal membrane |
| Mass | **31.9 g (E)**. See §7 |
| Battery | Hardware baseline: 650 mAh / 2.52 Wh, 35 × 32 × 5.5. **This cell does not fit the housing** (§11). The ID proposal is 30 × 27 × 5.5, ~470 mAh (E) |

**Ergonomics.**
- 42 mm sits well inside the P5 female hand breadth (about 69 mm), and the thumb pad lands naturally in the dish.
- The rocker sits under the index finger when the Pebble is pinched.
- At 13.6 mm thick it does not roll when set down, because the back dome is only 0.45.
- Clipped on a strap, the dish faces outward and up. A press from above is natural, and the ring is visible in peripheral vision.
- The PC shell stays below the IEC 62368-1 TS1 touch limit (43 °C for contact longer than 8 h) because Lite has no application processor (hardware ECR-01).

## 4. LORE Square (S1)

| Parameter | Value |
|---|---|
| Envelope | **54.0 × 54.0 × 12.0**: back bulge 0.8 + frame 11.05 + glass proud 0.15. Drawing: [`drawings/square.svg`](drawings/square.svg) |
| Plan | Rounded square with R13 corners and a superelliptic blend (n = 3.4, curvature-continuous) |
| Edge radii | Front R2.0, back R3.0. Diamond-cut chamfer 0.35 × 45° around the glass |
| Wall | 1.2 aluminium, 0.8 minimum at the antenna splits. Internal cavity 51.6 across flats. Fits the 48 × 48 R10 board and the 46 × 40 cell with ≥ 1.0 clearance (§11) |
| Cover | Corning Gorilla Glass Victus 2, 0.7 thick, 2.5D edge, **47.75 across flats**. Black ink mask, ALS window at y = +19 |
| Display | 1.6" AMOLED, 466 × 466, 28.73 square active area, R5.5 corners, ~412 ppi, on-cell touch, 1000-nit HBM. **EVT uses the standard 1.43" panel**; the ID shows the 1.6" semi-custom cut |
| Crown | Right side at y = +9: Ø6.0, 2.2 proud, 40-ridge knurl, 316L (hardware MEC3). PixArt optical rotation sensor + push; O-ring on the stem |
| Talk key | Right side at y = −8: 11.0 × 3.6 pill, 0.8 proud, Terracotta anodise, 0.3 travel, 3.0 N |
| SOS key | Left side at y = −2: 7.0 × 3.0, **recessed 0.25 in a ridged pocket** so a pocket or bag cannot press it. Requires a 2 s hold (ux-spec §6) |
| USB-C | Bottom edge, centred: 9.2 × 3.4 opening. Sealed receptacle (hardware J1: USB-C 16-pin mid-mount, IPX8-gasketed). USB 2.0 + PD sink |
| Speaker | 15 × 11 box. 5 slots, 0.8 × 3.2 at 1.7 pitch, starting 8.5 right of centre on the bottom edge. ePTFE membrane |
| Mics | 3 in total: 2 on the top edge at x = ±6 (beamforming) and 1 on the bottom edge at x = −10 (AEC reference) |
| Antennas | Frame-as-antenna with **4 nano-moulded (NMT) PBT splits**, 0.8 wide, on the top and bottom edges at x = ±12. Serves LTE Cat-1bis (D11), GNSS L1+L5 and Wi-Fi/BT |
| Back | AG-etched glass 0.7, 45.6 across flats (inset 4.2), colour-matched, with the LORE Mount insert. Laser etch: wordmark, model, regulatory text |
| Attach points | LORE Mount on the back. Ø1.8 cross-drilled tether hole in the NW corner, for a cord loop |
| Charging | LORE Mount pogo (5 W) or USB-C PD sink |
| Left-hand use | The plan is symmetric, so *Settings → Rotate 180°* puts the crown and Talk key on the left (the UI and IMU frame flip) |
| IP target | **IP67**. eSIM only, so there is no tray |
| Mass | **58.6 g (E)** |
| Battery | 1100 mAh / 4.27 Wh, 46 × 40 × 4.0 (hardware). With Cat-1bis (D11) the cell stays rectangular, so the L-shaped-cell risk in pcb-stackup §3 goes away |

**Ergonomics.**
- 54 mm is the largest square that still sits inside the P5 female palm with the thumb free to reach the crown (the in-hand render is `renders/in-hand-square.png`).
- At 12 mm it is thinner than a typical phone camera bump plus case, and it sits flat on a lanyard.
- On a lanyard the device hangs at roughly sternum height and tilts up about 15° when lifted by the thumb.
- At 412 ppi, glance text is legible at a 300–400 mm reading distance.
- The crown is the smallest control (Ø6, 2.2 proud). It is sized for a gloved thumb, and the gloved-operation test uses EN ISO 21420 dexterity-class gloves.
- Skin temperature design limit: IEC 62368-1 TS1, **43 °C for contact longer than 8 h**. Hardware's 2.2 W sustainable figure in an Al body (hardware README, Thermal) is the guard.

## 5. LORE Atlas (A1): differences from Square

| Parameter | Value |
|---|---|
| Envelope | **54.0 × 54.0 × 13.5** (D12 / ECR-02): back bulge 0.8 + frame 12.55 + glass proud 0.15. The extra 1.5 mm over Square takes the stacked board sandwich (2 × 46 × 46 boards + 1.6 mm interposer), the BG95-S5 NTN module and the camera, and lets the cell grow from 4.0 to 5.2 mm (1450 mAh / 5.63 Wh). That gives a "2+ days" claim (simulated 2.4 days with optimised firmware). Drawing: [`drawings/atlas.svg`](drawings/atlas.svg) |
| Body | Ti-6Al-4V (Grade 5), 5-axis CNC from bar. Natural bead-blast or black DLC. 1.2 wall |
| Cover | Sapphire 0.8, double-side AR (R < 1 %), oleophobic coating |
| Back | Zirconia ceramic 0.9, 45.6 across flats (RF-transparent for LTE, NTN and GNSS). Warm grey on Ti, black on DLC |
| Crown | Ti stem and cap with **ZrN PVD "brass-tone"** (L\*a\*b\* ≈ 72 / 4 / 28). Unlike real brass, it does not tarnish |
| Glance camera | Front, in the top glass band at y = +19. OV13B10 13 MP fixed-focus wide module: Ø2.6 lens under a Ø5.2 polished trim |
| Privacy LED | White, Ø0.7, 4.2 mm right of the lens (x = +4.2). **Hard-wired**: lit whenever the sensor is powered, and firmware cannot override it |
| Satellite SOS | Quectel BG95-S5 NTN (Skylo). The patch and frame antenna are tuned for sky view when the device is worn on the chest |
| Charging | Same as Square (pogo 5 W + USB-C PD) |
| IP target | **IP68** (1.5 m, 30 min) |
| Mass | **88.6 g (E)**. At 13.5 mm the Ti unibody is 18.2 g and the cell is 25.6 g; §7 has the breakdown |

**Ergonomics.**
- 88.6 g on a lanyard puts about 0.87 N on the neck, and the leather strap spreads it across a 10 mm width.
- 89 g is the comfort ceiling we set for all-day neck wear (E, to be validated in the EVT wear trial: 10 users × 3 days).
- The extra 1.5 mm reads as a heavier, more "instrument" object. The R3 back fillet hides it in profile, and the front fillets match Square, so both look the same from the front.
- Titanium conducts heat less well than aluminium (Ti-6Al-4V ~7 W/m·K vs ~150 W/m·K for 6013 Al). Atlas therefore relies on the 0.4 mm vapour chamber (hardware MEC9) to keep the skin side below 43 °C.

## 6. Control layout rationale

- **Crown above the Talk key on the same side.** The thumb sweeps vertically with no change of grip. The crown sits at the top so that, on a lanyard, the hand coming up from below meets the Talk key first; Talk is the most frequent action.
- **SOS on the opposite side, recessed.** Opposition makes squeeze-plus-hold a deliberate act. The hold is 2 s with haptic pulses (ux-spec §6). Accidental-trigger target: < 1 per 1,000 device-days in EVT pocket tests.
- **Pebble has no separate SOS key.** It uses the Talk dish held for 3 s, plus phone confirmation (ux-spec §6).
- **Tactile coding.** Every control can be told apart by touch with gloves on:
  - crown: knurled
  - Talk: smooth and convex
  - SOS: ridged and concave
  - Pebble Talk: smooth concave dish

## 7. Mass budget per part (estimate)

Generated by `scripts/mass_budget.py` from `params.json`. The script also writes `mass-budget.md` and `mass-budget.json`, which the render captions and the viewer read. Housing masses are computed from the geometry; electronics are typical-datasheet masses for the parts in `hardware/bom/`.

**What changed in this revision:**
- Atlas is computed at the D12 thickness of 13.5 mm (frame 12.55).
- The mid-frame and thermal stack now follow the hardware BOM: SUS 0.2 stamped mid-frame, Cu/graphite/VC-lite, plus a 0.4 mm vapour chamber on Atlas.
- Pebble electronics follow the Lite BOM (D10).
- Net effect: Pebble 33 → 31.9 g, Square 57 → 58.6 g, Atlas 85 → 88.6 g.

<!-- mass-budget:begin -->

**LORE Pebble: 31.9 g** (estimate, ±10 %)

| Part | g | % |
|---|---:|---:|
| Housing top + back, PC-GF10, 1.4 mm wall | 7.8 | 24 |
| 2K soft-touch PU paint (~40 um) | 0.4 | 1 |
| Talk cap + PMMA light guide | 1.6 | 5 |
| Battery 650 mAh / 2.52 Wh | 11.5 | 36 |
| Logic board + shields, Lite (D10): BT audio SoC, nRF54L15, 64 MB NOR, LC29HAA GNSS, 36x36 8L HDI | 3.6 | 11 |
| Speaker 13x9 + acoustic seal | 1.3 | 4 |
| LORE Mount: 316L insert + N52 ring magnet | 3.4 | 11 |
| 4-pin pogo receiver, LRA, 2 mics, flexes, PSA, screws | 2.4 | 8 |
| **Total** | **31.9** | 100 |

**LORE Square: 58.6 g** (estimate, ±10 %)

| Part | g | % |
|---|---:|---:|
| Unibody, 6013-T6 Al, 1.2 mm wall + ledges | 10.2 | 17 |
| Cover, Victus 2 0.7 mm | 3.6 | 6 |
| Back, AG glass 0.7 mm | 3.4 | 6 |
| AMOLED module 1.6" + on-cell touch | 2.6 | 4 |
| Mid-frame SUS 0.2 stamped (display support, ground) | 2.2 | 4 |
| Thermal: Cu 50 um + 2x graphite + TIM + VC-lite 0.3 | 1.4 | 2 |
| Battery 1100 mAh / 4.27 Wh | 19.4 | 33 |
| Logic board 48x48 10L ELIC + shields (Genio 720, 6 GB, 64 GB UFS, LTE Cat-1bis per D11) | 5.6 | 10 |
| Speaker 15x11, LRA, mics, flexes | 3.2 | 5 |
| Crown (encoder) + Talk + SOS keys | 1.1 | 2 |
| LORE Mount: 316L insert + N52 ring magnet + 4-pin pogo | 3.6 | 6 |
| Antennas, USB-C receptacle, PSA, gaskets, screws | 2.3 | 4 |
| **Total** | **58.6** | 100 |

**LORE Atlas: 88.6 g** (estimate, ±10 %)

| Part | g | % |
|---|---:|---:|
| Unibody, Ti-6Al-4V, 1.2 mm wall + ledges | 18.2 | 21 |
| Cover, sapphire 0.8 mm | 6.8 | 8 |
| Back, zirconia 0.9 mm | 10.9 | 12 |
| AMOLED module 1.6" + on-cell touch | 2.6 | 3 |
| Mid-frame SUS 0.2 stamped (display support, ground) | 2.2 | 2 |
| Thermal: Cu 50 um + 2x graphite + TIM + VC-lite 0.3 + Ti-compatible VC 0.4 + Cu spreader | 3.0 | 3 |
| Battery 1450 mAh / 5.63 Wh | 25.6 | 29 |
| Logic boards, sandwich 2x46x46 + 1.6 interposer (Genio 720, 8 GB, 128 GB UFS, LTE, BG95-S5 NTN) | 7.5 | 8 |
| Speaker 15x11, LRA, mics, flexes | 3.2 | 4 |
| Crown (encoder) + Talk + SOS keys | 1.6 | 2 |
| LORE Mount: 316L insert + N52 ring magnet + 4-pin pogo | 3.6 | 4 |
| Antennas, USB-C receptacle, PSA, gaskets, screws | 2.3 | 3 |
| Glance camera OV13B10 module + trim | 1.1 | 1 |
| **Total** | **88.6** | 100 |

<!-- mass-budget:end -->

## 8. CMF (colour · material · finish)

| SKU / finish | Substrate | Process | Colour target | Gloss / Ra | Notes |
|---|---|---|---|---|---|
| Pebble **Bone** | PC + 10 % GF (e.g. SABIC Lexan 3412R class) | Injection mould, then 2K PU soft-touch paint, 35–45 µm | Bone `#F3EEE6`, L\* 93 | 2–3 GU @ 60° | Anti-yellowing UV package. ΔE < 1.5 after 300 h Xenon |
| Pebble **Ink** | same | same | Ink `#14161A` | 2–3 GU | Pigment chosen for low sebum shine (rub test, 5,000 cycles) |
| Pebble **Terracotta** | same | same | Terracotta `#C4623A` | 2–3 GU | Brand accent colour. Brand holds the Lab master |
| Pebble light guide | PMMA, frosted | Mould, then texture VDI 24 on the outer face | Clear / diffuse | — | Even ring with 8 LEDs: luminance uniformity ≥ 70 % (E) |
| Square **Ink** | 6013-T6 Al | CNC → tumble → **bead-blast (ceramic B120)** → Type II sulphuric anodise 12–15 µm, black/blue-black dye, hot-water seal → **diamond-cut chamfer** (bright, clear re-anodise 5 µm) | near `#3B3C40` | Ra 0.8–1.0 body / Ra 0.05 chamfer | NMT splits in PBT colour-matched to the dye |
| Square **Sand** | same | same process, gold-bronze dye at low concentration | near `#CDBDA3` | same | Hardest anodise colour to hold. ΔE < 1.0 batch to batch |
| Square crown | 316L (hardware MEC3) | Turn + knurl → bead-blast → PVD: black CrN (Ink) / light ZrN "champagne" (Sand) | matched to the body, ΔE < 3 | knurl satin, cap polished | Steel stays crisp where anodised Al would wear at the knurl |
| Talk key (Square) | 6063 Al | Bead-blast + Terracotta anodise | Terracotta | Ra 0.8 | A separate part, so it can be tinted independently |
| SOS key (S/A) | 316L | Bead-blast, body-matched PVD; ridged face | body colour | Ra 0.8 | Found by its pocket and ridges, not by colour. See §12 H6 |
| Atlas **Titanium** | Ti-6Al-4V | CNC → **bead-blast (glass bead 100 µm)** → passivate. Chamfer hand-polished | natural, ~`#A29D94` | Ra 0.6–0.9 | No coating, so wear only patinates |
| Atlas **Black DLC** | Ti-6Al-4V | Bead-blast → **DLC (a-C:H, PACVD), 2–3 µm, ~2,000 HV** | `#2A2A2D` | Ra 0.4 | The chamfer is polished before coating, so it stays bright |
| Atlas crown | Ti Gr.5 | Polish + **ZrN PVD**, 0.5 µm | "brass-tone" | mirror cap / satin knurl | Matches Brass `#B8935A` within ΔE 3 |
| Cover (S/A) | Victus 2 / sapphire | 2-layer ink mask, AF coating. AR coating on sapphire | — | — | The mask hides the 1.6" border on the 47.75 cover |
| Back (S/A) | AG glass 0.7 / zirconia 0.9 | AG etch, colour back-print / sinter, polish, laser etch | body-matched | AG haze 10–15 % | See §12 H4 (hardware's PC+GF IMR back is the cost-down fallback) |

## 9. Sealing and IP

| SKU | IP target | Ports and openings |
|---|---|---|
| Pebble | IP67 (1 m, 30 min) | No open port: 2 mics, speaker grille, button wiper seal |
| Square | IP67 (1 m, 30 min) | USB-C (sealed), 3 mics, speaker, crown, 2 keys |
| Atlas | IP68 (1.5 m, 30 min) | As Square, plus the camera window (bonded sapphire, PSA + adhesive) |

| Path | Solution |
|---|---|
| Cover to frame | 0.25 PSA gasket (tesa 61395 class) + 0.2 dispensed adhesive bead |
| Back to frame | PSA + perimeter LSR gasket. The back stays serviceable (heat-release PSA) |
| Crown | Double FKM O-ring on the stem, plus a labyrinth |
| Keys | Silicone boot under the key, 0.3 compression |
| Acoustic | ePTFE membranes rated 1 m / 30 min (IP67), and 1.5 m on Atlas (IP68) |
| USB-C | Sealed receptacle with an integral O-ring. The port tolerates wet insertion: the PMIC detects moisture and disables VBUS |
| Pressure | One ePTFE vent behind the speaker equalises barometric change (the BMP390 reads through it) |
| Pogo pads | Insert-moulded / glass-frit sealed through the 316L insert; no gasket path |

## 10. Drop and durability

| Test | Target |
|---|---|
| Free fall | 1.5 m onto concrete, 26 drops (6 faces, 12 edges, 8 corners), per IEC 60068-2-31. Pebble also gets 1.0 m lanyard-swing impacts |
| Tumble | 500 cycles at 0.5 m (IEC 60068-2-31 tumble) |
| Glass | Victus 2: Corning's lab claim is survival of drops up to 1 m onto a concrete-replica surface; we verify on our stack at EVT. Sapphire is Mohs 9: scratch-proof, but more brittle on edge hits, hence the metal lip |
| Clip / lanyard | 50 N pull at the LORE Mount. Above 80 N the lanyard yoke breaks away by design (safety) |

**Impact energy at 1.5 m (E = m·g·h):**
- Pebble: 0.47 J
- Square: 0.86 J
- Atlas: 1.30 J (+51 % over Square)

**Per-SKU drop design:**
- **Pebble.** The soft-touch PC + GF shell absorbs impact, and there is no glass. The cap floats on 4 snap hooks with 0.2 clearance, and the dome and fillets have no sharp edge that could concentrate a strike.
- **Square.** The glass is proud by only 0.15, inside a 0.35 metal lip, so a corner hit lands on metal first. The frame corners have a 1.4 local wall. The battery has 0.3 Z clearance and a foam pad. The crown sits in the side-wall zone, not on a corner.
- **Atlas.** Everything on Square applies, plus the following:
  - The 51 % higher drop energy goes into a Ti frame with ~2.5× the yield strength of 6013-T6 Al (~880 vs ~350 MPa).
  - The zirconia back is 0.9 thick (sintered, ~1,000 MPa flexural strength).
  - The camera window sits 0.1 below the sapphire surface (design target), so a face-down drop does not land on it.
  - The Rugged Case (accessories.md) is the recommended add-on for adventure use.

## 11. Packaging fit check (ID cavity vs hardware parts)

`scripts/fit_check.py` checks hardware's cells and PCBs against the inner cavity (outer plan offset by the wall, with fillet run-out near the faces, 0.3 clearance). It is an estimate, not CAD.

| SKU | Part | Fits? | Note |
|---|---|---|---|
| Pebble | Cell LP553532, 35 × 32 × 5.5, 650 mAh (bom_pebble_lite BT1) | **No** (corner index 1.53) | Square-cornered parts do not fit inside a 42 mm n = 2.6 superellipse |
| Pebble | PCB 36 × 36 R9 (pcb-stackup §1) | **No** (1.22) | |
| Pebble | **ID proposal:** cell 30 × 27 × 5.5, ~470 mAh (E) | yes | Scaling ECR-01's "~3+ day" Lite estimate by capacity gives ~2.2 days (E), still above the 1.5-day claim. −3.2 g |
| Pebble | **ID proposal:** PCB 35 × 35 R12 | yes | |
| Square | Cell 46 × 40 × 4.0, 1100 mAh | yes (0.59) | |
| Square | PCB 48 × 48 R10 | yes (0.62) | |
| Atlas | Cell 46 × 40 × 5.2, 1450 mAh | yes (0.59) | |
| Atlas | PCB sandwich 46 × 46 (R10 assumed) | yes (0.43) | |

## 12. Hardware alignment register (ID ↔ `hardware/`)

| # | Topic | Hardware says | ID position | Status |
|---|---|---|---|---|
| H1 | Pogo | J2 `POGO-4P-1.5mm`, 4-pin | Adopted: 4 pads Ø1.6 @ 2.5 (V+ · D · ID · GND). Was 2 pads in ID-A2 | **Closed** (params, geometry, drawings and renders updated) |
| H2 | Pebble LED count | 8 RGB LEDs on LP5024 | Adopted: 8 | **Closed** |
| H3 | Pebble USB-C | Lite BOM keeps J1 USB-C + in-box C-to-C cable | Delete J1. Ship a USB-C-to-LORE-Mount magnetic charging cable instead of ACC1 (about cost-neutral). Benefits: one less seal path, the IP67 claim gets simpler, and the face stays clean | **Open**: needs a hardware decision |
| H4 | Square back | MEC2 PC + GF, IMR texture | AG-etched glass 0.7 is the design intent (premium feel, colour-matched). PC + GF IMR is the D11 cost-down fallback (−$1.10 E) | **Open**: Finance / Hardware |
| H5 | Cover thickness | Square 0.55 aluminosilicate; Atlas sapphire 0.7 | Square Victus 2 **0.7**; Atlas sapphire **0.8**, for drop margin. pcb-stackup §3 carries 2.65 of frame and tolerance allowance, so +0.15 / +0.1 can be absorbed | **Open**: confirm in the EVT drop build |
| H6 | SOS accent | MEC4 "terracotta SOS accent" | Terracotta goes on the **Talk** key (most-used control, brand accent). SOS stays body-coloured and is found by its recessed ridged pocket, which avoids a red "panic" cue on a travel object | **Open**: UX to confirm |
| H7 | Pebble shell resin | MEC1 PC + 30 % GF | PC + **10 %** GF: better soft-touch paint adhesion, no fibre read-through on the domes, and better impact. Stiffness comes from 0.8 ribs | **Open**: molder DFM |
| H8 | Pebble cell and PCB | 35 × 32 × 5.5 cell; 36 × 36 R9 PCB | Do not fit (§11). Proposal: 30 × 27 cell, 35 × 35 R12 board, or keep the cell and grow the plan to 44 mm | **Open**: blocks Pebble EVT layout |
| H9 | Mid-frame | MEC7 SUS 0.2 stamped | Adopted in the mass budget and the exploded render (was PC-GF30 + Mg) | **Closed** |
| H10 | Square LTE | D11: Cat-1bis | Exploded-view label and mass budget updated. Removes the L-shaped-cell risk | **Closed** |
| H11 | Atlas thickness | ECR-02: 13.5 mm | Adopted (D12). Mass, drawings, models, captions and spec all at 13.5 | **Closed** |

## 13. Open issues

1. **1.6" panel.** The cut is semi-custom (hardware estimates $40–80k NRE). EVT runs on the 1.43" panel, which grows the black border to about 11 mm. Accepted for EVT.
2. **Atlas mass (88.6 g)** is the heaviest in the family. A DVT option is a 0.9 mm Ti wall: −6 g (E), but it needs FEA plus a drop re-test.
3. **Square antenna splits** need a 3D-tuned position from RF simulation (`hardware/simulations`). x = ±12 is a placeholder.
4. **Pebble packaging (H8)** is the critical-path ID↔hardware item for Pebble EVT.
5. **SOS pocket and Mount recess** are drawn as true recesses. The 3D models show them as flush decals (no boolean cut). The drawings govern.

## 14. Regenerating this package

```
cd design
python3 industrial/scripts/mass_budget.py      # mass-budget.md/.json + §7 tables in this file
python3 industrial/scripts/drawings.py         # drawings/*.svg + *.png
python3 industrial/scripts/fit_check.py        # §11 table (prints markdown)
node tools/render.mjs industrial/scripts/jobs-export.json        # models/*.glb, *.stl
node tools/render.mjs industrial/scripts/jobs-accessories.json   # accessory renders
python3 industrial/scripts/contact_sheet.py    # renders/contact-sheet.png
```
