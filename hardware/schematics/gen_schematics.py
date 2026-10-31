#!/usr/bin/env python3
"""
LORE Square - reference schematic sheets (schemdraw, net-label style)
=====================================================================
These are *reference/architecture* schematics for EVT schematic capture (Altium/Cadence by
the ODM): they fix the interfaces, net names, pull-ups, protection and matching topology.
Pin names for MediaTek Genio 720 / companion PMIC are indicative (datasheets under NDA);
module pin names follow the public Quectel / Bosch / TI / Infineon documentation and must be
re-verified against the latest hardware design guides at capture time.
Run: python3 gen_schematics.py  → sheetNN_*.svg / .png
"""
import os
import schemdraw
import schemdraw.elements as elm

HERE = os.path.dirname(os.path.abspath(__file__))
schemdraw.use("matplotlib")
schemdraw.config(fontsize=10, font="DejaVu Sans")


def ic(d, xy, name, left, right, top=(), bottom=(), w=4.2):
    pins = [elm.IcPin(name=p, side="left") for p in left] + [elm.IcPin(name=p, side="right") for p in right]
    pins += [elm.IcPin(name=p, side="top") for p in top] + [elm.IcPin(name=p, side="bottom") for p in bottom]
    e = elm.Ic(pins=pins, edgepadW=0.6, edgepadH=0.4, pinspacing=0.75, w=w, leadlen=0.6).label(name, "top", fontsize=11)
    e.at(xy).theta(0)
    d.add(e)
    return e


def net(d, el, pin, label, direction="right", length=1.2, color="#0D1B2A"):
    p = el.absanchors[pin]
    ln = getattr(elm.Line(), direction)(length).at(p).color(color)
    d.add(ln)
    loc = {"right": "right", "left": "left", "up": "top", "down": "bottom"}[direction]
    d.add(elm.Label().at(ln.end).label(label, loc=loc, color=color, fontsize=9))
    return ln


_TITLE = {}


def title(d, xy, text, sub):
    _TITLE["t"] = (text, sub)   # drawn in save() above the computed bounding box


def save(d, name):
    bb = d.get_bbox()
    text, sub = _TITLE["t"]
    d.add(elm.Label().at((bb.xmin, bb.ymax + 2.0)).label(text, fontsize=15, halign="left", color="#14161A"))
    d.add(elm.Label().at((bb.xmin, bb.ymax + 1.1)).label(sub, fontsize=9, halign="left", color="#5E6B4E"))
    p = os.path.join(HERE, f"{name}.svg")
    d.save(p)
    d.save(p.replace(".svg", ".png"), dpi=130)
    print("wrote", p)


# ---------------------------------------------------------------------------------- sheet 1
def sheet_power():
    with schemdraw.Drawing(show=False) as d:
        title(d, (0, 15), "Sheet 1 - Power tree: USB-C / pogo, charger, battery, fuel gauge, rails",
              "VBUS 5 V sink-only (Rd 5.1k x2), 1.1 A CC charge (1C), 4.45 V HV cell, JEITA via NTC, ship mode")
        usb = ic(d, (0, 10), "J1 USB-C 16p", [], ["VBUS", "CC1", "CC2", "D+", "D-", "GND"], w=2.5)
        net(d, usb, "CC1", "5k1 to GND (Rd)"); net(d, usb, "CC2", "5k1 to GND (Rd)")
        net(d, usb, "D+", "USB_DP → SoC USB2 (ESD TPD4E05U06)"); net(d, usb, "D-", "USB_DM → SoC")
        d.add(elm.Line().at(usb.absanchors["VBUS"]).right(1.5))
        d.add(elm.Zener().down(1.2).label("TVS 5V\nPESD5V0", loc="bottom"))
        d.add(elm.Ground())
        pogo = ic(d, (0, 4), "J2 pogo 4p", [], ["P_VIN", "P_GND", "P_ID", "P_UART"], w=2.5)
        net(d, pogo, "P_ID", "1-wire dock ID → nRF54L15 P1.04"); net(d, pogo, "P_UART", "factory UART (test mode)")
        d.add(elm.Line().at(pogo.absanchors["P_VIN"]).right(1.5))
        d.add(elm.Diode().right(1.5).label("ideal-diode OR\n(TPS2116)", loc="top"))
        chg = ic(d, (12, 9), "U41 BQ25620 charger",
                 ["VBUS", "PMID", "REGN", "TS", "SDA", "SCL", "INT", "CE"],
                 ["SW", "SYS", "BAT", "BATP", "PG", "QON"], w=4.5)
        net(d, chg, "VBUS", "VBUS (from J1 / pogo OR)", "left", 1.8)
        net(d, chg, "TS", "NTC 10k B3435 in pack", "left", 1.8)
        net(d, chg, "SDA", "I2C0_SDA (1.8V, 2k2 PU)", "left", 1.8); net(d, chg, "SCL", "I2C0_SCL", "left", 1.8)
        net(d, chg, "INT", "CHG_INT_N → SoC EINT", "left", 1.8); net(d, chg, "CE", "CHG_CE_N (GND)", "left", 1.8)
        net(d, chg, "SW", "L 1.0uH 0806 → SYS"); net(d, chg, "SYS", "VSYS 3.4-4.45 V (2x22uF)")
        net(d, chg, "BAT", "VBAT"); net(d, chg, "QON", "ship-mode wake = SOS key")
        bat = ic(d, (23, 9), "BT1 1100 mAh Li-ion", ["B+", "NTC", "B-"], [], w=3)
        fg = ic(d, (23, 3), "U42 MAX17262 FG", [], ["BATT", "CSP", "CSN", "SDA", "SCL", "ALRT"], w=3)
        net(d, fg, "SDA", "I2C0", "right", 1.0); net(d, fg, "ALRT", "FG_ALRT_N → hub", "right", 1.0)
        pm = ic(d, (12, 1), "U2 Genio companion PMIC (indicative)",
                ["VSYS_IN", "PWRKEY", "RTC_32K", "SPMI_CLK", "SPMI_DATA"],
                ["VPROC_B (big)", "VPROC_L (LITTLE)", "VCORE/VNPU", "VDD2H/VDDQ", "VIO18", "VA12/VUFS", "VAUD18 + codec"], w=5)
        net(d, pm, "VSYS_IN", "VSYS", "left", 1.6); net(d, pm, "PWRKEY", "PWRKEY_N ← hub", "left", 1.6)
        net(d, pm, "SPMI_CLK", "SPMI ↔ SoC", "left", 1.6)
        lte = ic(d, (34, 10), "U43 TPS63810 buck-boost", ["VIN", "EN", "MODE"], ["VOUT", "PG"], w=3.2)
        net(d, lte, "VIN", "VSYS", "left", 1.0); net(d, lte, "EN", "LTE_PWR_EN ← SoC", "left", 1.0)
        net(d, lte, "VOUT", "VBAT_LTE 3.8 V / 2 A peak (+ 470uF tantalum-polymer)")
        ls = ic(d, (34, 3), "U44a-d load switches / LDOs", ["VIN", "EN_GNSS", "EN_SNS", "EN_MIC"],
                ["3V3_GNSS (TPS22916)", "1V8_SNS AON (TLV755P)", "MICBIAS/1V8_MIC", "3V3_SPK → TAS2563 VBAT"], w=4)
        net(d, ls, "VIN", "VSYS", "left", 1.0)
        save(d, "sheet01_power_tree")


# ---------------------------------------------------------------------------------- sheet 2
def sheet_gnss():
    with schemdraw.Drawing(show=False) as d:
        title(d, (0, 9), "Sheet 2 - GNSS L1+L5: Quectel LC29HAA, antenna feed and matching",
              "Passive LDS antenna on top edge (sky-facing when clipped); 50 ohm CPW-G, pi-match DNP-tunable; L1 1575.42 / L5 1176.45 MHz")
        d += elm.Antenna().at((0, 4)).label("ANT_GNSS\nLDS L1/L5", loc="top")
        d += elm.Line().down(0.5)
        d += elm.Dot()
        p0 = d.here
        d += elm.Capacitor().down(1.5).at(p0).label("C1 DNP\n(shunt)", loc="bottom")
        d += elm.Ground()
        d += elm.Line().right(1.5).at(p0)
        d += elm.Inductor2().right(2).label("L1 0R/ 2.2nH\n(series)", loc="top")
        d += elm.Dot()
        p1 = d.here
        d += elm.Capacitor().down(1.5).at(p1).label("C2 DNP\n(shunt)", loc="bottom")
        d += elm.Ground()
        d += elm.Line().right(1.2).at(p1)
        d += elm.Zener().down(1.5).label("ESD 0.15pF\nESD0P2RF", loc="bottom")
        d += elm.Ground()
        d += elm.Line().right(2.5).at((p1[0] + 1.2, p1[1]))
        g = ic(d, (9, 7), "U10 Quectel LC29HAA (L1+L5)",
               ["RF_IN", "VCC", "V_BCKP", "RESET_N"], ["TXD1", "RXD1", "1PPS", "WAKEUP/STANDBY", "GND (x n)"], w=4.5)
        net(d, g, "VCC", "3V3_GNSS (load switch, 10uF+100nF)", "left", 2.0)
        net(d, g, "V_BCKP", "VBCKP 3.0V from hub LDO (hot-start under 1 s)", "left", 2.0)
        net(d, g, "RESET_N", "GNSS_RST_N ← hub (open-drain)", "left", 2.0)
        net(d, g, "TXD1", "UART_GNSS_RX (SoC UART2 / hub) 115200-921600")
        net(d, g, "RXD1", "UART_GNSS_TX")
        net(d, g, "1PPS", "GNSS_PPS → SoC timestamp GPIO + hub")
        net(d, g, "WAKEUP/STANDBY", "GNSS_WAKE ← hub (duty-cycling)")
        d.add(elm.Label().at((0, -1.5)).label(
            "Layout: keep-out 3 mm around feed; no DC-DC within 10 mm; LTE B13/B14 harmonic (2x787 MHz ~ L1) → notch/SAW option at EVT; "
            "run desense test with LTE TX at max power on all bands.", fontsize=8.5, halign="left"))
        save(d, "sheet02_gnss_antenna")


# ---------------------------------------------------------------------------------- sheet 3
def sheet_sensors():
    with schemdraw.Drawing(show=False) as d:
        title(d, (0, 13), "Sheet 3 - Always-on sensor hub: nRF54L15 + BHI360 + BMM350 + BMP390",
              "Hub stays powered in AP suspend; BHI360 runs fusion/PDR on-chip; BMM350 on BHI360 aux master (I3C/I2C)")
        h = ic(d, (0, 4), "U5 nRF54L15 (hub)",
               ["SPIM00_SCK", "SPIM00_MOSI", "SPIM00_MISO", "CS_BHI", "BHI_HIRQ", "BHI_RST_N",
                "TWIM21_SDA", "TWIM21_SCL", "BARO_INT"],
               ["UARTE20_TX", "UARTE20_RX", "AP_WAKE", "HUB_IRQ_N", "KEY_SOS", "KEY_TALK", "CROWN_MOT", "PWRKEY_N", "SWD"], w=5)
        for p, lab in (("UARTE20_TX", "→ SoC UART1_RX 1 Mbps"), ("UARTE20_RX", "← SoC UART1_TX"),
                       ("AP_WAKE", "→ SoC EINT (wake AP)"), ("HUB_IRQ_N", "← SoC GPIO"),
                       ("KEY_SOS", "SW3 (100k PU, RC 1ms)"), ("KEY_TALK", "SW2 crown push"),
                       ("CROWN_MOT", "← PAT9125 MOTION"), ("PWRKEY_N", "→ PMIC PWRKEY"), ("SWD", "TP (Tag-Connect)")):
            net(d, h, p, lab, length=1.0)
        bhi = ic(d, (-14, 9), "U20 BHI360", ["VDD", "VDDIO"], ["SCK", "SDI", "SDO", "CSB", "HIRQ", "RESETN", "MSDA", "MSCL"], w=3.2)
        net(d, bhi, "VDD", "1V8_SNS", "left"); net(d, bhi, "VDDIO", "1V8_SNS", "left")
        mag = ic(d, (-14, 1), "U21 BMM350", ["VDD", "VDDIO", "INT"], ["SDA", "SCL", "ADSEL"], w=3.0)
        net(d, mag, "SDA", "BHI MSDA (4k7 PU)"); net(d, mag, "SCL", "BHI MSCL (4k7 PU)")
        net(d, mag, "VDD", "1V8_SNS", "left"); net(d, mag, "INT", "DRDY → BHI GPIO", "left")
        bar = ic(d, (-14, -4), "U22 BMP390", ["VDD", "VDDIO", "SDO"], ["SDA", "SCL", "INT"], w=3.0)
        net(d, bar, "SDA", "TWIM21_SDA (2k2 PU to 1V8_SNS)"); net(d, bar, "SCL", "TWIM21_SCL")
        net(d, bar, "INT", "BARO_INT"); net(d, bar, "SDO", "GND (addr 0x76)", "left")
        for p, lab in (("SPIM00_SCK", "BHI SCK 20 MHz"), ("SPIM00_MOSI", "BHI SDI"), ("SPIM00_MISO", "BHI SDO"),
                       ("CS_BHI", "BHI CSB"), ("BHI_HIRQ", "BHI HIRQ"), ("BHI_RST_N", "BHI RESETN"),
                       ("TWIM21_SDA", "to BMP390 / FG / DRV2605L"), ("TWIM21_SCL", ""), ("BARO_INT", "")):
            net(d, h, p, lab, "left", 1.0)
        d.add(elm.Label().at((-14, -8)).label(
            "Magnetometer placement: ≥ 15 mm from speaker magnet, LRA, battery tabs and dock magnets; route no high-current loops under U21. "
            "Factory hard/soft-iron calibration stored in hub flash.", fontsize=8.5, halign="left"))
        save(d, "sheet03_sensor_bus")


# ---------------------------------------------------------------------------------- sheet 4
def sheet_audio():
    with schemdraw.Drawing(show=False) as d:
        title(d, (0, 10), "Sheet 4 - Audio: 2x PDM mics, TAS2563 smart amp + 1511 speaker, PMIC codec",
              "Mics 22 mm apart on top/bottom edges for 2-mic beamforming + wind NR; speaker on back cover port (IP67 ePTFE)")
        m1 = ic(d, (0, 4), "MK1 IM73D122 (L)", ["VDD", "SELECT"], ["DATA", "CLK"], w=2.8)
        m2 = ic(d, (0, -1), "MK2 IM73D122 (R)", ["VDD", "SELECT"], ["DATA", "CLK"], w=2.8)
        net(d, m1, "VDD", "1V8_MIC", "left"); net(d, m1, "SELECT", "GND (L ch)", "left")
        net(d, m2, "VDD", "1V8_MIC", "left"); net(d, m2, "SELECT", "VDD (R ch)", "left")
        net(d, m1, "DATA", "PDM_DATA0 → SoC"); net(d, m1, "CLK", "PDM_CLK 2.4 MHz (33R series)")
        net(d, m2, "DATA", "PDM_DATA0 (shared)"); net(d, m2, "CLK", "PDM_CLK")
        a = ic(d, (14, 4), "U30 TAS2563", ["VBAT", "VDD", "SBCLK", "FSYNC", "SDIN", "SDOUT", "SDA", "SCL", "IRQZ", "SDZ"],
               ["OUT_P", "OUT_N", "VBST"], w=3.5)
        for p, lab in (("VBAT", "3V3_SPK/VSYS"), ("VDD", "1V8"), ("SBCLK", "I2S1_BCK ← SoC"), ("FSYNC", "I2S1_LRCK"),
                       ("SDIN", "I2S1_DO"), ("SDOUT", "I2S1_DI (IV-sense echo ref)"), ("SDA", "I2C1_SDA"), ("SCL", "I2C1_SCL"),
                       ("IRQZ", "AMP_IRQ_N"), ("SDZ", "AMP_SD_N")):
            net(d, a, p, lab, "left", 1.2)
        d += elm.Line().at(a.absanchors["OUT_P"]).right(1.5)
        d += elm.Inductor2().right(1.2).label("FB 600R", loc="top")
        d += elm.Speaker().right().anchor("in1").label("LS1 8R 0.5W\n1511 box", loc="right")
        d.add(elm.Label().at((0, -5)).label(
            "Codec path: companion-PMIC codec handles analog sidetone/debug only; production audio is digital (PDM in, I2S out, BT out). "
            "AEC reference = TAS2563 SDOUT.", fontsize=8.5, halign="left"))
        save(d, "sheet04_audio")


# ---------------------------------------------------------------------------------- sheet 5
def sheet_lte():
    with schemdraw.Drawing(show=False) as d:
        title(d, (0, 15), "Sheet 5 - LTE Cat-4 (Quectel EG25-G) + eUICC (Infineon OC1230) + Wi-Fi/BT combo",
              "USB2 HS data (QMI/MBIM), UART for AT/low-power, eUICC on USIM1; aperture tuner on main antenna; RX diversity routed")
        m = ic(d, (0, 4), "U6 Quectel EG25-G",
               ["VBAT_BB", "VBAT_RF", "PWRKEY", "RESET_N", "USB_DP", "USB_DM", "USB_VBUS", "MAIN_RXD", "MAIN_TXD",
                "MAIN_DTR", "MAIN_RI", "STATUS", "W_DISABLE#", "AP_READY"],
               ["ANT_MAIN", "ANT_DIV", "ANT_GNSS (NC)", "USIM_VDD", "USIM_CLK", "USIM_RST", "USIM_DATA", "USIM_PRESENCE",
                "GRFC1", "GRFC2"], w=5)
        for p, lab in (("VBAT_BB", "VBAT_LTE 3.8 V"), ("VBAT_RF", "VBAT_LTE (100uF+33pF+10pF)"),
                       ("PWRKEY", "← Q (SoC LTE_PWRKEY)"), ("RESET_N", "← Q (SoC LTE_RST)"),
                       ("USB_DP", "SoC USB2 port1 DP (90R diff)"), ("USB_DM", "SoC USB2 port1 DM"),
                       ("USB_VBUS", "1V8→detect via GPIO (enables USB suspend)"),
                       ("MAIN_RXD", "SoC UART3_TX (1V8)"), ("MAIN_TXD", "SoC UART3_RX"),
                       ("MAIN_DTR", "SoC GPIO (sleep ctrl)"), ("MAIN_RI", "→ SoC EINT (wake on SMS/data)"),
                       ("STATUS", "→ SoC GPIO"), ("W_DISABLE#", "airplane mode"), ("AP_READY", "← SoC GPIO")):
            net(d, m, p, lab, "left", 1.6)
        net(d, m, "ANT_GNSS (NC)", "NC (GNSS on LC29H)")
        net(d, m, "GRFC1", "→ U11 BGSA14 V1 (tuner)"); net(d, m, "GRFC2", "→ U11 V2")
        net(d, m, "ANT_DIV", "pi-match → ANT_DIV (bottom frame slot)")
        net(d, m, "ANT_MAIN", "pi-match → U11 tuner → frame slot (top)")
        e = ic(d, (25, 4), "U7 OC1230 eUICC", ["VCC", "CLK", "RST", "IO"], ["GND"], w=2.8)
        for p in ("VCC", "CLK", "RST", "IO"):
            net(d, e, p, f"USIM_{'VDD' if p=='VCC' else p if p!='IO' else 'DATA'} (22R + ESD + 33pF)", "left", 0.8)
        w = ic(d, (25, -6), "U8 Wi-Fi6/BT5.4 combo (MT79xx class)",
               ["PCIe/SDIO", "BT_UART", "BT_PCM/I2S", "WL_EN", "BT_EN", "WAKE_HOST"], ["ANT_2G5G", "COEX"], w=4.5)
        net(d, w, "ANT_2G5G", "FEM → diplexer → LDS (side)"); net(d, w, "COEX", "LTE B7/B40/B41 coex ← modem")
        d.add(elm.Label().at((0, -9)).label(
            "eSIM: OC1230 is SGP.22 consumer eUICC; bootstrap profile loaded by connectivity partner at EOL test. "
            "Quectel notes: USB connected blocks sleep → use USB selective suspend + UART for idle; GNSS engine of EG25-G disabled.",
            fontsize=8.5, halign="left"))
        save(d, "sheet05_lte_esim_wireless")


# ---------------------------------------------------------------------------------- sheet 6
def sheet_display_ui():
    with schemdraw.Drawing(show=False) as d:
        title(d, (0, 12), "Sheet 6 - Display, crown, buttons, haptics, secure element",
              "AMOLED 466x466 MIPI-DSI 1-lane (QSPI fallback), on-cell touch on I2C; PAT9125 crown; DRV2605L + LRA")
        lcd = ic(d, (0, 4), "J3 AMOLED FPC 30p (BTB)",
                 ["DSI_CLK_P/N", "DSI_D0_P/N", "TE", "RESX", "VDDI 1V8", "VCI 3V0", "VBAT (ELVDD/ELVSS DC-DC)", "TP_SDA", "TP_SCL", "TP_INT", "TP_RST"],
                 [], w=5)
        for p, lab in (("DSI_CLK_P/N", "SoC DSI0 CLK (100R diff, ≤40 mm)"), ("DSI_D0_P/N", "SoC DSI0 D0"),
                       ("TE", "→ SoC TE (tear sync)"), ("RESX", "← SoC GPIO"), ("VDDI 1V8", "VIO18"),
                       ("VCI 3V0", "3V0 LDO (TLV755P)"), ("VBAT (ELVDD/ELVSS DC-DC)", "VSYS via load switch"),
                       ("TP_SDA", "I2C2_SDA"), ("TP_SCL", "I2C2_SCL"), ("TP_INT", "→ SoC EINT"), ("TP_RST", "← SoC")):
            net(d, lcd, p, lab, "left", 1.2)
        cr = ic(d, (14, 7), "U51 PAT9125EL", ["VDD", "VDDIO", "SDA", "SCL", "MOTION", "PD"], [], w=3)
        for p, lab in (("VDD", "3V0"), ("VDDIO", "1V8_SNS"), ("SDA", "hub TWIM21"), ("SCL", "hub TWIM21"),
                       ("MOTION", "CROWN_MOT → hub"), ("PD", "← hub")):
            net(d, cr, p, lab, "left", 0.9)
        hp = ic(d, (14, 0), "U31 DRV2605L", ["VDD", "SDA", "SCL", "EN", "IN/TRIG"], ["OUT+", "OUT-"], w=3)
        for p, lab in (("VDD", "VSYS"), ("SDA", "hub TWIM21"), ("SCL", "hub"), ("EN", "← hub"), ("IN/TRIG", "← hub PWM")):
            net(d, hp, p, lab, "left", 0.9)
        net(d, hp, "OUT+", "M1 LRA 170 Hz"); net(d, hp, "OUT-", "M1")
        se = ic(d, (26, 6), "U12 SE050E", ["VCC", "SDA", "SCL", "ENA"], [], w=2.6)
        for p, lab in (("VCC", "1V8"), ("SDA", "SoC I2C3 (secure, TZ)"), ("SCL", "I2C3"), ("ENA", "← SoC")):
            net(d, se, p, lab, "left", 0.9)
        d.add(elm.Label().at((14, -5)).label(
            "Buttons: SW1 side (2x=around me), SW2 crown push (talk), SW3 SOS (long-press 3 s, hub-only path; "
            "works with AP crashed). All with 100k PU, 10nF, ESD.", fontsize=8.5, halign="left"))
        save(d, "sheet06_display_ui")


if __name__ == "__main__":
    sheet_power(); sheet_gnss(); sheet_sensors(); sheet_audio(); sheet_lte(); sheet_display_ui()
