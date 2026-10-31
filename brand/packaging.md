# LORE packaging

**Owner:** Brand (with Design for inserts and Legal-ops for regulatory marks and supply) · **v0.3 concept for supplier RFQ** · 2026-10-31
**Files:** dielines `packaging/dieline-{pebble,square,atlas}.svg` (1:1 mm) · art `packaging/box-art.svg` · previews `packaging/png/` · generator `scripts/build_packaging.py`

> All dimensions are **structural estimates** based on the COMPANY.md device sizes (Pebble 42×42×14 mm, Square/Atlas 54×54×12 mm). They freeze after EVT units and supplier white samples (Q1 2027). Paper names are **candidates to verify** for availability, FSC certification and price.

## 1. Principles
1. **Zero plastic.** No film windows, no PET trays, no foam, no lamination, no plastic cable ties, no shrink-wrap. Tamper evidence comes from paper seals.
2. **FSC-certified fibre only** (FSC Recycled or FSC Mix). Use water-based PVA or starch glues, and soy/vegetable-based or low-migration inks.
3. **One-handed, unhurried opening.** Opening the box should feel like a door slowly opening.
4. **Quiet outside, warm inside.** The outside is calm (Bone or Ink), and the inside lid carries a Terracotta message.
5. **Right-sized.** Keep void fill under 40% and size the box to the contents. We aim to fit a 300 × 200 mm e-commerce mailer (Pebble/Square) to cut shipping volume.
6. **Recyclable as a whole** in household paper recycling. The only exceptions are Atlas magnets (if used) and foil, which must be checked (see §6).

## 2. SKUs and structures

| | **LORE Pebble** (LP-01) | **LORE Square** (LS-01) | **LORE Atlas** (LA-01) |
|---|---|---|---|
| Price (target) | $149 | $299 | $599 |
| Structure | **Drawer box**: glue-free double-wall tray + wrap sleeve | **Rigid set-up box**: telescoping lid and base | **Rigid set-up box**, deeper, with a ribbon pull and a 2-tier insert |
| Outer dims (est.) | Sleeve ≈ 102 × 101 × 40 mm | Lid 132 × 132 × 48 mm (base 128 × 128 × 46) | Lid 159 × 159 × 62 mm (base 154 × 154 × 60) |
| Board | 400 g/m² FSC Recycled uncoated folding boxboard (tray). 360 g/m² through-dyed Terracotta (sleeve) | 1.5 mm FSC Recycled greyboard | 2.0 mm FSC Recycled greyboard |
| Wrap / face stock (candidate) | Tray Bone (cand. Fedrigoni *Materica Gesso*). Sleeve *Materica Terra Rossa* | 120 g/m² Bone uncoated (cand. *Materica Gesso*) | 140 g/m² Ink through-dyed (cand. *Materica Pepper*) |
| Inside liner | Printed inside of tray base | 120 g/m² Terracotta liner (inside lid) | Terracotta liner + Brass foil keyhole |
| Insert | Wet-pressed moulded fibre nest (device + clip) | Wet-pressed moulded fibre: device nest, finger scoop, cable/lanyard well | 2-tier moulded fibre plus a paperboard drawer for LORE Kit accessories |
| Print / finish | Sleeve: 1 PMS Bone line pattern. Tray: blind deboss | Lid: 0.5 mm **blind deboss** keyhole, Ink 1-PMS wordmark | Lid: **brass-tone hot foil** keyhole and wordmark, 12 mm undyed cotton grosgrain ribbon pull |
| Contents | Pebble, Clip, USB-C cable (paper band), Quick-start card, "Look up." card | Square, wrist strap or lanyard, USB-C cable, Quick-start, eSIM activation card (QR only), Look-up card | Atlas, leather lanyard, magnetic dock, USB-C cable, Quick-start, **Atlas Journal** (A6 linen, 96 pp), Look-up card |
| Est. packed weight | ≈ 140 g | ≈ 330 g | ≈ 620 g |

Weights are estimates. Packaging cost is owned by Finance and Legal-ops (supply) RFQs. As a planning guide, packaging should stay at or below roughly 3–5% of retail price per SKU. **Not supplier-quoted.**

## 3. Dielines

| File | Contents |
|---|---|
| `packaging/dieline-pebble.svg` | Double-wall tray (four lock tabs into base slots, corner flaps tucked between walls, Ø22 thumb notch through both layers) + sleeve (glue seam 14 mm, open ends, Ø24 thumb notches) |
| `packaging/dieline-square.svg` | Lid and base **wrap papers** (15 mm turn-ins, corner ears, glue area) + greyboard blanks (V-grooved, corner-taped with paper tape) |
| `packaging/dieline-atlas.svg` | Same as Square at Atlas dimensions, 18 mm turn-in, 2.0 mm board |

**Conventions:** CUT is solid magenta `#E6007E`. CREASE is dashed cyan `#009FE3`. BLEED is 3 mm, dotted green. GLUE is hatched orange. Units are mm at 1:1. Convert to the converter's template (ArtiosCAD/ESKO) before production. Board caliper `t` is estimated at 0.6 mm (folding board) and 1.5/2.0 mm (greyboard).

**Tolerances:** the lid-to-base clearance is 1.0 mm air gap. This gives the slow "parachute" lift, where air resistance lowers the base out of the lid over about 2–3 s. Prototype with ±0.3 mm iterations. Sleeve-to-tray clearance is 1.0 mm.

## 4. Art and print

See `packaging/box-art.svg` / `png/box-art.png`.
- **Pebble sleeve top:** Terracotta stock with a Bone hairline street pattern. It is illustrative now and will be generated from OpenStreetMap data per City Bundle, with ODbL credit. Bone wordmark and "PEBBLE".
- **Square lid:** Bone wrap, 0.5 mm blind-debossed Keyhole symbol Ø36 mm, Ink wordmark 6 mm cap, "SQUARE" in mono.
- **Atlas lid:** Ink wrap with brass-tone foil keyhole and wordmark. The cotton ribbon pull exits the right side.
- **Front wall (Square shown):** "Every street has a story." in Fraunces, a mono spec line and a **regulatory zone** (CE, UKCA, FCC ID, WEEE bin, battery marks, FSC label with licence code, recycling instructions, country of origin). **Legal-ops supplies the final marks. Brand does not draw regulatory marks.**
- **Base underside:** barcode (GTIN-13, from GS1 membership), SKU, colour, IMEI/serial label area (paper label), and the FSC label.
- **Colour management:** use Pantone for Ink and Terracotta where flat print is needed, and through-dyed stocks elsewhere. Approve on press against drawdowns.

## 5. Opening sequence (Square / Atlas; the Pebble version is in brackets)
1. **The seal.** A 20 mm Bone paper seal with a debossed keyhole closes the belly band. Breaking it is the only tamper evidence. *(Pebble: the seal sits on the sleeve end.)*
2. **The lift.** Lift the lid by the sides (Atlas: by the ribbon). The base sinks out slowly on its air cushion over about 2–3 s. *(Pebble: push the tray out of the sleeve through the thumb notch.)*
3. **The message.** The first thing you see is the Terracotta inside lid:
   > ***Look up.*** The best things in a city are rarely at eye level. A date over a doorway. A saint on a corner. A keyhole with a dome inside it. Put your phone away. We'll tell you where to look.
4. **The object.** The device sits alone in a fibre nest, screen down (Square/Atlas) so the first thing you see is the back engraving. A finger scoop sits at 12 o'clock.
5. **The card.** Beneath the device is the "Hello." quick-start card with four steps: hold 3 s, pair earphones, scan for the app, walk.
6. **The rest.** Lift the fibre tray to find the cable (paper-banded), strap or lanyard and documents. Atlas adds a drawer holding the dock and the Atlas Journal.
7. **The sound.** On first power-on, the device plays the sonic logo (D5–A5–D6) and says: *"Hello. I'm LORE. Let's go and look at something."*

## 6. Sustainability checks and open questions
- [ ] Confirm FSC chain-of-custody certificates for the converter and every paper (Legal-ops).
- [ ] Hot foil: check repulpability with the supplier, or switch Atlas to **blind deboss + brass ink**.
- [ ] Atlas ribbon: check undyed cotton supply. No magnets are planned. If a magnetic closure is added, it must be removable and labelled.
- [ ] Moulded fibre: specify wet-pressed (smooth) vs dry-pressed (cheaper, rougher) after samples. The target is a smooth finish for Square and Atlas.
- [ ] Shipping test to ISTA 3A for e-commerce, and drop test the base nest with EVT units.
- [ ] EPR/packaging-law labelling for the EU (PPWR), UK and US states. Legal-ops owns this.
- [ ] Do a carbon/LCA estimate once weights are real. Don't make claims before then.
