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
    ("Base (Research prices, hardware COGS, D11 Square cost-down to $185 ex-NRE from Jul-28)", {}),
    ("Square fallback price $329 (D11 trigger)", {"msrp_sq": 329, "ks_sq": 226, "pre_sq": 285}),
    ("Square cost-down fails: stays at $227 ex-NRE", {"sq_index": 1.0}),
    ("Square cost-down fails + price $329", {"sq_index": 1.0, "msrp_sq": 329, "pre_sq": 285}),
    ("Square hits D11 target: $168 ex-NRE (<=$240 incl. NRE) from Jul-28", {"sq_index": {str(i): v for i, v in [(20, .74), (21, .74), (22, .74), (23, .74), (24, .74), (25, .74), (26, .73), (27, .71), (28, .69)]}}),
    ("Atlas back to $549", {"msrp_atl": 549, "pre_atl": 459}),
    ("China FATP tariff (+20% of FOB)", {"freight_duty": 0.21}),
    ("Explorer attach -25% (all SKUs)", {"attach_peb": 0.21, "attach_sq": 0.30, "attach_atl": 0.41}),
    ("Churn 8%/mo instead of 6%", {"churn": 0.08}),
    ("Churn 4%/mo instead of 6%", {"churn": 0.04}),
    ("eSIM data $3.00/GB instead of $1.60", {"data_cost_gb": 3.0}),
    ("Retail margin 45% instead of 38%", {"retail_margin": 0.45}),
    ("DTC promo discount 12% instead of 6%", {"dtc_disc": 0.12}),
    ("Kickstarter half of base (2,300 backers)", {"ks_units": 2300, "pre_units": 350}),
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
