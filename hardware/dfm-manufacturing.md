# DFM and Manufacturing Plan

The manufacturing partner landscape below is described by **type** only. LORE has no relationships, quotes or NDAs in place yet. Costs are **estimates to be verified** by RFQ.

## 1. ODM / EMS strategy

| Option | Who (type) | Pros | Cons | Fit |
|---|---|---|---|---|
| **A. JDM/ODM for wearables** (Shenzhen/Dongguan/Huizhou; smartwatch, kids-watch and earbud ODMs; typically 5–30k units/month lines with in-house RF/SAR labs) | wearable ODM with LTE-watch experience | own LTE/antenna/SAR know-how, fast EVT, existing CNC/NMT supply base | IP-sharing terms; "their" BSP habits; minimum volumes ~10k/yr | **Recommended for Square/Atlas** |
| B. Tier-2 EMS + LORE-owned design (Shenzhen/Suzhou EMS 50–500 staff; or VN/MY sites of the same groups) | EMS with consumer-electronics FATP | LORE owns all design files; clean IP; easy to dual-source | LORE must staff RF, mechanical, test and NPI (~4–6 extra FTE) | **Recommended for Pebble** (simpler RF) |
| C. Tier-1 EMS (multinational) | – | best process control, VN/MY/MX footprint for tariffs | MOQ and engagement minimums too high for 5k first-year volume | Later (2028+, >100k/yr) |

**Plan:**
- Run an RFQ to 4 ODMs and 3 EMSs in Dec 2026 and select by Jan 2027.
- Design files (schematic, layout, mechanical CAD, test specs) remain **LORE property** by contract.
- Escrow the ODM's firmware build scripts.
- Final assembly (FATP) in **Vietnam or Malaysia** from PVT. The China-FATP tariff scenario adds about $44 to Square landed cost (see the BOM). EVT/DVT is built in Shenzhen for speed.

## 2. Build plan (EVT / DVT / PVT)

| Phase | Dates | Units (P / S / A) | Purpose | Exit criteria |
|---|---|---|---|---|
| Proto (dev boards) | Nov 2026 – Jan 2027 | 10 / 10 / 5 rigs | Genio 520/720 EVK + sensor/radio daughterboards + 3D-printed shells; firmware bring-up; Rome field tests | Map Vision ≥ 95 % left/right on a recorded Rome dataset; power numbers within 20 % of the sim |
| **EVT** | PCB tape-out Jan 2027; build **Mar 2027** | 15 / 25 / 10 (**50 total**, per COMPANY.md) | form-fit, all circuits, first antennas, pre-scans, beta testers | all functions working; OTA TRP/TIS within 3 dB of target; no Sev-1 HW bugs |
| **DVT** | build **Jun 2027** (2 builds: DVT1 Jun, DVT2 Jul) | 150 / 300 / 120 | final tooling T1/T2, reliability (drop 1.5 m ×26, IP67, 85/85, thermal shock, button 200k, crown 100k, cable flex), certification samples, Kickstarter demo units | certifications started; reliability pass; cosmetic spec frozen |
| **PVT** | **Sep 2027** | 500 / 1,000 / 300 | line validation at VN/MY FATP, yield ramp, golden samples, packaging drop test | FPY ≥ 92 %, CpK ≥ 1.33 on critical dims, all certs granted |
| MP ramp | **Oct–Dec 2027** | 5,000 first-ship (Kickstarter mix, E: 1.5k / 2.5k / 1k) | | |

## 3. Test strategy and fixtures

| Station | What | Fixture cost (E) |
|---|---|---|
| SMT AOI + 3D SPI + X-ray (BGA/LGA voids on SoC, DRAM, EG25-G) | in-line | EMS-owned |
| ICT / boundary-scan + flying probe (EVT/DVT) | shorts/opens, rails | $8k per SKU |
| Board FCT: power rails, PMIC, DRAM stress, UFS, sensors (static IMU/mag/baro), audio loopback, display, buttons | pogo-bed + shielded box | $12k per SKU ×2 |
| RF calibration and verification: LTE (call-box non-signalling, e.g. R&S CMW/Keysight-class), Wi-Fi/BT, GNSS C/N0 with a GNSS simulator | shielded boxes, couplers | $35k (Square/Atlas), $15k (Pebble) + test-set rental |
| **Sensor calibration**: 6-position IMU tumble + magnetometer rotation in a Helmholtz cage (hard/soft iron); barometer offset | motorised gimbal + Helmholtz cage | $20k per line |
| Air-leak test (IP67 proxy, Δp decay) | | $6k |
| Final: OTA radiated sanity check, camera MTF/focus (Atlas), speaker/mic acoustic box, haptics accelerometer, cosmetic check, eSIM bootstrap and key injection (HSM), ship mode | | $15k per SKU |
| Run-in: 2 h LLM thermal soak, 10% sample | racks | $5k |

The fixture totals match the BOM NRE: Pebble $45k, Square $95k, Atlas $120k.

**Yield targets:**

| Stage | DVT | PVT | MP |
|---|---|---|---|
| SMT FPY | 95 % | 97 % | ≥ 98.5 % |
| FATP FPY | 85 % | 92 % | ≥ 96 % |
| Overall | 80 % | 89 % | ≥ 94.5 % |

The BOM models yield loss as 7 % @1k, 3.5 % @10k and 2 % @100k of material plus conversion.

## 4. Tooling (E)

| Item | Pebble | Square | Atlas |
|---|---|---|---|
| Injection moulds (P20/H13 steel, 1+1 or 2-cavity): shells, light guide, keypad, back cover, internal carriers | $55k | $30k | $20k |
| NMT / insert-mould tools for antenna breaks | – | $30k | $35k (ceramic-filled) |
| CNC fixtures + programs (Al 5-axis; **Ti** 5-axis needs ~3× cycle time and carbide tooling consumption ~$1–2/unit) | – | $35k | $70k |
| Anodise / DLC / PVD racking, laser-marking jigs | – | $8k | $15k |
| Display cover glass / sapphire cutting + printing tools | – | $10k | $25k |
| Semi-custom AMOLED NRE (cut / FPC) | – | shared $40k (E; amortised in Square/Atlas) | |
| Crown / button turning tools | $5k | $7k | $10k |
| Battery tooling (custom pouch die) | $5k | $6k | $8k |
| Packaging tooling (die-cut, pulp moulds) | $10k | $10k | $15k |
| Clip / accessory moulds | $20k | $4k | $12k |
| **Total** | **≈ $95k** | **≈ $140k** | **≈ $210k** |

Tooling lead time is 6–8 weeks from T0 to T1. Allow 2 tuning loops (T2/T3) before DVT2.

## 5. MOQ and lead-time risks

| Part | Typical MOQ / lead time (E) | Risk | Mitigation |
|---|---|---|---|
| LPDDR5 / UFS | reel 1–2k; **16–30 weeks** in shortage | **High** | Place a non-cancellable PO for the 2027 build in Q1 2027. Qualify CXMT LPDDR5 as second source (note US-market perception/export-control review) |
| Genio 520/720 | via MediaTek distributor; account approval needed; 12–16 weeks | Medium | Register the design early; get distributor (Richardson/Avnet/WPG) DWR |
| Quectel EG25-G / BG95-S5 / LC29H | 1 tray (~100–250); 8–12 weeks | Low–Medium | 3-month safety stock |
| Semi-custom AMOLED | MOQ 3–5k + NRE; 12–16 weeks | **High** | 1.43" standard panel as fallback; ID allows a bezel change |
| Custom Li-ion cell | MOQ 5–10k; 10–12 weeks + UN38.3 | Medium | Use a vendor's existing cell size with the same footprint for EVT |
| Ti CNC housings | capacity limited; 10 weeks | Medium | Two CNC suppliers by DVT |
| Sapphire | 8–10 weeks | Low | |
| Infineon OC1230 eUICC | via connectivity partner; profile logistics | Medium | Pick the partner early |

## 6. Supply-chain risk register

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| 1 | DRAM shortage drives memory +50–100 % ([TrendForce](https://www.trendforce.com/presscenter/news/20260514-13044.html)) | High | High: about $20–40/unit | Buy-ahead; 6 GB Square; Pebble Lite ECR; DRAM sensitivity in the BOM | HW + Finance |
| 2 | US tariffs on China-assembled electronics (Section 301 survived the Feb 2026 SCOTUS IEEPA ruling; rates in flux) | High | High: ~$20–45/unit | VN/MY FATP from PVT; HTS ruling request | Ops/Legal |
| 3 | Single-source SoC (MediaTek) | Medium | High | Alternate board spins for QCS6490 / RK3576 not funded; keep dev kits only | HW |
| 4 | Cellular SEP royalty demands above the $5–6.5 budget | Medium | Medium | Licence counsel; prefer modules with a licence pass-through where available | Legal |
| 5 | Carrier certification delays the Q4 2027 ship | Medium | High | Wi-Fi/BLE-only fallback firmware; ship Pebble first | HW |
| 6 | Antenna underperformance in metal bodies | Medium | High | CTIA chamber from EVT; aperture tuner; plastic back | RF |
| 7 | ODM IP leakage / clone | Medium | Medium | Ownership clauses, split programming (keys injected only at LORE-controlled HSM), SE050 attestation | Legal/HW |
| 8 | Battery safety incident | Low | Very high | Tier-1 cells only, IEC 62133-2, 100 % OCV/IR screening, pouch swell allowance 8 % | HW |
| 9 | Export control / sanctions (eUICC, crypto, Chinese DRAM) | Low | Medium | ECCN classification (5A992 expected), screening | Legal |
| 10 | Natural disaster or Taiwan Strait disruption (6 nm TSMC for Genio) | Low | Very high | 6 months of SoC buffer at MP | Ops |
