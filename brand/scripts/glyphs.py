"""Outline text from the brand's OFL variable fonts into SVG path data.

Used by build_logos.py so that every logo SVG is font-independent (pure paths).
"""
import os
from functools import lru_cache
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "typography", "fonts")
FILES = {
    "fraunces": "fraunces-latin-full-normal.woff2",
    "fraunces-italic": "fraunces-latin-full-italic.woff2",
    "inter": "inter-latin-opsz-normal.woff2",
    "mono": "jetbrains-mono-latin-wght-normal.woff2",
}


@lru_cache(maxsize=None)
def font(name, **axes):
    f = TTFont(os.path.join(FONTS, FILES[name]))
    return instancer.instantiateVariableFont(f, axes, inplace=False)


def text_path(text, name, size, x=0.0, y=0.0, tracking=0.0, kern=True, **axes):
    """Return (svg_path_d, advance_width_px, bbox) for `text` at baseline (x, y).

    tracking is in em units (0.1 = 10% of font size added after each glyph).
    """
    f = font(name, **tuple_axes(axes))
    upm = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    hmtx = f["hmtx"]
    s = size / upm
    pen = SVGPathPen(gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
    bpen = BoundsPen(gs)
    cx = x
    FALLBACK = {'→': '->', '≤': '<=', '≥': '>=', '×': 'x', '−': '-', '–': '-', '—': '-'}
    text = ''.join(c if ord(c) in cmap else FALLBACK.get(c, '?') for c in text)
    names = [cmap.get(ord(c), cmap[ord('?')]) for c in text]
    kerning = gpos_pairs(f) if kern else {}
    for i, g in enumerate(names):
        t = (s, 0, 0, -s, cx, y)
        gs[g].draw(TransformPen(pen, t))
        gs[g].draw(TransformPen(bpen, t))
        adv = hmtx[g][0]
        if i + 1 < len(names):
            adv += kerning.get((g, names[i + 1]), 0)
        cx += adv * s + (tracking * size if i + 1 < len(names) else 0)
    return pen.getCommands(), cx - x, bpen.bounds


def tuple_axes(axes):
    return axes


@lru_cache(maxsize=None)
def _pairs_cache(id_):
    return {}


def gpos_pairs(f):
    """Very small PairPos (format 1 + 2) reader for kerning."""
    out = {}
    if "GPOS" not in f:
        return out
    gpos = f["GPOS"].table
    for lookup in gpos.LookupList.Lookup:
        subs = lookup.SubTable
        for st in subs:
            if lookup.LookupType == 9:
                st = st.ExtSubTable
            if getattr(st, "LookupType", lookup.LookupType) != 2:
                continue
            cov = st.Coverage.glyphs
            if st.Format == 1:
                for i, first in enumerate(cov):
                    for pvr in st.PairSet[i].PairValueRecord:
                        v = getattr(pvr.Value1, "XAdvance", 0) if pvr.Value1 else 0
                        out.setdefault((first, pvr.SecondGlyph), v)
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs
                c2 = st.ClassDef2.classDefs
                second_by_class = {}
                for g, c in c2.items():
                    second_by_class.setdefault(c, []).append(g)
                for first in cov:
                    k1 = c1.get(first, 0)
                    rec = st.Class1Record[k1]
                    for k2, r2 in enumerate(rec.Class2Record):
                        v = getattr(r2.Value1, "XAdvance", 0) if r2.Value1 else 0
                        if v:
                            for sec in second_by_class.get(k2, []):
                                out.setdefault((first, sec), v)
    return out
