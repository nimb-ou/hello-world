# PCB Stack-up, Board Outline and Internal Stack

All dimensions are estimates to be confirmed with the ID team (`design/`) and the PCB fab DFM review.

## 1. Board outlines

| SKU | Enclosure (ID) | Main PCB outline | Thickness | Placement |
|---|---|---|---|---|
| Pebble | 42 × 42 × 14 mm rounded pebble | 36 × 36 mm rounded-square (R 9 mm), one board + 2 flexes | 0.8 mm | double-sided; battery beside/under board |
| Square | 54 × 54 × 12 mm | **48 × 48 mm** rounded (R 10 mm) with a 6 × 10 mm notch for the crown/buttons | 0.8 mm | double-sided; EG25-G on the **bottom side**, nested beside the battery pocket |
| Atlas | 54 × 54 × 13.5 mm | **Sandwich**: 2 boards of 46 × 46 mm + 1.6 mm interposer ring (frame board) | 0.65 mm each | AP/DRAM/UFS/PMIC on the top board; EG25-G, BG95-S5, GNSS and camera connector on the bottom board |

## 2. Layer stack-ups

### Square: 10-layer any-layer HDI (ELIC), 0.8 mm

| Layer | Use | Cu |
|---|---|---|
| L1 | components top (SoC, DRAM, PMIC), fine-pitch escape | 12 µm + plating |
| L2 | GND (reference for L1 RF/high-speed) | 12 µm |
| L3 | high-speed: DSI, USB, UFS, LPDDR5 byte lanes | 12 µm |
| L4 | GND | 12 µm |
| L5 | power: VSYS, VPROC, VCORE/VNPU (wide pours) | 18 µm |
| L6 | power: VDDQ, VIO18, VBAT_LTE | 18 µm |
| L7 | GND | 12 µm |
| L8 | signals: UART, I2C, SPI, GPIO, LPDDR CA | 12 µm |
| L9 | GND (RF reference) | 12 µm |
| L10 | components bottom (EG25-G, LC29H, FEM, tuner), RF CPW-G | 12 µm + plating |

Construction and RF rules:
- Stacked laser microvias (any-layer).
- Min line/space 40/40 µm, 0.3 mm via-in-pad under the 0.35/0.4 mm-pitch SoC BGA.
- Materials: low-loss (Df ≈ 0.008) on L1–L3; standard mid-Tg FR-4 core; ENEPIG finish.
- Controlled impedance: 50 Ω single-ended RF (CPW-G on L10 referenced to L9), 90 Ω USB, 100 Ω DSI/UFS, LPDDR5 40 Ω / 80 Ω per reference design.
- Via-fence every λ/20 along RF traces.

### Pebble: 8-layer HDI 2+4+2, 0.8 mm

Same principles. LPDDR5 x32 can escape with 2+N+2, but any-layer is preferred if the Genio 520 package pitch is 0.35 mm (verify).

### Atlas: 2 × 10-layer any-layer + interposer

Interposer: 0.4 mm pitch, ~180 pins. It carries the CSI-2, USB, UART and power nets. A mature process (iPhone-class), but expect about 2–3 % lower SMT yield and a cost premium (in the BOM).

## 3. Z-stack (Square, 12.0 mm budget)

| Item | Thickness (mm) |
|---|---|
| Cover glass (0.55) + OCA (0.10) | 0.65 |
| AMOLED module incl. on-cell touch + foam/Cu backing | 0.95 |
| Air gap + mid-frame SUS 0.2 + graphite | 0.45 |
| PCB top components (SoC + DRAM ≈ 1.0) + shield can | 1.10 |
| PCB | 0.80 |
| Bottom components: **EG25-G 2.4 nested beside the battery** (battery pocket is 32 mm wide, beside the 29 mm module) | (0 in stack) |
| Battery (swell allowance 8 %) | 4.00 + 0.30 |
| Back cover PC+GF incl. pogo bosses | 1.10 |
| Al frame top lip + bottom chamfer, tolerances | 2.65 |
| **Total** | **12.0** |

Nesting the module side-by-side with the battery is the critical layout decision: the 48 × 48 board area is shared between a 29 × 32 module zone and a 46 × 40 battery outline that partially overlaps the board footprint. This needs a cut-out ("L-shaped") battery or a smaller cell.

**Open issue for ID co-design at EVT:** if the battery has to become L-shaped (~950 mAh), Square battery life drops about 14 %. This is why ECR-05 (Cat-1bis, ~18 × 16 mm module) is valuable.

## 4. Keep-outs

- **GNSS LDS:** top edge, 3 mm clearance to metal and display ground, with no DC-DC within 10 mm.
- **LTE main:** top frame slot plus the NMT break. Feed and tuner within 5 mm of the slot.
- **Magnetometer:** at least 15 mm from the speaker, LRA, pogo magnets and battery tabs. Place the BMM350 in the corner diagonal to the speaker.
- **Mic ports:** top and bottom edges, 22 mm apart; ePTFE vents (IP67).
- **Thermal:** SoC under the display centre, with a graphite + Cu foil spreader to the Al frame. Keep the battery ≥ 3 mm from the SoC hotspot, with an insulating layer between them.
