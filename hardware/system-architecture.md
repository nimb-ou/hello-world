# LORE System Architecture (Hardware): Pebble, Square, Atlas

Owner: Head of Hardware Engineering. Status: pre-EVT architecture freeze candidate, v0.9 (2026-10-31).

Conventions:
- **(E)** marks an engineering estimate.
- **(D)** marks a figure taken from a datasheet or distributor listing.
- **"verify"** marks an item to confirm under NDA or by RFQ.

COMPANY.md is the requirement baseline. Where this document recommends a deviation, it is flagged as an **ECR** (engineering change request) for the founder to decide.

---

## 1. Requirements traceability (from COMPANY.md)

| Requirement | Pebble | Square | Atlas | Hardware implication |
|---|---|---|---|---|
| Size | 42×42×14 | 54×54×12 | same footprint; **13.5 mm proposed** | Atlas needs a stacked PCB, camera, NTN module and a bigger cell, so a 1.5 mm thicker body is proposed (ECR-02) |
| Display | none, LED ring | 1.6" AMOLED 466×466 | same + sapphire | MIPI-DSI 1-lane / QSPI DDIC, ~90 mW active |
| Connectivity | BLE to phone + Wi-Fi | LTE Cat-4 global eSIM + Wi-Fi + BT 5.4 LE Audio | + satellite SOS (NTN) | Quectel EG25-G + Infineon OC1230 eUICC; Quectel BG95-S5 on Atlas |
| On-device AI | ~1B | 3B | 3–4B + vision | 4 / 6 / 8 GB LPDDR5; 10 TOPS NPU |
| Map Vision | L1+L5 GNSS, 9-axis IMU + compass, step detection | same | same | LC29HAA + BHI360 + BMM350 + BMP390 on an always-on hub |
| Battery | 1.5 days | 2 days | 3 days | 2.52 / 4.27 / 5.63 Wh. Simulated: 2.1 / 2.1 / 2.4 days (see §7) |
| Controls | press = talk, 2× = around me, long = SOS | + crown | + crown | SOS works even if the AP has crashed, because it is routed through the always-on hub |
| Audio | your own earphones (LE Audio + Classic A2DP) + small speaker | same | same | Needs a **dual-mode** BT source. This rules out BLE-only Nordic parts as the audio radio |

---

## 2. SoC selection

### 2.1 What the AI requirement actually demands

On-device LLM decode is **memory-bandwidth-bound**: each generated token streams the entire weight set from DRAM.

| Model | INT4 weights | Runtime RAM (weights + 4k KV + ASR + TTS) | Decode upper bound at 25.6 GB/s × 60 % |
|---|---|---|---|
| 1B (Llama-3.2-1B / Qwen3-1.7B-class) | ~0.65 GB | ~1.3 GB | ~24 tok/s |
| 3B (Llama-3.2-3B / Qwen-class) | ~1.75 GB | ~2.6 GB | ~9 tok/s |
| 4B + small VLM | ~2.3 GB + 0.4 GB | ~3.4 GB | ~7 tok/s |

Add an OS footprint on top:
- Yocto/Linux: ~0.4–0.6 GB.
- AOSP without GMS: ~1.8–2.5 GB.

That leads to **4 GB (Pebble), 6 GB (Square, Linux or slim AOSP), and 8 GB (Atlas)**. NPU TOPS mostly matters for prefill, ASR, and vision. Any NPU at or above 6 TOPS with transformer support is adequate, so **DRAM bandwidth and power** are the real discriminators.

### 2.2 Candidate evaluation

| Candidate | Node / CPU | NPU | DRAM | OS support | Longevity | Price (E) | Power fit for wearables | Verdict |
|---|---|---|---|---|---|---|---|---|
| **MediaTek Genio 720 (MT8391)** | 6 nm, 2×A78 + 6×A55 | **10 TOPS**, 8th-gen, transformer-native [(MediaTek)](https://www.mediatek.com/press-room/mediatek-unveils-genio-720-and-genio-520-iot-platforms-for-generative-ai-applications) | LPDDR5-6400, up to 16 GB | Android, Yocto, Ubuntu (Yocto/Ubuntu on the roadmap for 520 per [MediaTek FAQ](https://genio.mediatek.com/genio-520)) | to 2035 [(MediaTek longevity)](https://www.mediatek.com/iot-longevity) | $27–36 (E) | Good: phone-derived 6 nm, low suspend power | **Chosen: Square, Atlas** |
| **MediaTek Genio 520 (MT8371)** | 6 nm, same CPU cluster at lower clocks | 10 TOPS (same NPU/memory subsystem as 720) | LPDDR5 | Android at launch; Yocto roadmap | to 2035 | $18.5–27 (E) | Good | **Chosen: Pebble** (pin-compatible with 720 → one BSP, one NeuroPilot toolchain) |
| Qualcomm QCM6490 / QCS6490 | 6 nm, Kryo 670 | 12 TOPS [(Qualcomm brief)](https://docs.qualcomm.com/doc/87-28733-1/87-28733-1_REV_F_QUALCOMM_QCS6490_QCM6490_Processors_Product_Brief.pdf) | LPDDR5 2×16 @3200 MHz, up to 16 GB | Android, Qualcomm Linux, Ubuntu; mainline device trees (Fairphone 5) | to July 2036 [(Qualcomm PLP)](https://www.qualcomm.com/products/product-longevity-program) | $45–60 (E) + 3 PMICs + WCN6750 | Good | **Strong alternate.** QCM6490 integrates a 5G/LTE modem, which saves the $26 module, but chip-down cellular adds RFFE design, 5G SEP royalties, and full PTCRB/GCF on our own RF. Revisit for Square v2 cost-down |
| Rockchip RK3576 | 8 nm, 4×A72 + 4×A53 | 6 TOPS, RKLLM toolkit | LPDDR4X/5, **32-bit** bus | Linux (mature), Android 14 | – | ~$15–20 (E) | Fair: A72 + 8 nm burns more | **Pebble fallback** if the Genio 520 Yocto BSP slips; LLM decode ≈ half of RK3588 per [CNX](https://www.cnx-software.com/2024/07/15/rockchip-rkllm-toolkit-npu-accelerated-large-language-models-rk3588-rk3588s-rk3576/) |
| Rockchip RK3588S | 8 nm, 4×A76 + 4×A55 | 6 TOPS | 64-bit LPDDR4X/5 | Linux, Android | – | ~$30–40 (E) | **Poor**: 8–15 W board-level figures reported | Rejected (thermal/power) |
| NXP i.MX 95 | 16 nm, 6×A55 | ~2 TOPS eIQ Neutron [(Ezurio)](https://www.ezurio.com/support/faqs/what-is-the-npu-performance-on-the-nitrogen95-and-how-does-it-support-edge-ai-inference-workloads) | LPDDR5/4X | Linux (excellent) | 15 yrs | $35+ (E) | OK, but weak AI | Rejected: too little AI per watt for 3B |
| nRF5340 / nRF54 + Ambiq / ESP32-S3 | MCU | none / micro-NPU | SRAM, PSRAM ≤ 32 MB | Zephyr / FreeRTOS | – | $3–6 | Excellent | Cannot run a 1B LLM. Basis for the **Pebble Lite ECR** (§8) |
| Unisoc W517 / Snapdragon W5 Gen 2 (watch SoCs) | 12/4 nm, 4×A53/A55 | none / weak | 2 GB-class | Wear OS / RTOS | – | $15–25 | Excellent; W5 Gen 2 has integrated LTE + NB-NTN ([Skylo](https://www.skylo.tech/newsroom/google-and-skylo-expand-satellite-connectivity-to-pixel-10-series-and-unveil-pixel-watch-4)) | Rejected for v1 because it cannot hold a 3B model. The W5 Gen 2 is interesting for a future "Atlas Lite" |

**Why Genio over QCM6490 for v1.**
- **Pin-compatible 520/720** means one schematic family, one BSP, and one NPU toolchain across all three SKUs. That matters for a small software team.
- The modular LTE approach avoids chip-down RF certification in v1.
- Cost is lower.

**Risks.**
- Genio 520/720 are young (sampling Q2 2025). Yocto support for the 520 was "roadmap" at launch, which is the reason AOSP is the fallback OS.
- MediaTek NeuroPilot LLM tooling is less public than Qualcomm Genie. Mitigation: keep a QCS6490 SOM-based "B-plan" dev kit in the lab through EVT.

### 2.3 Always-on companion MCU (all SKUs): Nordic nRF54L15

Role:
- Sensor hub: owns the BHI360, BMM350 and BMP390 while the AP sleeps.
- Buttons, crown, LED ring and haptics.
- The **SOS path that works with the AP crashed or asleep**.
- AP power sequencing (PWRKEY).
- A BLE "find my device" beacon.

It costs about 3 µA in system-off and about 1 mW in walking-fusion mode. Alternate: Ambiq Apollo4 Lite.

---

## 3. Per-SKU architecture

Block diagrams: `block-diagrams/{pebble,square,atlas}_block_diagram.svg|png`.

### 3.1 LORE Pebble (42×42×14 mm, $149)

| Function | Part | Notes |
|---|---|---|
| AP | MediaTek Genio 520 + 4 GB LPDDR5 + 32 GB eMMC | 1B INT4 LLM, on-device ASR (Whisper-base-class) and TTS. AP suspended about 85 % of walking time |
| Hub | Nordic nRF54L15 | always-on |
| Wi-Fi/BT | MediaTek MT79xx Wi-Fi 6 + BT 5.4 dual-mode combo (exact part per Genio reference design; LE Audio source support **verify**) | A2DP source to classic earbuds, LE Audio unicast/Auracast, BLE GATT to the phone app |
| GNSS | Quectel LC29HAA L1+L5, 12.2×16×2.5 mm, 24 mA tracking [(D)](https://quectel.com/content/uploads/sites/3/2022/06/Quectel_LC29H_GNSS_Specification_V1.2.pdf) | Alternate u-blox NEO-F10N (~21 mA @ 3.0 V) |
| IMU | Bosch BHI360 (6-axis + programmable fusion core, PDR/step on-chip) ~$4.62 @5k [(D)](https://futureelectronics.com/resources/featured-products/bosch-sensortec-bmm350-magnometer-bhi360-imu-based-sensor-system) | Alternate TDK ICM-45686 (~$4.37 @1k [(D)](https://www.xonelec.com/mpn/tdk/icm45686)) + host fusion |
| Magnetometer | Bosch BMM350 on the BHI360 aux bus | Alternate MEMSIC MMC5983MA |
| Barometer | Bosch BMP390 | "look up" / floor / altitude aid |
| Audio | 2× Infineon IM73D122 PDM mics, TI TAS2563 smart amp, 13×9 mm speaker | Speaker is a fallback only |
| UI | TI LP5024 + 8 RGB LEDs + light-guide ring; main button + volume rocker; DRV2605L + X-axis LRA | |
| Power | 650 mAh / 2.52 Wh Li-ion (4.45 V HV); ADI MAX77654 SIMO PMIC/charger for hub rails; Genio PMIC for AP rails; MAX17262 fuel gauge; USB-C + 4-pin magnetic pogo | |
| Security | NXP SE050E (device identity, attestation, theft-lock keys) + Genio TrustZone/OP-TEE | |
| Enclosure | PC + 30 % GF soft-touch, IP67 target, detachable clip | |

### 3.2 LORE Square (54×54×12 mm, $299)

| Function | Part | Notes |
|---|---|---|
| AP | **MediaTek Genio 720 (MT8391)** + 6 GB LPDDR5-6400 + 64 GB UFS 2.2 | 3B INT4 resident. 6 GB assumes Yocto or slim AOSP without GMS. Choose 8 GB if the software team picks full AOSP |
| LTE | **Quectel EG25-G** Cat-4 global (B1/2/3/4/5/7/8/12/13/18/19/20/25/26/28/38/39/40/41), LGA 29×32×2.4 mm; ~€45 @250 at SOS [(D)](https://www.soselectronic.com/en-us/products/quectel/eg25ggb-256-sgns-308062) | Pre-certified (FCC/CE/PTCRB/GCF at module level), which cuts certification cost and risk. Its size is the main area problem on a 48 mm board |
| eSIM | **Infineon OPTIGA Connect Consumer OC1230**: GSMA SGP.22 consumer eUICC, WLCSP 1.8×1.6×0.4 mm [(Infineon)](https://infineon.com/cms/en/product/security-smart-card-solutions/optiga-embedded-security-solutions/optiga-connect/oc1230/) | The ST ST4SIM-200M is SGP.02 M2M ([ST](https://www.st.com/en/secure-mcus/st4sim-200m.html)), so it is wrong for consumer RSP and rejected. Thales/Kigen eUICC is the alternate |
| Wi-Fi/BT | MediaTek MT79xx combo (as Pebble) + FEM | LE Audio + Auracast + A2DP |
| GNSS / sensors | LC29HAA, BHI360, BMM350, BMP390 | same as Pebble |
| Display | 1.6" AMOLED, 466×466 (~412 ppi on a 28.7 mm square active area), on-cell touch, CO5300 / RM690B0-class DDIC, MIPI-DSI 1-lane (QSPI fallback), AOD, 1000-nit HBM | 466×466 panels exist at 1.43" ($7.8–13 at Tailorpixels, [(D)](https://tailorpixels.com/?p=26783)) and 1.75". **A 1.60" square-ish cut is semi-custom** (Visionox/BOE/Tianma): NRE about $40–80k (E), included in tooling. EVT uses the 1.43" standard panel |
| Cover | 0.55 mm 2.5D aluminosilicate, AR+AF | |
| Controls | Crown with PixArt PAT9125EL optical rotation sensing + push; side button; SOS button; DRV2605L + LRA | |
| Audio | 2 mics, TAS2563, 15×11 mm speaker | |
| Power | 1100 mAh / 4.27 Wh Si-C anode cell, 4.0×46×40 mm (≈ 580 Wh/L; **E, cell-vendor confirm**); TI BQ25620 buck charger; TPS63810 3.8 V/2 A LTE rail; MAX17262 | |
| Body | 6013-T6 Al CNC unibody, NMT antenna breaks, anodised Ink/Sand; RF-transparent PC+GF back with pogo; IP67 | |

### 3.3 LORE Atlas (54×54×13.5 mm proposed, $549)

Everything in the Square, plus:

| Function | Part | Notes |
|---|---|---|
| AP memory | 8 GB LPDDR5 + 128 GB UFS 3.1 | 3–4B LLM + small VLM resident |
| Satellite SOS | **Quectel BG95-S5**: 3GPP Rel-17 IoT-NTN (S- and L-band), **Skylo-certified** (Jan 2025), plus LTE-M/NB-IoT fallback and GNSS; 23.6×19.9×2.2 mm [(Quectel)](https://www.quectel.com/news-and-pr/ces-2025-satellite-communication-module-bg95-s5-skylo-certification/) | No smartphone-grade Cat-4 + NTN module was found on the open market. Two-module design: EG25-G for broadband, BG95-S5 for SOS. Precedent: Pixel Watch 4 NB-NTN on Skylo |
| Camera | **OmniVision OV13B10** 13 MP 1/3", 1.12 µm, fixed-focus wide module 6.4×7.2 mm [(OVT)](https://www.ovt.com/wp-content/uploads/2023/05/OV13B-PB-v1.2-WEB.pdf), MIPI CSI-2 4-lane; ~100° DFOV custom lens; privacy LED hard-wired to sensor power | Alternate OV08B10 8 MP (5.1×6.5 mm FF module) |
| Body | Ti-6Al-4V (Gr.5) CNC, bead-blast or black DLC; sapphire 0.7 mm cover; zirconia ceramic back (RF window); brass-tone PVD crown ring | |
| Battery | 1450 mAh / 5.63 Wh, 5.2×46×40 mm | Simulated 2.44 days, below the 3-day target. See ECR-03 |
| Thermal | 0.4 mm vapour chamber + Cu spreader | Ti in-plane conductivity is only ~7 W/m·K |
| PCB | Stacked "sandwich" board: 2× 10-layer any-layer HDI with interposer | |

---

## 4. Interfaces summary (Square; Atlas adds CSI-2 + NTN UART)

| Bus | Master | Slaves / function |
|---|---|---|
| LPDDR5 x32 | SoC | DRAM |
| UFS 2.2 / eMMC | SoC | storage |
| USB2 HS port 1 | SoC | EG25-G (QMI/MBIM data) |
| UART3 (1.8 V) | SoC | EG25-G AT/control, RI wake |
| PCIe or SDIO + UART + PCM | SoC | Wi-Fi/BT combo |
| UART2 + PPS | SoC (or hub) | LC29HAA NMEA/binary, 1PPS timestamp |
| UART1 1 Mbps + AP_WAKE/HUB_IRQ | SoC ↔ nRF54L15 | sensor batches, key events, power control |
| SPI 20 MHz | nRF54L15 | BHI360 (aux master → BMM350) |
| I2C (hub TWIM21) | nRF54L15 | BMP390, MAX17262, DRV2605L, PAT9125, BQ25620 (shared I2C0 alt.) |
| I2C1 / I2S1 (TDM) | SoC | TAS2563 control + audio + IV-sense echo reference |
| PDM | SoC | 2 mics |
| MIPI-DSI 1-lane + I2C2 | SoC | AMOLED + touch |
| I2C3 (secure world) | SoC | SE050E |
| USIM | EG25-G | OC1230 eUICC |
| SPMI | SoC | companion PMIC |

The full pin map is in `schematics/pinmap.md`.

---

## 5. Power architecture

```
USB-C 5 V (sink, Rd) ─┐
                      ├─ideal-diode OR─► BQ25620 buck charger ──► VSYS 3.4–4.45 V ──┬─► Genio PMIC (VPROC_B/L, VCORE/VNPU, VDD2H/VDDQ, VIO18, VUFS, VAUD)
Pogo 5 V (dock/puck) ─┘                        │                                  ├─► TPS63810 → VBAT_LTE 3.8 V / 2 A (EG25-G)  [BG95-S5 on Atlas]
                                         BAT ◄─┘ (Li-ion 4.45 V HV, NTC, PCM)      ├─► load switches: 3V3_GNSS, 1V8_SNS (AON), MIC, SPK, display VCI/VBAT
                                         MAX17262 fuel gauge                      └─► nRF54L15 (always on; ~3 µA off / ~1 mW walking)
```

Ship mode is entered at EOL. Wake is by the SOS key through the charger's QON pin.

Charging rates:
- Pebble: 1C (0.65 A), about 75 min to 80 %.
- Square / Atlas: 1C (1.1 / 1.45 A), about 60 min to 80 %.
- JEITA-compliant: 0–10 °C at 0.5C, no charge above 45 °C.

---

## 6. Memory, storage, and City Pack sizing

| Item | Size (E) |
|---|---|
| Rome City Pack: vector map + building footprints/entrances + routing graph + ~3,000 stories (text) + POI DB | 300–600 MB |
| Pre-rendered story audio (optional, Opus 24 kbps, 30 s each) | ~90 MB per 1,000 stories |
| Models: 1B INT4 / 3B INT4 / 4B INT4 + VLM | 0.65 / 1.75 / 2.7 GB |
| ASR + TTS + wake/VAD | ~0.3 GB |
| OS (Yocto / AOSP) | 2 / 6 GB |

Storage choice: 32 GB on Pebble (3 packs), 64 GB on Square (10+ packs), 128 GB on Atlas (20 packs + photos).

---

## 7. Battery sizing (see `simulations/results.md`)

| SKU | Cell | Target | Simulated (optimised FW, new) | Aged (80 %) | Status |
|---|---|---|---|---|---|
| Pebble | 650 mAh / 2.52 Wh | 1.5 d | 2.13 d | 1.71 d | OK with firmware power work |
| Square | 1100 mAh / 4.27 Wh | 2 d | 2.07 d | 1.66 d | Marginal |
| Atlas | 1450 mAh / 5.63 Wh | 3 d | 2.44 d | 1.95 d | **Gap** |

Without the firmware optimisations (GNSS duty-cycling with PDR, AP suspend between stories, LC3), every SKU misses its target by 20–45 %.

---

## 8. Engineering change requests (for the founder)

| ECR | Proposal | Why | Impact |
|---|---|---|---|
| **ECR-01 Pebble Lite** | Replace the Linux AP with a dual-mode BT audio SoC (Airoha/BES/Realtek class) + nRF54L15. The ~1B model runs **on the user's phone** in the LORE app, and offline stories are cached on 64 MB NOR | At $149 the COMPANY.md Pebble (Genio 520 + 4 GB DRAM under a DRAM shortage) costs **$126 landed ex-NRE @10k**, i.e. negative-to-15 % margin | Pebble Lite: **$63 landed ex-NRE @10k**, ~3+ day battery, lower thermal risk. Loses standalone on-device AI without a phone |
| **ECR-02 Atlas thickness** | 13.5 mm instead of the Square's 12 mm | stacked PCB + NTN module + camera + bigger cell | ID |
| **ECR-03 Atlas battery claim** | Either go to 14.5 mm with an ~1,800 mAh cell, or define "3 days" at 4 h walking/day | the 2.44-day simulation misses 3 days | Marketing / ID |
| **ECR-04 Price/COGS** | Square at $299 has **~24 % hardware GM ex-NRE** at 10k under 2026 DRAM pricing. Consider $349, or reach v2 cost-down via chip-down LTE (QCM6490) and 6 GB → 4 GB with cloud-first 3B | see `bom/BOM.md` | Finance |
| ECR-05 LTE category | Evaluate LTE Cat-1bis (e.g. Quectel EG800Q-class, ~18×16 mm, ~1/3 the cost) instead of Cat-4. LORE traffic is voice, text, and small audio; packs download on Wi-Fi | board area and power | COMPANY.md specifies Cat-4, so this is a founder decision. Note the Qualcomm IoT licence excludes Cat-1bis from its program scope ([Qualcomm](https://www.qualcomm.com/licensing/cellular-iot-licensing-program)) |

---

## 9. Key technical risks

1. **DRAM pricing.** TrendForce reported LPDDR5X contract prices up 78–83 % QoQ in 2Q26 after about 90 % in 1Q26 ([TrendForce](https://www.trendforce.com/presscenter/news/20260514-13044.html)). Memory is 20–25 % of every BOM.
2. **EG25-G area** (29×32 mm) on a ~48 mm board. It forces double-sided placement with the module on the bottom side under the battery. Mitigations: Cat-1bis (ECR-05) or chip-down v2.
3. **Battery targets.** These depend on firmware power discipline (above).
4. **Antenna performance in metal bodies.** Cell range is estimated at about 0.72–0.77× a phone. Early OTA chamber work is needed at EVT.
5. **Genio BSP maturity** (Yocto on the 520) and LLM tooling. Hedge: RK3576 (Pebble) or QCS6490 (Square/Atlas).
6. **Semi-custom 1.60" AMOLED.** MOQ and NRE risk; the 1.43" standard panel is the fallback.
7. **Cellular SEP royalties** and tariffs. See BOM assumptions and `dfm-manufacturing.md`.
