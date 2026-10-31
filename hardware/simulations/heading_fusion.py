#!/usr/bin/env python3
"""
Map Vision heading fusion - Monte-Carlo simulation (ALL DATA SIMULATED)
======================================================================
Question: can LORE reliably say "on your LEFT / RIGHT" in a dense historic city where the
magnetometer is disturbed (steel, tram lines, parked cars, rebar) and GNSS suffers multipath?

Simulated world
  * Pedestrian route of ~2 km through an irregular street network (Rome-like: 40-160 m blocks,
    90 deg and 25-60 deg turns), 1.35 m/s, 1.8 steps/s, stops at crossings.
  * Device clipped to a bag strap / pocket: unknown mounting yaw offset alpha (U(-35, 35) deg)
    plus body sway (+/-4 deg at half the step frequency).
  * Gyro (BHI360-class): 25 Hz, white noise 0.15 deg/s, initial bias N(0, 0.4 deg/s), bias RW.
  * Magnetometer (BMM350-class): Earth horizontal field 25 uT (Rome), noise 0.3 uT,
    hard-iron residual 1.5 uT, plus spatial disturbance patches (every ~35 m, 3-15 m wide,
    up to ~15 uT) -> heading errors of tens of degrees near ironwork/cars/trams.
  * GNSS @1 Hz: Gauss-Markov position error + urban-canyon multipath bias in canyon segments;
    Doppler velocity noise. Two receivers: L1+L5 (LC29H-class) and L1-only.

Estimators compared (walking heading = device heading - alpha)
  A  Raw compass (given the TRUE mounting offset - i.e. idealised) + raw GNSS position
  B  GNSS course-over-ground only + raw GNSS position
  C  Complementary filter (gyro + mag, tau 2 s) + learned offset + raw GNSS position
  D  EKF [psi, gyro bias, alpha]: gyro propagation, |B|-norm + chi^2-gated mag updates,
     GNSS course updates; position = PDR + GNSS Kalman with outlier gating
  E  D + map-matching (snap to street centreline from City Pack geometry; heading aligned
     to street bearing when within 30 deg) - this is what Map Vision ships
  D/E are also run with L1-only GNSS to quantify the value of L5.

Outputs: heading_fusion_trace.png, heading_fusion_accuracy.png, heading_error_cdf.png,
         heading_results.json
Run: python3 heading_fusion.py  [~1-2 min]
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
D2R, R2D = np.pi / 180, 180 / np.pi
FS = 25.0
DT = 1 / FS
H_EARTH = 25.0  # uT horizontal, Rome (approx.)
INK, TERRA, BRASS, OLIVE, FOG, NIGHT = "#14161A", "#C4623A", "#B8935A", "#5E6B4E", "#9AA0A6", "#0D1B2A"


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


# ------------------------------------------------------------------------------------------ world
def make_route(rng, total=2000.0):
    pts = [np.array([0.0, 0.0])]
    hdg = rng.uniform(0, 2 * np.pi)
    canyon = []
    L = 0
    while L < total:
        seg = rng.uniform(40, 160)
        p = pts[-1] + seg * np.array([np.sin(hdg), np.cos(hdg)])  # x=East, y=North, heading from North
        pts.append(p)
        canyon.append(rng.random() < 0.45)        # narrow street with tall facades
        L += seg
        turn = rng.choice([-1, 1]) * (np.pi / 2 if rng.random() < 0.6 else rng.uniform(25, 60) * D2R)
        hdg = wrap(hdg + turn)
    return np.array(pts), np.array(canyon)


def walk(route, rng, v=1.35):
    """True trajectory sampled at FS: positions, walking heading, along-track s, segment index."""
    seg_vec = np.diff(route, axis=0)
    seg_len = np.linalg.norm(seg_vec, axis=1)
    seg_hdg = np.arctan2(seg_vec[:, 0], seg_vec[:, 1])
    cum = np.concatenate([[0], np.cumsum(seg_len)])
    pos, hdg, sidx, sarr, moving = [], [], [], [], []
    s, t = 0.0, 0.0
    stop_until = -1
    next_stop = rng.uniform(150, 400)
    psi = seg_hdg[0]
    while s < cum[-1] - 0.01:
        k = min(np.searchsorted(cum, s, side="right") - 1, len(seg_len) - 1)
        mv = t >= stop_until
        if mv and s > next_stop:            # stop at a crossing
            stop_until = t + rng.uniform(5, 25)
            next_stop = s + rng.uniform(150, 400)
            mv = False
        target = seg_hdg[k]
        # smooth turn: heading slews at max 90 deg/s toward segment bearing
        d = wrap(target - psi)
        psi = wrap(psi + np.clip(d, -np.pi / 2 * DT, np.pi / 2 * DT))
        if mv:
            s += v * DT
        frac = (s - cum[k]) / seg_len[k]
        pos.append(route[k] + frac * seg_vec[k])
        hdg.append(psi); sidx.append(k); sarr.append(s); moving.append(mv)
        t += DT
    return dict(pos=np.array(pos), hdg=np.array(hdg), seg=np.array(sidx), s=np.array(sarr),
                moving=np.array(moving), seg_hdg=seg_hdg, cum=cum, seg_len=seg_len)


def mag_disturbance_field(rng, route_len):
    """Spatial patches along track: centre s, width, 2-D disturbance vector (uT, world frame)."""
    n = int(route_len / 35)
    c = np.sort(rng.uniform(0, route_len, n))
    w = rng.uniform(3, 15, n)
    amp = rng.gamma(2.0, 3.5, n)                       # median ~6 uT, tail to ~20 uT
    ang = rng.uniform(0, 2 * np.pi, n)
    return c, w, amp, ang


def disturbance_at(s, field):
    c, w, amp, ang = field
    g = amp[None, :] * np.exp(-0.5 * ((s[:, None] - c[None, :]) / w[None, :]) ** 2)
    return np.stack([(g * np.sin(ang)).sum(1), (g * np.cos(ang)).sum(1)], 1)


# ------------------------------------------------------------------------------------------ sensors
def sensors(tr, rng, l5=True):
    n = len(tr["hdg"])
    t = np.arange(n) * DT
    alpha = rng.uniform(-35, 35) * D2R
    step_f = 1.8
    sway = 4 * D2R * np.sin(2 * np.pi * step_f / 2 * t + rng.uniform(0, 6.28)) * tr["moving"]
    psi_dev = wrap(tr["hdg"] + alpha + sway)
    # gyro
    bias0 = rng.normal(0, 0.4) * D2R
    bias = bias0 + np.cumsum(rng.normal(0, 0.002 * D2R, n))
    omega_true = np.concatenate([[0], wrap(np.diff(psi_dev)) / DT])
    gyro = omega_true + bias + rng.normal(0, 0.15 * D2R, n)
    # magnetometer (horizontal components in device frame)
    field = mag_disturbance_field(rng, tr["s"][-1] + 10)
    B = np.stack([np.zeros(n), np.full(n, H_EARTH)], 1) + disturbance_at(tr["s"], field)
    c, s_ = np.cos(psi_dev), np.sin(psi_dev)
    # rotate world (E,N) into device (fwd=y_dev, right=x_dev): heading psi measured clockwise from N
    bx = c * B[:, 0] - s_ * B[:, 1]
    by = s_ * B[:, 0] + c * B[:, 1]
    hi = rng.normal(0, 1.5, 2)
    bx += hi[0] + rng.normal(0, 0.3, n)
    by += hi[1] + rng.normal(0, 0.3, n)
    psi_mag = wrap(np.arctan2(-bx, by))
    bnorm = np.hypot(bx, by)
    # GNSS 1 Hz
    k1 = np.arange(0, n, int(FS))
    sig_gm, sig_mp, sig_v = (2.0, 5.0, 0.10) if l5 else (3.5, 11.0, 0.18)
    gm = np.zeros((len(k1), 2))
    for i in range(1, len(k1)):
        gm[i] = gm[i - 1] * np.exp(-1 / 30) + rng.normal(0, sig_gm * np.sqrt(1 - np.exp(-2 / 30)), 2)
    canyon = tr["canyon"][tr["seg"][k1]]
    seg_h = tr["seg_hdg"][tr["seg"][k1]]
    perp = np.stack([np.cos(seg_h), -np.sin(seg_h)], 1)
    mp = np.zeros(len(k1))
    for i in range(1, len(k1)):   # slowly varying lateral multipath bias in canyons
        mp[i] = 0.9 * mp[i - 1] + rng.normal(0, sig_mp * 0.44)
    gpos = tr["pos"][k1] + gm + (canyon * mp)[:, None] * perp
    vel_true = np.stack([np.sin(tr["hdg"][k1]), np.cos(tr["hdg"][k1])], 1) * 1.35 * tr["moving"][k1, None]
    gvel = vel_true + rng.normal(0, 1, (len(k1), 2)) * sig_v * (1 + 1.5 * canyon)[:, None]
    return dict(alpha=alpha, gyro=gyro, psi_mag=psi_mag, bnorm=bnorm, k1=k1, gpos=gpos, gvel=gvel,
                psi_dev=psi_dev, canyon_g=canyon)


# ------------------------------------------------------------------------------------------ estimators
def run_estimators(tr, se, rng, map_match_route):
    n = len(tr["hdg"])
    k1set = {k: i for i, k in enumerate(se["k1"])}
    # A raw compass with true alpha
    hA = wrap(se["psi_mag"] - se["alpha"])
    # B GNSS course (held between fixes, held when slow)
    hB = np.zeros(n); last = se["psi_mag"][0] - se["alpha"]
    # C complementary
    hC = np.zeros(n); psi_c = se["psi_mag"][0]; alpha_c = 0.0
    # D EKF
    x = np.array([se["psi_mag"][0], 0.0, 0.0])
    P = np.diag([(30 * D2R) ** 2, (0.5 * D2R) ** 2, (40 * D2R) ** 2])
    Q = np.diag([(0.15 * D2R) ** 2 * DT, (0.002 * D2R) ** 2, (0.01 * D2R) ** 2 * DT])
    hD = np.zeros(n)
    # position filters
    gpos_hold = se["gpos"][0].copy()
    posA = np.zeros((n, 2)); posD = np.zeros((n, 2)); posE = np.zeros((n, 2)); hE = np.zeros(n)
    p = se["gpos"][0].copy(); Pp = np.eye(2) * 25
    step_phase = 0.0
    mag_rej = 0; mag_tot = 0
    for k in range(n):
        w = se["gyro"][k]
        # --- C
        psi_c = wrap(psi_c + w * DT)
        if k % 5 == 0:
            psi_c = wrap(psi_c + (DT * 5 / 2.0) * wrap(se["psi_mag"][k] - psi_c))
        # --- D predict
        x[0] = wrap(x[0] + (w - x[1]) * DT)
        F = np.array([[1, -DT, 0], [0, 1, 0], [0, 0, 1]])
        P = F @ P @ F.T + Q
        # mag update @5 Hz with norm + chi2 gating
        if k % 5 == 0:
            mag_tot += 1
            Hm = np.array([1.0, 0, 0])
            yv = wrap(se["psi_mag"][k] - x[0])
            Rm = (5 * D2R) ** 2
            S = Hm @ P @ Hm + Rm
            if abs(se["bnorm"][k] - H_EARTH) < 2.5 and yv * yv / S < 6.6:
                K = P @ Hm / S
                x = x + K * yv; x[0] = wrap(x[0]); P = P - np.outer(K, Hm) @ P
            else:
                mag_rej += 1
        if k in k1set:
            i = k1set[k]
            v = se["gvel"][i]; spd = np.hypot(*v)
            course = np.arctan2(v[0], v[1])
            if spd > 0.8:
                last = course
                # C: learn mounting offset slowly
                alpha_c = wrap(alpha_c + 0.05 * wrap(psi_c - alpha_c - course))
                if abs(w) < 15 * D2R:
                    Hg = np.array([1.0, 0, -1.0])
                    yv = wrap(course - (x[0] - x[2]))
                    Rg = (se_sig_course(spd, se["canyon_g"][i])) ** 2
                    S = Hg @ P @ Hg + Rg
                    if yv * yv / S < 9:
                        K = P @ Hg / S
                        x = x + K * yv; x[0] = wrap(x[0]); x[2] = wrap(x[2]); P = P - np.outer(K, Hg) @ P
            gpos_hold = se["gpos"][i]
            # position KF GNSS update with gating
            yv = se["gpos"][i] - p
            Rp = np.eye(2) * (3.0 if True else 6.0) ** 2
            S = Pp + Rp
            d2 = yv @ np.linalg.solve(S, yv)
            if d2 < 13.8:
                K = Pp @ np.linalg.inv(S)
                p = p + K @ yv; Pp = (np.eye(2) - K) @ Pp
        hB[k] = last
        hC[k] = wrap(psi_c - alpha_c)
        hD[k] = wrap(x[0] - x[2])
        # PDR propagation on steps
        if tr["moving"][k]:
            step_phase += 1.8 * DT
            if step_phase >= 1:
                step_phase -= 1
                L = 0.75 * (1 + rng.normal(0, 0.05))
                p = p + L * np.array([np.sin(hD[k]), np.cos(hD[k])])
                Pp = Pp + np.eye(2) * 0.15 ** 2
        posA[k] = gpos_hold
        posD[k] = p
        # E map matching
        if k % 5 == 0:
            pe, he_off = map_match(p, hD[k], map_match_route)
            he_off = wrap(he_off - hD[k])
        posE[k] = pe; hE[k] = wrap(hD[k] + he_off)
    return dict(A=(hA, posA), B=(hB, posA), C=(hC, posA), D=(hD, posD), E=(hE, posE),
                mag_reject_rate=mag_rej / max(mag_tot, 1))


def se_sig_course(spd, canyon):
    return max(np.arctan2(0.10 * (1 + 1.5 * canyon), spd), 3 * D2R) * 1.5


def map_match(p, h, mm):
    A, B, segh = mm
    AB = B - A
    t = np.clip(((p - A) * AB).sum(1) / (AB * AB).sum(1), 0, 1)
    proj = A + t[:, None] * AB
    d = np.linalg.norm(proj - p, axis=1)
    # prefer segments whose bearing agrees with heading (either direction)
    ang = np.abs(wrap(segh - h))
    ang = np.minimum(ang, np.pi - ang)
    cost = d + 25 * (ang > 45 * D2R)
    j = np.argmin(cost)
    he = h
    dd = wrap(segh[j] - h)
    if abs(dd) < 30 * D2R:
        he = segh[j]
    elif abs(wrap(segh[j] + np.pi - h)) < 30 * D2R:
        he = wrap(segh[j] + np.pi)
    return proj[j], he


# ------------------------------------------------------------------------------------------ POIs & scoring
def make_pois(tr, rng):
    pois = []
    for k, L in enumerate(tr["seg_len"]):
        n = int(L // 22)
        for j in range(n):
            s_al = tr["cum"][k] + (j + 0.5) * L / max(n, 1)
            side = rng.choice([-1, 1])            # -1 left, +1 right (relative to travel direction)
            lat = rng.uniform(6, 18)              # facade / monument offset from centreline, m
            pois.append((k, s_al, side, lat))
    return pois


def score(tr, est, pois):
    hdg_err = {}
    for m, (h, _) in est.items():
        if not isinstance(h, np.ndarray):
            continue
        e = np.abs(wrap(h - tr["hdg"]))[tr["moving"]] * R2D
        hdg_err[m] = e
    acc = {m: [] for m in hdg_err}
    for (k, s_al, side, lat) in pois:
        # announce when the walker is 6 m before abeam
        idx = np.searchsorted(tr["s"], s_al - 6)
        if idx >= len(tr["s"]) or not tr["moving"][idx]:
            continue
        hk = tr["seg_hdg"][k]
        fwd = np.array([np.sin(hk), np.cos(hk)])
        right = np.array([np.cos(hk), -np.sin(hk)])
        poi = tr["route"][k] + (s_al - tr["cum"][k]) * fwd + side * lat * right   # POI world position
        for m, (h, pos) in est.items():
            if not isinstance(h, np.ndarray):
                continue
            v = poi - pos[idx]
            brg = np.arctan2(v[0], v[1])
            rel = wrap(brg - h[idx])
            acc[m].append((1 if rel > 0 else -1) == side)
    return hdg_err, {m: float(np.mean(v)) for m, v in acc.items()}


def main(runs=16, seed=7):
    rng = np.random.default_rng(seed)
    methods = ["A", "B", "C", "D", "E"]
    agg = {f"{m}{tag}": dict(err=[], acc=[]) for m in methods for tag in ("", "_L1")}
    rej = []
    trace = None
    for r in range(runs):
        route, canyon = make_route(rng)
        tr = walk(route, rng)
        tr["canyon"] = canyon
        tr["route"] = route
        pois = make_pois(tr, rng)
        mm = (route[:-1], route[1:], tr["seg_hdg"])
        for l5, tag in ((True, ""), (False, "_L1")):
            rr = np.random.default_rng(seed * 1000 + r)  # same sensor noise draw for L1/L5 except GNSS model
            se = sensors(tr, rr, l5=l5)
            est = run_estimators(tr, se, rr, mm)
            if l5: rej.append(est.pop("mag_reject_rate"))
            else: est.pop("mag_reject_rate")
            errs, acc = score(tr, est, pois)
            for m in methods:
                agg[m + tag]["err"].append(errs[m]); agg[m + tag]["acc"].append(acc[m])
            if r == 0 and l5:
                trace = (tr, se, est)
        print(f"run {r+1}/{runs} done")

    names = {"A": "A Raw compass (ideal mount)", "B": "B GNSS course only", "C": "C Complementary gyro+mag",
             "D": "D EKF gyro+mag(gated)+GNSS", "E": "E EKF + map-matching (Map Vision)"}
    res = {}
    for key, v in agg.items():
        e = np.concatenate(v["err"])
        res[key] = dict(name=names[key[0]] + (" [L1-only GNSS]" if key.endswith("_L1") else " [L1+L5]"),
                        heading_rmse_deg=round(float(np.sqrt(np.mean(e ** 2))), 1),
                        heading_median_deg=round(float(np.median(e)), 1),
                        heading_p95_deg=round(float(np.percentile(e, 95)), 1),
                        left_right_accuracy=round(float(np.mean(v["acc"])), 4),
                        left_right_acc_min_run=round(float(np.min(v["acc"])), 4))
    res["mag_update_rejection_rate"] = round(float(np.mean(rej)), 3)
    res["runs"] = runs
    with open(os.path.join(HERE, "heading_results.json"), "w") as f:
        json.dump(res, f, indent=1)

    # ---------- plots
    tr, se, est = trace
    t = np.arange(len(tr["hdg"])) * DT
    sl = slice(0, int(420 * FS))
    fig, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    ax[0].plot(t[sl], np.unwrap(tr["hdg"][sl]) * R2D, color=INK, lw=2, label="True walking heading")
    for m, col in (("A", FOG), ("C", BRASS), ("D", TERRA), ("E", OLIVE)):
        ax[0].plot(t[sl], (np.unwrap(tr["hdg"][sl]) + wrap(est[m][0][sl] - tr["hdg"][sl])) * R2D, color=col, lw=1,
                   label=names[m], alpha=0.9)
    ax[0].set_ylabel("Heading, deg"); ax[0].legend(fontsize=7, frameon=False, ncol=2)
    ax[0].set_title("SIMULATED walk (run 1, first 7 min): heading estimates")
    for m, col in (("A", FOG), ("C", BRASS), ("D", TERRA), ("E", OLIVE)):
        ax[1].plot(t[sl], wrap(est[m][0][sl] - tr["hdg"][sl]) * R2D, color=col, lw=0.8, label=m)
    ax[1].axhspan(-45, 45, color=OLIVE, alpha=0.06)
    ax[1].set_ylabel("Heading error, deg"); ax[1].set_xlabel("Time, s"); ax[1].set_ylim(-120, 120)
    ax[1].legend(fontsize=7, frameon=False, ncol=4)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "heading_fusion_trace.png"), dpi=150)

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    keys = methods
    a5 = [res[k]["left_right_accuracy"] * 100 for k in keys]
    a1 = [res[k + "_L1"]["left_right_accuracy"] * 100 for k in keys]
    xx = np.arange(len(keys))
    ax[0].bar(xx - 0.2, a5, 0.4, color=TERRA, label="L1+L5 GNSS")
    ax[0].bar(xx + 0.2, a1, 0.4, color=FOG, label="L1-only GNSS")
    for i in range(len(keys)):
        ax[0].text(xx[i] - 0.2, a5[i] + 0.8, f"{a5[i]:.1f}", ha="center", fontsize=7)
        ax[0].text(xx[i] + 0.2, a1[i] + 0.8, f"{a1[i]:.1f}", ha="center", fontsize=7)
    ax[0].set_xticks(xx); ax[0].set_xticklabels([names[k].split(" ", 1)[1][:22] for k in keys], rotation=20, ha="right", fontsize=7)
    ax[0].set_ylim(40, 105); ax[0].set_ylabel("Left/right classification accuracy, %")
    ax[0].set_title(f"Left/right accuracy ({runs} SIMULATED walks, ~{runs*2} km)")
    ax[0].legend(frameon=False, fontsize=8)
    r5 = [res[k]["heading_rmse_deg"] for k in keys]; p95 = [res[k]["heading_p95_deg"] for k in keys]
    ax[1].bar(xx - 0.2, r5, 0.4, color=INK, label="RMSE")
    ax[1].bar(xx + 0.2, p95, 0.4, color=BRASS, label="95th pct")
    ax[1].set_xticks(xx); ax[1].set_xticklabels([names[k].split(" ", 1)[1][:22] for k in keys], rotation=20, ha="right", fontsize=7)
    ax[1].set_ylabel("Walking-heading error, deg (L1+L5)"); ax[1].legend(frameon=False, fontsize=8)
    ax[1].set_title("Heading error while moving")
    for a in ax: a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "heading_fusion_accuracy.png"), dpi=150)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for m, col in (("A", FOG), ("B", NIGHT), ("C", BRASS), ("D", TERRA), ("E", OLIVE)):
        e = np.sort(np.concatenate(agg[m]["err"]))
        ax.plot(e, np.linspace(0, 1, len(e)), color=col, label=names[m])
    ax.set_xscale("log"); ax.set_xlim(0.3, 180); ax.set_xlabel("Absolute heading error, deg"); ax.set_ylabel("CDF")
    ax.set_title("Heading error CDF (SIMULATED, L1+L5)"); ax.legend(fontsize=7, frameon=False); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "heading_error_cdf.png"), dpi=150)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
