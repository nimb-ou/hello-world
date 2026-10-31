#!/usr/bin/env python3
"""
LORE Labs - Hardware BOM & landed-COGS generator
================================================
Generates, for each SKU (Pebble, Square, Atlas) plus the proposed "Pebble Lite" ECR variant:
  * bom_<sku>.csv          - full line-item BOM with 1k / 10k / 100k unit prices
  * cogs_summary.csv       - landed COGS roll-up per SKU per volume tier
  * BOM.md                 - human-readable tables (regenerated every run)
  * cogs_summary.png       - stacked-bar chart of landed COGS by category @ 10k
  * cogs_vs_volume.png     - landed COGS vs volume for every SKU

PRICING POLICY
--------------
* Every price is USD per finished unit.
* "src" column: D = distributor list price seen (see SOURCES; volume price extrapolated),
  E = engineering estimate (no public price; NDA silicon, custom parts, labour),
  Q = to be replaced by an RFQ quote at EVT.  Treat all E figures as +/-25 %.
* Memory is priced from the 2026 mobile-DRAM shortage (TrendForce, 2Q26 +78-83 % QoQ for
  LPDDR5X) with an assumed partial normalisation by our 2027 build window. This is the single
  most volatile line in every BOM.
* NRE (certification + tooling + fixtures) is amortised over the tier volume, i.e. the
  1k column shows the true cost of a 1k-unit programme. Landed COGS is also reported ex-NRE.
* Duty: base case = final assembly (FATP) in Vietnam/Malaysia, 0 % US MFN duty assumed for
  HTS 8517.62 (data transmission apparatus). China-FATP scenario applies an assumed 20 %
  tariff (Section 301 tiers; unverified, see SOURCES['tariff']).

Run:  python3 build_bom.py
"""
import csv
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
TIERS = ["1k", "10k", "100k"]
TIER_QTY = {"1k": 1_000, "10k": 10_000, "100k": 100_000}

SOURCES = {
    "genio": "https://www.mediatek.com/press-room/mediatek-unveils-genio-720-and-genio-520-iot-platforms-for-generative-ai-applications",
    "genio_long": "https://www.mediatek.com/iot-longevity",
    "dram": "https://www.trendforce.com/presscenter/news/20260514-13044.html",
    "eg25": "https://uk.rs-online.com/web/p/rf-modules/2069157",
    "eg25_sos": "https://www.soselectronic.com/en-us/products/quectel/eg25ggb-256-sgns-308062",
    "bg95s5": "https://www.quectel.com/news-and-pr/ces-2025-satellite-communication-module-bg95-s5-skylo-certification/",
    "lc29h": "https://quectel.com/content/uploads/sites/3/2022/06/Quectel_LC29H_GNSS_Specification_V1.2.pdf",
    "bhi360": "https://www.digikey.fr/en/product-highlight/b/bosch-sensortec/bhi360-programmable-sensor-system",
    "bmm350": "https://www.mouser.in/bosch-bmm350-magnetometer/",
    "icm45686": "https://www.xonelec.com/mpn/tdk/icm45686",
    "oc1230": "https://infineon.com/cms/en/product/security-smart-card-solutions/optiga-embedded-security-solutions/optiga-connect/oc1230/",
    "amoled": "https://tailorpixels.com/?p=26783",
    "max77654": "https://www.digikey.co.uk/en/products/detail/analog-devices-inc-maxim-integrated/MAX77654AENV-T/17882955",
    "ov13b10": "https://www.ovt.com/wp-content/uploads/2023/05/OV13B-PB-v1.2-WEB.pdf",
    "btsig": "https://www.bluetooth.com/fee-schedule/",
    "qcom_iot_lic": "https://www.qualcomm.com/licensing/cellular-iot-licensing-program",
    "sisvel_iot": "https://sisvel.com/insights/cellular-iot-patent-royalties-a-closer-look",
    "tariff": "https://goodhopefreight.com/info/logistics-knowledge/us-additional-tariffs-2026.html",
}

# ---------------------------------------------------------------------------------------------
# Line item helper:  (category, ref, description, mfr, mpn, qty, (p1k, p10k, p100k), src, supplier, alternates)
# prices are per *each*; qty multiplies.
# ---------------------------------------------------------------------------------------------
def L(cat, ref, desc, mfr, mpn, qty, prices, src, supplier, alt=""):
    return dict(cat=cat, ref=ref, desc=desc, mfr=mfr, mpn=mpn, qty=qty,
                p1k=prices[0], p10k=prices[1], p100k=prices[2], src=src, supplier=supplier, alt=alt)


# ---------------------------------------------------------------- common blocks
def sensors_block():
    return [
        L("Sensors", "U20", "6-axis IMU + programmable fusion MCU (BSX, PDR, step/heading)", "Bosch Sensortec", "BHI360", 1,
          (4.70, 3.95, 3.30), "D", "Digi-Key/Future (franchised)", "TDK ICM-45686 + host fusion"),
        L("Sensors", "U21", "3-axis magnetometer, +/-2000 uT, 0.1 uT noise-class, I3C/I2C", "Bosch Sensortec", "BMM350", 1,
          (2.10, 1.65, 1.35), "D", "Mouser/Future", "MEMSIC MMC5983MA"),
        L("Sensors", "U22", "Barometric pressure sensor (floor/look-up, altitude aid)", "Bosch Sensortec", "BMP390", 1,
          (2.40, 1.90, 1.50), "E", "Digi-Key/Future", "Infineon DPS368"),
    ]


def audio_block(speaker="1511"):
    return [
        L("Audio", "MK1-2", "Digital MEMS mic, PDM, 73 dB SNR, IP57 (beamforming pair)", "Infineon", "IM73D122V01", 2,
          (1.15, 0.92, 0.75), "E", "Digi-Key/Avnet", "Knowles SPH0690LM4H-1"),
        L("Audio", "U30", "Smart Class-D speaker amp w/ boost + IV-sense speaker protection, I2S/TDM", "Texas Instruments", "TAS2563YFP", 1,
          (1.60, 1.30, 1.05), "E", "TI direct/Arrow", "Analog Devices MAX98390"),
        L("Audio", "LS1", f"Micro-speaker {speaker} box, 8 ohm 0.5 W, IP67 membrane", "AAC / Goertek", f"SPK-{speaker}-custom", 1,
          (1.00, 0.75, 0.58), "E", "AAC/Goertek RFQ", "Knowles/ Merry"),
    ]


def haptics_block():
    return [
        L("Haptics", "U31", "Haptic driver, LRA auto-resonance, ROM effects", "Texas Instruments", "DRV2605LYZFR", 1,
          (1.10, 0.88, 0.70), "E", "TI direct/Arrow", "Awinic AW86224"),
        L("Haptics", "M1", "X-axis linear resonant actuator 0.8 G, 170 Hz (custom 10x3.5x2.5 mm)", "AAC / Jahwa", "LRA-X1035-custom", 1,
          (1.30, 0.95, 0.75), "E", "AAC RFQ", "Vybronics VG0832012"),
    ]


def power_common(fg="MAX17262", charger=("TI", "BQ25620RYKR", (1.45, 1.15, 0.92))):
    return [
        L("Power", "U41", "Li-ion charger (USB-C 5 V in, I2C, JEITA, ship mode)", charger[0], charger[1], 1,
          charger[2], "E", "TI direct/Arrow", "SGMicro SGM41511 / Southchip SC8551"),
        L("Power", "U42", "Fuel gauge ModelGauge m5 EZ, internal sense, cycle/age tracking", "Analog Devices", fg, 1,
          (1.55, 1.25, 1.00), "E", "ADI/Digi-Key", "TI BQ27427"),
        L("Power", "J1", "USB-C 16-pin mid-mount receptacle, IPX8-gasketed", "Amphenol / Korea Hirose", "USB-C-16P-WP", 1,
          (0.55, 0.42, 0.33), "E", "Amphenol RFQ", "JAE DX07 series"),
        L("Power", "D1-4", "ESD/TVS arrays (USB, buttons, pogo)", "Nexperia / TI", "PESD5V0X1BL / TPD4E05U06", 4,
          (0.08, 0.06, 0.05), "E", "Distribution", ""),
        L("Power", "J2", "4-pin magnetic pogo receiver (dock / power-puck)", "CFE / Lotes", "POGO-4P-1.5mm", 1,
          (0.60, 0.45, 0.35), "E", "Shenzhen pogo vendor RFQ", ""),
    ]


def passives(n_parts, base):
    return [
        L("Passives", "R/C/L", f"Passives (~{n_parts} pcs, 01005/0201/0402 MLCC, R, ferrite, inductors)", "Murata/Samsung EM/Yageo", "various", 1,
          base, "E", "Distribution", ""),
        L("Passives", "Y1-3", "Crystals / TCXO (32.768 kHz, 26 MHz SoC, 38.4 MHz radio)", "Epson / NDK / TXC", "various", 1,
          (0.70, 0.55, 0.45), "E", "Distribution", ""),
    ]


# ---------------------------------------------------------------- SKUs
def bom_pebble():
    b = [
        # --- compute
        L("Compute", "U1", "Application SoC, 6 nm, 2xA78+6xA55, 10 TOPS NPU (MT8371)", "MediaTek", "Genio 520 (MT8371)", 1,
          (27.0, 22.0, 18.5), "E", "MediaTek via Richardson/Avnet/WPG", "Rockchip RK3576 (6 TOPS, LPDDR4X)"),
        L("Compute", "U2", "Companion PMIC set per Genio 520 reference design", "MediaTek", "MT63xx-class PMIC (NDA)", 1,
          (4.20, 3.50, 2.90), "E", "MediaTek", ""),
        L("Compute", "U3", "LPDDR5 4 GB (x32, 6400 MT/s) - 1B INT4 LLM + ASR + TTS", "Micron / SK hynix / Samsung / CXMT", "LPDDR5-4GB-x32", 1,
          (30.0, 26.0, 22.0), "E", "Franchised / broker (shortage)", "CXMT LPDDR5 (cost hedge)"),
        L("Compute", "U4", "eMMC 5.1 32 GB (OS + 3 City Packs + models)", "Kioxia / Samsung / Longsys", "eMMC-32GB", 1,
          (4.80, 4.00, 3.40), "E", "Franchised", "UFS 2.2 32GB"),
        L("Compute", "U5", "Always-on MCU: sensor hub, buttons, LED ring, power sequencing, BLE beacon", "Nordic Semiconductor", "nRF54L15-CAAA (WLCSP)", 1,
          (2.30, 1.90, 1.60), "E", "Nordic distribution", "Ambiq Apollo4 Lite"),
        # --- connectivity
        L("RF", "U6", "Wi-Fi 6 (1x1) + BT 5.4 dual-mode (BR/EDR A2DP + LE Audio) combo, per Genio ref design", "MediaTek", "MT79xx combo (e.g. MT7920/MT7921 class)", 1,
          (4.80, 4.00, 3.40), "E", "MediaTek", "AzureWave/USI module (EVT only)"),
        L("RF", "U7", "2.4/5 GHz FEM / diplexer", "Qorvo / Skyworks", "FEM-WiFi6-2G5G", 1,
          (0.90, 0.70, 0.55), "E", "Distribution", ""),
        L("RF", "U8", "GNSS L1+L5 module, GPS/GAL/BDS/QZSS/NavIC, 12.2x16x2.5 mm", "Quectel", "LC29HAA", 1,
          (7.80, 6.30, 5.30), "D", "Quectel / Mouser", "u-blox NEO-F10N"),
        L("RF", "ANT1-3", "Antennas: GNSS L1/L5 LDS, Wi-Fi/BT LDS on plastic carrier", "Pulse / Sunway / Luxshare", "LDS custom", 1,
          (1.40, 1.05, 0.80), "E", "Antenna house RFQ", "FPC antennas"),
    ]
    b += sensors_block() + audio_block("1309") + haptics_block()
    b += [
        L("UI", "U50", "24-ch constant-current LED driver (8 RGB LEDs ring)", "Texas Instruments", "LP5024RSMR", 1,
          (1.25, 1.00, 0.80), "E", "TI", "Awinic AW20036"),
        L("UI", "LED1-8", "RGB side-view LED 1.0x0.5 mm", "Everlight / Kingbright", "RGB-0402-SV", 8,
          (0.07, 0.05, 0.04), "E", "Distribution", ""),
        L("UI", "SW1-2", "Tact switch 4 N, 200k cycles (main button + volume rocker)", "C&K / Alps", "KMR2-class", 2,
          (0.14, 0.11, 0.09), "E", "Distribution", ""),
        L("Security", "U9", "Secure element (device identity, attestation keys, anti-clone)", "NXP", "SE050E2HQ1", 1,
          (2.10, 1.70, 1.35), "E", "NXP distribution", "Infineon OPTIGA Trust M"),
        L("Power", "BT1", "Li-ion polymer 650 mAh 3.87 V (2.52 Wh), 4.45 V HV, PCM+NTC, 5.5x35x32 mm", "ATL / Sunwoda / SCUD", "LP553532-650", 1,
          (3.30, 2.70, 2.25), "E", "Cell vendor RFQ", "EVE / Desay"),
    ]
    b += power_common(charger=("Analog Devices", "MAX77654AENV+ (charger+3 buck-boost SIMO, rails for MCU/sensors)", (3.20, 2.55, 2.10)))
    b += passives(330, (2.20, 1.70, 1.40))
    b += [
        L("PCB", "PCB1", "Main PCB 8-layer HDI 2+4+2, 36 mm round-square, 0.8 mm, ENEPIG", "Unimicron / Zhen Ding / Kinwong / SCC", "LORE-PB-MAIN", 1,
          (6.00, 4.40, 3.40), "E", "PCB fab RFQ", ""),
        L("PCB", "FPC1-2", "Flex: battery/pogo flex, button+LED flex", "Career / Flexium / MFLEX", "LORE-PB-FPC", 1,
          (1.40, 1.05, 0.85), "E", "FPC fab RFQ", ""),
        L("PCB", "SH1-3", "Stamped RF shield cans (frame+lid), nickel-silver", "Local Shenzhen stamping", "SHIELD-PB", 3,
          (0.22, 0.16, 0.12), "E", "Stamping vendor", ""),
        L("PCB", "J3-4", "Board-to-board connectors (battery, FPC)", "Panasonic / Hirose", "AXE6 / BM28 class", 2,
          (0.30, 0.24, 0.19), "E", "Distribution", ""),
        # --- mechanical
        L("Mechanical", "MEC1", "Top shell PC+30%GF, soft-touch PU paint, Bone/Ink/Terracotta", "Tier-1 molder (Dongguan)", "LORE-PB-TOP", 1,
          (1.60, 1.10, 0.80), "E", "Molder RFQ", ""),
        L("Mechanical", "MEC2", "Bottom shell PC+GF with pogo bosses & clip rail", "Tier-1 molder", "LORE-PB-BOT", 1,
          (1.20, 0.85, 0.62), "E", "Molder RFQ", ""),
        L("Mechanical", "MEC3", "LED light-guide ring (PMMA, frosted) + diffuser", "Tier-1 molder", "LORE-PB-LGR", 1,
          (0.55, 0.38, 0.28), "E", "Molder RFQ", ""),
        L("Mechanical", "MEC4", "Button caps (zinc die-cast, PVD) + rubber keypad", "Die-caster", "LORE-PB-BTN", 1,
          (0.65, 0.45, 0.35), "E", "RFQ", ""),
        L("Mechanical", "MEC5", "Gaskets, PSA die-cuts, acoustic vents (ePTFE IP67)", "Saati / Gore / 3M", "various", 1,
          (1.10, 0.85, 0.68), "E", "Die-cut converter", ""),
        L("Mechanical", "MEC6", "Thermal: graphite sheet 40 um + TIM gel", "Panasonic PGS / Jones", "various", 1,
          (0.45, 0.35, 0.28), "E", "Converter", ""),
        L("Mechanical", "MEC7", "Detachable spring-steel clip with PC overmould", "Stamping + molding", "LORE-PB-CLIP", 1,
          (0.90, 0.65, 0.50), "E", "RFQ", ""),
        L("Mechanical", "MEC8", "Screws/inserts/magnets (dock alignment, N52 x2)", "various", "various", 1,
          (0.35, 0.27, 0.21), "E", "RFQ", ""),
    ]
    b += packaging_block(cable=True, extra=("Silicone lanyard loop", (0.80, 0.60, 0.45)))
    return b


def packaging_block(cable=True, extra=None, premium=False):
    p = [
        L("Packaging", "PKG1", ("Rigid two-piece box, wrapped FSC paper, foil, magnet close" if premium else
                                "Rigid FSC box with sleeve, moulded-pulp insert"), "Shenzhen packaging house", "LORE-PKG",
          1, ((6.50, 4.80, 3.80) if premium else (3.20, 2.40, 1.85)), "E", "Packaging RFQ", ""),
        L("Packaging", "PKG2", "Quick-start guide, regulatory leaflet, labels", "Printer", "LORE-QSG", 1,
          (0.30, 0.22, 0.17), "E", "Printer", ""),
    ]
    if cable:
        p.append(L("Packaging", "ACC1", "USB-C to USB-C braided 1 m cable (60 W, E-marker-less)", "Cable OEM", "CBL-C2C-1M", 1,
                   (1.30, 1.00, 0.80), "E", "Cable OEM", ""))
    if extra:
        p.append(L("Packaging", "ACC2", extra[0], "Accessory OEM", "ACC", 1, extra[1], "E", "RFQ", ""))
    return p


def bom_square():
    b = [
        L("Compute", "U1", "Application SoC, 6 nm, 2xA78+6xA55, 10 TOPS NPU, Mali GPU (MT8391)", "MediaTek", "Genio 720 (MT8391)", 1,
          (36.0, 30.0, 25.5), "E", "MediaTek via Richardson/Avnet/WPG", "Qualcomm QCS6490 (12 TOPS)"),
        L("Compute", "U2", "Companion PMIC set per Genio 720 reference design (incl. audio codec)", "MediaTek", "MT63xx-class PMIC (NDA)", 1,
          (4.80, 4.00, 3.30), "E", "MediaTek", ""),
        L("Compute", "U3", "LPDDR5 6 GB (x32, 6400 MT/s) - 3B INT4 LLM resident (Linux, not GMS Android)", "Micron / SK hynix / Samsung / CXMT", "LPDDR5-6GB-x32", 1,
          (46.0, 38.0, 32.0), "E", "Franchised / broker (shortage)", "CXMT LPDDR5"),
        L("Compute", "U4", "UFS 2.2 64 GB", "Kioxia / Samsung / SK hynix", "UFS22-64GB", 1,
          (8.50, 7.20, 6.20), "E", "Franchised", "eMMC 5.1 64GB"),
        L("Compute", "U5", "Always-on MCU: sensor hub, crown, buttons, SOS path, power sequencing", "Nordic Semiconductor", "nRF54L15-CAAA (WLCSP)", 1,
          (2.30, 1.90, 1.60), "E", "Nordic distribution", "Ambiq Apollo4 Lite"),
        L("RF", "U6", "LTE Cat-4 global module (FDD/TDD, 3G fallback), LGA 29x32x2.4 mm", "Quectel", "EG25-G (EG25GGB-256-SGNS)", 1,
          (38.0, 26.0, 21.0), "D", "Quectel direct / RS / SOS", "Quectel EG95-EX/NA regional; chip-down v2"),
        L("RF", "U7", "Consumer eSIM eUICC, GSMA SGP.22, WLCSP 1.8x1.6 mm", "Infineon", "OPTIGA Connect Consumer OC1230", 1,
          (1.60, 1.25, 0.95), "E", "Infineon / connectivity partner", "Thales/Kigen eUICC; ST ST4SIM (SGP.32)"),
        L("RF", "U8", "Wi-Fi 6 + BT 5.4 dual-mode combo (LE Audio, Auracast, A2DP) per Genio ref design", "MediaTek", "MT79xx combo (MT7920/MT7921 class)", 1,
          (4.80, 4.00, 3.40), "E", "MediaTek", "AzureWave module (EVT)"),
        L("RF", "U9", "2.4/5 GHz FEM", "Qorvo / Skyworks", "FEM-WiFi6-2G5G", 1,
          (0.90, 0.70, 0.55), "E", "Distribution", ""),
        L("RF", "U10", "GNSS L1+L5 module 12.2x16x2.5 mm", "Quectel", "LC29HAA", 1,
          (7.80, 6.30, 5.30), "D", "Quectel / Mouser", "u-blox NEO-F10N"),
        L("RF", "U11", "LTE antenna aperture tuner SP4T (low-band tuning for metal body)", "Infineon", "BGSA14GN10", 1,
          (0.65, 0.50, 0.40), "E", "Infineon", "Qorvo QAT3550"),
        L("RF", "ANT1-4", "Antennas: LTE main (frame slot) + LTE div + GNSS L1/L5 + Wi-Fi/BT (LDS)", "Pulse / Sunway / Luxshare", "LDS + frame-feed", 1,
          (2.60, 1.95, 1.50), "E", "Antenna house RFQ", ""),
        L("RF", "J5-8", "Micro-coax + spring contacts for frame antenna feeds", "I-PEX / Murata", "MHF7S / spring clips", 1,
          (0.90, 0.68, 0.52), "E", "Distribution", ""),
    ]
    b += sensors_block() + audio_block("1511") + haptics_block()
    b += [
        L("Display", "LCD1", "1.6in AMOLED 466x466 round-corner, on-cell touch, MIPI-DSI 1-lane / QSPI, AOD, 1000 nit HBM", "Visionox / BOE / Tianma", "AMOLED-1.60-466-custom (CO5300/RM690B0 DDIC)", 1,
          (15.0, 12.0, 9.80), "E", "Panel maker RFQ (semi-custom cut)", "1.43in 466x466 std panel (EVT)"),
        L("Display", "CG1", "Cover glass 2.5D aluminosilicate 0.55 mm, AR+AF coat, printed mask", "Lens Tech / Biel", "CG-SQ-055", 1,
          (2.10, 1.65, 1.30), "E", "Lens Technology RFQ", "Corning Gorilla / AGC Dragontrail"),
        L("UI", "U51", "Optical crown rotation sensor (finger-nav, 0.1 deg-class)", "PixArt", "PAT9125EL-TKIT", 1,
          (1.70, 1.35, 1.05), "E", "PixArt distributor", "Hall + magnet ring"),
        L("UI", "SW1-3", "Tact switches (crown push, main button, SOS)", "C&K / Alps", "KMR2-class", 3,
          (0.14, 0.11, 0.09), "E", "Distribution", ""),
        L("Security", "U12", "Secure element (device identity, theft-lock, attestation)", "NXP", "SE050E2HQ1", 1,
          (2.10, 1.70, 1.35), "E", "NXP", "Infineon OPTIGA Trust M"),
        L("Power", "BT1", "Li-ion polymer 1100 mAh 3.88 V (4.27 Wh), Si-C anode, 4.45 V, 4.0x46x40 mm, PCM+NTC", "ATL / Sunwoda / SCUD", "LP404640-1100", 1,
          (4.80, 3.90, 3.20), "E", "Cell vendor RFQ", "EVE / Desay"),
    ]
    b += power_common()
    b += [
        L("Power", "U43", "3.8 V high-current buck-boost for LTE PA rail (2 A peaks)", "Texas Instruments", "TPS63810", 1,
          (1.30, 1.05, 0.85), "E", "TI", "Richtek RT6160"),
        L("Power", "U44", "Load switches / LDOs (GNSS, sensors, mic bias)", "TI / Torex", "TPS22916 / TLV755P", 4,
          (0.18, 0.14, 0.11), "E", "Distribution", ""),
    ]
    b += passives(520, (3.10, 2.40, 1.95))
    b += [
        L("PCB", "PCB1", "Main PCB 10-layer any-layer HDI, 48x48 mm rounded, 0.8 mm, ENEPIG", "Unimicron / Zhen Ding / AT&S", "LORE-SQ-MAIN", 1,
          (10.50, 7.40, 5.80), "E", "PCB fab RFQ", ""),
        L("PCB", "FPC1-4", "Flex: display tail, crown/button flex, battery/pogo flex, antenna feed flex", "Career / Flexium / MFLEX", "LORE-SQ-FPC", 1,
          (2.40, 1.80, 1.40), "E", "FPC fab RFQ", ""),
        L("PCB", "SH1-5", "RF shield cans (SoC/DRAM, LTE, Wi-Fi, GNSS, PMIC)", "Shenzhen stamping", "SHIELD-SQ", 5,
          (0.22, 0.16, 0.12), "E", "Stamping vendor", ""),
        L("PCB", "J3-6", "Board-to-board connectors (display, battery, flexes)", "Panasonic / Hirose", "A35S / BM28", 4,
          (0.32, 0.25, 0.20), "E", "Distribution", ""),
        L("Mechanical", "MEC1", "Unibody housing 6013-T6 Al, CNC 5-axis + NMT antenna breaks + anodise (Ink/Sand) + laser", "Catcher / Foxconn / BYD Elec / Tongda", "LORE-SQ-HSG", 1,
          (17.0, 11.5, 8.50), "E", "CNC house RFQ", "Die-cast Al + CNC finish"),
        L("Mechanical", "MEC2", "Back cover PC+GF RF-transparent, IMR texture, pogo inserts, laser marking", "Tier-1 molder", "LORE-SQ-BACK", 1,
          (1.50, 1.05, 0.80), "E", "Molder RFQ", "Zirconia ceramic"),
        L("Mechanical", "MEC3", "Crown: 316L SS machined, knurled, with shaft seal", "Precision turning", "LORE-SQ-CRN", 1,
          (1.40, 1.00, 0.78), "E", "RFQ", ""),
        L("Mechanical", "MEC4", "Button caps 316L SS / Al, terracotta SOS accent", "Precision turning", "LORE-SQ-BTN", 2,
          (0.40, 0.28, 0.22), "E", "RFQ", ""),
        L("Mechanical", "MEC5", "Gaskets, display PSA, acoustic vents ePTFE (IP67), mid-frame foam", "Saati / Gore / 3M", "various", 1,
          (1.50, 1.15, 0.92), "E", "Die-cut converter", ""),
        L("Mechanical", "MEC6", "Thermal: Cu foil 50 um + 2x graphite 40 um + TIM gel + vapour-chamber-lite (0.3 mm)", "Jones / Auras / Panasonic", "various", 1,
          (1.60, 1.20, 0.95), "E", "Converter", "Graphite-only"),
        L("Mechanical", "MEC7", "Mid-frame SUS 0.2 mm stamped (display support, ground)", "Stamping", "LORE-SQ-MF", 1,
          (0.55, 0.40, 0.30), "E", "RFQ", ""),
        L("Mechanical", "MEC8", "Screws (Torx T2), magnets N52 for dock (x2), lanyard pin", "various", "various", 1,
          (0.40, 0.30, 0.24), "E", "RFQ", ""),
    ]
    b += packaging_block(cable=True, extra=("Leather-look lanyard + quick-release clip", (1.60, 1.20, 0.90)))
    return b


def bom_atlas():
    b = bom_square()
    rep = {
        "U3": L("Compute", "U3", "LPDDR5 8 GB (x32, 6400 MT/s) - 3-4B INT4 LLM + VLM resident", "Micron / SK hynix / Samsung", "LPDDR5-8GB-x32", 1,
                (60.0, 50.0, 42.0), "E", "Franchised (shortage)", "12 GB if 4B+VLM concurrency needed"),
        "U4": L("Compute", "U4", "UFS 3.1 128 GB", "Kioxia / Samsung", "UFS31-128GB", 1,
                (14.0, 12.0, 10.3), "E", "Franchised", ""),
        "BT1": L("Power", "BT1", "Li-ion polymer 1450 mAh 3.88 V (5.63 Wh), Si-C anode, 5.2x46x40 mm, PCM+NTC", "ATL / Sunwoda", "LP524640-1450", 1,
                 (6.00, 4.90, 4.00), "E", "Cell vendor RFQ", ""),
        "PCB1": L("PCB", "PCB1", "Stacked main board: 2x 10-layer any-layer HDI + interposer (sandwich), 48x48 mm", "Unimicron / Zhen Ding / AT&S", "LORE-AT-MAIN-STACK", 1,
                  (19.0, 13.5, 10.5), "E", "PCB fab RFQ", "Single board + daughterboard"),
        "CG1": L("Display", "CG1", "Sapphire cover 0.7 mm, double-side AR, AF, PVD mask", "Biel / Crystal-Optech / Lens Tech", "SAP-AT-070", 1,
                 (9.00, 6.50, 5.00), "E", "Sapphire finisher RFQ", "Aluminosilicate (cost-down)"),
        "MEC1": L("Mechanical", "MEC1", "Housing Ti Gr.5 (Ti-6Al-4V) CNC 5-axis, bead-blast or black DLC, ceramic-filled antenna breaks", "Catcher / BYD Elec / Lens Tech", "LORE-AT-HSG", 1,
                  (46.0, 30.0, 22.0), "E", "Ti CNC house RFQ", "Ti Gr.2 (easier machining) / MIM Ti"),
        "MEC2": L("Mechanical", "MEC2", "Back cover zirconia ceramic (RF window) with pogo pads + camera bezel", "Sinocera / Lens Tech", "LORE-AT-BACK", 1,
                  (5.50, 4.00, 3.10), "E", "Ceramic RFQ", "Sapphire back"),
        "MEC3": L("Mechanical", "MEC3", "Crown: Ti machined with brass-tone PVD accent ring", "Precision turning", "LORE-AT-CRN", 1,
                  (2.80, 2.00, 1.55), "E", "RFQ", ""),
        "PKG1": packaging_block(premium=True)[0],
        "ANT1-4": L("RF", "ANT1-4", "Antennas: LTE main+div (Ti frame segments), GNSS L1/L5, Wi-Fi/BT, NTN L/S-band", "Pulse / Sunway / Luxshare", "frame-feed + LDS", 1,
                    (3.60, 2.70, 2.10), "E", "Antenna house RFQ", ""),
    }
    b = [rep.get(x["ref"], x) for x in b]
    b += [
        L("RF", "U13", "3GPP Rel-17 IoT-NTN module (Skylo-certified) + LTE-M/NB fallback, 23.6x19.9x2.2 mm", "Quectel", "BG95-S5", 1,
          (19.0, 14.5, 11.5), "E", "Quectel", "Quectel CC660D-LS (NTN-only)"),
        L("RF", "U14", "SPDT RF switch NTN/LTE antenna share", "Infineon / pSemi", "BGS12P2L6", 1,
          (0.30, 0.24, 0.19), "E", "Distribution", ""),
        L("Camera", "CAM1", "13 MP 1/3in 1.12 um 'Glance' camera, fixed-focus wide (~100 deg DFOV) module 6.4x7.2 mm, MIPI CSI-2 4-lane", "OmniVision (module: Sunny / Q-Tech / O-Film)", "OV13B10 FF module", 1,
          (6.20, 5.10, 4.30), "E", "Module house RFQ", "OmniVision OV08B10 8 MP"),
        L("Camera", "CAM2", "Camera window sapphire 4 mm + privacy LED", "Biel / Everlight", "CAMWIN-AT", 1,
          (0.80, 0.60, 0.45), "E", "RFQ", ""),
        L("Mechanical", "MEC9", "Extra thermal: 0.4 mm Ti-compatible vapour chamber + Cu heat-spreader", "Auras / Jones", "VC-AT-04", 1,
          (3.20, 2.40, 1.90), "E", "Thermal vendor RFQ", ""),
    ]
    b = [x for x in b if x["ref"] != "ACC2"]
    b.append(L("Packaging", "ACC2", "Full-grain leather lanyard + Ti quick-release + polishing cloth", "Accessory OEM", "ACC-AT", 1,
               (4.00, 3.00, 2.30), "E", "RFQ", ""))
    return b


def bom_pebble_lite():
    """ECR proposal (not COMPANY.md-compliant): MCU-class Pebble, ~1B model runs on the user's phone."""
    keep_refs = {"U8", "ANT1-3", "U20", "U21", "U22", "MK1-2", "U30", "LS1", "U31", "M1", "U50", "LED1-8", "SW1-2",
                 "U9", "BT1", "U41", "U42", "J1", "D1-4", "J2", "Y1-3", "FPC1-2", "SH1-3", "J3-4",
                 "MEC1", "MEC2", "MEC3", "MEC4", "MEC5", "MEC7", "MEC8", "PKG1", "PKG2", "ACC1", "ACC2"}
    b = [x for x in bom_pebble() if x["ref"] in keep_refs]
    b += [
        L("Compute", "U1", "Dual-mode BT 5.4 audio SoC (BR/EDR source + LE Audio/Auracast) + DSP, 8 MB flash", "Airoha / Bestechnic / Realtek", "AB159x / BES27xx / RTL8773 class (source FW)", 1,
          (3.80, 3.10, 2.60), "E", "Vendor RFQ", ""),
        L("Compute", "U5", "Host MCU: sensor fusion, offline narration cache, BLE to phone", "Nordic Semiconductor", "nRF54L15", 1,
          (2.30, 1.90, 1.60), "E", "Nordic distribution", ""),
        L("Compute", "U4", "QSPI NOR 64 MB (story audio cache, 1 neighbourhood)", "Winbond / GigaDevice", "W25Q512 class", 1,
          (2.20, 1.80, 1.50), "E", "Distribution", ""),
        L("Passives", "R/C/L", "Passives (~180 pcs)", "Murata/Samsung EM/Yageo", "various", 1, (1.20, 0.95, 0.78), "E", "Distribution", ""),
        L("PCB", "PCB1", "Main PCB 6-layer HDI 1+4+1, 36 mm", "Kinwong / SCC", "LORE-PBL-MAIN", 1, (3.20, 2.40, 1.90), "E", "PCB RFQ", ""),
    ]
    return b


# ---------------------------------------------------------------- conversion layers (per unit, per tier)
CONV = {
    # SMT (double-sided), FATP labour, test (ICT/FCT/RF cal/IP leak/display/audio), programming + key injection, freight
    "pebble":      dict(smt=(4.2, 2.8, 2.1), fatp=(6.0, 3.9, 3.0), test=(3.6, 2.4, 1.7), prog=(0.45, 0.35, 0.25), freight=(2.2, 1.4, 1.1)),
    "pebble_lite": dict(smt=(2.6, 1.8, 1.3), fatp=(5.0, 3.3, 2.5), test=(2.4, 1.6, 1.2), prog=(0.30, 0.25, 0.18), freight=(2.0, 1.3, 1.0)),
    "square":      dict(smt=(6.0, 4.0, 3.0), fatp=(9.0, 6.0, 4.5), test=(5.5, 3.6, 2.6), prog=(0.55, 0.42, 0.30), freight=(2.8, 1.8, 1.4)),
    "atlas":       dict(smt=(7.5, 5.0, 3.8), fatp=(13.0, 8.5, 6.4), test=(7.0, 4.6, 3.3), prog=(0.60, 0.45, 0.33), freight=(3.4, 2.2, 1.7)),
}
YIELD = {"1k": 0.07, "10k": 0.035, "100k": 0.02}   # scrap/rework loss as fraction of material+conversion
# royalties / licences per unit (estimates)
ROYALTY = {
    "pebble":      [("Bluetooth/LC3 (SIG membership covers LC3; no per-unit fee)", 0.00),
                    ("Optional AAC encoder licence (Via LA) - not in baseline", 0.00),
                    ("OS/BSP: AOSP/Yocto - no per-unit fee", 0.00)],
    "pebble_lite": [("No per-unit royalties in baseline", 0.00)],
    "square":      [("Cellular LTE Cat-4 SEP stack (Qualcomm IoT program 3.5-5% of module price + Nokia/Ericsson/InterDigital/Huawei etc.; est.)", 5.00),
                    ("eUICC bootstrap profile + EUM/SM-DS fees (connectivity partner; est.)", 0.80),
                    ("OS/BSP AOSP - no per-unit fee", 0.00)],
    "atlas":       [("Cellular LTE Cat-4 + NB-IoT/LTE-M/NTN SEP stack (est.)", 6.50),
                    ("eUICC bootstrap profile + EUM/SM-DS fees (est.)", 0.80),
                    ("H.264/HEVC encode (Via LA / Access Advance) for Glance clips (est.)", 0.40),
                    ("Skylo NTN device activation (est., may be opex)", 1.00)],
}
# NRE (one-off, USD) - see ../certification.md and ../dfm-manufacturing.md
NRE = {
    "pebble":      dict(cert=165_000, tooling=95_000, fixtures=45_000),
    "pebble_lite": dict(cert=140_000, tooling=95_000, fixtures=35_000),
    "square":      dict(cert=485_000, tooling=140_000, fixtures=95_000),
    "atlas":       dict(cert=640_000, tooling=210_000, fixtures=120_000),
}
CHINA_TARIFF = 0.20   # scenario only


def rollup(sku, bom):
    out = {}
    for i, t in enumerate(TIERS):
        key = "p" + t
        cats = {}
        for x in bom:
            cats[x["cat"]] = cats.get(x["cat"], 0) + x["qty"] * x[key]
        material = sum(cats.values())
        c = CONV[sku]
        conv = c["smt"][i] + c["fatp"][i] + c["test"][i] + c["prog"][i]
        yl = YIELD[t] * (material + conv)
        roy = sum(v for _, v in ROYALTY[sku])
        n = NRE[sku]
        cert_am = n["cert"] / TIER_QTY[t]
        tool_am = (n["tooling"] + n["fixtures"]) / TIER_QTY[t]
        freight = c["freight"][i]
        fob = material + conv + yl
        ex_nre = fob + roy + freight
        landed = ex_nre + cert_am + tool_am
        out[t] = dict(categories=cats, material=material, smt=c["smt"][i], fatp=c["fatp"][i], test=c["test"][i],
                      prog=c["prog"][i], conversion=conv, yield_loss=yl, royalties=roy, freight=freight,
                      cert_amort=cert_am, tooling_amort=tool_am, fob=fob, landed_ex_nre=ex_nre,
                      landed=landed, landed_china_fatp=landed + CHINA_TARIFF * fob)
    return out


def write_csv(sku, bom):
    path = os.path.join(HERE, f"bom_{sku}.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "ref", "description", "manufacturer", "mpn", "qty",
                    "unit_1k", "unit_10k", "unit_100k", "ext_1k", "ext_10k", "ext_100k",
                    "price_basis", "supplier", "alternates"])
        for x in bom:
            w.writerow([x["cat"], x["ref"], x["desc"], x["mfr"], x["mpn"], x["qty"],
                        f'{x["p1k"]:.2f}', f'{x["p10k"]:.2f}', f'{x["p100k"]:.2f}',
                        f'{x["qty"]*x["p1k"]:.2f}', f'{x["qty"]*x["p10k"]:.2f}', f'{x["qty"]*x["p100k"]:.2f}',
                        x["src"], x["supplier"], x["alt"]])
    return path


PRICE = {"pebble": 149, "pebble_lite": 149, "square": 299, "atlas": 549}
NAMES = {"pebble": "Pebble", "pebble_lite": "Pebble Lite (ECR)", "square": "Square", "atlas": "Atlas"}


def md_table_bom(bom):
    s = "| Cat | Ref | Description | Mfr | MPN | Qty | $ @1k | $ @10k | $ @100k | Basis | Alternate |\n"
    s += "|---|---|---|---|---|---:|---:|---:|---:|:-:|---|\n"
    for x in bom:
        s += (f'| {x["cat"]} | {x["ref"]} | {x["desc"]} | {x["mfr"]} | {x["mpn"]} | {x["qty"]} | '
              f'{x["qty"]*x["p1k"]:.2f} | {x["qty"]*x["p10k"]:.2f} | {x["qty"]*x["p100k"]:.2f} | {x["src"]} | {x["alt"]} |\n')
    return s


def md_rollup(sku, r):
    rows = [("Electronics + mechanical + packaging material", "material"), ("SMT", "smt"), ("FATP labour", "fatp"),
            ("Test (ICT/FCT/RF cal/IP leak)", "test"), ("Programming & key injection", "prog"),
            ("Yield loss / scrap", "yield_loss"), ("**FOB factory**", "fob"), ("Royalties & licences", "royalties"),
            ("Freight & insurance to US/EU 3PL", "freight"), ("**Landed COGS ex-NRE**", "landed_ex_nre"),
            ("Certification amortisation", "cert_amort"), ("Tooling + fixture amortisation", "tooling_amort"),
            ("**Landed COGS incl. NRE (VN/MY FATP, 0% duty)**", "landed"),
            ("Scenario: China FATP (+20% tariff on FOB)", "landed_china_fatp")]
    s = "| Line | @1k | @10k | @100k |\n|---|---:|---:|---:|\n"
    for name, k in rows:
        s += f"| {name} | " + " | ".join(f"{r[t][k]:,.2f}" for t in TIERS) + " |\n"
    gm = (PRICE[sku] - r["10k"]["landed"]) / PRICE[sku]
    gm_ex = (PRICE[sku] - r["10k"]["landed_ex_nre"]) / PRICE[sku]
    s += (f"\nTarget retail ${PRICE[sku]} -> hardware gross margin @10k on DTC price: **{gm*100:.0f} %** incl. NRE, "
          f"{gm_ex*100:.0f} % ex-NRE (before payment fees, returns, warranty, channel margin).\n")
    return s


def main():
    boms = {"pebble": bom_pebble(), "square": bom_square(), "atlas": bom_atlas(), "pebble_lite": bom_pebble_lite()}
    results = {}
    for sku, b in boms.items():
        write_csv(sku, b)
        results[sku] = rollup(sku, b)

    # summary csv
    with open(os.path.join(HERE, "cogs_summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sku", "tier", "material", "conversion", "yield_loss", "fob", "royalties", "freight",
                    "landed_ex_nre", "cert_amort", "tooling_amort", "landed_incl_nre", "landed_china_fatp_scenario",
                    "target_price", "gm_incl_nre"])
        for sku, r in results.items():
            for t in TIERS:
                x = r[t]
                w.writerow([sku, t] + [f"{x[k]:.2f}" for k in ["material", "conversion", "yield_loss", "fob", "royalties", "freight",
                                                              "landed_ex_nre", "cert_amort", "tooling_amort", "landed", "landed_china_fatp"]]
                           + [PRICE[sku], f"{(PRICE[sku]-x['landed'])/PRICE[sku]:.3f}"])
    with open(os.path.join(HERE, "cogs_summary.json"), "w") as f:
        json.dump({s: {t: {k: (round(v, 2) if isinstance(v, float) else {kk: round(vv, 2) for kk, vv in v.items()})
                           for k, v in r[t].items()} for t in TIERS} for s, r in results.items()}, f, indent=1)

    # markdown
    md = ["# LORE - Costed Bill of Materials & Landed COGS\n",
          "_Generated by `build_bom.py` - do not hand-edit; edit the script and re-run._\n",
          "All prices USD per unit. **Basis:** D = distributor price observed (volume extrapolated), "
          "E = engineering estimate (NDA silicon, custom parts, labour; treat as +/-25 %), Q = RFQ pending. "
          "Memory lines are priced for the 2026-27 DRAM shortage and are the most volatile items.\n",
          "## Summary @ 10k units\n",
          "| SKU | Material | FOB | Landed ex-NRE | Landed incl. NRE | China-FATP scenario | Target price | GM incl. NRE |\n|---|---:|---:|---:|---:|---:|---:|---:|\n"]
    for sku in ["pebble", "square", "atlas", "pebble_lite"]:
        x = results[sku]["10k"]
        md.append(f"| {NAMES[sku]} | {x['material']:.2f} | {x['fob']:.2f} | {x['landed_ex_nre']:.2f} | **{x['landed']:.2f}** | "
                  f"{x['landed_china_fatp']:.2f} | {PRICE[sku]} | {(PRICE[sku]-x['landed'])/PRICE[sku]*100:.0f} % |\n")
    md.append("\n![COGS by category](cogs_summary.png)\n\n![COGS vs volume](cogs_vs_volume.png)\n")
    md.append("\n## Assumptions\n"
              "* Conversion costs (SMT, FATP, test) are estimates for a Tier-2 Shenzhen/Dongguan EMS or VN/MY site, at 2026 labour rates.\n"
              f"* Yield loss: {', '.join(f'{t}: {YIELD[t]*100:.1f} %' for t in TIERS)} of material+conversion.\n"
              "* NRE amortised over the tier volume (1k column = true cost of a 1k programme). NRE totals: "
              + "; ".join(f"{NAMES[s]} cert ${NRE[s]['cert']/1e3:.0f}k + tooling ${NRE[s]['tooling']/1e3:.0f}k + fixtures ${NRE[s]['fixtures']/1e3:.0f}k" for s in NRE) + ".\n"
              "* Base duty case: FATP in Vietnam/Malaysia, 0 % US MFN on HTS 8517.62 (assumed - confirm with customs broker). "
              "China-FATP scenario adds 20 % of FOB (assumed Section 301 tiers; source unverified).\n"
              "* Royalties are estimates: cellular SEPs for LTE Cat-4 IoT-class devices (Qualcomm IoT program publishes 3.5-5 % of module price; "
              "other licensors bilateral). Risk: licensors may assert handset/wearable-class rates.\n"
              "* Not in COGS: warranty reserve (budget 2-3 % of revenue), payment fees, returns, eSIM data (opex, in Finance model), "
              "Kickstarter fulfilment.\n")
    md.append("\n## Sources\n" + "".join(f"* `{k}`: {v}\n" for k, v in SOURCES.items()))
    for sku in ["pebble", "square", "atlas", "pebble_lite"]:
        md.append(f"\n---\n\n## {NAMES[sku]} - landed COGS roll-up\n\n" + md_rollup(sku, results[sku]))
        md.append("\nRoyalty lines:\n" + "".join(f"* {n}: ${v:.2f}\n" for n, v in ROYALTY[sku]))
        md.append(f"\n### {NAMES[sku]} - line items (extended cost)\n\n" + md_table_bom(boms[sku]))
    with open(os.path.join(HERE, "BOM.md"), "w") as f:
        f.write("".join(md))

    # charts
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    pal = ["#14161A", "#C4623A", "#B8935A", "#5E6B4E", "#9AA0A6", "#0D1B2A", "#E0B8A3", "#8C9A7A", "#D9CBB0", "#6E7781",
           "#A44A2A", "#3B4A5C", "#CFC6B8", "#7F6A45"]
    order = ["Compute", "RF", "Display", "Camera", "Sensors", "Audio", "Haptics", "UI", "Security", "Power", "Passives", "PCB",
             "Mechanical", "Packaging"]
    extra = [("Conversion (SMT/FATP/test)", "conversion"), ("Yield loss", "yield_loss"), ("Royalties", "royalties"),
             ("Freight", "freight"), ("NRE amortisation", None)]
    skus = ["pebble", "pebble_lite", "square", "atlas"]
    fig, ax = plt.subplots(figsize=(11, 6.5))
    bottoms = [0] * len(skus)
    layers = order + [e[0] for e in extra]
    colors = pal + ["#4A4F57", "#E8DCC8", "#7A3E25", "#B0B5BA", "#D8A48F"]
    for li, layer in enumerate(layers):
        vals = []
        for s in skus:
            x = results[s]["10k"]
            if layer in order:
                vals.append(x["categories"].get(layer, 0))
            else:
                k = dict(extra)[layer]
                vals.append(x[k] if k else x["cert_amort"] + x["tooling_amort"])
        ax.bar([NAMES[s] for s in skus], vals, bottom=bottoms, color=colors[li % len(colors)], label=layer,
               edgecolor="white", linewidth=0.5)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    for i, s in enumerate(skus):
        ax.text(i, bottoms[i] + 4, f"${bottoms[i]:.0f}\n(target ${PRICE[s]})", ha="center", fontsize=9)
    ax.set_ylabel("USD per unit (landed, incl. NRE amortised over 10k)")
    ax.set_title("LORE landed COGS by category @ 10k units (estimates; see BOM.md)")
    ax.legend(ncol=2, fontsize=8, loc="upper left", frameon=False)
    ax.set_ylim(0, max(bottoms) * 1.25)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "cogs_summary.png"), dpi=150)

    fig, ax = plt.subplots(figsize=(8, 5))
    for s, c in zip(skus, ["#C4623A", "#B8935A", "#14161A", "#5E6B4E"]):
        ax.plot([1, 10, 100], [results[s][t]["landed"] for t in TIERS], "-o", color=c, label=f"{NAMES[s]} incl. NRE")
        ax.plot([1, 10, 100], [results[s][t]["landed_ex_nre"] for t in TIERS], "--", color=c, alpha=0.6, label=f"{NAMES[s]} ex-NRE")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xticks([1, 10, 100]); ax.set_xticklabels(["1k", "10k", "100k"])
    ax.set_xlabel("Programme volume (units)"); ax.set_ylabel("Landed COGS, USD/unit (log)")
    ax.set_title("Landed COGS vs volume (NRE amortised over volume)")
    ax.legend(fontsize=7, frameon=False, ncol=2)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "cogs_vs_volume.png"), dpi=150)

    # DRAM sensitivity: memory re-priced at pre-shortage-like $3.0/GB (10k tier)
    sens = {}
    gb = {"pebble": 4, "square": 6, "atlas": 8, "pebble_lite": 0}
    for s_ in boms:
        dram_now = sum(x["p10k"] for x in boms[s_] if x["mpn"].startswith("LPDDR5"))
        delta = dram_now - 3.0 * gb[s_]
        sens[s_] = dict(dram_10k=dram_now, normalised=3.0 * gb[s_],
                        landed_ex_nre_normalised=results[s_]["10k"]["landed_ex_nre"] - delta * (1 + YIELD["10k"]))
    with open(os.path.join(HERE, "dram_sensitivity.json"), "w") as f:
        json.dump(sens, f, indent=1)
    with open(os.path.join(HERE, "BOM.md"), "a") as f:
        f.write("\n---\n\n## DRAM price sensitivity (@10k)\n\n| SKU | DRAM in BOM | DRAM @ $3.0/GB | Landed ex-NRE (shortage) | Landed ex-NRE (normalised) |\n|---|---:|---:|---:|---:|\n")
        for s_ in ["pebble", "square", "atlas", "pebble_lite"]:
            v = sens[s_]
            f.write(f"| {NAMES[s_]} | {v['dram_10k']:.2f} | {v['normalised']:.2f} | {results[s_]['10k']['landed_ex_nre']:.2f} | {v['landed_ex_nre_normalised']:.2f} |\n")
    for s in ["pebble", "square", "atlas", "pebble_lite"]:
        x = results[s]
        print(f"{NAMES[s]:18s} material@10k={x['10k']['material']:7.2f}  landed ex-NRE={x['10k']['landed_ex_nre']:7.2f}  "
              f"landed incl NRE: 1k={x['1k']['landed']:8.2f} 10k={x['10k']['landed']:7.2f} 100k={x['100k']['landed']:7.2f}  "
              f"GM@10k={(PRICE[s]-x['10k']['landed'])/PRICE[s]*100:4.0f}%  exNRE-normDRAM={sens[s]['landed_ex_nre_normalised']:.2f}")


if __name__ == "__main__":
    main()
