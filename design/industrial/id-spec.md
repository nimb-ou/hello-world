# LORE industrial design specification: Pebble P1 · Square S1 · Atlas A1

**Rev:** EVT-0 / ID-A3 · 2026-10-31 · Owner: Head of Design · Status: frozen for EVT tooling quotes, open for DVT
**Sources of truth:** geometry lives in [`params.json`](params.json), which drives the 3D models, the drawings and the mass budget. Electronics come from `hardware/README.md` and `hardware/system-architecture.md`. Product decisions D10–D13 are in `company/decisions-log.md`.
All dimensions are in mm. **(E)** marks an estimate that EVT measurement must confirm.

---

## 1. Design intent

LORE is worn, not held. The phone stays in the pocket and LORE sits on a strap, a lanyard or a palm. Three rules drove every decision:

1. **Operable blind.** Every primary action can be found by touch alone, with a different texture per control:
   - Pebble: a concave dish.
   - Square and Atlas: a knurled crown, a smooth pill and a ridged recess.
2. **Quiet object.** There is no visible logo on the front. Front-side colour is limited to one accent: the Terracotta Talk key or the brass-tone crown. The LED ring is the only thing that "speaks".
3. **One interface.** Every SKU and every accessory meets at the **LORE Mount** (§2). That gives one clip, one dock and one lanyard for the whole family.

Reference set: Leica Q3 (tactile restraint), Teenage Engineering OP-1 field (honest controls), Nothing Ear (light as language), Apple Watch Ultra (crown guarding and titanium finishing).

## 2. Shared architecture: the LORE Mount

| Item | Spec |
|---|---|
| Female recess (device back) | Ø24.0, 0.6 deep, 316L stainless insert, bead-blast Ra 0.8 |
| Lock | 3 bayonet lugs, 4.0 wide, 30° twist to lock, spring detent ≥ 1.5 N·cm |
| Magnet | N52 sintered NdFeB ring, OD 22 / ID 14 / 1.0 thick, Ni-Cu-Ni + epoxy, axially magnetised. Self-aligns and holds 0.9 kgf on steel (E) without the twist |
| Pogo | 2 pads, Ø2.0 at 5.0 pitch, Au 0.76 µm over Ni, flush to −0.05. Mating pins: Mill-Max 0906-class spring pins, 1.0 N each |
| Power | 5 V / 1 A (5 W) over pogo. Polarity is keyed by lug geometry, and the 1-wire ID pin is shared with V− (accessory ID by resistor) |
| Test | 10,000 twist cycles, 50 N straight pull (locked), 1,000 h salt-fog on the 316L insert |

Every accessory carries the male puck: Ø23.6 × 2.4, with 3 lugs and 2 spring pins.

## 3. LORE Pebble (P1), the "Lite" tethered design (D10)

| Parameter | Value |
|---|---|
| Envelope | **42.0 × 42.0 × 14.0** (plan superellipse n = 2.6; body 12.6 + top dome 0.95 + back dome 0.45) |
| Edge radii | Top fillet R5.0, bottom fillet R4.2, continuous with the domes (G1 at EVT, G2 target at DVT) |
| Wall | 1.4 nominal PC+10 % GF; 1.0 minimum at the speaker grille; 0.8 ribs on 6 mm pitch |
| Talk control | The **whole top cap is the button**: a floating dish, ~23 across flats, 0.45 concave, 0.35 travel, metal dome 2.4 N, 0.3 parting gap with a TPE wiper seal |
| LED ring | Frosted PMMA light guide following the plan outline, ~1.0 wide, flush +0.03. 8 RGB LEDs on TI LP5024 per hardware/ (the drawings show 12 positions, reconcile at EVT) |
| Volume rocker | East side, centred, 9.0 × 2.6 pill, 0.6 proud, 0.25 travel |
| Mics | 2 × Ø0.8 on the north edge, 14 apart (beamforming axis = forward when clipped), ePTFE membranes |
| Speaker | 13 × 9 (hardware) behind 9 × Ø0.7 holes at 1.4 pitch, south edge. ePTFE (GORE AE-series class) |
| Charging | Pogo only, through the LORE Mount. **No USB-C**: it saves 3.5 mm of Z, a seal path and about $0.60, and the Dock, Power Puck and clip-charger cover travel |
| Tether | Hidden tunnel for a 2 mm cord: 2 × Ø2.2 holes at 5 pitch on the back, NW corner |
| IP | **IP67** (1 m, 30 min). There is no open port, and the button uses a wiper seal plus an internal membrane |
| Mass | **33 g (E)**. See [mass-budget.md](mass-budget.md) |
| Battery | 650 mAh / 2.52 Wh (hardware/) |

**Ergonomics.**
- 42 mm sits inside the P5 female palm width (about 69 mm) and the thumb pad lands naturally in the dish.
- The rocker is under the index finger when the Pebble is pinched.
- At 14 mm thick, the Pebble does not roll when set down; the back dome is only 0.45.
- Clipped on a strap, the dish faces outward and up, so a press from above is natural and the ring is visible in peripheral vision.

## 4. LORE Square (S1)

| Parameter | Value |
|---|---|
| Envelope | **54.0 × 54.0 × 12.0** (back bulge 0.8 + frame 11.05 + glass proud 0.15) |
| Plan | Rounded square, R13 corners with superelliptic blend (n = 3.4, curvature-continuous) |
| Edge radii | Front R2.0, back R3.0. Diamond-cut chamfer 0.35 × 45° around the glass |
| Wall | 1.2 aluminium. 0.8 minimum at the antenna splits |
| Cover | Corning Gorilla Glass Victus 2, 0.7, 2.5D edge, 47.0 across flats, black ink mask, ALS window at y = +19 |
| Display | 1.6" AMOLED, 466 × 466, 28.73 square active area, R5.5 corners, ~412 ppi, on-cell touch, 1000-nit HBM (hardware/). **EVT uses the standard 1.43" panel.** The ID shows the 1.6" semi-custom cut |
| Crown | Right side at y = +9: Ø6.0, 2.2 proud, 40-ridge knurl, PixArt PAT9125EL optical rotation + push, with an O-ring on the stem |
| Talk key | Right side at y = −8: 11.0 × 3.6 pill, 0.8 proud, Terracotta anodise, 0.3 travel, 3.0 N |
| SOS key | Left side at y = −2: 7.0 × 3.0, **recessed 0.25 in a ridged pocket**, so a pocket or bag cannot press it. A 2 s hold is required (see ux-spec §6) |
| USB-C | Bottom edge, centred, 9.2 × 3.4 opening, IPX7-rated receptacle (e.g. a JAE DX07-class waterproof receptacle), USB 2.0 + PD sink |
| Speaker | 15 × 11 box, 5 slots 0.8 × 3.2 at 1.7 pitch, bottom edge right of USB-C, ePTFE |
| Mics | 3: 2 on the top edge at x = ±6 (beamforming), 1 on the bottom edge at x = −10 (AEC reference) |
| Antennas | Frame-as-antenna with **4 nano-moulded (NMT) PBT splits**, 0.8 wide, on the top and bottom edges at x = ±12. LTE (Cat-1bis per D11), GNSS L1+L5, Wi-Fi/BT |
| Back | AG-etched glass 0.7, colour-matched, with the LORE Mount insert. Laser etch: LORE wordmark, model, regulatory text |
| Tether | Ø1.8 cross-drilled tether hole in the NW corner, for a cord loop |
| Left-hand use | The plan is symmetric, so *Settings → Rotate 180°* puts the crown and Talk key on the left (UI and IMU frame flip) |
| IP | **IP67**. eSIM only, so there is no tray |
| Mass | **57 g (E)** |
| Battery | 1100 mAh / 4.27 Wh |

## 5. LORE Atlas (A1): differences from Square

| Parameter | Value |
|---|---|
| Envelope | **54.0 × 54.0 × 13.5** (ECR-02 / D12). The extra 1.5 mm is all battery: 1450 mAh / 5.63 Wh, so the claim is "2+ days" |
| Body | Ti-6Al-4V (Grade 5), 5-axis CNC from bar. Natural bead-blast or black DLC |
| Cover | Sapphire 0.8, double-side AR (R < 1 %), oleophobic |
| Back | Zirconia ceramic 0.9 (RF-transparent for LTE, NTN and GNSS). Warm grey on Ti, black on DLC |
| Crown | Ti stem and cap with **ZrN PVD "brass-tone"** (L\*a\*b\* ≈ 72 / 4 / 28). It will not tarnish, unlike real brass |
| Glance camera | Front, top band at y = +19: OV13B10 13 MP (hardware/), Ø2.6 lens under a Ø5.2 polished trim. A **hardware-wired white privacy LED** sits 4.2 mm right of the lens and is on whenever the sensor is powered (firmware cannot override it) |
| Satellite SOS | Quectel BG95-S5 NTN (Skylo). The patch and frame antenna are tuned for sky view when the device is on the chest |
| IP | **IP68** (1.5 m, 30 min) |
| Mass | **85 g (E)**. A titanium lanyard draws ~0.8 N on the neck, which is comfortable (lighter than a typical 90 g ID badge with holder) |

## 6. Control layout rationale

- **Crown above the Talk key on the same side.** The thumb sweeps vertically with no grip change. The crown sits at the top so that, on a lanyard, the hand comes up from below and meets the Talk key first, because Talk is the most frequent action.
- **SOS on the opposite side, recessed.** Opposition makes a squeeze-plus-hold a deliberate act. The hold is 2 s with haptic pulses (ux-spec §6). Accidental-trigger target: < 1 per 1,000 device-days in EVT pocket tests.
- **Tactile coding.** The crown is knurled, Talk is smooth and convex, SOS is a ridged concave pocket, and the Pebble Talk is a smooth concave dish. All are told apart by touch with gloves on (EN 420 class 2 test planned).

## 7. CMF (colour · material · finish)

| SKU / finish | Substrate | Process | Colour target | Gloss / Ra | Notes |
|---|---|---|---|---|---|
| Pebble **Bone** | PC+10 % GF (e.g. SABIC Lexan 3412R class) | Injection mould → 2K PU soft-touch paint, 35–45 µm | Bone, ref. `#F3EEE6`, L\* 93 | 2–3 GU @60° | Anti-yellowing UV package; ΔE < 1.5 after 300 h Xenon |
| Pebble **Ink** | same | same | Ink `#14161A` | 2–3 GU | Pigment chosen for low sebum shine (rub test 5,000 cycles) |
| Pebble **Terracotta** | same | same | Terracotta `#C4623A` | 2–3 GU | Brand accent colour; Lab master held by Brand |
| Square **Ink** | 6013-T6 Al | CNC → tumble → **bead-blast (ceramic B120)** → Type II sulphuric anodise 12–15 µm, black/blue-black dye, hot-water seal → **diamond-cut chamfer** (bright, clear re-anodise 5 µm) | near `#3B3C40` | Ra 0.8–1.0 body / Ra 0.05 chamfer | NMT splits in PBT colour-matched to dye |
| Square **Sand** | same | same, gold-bronze dye at low concentration | near `#CDBDA3` | same | Hardest anodise colour to hold; ΔE < 1.0 batch to batch |
| Talk key (both Square) | 6063 Al | Bead-blast + Terracotta anodise | Terracotta | Ra 0.8 | Separate part so it can be tinted independently |
| Atlas **Titanium** | Ti-6Al-4V | CNC → **bead-blast (glass bead 100 µm)** → passivate. Chamfer hand-polished | natural, ~`#A29D94` | Ra 0.6–0.9 | No coating, so wear only patinates |
| Atlas **Black DLC** | Ti-6Al-4V | Bead-blast → **DLC (a-C:H, PACVD), 2–3 µm, ~2,000 HV** | `#2A2A2D` | Ra 0.4 | Chamfer polished before coating so it stays bright |
| Atlas crown | Ti Gr.5 | Polish + **ZrN PVD**, 0.5 µm | "brass-tone" | mirror cap / knurl satin | Matches Brass `#B8935A` within ΔE 3 |
| Cover (S/A) | Victus 2 / sapphire | Ink mask (2 layers), AF coating. AR coating on sapphire | — | — | Mask hides the 1.6" border on a 47 mm cover |

## 8. Sealing and IP

| Path | Solution |
|---|---|
| Cover to frame | 0.25 PSA gasket (tesa 61395 class) + 0.2 dispensed adhesive bead |
| Back to frame | PSA + perimeter LSR gasket; the back stays serviceable (heat-release PSA) |
| Crown | Double O-ring on the stem (FKM), plus a labyrinth |
| Keys | Silicone boot under the key, 0.3 compression |
| Acoustic | ePTFE membranes, 1 m / 30 min rated (IP67) and 1.5 m (IP68) on Atlas |
| USB-C | Sealed receptacle with an integral O-ring. The port tolerates wet insertion; the PMIC detects moisture and disables VBUS |
| Pressure | One ePTFE vent behind the speaker equalises barometric change (BMP390 reads through it) |

## 9. Drop and durability

| Test | Target |
|---|---|
| Free fall | 1.5 m onto concrete, 26 drops (6 faces, 12 edges, 8 corners), per IEC 60068-2-31. 1.0 m for Pebble on a lanyard swing |
| Tumble | 500 cycles at 0.5 m (IEC 60068-2-31 tumble) |
| Glass | Victus 2 survives a 2.0 m drop onto 180-grit (Corning rating). Sapphire Mohs 9 |
| Design features | Glass proud only 0.15 with a 0.35 metal lip around it, so a corner hit lands on metal first. Frame corners have 1.4 local wall. The battery has 0.3 Z clearance and a foam pad. The crown sits in the side-wall zone, not on a corner |
| Pebble | Soft-touch over GF-PC absorbs impact. No glass. The cap floats on 4 snap hooks with 0.2 clearance |
| Clip/lanyard | 50 N pull at the LORE Mount. Above 80 N the lanyard yoke is designed to break away (safety) |

## 10. Mass summary (estimate)

Pebble **33 g** · Square **57 g** · Atlas **85 g**. Full breakdown: [mass-budget.md](mass-budget.md) (generated by `scripts/mass_budget.py`).

## 11. Open issues and ECR alignment

1. **1.6" panel.** The cut is semi-custom (hardware/ estimates $40–80k NRE). EVT runs on the 1.43" panel, which grows the black border to about 11 mm. Accepted for EVT.
2. **Pebble LED count.** The ID shows 12 positions and hardware/ specifies 8 on the LP5024. 8 is fine optically with a 1.0 frosted guide: use 8.
3. **Atlas weight (85 g)** is the heaviest in the family. A DVT option is a 0.9 mm Ti wall (−6 g, needs FEA).
4. **Square antenna splits** need a 3D-tuned position from RF simulation (`hardware/simulations`). x = ±12 is a placeholder.
5. **SOS key** was added per hardware/system-architecture.md ("SOS button"). Pebble has no dedicated SOS key: it uses the Talk dish held for 3 s, plus phone confirmation (ux-spec §6).
