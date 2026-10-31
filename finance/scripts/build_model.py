#!/usr/bin/env python3
"""
LORE Labs, Inc. -- Financial model builder.

Builds finance/LORE_Financial_Model.xlsx with LIVE Excel formulas.
All inputs live on 'Assumptions' (blue font) and 'Scenarios'; every other
sheet is formulas. Timeline: monthly Nov-2026 .. Dec-2028 (26 cols),
then annual FY2029, FY2030, FY2031 (3 cols) on every time-series sheet.

Run:  python3 finance/scripts/build_model.py
Then: python3 finance/scripts/recalc_and_verify.py   (LibreOffice recalc + checks)

Author: CFO office (finance/). All figures are ESTIMATES unless sourced.
"""
import datetime as dt
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.workbook.defined_name import DefinedName

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.dirname(HERE)
OUT = os.path.join(FIN, "LORE_Financial_Model.xlsx")

# Optional overrides (used by recalc script to flip scenario etc.)
OVERRIDES = json.loads(os.environ.get("LORE_OVERRIDES", "{}"))

# --------------------------------------------------------------------------
# Timeline
# --------------------------------------------------------------------------
PERIODS = []
y, m = 2026, 11
while (y, m) <= (2028, 12):
    PERIODS.append(dict(label=dt.date(y, m, 1).strftime("%b-%y"), year=y, month=m,
                        key=y * 100 + m, months=1, monthly=True, start=dt.date(y, m, 1)))
    m += 1
    if m == 13:
        y, m = y + 1, 1
for yr in (2029, 2030, 2031):
    PERIODS.append(dict(label=f"FY{yr}", year=yr, month=1, key=yr, months=12,
                        monthly=False, start=dt.date(yr, 1, 1)))
NP = len(PERIODS)            # 29
NM = sum(p["monthly"] for p in PERIODS)  # 26
FC = 3                       # first period column = C
COLS = [CL(FC + i) for i in range(NP)]
FIRST, LAST = COLS[0], COLS[-1]
FY = [2026, 2027, 2028, 2029, 2030, 2031]
SUMC0 = FC + NP + 1          # annual summary block starts after a spacer col
SUMCOLS = [CL(SUMC0 + k) for k in range(len(FY))]
HDR_ROWS = 6                 # rows 1..6 are headers on TS sheets; data from 8


def idx_of(key):
    for i, p in enumerate(PERIODS):
        if p["key"] == key:
            return i
    raise KeyError(key)


def months_idx(year):
    return [i for i, p in enumerate(PERIODS) if p["monthly"] and p["year"] == year]


# --------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------
BLUE = Font(name="Inter", color="0000FF")
BOLD = Font(name="Inter", bold=True)
TITLE = Font(name="Inter", bold=True, size=14, color="14161A")
HDR = Font(name="Inter", bold=True, color="F3EEE6")
HDRFILL = PatternFill("solid", fgColor="14161A")
SECFILL = PatternFill("solid", fgColor="F3EEE6")
INFILL = PatternFill("solid", fgColor="FFF7E0")
TOTFONT = Font(name="Inter", bold=True)
NOTE = Font(name="Inter", italic=True, color="5E6B4E", size=9)
THIN = Side(style="thin", color="9AA0A6")
TOPB = Border(top=THIN)

F_USD = '#,##0;[Red](#,##0);"-"'
F_USD2 = '#,##0.00;[Red](#,##0.00);"-"'
F_PCT = '0.0%;[Red]-0.0%;"-"'
F_NUM = '#,##0;[Red](#,##0);"-"'
F_NUM1 = '#,##0.0;[Red](#,##0.0);"-"'
F_X = '0.00"x"'

wb = Workbook()
wb.remove(wb.active)


def add_name(name, ref):
    wb.defined_names[name] = DefinedName(name, attr_text=ref)


def q(sheet):
    return f"'{sheet}'"


# --------------------------------------------------------------------------
# Time-series sheet helper
# --------------------------------------------------------------------------
class TS:
    def __init__(self, name, title, summary=None):
        self.name = name
        self.ws = wb.create_sheet(name)
        self.rows = {}
        self.r = HDR_ROWS + 2
        self.summary = summary  # None | True (adds FY summary block)
        ws = self.ws
        ws["A1"] = title
        ws["A1"].font = TITLE
        ws.column_dimensions["A"].width = 46
        ws.column_dimensions["B"].width = 12
        for c in COLS:
            ws.column_dimensions[c].width = 11.5
        labels = ["Period", "Year", "Months in period", "Period start", "Period key"]
        for k, lab in enumerate(labels):
            rr = 2 + k
            ws.cell(rr, 1, lab).font = BOLD
            for i, c in enumerate(COLS):
                src = f"Timeline!{c}{rr}"
                cell = ws[f"{c}{rr}"]
                cell.value = f"={src}"
                if rr == 2:
                    cell.font, cell.fill = HDR, HDRFILL
                    cell.alignment = Alignment(horizontal="center")
                if rr == 5:
                    cell.number_format = "mmm-yy"
        if summary:
            ws.column_dimensions[CL(FC + NP)].width = 3
            for k, fy in enumerate(FY):
                c = SUMCOLS[k]
                ws.column_dimensions[c].width = 13
                ws[f"{c}2"] = f"FY{fy}" + (" (Nov-Dec)" if fy == 2026 else "")
                ws[f"{c}2"].font, ws[f"{c}2"].fill = HDR, PatternFill("solid", fgColor="C4623A")
                ws[f"{c}3"] = fy
        ws.freeze_panes = "C7"

    def section(self, label):
        self.r += 1
        c = self.ws.cell(self.r, 1, label)
        c.font = BOLD
        for col in range(1, FC + NP):
            self.ws.cell(self.r, col).fill = SECFILL
        self.r += 1

    def add(self, key, label, f, fmt=F_USD, unit="", total=False, summ="sum", note=None):
        """f: callable(i) -> formula string (without '=') or number."""
        r = self.r
        self.rows[key] = r
        ws = self.ws
        ws.cell(r, 1, label)
        ws.cell(r, 2, unit).font = NOTE
        for i, c in enumerate(COLS):
            v = f(i)
            cell = ws[f"{c}{r}"]
            cell.value = f"={v}" if isinstance(v, str) else v
            cell.number_format = fmt
            if total:
                cell.font, cell.border = TOTFONT, TOPB
        if total:
            ws.cell(r, 1).font = TOTFONT
        if self.summary and summ:
            for k, fy in enumerate(FY):
                sc = SUMCOLS[k]
                rng = f"${FIRST}{r}:${LAST}{r}"
                yr = f"${FIRST}$3:${LAST}$3"
                if summ == "sum":
                    fml = f"=SUMIF({yr},{sc}$3,{rng})"
                elif summ == "last":
                    # last period of that FY: monthly Dec or the annual col
                    fml = f"=LOOKUP(2,1/({yr}={sc}$3),{rng})"
                    lastcol = self._last_col(fy)
                    fml = f"={lastcol}{r}"
                elif summ == "avg":
                    fml = f"=SUMIF({yr},{sc}$3,{rng})/COUNTIF({yr},{sc}$3)"
                else:  # custom callable(k,fy) -> formula
                    fml = "=" + summ(k, fy)
                cell = ws[f"{sc}{r}"]
                cell.value = fml
                cell.number_format = fmt
                if total:
                    cell.font, cell.border = TOTFONT, TOPB
        if note:
            ws.cell(r, FC + NP + (len(FY) + 2 if self.summary else 1), note).font = NOTE
        self.rows[key] = r
        self.r += 1
        return r

    def _last_col(self, fy):
        cand = [i for i, p in enumerate(PERIODS) if p["year"] == fy]
        return COLS[cand[-1]]

    def ref(self, key, i, absolute=False, sheet_prefix=True):
        r = self.rows[key]
        c = COLS[i]
        if absolute:
            c, r = f"${c}", f"${r}"
        return f"{q(self.name)}!{c}{r}" if sheet_prefix else f"{c}{r}"

    def sref(self, key, k):
        """Reference to the annual summary column k (FY index)."""
        return f"{q(self.name)}!{SUMCOLS[k]}{self.rows[key]}"

    def rng(self, key, i0, i1):
        r = self.rows[key]
        return f"{q(self.name)}!{COLS[i0]}{r}:{COLS[i1]}{r}"


def R(ts, key):
    """shorthand: returns function i -> ref"""
    return lambda i: ts.ref(key, i)


# --------------------------------------------------------------------------
# 0. Timeline sheet
# --------------------------------------------------------------------------
tl = wb.create_sheet("Timeline")
tl["A1"] = "Timeline (monthly Nov-2026 to Dec-2028, then annual FY2029-FY2031)"
tl["A1"].font = TITLE
for k, lab in enumerate(["Period", "Year", "Months in period", "Period start", "Period key", "Monthly flag (1=month)"]):
    tl.cell(2 + k, 1, lab).font = BOLD
for i, p in enumerate(PERIODS):
    c = COLS[i]
    tl[f"{c}2"] = p["label"]
    tl[f"{c}3"] = p["year"]
    tl[f"{c}4"] = p["months"]
    tl[f"{c}5"] = p["start"]
    tl[f"{c}5"].number_format = "mmm-yy"
    tl[f"{c}6"] = p["key"]
    tl[f"{c}7"] = 1 if p["monthly"] else 0
# NB: TS header row 6 reads Timeline row 6 = key.
tl.column_dimensions["A"].width = 30

# --------------------------------------------------------------------------
# 1. Scenarios
# --------------------------------------------------------------------------
sc = wb.create_sheet("Scenarios")
sc["A1"] = "Scenarios -- set the selector (1 = Bear, 2 = Base, 3 = Bull). Every sheet recalculates."
sc["A1"].font = TITLE
sc["A3"] = "ACTIVE SCENARIO (1/2/3)"
sc["A3"].font = BOLD
sc["C3"] = OVERRIDES.get("Scenario", 2)
sc["C3"].font = Font(name="Inter", color="0000FF", bold=True, size=14)
sc["C3"].fill = INFILL
add_name("Scenario", "Scenarios!$C$3")
sc["D3"] = '=CHOOSE(Scenario,"Bear","Base","Bull")'
sc["D3"].font = BOLD
for j, h in enumerate(["Driver", "Name", "Bear", "Base", "Bull", "LIVE", "What it does / rationale"]):
    cell = sc.cell(5, 1 + j, h)
    cell.font, cell.fill = HDR, HDRFILL
SCN = [
    ("Unit volume multiplier (KS + regular sales)", "sc_vol", 0.55, 1.0, 1.45,
     "Bear ~ a mid-sized KS ($0.55M) and slow retail; bull ~ breakout KS + strong retail sell-through."),
    ("Hardware & subscription price multiplier", "sc_price", 0.93, 1.0, 1.0,
     "Bear assumes ~7% deeper promotions / price cuts."),
    ("Subscription attach multiplier", "sc_attach", 0.70, 1.0, 1.25,
     "Applied to post-trial paid conversion per SKU."),
    ("Subscription churn multiplier", "sc_churn", 1.30, 1.0, 0.80,
     "Bear 7.8%/mo, base 6.0%/mo, bull 4.8%/mo."),
    ("Landed COGS multiplier", "sc_cogs", 1.10, 1.0, 0.95,
     "Bear: memory price spike / tariffs; bull: better ODM quote."),
    ("CAC / paid-acquisition multiplier", "sc_cac", 1.35, 1.0, 0.85,
     "Applied to paid CAC per DTC unit."),
]
for j, (lab, nm, b, base, bu, why) in enumerate(SCN):
    r = 6 + j
    sc.cell(r, 1, lab)
    sc.cell(r, 2, nm).font = NOTE
    for k, v in enumerate((b, base, bu)):
        cc = sc.cell(r, 3 + k, v)
        cc.font, cc.fill, cc.number_format = BLUE, INFILL, "0.00"
    sc.cell(r, 6, f"=CHOOSE(Scenario,C{r},D{r},E{r})").number_format = "0.00"
    sc.cell(r, 6).font = BOLD
    sc.cell(r, 7, why).font = NOTE
    add_name(nm, f"Scenarios!$F${r}")
sc.column_dimensions["A"].width = 46
sc.column_dimensions["G"].width = 90
SC_SNAP_ROW = 6 + len(SCN) + 3   # snapshot table is written by recalc script

# --------------------------------------------------------------------------
# 2. Assumptions (scalars with names + time-series inputs)
# --------------------------------------------------------------------------
asm = wb.create_sheet("Assumptions", 0)
asm["A1"] = "Assumptions -- all inputs in BLUE. Estimates unless a source is cited. Prices ex-VAT/sales tax."
asm["A1"].font = TITLE
for j, h in enumerate(["Input", "Name", "Value", "Unit", "Basis / source"]):
    cell = asm.cell(3, 1 + j, h)
    cell.font, cell.fill = HDR, HDRFILL
asm.column_dimensions["A"].width = 52
asm.column_dimensions["B"].width = 18
asm.column_dimensions["C"].width = 12
asm.column_dimensions["D"].width = 14
asm.column_dimensions["E"].width = 110
_ar = [4]
SCALARS = {}


def a_sec(title):
    _ar[0] += 1
    c = asm.cell(_ar[0], 1, title)
    c.font = BOLD
    for col in range(1, 6):
        asm.cell(_ar[0], col).fill = SECFILL
    _ar[0] += 1


def a_in(label, name, value, unit="", basis="", fmt=None):
    value = OVERRIDES.get(name, value)
    r = _ar[0]
    asm.cell(r, 1, label)
    asm.cell(r, 2, name).font = NOTE
    c = asm.cell(r, 3, value)
    c.font, c.fill = BLUE, INFILL
    if fmt:
        c.number_format = fmt
    elif "%" in unit:
        c.number_format = "0.0%"
    else:
        c.number_format = "#,##0.00" if isinstance(value, float) else "#,##0"
    asm.cell(r, 4, unit).font = NOTE
    asm.cell(r, 5, basis).font = NOTE
    add_name(name, f"Assumptions!$C${r}")
    SCALARS[name] = value
    _ar[0] += 1


a_sec("General & finance")
a_in("Opening cash (Nov-2026, before pre-seed)", "opening_cash", 0, "$", "Founder-funded work to date excluded.")
a_in("Interest earned on cash (annual)", "interest_rate", 0.035, "%/yr", "US T-bill / treasury MMF yields ~3.5-4% (2026), conservative.")
a_in("Corporate income tax rate (after NOLs)", "tax_rate", 0.21, "%", "US federal 21%; state ignored; NOLs offset until cumulative pre-tax > 0.")
a_in("Employer burden on salary (benefits, payroll tax)", "burden", 0.25, "%", "Typical US startup 20-30%. Legal-ops owns final salary bands.")
a_in("Annual salary inflation (from 2028)", "salary_infl", 0.03, "%/yr", "Estimate.")

a_sec("Hardware pricing (MSRP from COMPANY.md; KS prices = early-bird)")
a_in("LORE Pebble MSRP", "msrp_peb", 149, "$", "COMPANY.md target price.")
a_in("LORE Square MSRP", "msrp_sq", 299, "$", "Research final (holds COMPANY.md). CFO FLAG: with hardware/bom landed $227 @10k the DTC hardware margin is single-digit until DRAM normalises & 100k-tier pricing; see pricing-margin-sensitivity.md.")
a_in("LORE Atlas MSRP", "msrp_atl", 599, "$", "Research recommends $599 (COMPANY.md $549). Atlas launches Sep-2028 (CFO assumption: NTN + camera + titanium need a separate EVT/DVT cycle).")
a_in("Kickstarter blended pledge price -- Pebble", "ks_peb", 113, "$", "GTM tiers $99 (750) / $115 (2,000) / $125.")
a_in("Kickstarter blended pledge price -- Square", "ks_sq", 226, "$", "GTM tiers $199 (750) / $229 (2,000) / $249.")
a_in("Post-campaign pre-order price -- Pebble", "pre_peb", 129, "$", "BackerKit/website pre-order, ~13% off (Research).")
a_in("Kickstarter blended pledge price -- Atlas", "ks_atl", 405, "$", "GTM Atlas Founders Edition $399 (500 numbered) + later tiers.")
a_in("Post-campaign pre-order price -- Atlas", "pre_atl", 499, "$", "Research KS standard tier.")
a_in("Post-campaign pre-order price -- Square", "pre_sq", 259, "$", "~13% off $299 (Research).")
a_in("Average DTC promo discount vs MSRP", "dtc_disc", 0.06, "%", "Blended codes/bundles/Black Friday.")
a_in("Retailer / distributor margin (off MSRP)", "retail_margin", 0.38, "%", "Consumer electronics retail margins typically 30-45% incl. distributor; estimate.")
a_in("Returns & refunds allowance (of HW revenue)", "returns_pct", 0.04, "%", "Consumer electronics 3-8%; estimate.")

a_sec("Landed COGS per unit, 10k tier (RECONCILED to hardware/bom/cogs_summary.csv, 30-Oct-2026); NRE (cert/tooling) is expensed/capitalised separately")
a_in("Pebble (ships as Pebble Lite ECR spec) -- FOB incl. conversion & yield", "bom_peb", 62.03, "$", "hardware/bom: Pebble Lite (ECR, cloud AI, no DRAM) FOB @10k $62.03. Full-spec Pebble (on-device 1B model) is $125.06 FOB -> negative margin at $149, so CFO base case ships the ECR spec.")
a_in("Pebble -- royalties", "asm_peb", 0.0, "$", "hardware/bom: none (no cellular).")
a_in("Pebble -- extra packaging (included in FOB)", "pkg_peb", 0.0, "$", "Included in hardware/bom FOB.")
a_in("Square -- FOB incl. conversion & yield (launch/DVT quote)", "bom_sq", 219.11, "$", "hardware/bom @10k: $227 landed ex-NRE (~$299 incl. NRE amortised over 10k). D11 cost-down (Cat-1bis) applied via the Square cost index below.")
a_in("Square -- cellular SEP royalties", "asm_sq", 5.80, "$", "hardware/bom estimate.")
a_in("Square -- extra packaging (included in FOB)", "pkg_sq", 0.0, "$", "")
a_in("Atlas -- FOB incl. conversion & yield", "bom_atl", 305.55, "$", "hardware/bom @10k.")
a_in("Atlas -- royalties", "asm_atl", 8.70, "$", "hardware/bom estimate.")
a_in("Atlas -- extra packaging (included in FOB)", "pkg_atl", 0.0, "$", "")
a_in("Inbound freight, insurance & duties (% of FOB)", "freight_duty", 0.01, "%", "hardware/bom: freight $1.3-2.2/unit; 0% US duty assumes VN/MY FATP (China FATP adds ~20% of FOB -- see sensitivity).")
a_in("Warranty reserve (% of HW revenue)", "warranty_pct", 0.02, "%", "1-2 yr warranty; estimate.")
a_in("DTC outbound shipping + 3PL pick/pack per unit", "dtc_ship", 11.0, "$", "3PL ~$3-4 + ground/intl blend.")
a_in("Retail distribution cost per unit", "retail_dist", 4.0, "$", "Palletised to DC.")
a_in("Pre-order (KS) fulfilment cost per unit, net of shipping charged", "ks_fulfil_net", 6.0, "$", "Backers pay shipping; residual subsidy + 3PL.")
a_in("Card processing -- % (DTC)", "pay_pct", 0.029, "%", "Stripe/Shopify Payments standard 2.9% + $0.30.")
a_in("Card processing -- fixed per order", "pay_fixed", 0.30, "$", "")

a_sec("Kickstarter / pre-orders (Q2-2027 campaign; ships Nov-2027 to Jan-2028)")
a_in("Kickstarter backer units (base, before scenario)", "ks_units", 4600, "units", "GTM base case: $1.04M gross / ~4,600 backers (gtm/kickstarter/campaign-plan.md); ~1 device per backer, kits/add-ons in accessories.")
a_in("Post-campaign pre-order units (BackerKit / website)", "pre_units", 700, "units", "Late pledges typically 15-30% of campaign units.")
a_in("Pre-order SKU mix -- Pebble share", "pre_mix_peb", 0.45, "%", "Research mix 45/40/15.")
a_in("Pre-order SKU mix -- Atlas share (Square = remainder)", "pre_mix_atl", 0.15, "%", "Atlas Founders ship Apr-2028 (GTM tier table).")
a_in("Kickstarter platform fee", "ks_fee", 0.05, "%", "Kickstarter 5% of funds (https://www.launchboom.com/crowdfunding-tips/how-much-does-kickstarter-charge/)")
a_in("Kickstarter payment processing %", "ks_proc", 0.03, "%", "3% + $0.20 per pledge (https://www.pledgebox.com/post/how-much-does-kickstarter-take)")
a_in("Kickstarter processing fixed per pledge", "ks_proc_fixed", 0.20, "$", "")
a_in("Average units per pledge", "units_per_pledge", 1.15, "units", "Estimate (two-packs, gifts).")

a_sec("Subscription -- LORE Pass (COMPANY.md)")
a_in("Explorer list price per month", "sub_price", 9.99, "$/mo", "COMPANY.md.")
a_in("Realised ARPU as % of list (annual-plan discount, promos)", "arpu_real", 0.86, "%", "~40% on Research-recommended $79/yr annual plan.")
a_in("Free Explorer trial included with every device", "trial_months", 3, "months", "COMPANY.md.")
a_in("Post-trial paid attach -- Pebble", "attach_peb", 0.28, "%", "Pebble ships as cloud-AI (ECR) spec, so unlimited live AI needs the Pass; no eSIM. Hardware-subscription comps: Whoop/Oura are mandatory/near-mandatory; ours is optional.")
a_in("Post-trial paid attach -- Square", "attach_sq", 0.40, "%", "eSIM data makes Pass the natural default.")
a_in("Post-trial paid attach -- Atlas", "attach_atl", 0.55, "%", "Premium buyer; satellite SOS.")
a_in("Monthly churn of paid Explorer subs (base)", "churn", 0.06, "%/mo", "Consumer subscription apps lose most subs in month 1; travel is seasonal (https://www.revenuecat.com/state-of-subscription-apps-2025). Annualised ~52%.")
a_in("Trip Pass price (14 days, 5 GB)", "trip_price", 32.0, "$", "Blend: 85% $29 (14d/5GB) + 15% $49 (30d/10GB) (Research).")
a_in("Trip Pass purchase rate per month (non-paying eSIM devices)", "trip_rate", 0.03, "/mo", "~0.36 trips/yr bought by non-subscribers; estimate.")
a_in("Device inactivity (abandonment) rate per month", "device_inactive", 0.02, "%/mo", "~22%/yr of installed base goes dormant.")

a_sec("Accessories, affiliate, B2B fleet")
a_in("Accessory attach (orders per device sold)", "acc_attach", 0.30, "orders/unit", "LORE Kit: clip, lanyard, dock, case, Buds.")
a_in("Accessory average order value", "acc_aov", 45.0, "$", "Mix of $19-39 straps/cases/docks and $129 LORE Buds (Research price).")
a_in("Accessory COGS (% of revenue)", "acc_cogs_pct", 0.38, "%", "Accessories typically 55-70% GM.")
a_in("B2B fleet rental fee per device per month", "fleet_fee", 22.0, "$/unit/mo", "Hostels/tour operators re-rent at ~$5-8/day.")
a_in("Fleet device cost (capitalised)", "fleet_unit_cost", 95.0, "$/unit", "Blend of Pebble/Square landed cost + rugged case.")
a_in("Fleet cloud + data cost per device per month", "fleet_cloud", 3.0, "$/unit/mo", "")
a_in("Fleet device replacement / loss rate per month", "fleet_replace", 0.01, "%/mo", "")

a_sec("Cloud / AI COGS per paid user-month (2027-28 prices; deflation thereafter)")
a_in("LLM inference (live Q&A, ~150 queries/mo)", "llm_cost", 0.30, "$/user-mo", "~300k in / 45k out tokens on a Flash-class model: $0.30/M in, $2.50/M out (https://www.morphllm.com/gemini-api-pricing).")
a_in("Speech-to-text", "stt_cost", 0.15, "$/user-mo", "~25 min/mo at ~$0.006/min.")
a_in("Cloud neural TTS (stories pre-rendered & cached; live answers only)", "tts_cost", 0.70, "$/user-mo", "~45k chars at ~$0.016/1k (standard neural); premium ElevenLabs $0.04-0.10/1k would be 3-6x (https://developer.puter.com/tutorials/elevenlabs-api-pricing/).")
a_in("Infra: hosting, maps/places API, observability", "infra_cost", 0.25, "$/user-mo", "")
a_in("Data used per Explorer eSIM user per month", "data_gb_used", 0.70, "GB", "1 GB allowance; most users under-consume.")
a_in("Wholesale eSIM data cost per GB (blended global)", "data_cost_gb", 1.60, "$/GB", "Wholesale lists ~EUR2.5/GB small-volume, ~$1.85/GB illustrative blend (https://simology.io/blog/wholesale-pricing-forecasting-volume-tiers-commitments-and-margins); target with MVNE at volume.")
a_in("Billing fees on subscriptions (blend web checkout + app stores)", "sub_pay_fee", 0.08, "% of rev", "Web checkout ~3%, app stores 15%; blended.")
a_in("Free-tier / offline active device cost per month", "free_cost", 0.12, "$/device-mo", "Pack downloads, basic narration.")
a_in("Trip Pass data actually used", "trip_data_gb", 2.5, "GB", "Half of the 5 GB allowance.")
a_in("Trip Pass AI cost", "trip_ai", 0.80, "$/pass", "")
a_in("AI unit-cost deflation per year (from 2029)", "ai_defl", 0.20, "%/yr", "Token prices have fallen >50%/yr historically; conservative.")
a_in("Data cost deflation per year (from 2029)", "data_defl", 0.08, "%/yr", "")

a_sec("Working capital")
a_in("ODM deposit at PO (% of landed cost)", "odm_dep", 0.30, "%", "30/70 is the common opening term (https://harris-sliwoski.com/chinalawblog/china-manufacturing-payment-terms/).")
a_in("Deposit paid N months before shipment month", "dep_lead", 3, "months", "Component lead time (LTE modules, AMOLED).")
a_in("Balance (70%) paid N months before shipment month", "bal_lead", 1, "months", "Against B/L, ~4-5 wk ocean.")
a_in("Inventory days (annual years FY29+)", "inv_days", 60, "days of HW COGS", "")
a_in("Retail receivable days", "ar_days", 45, "days", "Net-45 typical for big-box / Amazon vendor.")

a_sec("Sales & marketing")
a_in("Retail co-op / MDF / displays (% of retail HW revenue)", "retail_coop", 0.06, "%", "")
add_name("FirstYear", "Assumptions!$C$2")
asm["B2"] = "Model base year"
asm["C2"] = 2027

# ---- time-series inputs (same column layout as TS sheets) ----
_ar[0] += 2
TSIN_HDR = _ar[0]
asm.cell(TSIN_HDR, 1, "TIME-SERIES INPUTS (blue) -- monthly Nov-26..Dec-28, then FY2029-FY2031").font = TITLE
_ar[0] += 1
asm.cell(_ar[0], 1, "Period").font = BOLD
for i, c in enumerate(COLS):
    cell = asm[f"{c}{_ar[0]}"]
    cell.value = f"=Timeline!{c}2"
    cell.font, cell.fill = HDR, HDRFILL
TSIN_PERIOD_ROW = _ar[0]
_ar[0] += 1
TSIN = {}


def by_period(monthly_map=None, annual=None, default=0.0, year_default=None):
    """Build list of NP values. monthly_map: {key: value}; year_default: {year: value for every month}; annual: {year: value}."""
    vals = []
    for p in PERIODS:
        if p["monthly"]:
            v = default
            if year_default and p["year"] in year_default:
                v = year_default[p["year"]]
            if monthly_map and p["key"] in monthly_map:
                v = monthly_map[p["key"]]
        else:
            v = (annual or {}).get(p["year"], default)
        vals.append(v)
    return vals


def ts_in(name, label, vals, fmt=F_NUM, basis=""):
    if name in OVERRIDES:  # scalar -> all periods; dict {period_index: value}
        o = OVERRIDES[name]
        vals = [o] * NP if not isinstance(o, dict) else [o.get(str(i), v) for i, v in enumerate(vals)]
    r = _ar[0]
    asm.cell(r, 1, label)
    asm.cell(r, 2, name).font = NOTE
    for i, c in enumerate(COLS):
        cell = asm[f"{c}{r}"]
        cell.value = vals[i]
        cell.font, cell.fill, cell.number_format = BLUE, INFILL, fmt
    if basis:
        asm.cell(r, FC + NP + 1, basis).font = NOTE
    TSIN[name] = r
    _ar[0] += 1


def A(name):
    return lambda i: f"Assumptions!{COLS[i]}{TSIN[name]}"


# units: regular (non-pre-order) sell-in units, all SKUs
reg_2028 = [1250, 1350, 1650, 2050, 2450, 2850, 3350, 3450, 3250, 3650, 5250, 7400]
reg_units = by_period(monthly_map={**{202800 + k + 1: v for k, v in enumerate(reg_2028)}},
                      annual={2029: 120000, 2030: 250000, 2031: 400000})
ts_in("reg_units", "Regular unit sales, all SKUs (DTC + retail), base", reg_units, F_NUM,
      "Research final units: 5k 2027 (all pre-orders), 40k 2028, 120k 2029, 250k 2030; 400k 2031 (Research SOM table).")
ts_in("pre_ship_pct", "Pre-order units shipped (% of total pre-orders)",
      by_period(monthly_map={202711: 0.30, 202712: 0.45, 202801: 0.25}), F_PCT, "Pebble/Square: SEB/EB tiers Dec-2027, KS Special Jan-2028 (GTM); first units Nov.")
ts_in("pre_collect_pct", "Pre-order cash collected (% of total pre-orders)",
      by_period(monthly_map={202707: 4600/5300, 202708: 0.0425, 202709: 0.0425, 202710: 0.0471}), F_PCT,
      "Campaign 25 May-24 Jun 2027 (GTM); Kickstarter payout ~14 days after close = Jul-2027; BackerKit late pledges Aug-Oct.")
ts_in("pre_ship_atl", "Atlas pre-order units shipped (% of Atlas pre-orders)",
      by_period(monthly_map={202804: 1.0}), F_PCT, "Atlas Founders Edition delivery Apr-2028 (GTM).")
ts_in("retail_share", "Retail / wholesale share of regular units",
      by_period(monthly_map={**{202800 + k: 0.10 for k in range(1, 7)}, **{202800 + k: 0.25 for k in range(7, 13)}},
                annual={2029: 0.30, 2030: 0.35, 2031: 0.35}), F_PCT, "Retail from 2028 (COMPANY.md). DTC-led (Oura/Whoop-style) because retail margin on Square is thin at BOM-reconciled COGS.")
mix_peb = by_period(year_default={2026: 0.53, 2027: 0.53, 2028: 0.45},
                    monthly_map={202801: 0.53, 202802: 0.53, 202803: 0.53},
                    annual={2029: 0.45, 2030: 0.45, 2031: 0.45})
mix_atl = by_period(year_default={2028: 0.15}, monthly_map={202801: 0.0, 202802: 0.0, 202803: 0.0},
                    annual={2029: 0.15, 2030: 0.15, 2031: 0.15})
mix_sq = [round(1 - a - b, 4) for a, b in zip(mix_peb, mix_atl)]
ts_in("mix_peb", "SKU mix of regular units -- Pebble", mix_peb, F_PCT)
ts_in("mix_sq", "SKU mix of regular units -- Square", mix_sq, F_PCT)
ts_in("mix_atl", "SKU mix of regular units -- Atlas (regular sales from Apr-2028)", mix_atl, F_PCT)
ts_in("fleet_end", "B2B fleet devices deployed (end of period)",
      by_period(monthly_map={202804: 50, 202805: 100, 202806: 150, 202807: 200, 202808: 250, 202809: 300,
                             202810: 400, 202811: 500, 202812: 600},
                annual={2029: 2500, 2030: 6000, 2031: 11000}), F_NUM, "Hostels & tour operators.")
ts_in("cogs_index", "Landed-COGS index (learning curve / volume)",
      by_period(default=1.0, monthly_map={202807: 0.95, 202808: 0.95, 202809: 0.95, 202810: 0.95, 202811: 0.95, 202812: 0.95}, annual={2029: 0.89, 2030: 0.82, 2031: 0.79}), "0.00", "Pebble & Atlas. hardware/bom 10k->100k tier ratio ~0.79-0.80; H2-2028 0.95 = DRAM normalisation (Atlas).")
ts_in("sq_index", "Square cost-down index vs launch quote (D11 LTE Cat-1bis programme)",
      by_period(default=1.0, monthly_map={202807: 0.81, 202808: 0.81, 202809: 0.81, 202810: 0.81, 202811: 0.81, 202812: 0.81},
                annual={2029: 0.80, 2030: 0.77, 2031: 0.75}), "0.00",
      "D11 target <=$240 landed incl. NRE (~$168 ex-NRE) by unit 10k. Base assumes $185 ex-NRE from Jul-28 (target missed by ~10%: conservative), ~$170 by 2031 (hardware 100k tier ~$183 incl. royalties).")
ts_in("affiliate_rate", "Affiliate booking revenue per active device per month",
      by_period(default=0.30, annual={2029: 0.40, 2030: 0.50, 2031: 0.60}), F_USD2,
      "Tours/hotels/restaurants commissions (~8% tours, ~4-6% hotels) on in-app bookings.")
ts_in("cac", "Paid CAC per regular DTC unit (before scenario)",
      by_period(year_default={2026: 0, 2027: 45, 2028: 60}, annual={2029: 65, 2030: 62, 2031: 60}), F_USD,
      "Consumer electronics CAC ~$76-120 across all channels (https://tenten.co/shopify/d2c-cac-benchmarks-2026/); ours lower as KS community + PR + affiliates drive a share.")
ts_in("ks_mkt", "Kickstarter pre-launch & campaign marketing",
      by_period(monthly_map={202702: 15000, 202703: 35000, 202704: 55000, 202705: 70000, 202706: 55000}),
      F_USD, "GTM budget $230k: 12-week list build to 20k emails + 2k $1 VIPs, video, campaign ads (gtm/kickstarter/prelaunch-plan.md).")
ts_in("brand_mkt", "Brand, content, PR & events (non-paid-acquisition)",
      by_period(year_default={2026: 3000, 2027: 6000, 2028: 40000},
                monthly_map={202707: 15000, 202708: 15000, 202709: 15000, 202710: 20000, 202711: 25000, 202712: 25000},
                annual={2029: 1200000, 2030: 2500000, 2031: 4000000}), F_USD)
ts_in("nre_id", "R&D: ID / ME / CMF design agency",
      by_period(monthly_map={202611: 25000, 202612: 25000, 202701: 20000, 202702: 15000, 202703: 10000,
                             202801: 20000, 202802: 20000, 202803: 15000},
                annual={2029: 300000, 2030: 400000, 2031: 500000}), F_USD)
ts_in("nre_odm", "R&D: ODM engineering NRE (EVT/DVT/PVT)",
      by_period(monthly_map={202612: 30000, 202701: 30000, 202702: 20000, 202707: 80000, 202708: 60000,
                             202709: 140000, 202710: 120000, 202711: 60000},
                annual={2029: 600000, 2030: 900000, 2031: 1200000}), F_USD, "Pebble+Square 2027; Atlas 2028; Gen-2 2029+.")
ts_in("nre_proto", "R&D: prototype builds (EVT 50u, DVT 150u, PVT)",
      by_period(monthly_map={202702: 35000, 202707: 40000, 202709: 60000, 202711: 30000, 202805: 30000},
                annual={2029: 150000, 2030: 200000, 2031: 250000}), F_USD, "Q1-2027: 50 EVT units (COMPANY.md).")
ts_in("nre_cert", "R&D: certification (FCC/CE/UKCA/IC, PTCRB/GCF, carrier, NTN)",
      by_period(monthly_map={202708: 80000, 202709: 300000, 202710: 270000, 202711: 300000, 202712: 340000},
                annual={2029: 250000, 2030: 300000, 2031: 350000}), F_USD,
      "hardware: cert Pebble $165k + Square $485k + Atlas $640k (H2-2027).")
ts_in("nre_content", "R&D: City Pack content (fact-checking, data licences, editors' contracts)",
      by_period(monthly_map={202611: 8000, 202612: 8000, 202701: 8000, 202702: 8000, 202703: 8000,
                             202707: 10000, 202708: 10000, 202709: 10000, 202710: 10000, 202711: 10000, 202712: 10000},
                year_default={2028: 35000},
                annual={2029: 750000, 2030: 1000000, 2031: 1250000}), F_USD,
      "~$25k per new city; 20 cities in 2028 (COMPANY.md), +30/+40/+50 per year after.")
ts_in("nre_sw", "R&D: dev tools, cloud dev/test, on-device model fine-tuning compute",
      by_period(year_default={2026: 3000, 2027: 5000, 2028: 12000}, annual={2029: 250000, 2030: 400000, 2031: 600000}), F_USD)
ts_in("tooling", "Capex: production tooling & test fixtures",
      by_period(monthly_map={202707: 190000, 202708: 185000, 202710: 330000, 202812: 100000},
                annual={2029: 500000, 2030: 800000, 2031: 1000000}), F_USD,
      "hardware: tooling + test fixtures Pebble $140k, Square $235k, Atlas $330k.")
ts_in("ga_other", "G&A non-personnel (legal, IP, accounting, insurance, office, SaaS)",
      by_period(year_default={2026: 12000, 2027: 12000, 2028: 35000},
                monthly_map={202708: 20000, 202709: 20000, 202710: 20000, 202711: 20000, 202712: 20000},
                annual={2029: 600000, 2030: 1000000, 2031: 1500000}), F_USD,
      "Incl. SAFE/seed legal, provisional patents, D&O + product liability insurance.")

# --------------------------------------------------------------------------
# 3. Pricing & Mix
# --------------------------------------------------------------------------
pm = TS("Pricing & Mix", "Pricing & SKU mix -- units by SKU and channel", summary=True)
SKUS = [("peb", "Pebble"), ("sq", "Square"), ("atl", "Atlas")]
pm.section("Prices ($/unit)")
for s, nm in SKUS:
    pm.add(f"msrp_{s}", f"MSRP -- {nm}", lambda i, s=s: f"msrp_{s}*sc_price", F_USD, "$", summ=None)
for s, nm in SKUS:
    pm.add(f"dtc_{s}", f"DTC net price -- {nm}", lambda i, s=s: f"{pm.ref('msrp_'+s, i)}*(1-dtc_disc)", F_USD2, "$", summ=None)
for s, nm in SKUS:
    pm.add(f"ret_{s}", f"Retail sell-in price -- {nm}", lambda i, s=s: f"{pm.ref('msrp_'+s, i)}*(1-retail_margin)", F_USD2, "$", summ=None)
pm.add("pre_px_peb", "Pre-order blended price -- Pebble",
       lambda i: "(ks_units*ks_peb+pre_units*pre_peb)/(ks_units+pre_units)*sc_price", F_USD2, "$", summ=None)
pm.add("pre_px_sq", "Pre-order blended price -- Square",
       lambda i: "(ks_units*ks_sq+pre_units*pre_sq)/(ks_units+pre_units)*sc_price", F_USD2, "$", summ=None)
pm.add("pre_px_atl", "Pre-order blended price -- Atlas",
       lambda i: "(ks_units*ks_atl+pre_units*pre_atl)/(ks_units+pre_units)*sc_price", F_USD2, "$", summ=None)
pm.section("Units")
pm.add("reg_total", "Regular units sold (after scenario)", lambda i: f"{A('reg_units')(i)}*sc_vol", F_NUM, "units")
for s, nm in SKUS:
    pm.add(f"mix_{s}", f"Mix -- {nm}", A(f"mix_{s}"), F_PCT, "%", summ=None)
pm.add("retail_sh", "Retail share", A("retail_share"), F_PCT, "%", summ=None)
for s, nm in SKUS:
    pm.add(f"dtcu_{s}", f"DTC units -- {nm}",
           lambda i, s=s: f"{pm.ref('reg_total', i)}*{pm.ref('mix_'+s, i)}*(1-{pm.ref('retail_sh', i)})", F_NUM, "units")
for s, nm in SKUS:
    pm.add(f"retu_{s}", f"Retail units -- {nm}",
           lambda i, s=s: f"{pm.ref('reg_total', i)}*{pm.ref('mix_'+s, i)}*{pm.ref('retail_sh', i)}", F_NUM, "units")
pm.add("preu_peb", "Pre-order units shipped -- Pebble", lambda i: f"(ks_units+pre_units)*sc_vol*{A('pre_ship_pct')(i)}*pre_mix_peb", F_NUM, "units")
pm.add("preu_sq", "Pre-order units shipped -- Square", lambda i: f"(ks_units+pre_units)*sc_vol*{A('pre_ship_pct')(i)}*(1-pre_mix_peb-pre_mix_atl)", F_NUM, "units")
pm.add("preu_atl", "Pre-order units shipped -- Atlas", lambda i: f"(ks_units+pre_units)*sc_vol*{A('pre_ship_atl')(i)}*pre_mix_atl", F_NUM, "units")
pm.add("pre_total", "Pre-order (KS + late pledge) units shipped",
       lambda i: f"{pm.ref('preu_peb', i)}+{pm.ref('preu_sq', i)}+{pm.ref('preu_atl', i)}", F_NUM, "units")
for s, nm in SKUS:
    pm.add(f"units_{s}", f"Total units shipped -- {nm}",
           (lambda i, s=s: f"{pm.ref('dtcu_'+s, i)}+{pm.ref('retu_'+s, i)}+{pm.ref('preu_'+s, i)}"),
           F_NUM, "units")
pm.add("units_total", "TOTAL UNITS SHIPPED", lambda i: "+".join(pm.ref(f"units_{s}", i) for s, _ in SKUS), F_NUM, "units", total=True)
pm.add("dtcu_total", "DTC regular units", lambda i: "+".join(pm.ref(f"dtcu_{s}", i) for s, _ in SKUS), F_NUM, "units")
pm.add("retu_total", "Retail units", lambda i: "+".join(pm.ref(f"retu_{s}", i) for s, _ in SKUS), F_NUM, "units")
pm.add("cum_units", "Cumulative units shipped",
       lambda i: f"SUM({pm.ref('units_total', 0).split('!')[0]}!${FIRST}{pm.rows['units_total']}:{COLS[i]}{pm.rows['units_total']})",
       F_NUM, "units", summ="last")

# --------------------------------------------------------------------------
# 4. Subscription cohort model
# --------------------------------------------------------------------------
co = TS("Subscription Cohorts", "LORE Pass subscription model -- trial -> paid conversion, churn, ARPU, installed base", summary=True)
co.section("Conversion pipeline")
co.add("units", "Devices shipped (each gets a 3-month Explorer trial)", R(pm, "units_total"), F_NUM, "units")
co.add("conv_base", "Expected paid conversions from this period's devices",
       lambda i: "MIN(1,sc_attach)*0+(" + "+".join(f"{pm.ref('units_'+s, i)}*MIN(1,attach_{s}*sc_attach)" for s, _ in SKUS) + ")",
       F_NUM, "subs")
co.add("attach_w", "Weighted attach rate (after scenario)",
       lambda i: f"IF({co.ref('units', i)}>0,{co.ref('conv_base', i)}/{co.ref('units', i)},0)", F_PCT, "%", summ=None)


def new_paid(i):
    p = PERIODS[i]
    if p["monthly"]:
        lag = SCALARS["trial_months"]
        return co.ref("conv_base", i - lag) if i - lag >= 0 else "0"
    # annual: 75% of own year's conversions + trial pipeline from prior year's last quarter
    if p["year"] == 2029:
        q4 = [i2 for i2 in months_idx(2028)][-3:]
        prior = "+".join(co.ref("conv_base", j) for j in q4)
    else:
        prior = f"{co.ref('conv_base', i - 1)}*0.25"
    return f"{co.ref('conv_base', i)}*0.75+{prior}"


co.add("new_paid", "New paid Explorer subscribers (trial ends)", new_paid, F_NUM, "subs")
co.add("churn_m", "Monthly churn (after scenario)", lambda i: "MIN(0.5,churn*sc_churn)", F_PCT, "%/mo", summ=None)
co.section("Paid subscriber roll-forward")
co.add("beg", "Beginning paid subs", lambda i: "0" if i == 0 else co.ref("end", i - 1) if False else ("0" if i == 0 else f"{q(co.name)}!{COLS[i-1]}{{END}}"), F_NUM, "subs", summ=None)
END_PLACEHOLDER_ROW = co.rows["beg"]


def end_subs(i):
    b, n, c = co.ref("beg", i), co.ref("new_paid", i), co.ref("churn_m", i)
    if PERIODS[i]["monthly"]:
        return f"{b}*(1-{c})+{n}"
    return f"{b}*(1-{c})^12+{n}*(1-(1-{c})^12)/(12*{c})"


co.add("churned", "Churned subs", lambda i: f"{co.ref('beg', i)}+{co.ref('new_paid', i)}-{co.ref('end', i)}" if False else "0", F_NUM, "subs")
CHURN_ROW = co.rows["churned"]
co.add("end", "Ending paid subs", end_subs, F_NUM, "subs", total=True, summ="last")
# fix forward refs
for i, c in enumerate(COLS):
    co.ws[f"{c}{co.rows['beg']}"] = "=0" if i == 0 else f"={COLS[i-1]}{co.rows['end']}"
    co.ws[f"{c}{CHURN_ROW}"] = f"={c}{co.rows['beg']}+{c}{co.rows['new_paid']}-{c}{co.rows['end']}"
co.add("avg_paid", "Average paid subs in period", lambda i: f"({co.ref('beg', i)}+{co.ref('end', i)})/2", F_NUM, "subs", summ="avg")
co.add("paid_months", "Paid subscriber-months", lambda i: f"{co.ref('avg_paid', i)}*Timeline!{COLS[i]}4", F_NUM, "sub-mo")
co.add("arpu", "Realised ARPU per paid sub-month", lambda i: "sub_price*arpu_real*sc_price", F_USD2, "$", summ=None)
co.add("sub_rev", "Subscription revenue (Explorer)", lambda i: f"{co.ref('paid_months', i)}*{co.ref('arpu', i)}", F_USD, "$", total=True)
co.add("arr", "Subscription ARR at period end (ending subs x ARPU x 12)", lambda i: f"{co.ref('end', i)}*{co.ref('arpu', i)}*12", F_USD, "$", summ="last")
co.section("Trials & installed base")


def trial_um(i):
    if PERIODS[i]["monthly"]:
        js = [j for j in range(max(0, i - 2), i + 1)]
        return "+".join(co.ref("units", j) for j in js)
    return f"{co.ref('units', i)}*trial_months"


co.add("trial_um", "Trial user-months (devices inside their free 3 months)", trial_um, F_NUM, "user-mo")
co.add("act_beg", "Active devices -- beginning", lambda i: "0", F_NUM, "devices", summ=None)


def act_end(i):
    b, u = co.ref("act_beg", i), co.ref("units", i)
    if PERIODS[i]["monthly"]:
        return f"{b}*(1-device_inactive)+{u}"
    return f"{b}*(1-device_inactive)^12+{u}*(1-(1-device_inactive)^12)/(12*device_inactive)"


co.add("act_end", "Active devices -- ending", act_end, F_NUM, "devices", total=True, summ="last")
for i, c in enumerate(COLS):
    co.ws[f"{c}{co.rows['act_beg']}"] = "=0" if i == 0 else f"={COLS[i-1]}{co.rows['act_end']}"
co.add("act_avg", "Active devices -- average", lambda i: f"({co.ref('act_beg', i)}+{co.ref('act_end', i)})/2", F_NUM, "devices", summ="avg")
co.add("act_months", "Active device-months", lambda i: f"{co.ref('act_avg', i)}*Timeline!{COLS[i]}4", F_NUM, "dev-mo")
co.add("esim_sh", "eSIM device share (Square + Atlas, period mix)",
       lambda i: f"{A('mix_sq')(i)}+{A('mix_atl')(i)}", F_PCT, "%", summ=None)
co.add("free_months", "Free-tier device-months (active, not paying, not in trial)",
       lambda i: f"MAX(0,{co.ref('act_months', i)}-{co.ref('paid_months', i)}-{co.ref('trial_um', i)})", F_NUM, "dev-mo")
co.add("trips", "Trip Passes sold", lambda i: f"{co.ref('free_months', i)}*{co.ref('esim_sh', i)}*trip_rate", F_NUM, "passes")
co.add("trip_rev", "Trip Pass revenue", lambda i: f"{co.ref('trips', i)}*trip_price*sc_price", F_USD, "$", total=True)
co.add("paid_pct", "Paid subs as % of active devices (end)",
       lambda i: f"IF({co.ref('act_end', i)}>0,{co.ref('end', i)}/{co.ref('act_end', i)},0)", F_PCT, "%", summ=None)

# --------------------------------------------------------------------------
# 5. Cloud / AI COGS
# --------------------------------------------------------------------------
cl = TS("Cloud & AI COGS", "Cloud / AI / data COGS per active user", summary=True)
cl.add("ai_idx", "AI unit-cost index", lambda i: "1" if PERIODS[i]["monthly"] else f"(1-ai_defl)^({PERIODS[i]['year']}-2028)", "0.00", summ=None)
cl.add("data_idx", "Data unit-cost index", lambda i: "1" if PERIODS[i]["monthly"] else f"(1-data_defl)^({PERIODS[i]['year']}-2028)", "0.00", summ=None)
cl.add("cost_paid", "Cost per paid (or trial) user-month",
       lambda i: f"(llm_cost+stt_cost+tts_cost)*{cl.ref('ai_idx', i)}+infra_cost+data_gb_used*data_cost_gb*{cl.ref('data_idx', i)}*{co.ref('esim_sh', i)}",
       F_USD2, "$", summ=None)
cl.add("cost_trip", "Cost per Trip Pass",
       lambda i: f"trip_data_gb*data_cost_gb*{cl.ref('data_idx', i)}+trip_ai*{cl.ref('ai_idx', i)}+sub_pay_fee*trip_price*sc_price",
       F_USD2, "$", summ=None)
cl.add("c_paid", "Paid subscribers: AI + data + infra", lambda i: f"{co.ref('paid_months', i)}*{cl.ref('cost_paid', i)}", F_USD)
cl.add("c_bill", "Subscription billing fees", lambda i: f"{co.ref('sub_rev', i)}*sub_pay_fee", F_USD)
cl.add("c_trial", "Trial users (3 free months)", lambda i: f"{co.ref('trial_um', i)}*{cl.ref('cost_paid', i)}", F_USD)
cl.add("c_free", "Free-tier devices", lambda i: f"{co.ref('free_months', i)}*free_cost", F_USD)
cl.add("c_trip", "Trip Passes", lambda i: f"{co.ref('trips', i)}*{cl.ref('cost_trip', i)}", F_USD)
cl.add("c_fleet", "B2B fleet devices", lambda i: f"(Timeline!{COLS[i]}4)*0+{{FLEETAVG}}*fleet_cloud*Timeline!{COLS[i]}4", F_USD)
FLEET_CLOUD_ROW = cl.rows["c_fleet"]
cl.add("c_total", "TOTAL CLOUD / AI / DATA COGS", lambda i: "+".join(cl.ref(k, i) for k in ["c_paid", "c_bill", "c_trial", "c_free", "c_trip", "c_fleet"]), F_USD, total=True)
cl.add("per_active", "Cloud COGS per active device-month",
       lambda i: f"IF({co.ref('act_months', i)}>0,{cl.ref('c_total', i)}/{co.ref('act_months', i)},0)", F_USD2, "$", summ=None)
cl.add("sub_gm", "Subscription gross margin (Explorer + Trip Pass, excl. trial & free)",
       lambda i: f"IF(({co.ref('sub_rev', i)}+{co.ref('trip_rev', i)})>0,1-({cl.ref('c_paid', i)}+{cl.ref('c_bill', i)}+{cl.ref('c_trip', i)})/({co.ref('sub_rev', i)}+{co.ref('trip_rev', i)}),0)",
       F_PCT, "%", summ=None)

# --------------------------------------------------------------------------
# 6. Revenue build
# --------------------------------------------------------------------------
rv = TS("Revenue Build", "Revenue build by stream", summary=True)
rv.section("Hardware")
rv.add("hw_dtc", "Hardware -- DTC (web/app)",
       lambda i: "+".join(f"{pm.ref('dtcu_'+s, i)}*{pm.ref('dtc_'+s, i)}" for s, _ in SKUS), F_USD)
rv.add("hw_ret", "Hardware -- retail / wholesale (sell-in)",
       lambda i: "+".join(f"{pm.ref('retu_'+s, i)}*{pm.ref('ret_'+s, i)}" for s, _ in SKUS), F_USD)
rv.add("hw_pre", "Hardware -- Kickstarter / pre-orders (recognised on shipment)",
       lambda i: "+".join(f"{pm.ref('preu_'+k, i)}*{pm.ref('pre_px_'+k, i)}" for k in ("peb", "sq", "atl")), F_USD)
rv.add("hw_gross", "Gross hardware revenue", lambda i: f"{rv.ref('hw_dtc', i)}+{rv.ref('hw_ret', i)}+{rv.ref('hw_pre', i)}", F_USD)
rv.add("hw_returns", "Less: returns & refunds allowance", lambda i: f"-{rv.ref('hw_gross', i)}*returns_pct", F_USD)
rv.add("hw_net", "Net hardware revenue", lambda i: f"{rv.ref('hw_gross', i)}+{rv.ref('hw_returns', i)}", F_USD, total=True)
rv.section("Recurring & other")
rv.add("subs", "Subscriptions -- LORE Pass Explorer", R(co, "sub_rev"), F_USD)
rv.add("trip", "Subscriptions -- Trip Pass", R(co, "trip_rev"), F_USD)
rv.add("acc", "Accessories (LORE Kit)", lambda i: f"{pm.ref('units_total', i)}*acc_attach*acc_aov*sc_price", F_USD)
rv.add("aff", "Affiliate bookings (hotels, tours, restaurants)", lambda i: f"{co.ref('act_months', i)}*{A('affiliate_rate')(i)}", F_USD)
rv.add("fleet_avg", "B2B fleet devices -- average deployed",
       lambda i: f"({A('fleet_end')(i)}+{('0' if i == 0 else A('fleet_end')(i-1))})/2", F_NUM, "devices", summ="avg")
rv.add("fleet", "B2B fleet rental", lambda i: f"{rv.ref('fleet_avg', i)}*fleet_fee*Timeline!{COLS[i]}4", F_USD)
rv.add("total", "TOTAL REVENUE", lambda i: "+".join(rv.ref(k, i) for k in ["hw_net", "subs", "trip", "acc", "aff", "fleet"]), F_USD, total=True)
rv.add("recurring", "Recurring revenue (subs + trip + fleet)", lambda i: f"{rv.ref('subs', i)}+{rv.ref('trip', i)}+{rv.ref('fleet', i)}", F_USD)
rv.add("rec_pct", "Recurring share of revenue",
       lambda i: f"IF({rv.ref('total', i)}>0,{rv.ref('recurring', i)}/{rv.ref('total', i)},0)", F_PCT, "%",
       summ=lambda k, fy: f"IF({SUMCOLS[k]}{rv.rows['total']}>0,{SUMCOLS[k]}{rv.rows['recurring']}/{SUMCOLS[k]}{rv.rows['total']},0)")
# patch fleet cloud cost now that fleet_avg exists
for i, c in enumerate(COLS):
    cl.ws[f"{c}{FLEET_CLOUD_ROW}"] = f"={rv.ref('fleet_avg', i)}*fleet_cloud*Timeline!{c}4"

# --------------------------------------------------------------------------
# 7. Hardware COGS
# --------------------------------------------------------------------------
hc = TS("Hardware COGS", "Hardware & accessory COGS (landed) + fulfilment", summary=True)
for s, nm in SKUS:
    hc.add(f"landed_{s}", f"Landed cost per unit -- {nm}",
           lambda i, s=s: f"(bom_{s}+asm_{s}+pkg_{s})*(1+freight_duty)*" + (A('sq_index')(i) if s == "sq" else A('cogs_index')(i)) + "*sc_cogs", F_USD2, "$", summ=None)
hc.add("product", "Product landed cost (units x landed)",
       lambda i: "+".join(f"{pm.ref('units_'+s, i)}*{hc.ref('landed_'+s, i)}" for s, _ in SKUS), F_USD)
hc.add("fulfil", "Fulfilment & outbound logistics",
       lambda i: f"{pm.ref('dtcu_total', i)}*dtc_ship+{pm.ref('retu_total', i)}*retail_dist+{pm.ref('pre_total', i)}*ks_fulfil_net", F_USD)
hc.add("payproc", "DTC card processing", lambda i: f"{rv.ref('hw_dtc', i)}*pay_pct+{pm.ref('dtcu_total', i)}*pay_fixed", F_USD)
hc.add("warranty", "Warranty reserve", lambda i: f"{rv.ref('hw_gross', i)}*warranty_pct", F_USD)
hc.add("hw_cogs", "HARDWARE COGS", lambda i: "+".join(hc.ref(k, i) for k in ["product", "fulfil", "payproc", "warranty"]), F_USD, total=True)
hc.add("acc_cogs", "Accessories COGS", lambda i: f"{rv.ref('acc', i)}*acc_cogs_pct", F_USD)
hc.add("hw_gm", "Hardware gross margin %",
       lambda i: f"IF({rv.ref('hw_net', i)}>0,1-{hc.ref('hw_cogs', i)}/{rv.ref('hw_net', i)},0)", F_PCT, "%",
       summ=lambda k, fy: f"IF({rv.sref('hw_net', k)}>0,1-{SUMCOLS[k]}{hc.rows['hw_cogs']}/{rv.sref('hw_net', k)},0)")

# --------------------------------------------------------------------------
# 8. Headcount
# --------------------------------------------------------------------------
hcws = wb.create_sheet("Headcount")
hcws["A1"] = "Headcount plan -- roles, start month, base salary (blue = input). Burden & inflation from Assumptions."
hcws["A1"].font = TITLE
ROLES = [
    # role, dept, count, start (y,m), salary, note
    ("Founder & CEO (Nimit Jain)", "G&A", 1, (2026, 11), 90000, "Below-market founder salary until seed."),
    ("Founding Eng -- Embedded / firmware", "R&D", 1, (2026, 11), 150000, ""),
    ("Founding Eng -- AI / story engine", "R&D", 1, (2026, 12), 160000, ""),
    ("Founding Eng -- mobile app / backend", "R&D", 1, (2027, 1), 140000, ""),
    ("Hardware lead (systems/EE, ODM mgmt)", "R&D", 1, (2027, 1), 165000, ""),
    ("Community & Kickstarter lead", "S&M", 1, (2027, 2), 95000, ""),
    ("Content editor / historian (City Packs)", "R&D", 1, (2027, 3), 75000, "Fact-checked stories w/ sources."),
    ("Head of operations & supply chain", "Ops & CS", 1, (2027, 8), 160000, "Seed hire."),
    ("Firmware engineer #2", "R&D", 1, (2027, 8), 140000, ""),
    ("Map Vision / sensor-fusion engineer", "R&D", 1, (2027, 9), 160000, ""),
    ("Product designer (device + app UX)", "R&D", 1, (2027, 9), 125000, ""),
    ("Customer support lead", "Ops & CS", 1, (2027, 10), 65000, ""),
    ("Growth marketing manager", "S&M", 1, (2027, 10), 120000, ""),
    ("Finance & ops manager / controller", "G&A", 1, (2027, 11), 110000, ""),
    ("Backend / cloud engineer", "R&D", 1, (2028, 1), 150000, ""),
    ("Mechanical engineer", "R&D", 1, (2028, 1), 140000, ""),
    ("Content editors", "R&D", 2, (2028, 2), 70000, "20 cities in 2028."),
    ("Customer support agents", "Ops & CS", 2, (2028, 3), 50000, ""),
    ("Retail & partnerships manager", "S&M", 1, (2028, 3), 120000, ""),
    ("B2B fleet sales lead", "S&M", 1, (2028, 4), 110000, ""),
    ("QA / test engineer", "R&D", 1, (2028, 4), 115000, ""),
    ("ML engineer #2 (on-device models)", "R&D", 1, (2028, 6), 165000, ""),
    ("Brand & content marketer", "S&M", 1, (2028, 6), 100000, ""),
    ("People & office ops", "G&A", 1, (2028, 9), 85000, ""),
    ("VP Engineering", "R&D", 1, (2028, 11), 210000, "Series A hire."),
    ("Customer support agents", "Ops & CS", 3, (2028, 11), 50000, "Holiday peak."),
    ("VP Marketing", "S&M", 1, (2029, 2), 200000, ""),
    ("R&D engineers (Gen-2, platform)", "R&D", 8, (2029, 3), 155000, ""),
    ("Content editors (30 new cities)", "R&D", 4, (2029, 3), 72000, ""),
    ("S&M team (performance, retail, EU/APAC)", "S&M", 5, (2029, 4), 110000, ""),
    ("Ops / supply-chain / quality", "Ops & CS", 3, (2029, 4), 100000, ""),
    ("Customer support agents", "Ops & CS", 6, (2029, 6), 50000, ""),
    ("G&A (finance, legal, people)", "G&A", 3, (2029, 6), 110000, ""),
    ("CFO", "G&A", 1, (2029, 9), 230000, ""),
    ("R&D engineers", "R&D", 10, (2030, 3), 160000, ""),
    ("Content editors", "R&D", 4, (2030, 3), 75000, ""),
    ("S&M team", "S&M", 6, (2030, 3), 115000, ""),
    ("Ops / CS", "Ops & CS", 8, (2030, 5), 60000, ""),
    ("G&A", "G&A", 3, (2030, 5), 120000, ""),
    ("R&D engineers", "R&D", 10, (2031, 3), 165000, ""),
    ("S&M team", "S&M", 6, (2031, 3), 120000, ""),
    ("Ops / CS", "Ops & CS", 10, (2031, 4), 60000, ""),
    ("G&A", "G&A", 3, (2031, 4), 125000, ""),
]
for j, h in enumerate(["Role", "Dept", "Count", "Start month", "Base salary ($/yr)", "Note"]):
    c = hcws.cell(3, 1 + j, h)
    c.font, c.fill = HDR, HDRFILL
for k, (role, dept, cnt, (yy, mm), sal, note) in enumerate(ROLES):
    r = 4 + k
    hcws.cell(r, 1, role)
    for col, v, fmt in [(2, dept, None), (3, cnt, "0"), (4, dt.date(yy, mm, 1), "mmm-yy"), (5, sal, "#,##0")]:
        c = hcws.cell(r, col, v)
        c.font, c.fill = BLUE, INFILL
        if fmt:
            c.number_format = fmt
    hcws.cell(r, 6, note).font = NOTE
R0, R1 = 4, 4 + len(ROLES) - 1
hcws.column_dimensions["A"].width = 44
hcws.column_dimensions["D"].width = 11
hcws.column_dimensions["E"].width = 14
hcws.column_dimensions["F"].width = 30

# calc block on a TS sheet
hp = TS("Headcount Plan", "Headcount & personnel cost by period (formulas from 'Headcount' role table)", summary=True)
hp.section("End-of-period headcount by role")
for k in range(len(ROLES)):
    r = R0 + k

    def fte(i, r=r):
        p = PERIODS[i]
        if p["monthly"]:
            return f"IF(Headcount!$D${r}<=Timeline!{COLS[i]}5,Headcount!$C${r},0)"
        return f"IF(Headcount!$D${r}<=DATE({p['year']},12,31),Headcount!$C${r},0)"
    hp.add(f"hc{k}", f"=Headcount!A{r}", fte, F_NUM, summ="last")
    hp.ws.cell(hp.rows[f"hc{k}"], 1).value = f"=Headcount!A{r}"
    hp.ws.cell(hp.rows[f"hc{k}"], 2).value = f"=Headcount!B{r}"
HC_FIRST, HC_LAST = hp.rows["hc0"], hp.rows[f"hc{len(ROLES)-1}"]
hp.section("Personnel cost by role (salary x (1+burden) x inflation)")
for k in range(len(ROLES)):
    r = R0 + k

    def cost(i, r=r):
        p = PERIODS[i]
        infl = f"(1+salary_infl)^MAX(0,{p['year']}-2027)"
        if p["monthly"]:
            return f"IF(Headcount!$D${r}<=Timeline!{COLS[i]}5,Headcount!$C${r}*Headcount!$E${r}/12*(1+burden)*{infl},0)"
        return (f"Headcount!$C${r}*Headcount!$E${r}*(1+burden)*{infl}*"
                f"MAX(0,MIN(12,({p['year']}-YEAR(Headcount!$D${r}))*12+13-MONTH(Headcount!$D${r})))/12")
    hp.add(f"pc{k}", "", cost, F_USD)
    hp.ws.cell(hp.rows[f"pc{k}"], 1).value = f"=Headcount!A{r}"
    hp.ws.cell(hp.rows[f"pc{k}"], 2).value = f"=Headcount!B{r}"
PC_FIRST, PC_LAST = hp.rows["pc0"], hp.rows[f"pc{len(ROLES)-1}"]
hp.section("Summary by department")
DEPTS = ["R&D", "S&M", "Ops & CS", "G&A"]
for d in DEPTS:
    hp.add(f"hcd_{d}", f"Headcount -- {d}",
           lambda i, d=d: f"SUMIF($B${HC_FIRST}:$B${HC_LAST},\"{d}\",{COLS[i]}{HC_FIRST}:{COLS[i]}{HC_LAST})", F_NUM, summ="last")
hp.add("hc_total", "TOTAL HEADCOUNT (end of period)", lambda i: "+".join(hp.ref(f"hcd_{d}", i) for d in DEPTS), F_NUM, total=True, summ="last")
for d in DEPTS:
    hp.add(f"pcd_{d}", f"Personnel cost -- {d}",
           lambda i, d=d: f"SUMIF($B${PC_FIRST}:$B${PC_LAST},\"{d}\",{COLS[i]}{PC_FIRST}:{COLS[i]}{PC_LAST})", F_USD)
hp.add("pc_total", "TOTAL PERSONNEL COST", lambda i: "+".join(hp.ref(f"pcd_{d}", i) for d in DEPTS), F_USD, total=True)

# --------------------------------------------------------------------------
# 9. Working capital & capex
# --------------------------------------------------------------------------
wc = TS("Working Capital", "Working capital: ODM deposits, inventory, retail AR, Kickstarter deferred revenue, capex", summary=True)
wc.section("Inventory & ODM payments")
wc.add("prod", "Product landed cost recognised (COGS)", R(hc, "product"), F_USD)


def prod_future(i, k):
    """landed cost of units shipped in period i+k (monthly), annual/12 beyond Dec-28."""
    j = i + k
    if j < NM:
        return hc.ref("product", j)
    return f"{hc.ref('product', NM)}/12"


def purchases(i):
    p = PERIODS[i]
    if p["monthly"]:
        dl, bl = int(SCALARS["dep_lead"]), int(SCALARS["bal_lead"])
        return f"odm_dep*{prod_future(i, dl)}+(1-odm_dep)*{prod_future(i, bl)}"
    return f"{wc.ref('prod', i)}+{wc.ref('inv', i)}-{wc.ref('inv', i-1)}"


wc.add("purch", "Cash paid to ODM (30% deposit at t-3, 70% at t-1)", lambda i: "0", F_USD)
wc.add("inv", "Inventory incl. ODM prepayments (end)", lambda i: "0", F_USD, summ="last")
for i, c in enumerate(COLS):
    p = PERIODS[i]
    wc.ws[f"{c}{wc.rows['purch']}"] = "=" + purchases(i)
    if p["monthly"]:
        prev = "0" if i == 0 else f"{COLS[i-1]}{wc.rows['inv']}"
        wc.ws[f"{c}{wc.rows['inv']}"] = f"={prev}+{c}{wc.rows['purch']}-{c}{wc.rows['prod']}"
    else:
        wc.ws[f"{c}{wc.rows['inv']}"] = f"={c}{wc.rows['prod']}*inv_days/365"
wc.section("Receivables")
wc.add("ar", "Retail accounts receivable (end)",
       lambda i: f"{rv.ref('hw_ret', i)}*(1-returns_pct)*" + ("ar_days/30" if PERIODS[i]["monthly"] else "ar_days/365"),
       F_USD, summ="last")
wc.section("Kickstarter / pre-order deferred revenue")
wc.add("pre_cash", "Pre-order cash collected (gross pledges)",
       lambda i: f"(ks_units+pre_units)*sc_vol*{A('pre_collect_pct')(i)}*(pre_mix_peb*{pm.ref('pre_px_peb', i)}+(1-pre_mix_peb-pre_mix_atl)*{pm.ref('pre_px_sq', i)}+pre_mix_atl*{pm.ref('pre_px_atl', i)})",
       F_USD)
wc.add("pre_rev", "Pre-order revenue recognised on shipment", R(rv, "hw_pre"), F_USD)
wc.add("deferred", "Deferred revenue -- pre-orders (end)",
       lambda i: f"{'0' if i == 0 else wc.ref('deferred', i-1)}+{wc.ref('pre_cash', i)}-{wc.ref('pre_rev', i)}" if False else "0",
       F_USD, summ="last")
for i, c in enumerate(COLS):
    prev = "0" if i == 0 else f"{COLS[i-1]}{wc.rows['deferred']}"
    wc.ws[f"{c}{wc.rows['deferred']}"] = f"={prev}+{c}{wc.rows['pre_cash']}-{c}{wc.rows['pre_rev']}"
wc.add("ks_fees", "Crowdfunding platform + processing fees (expensed in S&M)",
       lambda i: f"{wc.ref('pre_cash', i)}*(ks_fee+ks_proc)+(ks_units+pre_units)*sc_vol*{A('pre_collect_pct')(i)}/units_per_pledge*ks_proc_fixed",
       F_USD)
wc.section("Capex & depreciation (3-year straight line)")
wc.add("cap_tool", "Capex -- tooling & fixtures", A("tooling"), F_USD)


def fleet_capex(i):
    p = PERIODS[i]
    cur = A("fleet_end")(i)
    prv = "0" if i == 0 else A("fleet_end")(i - 1)
    if p["monthly"]:
        return f"(MAX(0,{cur}-{prv})+{prv}*fleet_replace)*fleet_unit_cost"
    return f"(MAX(0,{cur}-{prv})+({cur}+{prv})/2*fleet_replace*12)*fleet_unit_cost"


wc.add("cap_fleet", "Capex -- B2B fleet devices", fleet_capex, F_USD)
wc.add("capex", "TOTAL CAPEX", lambda i: f"{wc.ref('cap_tool', i)}+{wc.ref('cap_fleet', i)}", F_USD, total=True)


def ycap(year):
    """capex in a calendar year as formula (sum of monthly cols or annual col)."""
    idx = [j for j, p in enumerate(PERIODS) if p["year"] == year]
    if not idx:
        return "0"
    return f"SUM({wc.ref('capex', idx[0])}:{COLS[idx[-1]]}{wc.rows['capex']})"


def dep(i):
    p = PERIODS[i]
    ppe_prev = "0" if i == 0 else wc.ref("ppe", i - 1)
    if p["monthly"]:
        raw = "0" if i == 0 else f"SUM({wc.ref('capex', 0)}:{COLS[i-1]}{wc.rows['capex']})/36"
    else:
        Y = p["year"]
        raw = f"({ycap(Y)}*0.5+{ycap(Y-1)}+{ycap(Y-2)}+{ycap(Y-3)}*0.5)/3"
    return f"MIN({raw},{ppe_prev}+{wc.ref('capex', i)})"


wc.add("dep", "Depreciation", lambda i: "0", F_USD)
wc.add("ppe", "PP&E, net (end)", lambda i: "0", F_USD, summ="last")
for i, c in enumerate(COLS):
    wc.ws[f"{c}{wc.rows['dep']}"] = "=" + dep(i)
    prev = "0" if i == 0 else f"{COLS[i-1]}{wc.rows['ppe']}"
    wc.ws[f"{c}{wc.rows['ppe']}"] = f"={prev}+{c}{wc.rows['capex']}-{c}{wc.rows['dep']}"

# --------------------------------------------------------------------------
# 10. OpEx
# --------------------------------------------------------------------------
ox = TS("OpEx", "Operating expenses: R&D (incl. NRE), S&M, Operations & CS, G&A", summary=True)
ox.section("Research & development")
ox.add("rd_pc", "R&D personnel", R(hp, "pcd_R&D"), F_USD)
for key, lab in [("nre_id", "ID / ME / CMF design"), ("nre_odm", "ODM engineering NRE"), ("nre_proto", "Prototype builds"),
                 ("nre_cert", "Certification & compliance testing"), ("nre_content", "City Pack content & data licences"),
                 ("nre_sw", "Dev tools & ML compute")]:
    ox.add(key, lab, A(key), F_USD)
ox.add("rd", "TOTAL R&D", lambda i: "+".join(ox.ref(k, i) for k in ["rd_pc", "nre_id", "nre_odm", "nre_proto", "nre_cert", "nre_content", "nre_sw"]), F_USD, total=True)
ox.section("Sales & marketing")
ox.add("sm_pc", "S&M personnel", R(hp, "pcd_S&M"), F_USD)
ox.add("paid", "Paid acquisition (CAC x DTC regular units)", lambda i: f"{pm.ref('dtcu_total', i)}*{A('cac')(i)}*sc_cac", F_USD)
ox.add("ks_mkt", "Kickstarter pre-launch & campaign marketing", A("ks_mkt"), F_USD)
ox.add("ks_fees", "Crowdfunding platform & processing fees", R(wc, "ks_fees"), F_USD)
ox.add("brand", "Brand, content, PR & events", A("brand_mkt"), F_USD)
ox.add("coop", "Retail co-op / MDF / displays", lambda i: f"{rv.ref('hw_ret', i)}*retail_coop", F_USD)
ox.add("sm", "TOTAL S&M", lambda i: "+".join(ox.ref(k, i) for k in ["sm_pc", "paid", "ks_mkt", "ks_fees", "brand", "coop"]), F_USD, total=True)
ox.section("Operations & customer support")
ox.add("ops", "Ops & CS personnel", R(hp, "pcd_Ops & CS"), F_USD, total=True)
ox.section("General & administrative")
ox.add("ga_pc", "G&A personnel", R(hp, "pcd_G&A"), F_USD)
ox.add("ga_other", "G&A non-personnel", A("ga_other"), F_USD)
ox.add("ga", "TOTAL G&A", lambda i: f"{ox.ref('ga_pc', i)}+{ox.ref('ga_other', i)}", F_USD, total=True)
ox.add("opex", "TOTAL OPEX", lambda i: "+".join(ox.ref(k, i) for k in ["rd", "sm", "ops", "ga"]), F_USD, total=True)
ox.add("nre_total", "memo: NRE subtotal (ID, ODM, proto, cert)", lambda i: "+".join(ox.ref(k, i) for k in ["nre_id", "nre_odm", "nre_proto", "nre_cert"]), F_USD)

# --------------------------------------------------------------------------
# 11. Funding rounds (inputs) -- needed by cash flow
# --------------------------------------------------------------------------
fr = wb.create_sheet("Funding & Runway")
fr["A1"] = "Funding rounds & runway (blue = input). Period key = YYYYMM for monthly, YYYY for FY2029+."
fr["A1"].font = TITLE
for j, h in enumerate(["Round", "Instrument", "Period key", "Amount ($)", "Pre-money ($)", "Post-money ($)", "Notes"]):
    c = fr.cell(3, 1 + j, h)
    c.font, c.fill = HDR, HDRFILL
ROUNDS = [
    ("Pre-seed", "Post-money SAFE", 202611, 1500000, None, 12000000, "COMPANY.md: $1.5M SAFE at $12M post-money cap."),
    ("Seed", "Priced (Series Seed Preferred)", 202708, 6000000, 22000000, None, "After Kickstarter (COMPANY.md: $6M). Pre-money is a CFO estimate."),
    ("Seed extension", "Seed-2 preferred (priced at step-up to Seed)", 202803, OVERRIDES.get("seedx_amt", 3000000), 36000000, None, "CFO addition: bridges Mar-Sep 2028 (inventory for first retail + Atlas). Alternative: $3M inventory/venture-debt facility."),
    ("Series A", "Priced preferred", 202809, OVERRIDES.get("seriesA_amt", 25000000), 80000000, None, "Post-holiday 2028 traction; $100M post-money is the target (see valuation.md)."),
    ("Series B", "Priced preferred", 2030, OVERRIDES.get("seriesB_amt", 20000000), 230000000, None, "Growth / inventory for retail scale; sized to keep min cash > ~6 months of burn."),
]
for k, (nm, ins, key, amt, pre, post, note) in enumerate(ROUNDS):
    r = 4 + k
    fr.cell(r, 1, nm).font = BOLD
    fr.cell(r, 2, ins)
    for col, v in [(3, key), (4, amt)]:
        c = fr.cell(r, col, v)
        c.font, c.fill = BLUE, INFILL
    fr.cell(r, 4).number_format = "#,##0"
    if pre is None:  # SAFE: post-money cap input
        c = fr.cell(r, 6, post)
        c.font, c.fill, c.number_format = BLUE, INFILL, "#,##0"
        fr.cell(r, 5, f"=F{r}-D{r}").number_format = "#,##0"
    else:
        c = fr.cell(r, 5, pre)
        c.font, c.fill, c.number_format = BLUE, INFILL, "#,##0"
        fr.cell(r, 6, f"=E{r}+D{r}").number_format = "#,##0"
    fr.cell(r, 7, note).font = NOTE
FR_KEYS, FR_AMT = "'Funding & Runway'!$C$4:$C$8", "'Funding & Runway'!$D$4:$D$8"
for col, w in zip("ABCDEFG", [16, 30, 12, 14, 15, 15, 90]):
    fr.column_dimensions[col].width = w

# --------------------------------------------------------------------------
# 12. P&L
# --------------------------------------------------------------------------
pl = TS("P&L", "Income statement", summary=True)
pl.section("Revenue")
for k, lab in [("hw_net", "Hardware (net of returns)"), ("subs", "Subscriptions -- Explorer"), ("trip", "Subscriptions -- Trip Pass"),
               ("acc", "Accessories"), ("aff", "Affiliate"), ("fleet", "B2B fleet rental")]:
    pl.add(k, lab, R(rv, k), F_USD)
pl.add("rev", "TOTAL REVENUE", lambda i: f"SUM({COLS[i]}{pl.rows['hw_net']}:{COLS[i]}{pl.rows['fleet']})", F_USD, total=True)
pl.section("Cost of revenue")
pl.add("c_hw", "Hardware COGS (landed, fulfilment, payments, warranty)", R(hc, "hw_cogs"), F_USD)
pl.add("c_acc", "Accessories COGS", R(hc, "acc_cogs"), F_USD)
pl.add("c_cloud", "Cloud / AI / data COGS", R(cl, "c_total"), F_USD)
pl.add("cogs", "TOTAL COST OF REVENUE", lambda i: f"{pl.ref('c_hw', i)}+{pl.ref('c_acc', i)}+{pl.ref('c_cloud', i)}", F_USD, total=True)
pl.add("gp", "GROSS PROFIT", lambda i: f"{pl.ref('rev', i)}-{pl.ref('cogs', i)}", F_USD, total=True)


def ratio(num, den, sheet=pl):
    return dict(f=lambda i: f"IF({sheet.ref(den, i)}<>0,{sheet.ref(num, i)}/{sheet.ref(den, i)},0)",
                summ=lambda k, fy: f"IF({SUMCOLS[k]}{sheet.rows[den]}<>0,{SUMCOLS[k]}{sheet.rows[num]}/{SUMCOLS[k]}{sheet.rows[den]},0)")


g = ratio("gp", "rev")
pl.add("gm", "Gross margin %", g["f"], F_PCT, "%", summ=g["summ"])
pl.section("Operating expenses")
for k, lab in [("rd", "Research & development (incl. NRE)"), ("sm", "Sales & marketing"), ("ops", "Operations & customer support"), ("ga", "General & administrative")]:
    pl.add(k, lab, R(ox, k), F_USD)
pl.add("opex", "TOTAL OPEX", lambda i: f"SUM({COLS[i]}{pl.rows['rd']}:{COLS[i]}{pl.rows['ga']})", F_USD, total=True)
pl.add("ebitda", "EBITDA", lambda i: f"{pl.ref('gp', i)}-{pl.ref('opex', i)}", F_USD, total=True)
e = ratio("ebitda", "rev")
pl.add("ebitda_m", "EBITDA margin %", e["f"], F_PCT, "%", summ=e["summ"])
pl.add("da", "Depreciation", R(wc, "dep"), F_USD)
pl.add("ebit", "EBIT", lambda i: f"{pl.ref('ebitda', i)}-{pl.ref('da', i)}", F_USD)
pl.add("int", "Interest income on cash", lambda i: "0", F_USD)
pl.add("pbt", "Pre-tax income", lambda i: f"{pl.ref('ebit', i)}+{pl.ref('int', i)}", F_USD)
pl.add("cum_pbt", "memo: cumulative pre-tax income", lambda i: f"SUM(${FIRST}{pl.rows['pbt']}:{COLS[i]}{pl.rows['pbt']})", F_USD, summ="last")
pl.add("tax", "Income tax (after NOL usage)",
       lambda i: f"IF({pl.ref('cum_pbt', i)}>0,MAX(0,MIN({pl.ref('pbt', i)},{pl.ref('cum_pbt', i)}))*tax_rate,0)", F_USD)
pl.add("ni", "NET INCOME", lambda i: f"{pl.ref('pbt', i)}-{pl.ref('tax', i)}", F_USD, total=True)
pl.add("eb_cum", "memo: count of periods with positive EBITDA", lambda i: f"COUNTIF(${FIRST}{pl.rows['ebitda']}:{COLS[i]}{pl.rows['ebitda']},\">0\")", F_NUM,
       summ=lambda k, fy: "+".join(f"IF({SUMCOLS[j]}{pl.rows['ebitda']}>0,1,0)" for j in range(k + 1)))
pl.section("Key ratios & memo")
pl.add("hw_gm", "Hardware gross margin %", R(hc, "hw_gm"), F_PCT, "%",
       summ=lambda k, fy: f"{hc.sref('hw_gm', k)}")
pl.add("units", "Units shipped", R(pm, "units_total"), F_NUM, "units")
pl.add("subs_end", "Paid subscribers (end)", R(co, "end"), F_NUM, "subs", summ="last")
pl.add("arr", "Subscription ARR (end)", R(co, "arr"), F_USD, summ="last")
pl.add("hc", "Headcount (end)", R(hp, "hc_total"), F_NUM, summ="last")

# --------------------------------------------------------------------------
# 13. Cash flow
# --------------------------------------------------------------------------
cf = TS("Cash Flow", "Cash flow statement (indirect)", summary=True)
cf.section("Operating")
cf.add("ni", "Net income", R(pl, "ni"), F_USD)
cf.add("da", "Add: depreciation", R(wc, "dep"), F_USD)
cf.add("d_ar", "(Increase)/decrease in receivables", lambda i: f"{'0' if i == 0 else wc.ref('ar', i-1)}-{wc.ref('ar', i)}", F_USD)
cf.add("d_inv", "(Increase)/decrease in inventory & ODM deposits", lambda i: f"{'0' if i == 0 else wc.ref('inv', i-1)}-{wc.ref('inv', i)}", F_USD)
cf.add("d_def", "Increase/(decrease) in pre-order deferred revenue", lambda i: f"{wc.ref('deferred', i)}-{'0' if i == 0 else wc.ref('deferred', i-1)}", F_USD)
cf.add("cfo", "CASH FROM OPERATIONS", lambda i: f"SUM({COLS[i]}{cf.rows['ni']}:{COLS[i]}{cf.rows['d_def']})", F_USD, total=True)
cf.section("Investing")
cf.add("capex", "Capex (tooling + fleet devices)", lambda i: f"-{wc.ref('capex', i)}", F_USD)
cf.add("cfi", "CASH FROM INVESTING", lambda i: cf.ref("capex", i), F_USD, total=True)
cf.section("Financing")
cf.add("equity", "Equity / SAFE proceeds", lambda i: f"SUMIF({FR_KEYS},Timeline!{COLS[i]}6,{FR_AMT})", F_USD)
cf.add("cff", "CASH FROM FINANCING", lambda i: cf.ref("equity", i), F_USD, total=True)
cf.section("Cash")
cf.add("net", "Net change in cash", lambda i: f"{cf.ref('cfo', i)}+{cf.ref('cfi', i)}+{cf.ref('cff', i)}", F_USD, total=True)
cf.add("beg", "Beginning cash", lambda i: "opening_cash" if i == 0 else f"{COLS[i-1]}{{CFEND}}", F_USD,
       summ=lambda k, fy: f"{COLS[[j for j, p in enumerate(PERIODS) if p['year'] == fy][0]]}{cf.rows['beg']}")
cf.add("end", "ENDING CASH", lambda i: f"{cf.ref('beg', i)}+{cf.ref('net', i)}", F_USD, total=True, summ="last")
for i, c in enumerate(COLS):
    if i > 0:
        cf.ws[f"{c}{cf.rows['beg']}"] = f"={COLS[i-1]}{cf.rows['end']}"
cf.add("burn", "Net burn (operating + investing; positive = burning)", lambda i: f"-({cf.ref('cfo', i)}+{cf.ref('cfi', i)})", F_USD)
cf.add("cum_oi", "Cumulative operating + investing cash flow", lambda i: f"SUM(${FIRST}{cf.rows['cfo']}:{COLS[i]}{cf.rows['cfo']})+SUM(${FIRST}{cf.rows['cfi']}:{COLS[i]}{cf.rows['cfi']})", F_USD, summ="last")
cf.add("pos_cum", "memo: count of periods with positive op+inv cash flow", lambda i: f"COUNTIF(${FIRST}{cf.rows['burn']}:{COLS[i]}{cf.rows['burn']},\"<0\")", F_NUM,
       summ=lambda k, fy: "+".join(f"IF({SUMCOLS[j]}{cf.rows['burn']}<0,1,0)" for j in range(k + 1)))
cf.add("burn_m", "Average monthly net burn in period", lambda i: f"{cf.ref('burn', i)}/Timeline!{COLS[i]}4", F_USD, summ=None)
# interest income now (uses beginning cash -> not circular)
for i, c in enumerate(COLS):
    pl.ws[f"{c}{pl.rows['int']}"] = f"=MAX(0,{cf.ref('beg', i)})*interest_rate/12*Timeline!{c}4"

# --------------------------------------------------------------------------
# 14. Balance sheet (light)
# --------------------------------------------------------------------------
bs = TS("Balance Sheet", "Balance sheet (light)", summary=True)
bs.add("cash", "Cash", R(cf, "end"), F_USD, summ="last")
bs.add("ar", "Accounts receivable", R(wc, "ar"), F_USD, summ="last")
bs.add("inv", "Inventory & ODM prepayments", R(wc, "inv"), F_USD, summ="last")
bs.add("ppe", "PP&E, net (tooling, fleet)", R(wc, "ppe"), F_USD, summ="last")
bs.add("ta", "TOTAL ASSETS", lambda i: "+".join(bs.ref(k, i) for k in ["cash", "ar", "inv", "ppe"]), F_USD, total=True, summ="last")
bs.add("def", "Deferred revenue (pre-orders)", R(wc, "deferred"), F_USD, summ="last")
bs.add("tl", "TOTAL LIABILITIES", R(bs, "def"), F_USD, total=True, summ="last")
bs.add("pic", "Paid-in capital (SAFE + preferred)", lambda i: f"opening_cash+SUM({cf.rng('equity', 0, i).split('!')[0]}!${FIRST}{cf.rows['equity']}:{COLS[i]}{cf.rows['equity']})", F_USD, summ="last")
bs.add("re", "Retained earnings / (deficit)", lambda i: f"SUM({q(pl.name)}!${FIRST}{pl.rows['ni']}:{COLS[i]}{pl.rows['ni']})", F_USD, summ="last")
bs.add("te", "TOTAL EQUITY", lambda i: f"{bs.ref('pic', i)}+{bs.ref('re', i)}", F_USD, total=True, summ="last")
bs.add("tle", "TOTAL LIABILITIES + EQUITY", lambda i: f"{bs.ref('tl', i)}+{bs.ref('te', i)}", F_USD, total=True, summ="last")
bs.add("check", "CHECK (assets - L&E), must be 0", lambda i: f"ROUND({bs.ref('ta', i)}-{bs.ref('tle', i)},2)", F_USD2, summ="last")

# --------------------------------------------------------------------------
# 15. Funding & runway metrics (rows under round table)
# --------------------------------------------------------------------------
r0 = 11
fr.cell(r0, 1, "RUNWAY METRICS").font = TITLE
mrng_cash = f"{q(cf.name)}!${FIRST}${cf.rows['end']}:${COLS[NM-1]}${cf.rows['end']}"
mrng_burn = f"{q(cf.name)}!${FIRST}${cf.rows['burn']}:${COLS[NM-1]}${cf.rows['burn']}"
mrng_lab = f"Timeline!${FIRST}$2:${COLS[NM-1]}$2"
arng_cash = f"{q(cf.name)}!${FIRST}${cf.rows['end']}:${LAST}${cf.rows['end']}"
metrics = [
    ("Total equity raised through FY2031", f"=SUM(D4:D8)", F_USD),
    ("Minimum month-end cash, Nov-26..Dec-28", f"=MIN({mrng_cash})", F_USD),
    ("Month of minimum cash", f"=INDEX({mrng_lab},MATCH(MIN({mrng_cash}),{mrng_cash},0))", None),
    ("Minimum period-end cash incl. FY29-31", f"=MIN({arng_cash})", F_USD),
    ("Peak monthly net burn (monthly periods)", f"=MAX({mrng_burn})", F_USD),
    ("Month of peak burn", f"=INDEX({mrng_lab},MATCH(MAX({mrng_burn}),{mrng_burn},0))", None),
    ("Peak average monthly burn (any period incl. FY29-31)", f"=MAX({q(cf.name)}!${FIRST}${cf.rows['burn_m']}:${LAST}${cf.rows['burn_m']})", F_USD),
    ("Peak cumulative op+inv cash outflow (= minimum equity need before buffer)",
     f"=-MIN(0,MIN({q(cf.name)}!${FIRST}${cf.rows['cum_oi']}:${LAST}${cf.rows['cum_oi']}))", F_USD),
    ("First monthly period with positive EBITDA (monthly cols)",
     f"=IFERROR(INDEX({mrng_lab},MATCH(1,{q(pl.name)}!${FIRST}${pl.rows['eb_cum']}:${COLS[NM-1]}${pl.rows['eb_cum']},0)),\"after Dec-28\")", None),
    ("First fiscal year with positive EBITDA",
     f"=IFERROR(INDEX({q(pl.name)}!${SUMCOLS[0]}$3:${SUMCOLS[-1]}$3,MATCH(1,{q(pl.name)}!${SUMCOLS[0]}${pl.rows['eb_cum']}:${SUMCOLS[-1]}${pl.rows['eb_cum']},0)),\"after FY31\")", None),
    ("First fiscal year with positive operating+investing cash flow",
     f"=IFERROR(INDEX({q(cf.name)}!${SUMCOLS[0]}$3:${SUMCOLS[-1]}$3,MATCH(1,{q(cf.name)}!${SUMCOLS[0]}${cf.rows['pos_cum']}:${SUMCOLS[-1]}${cf.rows['pos_cum']},0)),\"after FY31\")", None),
]
FR_MET = {}
for k, (lab, fml, fmt) in enumerate(metrics):
    r = r0 + 1 + k
    fr.cell(r, 1, lab)
    c = fr.cell(r, 4, fml)
    c.font = BOLD
    if fmt:
        c.number_format = fmt
    FR_MET[lab] = r
fr.merge_cells(start_row=r0 + 1, start_column=1, end_row=r0 + 1, end_column=3) if False else None
fr.column_dimensions["A"].width = 62

# runway time series
rw = TS("Runway", "Cash runway by period", summary=False)
rw.add("cash", "Ending cash", R(cf, "end"), F_USD)
rw.add("burn", "Net burn in period", R(cf, "burn"), F_USD)
rw.add("burn3", "Trailing avg monthly burn (3 periods; annual = /12)",
       lambda i: (f"AVERAGE({rw.ref('burn', max(0, i-2))}:{COLS[i]}{rw.rows['burn']})" if PERIODS[i]["monthly"]
                  else f"{rw.ref('burn', i)}/12"), F_USD)
rw.add("runway", "Runway (months of cash at trailing burn)",
       lambda i: f"IF({rw.ref('burn3', i)}>0,{rw.ref('cash', i)}/{rw.ref('burn3', i)},999)", F_NUM1, "months")
rw.add("equity", "Equity raised", R(cf, "equity"), F_USD)

# --------------------------------------------------------------------------
# 16. Cap table
# --------------------------------------------------------------------------
ct = wb.create_sheet("Cap Table")
ct["A1"] = "Cap table -- fully diluted (formulas). Post-money SAFE converts at Seed; pool top-ups are in the pre-money ('option pool shuffle')."
ct["A1"].font = TITLE
ct.column_dimensions["A"].width = 44
for col in "BCDEFGHIJKL":
    ct.column_dimensions[col].width = 14
inp = [("Founder common shares", "ct_founder", 9000000, "#,##0"),
       ("Initial option pool (reserved at formation)", "ct_pool0", 1000000, "#,##0"),
       ("Target unallocated+allocated pool after Seed (% FD post)", "ct_pool_seed", 0.12, "0.0%"),
       ("Target pool after Series A (% FD post)", "ct_pool_A", 0.13, "0.0%"),
       ("Target pool after Series B (% FD post)", "ct_pool_B", 0.12, "0.0%")]
for k, (lab, nm, v, fmt) in enumerate(inp):
    r = 3 + k
    ct.cell(r, 1, lab)
    c = ct.cell(r, 2, v)
    c.font, c.fill, c.number_format = BLUE, INFILL, fmt
    add_name(nm, f"'Cap Table'!$B${r}")
# round refs
SAFE_AMT, SAFE_CAP = "'Funding & Runway'!$D$4", "'Funding & Runway'!$F$4"
SEED_AMT, SEED_PRE = "'Funding & Runway'!$D$5", "'Funding & Runway'!$E$5"
X_AMT, X_PRE = "'Funding & Runway'!$D$6", "'Funding & Runway'!$E$6"
A_AMT, A_PRE = "'Funding & Runway'!$D$7", "'Funding & Runway'!$E$7"
B_AMT, B_PRE = "'Funding & Runway'!$D$8", "'Funding & Runway'!$E$8"
r = 10
ct.cell(r, 1, "Derived share counts").font = BOLD
calc = [
    ("SAFE ownership at conversion (amount / post-money cap)", "ct_safe_pct", f"={SAFE_AMT}/{SAFE_CAP}", "0.00%"),
    ("Company capitalisation incl. SAFE (pre-Seed new money)", "ct_cap_safe", "=(ct_founder+ct_pool0)/(1-ct_safe_pct)", "#,##0"),
    ("SAFE conversion shares", "ct_safe_sh", "=ct_cap_safe*ct_safe_pct", "#,##0"),
    ("Seed: new money % of post", "ct_seed_pct", f"={SEED_AMT}/({SEED_PRE}+{SEED_AMT})", "0.00%"),
    ("Seed: post-money FD shares", "ct_post_seed", "=(ct_founder+ct_safe_sh)/(1-ct_seed_pct-ct_pool_seed)", "#,##0"),
    ("Seed: new preferred shares", "ct_seed_sh", "=ct_post_seed*ct_seed_pct", "#,##0"),
    ("Seed: pool top-up shares", "ct_pool_add_seed", "=ct_post_seed*ct_pool_seed-ct_pool0", "#,##0"),
    ("Seed price per share", "ct_seed_px", f"={SEED_AMT}/ct_seed_sh", "$0.0000"),
    ("SAFE effective price per share", "ct_safe_px", f"={SAFE_AMT}/ct_safe_sh", "$0.0000"),
    ("Seed-2 extension price per share (pre-money / post-Seed FD shares)", "ct_x_px", f"={X_PRE}/ct_post_seed", "$0.0000"),
    ("Seed-2 extension new shares", "ct_x_sh", f"={X_AMT}/ct_x_px", "#,##0"),
    ("Series A: new money % of post", "ct_A_pct", f"={A_AMT}/({A_PRE}+{A_AMT})", "0.00%"),
    ("Series A: post-money FD shares", "ct_post_A", "=(ct_founder+ct_safe_sh+ct_seed_sh+ct_x_sh)/(1-ct_A_pct-ct_pool_A)", "#,##0"),
    ("Series A: new preferred shares", "ct_A_sh", "=ct_post_A*ct_A_pct", "#,##0"),
    ("Series A: pool top-up shares", "ct_pool_add_A", "=ct_post_A*ct_pool_A-ct_post_seed*ct_pool_seed", "#,##0"),
    ("Series A price per share", "ct_A_px", f"={A_AMT}/ct_A_sh", "$0.0000"),
    ("Series B: new money % of post", "ct_B_pct", f"=IF({B_AMT}>0,{B_AMT}/({B_PRE}+{B_AMT}),0)", "0.00%"),
    ("Series B: post-money FD shares", "ct_post_B", "=(ct_founder+ct_safe_sh+ct_seed_sh+ct_x_sh+ct_A_sh)/(1-ct_B_pct-ct_pool_B)", "#,##0"),
    ("Series B: new preferred shares", "ct_B_sh", "=ct_post_B*ct_B_pct", "#,##0"),
    ("Series B: pool top-up shares", "ct_pool_add_B", "=ct_post_B*ct_pool_B-ct_post_A*ct_pool_A", "#,##0"),
    ("Series B price per share", "ct_B_px", f"=IF(ct_B_sh>0,{B_AMT}/ct_B_sh,0)", "$0.0000"),
]
for k, (lab, nm, fml, fmt) in enumerate(calc):
    rr = r + 1 + k
    ct.cell(rr, 1, lab)
    c = ct.cell(rr, 2, fml)
    c.number_format = fmt
    add_name(nm, f"'Cap Table'!$B${rr}")
r = r + len(calc) + 3
ct.cell(r, 1, "Ownership by stage (fully diluted)").font = BOLD
stages = ["Formation", "Post pre-seed SAFE (as-converted)", "Post Seed", "Post Seed-2 + Series A", "Post Series B"]
for j, s in enumerate(stages):
    c1 = ct.cell(r + 1, 2 + 2 * j, s)
    c1.font, c1.fill = HDR, HDRFILL
    ct.cell(r + 2, 2 + 2 * j, "Shares").font = BOLD
    ct.cell(r + 2, 3 + 2 * j, "%").font = BOLD
holders = [
    ("Founder (Nimit Jain)", ["ct_founder", "ct_founder", "ct_founder", "ct_founder", "ct_founder"]),
    ("Option pool (granted + unallocated)", ["ct_pool0", "ct_pool0", "ct_post_seed*ct_pool_seed", "ct_post_A*ct_pool_A", "ct_post_B*ct_pool_B"]),
    ("Pre-seed SAFE investors", ["0", "ct_safe_sh", "ct_safe_sh", "ct_safe_sh", "ct_safe_sh"]),
    ("Seed investors", ["0", "0", "ct_seed_sh", "ct_seed_sh", "ct_seed_sh"]),
    ("Seed-2 extension investors", ["0", "0", "0", "ct_x_sh", "ct_x_sh"]),
    ("Series A investors", ["0", "0", "0", "ct_A_sh", "ct_A_sh"]),
    ("Series B investors", ["0", "0", "0", "0", "ct_B_sh"]),
]
hr0 = r + 3
for k, (h, fs) in enumerate(holders):
    rr = hr0 + k
    ct.cell(rr, 1, h)
    for j, f in enumerate(fs):
        sc_ = ct.cell(rr, 2 + 2 * j, f"={f}")
        sc_.number_format = "#,##0"
tot_r = hr0 + len(holders)
ct.cell(tot_r, 1, "TOTAL FULLY DILUTED").font = BOLD
for j in range(len(stages)):
    colS = CL(2 + 2 * j)
    colP = CL(3 + 2 * j)
    ct[f"{colS}{tot_r}"] = f"=SUM({colS}{hr0}:{colS}{tot_r-1})"
    ct[f"{colS}{tot_r}"].number_format = "#,##0"
    ct[f"{colS}{tot_r}"].font = BOLD
    for rr in range(hr0, tot_r + 1):
        ct[f"{colP}{rr}"] = f"=IF({colS}${tot_r}>0,{colS}{rr}/{colS}${tot_r},0)"
        ct[f"{colP}{rr}"].number_format = "0.0%"
vr = tot_r + 2
ct.cell(vr, 1, "Implied post-money valuation ($)").font = BOLD
ct.cell(vr, 4, f"={SAFE_CAP}").number_format = "#,##0"
ct.cell(vr, 6, f"={SEED_PRE}+{SEED_AMT}").number_format = "#,##0"
ct.cell(vr, 8, f"={A_PRE}+{A_AMT}").number_format = "#,##0"
ct.cell(vr, 10, f"={B_PRE}+{B_AMT}").number_format = "#,##0"
ct.cell(vr + 1, 1, "Founder stake value at round price ($)").font = BOLD
for j, col in [(1, "D"), (2, "F"), (3, "H"), (4, "J")]:
    pcol = CL(3 + 2 * j)
    ct[f"{col}{vr+1}"] = f"={pcol}{hr0}*{col}{vr}"
    ct[f"{col}{vr+1}"].number_format = "#,##0"
ct.cell(vr + 3, 1, "Notes: SAFE = YC post-money SAFE; conversion assumes Seed price > SAFE cap price (true at $22M pre). "
                   "No discount modelled. Liquidation preferences 1x non-participating assumed; not modelled here.").font = NOTE
CAP_HR0, CAP_TOT = hr0, tot_r

# --------------------------------------------------------------------------
# 17. Unit Economics per SKU
# --------------------------------------------------------------------------
ue = wb.create_sheet("Unit Economics", 3)
ue["A1"] = "Unit economics per SKU -- H2-2028 steady-state basis (live). DTC = direct web/app sale; Retail = sell-in to retailer."
ue["A1"].font = TITLE
ue.column_dimensions["A"].width = 58
hdrs = ["Pebble DTC", "Square DTC", "Atlas DTC", "Pebble Retail", "Square Retail", "Atlas Retail"]
for j, h in enumerate(hdrs):
    c = ue.cell(3, 2 + j, h)
    c.font, c.fill = HDR, HDRFILL
    ue.column_dimensions[CL(2 + j)].width = 15
ue.cell(3, 9, "Notes").font = BOLD
ue.column_dimensions["I"].width = 80
ADJ = COLS[idx_of(202806)]  # mid-2028 column for period-specific values
ADJ_C = COLS[idx_of(202812)]  # H2-2028 steady-state cost column
UE = {}


def ue_row(r, label, fn, fmt=F_USD2, note="", bold=False):
    ue.cell(r, 1, label).font = BOLD if bold else Font(name="Inter")
    for j in range(6):
        s = SKUS[j % 3][0]
        ch = "dtc" if j < 3 else "ret"
        v = fn(s, ch, CL(2 + j))
        c = ue.cell(r, 2 + j, f"={v}" if isinstance(v, str) else v)
        c.number_format = fmt
        if bold:
            c.font, c.border = TOTFONT, TOPB
    if note:
        ue.cell(r, 9, note).font = NOTE
    UE[label] = r


rr = 4
lines = [
    ("MSRP", lambda s, ch, c: f"msrp_{s}*sc_price", F_USD2, "", False),
    ("Discount / retailer margin", lambda s, ch, c: f"-B_MSRP*" + ("dtc_disc" if ch == "dtc" else "retail_margin"), F_USD2, "DTC promo vs retailer margin.", False),
    ("Returns allowance", lambda s, ch, c: "-(B_MSRP+B_DISC)*returns_pct", F_USD2, "", False),
    ("Net revenue per unit", lambda s, ch, c: "B_MSRP+B_DISC+B_RET", F_USD2, "", True),
    ("Landed COGS (BOM + assembly + pack + freight/duty)", lambda s, ch, c: f"-'Hardware COGS'!{ADJ_C}{hc.rows['landed_'+s]}", F_USD2, "Dec-2028 landed cost ex-NRE (after D11 Square cost-down & DRAM normalisation).", False),
    ("Fulfilment / distribution", lambda s, ch, c: "-dtc_ship" if ch == "dtc" else "-retail_dist", F_USD2, "", False),
    ("Payment processing", lambda s, ch, c: "-((B_MSRP+B_DISC)*pay_pct+pay_fixed)" if ch == "dtc" else "0", F_USD2, "", False),
    ("Warranty reserve", lambda s, ch, c: "-(B_MSRP+B_DISC)*warranty_pct", F_USD2, "", False),
    ("Hardware gross profit per unit", lambda s, ch, c: "B_NET+B_COGS+B_FUL+B_PAY+B_WAR", F_USD2, "", True),
    ("Hardware gross margin %", lambda s, ch, c: "IF(B_NET>0,B_HWGP/B_NET,0)", F_PCT, "", False),
    ("Acquisition cost (paid CAC DTC; co-op for retail)", lambda s, ch, c: (f"-'Assumptions'!{ADJ}{TSIN['cac']}*sc_cac" if ch == "dtc" else "-(B_MSRP+B_DISC)*retail_coop"), F_USD2, "FY2028 CAC.", False),
    ("Hardware contribution after acquisition", lambda s, ch, c: "B_HWGP+B_CAC", F_USD2, "", True),
    ("Accessories gross profit per device", lambda s, ch, c: "acc_attach*acc_aov*sc_price*(1-acc_cogs_pct)", F_USD2, "", False),
    ("Free 3-month trial cost (cloud)", lambda s, ch, c: f"-trial_months*'Cloud & AI COGS'!{ADJ}{cl.rows['cost_paid']}", F_USD2, "Every device gets 3 months of Explorer.", False),
    ("Paid attach after trial", lambda s, ch, c: f"MIN(1,attach_{s}*sc_attach)", F_PCT, "", False),
    ("Subscription gross profit per paid month", lambda s, ch, c: f"sub_price*arpu_real*sc_price*(1-sub_pay_fee)-'Cloud & AI COGS'!{ADJ}{cl.rows['cost_paid']}", F_USD2, "", False),
    ("Expected paid lifetime (months) = 1/churn", lambda s, ch, c: "1/MIN(0.5,churn*sc_churn)", F_NUM1, "", False),
    ("Subscription LTV (gross profit, undiscounted)", lambda s, ch, c: "B_ATT*B_SUBGP*B_LIFE", F_USD2, "", False),
    ("Affiliate gross profit over device life", lambda s, ch, c: f"'Assumptions'!{ADJ}{TSIN['affiliate_rate']}/device_inactive", F_USD2, "Rate x expected active life (1/inactivity).", False),
    ("TOTAL LIFETIME CONTRIBUTION PER DEVICE", lambda s, ch, c: "B_HWC+B_ACC+B_TRIAL+B_LTV+B_AFF", F_USD2, "", True),
    ("Lifetime contribution / acquisition cost (LTV:CAC)", lambda s, ch, c: "IF(B_CAC<0,(B_TOT-B_CAC)/-B_CAC,0)", F_X, "Contribution before CAC divided by CAC.", False),
    ("Payback on CAC (months after purchase)", lambda s, ch, c: "IF(B_HWGP+B_ACC>=-B_CAC,0,(-B_CAC-B_HWGP-B_ACC)/MAX(0.01,B_ATT*B_SUBGP))", F_NUM1, "0 = paid back at sale by hardware margin.", False),
]
TOK = {"B_MSRP": 0, "B_DISC": 1, "B_RET": 2, "B_NET": 3, "B_COGS": 4, "B_FUL": 5, "B_PAY": 6, "B_WAR": 7, "B_HWGP": 8,
       "B_HWGM": 9, "B_CAC": 10, "B_HWC": 11, "B_ACC": 12, "B_TRIAL": 13, "B_ATT": 14, "B_SUBGP": 15, "B_LIFE": 16,
       "B_LTV": 17, "B_AFF": 18, "B_TOT": 19}
for k, (lab, fn, fmt, note, bold) in enumerate(lines):
    r = rr + k

    def wrap(s, ch, c, fn=fn):
        f = fn(s, ch, c)
        for tok in sorted(TOK, key=len, reverse=True):
            f = f.replace(tok, f"{c}{rr + TOK[tok]}")
        return f
    ue_row(r, lab, wrap, fmt, note, bold)
UE_FIRST = rr
# sensitivity grid: GM% by price and COGS delta (DTC), per SKU
sr = rr + len(lines) + 3
ue.cell(sr, 1, "Sensitivity: DTC hardware gross margin % by price (rows) and landed-COGS change (cols)").font = TITLE
deltas = [-0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.20]
price_pts = {"peb": [119, 129, 139, 149, 169, 179], "sq": [249, 269, 279, 299, 329, 349], "atl": [449, 499, 529, 549, 599, 649]}
SENS_ROWS = {}
cur = sr + 1
for s, nm in SKUS:
    ue.cell(cur, 1, f"{nm}: price \\ COGS delta").font = BOLD
    for j, d in enumerate(deltas):
        c = ue.cell(cur, 2 + j, d)
        c.font, c.fill, c.number_format = BLUE, INFILL, "+0%;-0%;0%"
    hdr_r = cur
    for k, ppt in enumerate(price_pts[s]):
        r2 = cur + 1 + k
        c = ue.cell(r2, 1, ppt)
        c.font, c.fill, c.number_format = BLUE, INFILL, "$#,##0"
        for j in range(len(deltas)):
            col = CL(2 + j)
            net = f"($A{r2}*(1-dtc_disc)*(1-returns_pct))"
            cogs = f"((bom_{s}+asm_{s}+pkg_{s})*(1+freight_duty)*(1+{col}${hdr_r})+dtc_ship+$A{r2}*(1-dtc_disc)*(pay_pct+warranty_pct)+pay_fixed)"
            ue[f"{col}{r2}"] = f"=1-{cogs}/{net}"
            ue[f"{col}{r2}"].number_format = "0.0%"
    SENS_ROWS[s] = (hdr_r, cur + 1, cur + len(price_pts[s]))
    cur = cur + len(price_pts[s]) + 2

# --------------------------------------------------------------------------
# 18. Dashboard
# --------------------------------------------------------------------------
db = wb.create_sheet("Dashboard", 0)
db["A1"] = "LORE Labs -- CFO Dashboard"
db["A1"].font = Font(name="Fraunces", bold=True, size=20, color="C4623A")
db["A2"] = '="Scenario: "&Scenarios!D3&"   |   all figures USD, live from model"'
db["A2"].font = NOTE
db.column_dimensions["A"].width = 44
for k, fy in enumerate(FY):
    c = db.cell(4, 2 + k, f"FY{fy}" + ("*" if fy == 2026 else ""))
    c.font, c.fill = HDR, HDRFILL
    db.column_dimensions[CL(2 + k)].width = 15
kpis = [
    ("Units shipped", pm, "units_total", F_NUM),
    ("Total revenue", pl, "rev", F_USD),
    ("  Hardware (net)", pl, "hw_net", F_USD),
    ("  Subscriptions (Explorer + Trip Pass)", None, None, F_USD),
    ("  Accessories", pl, "acc", F_USD),
    ("  Affiliate", pl, "aff", F_USD),
    ("  B2B fleet", pl, "fleet", F_USD),
    ("Revenue growth YoY", None, None, F_PCT),
    ("Gross profit", pl, "gp", F_USD),
    ("Gross margin %", pl, "gm", F_PCT),
    ("Hardware gross margin %", pl, "hw_gm", F_PCT),
    ("EBITDA", pl, "ebitda", F_USD),
    ("EBITDA margin %", pl, "ebitda_m", F_PCT),
    ("Net income", pl, "ni", F_USD),
    ("Ending cash", cf, "end", F_USD),
    ("Net burn (op + inv cash flow)", cf, "burn", F_USD),
    ("Equity raised in year", cf, "equity", F_USD),
    ("Paid subscribers (end)", co, "end", F_NUM),
    ("Subscription ARR (end)", co, "arr", F_USD),
    ("Active devices (end)", co, "act_end", F_NUM),
    ("Headcount (end)", hp, "hc_total", F_NUM),
]
DB = {}
for j, (lab, sh, key, fmt) in enumerate(kpis):
    r = 5 + j
    db.cell(r, 1, lab)
    DB[lab] = r
    for k in range(len(FY)):
        col = CL(2 + k)
        if lab.startswith("  Subscriptions"):
            f = f"={pl.sref('subs', k)}+{pl.sref('trip', k)}"
        elif lab == "Revenue growth YoY":
            f = "=0" if k == 0 else f"=IF({CL(1+k)}{DB['Total revenue']}>0,{col}{DB['Total revenue']}/{CL(1+k)}{DB['Total revenue']}-1,0)"
        else:
            f = f"={sh.sref(key, k)}"
        c = db[f"{col}{r}"]
        c.value = f
        c.number_format = fmt
db.cell(5 + len(kpis), 1, "* FY2026 = Nov-Dec stub").font = NOTE
mr = 5 + len(kpis) + 2
db.cell(mr, 1, "Funding & runway").font = TITLE
for k, lab in enumerate(["Total equity raised through FY2031", "Minimum month-end cash, Nov-26..Dec-28", "Month of minimum cash",
                          "Peak monthly net burn (monthly periods)", "Month of peak burn", "Peak average monthly burn (any period incl. FY29-31)",
                          "First monthly period with positive EBITDA (monthly cols)", "First fiscal year with positive EBITDA",
                          "First fiscal year with positive operating+investing cash flow", "Minimum period-end cash incl. FY29-31"]):
    db.cell(mr + 1 + k, 1, lab)
    c = db.cell(mr + 1 + k, 2, f"='Funding & Runway'!D{FR_MET[lab]}")
    c.number_format = F_USD
    c.font = BOLD
    DB[lab] = mr + 1 + k
# charts (native Excel charts)
ch1 = BarChart()
ch1.type, ch1.grouping, ch1.overlap = "col", "stacked", 100
ch1.title = "Revenue by stream (FY)"
data = Reference(db, min_col=1, max_col=7, min_row=DB["  Hardware (net)"], max_row=DB["  B2B fleet"])
ch1.add_data(data, from_rows=True, titles_from_data=True)
ch1.set_categories(Reference(db, min_col=2, max_col=7, min_row=4, max_row=4))
ch1.height, ch1.width = 8, 16
db.add_chart(ch1, "I4")
ch2 = LineChart()
ch2.title = "Gross margin % (FY)"
ch2.add_data(Reference(db, min_col=1, max_col=7, min_row=DB["Gross margin %"], max_row=DB["Hardware gross margin %"]), from_rows=True, titles_from_data=True)
ch2.set_categories(Reference(db, min_col=2, max_col=7, min_row=4, max_row=4))
ch2.height, ch2.width = 8, 16
db.add_chart(ch2, "I22")
ch3 = LineChart()
ch3.title = "Ending cash by period"
ch3.add_data(Reference(cf.ws, min_col=FC, max_col=FC + NP - 1, min_row=cf.rows["end"], max_row=cf.rows["end"]), from_rows=True, titles_from_data=False)
ch3.set_categories(Reference(cf.ws, min_col=FC, max_col=FC + NP - 1, min_row=2, max_row=2))
ch3.height, ch3.width = 8, 16
db.add_chart(ch3, "I40")
ch4 = BarChart()
ch4.title = "Headcount (end of FY)"
ch4.add_data(Reference(db, min_col=1, max_col=7, min_row=DB["Headcount (end)"], max_row=DB["Headcount (end)"]), from_rows=True, titles_from_data=True)
ch4.set_categories(Reference(db, min_col=2, max_col=7, min_row=4, max_row=4))
ch4.height, ch4.width = 8, 16
db.add_chart(ch4, "S4")

# --------------------------------------------------------------------------
# Sheet order & save
# --------------------------------------------------------------------------
order = ["Dashboard", "Assumptions", "Scenarios", "Pricing & Mix", "Unit Economics", "Subscription Cohorts", "Revenue Build",
         "Hardware COGS", "Cloud & AI COGS", "Headcount", "Headcount Plan", "OpEx", "Working Capital", "P&L", "Cash Flow",
         "Balance Sheet", "Funding & Runway", "Runway", "Cap Table", "Timeline"]
wb._sheets = [wb[n] for n in order]
wb.calculation.fullCalcOnLoad = True

# export a row map for the recalc/verify/chart scripts
ROWMAP = {
    "periods": [dict(label=p["label"], year=p["year"], key=p["key"], months=p["months"], monthly=p["monthly"]) for p in PERIODS],
    "cols": COLS, "sumcols": SUMCOLS, "fy": FY,
    "sheets": {ts.name: ts.rows for ts in [pm, co, cl, rv, hc, hp, wc, ox, pl, cf, bs, rw]},
    "ue_first": UE_FIRST, "ue_labels": {k: v for k, v in UE.items()},
    "dashboard": DB, "fr_metrics": FR_MET, "cap": {"hr0": CAP_HR0, "tot": CAP_TOT},
    "tsin": TSIN, "scalars": SCALARS, "sc_snap_row": SC_SNAP_ROW, "roles": len(ROLES),
}
out = os.environ.get("LORE_OUT", OUT)
wb.save(out)
with open(os.path.join(HERE, "rowmap.json"), "w") as fh:
    json.dump(ROWMAP, fh, indent=1, default=str)
print("saved", out)
