"""Packaging fit check: do hardware's cells and PCBs fit inside the ID housings (params.json)?
Inner cavity = outer plan outline offset by wall (+ fillet run-out near the back/front faces).
Run: python3 design/industrial/scripts/fit_check.py   (prints a markdown table; ESTIMATE, not CAD)"""
import json, math, os
P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'params.json')))

def inner_inset(z, zb, H, rb, rt, wall):
    """horizontal inset of the inner wall from the outer straight wall at height z (z from back face)"""
    zlo, zhi = zb + rb, zb + H - rt
    if z < zlo: r, dz = rb, zlo - z          # outer fillet radius; wall taken horizontally (slightly optimistic in the fillet)
    elif z > zhi: r, dz = rt, z - zhi
    else: return wall
    return wall + (r - math.sqrt(r * r - dz * dz)) if dz < r else 99

def se_inside(x, y, a, n):  # superellipse |x/a|^n + |y/a|^n <= 1
    return (abs(x) / a) ** n + (abs(y) / a) ** n

def sq_inside(x, y, half, r, n):  # rounded square with superelliptic corners
    cx = half - r; dx, dy = max(abs(x) - cx, 0), max(abs(y) - cx, 0)
    if abs(x) > half or abs(y) > half: return 9
    return (dx / r) ** n + (dy / r) ** n if r > 0 else 0

def rect_pts(L, W, rc, N=24):
    pts = []
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        cx, cy = sx * (L / 2 - rc), sy * (W / 2 - rc)
        for k in range(N + 1):
            a = math.atan2(sy, sx) - math.pi / 4 + k * (math.pi / 2) / N
            pts.append((cx + rc * math.cos(a), cy + rc * math.sin(a)))
    return pts

def check(sku, part, L, W, rc, z0, z1, clear=0.3):
    if sku == 'pebble':
        p = P['pebble']; zb, H, rb, rt, n, half = p['dome_bottom'], p['body_h'], p['fillet_bottom'], p['fillet_top'], p['superellipse_n'], p['plan_w'] / 2
        f = lambda x, y, a: se_inside(x, y, a, n)
    else:
        p = dict(P['square']); p.update(P['atlas'] if sku == 'atlas' else {}); H = p['thickness_total'] - p['back_bulge'] - p['glass_proud']
        zb, rb, rt, half, n, rcorner = p['back_bulge'], p['fillet_back'], p['fillet_front'], p['plan_w'] / 2, p['corner_n'], p['corner_r']
        f = lambda x, y, a: sq_inside(x, y, a, max(rcorner - (half - a), 0.5), n)
    worst = 0
    for z in (z0, (z0 + z1) / 2, z1):
        a = half - inner_inset(z, zb, H, rb, rt, p['wall']) - clear
        worst = max(worst, max(f(x, y, a) for x, y in rect_pts(L, W, rc)))
    return worst <= 1.0, worst

ROWS = [  # sku, part, L, W, corner r, z-range from back face (mm), source
    ('pebble', 'Cell LP553532 650 mAh 35×32×5.5', 35, 32, 1.0, 1.9, 7.4, 'hardware/bom/bom_pebble_lite.csv BT1'),
    ('pebble', 'PCB 36×36 R9 (0.8) + parts', 36, 36, 9.0, 7.6, 10.6, 'hardware/schematics/pcb-stackup.md §1'),
    ('pebble', 'ID proposal: cell 30×27×5.5 (~470 mAh E)', 30, 27, 1.0, 1.9, 7.4, 'this check'),
    ('pebble', 'ID proposal: PCB 35×35 R12', 35, 35, 12.0, 7.6, 10.6, 'this check'),
    ('square', 'Cell 1100 mAh 46×40×4.0', 46, 40, 1.5, 1.9, 6.2, 'pcb-stackup.md §3'),
    ('square', 'PCB 48×48 R10', 48, 48, 10.0, 6.4, 8.6, 'pcb-stackup.md §1'),
    ('atlas', 'Cell 1450 mAh 46×40×5.2', 46, 40, 1.5, 1.9, 7.4, 'bom_atlas.csv BT1'),
    ('atlas', 'PCB sandwich 46×46 (R10 assumed)', 46, 46, 10.0, 7.6, 11.0, 'pcb-stackup.md §1'),
]
if __name__ == '__main__':
    print('| SKU | Part | Fits (0.3 mm clearance)? | Worst-point index (≤ 1 fits) | Source |\n|---|---|---|---:|---|')
    for sku, part, L, W, rc, z0, z1, src in ROWS:
        ok, w = check(sku, part, L, W, rc, z0, z1)
        print(f'| {sku} | {part} | {"yes" if ok else "**NO**"} | {w:.2f} | {src} |')
