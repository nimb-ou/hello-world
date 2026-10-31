#!/usr/bin/env python3
"""Charts for the CFO pack, read from finance/model_summary.json (written by run_all.py)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(HERE)
OUT = os.path.join(FIN, "charts")
os.makedirs(OUT, exist_ok=True)
S = json.load(open(os.path.join(FIN, "model_summary.json")))
INK, BONE, TERRA, BRASS, OLIVE, FOG, NIGHT = "#14161A", "#F3EEE6", "#C4623A", "#B8935A", "#5E6B4E", "#9AA0A6", "#0D1B2A"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.edgecolor": FOG, "axes.labelcolor": INK, "xtick.color": INK,
                     "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": "white",
                     "axes.titleweight": "bold", "axes.titlesize": 13})
FYL = ["FY26*", "FY27", "FY28", "FY29", "FY30", "FY31"]
A = S["annual"]
musd = FuncFormatter(lambda v, _: f"${v/1e6:,.0f}M" if abs(v) >= 1e6 else f"${v/1e3:,.0f}k")


def save(fig, name, note="Source: LORE_Financial_Model.xlsx, base scenario. Estimates; *FY26 = Nov-Dec."):
    fig.text(0.01, 0.01, note, fontsize=7.5, color=FOG)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, name), dpi=160)
    plt.close(fig)


# 1 revenue by stream
fig, ax = plt.subplots(figsize=(9, 5))
streams = [("hw_net", "Hardware", INK), ("subs", "Explorer subs", TERRA), ("trip", "Trip Pass", BRASS),
           ("acc", "Accessories", OLIVE), ("aff", "Affiliate", FOG), ("fleet", "B2B fleet", NIGHT)]
bottom = [0] * 6
for k, lab, col in streams:
    ax.bar(FYL, A[k], bottom=bottom, label=lab, color=col, width=0.62)
    bottom = [b + v for b, v in zip(bottom, A[k])]
for x, v in zip(FYL, A["revenue"]):
    ax.text(x, v * 1.02 + 5e5, f"${v/1e6:,.1f}M", ha="center", fontsize=9)
ax.yaxis.set_major_formatter(musd)
ax.set_title("Revenue by stream")
ax.legend(frameon=False, ncol=3, fontsize=8.5, loc="upper left")
save(fig, "revenue_by_stream.png")

# 2 gross margin
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(FYL[1:], [v * 100 for v in A["gm"][1:]], marker="o", color=TERRA, lw=2.5, label="Blended gross margin")
ax.plot(FYL[1:], [v * 100 for v in A["hw_gm"][1:]], marker="o", color=INK, lw=2, label="Hardware gross margin")
for x, v in zip(FYL[1:], A["gm"][1:]):
    ax.annotate(f"{v*100:.0f}%", (x, v * 100), textcoords="offset points", xytext=(0, 8), ha="center", color=TERRA)
ax.set_ylabel("%")
ax.set_ylim(0, 60)
ax.set_title("Gross margin: hardware vs blended (subscriptions lift the blend)")
ax.legend(frameon=False)
save(fig, "gross_margin.png")

# 3 cash & runway
fig, ax = plt.subplots(figsize=(10, 5))
lab = S["periods"]
cash = S["monthly"]["cash"]
ax.bar(range(len(lab)), cash, color=[TERRA if c < 1e6 else INK for c in cash], width=0.7)
eq = S["monthly"]["equity"]
for i, e in enumerate(eq):
    if e:
        ax.annotate(f"+${e/1e6:.1f}M", (i, cash[i]), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8, color=OLIVE)
ax.set_xticks(range(len(lab)))
ax.set_xticklabels(lab, rotation=70, fontsize=7.5)
ax.yaxis.set_major_formatter(musd)
ax.set_title("Cash balance by period (monthly to Dec-28, then FY) with equity raises")
save(fig, "cash_runway.png", "Terracotta bars = cash below $1M. FY29-31 bars are year-end balances. Base scenario; estimates.")

# 4 headcount
fig, ax = plt.subplots(figsize=(9, 5))
bottom = [0] * 6
for k, l, col in [("hc_rd", "R&D", INK), ("hc_sm", "S&M", TERRA), ("hc_ops", "Ops & CS", OLIVE), ("hc_ga", "G&A", BRASS)]:
    ax.bar(FYL, A[k], bottom=bottom, label=l, color=col, width=0.6)
    bottom = [b + v for b, v in zip(bottom, A[k])]
for x, v in zip(FYL, A["hc"]):
    ax.text(x, v + 1.5, f"{v:.0f}", ha="center")
ax.set_title("Headcount at year end by department")
ax.legend(frameon=False)
save(fig, "headcount.png")

# 5 unit economics waterfall per SKU (DTC)
UE = S["unit_economics"]
steps = [("MSRP", "MSRP"), ("Discount / retailer margin", "Discount"), ("Returns allowance", "Returns"),
         ("Landed COGS (BOM + assembly + pack + freight/duty)", "Landed COGS"), ("Fulfilment / distribution", "Fulfilment"),
         ("Payment processing", "Payments"), ("Warranty reserve", "Warranty"), ("Acquisition cost (paid CAC DTC; co-op for retail)", "CAC"),
         ("Accessories gross profit per device", "Accessories"), ("Free 3-month trial cost (cloud)", "Trial cost"),
         ("Subscription LTV (gross profit, undiscounted)", "Sub LTV"), ("Affiliate gross profit over device life", "Affiliate")]
fig, axes = plt.subplots(1, 3, figsize=(15, 5.5), sharey=True)
for j, (ax, nm) in enumerate(zip(axes, ["Pebble", "Square", "Atlas"])):
    run = 0
    xs = []
    for i, (key, short) in enumerate(steps):
        v = UE[key][j] or 0
        col = INK if i == 0 else (OLIVE if v >= 0 else TERRA)
        ax.bar(i, v, bottom=run if i else 0, color=col, width=0.7)
        run = v if i == 0 else run + v
        xs.append(short)
    tot = UE["TOTAL LIFETIME CONTRIBUTION PER DEVICE"][j]
    ax.bar(len(steps), tot, color=BRASS, width=0.7)
    ax.text(len(steps), tot + 8, f"${tot:,.0f}", ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(range(len(steps) + 1))
    ax.set_xticklabels(xs + ["Lifetime\ncontribution"], rotation=70, fontsize=8)
    ax.set_title(f"{nm} (DTC, FY2028 costs)")
    ax.axhline(0, color=FOG, lw=0.8)
axes[0].set_ylabel("$ per device")
save(fig, "unit_economics_waterfall.png", "Lifetime contribution = HW gross profit - CAC + accessories + subscription LTV + affiliate - trial cost. Undiscounted. Estimates.")

# 6 scenarios revenue
fig, ax = plt.subplots(figsize=(9, 5))
for name, col in [("Bear", FOG), ("Base", TERRA), ("Bull", INK)]:
    ax.plot(FYL[1:], S["scenario_snapshot"][name]["rev"][1:], marker="o", color=col, lw=2.2, label=name)
ax.yaxis.set_major_formatter(musd)
ax.set_title("Revenue by scenario")
ax.legend(frameon=False)
save(fig, "scenarios_revenue.png")
print("charts written to", OUT)
