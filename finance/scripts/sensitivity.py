#!/usr/bin/env python3
"""Whole-model sensitivities: rebuild the workbook with one input overridden, recalc in LibreOffice,
and record FY2028/FY2031 revenue, gross margin, EBITDA, min cash and peak cumulative burn.
Writes finance/sensitivity_results.json (used in pricing-margin-sensitivity.md)."""
import json
import os
import subprocess
import sys
import tempfile

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(HERE)
PY = sys.executable
CASES = [
    ("Base (Research prices, hardware/bom COGS)", {}),
    ("Square MSRP $349 (CFO recommendation)", {"msrp_sq": 349, "ks_sq": 259, "pre_sq": 299}),
    ("Square value-engineered to $185 FOB (DRAM/LTE Cat-1bis)", {"bom_sq": 185.0}),
    ("Square $349 + VE $185 FOB", {"msrp_sq": 349, "ks_sq": 259, "pre_sq": 299, "bom_sq": 185.0}),
    ("Atlas back to $549", {"msrp_atl": 549, "ks_atl": 405, "pre_atl": 459}),
    ("Pebble full spec (on-device 1B, $125 FOB)", {"bom_peb": 125.06}),
    ("China FATP tariff (+20% of FOB)", {"freight_duty": 0.21}),
    ("Explorer attach -25% (all SKUs)", {"attach_peb": 0.21, "attach_sq": 0.30, "attach_atl": 0.41}),
    ("Churn 8%/mo instead of 6%", {"churn": 0.08}),
    ("Churn 4%/mo instead of 6%", {"churn": 0.04}),
    ("eSIM data $3.00/GB instead of $1.60", {"data_cost_gb": 3.0}),
    ("Retail margin 45% instead of 38%", {"retail_margin": 0.45}),
    ("DTC promo discount 12% instead of 6%", {"dtc_disc": 0.12}),
]


def run(over):
    d = tempfile.mkdtemp()
    raw, calc = os.path.join(d, "r.xlsx"), os.path.join(d, "c.xlsx")
    env = {**os.environ, "LORE_OUT": raw, "LORE_OVERRIDES": json.dumps(over)}
    subprocess.run([PY, os.path.join(HERE, "build_model.py")], check=True, env=env, stdout=subprocess.DEVNULL)
    subprocess.run([PY, os.path.join(HERE, "lo_recalc.py"), raw, calc], check=True)
    rm = json.load(open(os.path.join(HERE, "rowmap.json")))
    wb = openpyxl.load_workbook(calc, data_only=True)
    S, sc = rm["sheets"], rm["sumcols"]
    g = lambda sh, k, j: wb[sh][f"{sc[j]}{S[sh][k]}"].value
    fr = wb["Funding & Runway"]
    m = {k: fr[f"D{r}"].value for k, r in rm["fr_metrics"].items()}
    return dict(rev28=g("P&L", "rev", 2), rev31=g("P&L", "rev", 5), gm28=g("P&L", "gm", 2), gm31=g("P&L", "gm", 5),
                hwgm28=g("P&L", "hw_gm", 2), ebitda30=g("P&L", "ebitda", 4), ebitda31=g("P&L", "ebitda", 5),
                min_cash=m["Minimum period-end cash incl. FY29-31"],
                peak_need=m["Peak cumulative op+inv cash outflow (= minimum equity need before buffer)"],
                be=m["First fiscal year with positive EBITDA"])


res = []
for name, over in CASES:
    r = run(over)
    r["case"] = name
    res.append(r)
    print(name, {k: (round(v) if isinstance(v, float) and abs(v) > 2 else v) for k, v in r.items() if k != "case"})
# restore rowmap for base
subprocess.run([PY, os.path.join(HERE, "build_model.py")], check=True, env={**os.environ, "LORE_OUT": os.path.join(tempfile.mkdtemp(), "x.xlsx")}, stdout=subprocess.DEVNULL)
json.dump(res, open(os.path.join(FIN, "sensitivity_results.json"), "w"), indent=1)
