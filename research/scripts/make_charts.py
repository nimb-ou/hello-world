"""
LORE Research - chart generator.

Run from repo root:  python3 research/scripts/make_charts.py
Outputs PNGs to research/charts/ and research/launch-scoring.csv.
Numbers come from sizing_model.py (market sizing) and the tables in competitors.md /
launch-markets.md. Prices are list prices (USD) found in cited sources; positioning
coordinates are LORE Research analyst judgements (estimates), not measured data.
"""
import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sizing_model as sm  # noqa: E402

OUT = os.path.join(HERE, "..", "charts")
os.makedirs(OUT, exist_ok=True)

# Brand palette (COMPANY.md)
INK, BONE, TERRA, BRASS, OLIVE, FOG, NIGHT = ("#14161A", "#F3EEE6", "#C4623A", "#B8935A",
                                              "#5E6B4E", "#9AA0A6", "#0D1B2A")

plt.rcParams.update({
    "figure.facecolor": BONE, "axes.facecolor": BONE, "savefig.facecolor": BONE,
    "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "text.color": INK, "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 12,
})


def esc(text):
    """Escape $ so matplotlib does not treat price pairs as mathtext."""
    return text.replace("$", r"\$")


def footer(fig, text):
    fig.text(0.01, 0.01, esc(text), fontsize=7, color=FOG, ha="left", va="bottom")


# ---------------------------------------------------------------- 1. waterfall
def market_waterfall():
    b, s = sm.bottom_up(), sm.sam()
    som_rows = sm.som()
    cum_2030 = sum(r["units"] for r in som_rows if r["year"] <= 2030) / 1e6

    steps = [
        ("Unique intl\ntravellers", b["unique"]),
        ("High/upper-mid\nincome source", b["hi"]),
        ("Phase-1 sales\nmarkets", s["pool"]),
        ("Solo /\nindependent", s["solo"]),
        ("2+ intl\ntrips / yr", s["frequent"]),
        ("Will pay $150+\nfor travel device\n= SAM", s["people"]),
        ("SOM: cum.\nunits by 2030", cum_2030),
    ]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13, 5.6), gridspec_kw={"width_ratios": [1.7, 1]})

    prev = None
    for i, (label, val) in enumerate(steps):
        if prev is None:
            ax.bar(i, val, color=NIGHT)
        else:
            drop = prev - val
            ax.bar(i, val, color=TERRA if i >= 5 else OLIVE)
            ax.bar(i, drop, bottom=val, color=FOG, alpha=0.35)
        ax.text(i, val + 12, f"{val:,.1f}M" if val < 100 else f"{val:,.0f}M",
                ha="center", fontsize=9, fontweight="bold")
        prev = val
    ax.set_xticks(range(len(steps)))
    ax.set_xticklabels([s_[0] for s_ in steps], fontsize=8)
    ax.set_ylabel("People (millions)")
    ax.set_title("Bottom-up funnel: from all international travellers to LORE buyers")
    ax.set_ylim(0, 760)

    # right panel: $ view
    td_rows, td_total = sm.top_down(2027)
    labels = ["Top-down\n(2027 category\nspend)", "Bottom-up\nTAM", "SAM", "SOM\n(2030 rev.)"]
    som_2030 = [r for r in som_rows if r["year"] == 2030][0]["total"] / 1e9
    vals = [td_total, b["tam"], s["value"], som_2030]
    bottom = 0
    colors = [NIGHT, OLIVE, BRASS, FOG, TERRA]
    for (name, v), c in zip(td_rows, colors):
        ax2.bar(0, v, bottom=bottom, color=c, label=name)
        bottom += v
    ax2.bar(1, vals[1], color=OLIVE)
    ax2.bar(2, vals[2], color=TERRA)
    ax2.bar(3, vals[3], color=TERRA)
    for i, v in enumerate(vals):
        ax2.text(i, v + 0.4, f"${v:,.2f}B" if v < 1 else f"${v:,.1f}B", ha="center",
                 fontweight="bold", fontsize=9)
    ax2.set_xticks(range(4))
    ax2.set_xticklabels(labels, fontsize=8)
    ax2.set_ylabel("USD billions per year")
    ax2.set_title("TAM / SAM / SOM in dollars")
    ax2.legend(fontsize=6.5, loc="upper right", frameon=False)
    ax2.set_ylim(0, 36)
    footer(fig, "Source: LORE Research sizing_model.py. Inputs: UN Tourism, Juniper, TechSci, GII/360iResearch, "
                "Arival/Phocuswright + LORE estimates (see market-sizing.md). Estimates, not audited data.")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, "market-size-waterfall.png"), dpi=170)
    plt.close(fig)


# ---------------------------------------------------- 2. competitor price chart
PRICES = [
    # (name, category, device USD list price, recurring note)
    ("Bee Pioneer (Amazon)", "AI gadget", 50, "acq. by Amazon"),
    ("Limitless Pendant", "AI gadget", 99, "discontinued (Meta)"),
    ("invisaWear", "Safety", 99, "+$14.99/mo"),
    ("Plaud NotePin S", "AI gadget", 179, "+opt. AI plan"),
    ("Shokz OpenRun Pro 2", "Audio", 180, "-"),
    ("Rabbit R1", "AI gadget", 199, "no sub"),
    ("Timekettle W4 Pro", "Translator", 449, "launch price"),
    ("Pocketalk Plus", "Translator", 300, "incl. 2-yr data"),
    ("Oura Ring 4", "Wearable", 349, "+$5.99/mo"),
    ("Ray-Ban Meta Gen 2", "Big Tech", 379, "no sub"),
    ("Garmin inReach Mini 2", "Safety", 400, "+$14.95-34.95/mo"),
    ("Garmin inReach Mini 3", "Safety", 449, "+plan"),
    ("Humane AI Pin (dead)", "AI gadget", 699, "+$24/mo"),
    ("Apple Watch Ultra 3", "Big Tech", 799, "sat. SOS free 2 yrs"),
    ("Meta Ray-Ban Display", "Big Tech", 799, "no sub"),
    ("LORE Pebble", "LORE", 149, "3 mo Explorer incl."),
    ("LORE Square", "LORE", 299, "3 mo Explorer incl."),
    ("LORE Atlas", "LORE", 599, "3 mo Explorer incl."),
]
CAT_COLORS = {"AI gadget": FOG, "Safety": OLIVE, "Audio": BRASS, "Translator": NIGHT,
              "Wearable": BRASS, "Big Tech": INK, "LORE": TERRA}


def price_positioning():
    data = sorted(PRICES, key=lambda r: r[2])
    fig, ax = plt.subplots(figsize=(11, 7))
    for i, (name, cat, price, note) in enumerate(data):
        c = CAT_COLORS[cat]
        ax.hlines(i, 0, price, color=c, alpha=0.35, lw=2)
        ax.scatter(price, i, s=140 if cat == "LORE" else 70, color=c, zorder=3,
                   edgecolor=INK if cat == "LORE" else "none")
        ax.text(price + 12, i, esc(f"${price}  ({note})"), va="center", fontsize=8,
                fontweight="bold" if cat == "LORE" else "normal")
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([d[0] for d in data], fontsize=9)
    for lbl, d in zip(ax.get_yticklabels(), data):
        if d[1] == "LORE":
            lbl.set_color(TERRA)
            lbl.set_fontweight("bold")
    ax.set_xlim(0, 1000)
    ax.set_xlabel("Device list price, USD (launch/MSRP; sale prices excluded)")
    ax.set_title("Competitor & comparable price positioning vs. recommended LORE prices")
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=9, label=k)
               for k, c in CAT_COLORS.items()]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=8)
    footer(fig, "Sources: see competitors.md and pricing-research.md (prices as reported Oct 2025-Oct 2026). "
                "LORE prices = Research recommendation (Atlas $599 proposed vs $549 target).")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, "competitor-price-positioning.png"), dpi=170)
    plt.close(fig)


# ------------------------------------------------------------ 3. positioning map
# x: 0 = fully phone-dependent ... 10 = standalone (own data, offline, battery, controls)
# y: 0 = general-purpose ... 10 = travel-specialised (place stories, local, safety for travellers)
POSITIONS = [
    ("Audiala / AI audio-guide apps", 1.5, 8.6, FOG),
    ("VoiceMap / PocketGuide", 1.8, 9.2, FOG),
    ("Rick Steves Audio Europe", 2.6, 8.9, FOG),
    ("SmartGuide", 2.2, 8.0, FOG),
    ("Google Maps + Gemini (phone)", 1.0, 5.2, INK),
    ("Ray-Ban Meta / Android XR glasses", 3.2, 3.2, INK),
    ("Meta Ray-Ban Display", 3.8, 3.8, INK),
    ("Apple (iPhone sat. SOS, AirPods)", 2.2, 2.6, INK),
    ("OpenAI io device (expected)", 5.0, 1.8, INK),
    ("Plaud / Bee / Limitless", 3.5, 0.9, BRASS),
    ("Rabbit R1", 6.0, 1.4, BRASS),
    ("Humane AI Pin (dead)", 8.2, 1.2, BRASS),
    ("Airalo / Holafly / Saily", 1.2, 6.6, OLIVE),
    ("Garmin inReach", 9.2, 4.6, OLIVE),
    ("invisaWear", 2.0, 3.8, OLIVE),
    ("Pocketalk", 8.4, 7.0, NIGHT),
    ("Timekettle", 3.0, 7.0, NIGHT),
    ("LORE Pebble", 4.6, 9.0, TERRA),
    ("LORE Square", 7.6, 9.3, TERRA),
    ("LORE Atlas", 9.0, 9.6, TERRA),
]


def positioning_map():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axhline(5, color=FOG, lw=0.8, ls="--")
    ax.axvline(5, color=FOG, lw=0.8, ls="--")
    for name, x, y, c in POSITIONS:
        lore = name.startswith("LORE")
        ax.scatter(x, y, s=260 if lore else 90, color=c, edgecolor=INK if lore else "none", zorder=3)
        ax.annotate(name, (x, y), xytext=(7, 6), textcoords="offset points", fontsize=8.5,
                    fontweight="bold" if lore else "normal", color=TERRA if lore else INK)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 10.6)
    ax.set_xlabel("Phone-dependent   →   Standalone (own data, offline packs, battery, physical controls)")
    ax.set_ylabel("General-purpose   →   Travel-specialised (place stories, local info, traveller safety)")
    ax.set_title("Positioning map: LORE owns the empty 'standalone + travel-specialised' quadrant")
    ax.text(9.9, 10.3, "LORE white space", ha="right", color=TERRA, fontsize=9, style="italic")
    ax.text(0.2, 0.25, "Big Tech / general AI gadgets", color=FOG, fontsize=9, style="italic")
    ax.text(0.2, 10.3, "Apps: specialised but live on the phone", color=FOG, fontsize=9, style="italic")
    ax.text(9.9, 0.25, "Standalone but generic / niche", ha="right", color=FOG, fontsize=9, style="italic")
    footer(fig, "Coordinates are LORE Research analyst scores (0-10) from the feature matrix in competitors.md - "
                "judgement, not measured data.")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, "positioning-map.png"), dpi=170)
    plt.close(fig)


# ------------------------------------------------------- 4. launch city scoring
WEIGHTS = {"volume": 0.20, "story": 0.20, "data": 0.15, "connectivity": 0.10,
           "purchasing": 0.15, "solo_walk": 0.10, "ops": 0.10}
CITIES = {
    #             volume story data conn purch solo ops
    "Rome":      (9, 10, 8, 7, 9, 8, 8),
    "Paris":     (8, 9, 9, 8, 9, 8, 7),
    "London":    (9, 9, 10, 6, 8, 8, 9),
    "Barcelona": (8, 7, 8, 8, 8, 9, 6),
    "Lisbon":    (6, 7, 7, 8, 7, 8, 8),
    "Istanbul":  (9, 10, 6, 7, 5, 6, 4),
    "Kyoto":     (7, 10, 6, 9, 8, 7, 4),
    "Tokyo":     (8, 7, 7, 9, 8, 7, 4),
    "New York":  (7, 7, 10, 8, 7, 8, 8),
    "Amsterdam": (6, 7, 9, 9, 8, 9, 7),
    "Prague":    (5, 9, 8, 8, 6, 9, 8),
    "Athens":    (6, 9, 6, 7, 7, 6, 7),
    "Florence":  (5, 10, 8, 7, 9, 9, 8),
    "Madrid":    (6, 6, 8, 8, 7, 7, 7),
    "Bangkok":   (10, 6, 5, 8, 4, 4, 5),
}


def launch_scoring():
    keys = list(WEIGHTS)
    rows = []
    for city, sc in CITIES.items():
        total = sum(WEIGHTS[k] * v for k, v in zip(keys, sc))
        rows.append((city, *sc, round(total, 2)))
    rows.sort(key=lambda r: -r[-1])
    with open(os.path.join(HERE, "..", "launch-scoring.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["city", *keys, "weighted_score"])
        w.writerows(rows)
    fig, ax = plt.subplots(figsize=(10, 6))
    names = [r[0] for r in rows][::-1]
    vals = [r[-1] for r in rows][::-1]
    ax.barh(names, vals, color=[TERRA if n == "Rome" else (BRASS if v >= 8.0 else OLIVE)
                                for n, v in zip(names, vals)])
    for i, v in enumerate(vals):
        ax.text(v + 0.05, i, f"{v:.2f}", va="center", fontsize=8.5)
    ax.set_xlim(0, 10)
    ax.set_xlabel("Weighted score (0-10)")
    ax.set_title("Launch city scoring matrix (weights in launch-markets.md)")
    footer(fig, "Scores are LORE Research judgements anchored on cited arrival, network and data sources; "
                "see launch-markets.md.")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, "launch-city-scores.png"), dpi=170)
    plt.close(fig)
    return rows


if __name__ == "__main__":
    market_waterfall()
    price_positioning()
    positioning_map()
    for r in launch_scoring():
        print(r)
    print("charts written to", os.path.abspath(OUT))
