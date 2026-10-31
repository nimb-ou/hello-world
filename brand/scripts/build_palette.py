"""Palette: swatch sheet SVG, contrast matrix SVG, tokens.json, lore-colors.css, palette.ase-like CSV."""
import json
import os

from tokens import CORE, FUNCTIONAL, INK, BONE, FOG, TERRA, hex_to_rgb, rgb_to_cmyk, contrast, mix
from build_logos import label, svg, wordmark_g, f

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "palette")
os.makedirs(OUT, exist_ok=True)

TINT_STEPS = [0.85, 0.7, 0.5, 0.3, 0.15]   # mix toward Bone (lighter)
SHADE_STEPS = [0.2, 0.4]                    # mix toward Ink (darker)


def text_on(hexv):
    return INK if contrast(hexv, INK) >= contrast(hexv, BONE) else BONE


def swatch_sheet():
    W, H = 2400, 1640
    p = []
    g, _ = wordmark_g(80, 70, 36, INK)
    p.append(g)
    t, _ = label("COLOUR SYSTEM · v1.0", W - 80, 100, 18, FOG, "mono", tracking=0.14, anchor="end")
    p.append(t)
    t, _ = label("Warm ground, dark ink, one terracotta voice.", 80, 210, 56, INK, "fraunces")
    p.append(t)
    t, _ = label("Proportion guide: Bone 60 · Ink 25 · Terracotta 7 · Brass/Olive/Fog/Night 8 (combined). Values: sRGB master; CMYK naive (confirm with printer ICC); Pantone = nearest candidate, unverified.",
                 80, 260, 19, FOG, "inter")
    p.append(t)
    # proportion bar
    x = 80
    bw = W - 160
    for name, hexv, share in [("Bone", BONE, .60), ("Ink", INK, .25), ("Terracotta", TERRA, .07),
                              ("Brass", CORE[3][1], .03), ("Olive", CORE[4][1], .02), ("Fog", CORE[5][1], .015), ("Night", CORE[6][1], .015)]:
        w = bw * share
        p.append(f'<rect x="{f(x)}" y="300" width="{f(w)}" height="56" fill="{hexv}" stroke="{INK}" stroke-opacity=".08"/>')
        x += w
    # big swatches
    cw = (W - 160 - 6 * 20) / 7
    for i, (name, hexv, role, pms) in enumerate(CORE):
        x0 = 80 + i * (cw + 20)
        y0 = 400
        p.append(f'<rect x="{f(x0)}" y="{y0}" width="{f(cw)}" height="520" fill="{hexv}" stroke="{INK}" stroke-opacity=".10"/>')
        tc = text_on(hexv)
        t, _ = label(name, x0 + 24, y0 + 62, 38, tc, "fraunces")
        p.append(t)
        t, _ = label(f"{i + 1:02d}", x0 + cw - 24, y0 + 50, 15, tc, "mono", anchor="end")
        p.append(t)
        r, g_, b = hex_to_rgb(hexv)
        c, m, y, k = rgb_to_cmyk((r, g_, b))
        rows = [("HEX", hexv), ("RGB", f"{r} {g_} {b}"), ("CMYK", f"{c} {m} {y} {k}"),
                ("PMS", pms.split(" / ")[0].replace(" (solid)", "")),
                ("vs INK", f"{contrast(hexv, INK):.1f}:1"), ("vs BONE", f"{contrast(hexv, BONE):.1f}:1")]
        yy = y0 + 330
        for k_, v in rows:
            t, _ = label(k_, x0 + 24, yy, 13, tc, "mono", tracking=0.12)
            p.append(t)
            t, _ = label(v, x0 + 104, yy, 16, tc, "mono", wght=500)
            p.append(t)
            yy += 30
        # tints
        ty = 950
        steps = TINT_STEPS + [0] + SHADE_STEPS
        sh = 36
        toward = INK if name == "Bone" else BONE
        for j, s in enumerate(TINT_STEPS):
            hv = mix(hexv, toward, s if name != "Bone" else (1 - s) * 0.5)
            p.append(f'<rect x="{f(x0)}" y="{ty + j * sh}" width="{f(cw)}" height="{sh}" fill="{hv}"/>')
            lab = f"{int((1 - s) * 100)}" if name != "Bone" else f"+{int((1 - s) * 50)}K"
            t, _ = label(f"{lab}  {hv}", x0 + 14, ty + j * sh + 24, 12, text_on(hv), "mono")
            p.append(t)
        for j, s in enumerate(SHADE_STEPS):
            hv = mix(hexv, "#000000" if name in ("Ink", "Night") else INK, s)
            yy = ty + (len(TINT_STEPS) + j) * sh
            p.append(f'<rect x="{f(x0)}" y="{yy}" width="{f(cw)}" height="{sh}" fill="{hv}"/>')
            t, _ = label(f"+{int(s * 100)}K {hv}", x0 + 14, yy + 24, 12, text_on(hv), "mono")
            p.append(t)
        # role
        words = role.split()
        line, lines = "", []
        for w_ in words:
            if len(line) + len(w_) > 30:
                lines.append(line)
                line = w_
            else:
                line = (line + " " + w_).strip()
        lines.append(line)
        yy = 1250
        for ln in lines:
            t, _ = label(ln, x0, yy, 15, INK, "inter")
            p.append(t)
            yy += 22
    # functional
    t, _ = label("FUNCTIONAL — UI & SAFETY ONLY, NEVER DECORATIVE", 80, 1400, 16, FOG, "mono", tracking=0.14)
    p.append(t)
    for i, (name, hexv, role, pms) in enumerate(FUNCTIONAL):
        x0 = 80 + i * 760
        p.append(f'<rect x="{x0}" y="1430" width="120" height="120" fill="{hexv}"/>')
        r, g_, b = hex_to_rgb(hexv)
        t, _ = label(name, x0 + 150, 1470, 32, INK, "fraunces")
        p.append(t)
        t, _ = label(f"{hexv} · RGB {r} {g_} {b} · CMYK {' '.join(map(str, rgb_to_cmyk((r, g_, b))))} · PMS {pms}", x0 + 150, 1505, 14, INK, "mono")
        p.append(t)
        t, _ = label(role, x0 + 150, 1537, 16, FOG, "inter")
        p.append(t)
    return svg(W, H, "".join(p), "LORE colour palette", bg=BONE)


def contrast_matrix():
    cols = CORE + FUNCTIONAL
    n = len(cols)
    c = 120
    W, H = 260 + n * c + 60, 230 + n * c + 120
    p = []
    t, _ = label("WCAG 2.2 CONTRAST MATRIX — TEXT COLOUR (ROW) ON BACKGROUND (COLUMN)", 60, 80, 18, INK, "mono", tracking=0.1)
    p.append(t)
    t, _ = label("AAA ≥ 7 · AA ≥ 4.5 · AA-large ≥ 3 (18.66 px bold / 24 px) · — fails, do not use for text", 60, 120, 16, FOG, "inter")
    p.append(t)
    for j, (name, hexv, *_r) in enumerate(cols):
        x = 260 + j * c
        p.append(f'<rect x="{x}" y="150" width="{c}" height="60" fill="{hexv}"/>')
        t, _ = label(name.upper(), x + c / 2, 186, 12, text_on(hexv), "mono", anchor="middle", tracking=0.08)
        p.append(t)
    for i, (rn, rh, *_r) in enumerate(cols):
        y = 230 + i * c
        t, _ = label(rn, 60, y + c / 2 + 8, 22, INK, "fraunces")
        p.append(t)
        p.append(f'<rect x="200" y="{y + c / 2 - 18}" width="36" height="36" fill="{rh}" stroke="{INK}" stroke-opacity=".15"/>')
        for j, (cn, ch, *_q) in enumerate(cols):
            x = 260 + j * c
            p.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{ch}" stroke="{BONE}" stroke-width="2"/>')
            if i == j:
                continue
            r = contrast(rh, ch)
            grade = "AAA" if r >= 7 else "AA" if r >= 4.5 else "AA-L" if r >= 3 else "—"
            t, _ = label("Aa", x + 16, y + 52, 34, rh, "fraunces")
            p.append(t)
            tc = text_on(ch)
            t, _ = label(f"{r:.1f}", x + 16, y + 86, 15, tc, "mono", wght=600)
            p.append(t)
            t, _ = label(grade, x + 16, y + 106, 12, tc, "mono", tracking=0.1)
            p.append(t)
    return svg(W, H, "".join(p), "LORE contrast matrix", bg=BONE)


def tokens():
    data = {"version": "1.0.0", "updated": "2026-10-30", "source": "brand/brand-guidelines.md §8",
            "colors": {}, "functional": {}, "tints": {}}
    for name, hexv, role, pms in CORE:
        r, g, b = hex_to_rgb(hexv)
        data["colors"][name.lower()] = {"hex": hexv, "rgb": [r, g, b], "cmyk_naive": list(rgb_to_cmyk((r, g, b))),
                                        "pantone_candidate_unverified": pms, "role": role}
        data["tints"][name.lower()] = {str(int((1 - s) * 100)): mix(hexv, BONE, s) for s in TINT_STEPS}
    for name, hexv, role, pms in FUNCTIONAL:
        r, g, b = hex_to_rgb(hexv)
        data["functional"][name.lower()] = {"hex": hexv, "rgb": [r, g, b], "cmyk_naive": list(rgb_to_cmyk((r, g, b))),
                                            "pantone_candidate_unverified": pms, "role": role}
    data["semantic"] = {
        "light": {"bg": BONE, "surface": "#EAE3D7", "text": INK, "text-muted": "#5C5F66", "hairline": mix(FOG, BONE, 0.5),
                  "accent": TERRA, "accent-text-on": BONE, "link": "#A84E2A", "focus": TERRA},
        "dark": {"bg": CORE[6][1], "surface": "#13263A", "text": BONE, "text-muted": FOG, "hairline": "#2A3A4C",
                 "accent": "#D9774E", "accent-text-on": INK, "link": "#E59A78", "focus": "#D9774E"},
        "device-amoled": {"bg": "#000000", "text": BONE, "accent": TERRA, "sos": FUNCTIONAL[0][1]},
    }
    with open(os.path.join(OUT, "tokens.json"), "w") as fh:
        json.dump(data, fh, indent=2)
    css = [":root {", "  /* LORE colour tokens v1.0 — generated by brand/scripts/build_palette.py */"]
    for name, hexv, *_ in CORE + FUNCTIONAL:
        css.append(f"  --lore-{name.lower()}: {hexv};")
    for name, d in data["tints"].items():
        for k, v in d.items():
            css.append(f"  --lore-{name}-{k}: {v};")
    for k, v in data["semantic"]["light"].items():
        css.append(f"  --lore-{k}: {v};")
    css.append("}")
    css.append("@media (prefers-color-scheme: dark) {\n  :root {")
    for k, v in data["semantic"]["dark"].items():
        css.append(f"    --lore-{k}: {v};")
    css.append("  }\n}")
    with open(os.path.join(OUT, "lore-colors.css"), "w") as fh:
        fh.write("\n".join(css) + "\n")
    with open(os.path.join(OUT, "palette.csv"), "w") as fh:
        fh.write("name,hex,r,g,b,c,m,y,k,pantone_candidate_unverified,contrast_vs_ink,contrast_vs_bone,role\n")
        for name, hexv, role, pms in CORE + FUNCTIONAL:
            r, g, b = hex_to_rgb(hexv)
            c, m, y, k = rgb_to_cmyk((r, g, b))
            fh.write(f'{name},{hexv},{r},{g},{b},{c},{m},{y},{k},"{pms}",{contrast(hexv, INK):.2f},{contrast(hexv, BONE):.2f},"{role}"\n')


if __name__ == "__main__":
    with open(os.path.join(OUT, "palette.svg"), "w") as fh:
        fh.write(swatch_sheet())
    with open(os.path.join(OUT, "contrast-matrix.svg"), "w") as fh:
        fh.write(contrast_matrix())
    tokens()
    for name, hexv, *_ in CORE + FUNCTIONAL:
        print(f"{name:11s} {hexv}  vsInk {contrast(hexv, INK):5.2f}  vsBone {contrast(hexv, BONE):5.2f}  cmyk {rgb_to_cmyk(hex_to_rgb(hexv))}")
