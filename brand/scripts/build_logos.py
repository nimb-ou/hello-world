"""Build every LORE logo SVG (pure outlines — no live fonts) into brand/logo/.

Run:  python3 brand/scripts/build_logos.py   then   node brand/scripts/render_all.js
"""
import math
import os

from glyphs import text_path
from tokens import INK, BONE, TERRA, BRASS, OLIVE, FOG, NIGHT

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "logo")
SVG_DIR = os.path.join(OUT, "svg")
os.makedirs(SVG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Wordmark master parameters (Fraunces OFL, instanced + outlined, re-spaced)
# ---------------------------------------------------------------------------
WM_AXES = dict(opsz=72, wght=430, SOFT=0, WONK=0)
WM_SIZE = 100.0          # font size in master units
WM_TRACK = 0.15          # +15% em tracking
# optical pair corrections (em) applied after the glyph on the left
WM_PAIR = {"L": -0.045, "O": -0.005, "R": -0.02}


def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def wordmark_paths(x=0.0, baseline=0.0, size=WM_SIZE):
    """Return (d, width, cap_height) for the LORE wordmark at given size."""
    ds = []
    cx = x
    left = None
    top = None
    bottom = None
    right = None
    for ch in "LORE":
        d, adv, b = text_path(ch, "fraunces", size, cx, baseline, **WM_AXES)
        ds.append(d)
        left = b[0] if left is None else min(left, b[0])
        right = b[2] if right is None else max(right, b[2])
        top = b[1] if top is None else min(top, b[1])
        bottom = b[3] if bottom is None else max(bottom, b[3])
        cx += adv + (WM_TRACK + WM_PAIR.get(ch, 0)) * size
    return " ".join(ds), (left, top, right, bottom)


# Normalise the wordmark so its ink box starts at x=0 and the cap top is y=0.
_d, _bb = wordmark_paths()
WM_W = _bb[2] - _bb[0]
WM_H = _bb[3] - _bb[1]           # includes the tiny overshoot of O
WM_OFFX, WM_OFFY = -_bb[0], -_bb[1]
WM_D = _d


def wordmark_g(x, y, h, fill):
    """Place the wordmark with its ink box top-left at (x, y) and ink height h."""
    s = h / WM_H
    return (f'<g transform="translate({f(x)} {f(y)}) scale({s:.5f}) translate({f(WM_OFFX)} {f(WM_OFFY)})">'
            f'<path fill="{fill}" d="{WM_D}"/></g>'), WM_W * s


# ---------------------------------------------------------------------------
# The Keyhole symbol — geometry on a 100-unit grid
#   disc:      centre (50,50) r 50
#   head:      centre (50,40) r 13          (k = 26 = clear-space unit)
#   body:      flares from half-width 5 at y 50 to half-width 11.5 at y 77
#   proportions echo the Aventine keyhole + a Roman doorway + a standing figure.
# ---------------------------------------------------------------------------
HEAD_C = (50.0, 40.0)
HEAD_R = 13.0
BODY_TOP = (5.0, 50.0)      # half-width, y   (virtual — hidden inside the head)
BODY_BOT = (11.5, 77.0)


def _keyhole_points():
    (hx, hy), r = HEAD_C, HEAD_R
    # left side line through (hx-5, 50) and (hx-11.5, 77); find intersection with head circle
    x1, y1 = hx - BODY_TOP[0], BODY_TOP[1]
    x2, y2 = hx - BODY_BOT[0], BODY_BOT[1]
    dx, dy = x2 - x1, y2 - y1
    # solve |P(t) - C|^2 = r^2 for P = P1 + t*(dx,dy)
    fx, fy = x1 - hx, y1 - hy
    a = dx * dx + dy * dy
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - r * r
    disc = b * b - 4 * a * c
    t = (-b + math.sqrt(disc)) / (2 * a)       # exit point (lower one)
    if not (0 <= t <= 1):
        t = (-b - math.sqrt(disc)) / (2 * a)
    px, py = x1 + t * dx, y1 + t * dy
    return (px, py), (x2, y2)


def keyhole_d(cx=50, cy=50, scale=1.0, reverse=False):
    """Keyhole outline path. (cx,cy) = centre of the 100-grid; scale 1 = 100 units."""
    (px, py), (bx, by) = _keyhole_points()
    def P(x, y):
        return f((x - 50) * scale + cx), f((y - 50) * scale + cy)
    r = HEAD_R * scale
    lx, ly = P(px, py)
    rx, ry = P(100 - px, py)
    blx, bly = P(bx, by)
    brx, bry = P(100 - bx, by)
    if not reverse:   # clockwise
        return (f"M{lx} {ly}A{f(r)} {f(r)} 0 1 1 {rx} {ry}L{brx} {bry}L{blx} {bly}Z")
    return (f"M{rx} {ry}A{f(r)} {f(r)} 0 1 0 {lx} {ly}L{blx} {bly}L{brx} {bry}Z")


def circle_d(cx, cy, r, ccw=False):
    s = 0 if ccw else 1
    return (f"M{f(cx - r)} {f(cy)}A{f(r)} {f(r)} 0 1 {s} {f(cx + r)} {f(cy)}"
            f"A{f(r)} {f(r)} 0 1 {s} {f(cx - r)} {f(cy)}Z")


def symbol_d(x, y, size):
    """Disc with knocked-out keyhole, top-left (x,y), diameter size. Uses evenodd."""
    s = size / 100.0
    return circle_d(x + size / 2, y + size / 2, size / 2) + keyhole_d(x + size / 2, y + size / 2, s, reverse=True)


def svg(w, h, body, title, desc="", bg=None):
    bgr = f'<rect width="{f(w)}" height="{f(h)}" fill="{bg}"/>' if bg else ""
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {f(h)}" width="{f(w)}" height="{f(h)}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title>' + (f"<desc>{desc}</desc>" if desc else "") + bgr + body + "</svg>\n")


def write(name, content, folder=SVG_DIR):
    p = os.path.join(folder, name)
    with open(p, "w") as fh:
        fh.write(content)
    return p


def label(text, x, y, size, fill, font="inter", tracking=0.0, anchor="start", **axes):
    if not axes:
        axes = dict(opsz=14, wght=450) if font == "inter" else (dict(wght=420) if font == "mono" else dict(opsz=72, wght=400, SOFT=0, WONK=0))
    d, w, _ = text_path(text, font, size, 0, 0, tracking=tracking, **axes)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    return f'<path transform="translate({f(x)} {f(y)})" fill="{fill}" d="{d}"/>', w


# ---------------------------------------------------------------------------
COLOURWAYS = {
    # name: (wordmark/symbol fill, typical background for previews)
    "ink": (INK, BONE),
    "bone": (BONE, INK),
    "terracotta": (TERRA, BONE),
    "night": (BONE, NIGHT),
}


def build_core():
    files = []
    # ---- Wordmark (ink box + padding = 0; clear space is applied by the user) ----
    H = 100.0
    for cw, (fill, _bg) in COLOURWAYS.items():
        if cw == "night":
            continue
        g, w = wordmark_g(0, 0, H, fill)
        files.append(write(f"lore-wordmark-{cw}.svg", svg(w, H, g, "LORE wordmark",
                     "LORE wordmark. Outlined master — never retype.")))
    # ---- Symbol ----
    S = 100.0
    for cw, (fill, _bg) in COLOURWAYS.items():
        if cw == "night":
            continue
        body = f'<path fill="{fill}" fill-rule="evenodd" d="{symbol_d(0, 0, S)}"/>'
        files.append(write(f"lore-symbol-{cw}.svg", svg(S, S, body, "LORE Keyhole symbol")))
    # keyhole alone (positive) — for deboss, LED ring masks, app icon
    body = f'<path fill="{INK}" d="{keyhole_d(50, 50, 1.0)}"/>'
    files.append(write("lore-keyhole-glyph-ink.svg", svg(100, 100, body, "LORE keyhole glyph (positive)")))
    body = f'<path fill="{TERRA}" d="{keyhole_d(50, 50, 1.0)}"/>'
    files.append(write("lore-keyhole-glyph-terracotta.svg", svg(100, 100, body, "LORE keyhole glyph (positive)")))

    # ---- Horizontal lockup: symbol Ø = 1.5 × cap height, gap = 0.45 × Ø ----
    cap = 100.0
    D = 1.5 * cap
    gap = 0.45 * D
    wm_y = (D - cap) / 2
    for cw, (fill, _bg) in COLOURWAYS.items():
        if cw == "night":
            continue
        sym_fill = TERRA if cw == "ink" else fill
        g, w = wordmark_g(D + gap, wm_y, cap, fill)
        body = f'<path fill="{sym_fill}" fill-rule="evenodd" d="{symbol_d(0, 0, D)}"/>' + g
        files.append(write(f"lore-lockup-horizontal-{cw}.svg", svg(D + gap + w, D, body, "LORE horizontal lockup")))
        # mono version (symbol same colour as wordmark)
        if cw == "ink":
            body = f'<path fill="{fill}" fill-rule="evenodd" d="{symbol_d(0, 0, D)}"/>' + g
            files.append(write("lore-lockup-horizontal-ink-mono.svg", svg(D + gap + w, D, body, "LORE horizontal lockup (mono)")))

    # ---- Stacked lockup: symbol Ø = 2.0 × cap, gap = 0.8 × cap, optional tagline ----
    D2 = 2.0 * cap
    gap2 = 0.8 * cap
    for cw, (fill, _bg) in COLOURWAYS.items():
        if cw == "night":
            continue
        sym_fill = TERRA if cw == "ink" else fill
        _g, w = wordmark_g(0, 0, cap, fill)
        W = max(w, D2)
        g, _ = wordmark_g((W - w) / 2, D2 + gap2, cap, fill)
        body = f'<path fill="{sym_fill}" fill-rule="evenodd" d="{symbol_d((W - D2) / 2, 0, D2)}"/>' + g
        Ht = D2 + gap2 + cap
        files.append(write(f"lore-lockup-stacked-{cw}.svg", svg(W, Ht, body, "LORE stacked lockup")))
        # with tagline
        tag_size = 0.24 * cap
        tl, tw = label("EVERY STREET HAS A STORY.", 0, 0, tag_size, fill, "inter", tracking=0.28, opsz=14, wght=500)
        W3 = max(W, tw)
        g, _ = wordmark_g((W3 - w) / 2, D2 + gap2, cap, fill)
        tl, _ = label("EVERY STREET HAS A STORY.", W3 / 2, Ht + 0.62 * cap + tag_size * 0.73, tag_size,
                      fill, "inter", tracking=0.28, anchor="middle", opsz=14, wght=500)
        body = (f'<path fill="{sym_fill}" fill-rule="evenodd" d="{symbol_d((W3 - D2) / 2, 0, D2)}"/>' + g + tl)
        files.append(write(f"lore-lockup-stacked-tagline-{cw}.svg",
                           svg(W3, Ht + 0.62 * cap + tag_size, body, "LORE stacked lockup with tagline")))
    return files


# ---------------------------------------------------------------------------
def build_app_icons():
    files = []
    A = 1024.0
    k = 0.74 * A            # 100-grid scaled to 74% of icon -> keyhole is 37% of icon height
    # Primary: Terracotta field, Bone keyhole, faint inner ring (hairline) — reads at 29 px.
    body = (f'<rect width="{A}" height="{A}" fill="{TERRA}"/>'
            f'<path fill="{BONE}" d="{keyhole_d(A / 2, A / 2 - 0.02 * k + 4, k / 100)}"/>')
    files.append(write("lore-app-icon-1024.svg", svg(A, A, body, "LORE app icon")))
    # Dark appearance (iOS 18+/Android themed): Ink field, Terracotta keyhole
    body = (f'<rect width="{A}" height="{A}" fill="{INK}"/>'
            f'<path fill="{TERRA}" d="{keyhole_d(A / 2, A / 2 - 0.02 * k + 4, k / 100)}"/>')
    files.append(write("lore-app-icon-1024-dark.svg", svg(A, A, body, "LORE app icon (dark)")))
    # Tinted / monochrome (iOS tinted mode): white keyhole on transparent, as alpha mask
    body = f'<path fill="#FFFFFF" d="{keyhole_d(A / 2, A / 2 - 0.02 * k + 4, k / 100)}"/>'
    files.append(write("lore-app-icon-1024-tinted-mask.svg", svg(A, A, body, "LORE app icon (tinted mask)")))
    # Preview with iOS-style squircle mask (for decks only — never ship pre-masked to the stores)
    r = 0.2237 * A
    body = (f'<defs><clipPath id="sq"><rect width="{A}" height="{A}" rx="{f(r)}"/></clipPath></defs>'
            f'<g clip-path="url(#sq)"><rect width="{A}" height="{A}" fill="{TERRA}"/>'
            f'<path fill="{BONE}" d="{keyhole_d(A / 2, A / 2 - 0.02 * k + 4, k / 100)}"/></g>')
    files.append(write("lore-app-icon-preview-rounded.svg", svg(A, A, body, "LORE app icon (rounded preview)")))
    # Favicon: symbol disc tuned for 16–32 px (head slightly larger for legibility)
    body = (f'<circle cx="16" cy="16" r="16" fill="{TERRA}"/>'
            f'<path fill="{BONE}" d="{keyhole_d(16, 16.4, 0.36)}"/>')
    files.append(write("favicon.svg", svg(32, 32, body, "LORE")))
    return files


# ---------------------------------------------------------------------------
def build_concepts():
    """3 concepts on one sheet, with legibility tests and scoring."""
    W, H = 2400, 1500
    PW = 735
    parts = []
    t, _ = label("LORE — SYMBOL EXPLORATION, ROUND 3", 80, 110, 22, INK, "mono", tracking=0.12)
    parts.append(t)
    t, _ = label("Three routes to one idea: a story hidden in the street, waiting to be heard.", 80, 180, 44, INK,
                 "fraunces", opsz=72, wght=380, SOFT=0, WONK=0)
    parts.append(t)
    parts.append(f'<rect x="80" y="220" width="{W - 160}" height="1.5" fill="{INK}" opacity=".25"/>')

    def needle(x, y, s, fill):
        # compass needle (lozenge) + two sound arcs to the right
        cx, cy = x + 42 * s, y + 50 * s
        n = (f'<path fill="{fill}" d="M{f(cx)} {f(y + 8 * s)}L{f(cx + 9 * s)} {f(cy)}L{f(cx)} {f(y + 92 * s)}'
             f'L{f(cx - 9 * s)} {f(cy)}Z"/>'
             f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(3 * s)}" fill="{BONE}"/>'
             f'<path fill="{BONE}" d="M{f(cx)} {f(cy + 3 * s)}L{f(cx + 9 * s)} {f(cy)}L{f(cx)} {f(y + 92 * s)}L{f(cx - 9 * s)} {f(cy)}Z" opacity=".0"/>')
        arcs = ""
        for i, rr in enumerate((20, 32, 44)):
            a0 = math.radians(-40)
            a1 = math.radians(40)
            x0, y0 = cx + rr * s * math.cos(a0), cy + rr * s * math.sin(a0)
            x1, y1 = cx + rr * s * math.cos(a1), cy + rr * s * math.sin(a1)
            arcs += (f'<path fill="none" stroke="{fill}" stroke-width="{f(5 * s)}" stroke-linecap="round" '
                     f'd="M{f(x0)} {f(y0)}A{f(rr * s)} {f(rr * s)} 0 0 1 {f(x1)} {f(y1)}" opacity="{1 - i * 0.28:.2f}"/>')
        return n + arcs

    def quote(x, y, s, fill):
        # single open-quote: ball + tail, tail rising to upper right; reads also as a map pin turned
        bx, by, br = x + 44 * s, y + 62 * s, 24 * s
        tail = (f'M{f(x + 21 * s)} {f(y + 60 * s)}C{f(x + 20 * s)} {f(y + 34 * s)} {f(x + 38 * s)} {f(y + 14 * s)} '
                f'{f(x + 70 * s)} {f(y + 8 * s)}L{f(x + 72 * s)} {f(y + 15 * s)}C{f(x + 52 * s)} {f(y + 22 * s)} '
                f'{f(x + 42 * s)} {f(y + 32 * s)} {f(x + 41 * s)} {f(y + 40 * s)}Z')
        return f'<path fill="{fill}" d="{tail}"/><circle cx="{f(bx)}" cy="{f(by)}" r="{f(br)}" fill="{fill}"/>'

    def keyhole(x, y, s, fill):
        return f'<path fill="{fill}" fill-rule="evenodd" d="{symbol_d(x, y, 100 * s)}"/>'

    concepts = [
        ("A", "NEEDLE + WAVE", needle,
         ["A compass needle pointing true, with the arcs of a voice",
          "spreading from it. Says: direction and narration — Map",
          "Vision in one glyph. Honest, but close to generic nav /",
          "audio iconography; arcs vanish below 24 px."],
         (3, 2, 3, 2)),
        ("B", "OPEN QUOTE", quote,
         ["The first mark of every story: an opening quotation.",
          "Editorial, literary, Monocle-adjacent. Weakness: quote",
          "marks are a crowded symbol (messaging, reviews, media",
          "brands) and it says nothing about place or walking."],
         (2, 4, 3, 2)),
        ("C", "THE KEYHOLE", keyhole,
         ["Rome's Aventine keyhole frames St Peter's dome — a",
          "secret view hidden in a door. A keyhole is a doorway,",
          "a standing traveller and a map pin at once. Survives",
          "16 px, an LED ring, deboss and a 1-colour stamp."],
         (4, 5, 5, 4)),
    ]
    crit = ["OWNABLE", "SCALES TO 16 PX", "STORY FIT", "DEVICE FIT"]
    for i, (letter, name, fn, lines, scores) in enumerate(concepts):
        x0 = 80 + i * (PW + 20)
        sel = letter == "C"
        if sel:
            parts.append(f'<rect x="{x0 - 20}" y="250" width="{PW}" height="1170" rx="6" fill="none" stroke="{TERRA}" stroke-width="3"/>')
        t, _ = label(f"{letter}", x0, 320, 22, TERRA if sel else FOG, "mono", tracking=0.1)
        parts.append(t)
        t, _ = label(name, x0 + 40, 320, 22, INK, "mono", tracking=0.18)
        parts.append(t)
        if sel:
            t, _ = label("SELECTED", x0 + PW - 60, 320, 18, TERRA, "mono", tracking=0.2, anchor="end")
            parts.append(t)
        # hero
        parts.append(f'<rect x="{x0}" y="350" width="{PW - 40}" height="460" fill="{INK if i == 1 else "#EAE3D7"}"/>' if False else
                     f'<rect x="{x0}" y="350" width="{PW - 40}" height="460" fill="#EAE3D7"/>')
        parts.append(fn(x0 + (PW - 40) / 2 - 170, 410, 3.4, TERRA if sel else INK))
        # scale tests
        y = 850
        sx = x0
        for sz in (64, 32, 24, 16):
            parts.append(fn(sx, y + (64 - sz) / 2, sz / 100, INK))
            t, _ = label(f"{sz}", sx + sz / 2, y + 92, 14, FOG, "mono", anchor="middle")
            parts.append(t)
            sx += sz + 48
        # reversed tile
        parts.append(f'<rect x="{x0 + PW - 40 - 170}" y="{y - 10}" width="170" height="110" fill="{NIGHT}"/>')
        parts.append(fn(x0 + PW - 40 - 170 + 53, y + 3, 0.64, BONE))
        # rationale
        ly = 1010
        for ln in lines:
            t, _ = label(ln, x0, ly, 21, INK, "inter", opsz=14, wght=400)
            parts.append(t)
            ly += 33
        # scoring
        ly = 1180
        for c, sc in zip(crit, scores):
            t, _ = label(c, x0, ly, 15, FOG, "mono", tracking=0.12)
            parts.append(t)
            for d in range(5):
                parts.append(f'<circle cx="{x0 + 330 + d * 26}" cy="{ly - 6}" r="8" fill="{(TERRA if sel else INK) if d < sc else "none"}" stroke="{INK}" stroke-opacity=".35" stroke-width="{0 if d < sc else 1.5}"/>')
            ly += 40
        t, _ = label(f"TOTAL  {sum(scores)}/20", x0, ly + 20, 18, TERRA if sel else INK, "mono", tracking=0.12, wght=600)
        parts.append(t)
    t, _ = label("Scores are the brand team's internal judgement (Oct 2026), not consumer-tested. C scores 18/20; to be validated in Q1 2027 beta (unaided recall + 16 px legibility).",
                 80, H - 40, 16, FOG, "inter")
    parts.append(t)
    return write("concepts.svg", svg(W, H, "".join(parts), "LORE symbol concepts", bg=BONE), OUT)


# ---------------------------------------------------------------------------
def build_construction():
    W, H = 1600, 1000
    p = []
    s = 6.0   # 100 grid -> 600 px
    ox, oy = 120, 220
    # grid
    for i in range(0, 101, 5):
        op = ".35" if i % 25 == 0 else ".12"
        p.append(f'<line x1="{ox + i * s}" y1="{oy}" x2="{ox + i * s}" y2="{oy + 600}" stroke="{FOG}" stroke-opacity="{op}" stroke-width="1"/>')
        p.append(f'<line x1="{ox}" y1="{oy + i * s}" x2="{ox + 600}" y2="{oy + i * s}" stroke="{FOG}" stroke-opacity="{op}" stroke-width="1"/>')
    p.append(f'<path fill="{TERRA}" fill-opacity=".92" fill-rule="evenodd" d="{symbol_d(ox, oy, 600)}"/>')
    # head circle + body guides
    hx, hy = ox + 50 * s, oy + 40 * s
    p.append(f'<circle cx="{hx}" cy="{hy}" r="{13 * s}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-dasharray="6 5"/>')
    p.append(f'<circle cx="{hx}" cy="{hy}" r="4" fill="{INK}"/>')
    p.append(f'<line x1="{ox + 45 * s}" y1="{oy + 50 * s}" x2="{ox + 38.5 * s}" y2="{oy + 77 * s}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="6 5"/>')
    p.append(f'<line x1="{ox + 55 * s}" y1="{oy + 50 * s}" x2="{ox + 61.5 * s}" y2="{oy + 77 * s}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="6 5"/>')
    p.append(f'<circle cx="{ox + 300}" cy="{oy + 300}" r="300" fill="none" stroke="{INK}" stroke-width="1"/>')
    p.append(f'<circle cx="{ox + 300}" cy="{oy + 300}" r="4" fill="{INK}" fill-opacity=".5"/>')
    t, _ = label("SYMBOL CONSTRUCTION — 100-UNIT GRID", 120, 120, 20, INK, "mono", tracking=0.14)
    p.append(t)
    t, _ = label("The Keyhole", 120, 180, 48, INK, "fraunces")
    p.append(t)
    notes = [
        ("DISC", "Ø 100 · centre (50, 50)"),
        ("HEAD", "Ø 26 · centre (50, 40) — 10 u above disc centre"),
        ("BODY", "flares 10 u → 23 u wide, from y 50 to y 77"),
        ("BASE", "flat · sits 23 u above disc edge"),
        ("k", "= head Ø (26 u) = clear-space unit"),
        ("OPTICS", "keyhole spans y 27 to 77: its centre sits 2 u low"),
        ("", "so the void feels 'seated', like a door on its sill"),
        ("FAVICON", "≤ 32 px: keyhole scale +3%, head +0.4 px"),
        ("COLOUR", "Terracotta #C4623A disc · void = ground"),
        ("SOURCE", "logo/svg/lore-symbol-*.svg (outlines)"),
    ]
    y = 260
    for k_, v in notes:
        if k_:
            t, _ = label(k_, 820, y, 16, TERRA, "mono", tracking=0.12)
            p.append(t)
        t, _ = label(v, 960, y, 20, INK, "inter")
        p.append(t)
        y += 46
    # wordmark spec
    t, _ = label("WORDMARK", 820, 760, 16, TERRA, "mono", tracking=0.12)
    p.append(t)
    g, w = wordmark_g(960, 730, 60, INK)
    p.append(g)
    lines = ["Drawn from Fraunces (OFL) · opsz 72 · wght 430 · SOFT 0 · WONK 0",
             "Outlined, tracked +150, optical pairs L–O −45, R–E −20 (1/1000 em)",
             "Never retype the wordmark in a live font."]
    y = 840
    for ln in lines:
        t, _ = label(ln, 960, y, 17, FOG, "inter")
        p.append(t)
        y += 30
    return write("construction.svg", svg(W, H, "".join(p), "LORE symbol construction", bg=BONE), OUT)


def build_clearspace():
    W, H = 1600, 900
    p = []
    t, _ = label("CLEAR SPACE & MINIMUM SIZE", 100, 110, 20, INK, "mono", tracking=0.14)
    p.append(t)
    cap = 120.0
    D = 1.5 * cap
    gap = 0.45 * D
    k = 0.26 * D            # head diameter
    ox, oy = 100 + k, 250 + k
    g, w = wordmark_g(ox + D + gap, oy + (D - cap) / 2, cap, INK)
    LW = D + gap + w
    p.append(f'<rect x="{ox - k}" y="{oy - k}" width="{LW + 2 * k}" height="{D + 2 * k}" fill="{TERRA}" fill-opacity=".10" stroke="{TERRA}" stroke-dasharray="6 6"/>')
    p.append(f'<rect x="{ox}" y="{oy}" width="{LW}" height="{D}" fill="none" stroke="{FOG}" stroke-width="1"/>')
    p.append(f'<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(ox, oy, D)}"/>' + g)
    # k markers
    for (x, y) in [(ox - k, oy + D / 2), (ox + LW, oy + D / 2)]:
        p.append(f'<circle cx="{x + k / 2}" cy="{y}" r="{k / 2}" fill="none" stroke="{TERRA}" stroke-width="1.5"/>')
        t, _ = label("k", x + k / 2, y + 7, 20, TERRA, "mono", anchor="middle")
        p.append(t)
    for (x, y) in [(ox + D / 2, oy - k), (ox + D / 2, oy + D)]:
        p.append(f'<circle cx="{x}" cy="{y + k / 2}" r="{k / 2}" fill="none" stroke="{TERRA}" stroke-width="1.5"/>')
    t, _ = label("k = diameter of the keyhole head (26% of symbol Ø). Keep k clear on all sides; 2k on packaging & signage.", 100, 640, 20, INK, "inter")
    p.append(t)
    # min sizes
    x = 100
    y = 720
    specs = [("SYMBOL", 16, "16 px · 4 mm", "sym"), ("WORDMARK", 18, "72 px wide · 18 mm", "wm"),
             ("HORIZONTAL LOCKUP", 24, "112 px wide · 28 mm", "lh"), ("APP ICON", 29, "29 px (store minimum)", "ai")]
    for name, h, txt, kind in specs:
        if kind == "sym":
            p.append(f'<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(x, y, 16)}"/>')
        elif kind == "wm":
            gg, _w = wordmark_g(x, y + 2, 72 * WM_H / WM_W, INK)
            p.append(gg)
        elif kind == "lh":
            c = 24 / 1.5
            p.append(f'<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(x, y, 24)}"/>')
            gg, _w = wordmark_g(x + 24 + 0.45 * 24, y + (24 - c) / 2, c, INK)
            p.append(gg)
        else:
            p.append(f'<rect x="{x}" y="{y}" width="29" height="29" rx="6.5" fill="{TERRA}"/><path fill="{BONE}" d="{keyhole_d(x + 14.5, y + 14.7, 0.174)}"/>')
        t, _ = label(name, x, y + 70, 14, FOG, "mono", tracking=0.12)
        p.append(t)
        t, _ = label(txt, x, y + 98, 18, INK, "inter")
        p.append(t)
        x += 360
    return write("clearspace.svg", svg(W, H, "".join(p), "LORE clear space and minimum sizes", bg=BONE), OUT)


def build_misuse():
    """Don'ts sheet: 8 tiles of incorrect usage."""
    W, H = 1600, 900
    p = []
    t, _ = label("LOGO MISUSE — NEVER DO THIS", 80, 90, 20, INK, "mono", tracking=0.14)
    p.append(t)
    tiles = [
        ("Don't stretch or squash", "stretch"), ("Don't retype in Fraunces / any font", "retype"),
        ("Don't recolour outside the palette", "recolour"), ("Don't add effects or shadows", "shadow"),
        ("Don't rotate", "rotate"), ("Don't outline the symbol", "outline"),
        ("Don't place on busy photos", "busy"), ("Don't change lockup proportions", "proportion"),
    ]
    tw, th = 340, 300
    for i, (cap, kind) in enumerate(tiles):
        cx = 80 + (i % 4) * (tw + 25)
        cy = 140 + (i // 4) * (th + 70)
        p.append(f'<rect x="{cx}" y="{cy}" width="{tw}" height="{th - 60}" fill="#EAE3D7"/>')
        c = 34.0
        D = 1.5 * c
        gap = 0.45 * D
        _g, w = wordmark_g(0, 0, c, INK)
        p.append(f'<clipPath id="c{i}"><rect x="{cx}" y="{cy}" width="{tw}" height="{th - 60}"/></clipPath><g clip-path="url(#c{i})">')
        close_tile = True
        LW = D + gap + w
        x0 = cx + (tw - LW) / 2
        y0 = cy + (th - 60 - D) / 2
        lock = (f'<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(x0, y0, D)}"/>' + wordmark_g(x0 + D + gap, y0 + (D - c) / 2, c, INK)[0])
        if kind == "stretch":
            p.append(f'<g transform="translate({cx + tw / 2} {cy + 120}) scale(1.25 0.72) translate({-cx - tw / 2} {-cy - 120})">{lock}</g>')
        elif kind == "retype":
            p.append(f'<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(x0, y0, D)}"/>')
            t, _ = label("Lore", x0 + D + gap, y0 + D * 0.72, 58, INK, "fraunces", opsz=144, wght=700, SOFT=100, WONK=1)
            p.append(t)
        elif kind == "recolour":
            p.append(lock.replace(TERRA, "#2F80ED").replace(INK, "#8E44AD"))
        elif kind == "shadow":
            p.append(f'<defs><filter id="ds" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="4" dy="6" stdDeviation="3" flood-opacity=".45"/></filter></defs><g filter="url(#ds)">{lock}</g>')
        elif kind == "rotate":
            p.append(f'<g transform="rotate(-14 {cx + tw / 2} {cy + 120})">{lock}</g>')
        elif kind == "outline":
            p.append(f'<path fill="none" stroke="{TERRA}" stroke-width="2.5" fill-rule="evenodd" d="{symbol_d(x0, y0, D)}"/>' + wordmark_g(x0 + D + gap, y0 + (D - c) / 2, c, INK)[0])
        elif kind == "busy":
            stripes = "".join(f'<rect x="{cx + j * 22}" y="{cy}" width="11" height="{th - 60}" fill="{[OLIVE, BRASS, TERRA, NIGHT][j % 4]}" opacity=".7"/>' for j in range(16))
            p.append(stripes + lock)
        elif kind == "proportion":
            p.append(f'<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(x0 + 10, y0 + 18, D * 0.5)}"/>' + wordmark_g(x0 + D * 0.5 + 18, y0, c * 1.4, INK)[0])
        p.append('</g>')
        # red cross mark
        p.append(f'<g stroke="{"#D2392B"}" stroke-width="3"><line x1="{cx + tw - 34}" y1="{cy + 14}" x2="{cx + tw - 14}" y2="{cy + 34}"/><line x1="{cx + tw - 14}" y1="{cy + 14}" x2="{cx + tw - 34}" y2="{cy + 34}"/></g>')
        t, _ = label(cap, cx, cy + th - 25, 18, INK, "inter")
        p.append(t)
    return write("misuse.svg", svg(W, H, "".join(p), "LORE logo misuse", bg=BONE), OUT)


def build_overview():
    """All variants on their intended grounds — used for PNG preview sheet."""
    W, H = 2000, 1400
    p = []
    cells = [
        (BONE, "lh", INK, TERRA, "Primary · Ink + Terracotta on Bone"),
        (INK, "lh", BONE, TERRA, "Reverse · Bone + Terracotta on Ink"),
        (TERRA, "lh", BONE, BONE, "Terracotta ground · Bone mono"),
        (NIGHT, "st", BONE, TERRA, "Stacked · on Night"),
        ("#EAE3D7", "st", INK, INK, "Stacked mono · Ink on Sand"),
        (OLIVE, "st", BONE, BONE, "Stacked · Bone on Olive (City Packs)"),
    ]
    cw, ch = W / 3, (H - 120) / 2
    for i, (bg, kind, fg, sym, cap) in enumerate(cells):
        x0 = (i % 3) * cw
        y0 = 120 + (i // 3) * ch
        p.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(cw)}" height="{f(ch)}" fill="{bg}"/>')
        if kind == "lh":
            c = 64.0
            D = 1.5 * c
            gap = 0.45 * D
            _g, w = wordmark_g(0, 0, c, fg)
            LW = D + gap + w
            lx = x0 + (cw - LW) / 2
            ly = y0 + (ch - D) / 2 - 20
            p.append(f'<path fill="{sym}" fill-rule="evenodd" d="{symbol_d(lx, ly, D)}"/>' + wordmark_g(lx + D + gap, ly + (D - c) / 2, c, fg)[0])
        else:
            c = 52.0
            D = 2 * c
            _g, w = wordmark_g(0, 0, c, fg)
            lx = x0 + cw / 2
            ly = y0 + (ch - (D + 0.8 * c + c)) / 2 - 20
            p.append(f'<path fill="{sym}" fill-rule="evenodd" d="{symbol_d(lx - D / 2, ly, D)}"/>' + wordmark_g(lx - w / 2, ly + D + 0.8 * c, c, fg)[0])
        lc = FOG if bg in (BONE, "#EAE3D7") else (BONE if bg != TERRA else BONE)
        t, _ = label(cap.upper(), x0 + 40, y0 + ch - 36, 15, lc, "mono", tracking=0.12)
        p.append(t)
    g, w = wordmark_g(60, 40, 40, INK)
    p.append(f'<rect width="{W}" height="120" fill="{BONE}"/>' + g)
    t, _ = label("LOGO SYSTEM · v1.0 · OCT 2026", W - 60, 74, 18, FOG, "mono", tracking=0.14, anchor="end")
    p.append(t)
    return write("logo-overview.svg", svg(W, H, "".join(p), "LORE logo overview"), OUT)


if __name__ == "__main__":
    out = build_core() + build_app_icons()
    out += [build_concepts(), build_construction(), build_clearspace(), build_misuse(), build_overview()]
    for o in out:
        print(os.path.relpath(o, os.path.join(HERE, "..")))
