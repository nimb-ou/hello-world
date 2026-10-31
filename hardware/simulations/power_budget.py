#!/usr/bin/env python3
"""
LORE power budget & battery-life simulation (SIMULATED - engineering estimates, not measurements)
=================================================================================================
Model: each SKU = set of subsystems; each subsystem has a power (mW, at component rail) per
state. A usage *profile* sets each subsystem's state-occupancy (fraction of time in each state).
Battery-side power = sum(component power) / eta_conv  + PMIC quiescent.

Outputs (this folder):
  power_profiles.png         - continuous-use battery life (h) per SKU per profile
  power_breakdown.png        - stacked mW per subsystem for "narration walking" per SKU
  battery_day_curve.png      - state-of-charge over a simulated multi-day trip
  power_results.json         - all numbers (consumed by results.md)

Key datasheet anchors (others are engineering estimates, labelled E in comments):
  * Quectel LC29H: 24 mA @3.3 V tracking (L1+L5), 0.7 mA standby, 25 uA backup  [Quectel LC29H spec V1.2]
  * Quectel EG25-G: sleep 1.8 mA typ, idle 22 mA                                 [EG25-G LTE Standard Spec V1.6]
  * u-blox NEO-F10N alternate: ~21 mA @3.0 V tracking                            [u-blox NEO-F10N data sheet]
Firmware assumption flags: "baseline" = naive (GNSS always on while walking, A2DP SBC, AP awake
during whole story); "optimised" = GNSS duty-cycled with IMU PDR bridging, LE Audio LC3 where
the earbuds support it, AP suspended between stories with audio buffered (see firmware-interfaces.md).
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK, BONE, TERRA, BRASS, OLIVE, FOG, NIGHT = "#14161A", "#F3EEE6", "#C4623A", "#B8935A", "#5E6B4E", "#9AA0A6", "#0D1B2A"

ETA = 0.88        # aggregate DC/DC + LDO + path efficiency from battery (E)
USABLE = 0.95     # usable fraction of nameplate energy to 3.4 V cutoff (E)
AGED = 0.80       # capacity retention at ~500 cycles (design end-of-life)

SKUS = {
    "Pebble": dict(battery_wh=0.650 * 3.87, pmic_q=0.6,
                   soc=dict(suspend=6, light=160, active=450, llm=2200, vlm=0),   # Genio 520 + 4 GB LPDDR5 (E)
                   lte=None, display=None, camera=False, phone_link=True),
    "Square": dict(battery_wh=1.100 * 3.88, pmic_q=1.0,
                   soc=dict(suspend=7, light=180, active=500, llm=3800, vlm=0),   # Genio 720 + 6 GB (E)
                   lte=dict(off=0, sleep=9.5, rrc=380, stream=550), display=dict(off=0, aod=6, on=90),
                   camera=False, phone_link=False),
    "Atlas": dict(battery_wh=1.450 * 3.88, pmic_q=1.2,
                  soc=dict(suspend=9, light=185, active=520, llm=4200, vlm=4500),  # Genio 720 + 8 GB (E)
                  lte=dict(off=0, sleep=9.5, rrc=380, stream=550), display=dict(off=0, aod=6, on=90),
                  camera=True, phone_link=False),
}
# common subsystems (component-level mW)
GNSS = dict(off=0, backup=0.08, track=24 * 3.3)          # LC29H datasheet
SENS = dict(low=0.6, walk=3.5)                           # BHI360 step/low-power vs 100 Hz 9-axis fusion + baro + nRF54L15 (E)
BT = dict(off=0, idle=0.6, a2dp=25, lc3=12)              # combo-chip BT audio source (E)
PHONE_BLE = dict(idle=0.8, active=6)                      # Pebble BLE GATT link to phone (E)
WIFI = dict(off=0, scan=1.5)                              # Wi-Fi off except opportunistic pack sync (E)
MIC = dict(off=0, on=1.4)                                 # 2x PDM mics + PDM clock (E)
LED = dict(idle=0.2, walk=3.0)                            # Pebble LED ring average (E)
HAPT = dict(idle=0, walk=0.5)
CAM = dict(off=0, glance=650)                             # OV13B10 + ISP active (E)


def profile_power(sku, prof):
    """Return dict subsystem -> average component mW for a profile name."""
    c = SKUS[sku]
    s = c["soc"]
    p = {}
    if prof == "standby":
        p["SoC+DRAM"] = s["suspend"]
        p["Sensors+MCU"] = SENS["low"]
        p["GNSS"] = GNSS["backup"]
        p["BT/BLE"] = BT["idle"] + (PHONE_BLE["idle"] if c["phone_link"] else 0)
        if c["lte"]: p["LTE"] = c["lte"]["sleep"]
        p["LED/haptics"] = LED["idle"] if sku == "Pebble" else 0
    elif prof in ("walk_baseline", "walk_optimised"):
        opt = prof == "walk_optimised"
        ap_duty = 0.15 if opt else 0.60        # AP awake fraction (story render, routing, map-matching)
        p["SoC+DRAM"] = ap_duty * s["light"] + (1 - ap_duty) * s["suspend"]
        p["Sensors+MCU"] = SENS["walk"]
        gnss_duty = 0.40 if opt else 1.0
        p["GNSS"] = gnss_duty * GNSS["track"] + (1 - gnss_duty) * GNSS["backup"]
        story_frac = 0.45                       # fraction of time audio is playing (20-40 s stories + prompts)
        p["BT/BLE"] = BT["idle"] + story_frac * (BT["lc3"] if opt else BT["a2dp"]) + \
            (PHONE_BLE["active"] * 0.3 + PHONE_BLE["idle"] * 0.7 if c["phone_link"] else 0)
        p["Mics"] = 0.05 * MIC["on"]            # press-to-talk only
        if c["lte"]:
            rrc = 0.06 if opt else 0.12         # RRC-connected fraction for live data / prefetch
            p["LTE"] = rrc * c["lte"]["rrc"] + (1 - rrc) * c["lte"]["sleep"]
        if c["display"]:
            p["Display"] = 0.06 * c["display"]["on"]   # glances ~3.5 min per hour
        p["LED/haptics"] = (LED["walk"] if sku == "Pebble" else 0) + HAPT["walk"]
    elif prof == "lte_stream":                  # continuous cloud-AI conversation
        p["SoC+DRAM"] = s["active"]
        p["Sensors+MCU"] = SENS["walk"]
        p["GNSS"] = 0.4 * GNSS["track"]
        p["BT/BLE"] = BT["a2dp"] + (PHONE_BLE["active"] if c["phone_link"] else 0)
        p["Mics"] = MIC["on"]
        if c["lte"]:
            p["LTE"] = c["lte"]["stream"]
        if c["display"]:
            p["Display"] = 0.2 * c["display"]["on"]
    elif prof == "llm_sustained":               # back-to-back on-device LLM (thermal-limited in practice)
        p["SoC+DRAM"] = s["llm"]
        p["Sensors+MCU"] = SENS["walk"]
        p["BT/BLE"] = BT["a2dp"] * 0.5
        p["Mics"] = MIC["on"] * 0.3
        if c["lte"]: p["LTE"] = c["lte"]["sleep"]
        if c["display"]: p["Display"] = 0.3 * c["display"]["on"]
    elif prof == "nav_gnss":                    # turn-by-turn, GNSS continuous, screen on 25 %
        p["SoC+DRAM"] = 0.35 * s["light"] + 0.65 * s["suspend"]
        p["Sensors+MCU"] = SENS["walk"]
        p["GNSS"] = GNSS["track"]
        p["BT/BLE"] = BT["idle"] + 0.15 * BT["a2dp"] + (PHONE_BLE["idle"] if c["phone_link"] else 0)
        if c["lte"]: p["LTE"] = 0.05 * c["lte"]["rrc"] + 0.95 * c["lte"]["sleep"]
        if c["display"]: p["Display"] = 0.25 * c["display"]["on"]
    return p


def battery_mw(sku, comp):
    return sum(comp.values()) / ETA + SKUS[sku]["pmic_q"]


PROFILES = ["standby", "walk_baseline", "walk_optimised", "nav_gnss", "lte_stream", "llm_sustained"]
PLABEL = {"standby": "Standby (pocket, connected)", "walk_baseline": "Narration walk - baseline FW",
          "walk_optimised": "Narration walk - optimised FW", "nav_gnss": "Navigation, GNSS continuous",
          "lte_stream": "Cloud-AI conversation (LTE/BLE)", "llm_sustained": "On-device LLM sustained"}


def trip_day(sku, optimised=True):
    """Return list of (hours, battery mW) segments for one 24 h travel day (SIMULATED)."""
    c = SKUS[sku]
    walk = battery_mw(sku, profile_power(sku, "walk_optimised" if optimised else "walk_baseline"))
    stby = battery_mw(sku, profile_power(sku, "standby"))
    stream = battery_mw(sku, profile_power(sku, "lte_stream"))
    llm = battery_mw(sku, profile_power(sku, "llm_sustained"))
    # 6 h narration walking, 20 min cloud conversation, 40 on-device LLM answers x 6 s (+2 s prefill),
    # Atlas: 15 Glance captures (2 s camera + 3 s VLM). Remainder standby.
    segs = [("standby_night", 7.0, stby), ("walk_am", 3.0, walk), ("stream", 1 / 3, stream),
            ("llm", 40 * 8 / 3600, llm)]
    if c["camera"]:
        vlm_mw = (CAM["glance"] + c["soc"]["vlm"]) / ETA
        segs.append(("glance", 15 * 5 / 3600, vlm_mw))
    segs += [("walk_pm", 3.0, walk)]
    used = sum(h for _, h, _ in segs)
    segs.append(("standby_eve", 24 - used, stby))
    return segs


def main():
    res = {}
    for sku in SKUS:
        e_new = SKUS[sku]["battery_wh"] * USABLE * 1000      # mWh
        r = {"battery_wh": round(SKUS[sku]["battery_wh"], 2), "profiles": {}}
        for prof in PROFILES:
            comp = profile_power(sku, prof)
            mw = battery_mw(sku, comp)
            r["profiles"][prof] = dict(battery_mw=round(mw, 1), hours_new=round(e_new / mw, 1),
                                       hours_aged=round(e_new * AGED / mw, 1),
                                       breakdown={k: round(v / ETA, 2) for k, v in comp.items()})
        for opt in (False, True):
            segs = trip_day(sku, opt)
            mwh_day = sum(h * mw for _, h, mw in segs)
            key = "trip_day_optimised" if opt else "trip_day_baseline"
            r[key] = dict(mwh_per_day=round(mwh_day, 0), days_new=round(e_new / mwh_day, 2),
                          days_aged=round(e_new * AGED / mwh_day, 2),
                          hours_new=round(24 * e_new / mwh_day, 1))
        res[sku] = r

    with open(os.path.join(HERE, "power_results.json"), "w") as f:
        json.dump(res, f, indent=1)

    # --- chart 1: continuous-use hours
    fig, ax = plt.subplots(figsize=(11, 5.5))
    w = 0.26
    x = np.arange(len(PROFILES))
    for i, (sku, col) in enumerate(zip(SKUS, [TERRA, INK, OLIVE])):
        hrs = [res[sku]["profiles"][p]["hours_new"] for p in PROFILES]
        bars = ax.bar(x + (i - 1) * w, hrs, w, color=col, label=f"{sku} ({res[sku]['battery_wh']} Wh)")
        for b_, h in zip(bars, hrs):
            ax.text(b_.get_x() + b_.get_width() / 2, h * 1.05, f"{h:.0f}" if h >= 10 else f"{h:.1f}",
                    ha="center", fontsize=7)
    ax.set_yscale("log")
    ax.set_xticks(x); ax.set_xticklabels([PLABEL[p] for p in PROFILES], rotation=15, ha="right", fontsize=8)
    ax.set_ylabel("Hours of continuous use (new cell, log scale)")
    ax.set_title("SIMULATED battery life per usage profile (estimates; see power_budget.py)")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "power_profiles.png"), dpi=150)

    # --- chart 2: breakdown for walking (baseline vs optimised)
    subs = ["SoC+DRAM", "GNSS", "LTE", "BT/BLE", "Display", "Sensors+MCU", "Mics", "LED/haptics"]
    cols = [INK, TERRA, NIGHT, BRASS, OLIVE, FOG, "#D8A48F", "#8C9A7A"]
    fig, ax = plt.subplots(figsize=(10, 5))
    labels, bottoms = [], []
    cats = [(s, p) for s in SKUS for p in ("walk_baseline", "walk_optimised")]
    bottom = np.zeros(len(cats))
    for sub, col in zip(subs, cols):
        v = np.array([res[s]["profiles"][p]["breakdown"].get(sub, 0) for s, p in cats])
        ax.bar(range(len(cats)), v, bottom=bottom, color=col, label=sub, edgecolor="white", linewidth=0.5)
        bottom += v
    for i, (s, p) in enumerate(cats):
        ax.text(i, bottom[i] + 4, f"{res[s]['profiles'][p]['battery_mw']:.0f} mW", ha="center", fontsize=8)
    ax.set_xticks(range(len(cats)))
    ax.set_xticklabels([f"{s}\n{'baseline' if 'base' in p else 'optimised'}" for s, p in cats], fontsize=8)
    ax.set_ylabel("Battery-side power, mW")
    ax.set_title("Narration-walking power breakdown (SIMULATED)")
    ax.legend(ncol=4, fontsize=8, frameon=False)
    ax.set_ylim(0, bottom.max() * 1.3)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "power_breakdown.png"), dpi=150)

    # --- chart 3: state-of-charge over a trip
    fig, ax = plt.subplots(figsize=(10, 5))
    targets = {"Pebble": 36, "Square": 48, "Atlas": 72}
    for sku, col in zip(SKUS, [TERRA, INK, OLIVE]):
        for opt, ls in ((True, "-"), (False, ":")):
            e = SKUS[sku]["battery_wh"] * USABLE * 1000
            t, soc = [0.0], [100.0]
            day = trip_day(sku, opt)
            while soc[-1] > 0 and t[-1] < 24 * 5:
                for _, h, mw in day:
                    n = max(2, int(h * 12))
                    for _ in range(n):
                        dt = h / n
                        t.append(t[-1] + dt)
                        soc.append(soc[-1] - 100 * mw * dt / e)
                        if soc[-1] <= 0:
                            break
                    if soc[-1] <= 0:
                        break
            soc = np.clip(soc, 0, 100)
            ax.plot(t, soc, ls, color=col, label=f"{sku} {'optimised' if opt else 'baseline'} FW")
        ax.axvline(targets[sku], color=col, alpha=0.25, lw=6)
    ax.set_xlabel("Hours from full charge (day starts 00:00; 6 h walking/day)")
    ax.set_ylabel("Usable state of charge, %")
    ax.set_title("SIMULATED multi-day trip: SoC vs time (shaded = COMPANY.md target per SKU)")
    ax.set_xlim(0, 96); ax.set_ylim(0, 102)
    ax.legend(fontsize=8, frameon=False)
    ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "battery_day_curve.png"), dpi=150)

    for sku in SKUS:
        r = res[sku]
        print(sku, {p: (r["profiles"][p]["battery_mw"], r["profiles"][p]["hours_new"]) for p in PROFILES})
        print("   trip day baseline:", r["trip_day_baseline"], "\n   optimised:", r["trip_day_optimised"])


if __name__ == "__main__":
    main()
