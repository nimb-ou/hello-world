"""LORE general-arrangement drawings (A3, 2:1, third-angle) generated from params.json.

Run from anywhere:  python3 design/industrial/scripts/drawings.py
Writes design/industrial/drawings/<sku>.svg and <sku>.png (PNG preview via cairosvg).
Geometry mirrors lib/lore-geometry.js (same outlines and section profiles), so a change to
params.json moves the 3D models, the renders and these drawings together.
"""
import json, math, os, datetime
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D)
P = json.load(open(os.path.join(ROOT, 'params.json')))
try: MB = json.load(open(os.path.join(ROOT, 'mass-budget.json')))
except FileNotFoundError: MB = {}
OUT = os.path.join(ROOT, 'drawings'); os.makedirs(OUT, exist_ok=True)
K = 2.0  # drawing scale 2:1
INK, CTF, THIN, HID = '#14161A', '#C4623A', '#55585E', '#8A8D92'
FONT = "Inter, 'DejaVu Sans', 'Liberation Sans', sans-serif"; MONO = "'JetBrains Mono', 'DejaVu Sans Mono', monospace"

# ---------------------------------------------------------------- outlines (same maths as lore-geometry.js)
sgnpow = lambda v, e: math.copysign(abs(v) ** e, v)
def superellipse(w, h, n, N=720):
    return [(sgnpow(math.cos(t), 2 / n) * w / 2, sgnpow(math.sin(t), 2 / n) * h / 2) for t in (2 * math.pi * i / N for i in range(N))]
def squircle(w, h, r, n=2.0, Q=90):
    cx, cy, pts = w / 2 - r, h / 2 - r, []
    for x0, y0, q in [(cx, cy, 0), (-cx, cy, 1), (-cx, -cy, 2), (cx, -cy, 3)]:
        for i in range(Q + 1):
            t = (q + i / Q) * math.pi / 2; pts.append((x0 + r * sgnpow(math.cos(t), 2 / n), y0 + r * sgnpow(math.sin(t), 2 / n)))
    return pts
def normals(pts):
    out = []
    for i in range(len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[(i + 1) % len(pts)]
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; out.append((dy / L, -dx / L))
    return out
def offset(pts, o, s=1.0):
    return [((x + nx * o) * s, (y + ny * o) * s) for (x, y), (nx, ny) in zip(pts, normals(pts))]
def arc(cx, cy, r, a0, a1, n=24):
    return [(cx + r * math.cos(a0 + (a1 - a0) * k / n), cy + r * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]

# ---------------------------------------------------------------- half-section profiles (r outward, z up from back)
def pebble_profile(p):
    R, H, rt, rb, zb = p['plan_w'] / 2, p['body_h'], p['fillet_top'], p['fillet_bottom'], p['dome_bottom']
    sd = p['dish_s']
    top = lambda s: p['dome_top'] * (1 - s * s) if s >= sd else p['dome_top'] * (1 - sd * sd) - p['dish_depth'] * (1 - (s / sd) ** 2)
    pr = [((R - rb) * k / 20, zb - p['dome_bottom'] * (1 - (k / 20) ** 2)) for k in range(21)]
    pr += arc(R - rb, zb + rb, rb, -math.pi / 2, 0)[1:] + arc(R - rt, zb + H - rt, rt, 0, math.pi / 2)[1:]
    pr += [((R - rt) * (1 - k / 40), zb + H + top(1 - k / 40)) for k in range(1, 41)]
    ring_z = zb + H + top((p['led_ring_s_in'] + p['led_ring_s_out']) / 2) + 0.06
    return pr, {'zmax': ring_z, 'zdish': zb + H + top(0), 'zring_edge': zb + H + top(sd), 'zmid': zb + rb + (H - rt - rb) / 2}
def slate_profile(s):
    R, H, rt, rb, zb = s['plan_w'] / 2, s['frame_h'], s['fillet_front'], s['fillet_back'], s['back_bulge']
    bR = R - s['back_cover_inset']; gR = (R - rt) * s['glass_s']; zt = zb + H + s['glass_proud']
    pr = [(bR * k / 20, zb - ((zb - 0.12) * (1 - (k / 20) ** 2) + 0.12)) for k in range(21)] + [(bR, zb), (R - rb, zb)]
    pr += arc(R - rb, zb + rb, rb, -math.pi / 2, 0)[1:] + arc(R - rt, zb + H - rt, rt, 0, math.pi / 2)[1:]
    pr += [((R - rt) * s['chamfer_s'][0], zb + H), ((R - rt) * s['chamfer_s'][1], zb + H - 0.35), (gR, zb + H - 0.35), (gR, zt - 0.35)]
    pr += arc(gR - 0.35, zt - 0.35, 0.35, 0, math.pi / 2, 8)[1:] + [(0, zt)]
    return pr, {'zmax': zt, 'zmid': zb + rb + (H - rb - rt) / 2, 'zglass_bottom': zt - s['glass_t'], 'zfront': zb + H}
def full_silhouette(pr):  # mirror half-section -> closed loop in (u = r, v = z)
    return [(-r, z) for r, z in reversed(pr)] + [(r, z) for r, z in pr]

# ---------------------------------------------------------------- SVG primitives
class Sheet:
    def __init__(s): s.e = []
    def add(s, x): s.e.append(x)
    def poly(s, pts, w=0.35, c=INK, fill='none', dash=None, close=True):
        d = ' '.join(f'{x:.3f},{y:.3f}' for x, y in pts)
        s.add(f'<{"polygon" if close else "polyline"} points="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + ' stroke-linejoin="round"/>')
    def line(s, x1, y1, x2, y2, w=0.18, c=THIN, dash=None):
        s.add(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{c}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def circ(s, x, y, r, w=0.25, c=INK, fill='none', dash=None):
        s.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" stroke="{c}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def rect(s, x, y, w, h, rx=0, sw=0.25, c=INK, fill='none'):
        s.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx:.3f}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')
    def text(s, x, y, t, size=2.6, anchor='middle', c=INK, rot=0, font=FONT, weight=400):
        tr = f' transform="rotate({rot} {x:.3f} {y:.3f})"' if rot else ''
        s.add(f'<text x="{x:.3f}" y="{y:.3f}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{c}" text-anchor="{anchor}"{tr}>{t}</text>')
    def arrow(s, x, y, ang, c=INK):
        L, W = 2.2, 0.75; a, b = ang + math.pi, ang
        p = [(x, y), (x + L * math.cos(a) + W * math.cos(a + math.pi / 2), y + L * math.sin(a) + W * math.sin(a + math.pi / 2)),
             (x + L * math.cos(a) - W * math.cos(a + math.pi / 2), y + L * math.sin(a) - W * math.sin(a + math.pi / 2))]
        s.add('<polygon points="' + ' '.join(f'{u:.3f},{v:.3f}' for u, v in p) + f'" fill="{c}"/>')
    def hdim(s, x1, x2, yref, ydim, t, ctf=False, ref2=None):
        c = CTF if ctf else INK; sg = 1 if ydim > yref else -1
        for x, yr in ((x1, yref), (x2, ref2 if ref2 is not None else yref)):
            s.line(x, yr + sg * 0.8, x, ydim + sg * 1.5, 0.13, c)
        s.line(x1, ydim, x2, ydim, 0.18, c)
        inside = abs(x2 - x1) > 9
        s.arrow(x1, ydim, math.pi if inside else 0, c); s.arrow(x2, ydim, 0 if inside else math.pi, c)
        if not inside: s.line(min(x1, x2) - 4, ydim, max(x1, x2) + 4, ydim, 0.18, c)
        s.text((x1 + x2) / 2, ydim - 0.9, t, 2.5, c=c)
    def vdim(s, y1, y2, xref, xdim, t, ctf=False, ref2=None):
        c = CTF if ctf else INK; sg = 1 if xdim > xref else -1
        for y, xr in ((y1, xref), (y2, ref2 if ref2 is not None else xref)):
            s.line(xr + sg * 0.8, y, xdim + sg * 1.5, y, 0.13, c)
        s.line(xdim, y1, xdim, y2, 0.18, c)
        inside = abs(y2 - y1) > 9
        s.arrow(xdim, y1, -math.pi / 2 if inside else math.pi / 2, c); s.arrow(xdim, y2, math.pi / 2 if inside else -math.pi / 2, c)
        if not inside: s.line(xdim, min(y1, y2) - 4, xdim, max(y1, y2) + 4, 0.18, c)
        s.text(xdim - 0.9, (y1 + y2) / 2, t, 2.5, c=c, rot=-90)
    def leader(s, x0, y0, x1, y1, t, ctf=False, anchor=None):
        c = CTF if ctf else INK
        s.line(x0, y0, x1, y1, 0.15, c); s.arrow(x0, y0, math.atan2(y0 - y1, x0 - x1), c)
        a = anchor or ('start' if x1 >= x0 else 'end'); x2 = x1 + (8 if a == 'start' else -8)
        s.line(x1, y1, x2, y1, 0.15, c); s.text(x2 + (0.8 if a == 'start' else -0.8), y1 + 0.9, t, 2.4, anchor=a, c=c)
    def balloon(s, feat, at, n, ctf=False, r=2.3):
        c = CTF if ctf else INK; (fx, fy), (bx, by) = feat, at; d = math.hypot(bx - fx, by - fy) or 1
        s.line(fx, fy, bx - (bx - fx) / d * r, by - (by - fy) / d * r, 0.15, c); s.circ(fx, fy, 0.35, 0.1, c, fill=c)
        s.circ(bx, by, r, 0.25, c, fill='#FBFAF7'); s.text(bx, by + 0.85, str(n), 2.4, c=c, weight=500)
    def centre(s, x1, y1, x2, y2): s.line(x1, y1, x2, y2, 0.12, HID, '6 1.2 1 1.2')
    def label(s, x, y, t): s.text(x, y, t, 2.6, c=THIN, font=MONO, weight=500)
    def svg(s):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297">'
                '<rect width="420" height="297" fill="#FBFAF7"/>' + ''.join(s.e) + '</svg>')

# view transforms (model mm -> sheet mm). Third-angle: top above front, bottom below, right to the right, left to the left, back right of right.
def V(cx, cy, fx, fy): return lambda u, v: (cx + K * fx(u, v), cy + K * fy(u, v))

def draw(sku):
    is_peb = sku == 'pebble'
    if is_peb:
        p = P['pebble']; W = p['plan_w']; plan = superellipse(W, p['plan_h'], p['superellipse_n'])
        prof, z = pebble_profile(p)
    else:
        p = dict(P['square']); p.update(P['atlas'] if sku == 'atlas' else {}); p['frame_h'] = p['thickness_total'] - p['back_bulge'] - p['glass_proud']
        W = p['plan_w']; plan = squircle(W, p['plan_h'], p['corner_r'], p['corner_n'])
        prof, z = slate_profile(p)
    T = z['zmax']; Hh = W / 2; S = Sheet(); m = P['mount']; C = []  # C = callout texts, numbered in order of balloon()
    def balloon(feat, at, text, ctf=False):
        C.append((text, ctf)); n = len(C); S.balloon(feat, at, n, ctf); return n
    S.rect(10, 10, 400, 277, sw=0.5); S.rect(12, 12, 396, 273, sw=0.18, c=THIN)
    fx_, fy_, gap = 125, 135, 20
    front = V(fx_, fy_, lambda u, v: u, lambda u, v: -v)
    topv = V(fx_, fy_ - K * Hh - gap - K * T / 2, lambda u, v: u, lambda u, v: v - T / 2)       # u = x, v = z
    botv = V(fx_, fy_ + K * Hh + gap + K * T / 2, lambda u, v: u, lambda u, v: -(v - T / 2))
    rx = fx_ + K * Hh + gap + K * T / 2
    right = V(rx, fy_, lambda u, v: -(v - T / 2), lambda u, v: -u)                                # u = y, v = z
    lx = fx_ - K * Hh - gap - K * T / 2
    left = V(lx, fy_, lambda u, v: (v - T / 2), lambda u, v: -u)
    bx = rx + K * T / 2 + 30 + K * Hh
    back = V(bx, fy_, lambda u, v: -u, lambda u, v: -v)
    sil = full_silhouette(prof); tf = lambda f, pts: [f(u, v) for u, v in pts]
    vlabel = lambda x, y, t, a='middle': S.text(x, y, t, 2.6, a, THIN, font=MONO, weight=500)
    zm = z['zmid']
    # ------------------------------------------------ FRONT
    S.poly(tf(front, plan), 0.4)
    S.centre(*front(-Hh - 4, 0), *front(Hh + 4, 0)); S.centre(*front(0, -Hh - 4), *front(0, Hh + 4))
    S.hdim(front(-Hh, 0)[0], front(Hh, 0)[0], front(0, Hh)[1], front(0, Hh)[1] - 12, f'{W:.1f}', True)
    S.vdim(front(0, Hh)[1], front(0, -Hh)[1], front(-Hh, 0)[0], front(-Hh, 0)[0] - 10, f'{p["plan_h"]:.1f}', True)
    d45 = lambda pts, sgx, sgy: max(pts, key=lambda q: sgx * q[0] + sgy * q[1])
    if is_peb:
        inner = offset(plan, -p['fillet_top']); sc = lambda s_: [(x * s_, y * s_) for x, y in inner]
        S.poly(tf(front, sc(p['led_ring_s_out'])), 0.25); S.poly(tf(front, sc(p['led_ring_s_in'])), 0.25)
        S.poly(tf(front, sc(0.999)), 0.12, THIN, dash='1.2 0.8')
        rr = (W - 2 * p['fillet_top']) / 2 * (p['led_ring_s_in'] + p['led_ring_s_out']) / 2
        for k in range(8):  # hardware: 8 RGB LEDs on LP5024
            a = math.pi / 2 + k * math.pi / 4; S.circ(*front(rr * 0.97 * math.cos(a), rr * 0.97 * math.sin(a)), 0.5, 0.12, HID, dash='0.6 0.4')
        rk = Hh; S.poly(tf(front, [(rk - 0.2, -4.5), (rk + 0.45, -4.5), (rk + 0.45, 4.5), (rk - 0.2, 4.5)]), 0.3)
        dw = (W - 2 * p['fillet_top']) * p['led_ring_s_in']; ow = (W - 2 * p['fillet_top']) * p['led_ring_s_out']
        S.hdim(front(-ow / 2, 0)[0], front(ow / 2, 0)[0], front(0, 0)[1], front(0, -Hh)[1] + 6, f'{ow:.1f} RING O/F', ref2=None)
        balloon(front(*d45(plan, -1, 1)), front(-Hh - 3, Hh + 3), f'Plan: superellipse {W:.0f}×{p["plan_h"]:.0f}, n = {p["superellipse_n"]}; top fillet R{p["fillet_top"]}, bottom R{p["fillet_bottom"]}')
        balloon(front(-dw / 2 * 0.55, dw / 2 * 0.55), front(-4, 4), f'Talk dish: whole cap ≈{dw:.1f} A/F, {p["dish_depth"]} concave, 0.35 travel, 2.4 N dome')
        balloon(front(rr * 0.72, -rr * 0.72), front(Hh * 0.95, -Hh * 0.95), f'LED ring: frosted PMMA {dw:.1f}–{ow:.1f} A/F, 8 RGB LEDs (LP5024)')
        balloon(front(rk + 0.45, 2), front(Hh + 7, 12), 'Volume rocker, east side: 9.0 × 2.6 pill, 0.45 proud at centre, 0.25 travel')
    else:
        S.poly(tf(front, offset(plan, -p['fillet_front'], p['chamfer_s'][0])), 0.18, THIN)
        gw = (W - 2 * p['fillet_front']) * p['glass_s']; S.poly(tf(front, offset(plan, -p['fillet_front'], p['glass_s'])), 0.3)
        a = p['display_active'] / 2; S.rect(*front(-a, a), K * 2 * a, K * 2 * a, rx=K * p['display_r'], sw=0.18, c=THIN)
        S.rect(*front(Hh - 0.15, p['crown_y'] + p['crown_d'] / 2), K * (p['crown_protrusion'] + 0.15), K * p['crown_d'], sw=0.3)
        for k in range(1, 8): S.line(*front(Hh + 0.15, p['crown_y'] - 3 + k * 0.75), *front(Hh + p['crown_protrusion'], p['crown_y'] - 3 + k * 0.75), 0.08, THIN)
        S.rect(*front(Hh - 0.3, p['talk_y'] + p['talk_w'] / 2), K * (p['talk_protrusion'] + 0.3), K * p['talk_w'], rx=0.6, sw=0.3, fill='#E7B9A5')
        S.hdim(front(-gw / 2, 0)[0], front(gw / 2, 0)[0], front(0, gw / 2)[1], front(0, Hh)[1] - 5, f'{gw:.2f} GLASS A/F')
        S.vdim(front(0, a)[1], front(0, -a)[1], front(-a, 0)[0], front(-Hh, 0)[0] - 4, f'{2 * a:.2f} AA')
        S.vdim(front(0, 0)[1], front(0, p['crown_y'])[1], front(Hh + p['crown_protrusion'], 0)[0], front(Hh, 0)[0] + 9, f'{p["crown_y"]:.1f}')
        S.vdim(front(0, 0)[1], front(0, p['talk_y'])[1], front(Hh + 1, 0)[0], front(Hh, 0)[0] + 9, f'{abs(p["talk_y"]):.1f}')
        balloon(front(*d45(plan, -1, 1)), front(-Hh - 3, Hh + 3), f'Plan: rounded square, R{p["corner_r"]:.0f} corners, curvature-continuous blend n = {p["corner_n"]}')
        balloon(front(-gw / 2, -14), front(-Hh - 4, -18), ('Cover: sapphire ' if sku == 'atlas' else 'Cover: Gorilla Glass Victus 2, ') + f'{p["glass_t"]} thk, 2.5D, {p["glass_proud"]} proud; DC chamfer 0.35×45°')
        balloon(front(a - 1.6, -a + 1.6), front(a - 7, -a + 7), f'1.6" AMOLED {p["display_px"]}×{p["display_px"]}, active {2 * a:.2f} sq., R{p["display_r"]}, on-cell touch')
        if sku == 'atlas':
            cy = p['camera_y']; S.circ(*front(0, cy), K * p['camera_window_d'] / 2, 0.25); S.circ(*front(0, cy), K * p['camera_lens_d'] / 2, 0.2, THIN)
            S.circ(*front(p['privacy_led_dx'], cy), K * 0.35, 0.2, CTF)
            S.vdim(front(0, 0)[1], front(0, cy)[1], front(-p['camera_window_d'] / 2, 0)[0], front(-a, 0)[0] + 3, f'{cy:.1f}')
            balloon(front(-p['camera_window_d'] / 2, cy), front(-11, cy), f'Glance camera: Ø{p["camera_window_d"]} polished trim, Ø{p["camera_lens_d"]} lens, OV13B10')
            balloon(front(p['privacy_led_dx'] + 0.35, cy), front(11, cy), f'Privacy LED Ø0.7 at x = +{p["privacy_led_dx"]}, hard-wired to sensor power', True)
    vlabel(front(-Hh, 0)[0], front(0, -Hh)[1] + 6, 'FRONT', 'start')
    # ------------------------------------------------ TOP / BOTTOM edges
    for view, name, edge in ((topv, 'TOP', 1), (botv, 'BOTTOM', -1)):
        S.poly(tf(view, sil), 0.4); S.centre(*view(0, -1.5), *view(0, T + 1.5))
        out_y = view(0, -1)[1] - 6 if edge == 1 else view(0, -1)[1] + 6   # first dim lane (away from the front view)
        step = -6 if edge == 1 else 6
        if is_peb:
            S.poly([view(Hh - 0.2, zm - 1.3), view(Hh + 0.45, zm - 1.3), view(Hh + 0.45, zm + 1.3), view(Hh - 0.2, zm + 1.3)], 0.3)
            if edge == 1:
                for sx in (-1, 1): S.circ(*view(sx * p['mic_spacing'] / 2, zm + 0.8), K * p['mic_port_d'] / 2, 0.2)
                S.hdim(view(-p['mic_spacing'] / 2, 0)[0], view(p['mic_spacing'] / 2, 0)[0], view(0, zm + 0.8)[1], out_y, f'{p["mic_spacing"]:.1f}')
                balloon(view(p['mic_spacing'] / 2 + 0.4, zm + 0.8), view(Hh * 0.62, T + 3), f'Mics: 2× Ø{p["mic_port_d"]} on north edge, {p["mic_spacing"]} apart (beam axis forward), ePTFE')
                S.vdim(view(0, 0)[1], view(0, T)[1], view(-Hh, 0)[0], view(-Hh, 0)[0] - 8, f'{T:.2f}', True)
            else:
                n = p['speaker_holes']; xs_ = [(k - (n - 1) / 2) * p['speaker_hole_pitch'] for k in range(n)]
                for x in xs_: S.circ(*view(x, zm), K * p['speaker_hole_d'] / 2, 0.18)
                S.hdim(view(xs_[0], 0)[0], view(xs_[-1], 0)[0], view(0, zm)[1], out_y, f'{n - 1}×{p["speaker_hole_pitch"]}')
                balloon(view(xs_[-1] + 0.4, zm), view(Hh * 0.62, T + 3), f'Speaker 13×9: {n}× Ø{p["speaker_hole_d"]} @ {p["speaker_hole_pitch"]} on south edge, ePTFE')
        else:
            sw = p['antenna_split_w']; zb_, zf = p['back_bulge'] + p['fillet_back'], z['zfront'] - p['fillet_front']
            for sx in (-1, 1): S.rect(*view(sx * 12 - sw / 2, zb_ - 0.6 if edge == 1 else zf + 0.6), K * sw, K * (zf - zb_ + 1.2), sw=0.15, c=THIN, fill='#D9D6D0')
            S.rect(*view(Hh - 0.15, zm - p['crown_d'] / 2 if edge == 1 else zm + p['crown_d'] / 2), K * (p['crown_protrusion'] + 0.15), K * p['crown_d'], sw=0.3)
            if edge == 1:
                for sx in (-1, 1): S.circ(*view(sx * 6, zm), K * p['mic_port_d'] / 2, 0.2)
                S.hdim(view(-6, 0)[0], view(6, 0)[0], view(0, zm)[1], out_y, '12.0')
                S.hdim(view(-12, 0)[0], view(12, 0)[0], view(0, 0)[1], out_y + step, '24.0')
                S.vdim(view(0, 0)[1], view(0, T)[1], view(-Hh, 0)[0], view(-Hh, 0)[0] - 8, f'{T:.2f}', True)
                balloon(view(-6 - 0.4, zm), view(-Hh * 0.62, T + 3), 'Mics: 2× Ø0.8 top edge at x = ±6 (beamforming) + 1 bottom (AEC ref)')
                balloon(view(12 + sw / 2, zm), view(Hh * 0.62, T + 3), f'NMT antenna splits (PBT), {sw} wide, x = ±12, top and bottom edges')
            else:
                uw, uh = p['usb_c_opening']; S.rect(*view(-uw / 2, zm + uh / 2), K * uw, K * uh, rx=K * uh / 2, sw=0.3)
                S.rect(*view(-3.3, zm + 0.35), K * 6.6, K * 0.7, rx=0.3, sw=0.12, c=THIN)
                for k in range(p['speaker_slots']):
                    x = 8.5 + k * 1.7; S.rect(*view(x - p['speaker_slot'][1] / 2, zm + p['speaker_slot'][0] / 2), K * p['speaker_slot'][1], K * p['speaker_slot'][0], rx=0.6, sw=0.18)
                S.circ(*view(-10, zm), K * p['mic_port_d'] / 2, 0.2)
                S.hdim(view(-uw / 2, 0)[0], view(uw / 2, 0)[0], view(0, zm - uh / 2)[1], out_y, f'{uw}', True)
                lane2 = out_y + step; stop = out_y + 1.2
                S.hdim(view(-10, 0)[0], view(0, 0)[0], view(0, zm)[1], lane2, '10.0', ref2=stop)
                S.hdim(view(0, 0)[0], view(8.5, 0)[0], stop, lane2, '8.5', ref2=view(0, zm)[1])
                S.hdim(view(8.5, 0)[0], view(8.5 + 4 * 1.7, 0)[0], view(0, zm)[1], lane2, '4×1.7')
                balloon(view(uw / 2, zm + 1), view(3, T + 3.5), f'USB-C opening {uw}×{uh}, IPX7 sealed receptacle, USB 2.0 + PD sink', True)
                balloon(view(8.5 + 4 * 1.7 + 0.4, zm), view(Hh * 0.75, T + 3.5), f'Speaker 15×11: {p["speaker_slots"]} slots {p["speaker_slot"][1]}×{p["speaker_slot"][0]} @ 1.7, ePTFE')
        vlabel(view(-Hh, 0)[0] - (18 if edge == 1 else 6), view(0, T / 2)[1] + 0.9, name, 'end')
    # ------------------------------------------------ RIGHT side: y vertical, z horizontal (front toward the front view)
    S.poly(tf(right, sil), 0.4)
    S.centre(*right(0, -1.5), *right(0, T + 1.5)); S.centre(*right(-Hh - 3, zm), *right(Hh + 3, zm))
    y0 = right(-Hh, 0)[1] + 6
    S.hdim(right(0, T)[0], right(0, 0)[0], right(-Hh, 0)[1], y0 + 4, f'{T:.2f} MAX', True)
    if is_peb:
        x1, y1 = right(4.5, zm + 1.3); x2, y2 = right(-4.5, zm - 1.3)
        S.rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1), rx=K * 1.29, sw=0.3)
        bd = p['dome_bottom'] + p['body_h']
        S.hdim(right(0, bd)[0], right(0, 0)[0], right(-Hh, 0)[1], y0 + 10, f'{bd:.2f}')
        balloon(right(0.5, z['zdish']), right(Hh + 3, z['zdish'] + 3), f'Height: dish centre {z["zdish"]:.2f}, LED ring {z["zmax"]:.2f} max (envelope ≤ {p["thickness_total"]})')
        balloon(right(-Hh + 1.2, 1.2), right(-Hh - 2, -3), f'Back dome {p["dome_bottom"]}; wall {p["wall"]} PC+10% GF, 0.8 ribs @ 6')
    else:
        S.circ(*right(p['crown_y'], zm), K * p['crown_d'] / 2, 0.35); S.circ(*right(p['crown_y'], zm), K * (p['crown_d'] / 2 - 0.35), 0.15, THIN)
        x1, y1 = right(p['talk_y'] + p['talk_w'] / 2, zm + p['talk_h'] / 2); x2, y2 = right(p['talk_y'] - p['talk_w'] / 2, zm - p['talk_h'] / 2)
        S.rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1), rx=K * p['talk_h'] / 2, sw=0.3, fill='#E7B9A5')
        S.hdim(right(0, p['back_bulge'])[0], right(0, 0)[0], right(-Hh, 0)[1], y0 + 10, f'{p["back_bulge"]}')
        S.hdim(right(0, T)[0], right(0, z['zfront'])[0], right(-Hh, 0)[1], y0 + 16, f'{p["glass_proud"]}', True)
        balloon(right(p['crown_y'] + p['crown_d'] / 2, zm - 1), right(p['crown_y'] + 6, -4), f'Crown Ø{p["crown_d"]}, {p["crown_protrusion"]} proud, {p["crown_knurl"]}-ridge knurl, optical rotation + push' + (', Ti + ZrN' if sku == 'atlas' else ', 316L'))
        balloon(right(p['talk_y'] - p['talk_w'] / 2, zm - 1), right(p['talk_y'] - 8, -4), f'Talk key {p["talk_w"]}×{p["talk_h"]} pill, {p["talk_protrusion"]} proud, 0.3 travel, 3.0 N, Terracotta')
        balloon(right(-Hh + 0.9, p['back_bulge'] + 0.9), right(-Hh - 2, -3.5), f'Edge radii: back R{p["fillet_back"]}, front R{p["fillet_front"]}; back bulge {p["back_bulge"]}; wall {p["wall"]}')
    vlabel(right(0, T / 2)[0], right(Hh, 0)[1] - 3, 'RIGHT')
    # ------------------------------------------------ LEFT side (slate: SOS)
    if not is_peb:
        S.poly(tf(left, sil), 0.4); S.centre(*left(0, -1.5), *left(0, T + 1.5))
        for (hw, hh, fill, sw_) in ((3.9, 1.9, 'none', 0.25), (3.5, 1.5, '#E7B9A5', 0.2)):
            x1, y1 = left(-2 + hw, zm + hh); x2, y2 = left(-2 - hw, zm - hh)
            S.rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1), rx=K * hh, sw=sw_, fill=fill)
        for k in range(-2, 3): S.line(*left(-2 + k * 1.2, zm - 1.2), *left(-2 + k * 1.2, zm + 1.2), 0.1, THIN)
        S.vdim(left(0, 0)[1], left(-2, 0)[1], left(-Hh, 0)[0], left(0, -1)[0] - 4, '2.0')
        balloon(left(-2 - 3.9, zm), left(-14, T + 4), 'SOS key 7.0×3.0, recessed 0.25 in a ridged pocket, y = −2, 2 s hold', True)
        balloon(left(Hh - 0.6, zm), left(Hh + 3, T + 3), 'Tether hole Ø1.8, cross-drilled through the NW corner')
        vlabel(left(0, T / 2)[0], left(Hh, 0)[1] - 3, 'LEFT')
    # ------------------------------------------------ BACK
    S.poly(tf(back, plan), 0.4)
    S.centre(*back(-Hh - 4, 0), *back(Hh + 4, 0)); S.centre(*back(0, -Hh - 4), *back(0, Hh + 4))
    S.circ(*back(0, 0), K * m['recess_d'] / 2, 0.35, CTF)
    for r_ in (m['magnet_ring_od'] / 2, m['magnet_ring_id'] / 2): S.circ(*back(0, 0), K * r_, 0.15, HID, dash='1.2 0.8')
    for k in range(m['lugs']):
        a = math.pi / 2 + k * 2 * math.pi / m['lugs']; r = m['recess_d'] / 2 - 0.65
        S.circ(*back(r * math.cos(a), r * math.sin(a)), K * 0.5, 0.2, THIN)
    xs = [(k - (m['pogo_count'] - 1) / 2) * m['pogo_pitch'] for k in range(m['pogo_count'])]
    for x in xs: S.circ(*back(x, 0), K * m['pogo_pad_d'] / 2, 0.25, '#9C7A2E', fill='#E9D3A0')
    S.hdim(back(xs[0], 0)[0], back(xs[1], 0)[0], back(0, 0)[1], back(0, 0)[1] + 7, f'{m["pogo_pitch"]}', True)
    S.hdim(back(Hh, 0)[0], back(-Hh, 0)[0], back(0, -Hh)[1], back(0, -Hh)[1] + 10, f'{W:.1f}')
    S.text(back(0, 0)[0], back(0, -13.5 if not is_peb else -15)[1], 'LORE', 3.6 if not is_peb else 3.0, c=HID, font="Fraunces, 'DejaVu Serif', serif")
    S.text(back(0, 0)[0], back(0, -17.5)[1], 'LASER-ETCH ZONE', 1.6, c=HID, font=MONO)
    rd = m['recess_d'] / 2
    balloon(back(-rd * 0.707, rd * 0.707), back(-rd - 4, rd + 4), f'LORE Mount: Ø{m["recess_d"]} × {m["recess_depth"]} recess, 316L insert, {m["lugs"]} lugs × {m["lug_w"]}, {m["twist_deg"]}° twist', True)
    balloon(back(m['magnet_ring_od'] / 2 * 0.707, m['magnet_ring_od'] / 2 * 0.707), back(rd + 4, rd + 4), f'N52 ring magnet Ø{m["magnet_ring_od"]}/Ø{m["magnet_ring_id"]} × {m["magnet_thk"]} (hidden), axially magnetised')
    balloon(back(xs[0], m['pogo_pad_d'] / 2), back(xs[0] + 3, 6), f'{m["pogo_count"]}× pogo pad Ø{m["pogo_pad_d"]} @ {m["pogo_pitch"]}, Au 0.76 µm, flush −0.05: V+ · D · ID · GND', True)
    if is_peb:
        nrm = normals(plan); ia = min(range(len(plan)), key=lambda i: abs(math.atan2(plan[i][1], plan[i][0]) - 3 * math.pi / 4))
        x, y = plan[ia]; nx, ny = nrm[ia]; cx, cy = (x - nx * p['fillet_bottom']) * 0.84, (y - ny * p['fillet_bottom']) * 0.84
        tx, ty = -ny, nx; hp = p['tether_hole_pitch'] / 2
        for sgn in (-1, 1): S.circ(*back(cx + sgn * hp * tx, cy + sgn * hp * ty), K * p['tether_hole_d'] / 2, 0.25)
        balloon(back(cx + hp * tx, cy + hp * ty), back(cx - 3, Hh + 3), f'Tether tunnel: 2× Ø{p["tether_hole_d"]} @ {p["tether_hole_pitch"]} on the back, NW corner, 2 mm cord')
    else:
        S.poly(tf(back, offset(plan, -p['back_cover_inset'])), 0.25)
        ins = Hh - p['back_cover_inset']
        balloon(back(-ins * 0.6, -ins), back(-ins * 0.6 - 4, -Hh - 4), f'Back cover {W - 2 * p["back_cover_inset"]:.1f} A/F (inset {p["back_cover_inset"]}): ' + ('zirconia 0.9' if sku == 'atlas' else 'AG-etched glass 0.7'))
    vlabel(back(Hh, 0)[0], back(0, -Hh)[1] + 18, 'BACK', 'start')
    # ------------------------------------------------ key data (free area right of the top view)
    kx, ky = topv(Hh, 0)[0] + 12, 24
    mass = MB.get(sku, {}).get('total_g')
    rows = [('SKU', f'{p["name"]} · {p["code"]}'), ('ENVELOPE', f'{W:.1f} × {p["plan_h"]:.1f} × {T:.2f} max'), ('WALL', f'{p["wall"]} nominal'),
            ('IP', p['ip']), ('MASS', f'{mass:.1f} g (est.)' if mass else 'see mass-budget.md'),
            ('CHARGE', 'pogo 5 V/1 A' + ('' if is_peb else ' + USB-C PD')), ('FINISH', ' · '.join(f.upper() for f in p['finishes']))]
    S.text(kx, ky - 5, 'KEY DATA', 2.6, 'start', INK, font=MONO, weight=500)
    for i, (a_, b_) in enumerate(rows):
        S.text(kx, ky + i * 4.4, a_, 2.0, 'start', THIN, font=MONO); S.text(kx + 17, ky + i * 4.4, b_, 2.3, 'start')
    # ------------------------------------------------ callout table (top right, two columns)
    cx0 = back(Hh, 0)[0]; colw = (408 - 4 - cx0) / 2; per = 12
    S.text(cx0, ky - 5, 'CALLOUTS', 2.6, 'start', INK, font=MONO, weight=500)
    for i, (t, ctf) in enumerate(C):
        col, row = divmod(i, per); x0 = cx0 + col * colw; y0_ = ky + row * 4.3
        S.circ(x0 + 1.8, y0_ - 0.8, 1.8, 0.2, CTF if ctf else INK); S.text(x0 + 1.8, y0_, str(i + 1), 2.0, c=CTF if ctf else INK, weight=500)
        S.text(x0 + 4.6, y0_, t, 1.85, 'start', CTF if ctf else INK)
    # ------------------------------------------------ notes (bottom left)
    nx_, ny_ = 16, 264
    notes = ['NOTES', '1. Dimensions in mm. Scale 2:1 on A3, third-angle projection. Do not scale the print; the 3D model (models/*.glb) governs.',
             '2. General tolerances ISO 2768-mK unless stated. Orange = critical-to-function (CTF): 100 % check at EVT.',
             '3. Cosmetic class A: front and side faces. Class B: inside the Mount recess. No sink, flow or tool marks on class A.',
             f'4. CMF, sealing, drop and mass: id-spec.md. Internal layout: hardware/schematics/pcb-stackup.md. Generated by scripts/drawings.py from params.json rev {P["rev"]}.']
    for i, t in enumerate(notes): S.text(nx_, ny_ + i * 4.3, t, 2.6 if i == 0 else 2.15, 'start', INK if i == 0 else THIN, font=MONO if i == 0 else FONT, weight=500 if i == 0 else 400)
    # --- title block (bottom right)
    tx0, ty0, tw, th = 262, 239, 146, 45
    S.rect(tx0, ty0, tw, th, sw=0.4)
    for yy in (ty0 + 14, ty0 + 24.5, ty0 + 35): S.line(tx0, yy, tx0 + tw, yy, 0.2, INK)
    for xx in (tx0 + 50, tx0 + 98): S.line(xx, ty0 + 14, xx, ty0 + th, 0.2, INK)
    S.text(tx0 + 3, ty0 + 6.5, 'LORE Labs, Inc.', 4.2, 'start', font="Fraunces, 'DejaVu Serif', serif", weight=500)
    S.text(tx0 + 3, ty0 + 11.5, f'{p["name"]} ({p["code"]}) · general arrangement', 3.0, 'start')
    # third-angle symbol
    sx0, sy0 = tx0 + tw - 22, ty0 + 7
    S.add(f'<polygon points="{sx0},{sy0 - 3} {sx0 + 8},{sy0 - 1.5} {sx0 + 8},{sy0 + 1.5} {sx0},{sy0 + 3}" fill="none" stroke="{INK}" stroke-width="0.25"/>')
    S.circ(sx0 + 14, sy0, 3, 0.25); S.circ(sx0 + 14, sy0, 1.5, 0.25); S.line(sx0 - 1, sy0, sx0 + 18, sy0, 0.1, THIN, '1 0.6')
    cells = [('DRAWING No.', f'LORE-ID-{p["code"]}-GA-001'), ('REV', P['rev']), ('DATE', '2026-10-31'),
             ('SCALE', '2:1 (A3)'), ('UNITS', 'mm'), ('SHEET', '1 / 1'),
             ('MATERIAL', {'pebble': 'PC+10% GF, 2K soft-touch PU', 'square': '6013-T6 Al, Victus 2', 'atlas': 'Ti-6Al-4V, sapphire, ZrO2'}[sku]), ('DRAWN', 'LORE ID'), ('STATUS', 'EVT-0, for RFQ')]
    for i, (a_, b_) in enumerate(cells):
        col, row = i % 3, i // 3; x0 = tx0 + [0, 50, 98][col] + 2; y0_ = [ty0 + 14, ty0 + 24.5, ty0 + 35][row]
        S.text(x0, y0_ + 3, a_, 1.7, 'start', THIN, font=MONO); S.text(x0, y0_ + 7.6, b_, 2.5 if len(b_) < 24 else 2.1, 'start')
    svg = S.svg()
    open(os.path.join(OUT, f'{sku}.svg'), 'w').write(svg)
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, f'{sku}.png'), output_width=2480, output_height=1754)
    except ImportError:
        print('  (pip install cairosvg for PNG previews)')
    print(f'  drawings/{sku}.svg  T={T:.2f} mm')

for sku in ('pebble', 'square', 'atlas'): draw(sku)
