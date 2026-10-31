#!/usr/bin/env python3
"""
Thermal estimate for sustained on-device LLM in a 54x54x12 mm enclosure (SIMULATED, lumped model)
==================================================================================================
3-node RC network:  SoC junction  ->  internal (PCB + battery + mid-frame)  ->  shell  ->  ambient
  * Junction->internal: R_jc + spreading through graphite/Cu foil/vapour-chamber-lite   (E)
  * Internal->shell: TIM gel + air gaps                                                  (E)
  * Shell->ambient: natural convection + radiation over the exposed area, with a
    usage-condition factor (open air on a lanyard / in hand / in a pocket).
A skin-temperature governor caps SoC power when the shell exceeds the touch limit
(43 C for long-duration body contact; IEC 62368-1 TS1-class limits - estimate, verify with
safety lab), mirroring a Linux thermal-zone + NPU DVFS policy.

Outputs: thermal_llm.png, thermal_results.json
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
INK, TERRA, BRASS, OLIVE, FOG, NIGHT = "#14161A", "#C4623A", "#B8935A", "#5E6B4E", "#9AA0A6", "#0D1B2A"
SIGMA = 5.67e-8

DEV = {
    #           area m^2 (outer)          emissivity  C_int J/K  C_shell J/K  R_ji  R_is (K/W)
    "Square (Al, 54x54x12)":  dict(A=2 * .054 * .054 + 4 * .054 * .012, eps=0.85, Ci=38, Cs=22, Rji=6.0, Ris=2.5,
                                   llm_w=4.3, rest_w=0.35),
    "Atlas (Ti, 54x54x13.5)": dict(A=2 * .054 * .054 + 4 * .054 * .0135, eps=0.55, Ci=45, Cs=30, Rji=5.0, Ris=3.0,
                                   llm_w=4.7, rest_w=0.38),
    "Pebble (PC-GF, 42x42x14)": dict(A=2 * .042 * .042 + 4 * .042 * .014, eps=0.9, Ci=20, Cs=9, Rji=7.0, Ris=4.5,
                                     llm_w=2.5, rest_w=0.25),
}
COND = {"open air / lanyard": 1.0, "held in hand": 0.8, "in jacket pocket": 0.45}
H_NAT = 9.0          # W/m2K natural convection, small body (E)
T_SKIN = 43.0
T_J_MAX = 95.0


def h_total(Ts, Ta, eps, cond):
    Tk, Tak = Ts + 273.15, Ta + 273.15
    hr = eps * SIGMA * (Tk ** 2 + Tak ** 2) * (Tk + Tak)
    return (H_NAT + hr) * cond


def simulate(d, cond, Ta, p_fn, t_end=1800, dt=0.5, governor=True):
    n = int(t_end / dt)
    Tj = Ti = Ts = Ta
    out = np.zeros((n, 5))
    cap = 99.0
    for k in range(n):
        t = k * dt
        p_req = p_fn(t, d)
        if governor and Ts > T_SKIN - 1.0:
            cap = max(0.3, cap - 0.02 * dt * 10)   # step NPU/CPU OPP down
        elif governor and Ts < T_SKIN - 2.0:
            cap = min(99.0, cap + 0.01 * dt * 10)
        p = min(p_req, cap) if governor else p_req
        if Tj > T_J_MAX:
            p = min(p, 1.0)
        qji = (Tj - Ti) / d["Rji"]
        qis = (Ti - Ts) / d["Ris"]
        qsa = h_total(Ts, Ta, d["eps"], cond) * d["A"] * (Ts - Ta)
        Tj += dt * (p - qji) / 2.0           # junction + package ~2 J/K
        Ti += dt * (qji - qis) / d["Ci"]
        Ts += dt * (qis - qsa) / d["Cs"]
        out[k] = (t, Tj, Ti, Ts, p)
    return out


def sustainable_power(d, cond, Ta):
    """Steady-state power that holds the shell at T_SKIN."""
    return h_total(T_SKIN, Ta, d["eps"], cond) * d["A"] * (T_SKIN - Ta)


def main():
    res = {}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True)
    sustained = lambda t, d: d["llm_w"]
    bursty = lambda t, d: d["llm_w"] if (t % 60) < 8 else d["rest_w"]           # 8 s answer every minute
    convo = lambda t, d: d["llm_w"] if (t % 20) < 10 else d["rest_w"] + 0.9      # dense conversation, 50 % duty
    for ax, (name, d) in zip(axes, DEV.items()):
        r = {}
        for cond_name, cf in COND.items():
            r[cond_name] = dict(sustainable_w_25C=round(sustainable_power(d, cf, 25), 2),
                                sustainable_w_35C=round(sustainable_power(d, cf, 35), 2))
        for label, fn, col in (("sustained LLM", sustained, TERRA), ("dense conversation 50 %", convo, BRASS),
                               ("burst 8 s / 60 s", bursty, OLIVE)):
            o = simulate(d, 1.0, 25, fn)
            ug = simulate(d, 1.0, 25, fn, governor=False)
            t_hit = next((row[0] for row in ug if row[3] >= T_SKIN), None)
            r[label] = dict(max_shell_C_no_gov=round(float(ug[:, 3].max()), 1),
                            time_to_43C_s_no_gov=None if t_hit is None else round(float(t_hit)),
                            avg_power_with_gov_last10min=round(float(o[-1200:, 4].mean()), 2),
                            max_junction_C=round(float(o[:, 1].max()), 1))
            ax.plot(o[:, 0] / 60, o[:, 3], color=col, label=f"shell, {label} (governed)")
            ax.plot(ug[:, 0] / 60, ug[:, 3], ":", color=col, alpha=0.7)
        ax.axhline(T_SKIN, color=INK, lw=0.8, ls="--")
        ax.text(0.5, T_SKIN + 0.5, "43 C skin limit", fontsize=7)
        ax.set_title(f"{name}\nLLM {d['llm_w']} W, 25 C ambient, open air", fontsize=9)
        ax.set_xlabel("Minutes"); ax.grid(alpha=0.3)
        res[name] = r
    axes[0].set_ylabel("Shell temperature, C  (dotted = no governor)")
    axes[0].legend(fontsize=7, frameon=False, loc="lower right")
    fig.suptitle("SIMULATED lumped thermal model - on-device LLM", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "thermal_llm.png"), dpi=150)

    # decode-rate estimate (bandwidth-bound) and governed sustained rate
    bw = 25.6e9 * 0.6        # LPDDR5-6400 x32, 60 % achievable for decode (E)
    models = {"1B INT4 (~0.65 GB)": 0.65e9, "3B INT4 (~1.75 GB)": 1.75e9, "4B INT4 (~2.3 GB)": 2.3e9}
    res["decode_estimate_tok_s"] = {m: round(bw / b, 1) for m, b in models.items()}
    sq = DEV["Square (Al, 54x54x12)"]
    frac = sustainable_power(sq, 1.0, 25) / sq["llm_w"]
    res["square_3B_sustained_tok_s_open_air_25C"] = round(bw / models["3B INT4 (~1.75 GB)"] * min(1, frac), 1)
    with open(os.path.join(HERE, "thermal_results.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
