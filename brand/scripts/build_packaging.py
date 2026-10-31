"""LORE packaging: flat dielines (mm, 1:1) + top/front art for Pebble, Square, Atlas.

Dieline conventions (match legal/printer handoff):
  CUT    solid   #E6007E 0.25 mm
  CREASE dashed  #009FE3 0.25 mm (4/2)
  BLEED  dotted  #00A651 0.15 mm, 3 mm outside cut
  GLUE   hatched #F5A623 area
  SAFE   dashed  #9AA0A6 0.15 mm, 3 mm inside cut
All dimensions are STRUCTURAL ESTIMATES pending supplier samples and device EVT dims (Q1 2027).
"""
import math
import os

from build_logos import keyhole_d, symbol_d, wordmark_g, label, f
from tokens import INK, BONE, TERRA, BRASS, OLIVE, FOG, NIGHT

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "packaging")
os.makedirs(OUT, exist_ok=True)

CUT, CREASE, BLEED, GLUE, SAFE = "#E6007E", "#009FE3", "#00A651", "#F5A623", "#9AA0A6"


def doc(w, h, body, title):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{f(w)}mm" height="{f(h)}mm" viewBox="0 0 {f(w)} {f(h)}"><title>{title}</title>'
            f'<rect width="{f(w)}" height="{f(h)}" fill="#FFFFFF"/>{body}</svg>\n')


def cut(d):
    return f'<path d="{d}" fill="none" stroke="{CUT}" stroke-width="0.25" stroke-linejoin="round"/>'


def crease(x1, y1, x2, y2):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{CREASE}" stroke-width="0.25" stroke-dasharray="4 2"/>'


def glue(x, y, w, h):
    pid = f"g{int(x * 10)}{int(y * 10)}"
    return (f'<defs><pattern id="{pid}" width="2" height="2" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<line x1="0" y1="0" x2="0" y2="2" stroke="{GLUE}" stroke-width="0.6"/></pattern></defs>'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="url(#{pid})" opacity=".8"/>')


def dim(x1, y1, x2, y2, text, off=6, vertical=False):
    """Dimension line with ticks and label (mm)."""
    c = "#5C5F66"
    if not vertical:
        y = y1 - off
        s = (f'<line x1="{f(x1)}" y1="{f(y)}" x2="{f(x2)}" y2="{f(y)}" stroke="{c}" stroke-width="0.15"/>'
             f'<line x1="{f(x1)}" y1="{f(y - 1.5)}" x2="{f(x1)}" y2="{f(y + 1.5)}" stroke="{c}" stroke-width="0.15"/>'
             f'<line x1="{f(x2)}" y1="{f(y - 1.5)}" x2="{f(x2)}" y2="{f(y + 1.5)}" stroke="{c}" stroke-width="0.15"/>')
        t, _ = label(text, (x1 + x2) / 2, y - 1.2, 2.6, c, "mono", anchor="middle")
        return s + t
    x = x1 - off
    s = (f'<line x1="{f(x)}" y1="{f(y1)}" x2="{f(x)}" y2="{f(y2)}" stroke="{c}" stroke-width="0.15"/>'
         f'<line x1="{f(x - 1.5)}" y1="{f(y1)}" x2="{f(x + 1.5)}" y2="{f(y1)}" stroke="{c}" stroke-width="0.15"/>'
         f'<line x1="{f(x - 1.5)}" y1="{f(y2)}" x2="{f(x + 1.5)}" y2="{f(y2)}" stroke="{c}" stroke-width="0.15"/>')
    t, _ = label(text, 0, 0, 2.6, c, "mono", anchor="middle")
    return s + f'<g transform="translate({f(x - 1.2)} {f((y1 + y2) / 2)}) rotate(-90)">{t}</g>'


def panel_label(text, x, y, size=3.2):
    t, _ = label(text, x, y, size, "#9AA0A6", "mono", anchor="middle", tracking=0.1)
    return t


def legend(x, y, title, lines):
    p = []
    t, _ = label(title, x, y, 5, INK, "fraunces")
    p.append(t)
    yy = y + 9
    items = [(CUT, "solid", "CUT"), (CREASE, "4 2", "CREASE / FOLD"), (BLEED, "1 1", "BLEED +3 mm"), (GLUE, "hatch", "GLUE AREA")]
    for col, dash, name in items:
        if dash == "hatch":
            p.append(glue(x, yy - 2.5, 10, 3))
        else:
            p.append(f'<line x1="{x}" y1="{yy - 1}" x2="{x + 10}" y2="{yy - 1}" stroke="{col}" stroke-width="0.4" stroke-dasharray="{"" if dash == "solid" else dash}"/>')
        t, _ = label(name, x + 13, yy, 2.6, INK, "mono", tracking=0.08)
        p.append(t)
        yy += 5.5
    yy += 2
    for ln in lines:
        t, _ = label(ln, x, yy, 2.6, "#3A3D43", "inter")
        p.append(t)
        yy += 4.4
    return "".join(p)


# ---------------------------------------------------------------------------
# PEBBLE — drawer box: double-wall tray + wrap sleeve (folding boxboard, no glue on tray)
# ---------------------------------------------------------------------------
PEBBLE = dict(name="LORE Pebble", sku="LP-01", tray=(100, 100, 38), board=0.6)


def circle_path(cx, cy, r):
    return f"M{f(cx - r)} {f(cy)}A{f(r)} {f(r)} 0 1 0 {f(cx + r)} {f(cy)}A{f(r)} {f(r)} 0 1 0 {f(cx - r)} {f(cy)}Z"


def tray_dieline(L, W, H, t, ox, oy):
    """Double-wall crash-free tray. Base L×W; front/back walls fold over (2H − t) and lock with tabs.
    Side walls carry corner flaps (H − 1) tucked between the double walls."""
    p = []
    bx, by = ox + H + 2 * H - t, oy + 2 * H - t + 0   # base origin (room for walls)
    # coordinates
    x0, x1 = bx, bx + L
    y0, y1 = by, by + W
    # front (top in drawing) wall + fold-over
    fw = H                 # outer wall
    fi = H - t             # inner wall
    tab = 4                # lock tab depth
    pts = []
    # Outline: build clockwise from top-left of top fold-over
    top_outer = y0 - fw
    top_inner = y0 - fw - fi
    bot_outer = y1 + fw
    bot_inner = y1 + fw + fi
    # side walls with corner flaps
    left = x0 - H
    right = x1 + H
    flap = H - 1.0
    d = (f"M{f(x0 + 2 * t)} {f(top_inner)}"
         # top fold-over with two lock tabs
         f"L{f(x0 + L * 0.25 - 6)} {f(top_inner)}L{f(x0 + L * 0.25 - 6)} {f(top_inner - tab)}L{f(x0 + L * 0.25 + 6)} {f(top_inner - tab)}"
         f"L{f(x0 + L * 0.25 + 6)} {f(top_inner)}L{f(x0 + L * 0.75 - 6)} {f(top_inner)}L{f(x0 + L * 0.75 - 6)} {f(top_inner - tab)}"
         f"L{f(x0 + L * 0.75 + 6)} {f(top_inner - tab)}L{f(x0 + L * 0.75 + 6)} {f(top_inner)}L{f(x1 - 2 * t)} {f(top_inner)}"
         f"L{f(x1)} {f(top_outer)}"
         # right top corner flap (attached to right side wall, pointing up)
         f"L{f(x1 + 0.5)} {f(top_outer)}L{f(x1 + 0.5)} {f(y0 - flap)}L{f(right - 3)} {f(y0 - flap)}L{f(right)} {f(y0 - 3)}L{f(right)} {f(y0)}"
         f"L{f(right)} {f(y1)}L{f(right)} {f(y1 + 3)}L{f(right - 3)} {f(y1 + flap)}L{f(x1 + 0.5)} {f(y1 + flap)}L{f(x1 + 0.5)} {f(bot_outer)}L{f(x1)} {f(bot_outer)}"
         f"L{f(x1 - 2 * t)} {f(bot_inner)}"
         f"L{f(x0 + L * 0.75 + 6)} {f(bot_inner)}L{f(x0 + L * 0.75 + 6)} {f(bot_inner + tab)}L{f(x0 + L * 0.75 - 6)} {f(bot_inner + tab)}L{f(x0 + L * 0.75 - 6)} {f(bot_inner)}"
         f"L{f(x0 + L * 0.25 + 6)} {f(bot_inner)}L{f(x0 + L * 0.25 + 6)} {f(bot_inner + tab)}L{f(x0 + L * 0.25 - 6)} {f(bot_inner + tab)}L{f(x0 + L * 0.25 - 6)} {f(bot_inner)}"
         f"L{f(x0 + 2 * t)} {f(bot_inner)}L{f(x0)} {f(bot_outer)}L{f(x0 - 0.5)} {f(bot_outer)}L{f(x0 - 0.5)} {f(y1 + flap)}"
         f"L{f(left + 3)} {f(y1 + flap)}L{f(left)} {f(y1 + 3)}L{f(left)} {f(y1)}L{f(left)} {f(y0)}L{f(left)} {f(y0 - 3)}L{f(left + 3)} {f(y0 - flap)}"
         f"L{f(x0 - 0.5)} {f(y0 - flap)}L{f(x0 - 0.5)} {f(top_outer)}L{f(x0)} {f(top_outer)}Z")
    p.append(cut(d))
    # lock slots in base along front/back crease
    for yy in (y0 + t + 0.3, y1 - t - 1.3):
        for xx in (x0 + L * 0.25, x0 + L * 0.75):
            p.append(cut(f"M{f(xx - 6.3)} {f(yy)}h12.6v1h-12.6Z"))
    # thumb notch on the front wall (half-circle r 11)
    # full circle centred on the wall/fold-over crease -> notches both layers once folded
    p.append(cut(circle_path(x0 + L / 2, top_outer, 11)))
    # creases
    p += [crease(x0, y0, x1, y0), crease(x0, y1, x1, y1), crease(x0, y0, x0, y1), crease(x1, y0, x1, y1),
          crease(x0, top_outer, x1, top_outer), crease(x0, bot_outer, x1, bot_outer),
          crease(left, y0, x0, y0), crease(left, y1, x0, y1), crease(x1, y0, right, y0), crease(x1, y1, right, y1)]
    p.append(panel_label("BASE  (print: inside face — 'Look up.' blind)", x0 + L / 2, y0 + W / 2))
    p.append(panel_label("FRONT WALL", x0 + L / 2, y0 - H / 2 + 6))
    p.append(panel_label("FOLD-OVER (INNER)", x0 + L / 2, top_inner + fi / 2 - 2))
    p.append(panel_label("BACK WALL", x0 + L / 2, y1 + H / 2))
    p.append(panel_label("FOLD-OVER (INNER)", x0 + L / 2, bot_outer + fi / 2))
    p.append(f'<g transform="translate({f(left + H / 2)} {f(y0 + W / 2)}) rotate(-90)">{panel_label("SIDE WALL", 0, 0)}</g>')
    p.append(f'<g transform="translate({f(x1 + H / 2)} {f(y0 + W / 2)}) rotate(90)">{panel_label("SIDE WALL", 0, 0)}</g>')
    # dims
    p.append(dim(x0, top_inner - tab, x1, top_inner - tab, f"{L} (inner L)", off=6))
    p.append(dim(left, y0, left, y1, f"{W} (inner W)", off=6, vertical=True))
    p.append(dim(left, y1, left, y1 + H, f"{H}", off=6, vertical=True))
    extent = (left - 3, top_inner - tab - 3, right + 3, bot_inner + tab + 3)
    # bleed
    p.insert(0, f'<rect x="{f(extent[0])}" y="{f(extent[1])}" width="{f(extent[2] - extent[0])}" height="{f(extent[3] - extent[1])}" fill="none" stroke="{BLEED}" stroke-width="0.15" stroke-dasharray="1 1"/>')
    return "".join(p), extent


def sleeve_dieline(L, W, H, t, ox, oy):
    """Wrap sleeve: [glue 14][side H][top L][side H][bottom L], depth W. Open both ends; thumb notches on top."""
    clr = 1.0
    Ls, Ws, Hs = L + 2 * t + clr, W + clr, H + 2 * t + clr      # inner dims of sleeve
    g = 14
    xs = [ox, ox + g, ox + g + Hs, ox + g + Hs + Ls, ox + g + 2 * Hs + Ls, ox + g + 2 * Hs + 2 * Ls]
    y0, y1 = oy, oy + Ws
    p = []
    d = (f"M{f(xs[0])} {f(y0 + 4)}L{f(xs[1])} {f(y0)}L{f(xs[2] + Ls / 2 - 12)} {f(y0)}"
         f"L{f(xs[5])} {f(y0)}L{f(xs[5])} {f(y1)}L{f(xs[1])} {f(y1)}L{f(xs[0])} {f(y1 - 4)}Z")
    p.append(cut(d))
    # thumb notches both ends of the TOP panel
    cx = xs[2] + Ls / 2
    p.append(f'<path d="M{f(cx - 12)} {f(y0)}A12 12 0 0 0 {f(cx + 12)} {f(y0)}" fill="#FFFFFF" stroke="{CUT}" stroke-width="0.25"/>')
    p.append(f'<path d="M{f(cx - 12)} {f(y1)}A12 12 0 0 1 {f(cx + 12)} {f(y1)}" fill="#FFFFFF" stroke="{CUT}" stroke-width="0.25"/>')
    for x in xs[1:5]:
        p.append(crease(x, y0, x, y1))
    p.append(glue(xs[0] + 1, y0 + 4, g - 2, Ws - 8))
    names = ["GLUE", "SIDE", "TOP — ART", "SIDE", "BOTTOM — REG. / FSC"]
    for i, n in enumerate(names[1:], start=1):
        p.append(panel_label(n, (xs[i] + xs[i + 1]) / 2, y0 + Ws / 2 + 14))
    p.append(dim(xs[2], y0, xs[3], y0, f"{f(Ls)}", off=8))
    p.append(dim(xs[1], y0, xs[2], y0, f"{f(Hs)}", off=8))
    p.append(dim(xs[0], y0, xs[0], y1, f"{f(Ws)}", off=6, vertical=True))
    p.append(dim(xs[0], y1 + 18, xs[5], y1 + 18, f"{f(xs[5] - xs[0])} overall", off=6))
    extent = (xs[0] - 3, y0 - 3, xs[5] + 3, y1 + 3)
    p.insert(0, f'<rect x="{f(extent[0])}" y="{f(extent[1])}" width="{f(extent[2] - extent[0])}" height="{f(extent[3] - extent[1])}" fill="none" stroke="{BLEED}" stroke-width="0.15" stroke-dasharray="1 1"/>')
    return "".join(p), (Ls, Ws, Hs), extent


def rigid_wrap(L, W, h, turn, ox, oy, label_txt):
    """Wrap paper for a rigid set-up box part (lid or base) of outer L×W×h; turn-in `turn` mm; pinch ears on long sides."""
    p = []
    x0, y0 = ox + h + turn, oy + h + turn
    x1, y1 = x0 + L, y0 + W
    ear = h - 1                    # ear length on the long sides (wraps round the corner)
    d = (f"M{f(x0 - 0.5)} {f(y0 - h - turn)}L{f(x1 + 0.5)} {f(y0 - h - turn)}L{f(x1 + 0.5)} {f(y0 - h)}"
         f"L{f(x1 + ear)} {f(y0 - h + 2)}L{f(x1 + ear)} {f(y0 - 0.5)}"
         f"L{f(x1 + h + turn)} {f(y0 - 0.5)}L{f(x1 + h + turn)} {f(y1 + 0.5)}L{f(x1 + ear)} {f(y1 + 0.5)}"
         f"L{f(x1 + ear)} {f(y1 + h - 2)}L{f(x1 + 0.5)} {f(y1 + h)}L{f(x1 + 0.5)} {f(y1 + h + turn)}"
         f"L{f(x0 - 0.5)} {f(y1 + h + turn)}L{f(x0 - 0.5)} {f(y1 + h)}L{f(x0 - ear)} {f(y1 + h - 2)}L{f(x0 - ear)} {f(y1 + 0.5)}"
         f"L{f(x0 - h - turn)} {f(y1 + 0.5)}L{f(x0 - h - turn)} {f(y0 - 0.5)}L{f(x0 - ear)} {f(y0 - 0.5)}"
         f"L{f(x0 - ear)} {f(y0 - h + 2)}L{f(x0 - 0.5)} {f(y0 - h)}Z")
    p.append(cut(d))
    p += [crease(x0, y0, x1, y0), crease(x0, y1, x1, y1), crease(x0, y0, x0, y1), crease(x1, y0, x1, y1),
          crease(x0, y0 - h, x1, y0 - h), crease(x0, y1 + h, x1, y1 + h), crease(x0 - h, y0, x0 - h, y1), crease(x1 + h, y0, x1 + h, y1),
          crease(x1, y0, x1 + ear, y0), crease(x1, y1, x1 + ear, y1), crease(x0 - ear, y0, x0, y0), crease(x0 - ear, y1, x0, y1)]
    p.append(glue(x0 - h - turn, y0 - h - turn, L + 2 * h + 2 * turn, 0.01))  # (no-op keeps defs tidy)
    p.append(panel_label(label_txt, x0 + L / 2, y0 + W / 2))
    p.append(panel_label("TURN-IN", x0 + L / 2, y0 - h - turn / 2 + 1))
    p.append(panel_label("WALL", x0 + L / 2, y0 - h / 2 + 1))
    p.append(dim(x0, y0 - h - turn, x1, y0 - h - turn, f"{L}", off=5))
    p.append(dim(x0 - h - turn, y0, x0 - h - turn, y1, f"{W}", off=5, vertical=True))
    p.append(dim(x0 - h - turn, y1, x0 - h - turn, y1 + h, f"{h}", off=5, vertical=True))
    p.append(dim(x0 - h - turn, y1 + h, x0 - h - turn, y1 + h + turn, f"{turn}", off=5, vertical=True))
    ext = (x0 - h - turn - 3, y0 - h - turn - 3, x1 + h + turn + 3, y1 + h + turn + 3)
    p.insert(0, f'<rect x="{f(ext[0])}" y="{f(ext[1])}" width="{f(ext[2] - ext[0])}" height="{f(ext[3] - ext[1])}" fill="none" stroke="{BLEED}" stroke-width="0.15" stroke-dasharray="1 1"/>')
    p.append(glue(x0 + 2, y0 + 2, L - 4, W - 4))
    return "".join(p), ext


def title_block(x, y, w, sku, lines):
    p = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="44" fill="none" stroke="{INK}" stroke-width="0.25"/>']
    g, _ = wordmark_g(x + 5, y + 6, 6, INK)
    p.append(g)
    t, _ = label(sku, x + w - 5, y + 11, 3.2, TERRA, "mono", anchor="end", tracking=0.1)
    p.append(t)
    yy = y + 20
    for ln in lines:
        t, _ = label(ln, x + 5, yy, 2.6, INK, "mono")
        p.append(t)
        yy += 4.3
    return "".join(p)


def build_pebble():
    L, W, H = PEBBLE["tray"]
    t = PEBBLE["board"]
    body = []
    tray, ext = tray_dieline(L, W, H, t, 20, 30)
    body.append(tray)
    sl, (Ls, Ws, Hs), ext2 = sleeve_dieline(L, W, H, t, 20, ext[3] + 30)
    body.append(sl)
    Wd = max(ext[2], ext2[2]) + 120
    Hd = ext2[3] + 30
    body.append(legend(Wd - 105, 40, "Pebble — tray + sleeve", [
        "Tray inner 100 × 100 × 38 mm (device 42×42×14 in pulp nest).",
        "Sleeve inner %s × %s × %s mm (1.0 mm clearance)." % (f(Ls), f(Ws), f(Hs)),
        "Tray: 400 g/m² FSC Recycled uncoated board, Bone",
        "  (candidate: Fedrigoni Materica Gesso 360, verify).",
        "Sleeve: 360 g/m² Terracotta-through-dyed board",
        "  (candidate: Materica Terra Rossa, verify).",
        "Tray is glue-free: walls lock with 4 tabs.",
        "Sleeve: one glued side seam, water-based PVA.",
        "Print: 1 PMS (Ink) + blind deboss, no lamination.",
        "All dims ESTIMATES — freeze after EVT unit (Q1 2027).",
    ]))
    body.append(title_block(Wd - 105, Hd - 74, 95, "LP-01 · DIELINE v0.3", [
        "SCALE 1:1 · UNITS mm · THICKNESS t = 0.6",
        "DRAWN Brand / LORE Labs · 2026-10-30",
        "STATUS: concept for supplier RFQ",
        "NOT FOR PRODUCTION"]))
    with open(os.path.join(OUT, "dieline-pebble.svg"), "w") as fh:
        fh.write(doc(Wd, Hd, "".join(body), "LORE Pebble dieline"))


def build_rigid(name, sku, L, W, lid_h, base_h, board, turn, extra_lines, fname):
    body = []
    # lid outer = base outer + 2*(board + paper) clearance
    lidL, lidW = L + 2 * board + 1, W + 2 * board + 1
    lid, e1 = rigid_wrap(lidL, lidW, lid_h, turn, 20, 30, "LID TOP — ART (deboss + foil)")
    body.append(lid)
    base, e2 = rigid_wrap(L, W, base_h, turn, e1[2] + 25, 30, "BASE BOTTOM — REG./FSC")
    body.append(base)
    # greyboard blanks (no print) — shown small beneath
    gy = max(e1[3], e2[3]) + 25
    gx = 20
    t, _ = label("GREYBOARD BLANKS (V-GROOVED, CORNER-TAPED WITH PAPER TAPE)", gx, gy, 3, INK, "mono", tracking=0.08)
    body.append(t)
    for i, (ll, ww, hh, nm) in enumerate([(lidL, lidW, lid_h, "LID"), (L, W, base_h, "BASE")]):
        ox = gx + i * (lidL + 2 * lid_h + 30)
        oy = gy + 8 + hh
        d = (f"M{f(ox + hh)} {f(oy - hh)}h{f(ll)}v{f(hh)}h{f(hh)}v{f(ww)}h{f(-hh)}v{f(hh)}h{f(-ll)}v{f(-hh)}h{f(-hh)}v{f(-ww)}h{f(hh)}Z")
        body.append(cut(d))
        body += [crease(ox + hh, oy, ox + hh + ll, oy), crease(ox + hh, oy + ww, ox + hh + ll, oy + ww),
                 crease(ox + hh, oy, ox + hh, oy + ww), crease(ox + hh + ll, oy, ox + hh + ll, oy + ww)]
        body.append(panel_label(f"{nm} {f(ll)}×{f(ww)}×{hh}", ox + hh + ll / 2, oy + ww / 2))
    Wd = e2[2] + 120
    Hd = gy + 8 + max(lid_h, base_h) * 2 + max(lidW, W) + 20
    body.append(legend(Wd - 105, 40, f"{name} — rigid set-up box", extra_lines))
    body.append(title_block(Wd - 105, Hd - 60, 95, f"{sku} · DIELINE v0.3", [
        f"SCALE 1:1 · UNITS mm · BOARD {board} mm · TURN-IN {turn}",
        "DRAWN Brand / LORE Labs · 2026-10-30",
        "STATUS: concept for supplier RFQ",
        "NOT FOR PRODUCTION"]))
    with open(os.path.join(OUT, fname), "w") as fh:
        fh.write(doc(Wd, Hd, "".join(body), f"{name} dieline"))


# ---------------------------------------------------------------------------
# Top / front art (rendered as product-style flats)
# ---------------------------------------------------------------------------
def tiber_lines(x, y, w, h, col, op=0.35):
    """Abstract 'Rome' line pattern: a Tiber-like S-curve + street hairlines. ILLUSTRATIVE, not map data."""
    p = [f'<g fill="none" stroke="{col}" stroke-opacity="{op}" stroke-linecap="round">']
    for i in range(7):
        off = i * 1.6
        p.append(f'<path stroke-width="{0.35 if i else 0.6}" d="M{f(x + w * 0.62 + off)} {f(y)}C{f(x + w * 0.40 + off)} {f(y + h * 0.25)} {f(x + w * 0.80 + off)} {f(y + h * 0.45)} {f(x + w * 0.55 + off)} {f(y + h * 0.62)}S{f(x + w * 0.30 + off)} {f(y + h * 0.9)} {f(x + w * 0.42 + off)} {f(y + h)}"/>')
    import random
    rnd = random.Random(1765)   # Piranesi's year — deterministic pattern
    for _ in range(24):
        a = rnd.uniform(0, math.pi)
        cx, cy = rnd.uniform(x, x + w), rnd.uniform(y, y + h)
        ln = rnd.uniform(8, 34)
        p.append(f'<line stroke-width="0.25" x1="{f(cx - math.cos(a) * ln)}" y1="{f(cy - math.sin(a) * ln)}" x2="{f(cx + math.cos(a) * ln)}" y2="{f(cy + math.sin(a) * ln)}"/>')
    p.append("</g>")
    return "".join(p)


def box_art():
    """One sheet with top views of all three boxes + sleeve front + inside-lid message (mm units, scaled)."""
    W, H = 640, 470
    p = [f'<rect width="{W}" height="{H}" fill="#E7E1D6"/>']
    t, _ = label("PACKAGING — TOP & FRONT ART (FLAT, 1:1 mm, SHOWN ON STUDIO GREY)", 20, 22, 4.2, INK, "mono", tracking=0.12)
    p.append(t)
    deb = "#E3DCD0"   # blind deboss rendering: slight shadow + highlight
    shadow = '<defs><filter id="sh" x="-10%" y="-10%" width="130%" height="140%"><feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#0D1B2A" flood-opacity=".22"/></filter>' \
             '<filter id="deb"><feOffset dx="0" dy="0.35"/><feGaussianBlur stdDeviation="0.25"/><feComposite operator="out" in="SourceGraphic"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .45 0"/><feBlend in2="SourceGraphic"/></filter></defs>'
    p.append(shadow)

    # 1) Pebble sleeve (terracotta) — top 102.2 × 101 approx
    x, y, s = 20, 40, 1.0
    Ls, Ws = 102.2, 101.0
    p.append(f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{Ls}" height="{Ws}" fill="{TERRA}"/></g>')
    p.append(tiber_lines(x, y, Ls, Ws, BONE, 0.22))
    p.append(f'<path d="M{f(x + Ls / 2 - 12)} {f(y)}A12 12 0 0 0 {f(x + Ls / 2 + 12)} {f(y)}Z" fill="{BONE}"/>')
    g, w = wordmark_g(0, 0, 7, BONE)
    g, w = wordmark_g(x + Ls / 2 - w / 2, y + Ws - 20, 7, BONE)
    p.append(g)
    t, _ = label("PEBBLE", x + Ls / 2, y + Ws - 7, 2.6, BONE, "mono", anchor="middle", tracking=0.3)
    p.append(t)
    t, _ = label("PEBBLE · SLEEVE TOP · Terracotta stock, Bone 1-PMS line pattern, foil-free", x, y + Ws + 9, 2.8, INK, "mono")
    p.append(t)

    # 2) Square lid (Bone wrap, blind deboss symbol, Ink wordmark)
    x2 = 150
    Ls2 = 129.6
    p.append(f'<g filter="url(#sh)"><rect x="{x2}" y="{y}" width="{Ls2}" height="{Ls2}" fill="{BONE}"/></g>')
    p.append(f'<g filter="url(#deb)"><path fill="{deb}" fill-rule="evenodd" d="{symbol_d(x2 + Ls2 / 2 - 18, y + Ls2 / 2 - 26, 36)}"/></g>')
    g, w = wordmark_g(0, 0, 6, INK)
    g, _ = wordmark_g(x2 + Ls2 / 2 - w / 2, y + Ls2 - 24, 6, INK)
    p.append(g)
    t, _ = label("SQUARE", x2 + Ls2 / 2, y + Ls2 - 11, 2.4, FOG, "mono", anchor="middle", tracking=0.3)
    p.append(t)
    t, _ = label("SQUARE · LID · Bone wrap, 0.5 mm blind deboss keyhole, Ink 1-PMS wordmark", x2, y + Ls2 + 9, 2.8, INK, "mono")
    p.append(t)

    # 3) Atlas lid (Ink/Night wrap, Brass foil keyhole + wordmark)
    x3 = 310
    Ls3 = 156.2
    p.append(f'<g filter="url(#sh)"><rect x="{x3}" y="{y}" width="{Ls3}" height="{Ls3}" fill="{INK}"/></g>')
    p.append(f'<defs><linearGradient id="foil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D8BC85"/><stop offset=".45" stop-color="{BRASS}"/><stop offset=".7" stop-color="#8E6E3C"/><stop offset="1" stop-color="#CFAF74"/></linearGradient></defs>')
    p.append(f'<path fill="url(#foil)" d="{keyhole_d(x3 + Ls3 / 2, y + Ls3 / 2 - 8, 0.62)}"/>')
    g, w = wordmark_g(0, 0, 6.5, BRASS)
    g, _ = wordmark_g(x3 + Ls3 / 2 - w / 2, y + Ls3 - 26, 6.5, "url(#foil)")
    p.append(g)
    t, _ = label("ATLAS", x3 + Ls3 / 2, y + Ls3 - 12, 2.6, BRASS, "mono", anchor="middle", tracking=0.3)
    p.append(t)
    p.append(f'<rect x="{x3 + Ls3 - 2}" y="{y + Ls3 / 2 - 18}" width="2" height="36" fill="{BRASS}"/>')  # ribbon pull hint
    t, _ = label("ATLAS · LID · Ink wrap, brass foil (hot-stamp) keyhole + wordmark, cotton ribbon pull", x3, y + Ls3 + 9, 2.8, INK, "mono")
    p.append(t)

    # 4) Front/side face (Square) — regulatory band
    fy = 225
    p.append(f'<g filter="url(#sh)"><rect x="{x2}" y="{fy}" width="{Ls2}" height="50" fill="{BONE}"/></g>')
    t, _ = label("Every street has a story.", x2 + 8, fy + 15, 6, INK, "fraunces")
    p.append(t)
    lines = ["LORE SQUARE · AI TRAVEL COMPANION · INK", "1.6″ AMOLED · LTE + eSIM · 150+ COUNTRIES",
             "INCLUDES 3 MONTHS LORE PASS EXPLORER"]
    yy = fy + 26
    for ln in lines:
        t, _ = label(ln, x2 + 8, yy, 2.4, INK, "mono", tracking=0.08)
        p.append(t)
        yy += 4.4
    p.append(f'<rect x="{x2 + Ls2 - 34}" y="{fy + 22}" width="26" height="20" fill="none" stroke="{FOG}" stroke-width="0.3" stroke-dasharray="1 1"/>')
    t, _ = label("REG + FSC", x2 + Ls2 - 21, fy + 33, 2.2, FOG, "mono", anchor="middle")
    p.append(t)
    t, _ = label("SQUARE · FRONT WALL · product line + regulatory zone (legal-ops supplies marks)", x2, fy + 59, 2.8, INK, "mono")
    p.append(t)

    # 5) Inside-lid message (Square/Atlas)
    iy = 290
    ix = 20
    p.append(f'<g filter="url(#sh)"><rect x="{ix}" y="{iy}" width="125" height="125" fill="{TERRA}"/></g>')
    t, _ = label("Look up.", ix + 12, iy + 34, 16, BONE, "fraunces-italic", opsz=72, wght=380, SOFT=0, WONK=0)
    p.append(t)
    msg = ["The best things in a city are", "rarely at eye level. A date over", "a doorway. A saint on a corner.",
           "A keyhole with a dome inside it.", "", "Put your phone away.", "We'll tell you where to look."]
    yy = iy + 52
    for ln in msg:
        t, _ = label(ln, ix + 12, yy, 4.2, BONE, "inter", opsz=14, wght=420)
        p.append(t)
        yy += 6.4
    p.append(f'<path fill="{BONE}" fill-rule="evenodd" d="{symbol_d(ix + 125 - 22, iy + 125 - 22, 10)}"/>')
    t, _ = label("INSIDE LID · Terracotta liner paper, Bone 1-PMS · all SKUs", ix, iy + 134, 2.8, INK, "mono")
    p.append(t)

    # 6) Pulp insert plan (Square)
    px, py = 310, 225
    p.append(f'<rect x="{px}" y="{py}" width="125" height="125" fill="#D9D1C2"/>')
    p.append(f'<rect x="{px + 35.5}" y="{py + 22}" width="54" height="54" rx="11" fill="#C9C0AE" stroke="#B3A994" stroke-width="0.4"/>')
    p.append(f'<rect x="{px + 41}" y="{py + 27.5}" width="43" height="43" rx="8" fill="#111"/>')
    p.append(f'<circle cx="{px + 92}" cy="{py + 35}" r="3" fill="{BRASS}" opacity=".0"/>')
    p.append(f'<path d="M{px + 52} {py + 22} a10.5 10.5 0 0 1 21 0" fill="#BDB39F"/>')  # finger scoop
    p.append(f'<rect x="{px + 12}" y="{py + 88}" width="101" height="24" rx="4" fill="#C9C0AE" stroke="#B3A994" stroke-width="0.4"/>')
    t, _ = label("CABLE + LANYARD WELL (paper-banded)", px + 62.5, py + 102, 2.4, "#6B6250", "mono", anchor="middle")
    p.append(t)
    t, _ = label("SQUARE · MOULDED-FIBRE INSERT (wet-pressed, undyed) · plan view", px, py + 134, 2.8, INK, "mono")
    p.append(t)
    # quick-start card
    qx, qy = 470, 225
    p.append(f'<g filter="url(#sh)"><rect x="{qx}" y="{qy}" width="105" height="105" fill="{BONE}"/></g>')
    t, _ = label("Hello.", qx + 9, qy + 20, 9, INK, "fraunces")
    p.append(t)
    steps = ["1  Hold the button for 3 s.", "2  Pair your earphones.", "3  Scan for the LORE app.", "4  Walk. We'll talk."]
    yy = qy + 36
    for st in steps:
        t, _ = label(st, qx + 9, yy, 3.6, INK, "inter")
        p.append(t)
        yy += 8
    p.append(f'<rect x="{qx + 70}" y="{qy + 70}" width="26" height="26" fill="none" stroke="{INK}" stroke-width="0.4"/>')
    t, _ = label("QR", qx + 83, qy + 85, 3, FOG, "mono", anchor="middle")
    p.append(t)
    t, _ = label("QUICK-START CARD · 100 × 100 · 2-sided", qx, qy + 114, 2.8, INK, "mono")
    p.append(t)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W * 4}" height="{H * 4}"><title>LORE packaging art</title>{"".join(p)}</svg>\n'


if __name__ == "__main__":
    build_pebble()
    build_rigid("Square", "LS-01", 128, 128, 48, 46, 1.5, 15, [
        "Base outer 128 × 128 × 46; lid 132 × 132 × 48 (full-depth",
        "  telescope lid, 1 mm air gap = slow 'parachute' lift).",
        "Board: 1.5 mm FSC Recycled greyboard.",
        "Wrap: 120 g/m² Bone uncoated (cand. Materica Gesso).",
        "Liner: 120 g/m² Terracotta (inside-lid message).",
        "Insert: wet-pressed moulded fibre, undyed.",
        "Adhesive: water-based animal-free glue. No film, no PET.",
        "Finishes: blind deboss 0.5 mm; Ink 1-PMS; no laminate.",
        "All dims ESTIMATES pending EVT (Q1 2027).",
    ], "dieline-square.svg")
    build_rigid("Atlas", "LA-01", 154, 154, 62, 60, 2.0, 18, [
        "Base outer 154 × 154 × 60; lid 159 × 159 × 62.",
        "Board: 2.0 mm FSC Recycled greyboard.",
        "Wrap: 140 g/m² Ink through-dyed (cand. Materica Pepper).",
        "Foil: brass-tone hot foil (verify recyclability w/ supplier).",
        "Ribbon: 12 mm undyed cotton grosgrain pull (no nylon).",
        "Insert: 2-tier moulded fibre + paperboard drawer for Kit.",
        "Includes linen-bound 'Atlas Journal' (A6, 96 pp).",
        "All dims ESTIMATES pending EVT (Q1 2027).",
    ], "dieline-atlas.svg")
    with open(os.path.join(OUT, "box-art.svg"), "w") as fh:
        fh.write(box_art())
    print("ok")
