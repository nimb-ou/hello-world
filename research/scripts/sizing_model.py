"""
LORE Research - market sizing model (single source for the numbers in market-sizing.md).

Run:  python3 research/scripts/sizing_model.py
Prints every intermediate step so the math in market-sizing.md can be audited.
All inputs marked SRC come from cited sources (see market-sizing.md); inputs marked EST
are LORE Research estimates and must be validated by the survey (customer-survey.md).
"""

from dataclasses import dataclass


def cagr(start, end, years):
    return (end / start) ** (1 / years) - 1


def grow(value, rate, years):
    return value * (1 + rate) ** years


# ---------------------------------------------------------------------------
# 1. TOP-DOWN: adjacent category markets, projected to 2027 (first shipping year)
# ---------------------------------------------------------------------------
TOP_DOWN = {}

# Travel eSIM (Juniper): $1.8B 2025 -> $8.7B 2030  [SRC]
esim_cagr = cagr(1.8, 8.7, 5)
TOP_DOWN["Travel eSIM"] = dict(base_year=2025, base=1.8, cagr=esim_cagr,
                               relevant_share=1.00,  # EST: all travel eSIM spend is the 'connectivity job'
                               note="Juniper Research")

# Audio guide systems (broad, incl. hardware + apps): $2.8B 2025, 6.9% CAGR  [SRC, low confidence]
TOP_DOWN["Audio guides (all formats)"] = dict(base_year=2025, base=2.8, cagr=0.069,
                                              relevant_share=1.00, note="vendor estimate")

# Smart personal safety devices (TechSci): $12.2B 2024, 16% CAGR  [SRC]
# wearables ~32% of category (Market.us) [SRC]; travel-use share 20% [EST]
TOP_DOWN["Personal safety wearables (travel slice)"] = dict(base_year=2024, base=12.2, cagr=0.16,
                                                            relevant_share=0.32 * 0.20,
                                                            note="TechSci x Market.us wearable share x EST travel share")

# AI wearables (conservative, 360iResearch via GII): $36.38B 2025, 12.46% CAGR [SRC]
# share attributable to 'pocket assistant / travel companion' use cases 3% [EST]
TOP_DOWN["AI wearables (companion slice)"] = dict(base_year=2025, base=36.38, cagr=0.1246,
                                                  relevant_share=0.03, note="GII/360iResearch x EST")

# Travel experiences (Arival/Phocuswright): heading to $342B by 2029 [SRC]
# EST 2027 value ~ $300B; share that is self-guided digital audio/app ~0.5% [EST]
TOP_DOWN["Self-guided digital tours (slice of experiences)"] = dict(base_year=2027, base=300.0, cagr=0.0,
                                                                    relevant_share=0.005,
                                                                    note="Arival/Phocuswright x EST")


def top_down(year=2027):
    rows, total = [], 0.0
    for name, d in TOP_DOWN.items():
        v = grow(d["base"], d["cagr"], year - d["base_year"]) * d["relevant_share"]
        rows.append((name, v))
        total += v
    return rows, total


# ---------------------------------------------------------------------------
# 2. BOTTOM-UP: people x annual revenue per user
# ---------------------------------------------------------------------------
INTL_ARRIVALS_2025_M = 1520          # SRC UN Tourism, millions of arrivals
ARRIVALS_PER_UNIQUE_TRAVELLER = 2.2  # EST: multi-trip + multi-country double counting
HIGH_INCOME_SOURCE_SHARE = 0.60      # EST: share of unique travellers from high/upper-middle income markets
FREQUENT_SHARE = 0.35                # EST: share taking 2+ international trips a year

# Annual revenue per adopting user (LORE pricing, see pricing-research.md)
ASP_BLENDED = 0.45 * 149 + 0.40 * 299 + 0.15 * 599   # mix EST, prices = research recommendation
DEVICE_LIFE_YEARS = 3                                  # EST
SUB_REV_PER_YEAR = 58.0     # EST: avg 2 Trip Passes ($29) or equivalent Explorer months
ACCESSORY_AFFILIATE = 15.0  # EST: accessories + booking affiliate per user-year
ARPU_YEAR = ASP_BLENDED / DEVICE_LIFE_YEARS + SUB_REV_PER_YEAR + ACCESSORY_AFFILIATE

# SAM: Phase-1 sales markets (US+CA, UK, EU-27, AU/NZ) unique international travellers  (EST, see doc)
SAM_POOL_M = {"United States": 40, "Canada": 12, "United Kingdom": 45, "EU-27": 150, "Australia + NZ": 12}
SOLO_INDEPENDENT_SHARE = 0.30   # EST, triangulated from Skyscanner 43%, Global Rescue 35%, ABTA 27%
SAM_FREQUENT_SHARE = 0.45       # EST: of solo/independent travellers, share with 2+ intl trips/yr
PREMIUM_GADGET_PROPENSITY = 0.25  # EST: would pay $150+ for a travel-specific device

# SOM: research base-case unit plan (Finance owns final)
SOM_UNITS = {2027: 5_000, 2028: 40_000, 2029: 120_000, 2030: 250_000, 2031: 400_000}
SUB_ATTACH = 0.35            # EST: share of installed base paying in a given year after free 3 months
SUB_ARPU_PAYING = 90.0       # EST $/yr for a paying subscriber (mix of Explorer annual and Trip Passes)
ACCESSORY_PCT_OF_HW = 0.12   # EST
AFFILIATE_PER_ACTIVE = 8.0   # EST $/active device/yr
ACTIVE_RATE = 0.70           # EST share of installed base used in a year
INSTALLED_LIFE = 3           # years a device stays in the base


def bottom_up():
    unique = INTL_ARRIVALS_2025_M / ARRIVALS_PER_UNIQUE_TRAVELLER
    hi = unique * HIGH_INCOME_SOURCE_SHARE
    freq = hi * FREQUENT_SHARE
    tam_value = freq * ARPU_YEAR / 1000  # $B
    return dict(unique=unique, hi=hi, freq=freq, tam=tam_value)


def sam():
    pool = sum(SAM_POOL_M.values())
    solo = pool * SOLO_INDEPENDENT_SHARE
    frequent = solo * SAM_FREQUENT_SHARE
    premium = frequent * PREMIUM_GADGET_PROPENSITY
    value = premium * ARPU_YEAR / 1000  # $B per year
    return dict(pool=pool, solo=solo, frequent=frequent, people=premium, value=value)


def som():
    rows, base = [], []
    for year, units in SOM_UNITS.items():
        base.append(units)
        installed = sum(base[-INSTALLED_LIFE:])
        hw = units * ASP_BLENDED
        acc = hw * ACCESSORY_PCT_OF_HW
        subs = installed * SUB_ATTACH * SUB_ARPU_PAYING
        aff = installed * ACTIVE_RATE * AFFILIATE_PER_ACTIVE
        rows.append(dict(year=year, units=units, installed=installed, hw=hw, acc=acc, subs=subs,
                         aff=aff, total=hw + acc + subs + aff))
    return rows


if __name__ == "__main__":
    print(f"Travel eSIM implied CAGR 2025-30: {esim_cagr:.1%}")
    rows, total = top_down(2027)
    print("\nTOP-DOWN 2027 ($B)")
    for n, v in rows:
        print(f"  {n:<50} {v:6.2f}")
    print(f"  {'TOTAL':<50} {total:6.2f}")

    print(f"\nBlended ASP: ${ASP_BLENDED:.2f}; ARPU/yr: ${ARPU_YEAR:.2f}")
    b = bottom_up()
    print("\nBOTTOM-UP TAM")
    print(f"  unique intl travellers (M): {b['unique']:.0f}")
    print(f"  high/upper-middle income (M): {b['hi']:.0f}")
    print(f"  frequent 2+ trips (M): {b['freq']:.1f}")
    print(f"  TAM ($B/yr): {b['tam']:.2f}")

    s = sam()
    print("\nSAM")
    for k, v in s.items():
        print(f"  {k}: {v:.2f}")

    print("\nSOM (base case)")
    cum = 0
    for r in som():
        cum += r["units"]
        print(f"  {r['year']}: units {r['units']:>7,}  cum {cum:>9,}  installed {r['installed']:>9,}  "
              f"HW ${r['hw']/1e6:6.1f}M  Acc ${r['acc']/1e6:5.1f}M  Subs ${r['subs']/1e6:5.1f}M  "
              f"Aff ${r['aff']/1e6:4.1f}M  TOTAL ${r['total']/1e6:6.1f}M  share-of-SAM-people {cum/(s['people']*1e6):.1%}")
