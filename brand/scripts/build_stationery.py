"""Stationery (business card, letterhead, envelope) + merch concept sheet. mm units."""
import os

from build_logos import keyhole_d, symbol_d, wordmark_g, label, f
from tokens import INK, BONE, TERRA, BRASS, OLIVE, FOG, NIGHT

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "stationery")
os.makedirs(OUT, exist_ok=True)


def mmdoc(w, h, body, title, scale=None):
    sz = f'width="{f(w)}mm" height="{f(h)}mm"' if scale is None else f'width="{f(w * scale)}" height="{f(h * scale)}"'
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" {sz} viewBox="0 0 {f(w)} {f(h)}">'
            f'<title>{title}</title>{body}</svg>\n')


def card_front(x, y, bleed=0):
    W, H = 85, 55
    p = [f'<rect x="{x - bleed}" y="{y - bleed}" width="{W + 2 * bleed}" height="{H + 2 * bleed}" fill="{TERRA}"/>']
    p.append(f'<path fill="{BONE}" d="{keyhole_d(x + W / 2, y + H / 2 - 1, 0.42)}"/>')
    t, _ = label("Every street has a story.", x + W / 2, y + H - 6, 2.5, BONE, "fraunces-italic", anchor="middle", opsz=24, wght=400, SOFT=0, WONK=0)
    p.append(t)
    return "".join(p)


def card_back(x, y, bleed=0, name="Nimit Jain", role="Founder", email="nimit@lore.travel"):
    W, H = 85, 55
    p = [f'<rect x="{x - bleed}" y="{y - bleed}" width="{W + 2 * bleed}" height="{H + 2 * bleed}" fill="{BONE}"/>']
    g, _ = wordmark_g(x + 7, y + 7, 3.6, INK)
    p.append(g)
    p.append(f'<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(x + W - 7 - 5.4, y + 6.4, 5.4)}"/>')
    t, _ = label(name, x + 7, y + 33, 4.6, INK, "fraunces", opsz=24, wght=420, SOFT=0, WONK=0)
    p.append(t)
    t, _ = label(role.upper(), x + 7, y + 38.2, 1.9, FOG, "mono", tracking=0.18, wght=500)
    p.append(t)
    lines = [email, "lore.travel", "LORE Labs, Inc."]
    yy = y + 44.5
    for ln in lines:
        t, _ = label(ln, x + 7, yy, 2.1, INK, "inter", opsz=14, wght=430)
        p.append(t)
        yy += 3.2
    t, _ = label("41.8986° N  12.4769° E", x + W - 7, y + H - 7.1, 1.7, FOG, "mono", anchor="end", tracking=0.06)
    p.append(t)
    return "".join(p)


def build_cards():
    # print-ready singles with 3 mm bleed + crop marks
    for side, fn in (("front", card_front), ("back", card_back)):
        b = 3
        W, H = 85 + 2 * b + 12, 55 + 2 * b + 12
        ox, oy = b + 6, b + 6
        p = [f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>', fn(ox, oy, bleed=b)]
        for (cx, cy) in [(ox, oy), (ox + 85, oy), (ox, oy + 55), (ox + 85, oy + 55)]:
            dx = -1 if cx == ox else 1
            dy = -1 if cy == oy else 1
            p.append(f'<line x1="{cx + dx * (b + 1)}" y1="{cy}" x2="{cx + dx * (b + 6)}" y2="{cy}" stroke="#000" stroke-width="0.1"/>')
            p.append(f'<line x1="{cx}" y1="{cy + dy * (b + 1)}" x2="{cx}" y2="{cy + dy * (b + 6)}" stroke="#000" stroke-width="0.1"/>')
        with open(os.path.join(OUT, f"business-card-{side}.svg"), "w") as fh:
            fh.write(mmdoc(W, H, "".join(p), f"LORE business card {side} (85×55, 3 mm bleed)"))


def letterhead():
    W, H = 210, 297
    p = [f'<rect width="{W}" height="{H}" fill="{BONE}"/>']
    g, _ = wordmark_g(20, 20, 5.2, INK)
    p.append(g)
    p.append(f'<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(W - 20 - 7.6, 19, 7.6)}"/>')
    # fold marks
    for yy in (99, 198):
        p.append(f'<line x1="0" y1="{yy}" x2="5" y2="{yy}" stroke="{FOG}" stroke-width="0.2"/>')
    # address window guide (DL window, DIN 5008-ish position) — guide only
    t, _ = label("LORE LABS, INC. · DELAWARE (PLANNED) · lore.travel", 20, 50, 1.9, FOG, "mono", tracking=0.12)
    p.append(t)
    sample = [
        ("30 October 2026", "inter", 3.2, INK, 62),
        ("Dear traveller,", "fraunces", 5.2, INK, 80),
    ]
    for txt, fn, sz, col, yy in sample:
        axes = dict(opsz=14, wght=420) if fn == "inter" else dict(opsz=24, wght=400, SOFT=0, WONK=0)
        t, _ = label(txt, 20, yy, sz, col, fn, **axes)
        p.append(t)
    body = [
        "This is the LORE letterhead. Body copy is Inter 10/15 pt, set ragged-right on a",
        "120 mm measure from the 20 mm left margin. The salutation may use Fraunces at 15 pt;",
        "nothing else on the page should.",
        "",
        "Print on Bone uncoated 120 g/m² (FSC). Wordmark Ink, symbol Terracotta: two PMS,",
        "or digital on uncoated stock with the swatches in palette/palette.csv.",
        "",
        "Warmly,",
    ]
    yy = 94
    for ln in body:
        t, _ = label(ln, 20, yy, 3.5, INK, "inter", opsz=14, wght=400)
        p.append(t)
        yy += 5.3
    t, _ = label("Nimit Jain", 20, yy + 10, 5, INK, "fraunces", opsz=24, wght=420, SOFT=0, WONK=0)
    p.append(t)
    t, _ = label("FOUNDER", 20, yy + 15.5, 2.1, FOG, "mono", tracking=0.18)
    p.append(t)
    # footer
    p.append(f'<line x1="20" y1="{H - 22}" x2="{W - 20}" y2="{H - 22}" stroke="{INK}" stroke-opacity=".18" stroke-width="0.2"/>')
    t, _ = label("Every street has a story.", 20, H - 14, 3.2, INK, "fraunces-italic", opsz=24, wght=400, SOFT=0, WONK=0)
    p.append(t)
    t, _ = label("hello@lore.travel  ·  lore.travel  ·  @lore", W - 20, H - 14, 2.3, FOG, "mono", anchor="end", tracking=0.06)
    p.append(t)
    with open(os.path.join(OUT, "letterhead-a4.svg"), "w") as fh:
        fh.write(mmdoc(W, H, "".join(p), "LORE letterhead A4"))


def envelope():
    W, H = 220, 110  # DL
    p = [f'<rect width="{W}" height="{H}" fill="{BONE}"/>']
    g, _ = wordmark_g(14, 12, 4, INK)
    p.append(g)
    t, _ = label("LORE Labs, Inc. · lore.travel", 14, 24, 2.1, FOG, "mono", tracking=0.1)
    p.append(t)
    p.append(f'<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(W - 14 - 9, H - 14 - 9, 9)}"/>')
    with open(os.path.join(OUT, "envelope-dl.svg"), "w") as fh:
        fh.write(mmdoc(W, H, "".join(p), "LORE DL envelope"))


def mockup_sheet():
    """Presentation sheet: cards + letterhead on studio ground, for the brand board."""
    W, H = 400, 260
    p = [f'<rect width="{W}" height="{H}" fill="#DCD4C6"/>',
         '<defs><filter id="s" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="1.6" stdDeviation="1.8" flood-color="#0D1B2A" flood-opacity=".25"/></filter></defs>']
    # letterhead scaled
    p.append(f'<g filter="url(#s)" transform="translate(28 22) rotate(-3 0 0) scale(0.72)">')
    with open(os.path.join(OUT, "letterhead-a4.svg")) as fh:
        inner = fh.read().split(">", 2)[2].rsplit("</svg>", 1)[0]
        inner = inner.split("</title>", 1)[1]
    p.append(inner + "</g>")
    p.append(f'<g filter="url(#s)" transform="translate(210 48) rotate(4)">{card_front(0, 0)}</g>')
    p.append(f'<g filter="url(#s)" transform="translate(236 146) rotate(-2)">{card_back(0, 0)}</g>')
    p.append(f'<g filter="url(#s)" transform="translate(300 18) rotate(9) scale(.62)"><rect width="220" height="110" fill="{BONE}"/>'
             f'{wordmark_g(14, 12, 4, INK)[0]}<path fill="{TERRA}" fill-rule="evenodd" d="{symbol_d(220 - 23, 110 - 23, 9)}"/></g>')
    t, _ = label("STATIONERY · BONE UNCOATED · INK + TERRACOTTA · ILLUSTRATIVE MOCKUP", 28, H - 10, 3, INK, "mono", tracking=0.1)
    p.append(t)
    with open(os.path.join(OUT, "stationery-mockup.svg"), "w") as fh:
        fh.write(mmdoc(W, H, "".join(p), "LORE stationery mockup", scale=6))


def merch():
    W, H = 420, 185
    p = [f'<rect width="{W}" height="{H}" fill="{BONE}"/>']
    t, _ = label("LORE KIT & MERCH — CONCEPTS (NOT YET COSTED)", 16, 18, 3.6, INK, "mono", tracking=0.12)
    p.append(t)
    cells = []
    # tote
    def tote(x, y):
        s = (f'<path d="M{x + 18} {y + 28}q0 -20 22 -20t22 20" fill="none" stroke="#CDBF9F" stroke-width="3"/>'
             f'<rect x="{x + 6}" y="{y + 26}" width="68" height="76" fill="#E8DFCC" stroke="#CDBF9F" stroke-width=".6"/>'
             f'<path fill="{INK}" d="{keyhole_d(x + 40, y + 62, 0.34)}"/>'
             + label("LOOK UP.", x + 40, y + 92, 3.2, INK, "mono", anchor="middle", tracking=0.3)[0])
        return s
    def pin(x, y):
        return (f'<circle cx="{x + 40}" cy="{y + 55}" r="22" fill="{BRASS}"/><circle cx="{x + 40}" cy="{y + 55}" r="19.5" fill="{TERRA}"/>'
                f'<path fill="{BRASS}" d="{keyhole_d(x + 40, y + 55, 0.39)}"/>')
    def cap(x, y):
        return (f'<path d="M{x + 10} {y + 70}q0 -38 30 -38t30 38z" fill="{OLIVE}"/><path d="M{x + 40} {y + 70}h38q4 0 0 5h-38z" fill="#4C573F"/>'
                f'<path fill="{BONE}" fill-rule="evenodd" d="{symbol_d(x + 34, y + 48, 12)}"/>')
    def journal(x, y):
        return (f'<rect x="{x + 14}" y="{y + 14}" width="52" height="80" rx="1.5" fill="{NIGHT}"/>'
                f'<rect x="{x + 14}" y="{y + 14}" width="4" height="80" fill="#08121D"/>'
                + wordmark_g(x + 28, y + 26, 3.2, BRASS)[0]
                + label("STREET JOURNAL", x + 40, y + 36, 2.2, BRASS, "mono", anchor="middle", tracking=0.2)[0]
                + label("ROMA", x + 40, y + 86, 4, BONE, "fraunces", anchor="middle")[0])
    def tag(x, y):
        return (f'<rect x="{x + 22}" y="{y + 24}" width="36" height="58" rx="18" fill="{BRASS}"/>'
                f'<circle cx="{x + 40}" cy="{y + 33}" r="3" fill="{BONE}"/>'
                f'<path fill="#8E6E3C" d="{keyhole_d(x + 40, y + 60, 0.28)}"/>'
                f'<path d="M{x + 40} {y + 30}v-14" stroke="{INK}" stroke-width="1.2"/>')
    def postcard(x, y):
        return (f'<rect x="{x + 4}" y="{y + 34}" width="72" height="48" fill="{TERRA}" transform="rotate(-6 {x + 40} {y + 58})"/>'
                f'<rect x="{x + 6}" y="{y + 30}" width="72" height="48" fill="#FBF8F2" stroke="#DDD3C3" stroke-width=".4"/>'
                + label("Look up.", x + 12, y + 50, 7, INK, "fraunces-italic", opsz=48, wght=380, SOFT=0, WONK=0)[0]
                + label("NO. 01 · AVENTINE, ROMA", x + 12, y + 70, 2.2, FOG, "mono", tracking=0.12)[0])
    items = [("Canvas tote", "Organic cotton 10 oz, 1-colour Ink print.", tote),
             ("Enamel pin", "Hard enamel, brass-plated, 22 mm.", pin),
             ("Olive cap", "Garment-dyed cotton, Bone embroidery.", cap),
             ("Street Journal", "A6 linen notebook, brass foil, per city.", journal),
             ("Brass key tag", "Solid brass, laser-etched keyhole.", tag),
             ("Look up. postcards", "City series, FSC uncoated, 6 per pack.", postcard)]
    for i, (n, d, fn) in enumerate(items):
        x = 16 + i * 66
        y = 34
        p.append(f'<g transform="translate({x} {y}) scale(0.78)">{fn(0, 0)}</g>')
        t, _ = label(n, x + 2, y + 104, 3.6, INK, "fraunces")
        p.append(t)
        words = d.split()
        lines, cur = [], ""
        for w in words:
            if len(cur) + len(w) > 22:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        yy = y + 111
        for ln in lines:
            t, _ = label(ln, x + 2, yy, 2.3, "#3A3D43", "inter")
            p.append(t)
            yy += 3.6
    t, _ = label("Principle: merch must be useful on a walk. No disposable swag, no plastic, no slogans beyond our own lines.", 16, H - 14, 2.8, INK, "inter")
    p.append(t)
    with open(os.path.join(OUT, "merch-concepts.svg"), "w") as fh:
        fh.write(mmdoc(W, H, "".join(p), "LORE merch concepts", scale=6))


if __name__ == "__main__":
    build_cards()
    letterhead()
    envelope()
    mockup_sheet()
    merch()
    print("ok")
