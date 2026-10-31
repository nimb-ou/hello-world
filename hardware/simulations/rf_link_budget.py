#!/usr/bin/env python3
"""
RF link budgets for LTE / GNSS / Bluetooth / NTN in small metal bodies (SIMULATED / estimates)
=============================================================================================
Antenna efficiencies are engineering estimates for a 54 mm device with frame-slot or LDS
antennas; they MUST be replaced by OTA chamber data (CTIA TRP/TIS) at EVT.
Outputs: rf_link_budget.png, rf_results.json
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK, TERRA, BRASS, OLIVE, FOG, NIGHT = "#14161A", "#C4623A", "#B8935A", "#5E6B4E", "#9AA0A6", "#0D1B2A"


def fspl(d_m, f_hz):
    return 20 * np.log10(d_m) + 20 * np.log10(f_hz) - 147.55


# Antenna realised gain (dBi, avg incl. mismatch) per body / band (E)
ANT = {
    "Phone reference":       dict(lte_low=-4, lte_mid=-2, gnss=-3, bt=-2, ntn=-3),
    "Pebble (PC-GF)":        dict(lte_low=None, lte_mid=None, gnss=-5, bt=-3, ntn=None),
    "Square (Al + NMT splits)": dict(lte_low=-8, lte_mid=-5, gnss=-7, bt=-4, ntn=None),
    "Atlas (Ti + ceramic back)": dict(lte_low=-9, lte_mid=-6, gnss=-8, bt=-5, ntn=-6),
}
BODY = dict(lte=4.0, gnss=3.0, bt=12.0, ntn=3.0)   # body/clip loss dB (worn on chest/strap) (E)


def lte_mapl(g):
    # Uplink-limited MAPL, 64 kbps voice-class, 2 PRB; eNB NF 2 dB, required SINR -2 dB, 2RX, interference margin 3 dB
    ue_tx = 23.0
    enb_sens = -174 + 10 * np.log10(2 * 180e3) + 2 - 2 - 3   # dBm
    return ue_tx + g - BODY["lte"] - enb_sens - 3


def gnss_cn0(g, p_min_dbm, nf=2.0):
    return p_min_dbm + 174 + g - nf - BODY["gnss"]


def bt_margin(g_tx, tx=8.0, d=1.0, rx_sens=-92.0, g_rx=-8.0):
    return tx + g_tx - fspl(d, 2.44e9) - BODY["bt"] + g_rx - rx_sens


def ntn_cn0(g):
    # GEO L-band uplink 1.64 GHz, slant 38,000 km, UE 23 dBm, satellite G/T +10 dB/K (large GEO reflector) (E)
    eirp_dbw = 23 + g - BODY["ntn"] - 30
    return eirp_dbw - fspl(38_000e3, 1.64e9) + 10.0 + 228.6


def main():
    res = {}
    for dev, a in ANT.items():
        r = {}
        if a["lte_low"] is not None:
            r["LTE_MAPL_low_band_dB"] = round(lte_mapl(a["lte_low"]), 1)
            r["LTE_MAPL_mid_band_dB"] = round(lte_mapl(a["lte_mid"]), 1)
        r["GNSS_L1_CN0_dBHz_open_sky_min_signal"] = round(gnss_cn0(a["gnss"], -128.5), 1)
        r["GNSS_L5_CN0_dBHz_open_sky_min_signal"] = round(gnss_cn0(a["gnss"] - 0.5, -127.9), 1)
        r["BT_to_earbud_margin_dB_1m_through_body"] = round(bt_margin(a["bt"]), 1)
        if a["ntn"] is not None:
            r["NTN_uplink_CN0_dBHz"] = round(ntn_cn0(a["ntn"]), 1)
        res[dev] = r
    ref = res["Phone reference"]["LTE_MAPL_low_band_dB"]
    for dev in ("Square (Al + NMT splits)", "Atlas (Ti + ceramic back)"):
        delta = ref - res[dev]["LTE_MAPL_low_band_dB"]
        res[dev]["LTE_low_band_cell_range_vs_phone"] = round(10 ** (-delta / 35), 2)   # path-loss exponent 3.5
    res["thresholds"] = dict(GNSS_tracking_dBHz=28, GNSS_acquisition_dBHz=33,
                             NTN_single_tone_3k75_0dB_SNR_dBHz=round(10 * np.log10(3750), 1),
                             BT_margin_target_dB=15)
    with open(os.path.join(HERE, "rf_results.json"), "w") as f:
        json.dump(res, f, indent=1)

    devs = list(ANT)
    fig, ax = plt.subplots(1, 3, figsize=(14, 4.3))
    cols = [FOG, TERRA, INK, OLIVE]
    v = [res[d].get("LTE_MAPL_low_band_dB", 0) for d in devs]
    ax[0].bar(range(4), v, color=cols); ax[0].set_ylim(120, 150); ax[0].set_title("LTE uplink MAPL, low band (dB)")
    v = [res[d]["GNSS_L1_CN0_dBHz_open_sky_min_signal"] for d in devs]
    ax[1].bar(range(4), v, color=cols); ax[1].axhline(28, ls="--", color=INK, lw=0.8); ax[1].axhline(33, ls=":", color=INK, lw=0.8)
    ax[1].set_ylim(20, 42); ax[1].set_title("GNSS L1 C/N0 @ min signal, worn (dB-Hz)\n-- tracking 28, .. acquisition 33")
    v = [res[d]["BT_to_earbud_margin_dB_1m_through_body"] for d in devs]
    ax[2].bar(range(4), v, color=cols); ax[2].axhline(15, ls="--", color=INK, lw=0.8); ax[2].set_title("BT link margin to earbud (dB)")
    for a_ in ax:
        a_.set_xticks(range(4)); a_.set_xticklabels([d.split(" (")[0] for d in devs], fontsize=8)
        a_.spines[["top", "right"]].set_visible(False)
    fig.suptitle("SIMULATED link budgets (antenna gains are estimates pending OTA chamber data)", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "rf_link_budget.png"), dpi=150)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
