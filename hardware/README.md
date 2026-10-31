# LORE Labs: Hardware Engineering

Owner: Head of Hardware Engineering. Status: architecture v0.9, pre-EVT (2026-10-31).

This folder holds the electronics architecture, component selection, costed BOMs, reference schematics, power/RF/thermal/fusion simulations, certification plan, and manufacturing plan for **LORE Pebble, Square and Atlas**. COMPANY.md is the requirements baseline. Deviations are raised as ECRs in `system-architecture.md` §8.

Two marking conventions apply throughout:
- **(E)** = engineering estimate.
- **SIMULATED** = model output, not measured data.

## Index

| Path | Contents |
|---|---|
| [system-architecture.md](system-architecture.md) | Requirements traceability, SoC trade study, per-SKU architecture, interfaces, power tree, memory sizing, battery, ECRs, risks |
| [block-diagrams/](block-diagrams/) | `gen_block_diagrams.py` → `pebble/square/atlas_block_diagram.svg/.png` |
| [bom/](bom/) | `build_bom.py` → `bom_<sku>.csv`, `BOM.md` (line items + landed-COGS roll-up), `cogs_summary.csv/json`, `cogs_summary.png`, `cogs_vs_volume.png`, `dram_sensitivity.json` |
| [schematics/](schematics/) | `gen_schematics.py` → Square reference sheets 01–06 (power tree, GNSS + matching, sensor bus, audio, LTE + eSIM + Wi-Fi/BT, display/UI/haptics/SE); [pinmap.md](schematics/pinmap.md); [pcb-stackup.md](schematics/pcb-stackup.md) |
| [simulations/](simulations/) | `power_budget.py`, `heading_fusion.py`, `thermal.py`, `rf_link_budget.py`, PNG charts, JSON results, **[results.md](simulations/results.md)** |
| [certification.md](certification.md) | FCC/ISED, CE-RED (incl. EN 18031), UKCA, MIC/JATE, India WPC/BIS/TEC, PTCRB/GCF/carriers, BT SIG, Skylo, battery, RoHS/REACH/WEEE, SAR: costs and timeline |
| [dfm-manufacturing.md](dfm-manufacturing.md) | ODM/EMS strategy, EVT/DVT/PVT dates and quantities, test fixtures, yields, tooling, MOQ/lead times, supply-chain risk register |
| [firmware-interfaces.md](firmware-interfaces.md) | Hub/AP partitioning, protocol, driver list, power and thermal requirements, factory hooks, OTA/security |

Regenerate everything with:

```
pip install numpy matplotlib schemdraw cairosvg
cd bom && python3 build_bom.py
cd ../simulations && python3 power_budget.py && python3 heading_fusion.py && python3 thermal.py && python3 rf_link_budget.py
cd ../block-diagrams && python3 gen_block_diagrams.py
cd ../schematics && python3 gen_schematics.py
```

## Architecture summary

| | **Pebble** ($149) | **Square** ($299) | **Atlas** ($549) |
|---|---|---|---|
| AP SoC | **MediaTek Genio 520 (MT8371)**, 10 TOPS | **MediaTek Genio 720 (MT8391)**, 10 TOPS | **MediaTek Genio 720 (MT8391)** |
| RAM / storage | 4 GB LPDDR5 / 32 GB eMMC | 6 GB LPDDR5 / 64 GB UFS | 8 GB LPDDR5 / 128 GB UFS |
| On-device model | ~1B INT4 (~24 tok/s E) | 3B INT4 (~9 tok/s burst E) | 3–4B INT4 + VLM |
| Always-on hub | nRF54L15 + BHI360 / BMM350 / BMP390 | same | same |
| GNSS | Quectel LC29HAA L1+L5 | same | same |
| Cellular | – (BLE via phone) | Quectel EG25-G Cat-4 global + Infineon OC1230 eUICC | + Quectel BG95-S5 NTN (Skylo) |
| Wi-Fi / BT | Wi-Fi 6 + BT 5.4 dual-mode (A2DP + LE Audio/Auracast) | same | same |
| Display / camera | LED ring | 1.6" 466×466 AMOLED | AMOLED + sapphire, OV13B10 13 MP Glance |
| Battery | 650 mAh / 2.52 Wh | 1100 mAh / 4.27 Wh | 1450 mAh / 5.63 Wh |
| Body | PC+GF, 42×42×14 | Al 6013 + NMT, 54×54×12 | Ti Gr.5 + ceramic back, 54×54×13.5 (ECR-02) |

The Genio 520 and 720 are pin-compatible, which gives one BSP and one NPU toolchain. Alternates are QCS6490/QCM6490 (Square/Atlas) and RK3576 (Pebble).

## Headline results

**Landed COGS @10k units** (USD, VN/MY final assembly, 0 % duty assumed; `bom/BOM.md`):

| SKU | Landed ex-NRE | Landed incl. cert + tooling amortised over 10k | Gross margin at target price, incl. NRE | China-FATP tariff scenario |
|---|---|---|---|---|
| Pebble | $126 | **$157** | −5 % | $182 |
| Square | $227 | **$299** | 0 % | $343 |
| Atlas | $316 | **$413** | 25 % | $475 |
| Pebble Lite (ECR-01) | $63 | $90 | 39 % | $103 |

At 100k units, landed COGS incl. NRE falls to $105 / $190 / $263. Memory is the most volatile line: at a normalised $3/GB, Square ex-NRE would be about $206.

**Battery** (SIMULATED travel day: 6 h narration walk + 20 min cloud chat + 40 LLM answers, optimised firmware):

| SKU | Days (new cell) | Days (aged) | Target |
|---|---|---|---|
| Pebble | 2.1 | 1.7 | 1.5 |
| Square | 2.1 | 1.7 | 2 |
| Atlas | 2.4 | 2.0 | 3, **missed** |

With baseline (non-optimised) firmware the figures are 1.2 / 1.35 / 1.65 days.

**Map Vision** (SIMULATED): left/right accuracy is 99.9 % with EKF + map-matching + L1/L5, versus 98.1 % for an idealised raw compass. The EKF alone reaches 98.9 %. L1+L5 adds 3–7 points over L1-only for every non-map-matched method.

**Thermal**: in a 54 mm Al body the sustainable power is about 2.2 W (open air, 25 °C), so on-device LLM must be bursty. Sustained 3B decode is about 4.5 tok/s.

## Top risks

1. **Unit economics.** At 10k units with 2026 DRAM prices, Square and Pebble have no hardware margin once NRE is included. Options are ECR-01 (Pebble Lite), ECR-04 (price/cost-down), and DRAM buy-ahead.
2. **DRAM shortage and tariffs.**
3. **Battery targets** depend on firmware power work. The Atlas misses 3 days.
4. **EG25-G area and antennas in metal bodies.** Cell range is about 0.72–0.77× a phone (E). OTA chamber work is needed from EVT.
5. **Certification critical path.** Carrier acceptance and India are the longest items; total certification is about $485k (Square) and $640k (Atlas).
6. **Genio BSP maturity.**

## Sources

Key sources are cited inline in each document and listed in `bom/BOM.md` (Sources). Web prices were captured 2026-10-30/31 and change frequently. Every (E) value must be replaced with RFQ or bench data at EVT.
