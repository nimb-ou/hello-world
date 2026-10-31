// LORE parametric industrial-design geometry (three.js).
// Units: millimetres. Device local frame: +X right, +Y up (plan, "north" = top edge), +Z out of the front face.
// Everything is driven by industrial/params.json so the 3D, drawings and mass budget stay in sync.
import * as THREE from 'three';
import { FINISHES, M } from './materials.js';

// ------------------------------------------------------------------ outlines
// An outline is { p: [[x,y]...], n: [[nx,ny]...] } closed, CCW, uniformly resampled, centred on origin.
function resample(poly, N) {
  const L = [0];
  for (let i = 1; i <= poly.length; i++) {
    const a = poly[i - 1], b = poly[i % poly.length];
    L.push(L[i - 1] + Math.hypot(b[0] - a[0], b[1] - a[1]));
  }
  const total = L[L.length - 1], out = [];
  let j = 0;
  for (let k = 0; k < N; k++) {
    const t = (k / N) * total;
    while (L[j + 1] < t) j++;
    const a = poly[j], b = poly[(j + 1) % poly.length], f = (t - L[j]) / (L[j + 1] - L[j] || 1);
    out.push([a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]);
  }
  return out;
}
function withNormals(p) {
  const N = p.length, n = [];
  for (let i = 0; i < N; i++) {
    const a = p[(i - 1 + N) % N], b = p[(i + 1) % N];
    const tx = b[0] - a[0], ty = b[1] - a[1], l = Math.hypot(tx, ty) || 1;
    n.push([ty / l, -tx / l]);
  }
  return { p, n };
}
const sgnpow = (v, e) => Math.sign(v) * Math.pow(Math.abs(v), e);

export function superellipse(w, h, n, N = 384) {
  const raw = [];
  for (let i = 0; i < 2048; i++) {
    const t = (i / 2048) * Math.PI * 2;
    raw.push([sgnpow(Math.cos(t), 2 / n) * w / 2, sgnpow(Math.sin(t), 2 / n) * h / 2]);
  }
  return withNormals(resample(raw, N));
}
// Rounded rectangle with superelliptic (continuous-curvature) corners; n=2 -> circular arcs.
export function squircleRect(w, h, r, n = 2, N = 384) {
  const raw = [], cx = w / 2 - r, cy = h / 2 - r, Q = 128;
  const corners = [[cx, cy, 0], [-cx, cy, 1], [-cx, -cy, 2], [cx, -cy, 3]];
  for (const [x0, y0, q] of corners) {
    for (let i = 0; i <= Q; i++) {
      const t = (q + i / Q) * Math.PI / 2;
      raw.push([x0 + r * sgnpow(Math.cos(t), 2 / n), y0 + r * sgnpow(Math.sin(t), 2 / n)]);
    }
  }
  return withNormals(resample(raw, N));
}
export function circle(r, N = 192) {
  const p = [];
  for (let i = 0; i < N; i++) { const t = (i / N) * Math.PI * 2; p.push([Math.cos(t) * r, Math.sin(t) * r]); }
  return withNormals(p);
}
export function offsetOutline(ol, o, s = 1) {
  return withNormals(ol.p.map((q, i) => [(q[0] + ol.n[i][0] * o) * s, (q[1] + ol.n[i][1] * o) * s]));
}
export function outlineWidth(ol) { let m = 0; for (const q of ol.p) m = Math.max(m, q[0]); return m * 2; }

// ------------------------------------------------------------------ sweep
// profile: [{o, z, s}] — o = outward offset of outline (mm), s = scale toward centroid, z = height.
// Consecutive profile rings are bridged by quads. Bottom-centre -> side -> top-centre gives outward normals.
export function sweep(ol, profile, { uv = 60, flip = false } = {}) {
  const N = ol.p.length, R = profile.length;
  const pos = new Float32Array(N * R * 3), uvs = new Float32Array(N * R * 2);
  for (let k = 0; k < R; k++) {
    const { o = 0, z = 0, s = 1 } = profile[k];
    const ss = Math.max(s, 1e-4);
    for (let i = 0; i < N; i++) {
      const x = (ol.p[i][0] + ol.n[i][0] * o) * ss, y = (ol.p[i][1] + ol.n[i][1] * o) * ss;
      const idx = (k * N + i);
      pos[idx * 3] = x; pos[idx * 3 + 1] = y; pos[idx * 3 + 2] = z;
      uvs[idx * 2] = x / uv + 0.5; uvs[idx * 2 + 1] = y / uv + 0.5;
    }
  }
  const index = [];
  for (let k = 0; k < R - 1; k++) for (let i = 0; i < N; i++) {
    const a = k * N + i, b = k * N + (i + 1) % N, c = (k + 1) * N + (i + 1) % N, d = (k + 1) * N + i;
    if (flip) index.push(a, c, b, a, d, c); else index.push(a, b, c, a, c, d);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
  g.setIndex(index);
  g.computeVertexNormals();
  return g;
}

// Standard slab profile with independent top/bottom fillets and dome functions (s in 0..1).
export function slabProfile({ H, rt, rb, top = () => 0, bot = () => 0, cap = 28, fil = 14, part = 'all', sTopEnd = 0 }) {
  const out = [];
  const bottom = [], side = [], topc = [];
  for (let k = 0; k <= cap; k++) { const s = k / cap; bottom.push({ o: -rb, s, z: -bot(s) }); }
  for (let k = 1; k <= fil; k++) { const f = (k / fil) * Math.PI / 2; side.push({ o: -rb + rb * Math.sin(f), z: rb - rb * Math.cos(f) }); }
  for (let k = 1; k <= fil; k++) { const f = Math.PI / 2 + (k / fil) * Math.PI / 2; side.push({ o: -rt + rt * Math.sin(f), z: H - rt - rt * Math.cos(f) }); }
  for (let k = 1; k <= cap; k++) { const s = 1 - (k / cap) * (1 - sTopEnd); topc.push({ o: -rt, s, z: H + top(s) }); }
  if (part === 'bottom') return bottom;
  if (part === 'sideTop') return [bottom[bottom.length - 1], ...side, ...topc];
  return [...bottom, ...side, ...topc];
}
const dome = (h) => (s) => h * (1 - s * s);

// Find a point on the outline in a given direction (angle, radians) -> index
function idxAt(ol, ang) {
  let best = 0, bd = 1e9;
  for (let i = 0; i < ol.p.length; i++) {
    const a = Math.atan2(ol.p[i][1], ol.p[i][0]); let d = Math.abs(a - ang); d = Math.min(d, Math.PI * 2 - d);
    if (d < bd) { bd = d; best = i; }
  }
  return best;
}
function idxNearX(ol, x, ySign) {
  let best = 0, bd = 1e9;
  for (let i = 0; i < ol.p.length; i++) {
    if (Math.sign(ol.p[i][1]) !== ySign) continue;
    const d = Math.abs(ol.p[i][0] - x); if (d < bd) { bd = d; best = i; }
  }
  return best;
}
function idxNearY(ol, y, xSign) {
  let best = 0, bd = 1e9;
  for (let i = 0; i < ol.p.length; i++) {
    if (Math.sign(ol.p[i][0]) !== xSign) continue;
    const d = Math.abs(ol.p[i][1] - y); if (d < bd) { bd = d; best = i; }
  }
  return best;
}
// Place a flat feature (disc / slot) on a vertical side wall at outline index i, height z.
function onSide(ol, i, z, mesh, out = 0.02) {
  const [x, y] = ol.p[i], [nx, ny] = ol.n[i];
  mesh.position.set(x + nx * out, y + ny * out, z);
  mesh.up.set(0, 0, 1);
  mesh.lookAt(x + nx * 10, y + ny * 10, z);
  return mesh;
}
function hole(d, mat) { return new THREE.Mesh(new THREE.CircleGeometry(d / 2, 24), mat); }
function slot(w, h, mat, r = null) {
  const sh = roundedRectShape(w, h, r ?? h / 2);
  return new THREE.Mesh(new THREE.ShapeGeometry(sh, 12), mat);
}
export function roundedRectShape(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2; r = Math.min(r, w / 2, h / 2);
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  return s;
}
function normalizeUV(g) {
  g.computeBoundingBox(); const b = g.boundingBox, uv = g.attributes.uv, p = g.attributes.position;
  for (let i = 0; i < uv.count; i++) uv.setXY(i, (p.getX(i) - b.min.x) / (b.max.x - b.min.x), (p.getY(i) - b.min.y) / (b.max.y - b.min.y));
  uv.needsUpdate = true; return g;
}

// ------------------------------------------------------------------ back-plate texture (mount, pogo, laser etch)
function backTexture({ size, base, text, lines, mountR, rough = 0.5, mountSteel = '#B8B8B5', mirror = true }) {
  const S = 1024, px = S / size;
  const mk = () => { const c = document.createElement('canvas'); c.width = c.height = S; return c; };
  const col = mk(), rgh = mk(), met = mk();
  const gc = col.getContext('2d'), gr = rgh.getContext('2d'), gm = met.getContext('2d');
  const R = Math.round(rough * 255);
  gc.fillStyle = base; gc.fillRect(0, 0, S, S);
  gr.fillStyle = `rgb(${R},${R},${R})`; gr.fillRect(0, 0, S, S);
  gm.fillStyle = '#000'; gm.fillRect(0, 0, S, S);
  for (const g of [gc, gr, gm]) { g.save(); g.translate(S / 2, S / 2); if (mirror) g.scale(-1, 1); g.scale(1, -1); }
  // canvas y down; uv v up -> flip y so text reads correctly when viewing the back.
  const circleFill = (g, r, fill) => { g.beginPath(); g.arc(0, 0, r * px, 0, Math.PI * 2); g.fillStyle = fill; g.fill(); };
  // mount ring: dark gap, steel insert, magnet-ring shadow, bayonet lugs
  circleFill(gc, mountR + 0.35, 'rgba(10,10,10,0.9)'); circleFill(gr, mountR + 0.35, 'rgb(200,200,200)');
  circleFill(gc, mountR, mountSteel); circleFill(gm, mountR, '#fff'); circleFill(gr, mountR, 'rgb(95,95,95)');
  gc.strokeStyle = 'rgba(0,0,0,0.25)'; gc.lineWidth = 0.25 * px;
  gc.beginPath(); gc.arc(0, 0, (mountR - 1.6) * px, 0, Math.PI * 2); gc.stroke();
  for (let k = 0; k < 3; k++) {
    gc.save(); gc.rotate(k * Math.PI * 2 / 3 + Math.PI / 2);
    gc.fillStyle = 'rgba(0,0,0,0.55)'; gc.fillRect(-2 * px, (mountR - 1.3) * px, 4 * px, 1.0 * px); gc.restore();
  }
  // pogo pads (gold) + alignment dot
  for (const dx of [-2.5, 2.5]) {
    for (const [g, f] of [[gc, '#E3B866'], [gm, '#fff'], [gr, 'rgb(60,60,60)']]) { g.beginPath(); g.arc(dx * px, 0, 1.0 * px, 0, Math.PI * 2); g.fillStyle = f; g.fill(); }
    gc.beginPath(); gc.arc(dx * px, 0, 1.25 * px, 0, Math.PI * 2); gc.strokeStyle = 'rgba(0,0,0,0.6)'; gc.lineWidth = 0.3 * px; gc.stroke();
  }
  gc.beginPath(); gc.arc(0, (mountR - 3.2) * px, 0.45 * px, 0, Math.PI * 2); gc.fillStyle = 'rgba(0,0,0,0.5)'; gc.fill();
  // laser etch text (y positive = toward top edge)
  gc.fillStyle = text; gc.textAlign = 'center'; gc.textBaseline = 'middle';
  for (const L of lines) {
    gc.save(); gc.scale(1, -1);
    gc.font = `${L.weight || 500} ${L.size * px}px ${L.font || 'Inter'}`;
    if (L.track) gc.letterSpacing = `${L.track * px}px`;
    gc.fillText(L.t, 0, -L.y * px); gc.restore();
  }
  for (const g of [gc, gr, gm]) g.restore();
  const t = (c, srgb) => { const tx = new THREE.CanvasTexture(c); if (srgb) tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8; return tx; };
  return { map: t(col, true), roughnessMap: t(rgh), metalnessMap: t(met) };
}

function mat(f) { return typeof f === 'function' ? f() : f; }
function named(mesh, name, role) { mesh.name = name; mesh.userData.role = role; mesh.castShadow = true; mesh.receiveShadow = true; return mesh; }

// ------------------------------------------------------------------ LORE Pebble
export function buildPebble(PR, finishKey = 'bone', opts = {}) {
  const P = PR.pebble, F = FINISHES[finishKey];
  const g = new THREE.Group(); g.name = `LORE Pebble ${F.label}`;
  const ol = superellipse(P.plan_w, P.plan_h, P.superellipse_n);
  const H = P.body_h, rt = P.fillet_top, rb = P.fillet_bottom;
  const zb = P.dome_bottom; // body origin raised so back dome bottom sits at z=0
  const sd = P.dish_s, sIn = P.led_ring_s_in, sOut = P.led_ring_s_out;
  const topFn = (s) => (s >= sd ? P.dome_top * (1 - s * s) : P.dome_top * (1 - sd * sd) - P.dish_depth * (1 - (s / sd) ** 2));
  const botFn = dome(P.dome_bottom);
  const body = mat(F.body), dish = mat(F.dish);
  // side + top shell (to LED ring)
  const prof = slabProfile({ H, rt, rb, top: topFn, bot: botFn, part: 'sideTop', sTopEnd: sOut, cap: 20 });
  const shell = named(new THREE.Mesh(sweep(ol, prof), body), 'housing_top_shell', 'housing');
  // back (textured with mount + etch)
  const capR = (P.plan_w - 2 * rb) / 2;
  const bt = backTexture({ size: 60, base: F.back, text: F.backText, mountR: PR.mount.recess_d / 2, rough: 0.62,
    lines: [{ t: 'LORE', y: -15.0, size: 2.6, font: 'Fraunces', weight: 500, track: 0.5 },
      { t: 'Pebble · P1 · Designed by LORE Labs', y: -18.0, size: 0.95 }] });
  const backMat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, ...bt, metalness: 1, roughness: 1, sheen: 0.2, sheenRoughness: 0.8 });
  const back = named(new THREE.Mesh(sweep(ol, slabProfile({ H, rt, rb, bot: botFn, part: 'bottom', cap: 36 })), backMat), 'housing_back', 'housing');
  // LED light-guide ring (PMMA, follows the plan outline) and the floating Talk dish
  const ringProf = [{ o: -rt, s: sOut, z: H + topFn(sOut) + 0.03 }, { o: -rt, s: (sIn + sOut) / 2, z: H + topFn((sIn + sOut) / 2) + 0.06 }, { o: -rt, s: sIn, z: H + topFn(sIn) + 0.03 }];
  const ledMat = opts.led ? M.ledOn(opts.led.color, opts.led.intensity) : M.ledOff();
  const ring = named(new THREE.Mesh(sweep(ol, ringProf), ledMat), 'led_ring_lightguide', 'led');
  const dishProf = [{ o: -rt, s: sIn, z: H + topFn(sIn) - 0.05 }];
  for (let k = 1; k <= 24; k++) { const s = sIn * (1 - k / 24); dishProf.push({ o: -rt, s, z: H + topFn(s) }); }
  const dsh = named(new THREE.Mesh(sweep(ol, dishProf), dish), 'talk_button_cap', 'button');
  const parts = new THREE.Group(); parts.add(shell, back, ring, dsh); parts.position.z = zb; g.add(parts);
  // ports
  const hm = M.hole();
  const zMid = zb + rb + (H - rt - rb) / 2;
  for (const sx of [-1, 1]) parts.add(named(onSide(ol, idxNearX(ol, sx * P.mic_spacing / 2, 1), zMid - zb + 0.8, hole(P.mic_port_d, hm)), 'mic_port', 'port'));
  for (let k = 0; k < P.speaker_holes; k++) {
    const x = (k - (P.speaker_holes - 1) / 2) * P.speaker_hole_pitch;
    parts.add(named(onSide(ol, idxNearX(ol, x, -1), zMid - zb, hole(P.speaker_hole_d, hm)), 'speaker_hole', 'port'));
  }
  // tether tunnel: two holes on the back at the NW corner
  const ia = idxAt(ol, (3 * Math.PI) / 4);
  for (const t of [-0.5, 0.5]) {
    const i2 = (ia + Math.round(t * 14) + ol.p.length) % ol.p.length;
    const s = 0.84, [x, y] = ol.p[i2], [nx, ny] = ol.n[i2];
    const h = hole(P.tether_hole_d, hm); h.position.set((x - nx * rb) * s, (y - ny * rb) * s, -botFn(s) - 0.02); h.rotation.x = Math.PI;
    parts.add(named(h, 'tether_hole', 'port'));
  }
  g.userData = { sku: 'pebble', finish: finishKey, thickness: P.thickness_total, outline: ol };
  return g;
}

// ------------------------------------------------------------------ LORE Square / Atlas
export function squareParams(PR, sku) {
  const S = { ...PR.square };
  if (sku === 'atlas') Object.assign(S, PR.atlas);
  S.frame_h = S.thickness_total - S.back_bulge - S.glass_proud;
  return S;
}

export function buildSlate(PR, sku = 'square', finishKey = 'sq-ink', opts = {}) {
  const S = squareParams(PR, sku), F = FINISHES[finishKey];
  const g = new THREE.Group(); g.name = `${S.name} ${F.label}`;
  const ol = squircleRect(S.plan_w, S.plan_h, S.corner_r, S.corner_n);
  const H = S.frame_h, rt = S.fillet_front, rb = S.fillet_back, zb = S.back_bulge;
  const parts = new THREE.Group(); parts.position.z = zb; g.add(parts);
  const frameMat = mat(F.frame), chamferMat = mat(F.chamfer);
  // frame: back land ring -> side -> front land, open at the chamfer
  const cs = S.chamfer_s, inset = S.back_cover_inset;
  const sBackLand = (outlineWidth(ol) - 2 * inset) / (outlineWidth(ol) - 2 * rb);
  const frameProf = [];
  frameProf.push({ o: -rb, s: sBackLand - 0.002, z: 0.25 });
  frameProf.push({ o: -rb, s: sBackLand, z: 0 });
  for (const q of slabProfile({ H, rt, rb, part: 'sideTop', cap: 4, sTopEnd: cs[0] })) frameProf.push(q);
  const frame = named(new THREE.Mesh(sweep(ol, frameProf), frameMat), 'frame_unibody', 'housing');
  const chamfer = named(new THREE.Mesh(sweep(ol, [{ o: -rt, s: cs[0], z: H }, { o: -rt, s: cs[1], z: H - 0.35 }, { o: -rt, s: cs[1] - 0.002, z: H - 0.6 }]), chamferMat), 'diamond_cut_chamfer', 'housing');
  parts.add(frame, chamfer);
  // antenna split lines (nano-moulded PBT) on top & bottom edges
  const splitMat = new THREE.MeshStandardMaterial({ color: F.split, roughness: 0.5 });
  for (const sy of [1, -1]) for (const sx of [-1, 1]) {
    const i = idxNearX(ol, sx * 12, sy);
    const b = new THREE.Mesh(new THREE.PlaneGeometry(S.antenna_split_w, H - rb - rt + 1.2), splitMat);
    parts.add(named(onSide(ol, i, rb + (H - rb - rt) / 2, b, 0.015), 'antenna_split', 'housing'));
  }
  // cover glass (Victus 2 / sapphire), 2.5D edge
  const gol = offsetOutline(ol, -rt, S.glass_s);
  const gt = S.glass_t;
  const glassMat = sku === 'atlas' ? M.sapphire() : M.glass();
  const glass = named(new THREE.Mesh(sweep(gol, slabProfile({ H: gt, rt: 0.35, rb: 0.1, cap: 6, fil: 6 })), glassMat), sku === 'atlas' ? 'cover_sapphire' : 'cover_glass', 'glass');
  glass.position.z = H + S.glass_proud - gt; parts.add(glass);
  // display active area (466x466 AMOLED) as an emissive plane on the glass
  const a = S.display_active;
  const dg = normalizeUV(new THREE.ShapeGeometry(roundedRectShape(a, a, S.display_r), 24));
  const screenMat = new THREE.MeshPhysicalMaterial({ color: 0x000000, roughness: 0.04, ior: sku === 'atlas' ? 1.77 : 1.52, specularIntensity: sku === 'atlas' ? 0.45 : 0.55, envMapIntensity: 0.6,
    emissive: 0xffffff, emissiveIntensity: opts.screenOn === false ? 0 : (opts.screenIntensity ?? 1.0), emissiveMap: opts.screenTexture || null });
  if (!opts.screenTexture) screenMat.emissive.set(0x000000);
  const screen = named(new THREE.Mesh(dg, screenMat), 'display_466', 'screen');
  screen.position.set(0, S.display_offset_y, H + S.glass_proud + 0.004); screen.castShadow = false; parts.add(screen);
  // back cover (etched glass / zirconia) with mount + etch
  const bol = offsetOutline(ol, -inset);
  const bw = outlineWidth(bol);
  const bt = backTexture({ size: bw, base: F.back, text: F.backText, mountR: PR.mount.recess_d / 2, rough: F.backRough,
    lines: [{ t: 'LORE', y: -13.2, size: 3.0, font: 'Fraunces', weight: 500, track: 0.6 },
      { t: `${S.name.replace('LORE ', '')} · ${S.code}`, y: -16.6, size: 1.1, weight: 500, track: 0.2 },
      { t: 'Designed by LORE Labs · Model A26' + (sku === 'atlas' ? '20' : '10') + ' · IMEI on device', y: -18.8, size: 0.75 },
      { t: sku === 'atlas' ? 'Grade 5 titanium · sapphire crystal' : '6013 aluminium · Gorilla Glass Victus 2', y: 14.0, size: 0.8 }] });
  const backMat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, ...bt, metalness: 1, roughness: 1, clearcoat: F.backClear || 0.15, clearcoatRoughness: 0.3 });
  const backProf = [];
  for (let k = 0; k <= 30; k++) { const s = k / 30; backProf.push({ o: 0, s, z: -(zb - 0.12) * (1 - s * s) - 0.12 }); }
  backProf.push({ o: 0, s: 1, z: 0.05 });
  const back = named(new THREE.Mesh(sweep(bol, backProf, { uv: bw }), backMat), sku === 'atlas' ? 'back_zirconia' : 'back_glass', 'housing');
  parts.add(back);
  // crown (knurled, rotary + press) on the right side
  const crownMat = mat(F.crown);
  const crown = new THREE.Group(); crown.name = 'crown';
  const cg = new THREE.CylinderGeometry(S.crown_d / 2, S.crown_d / 2, S.crown_protrusion, 160, 1);
  const cp = cg.attributes.position;
  for (let i = 0; i < cp.count; i++) {
    const x = cp.getX(i), z = cp.getZ(i), r = Math.hypot(x, z); if (r < S.crown_d / 2 - 0.01) continue;
    const t = Math.atan2(z, x), k = 1 - 0.035 * (0.5 + 0.5 * Math.sign(Math.cos(t * S.crown_knurl)));
    cp.setX(i, x * k); cp.setZ(i, z * k);
  }
  cg.computeVertexNormals();
  const cm = named(new THREE.Mesh(cg, crownMat), 'crown_knurl', 'crown');
  const cap = named(new THREE.Mesh(new THREE.CylinderGeometry(S.crown_d / 2 - 0.35, S.crown_d / 2 - 0.25, 0.25, 96), sku === 'atlas' ? M.brass() : mat(F.chamfer)), 'crown_endcap', 'crown');
  cap.position.y = S.crown_protrusion / 2 + 0.12;
  crown.add(cm, cap); crown.rotation.z = -Math.PI / 2;
  const ci = idxNearY(ol, S.crown_y, 1);
  crown.position.set(ol.p[ci][0] + S.crown_protrusion / 2 - 0.15, S.crown_y, rb + (H - rb - rt) / 2);
  parts.add(crown);
  // Talk key (pill) below the crown
  const kol = squircleRect(S.talk_h, S.talk_w, S.talk_h / 2 - 0.01, 2, 128);
  const kg = sweep(kol, slabProfile({ H: S.talk_protrusion + 0.3, rt: 0.45, rb: 0.01, cap: 8, fil: 8 }));
  const key = named(new THREE.Mesh(kg, mat(F.key)), 'talk_key', 'button');
  key.rotation.y = Math.PI / 2;
  const ki = idxNearY(ol, S.talk_y, 1);
  key.position.set(ol.p[ki][0] - 0.3, S.talk_y, rb + (H - rb - rt) / 2);
  parts.add(key);
  // ports: USB-C + speaker + mics on the bottom edge, 2 mics on the top edge
  const hm = M.hole(), zMid = rb + (H - rb - rt) / 2;
  const usb = slot(S.usb_c_opening[0], S.usb_c_opening[1], hm);
  parts.add(named(onSide(ol, idxNearX(ol, 0, -1), zMid, usb), 'usb_c', 'port'));
  const tongue = slot(6.6, 0.7, M.usbTongue(), 0.2);
  parts.add(named(onSide(ol, idxNearX(ol, 0, -1), zMid, tongue, 0.03), 'usb_c_tongue', 'port'));
  for (let k = 0; k < S.speaker_slots; k++) {
    const x = 8.5 + k * 1.7;
    const sl = slot(S.speaker_slot[1], S.speaker_slot[0], hm); parts.add(named(onSide(ol, idxNearX(ol, x, -1), zMid, sl), 'speaker_slot', 'port'));
  }
  parts.add(named(onSide(ol, idxNearX(ol, -10, -1), zMid, hole(S.mic_port_d, hm)), 'mic_port', 'port'));
  for (const sx of [-1, 1]) parts.add(named(onSide(ol, idxNearX(ol, sx * 6, 1), zMid, hole(S.mic_port_d, hm)), 'mic_port', 'port'));
  // tether hole at NW corner (top-left), through the frame corner
  const ia = idxAt(ol, (3 * Math.PI) / 4);
  parts.add(named(onSide(ol, ia, zMid, hole(1.8, hm)), 'tether_hole', 'port'));
  // Atlas: Glance camera + privacy LED in the top glass band
  if (sku === 'atlas') {
    screenMat.iridescence = 0.25; screenMat.iridescenceIOR = 1.3; screenMat.iridescenceThicknessRange = [180, 320];
    const zt = H + S.glass_proud + 0.006;
    const ringG = new THREE.RingGeometry(S.camera_lens_d / 2 + 0.25, S.camera_window_d / 2, 96);
    const ring = named(new THREE.Mesh(ringG, M.steelPolish()), 'camera_trim', 'camera');
    ring.material.color.set(finishKey === 'at-dlc' ? 0x3a3a3e : 0xBDB7AC);
    ring.position.set(0, S.camera_y, zt);
    const lens = named(new THREE.Mesh(new THREE.CircleGeometry(S.camera_lens_d / 2 + 0.25, 64), M.lens()), 'camera_lens', 'camera');
    lens.position.set(0, S.camera_y, zt + 0.002);
    const pupil = new THREE.Mesh(new THREE.CircleGeometry(0.55, 32), new THREE.MeshPhysicalMaterial({ color: 0x000000, roughness: 0.02, clearcoat: 1 }));
    pupil.position.set(0, S.camera_y, zt + 0.004);
    const led = new THREE.Mesh(new THREE.CircleGeometry(0.35, 24), opts.cameraActive ? M.ledOn(0xffffff, 3) : new THREE.MeshPhysicalMaterial({ color: 0x15161a, roughness: 0.1 }));
    led.position.set(S.privacy_led_dx, S.camera_y, zt + 0.002);
    parts.add(ring, lens, pupil, named(led, 'privacy_led', 'camera'));
  }
  // ambient light sensor dot (both) — invisible through ink, a faint dot at top band
  const als = new THREE.Mesh(new THREE.CircleGeometry(0.5, 24), new THREE.MeshPhysicalMaterial({ color: 0x0b0c0e, roughness: 0.05, clearcoat: 1 }));
  als.position.set(sku === 'atlas' ? -4.2 : 0, sku === 'atlas' ? S.camera_y : 19.0, H + S.glass_proud + 0.003); parts.add(als);
  g.userData = { sku, finish: finishKey, thickness: S.thickness_total, outline: ol };
  return g;
}

export function buildDevice(PR, sku, finish, opts = {}) {
  if (sku === 'pebble') return buildPebble(PR, finish, opts);
  return buildSlate(PR, sku, finish, opts);
}

// ------------------------------------------------------------------ exploded internals (Square / Atlas)
function label(obj, text, sub) { obj.userData.label = text; obj.userData.sub = sub; return obj; }
function box(w, h, t, r, m, name) {
  const ol = squircleRect(w, h, r, 2, 128);
  return named(new THREE.Mesh(sweep(ol, slabProfile({ H: t, rt: Math.min(0.3, t / 3), rb: Math.min(0.3, t / 3), cap: 2, fil: 3 })), m), name, 'internal');
}
export function buildSlateExploded(PR, sku, finish, opts = {}) {
  const dev = buildSlate(PR, sku, finish, opts);
  const S = squareParams(PR, sku);
  const parts = dev.children[0];
  const find = (n) => parts.children.filter((c) => c.name === n);
  const gap = opts.gap ?? 9;
  const g = new THREE.Group(); g.name = 'exploded';
  const layer = (objs, z, lab, sub) => { const grp = new THREE.Group(); for (const o of objs) { parts.remove(o); grp.add(o); } grp.position.z = z; label(grp, lab, sub); g.add(grp); return grp; };
  // order back -> front
  layer(find(sku === 'atlas' ? 'back_zirconia' : 'back_glass'), -gap * 3.2, sku === 'atlas' ? 'Back · zirconia ceramic, laser-etched' : 'Back · AG-etched glass, colour-matched', 'LORE Mount: 316L insert, N52 magnet ring, 2× Au pogo');
  // battery + coil-free charge path
  const bat = box(38, 30, 4.6, 3, M.pouch(), 'battery');
  bat.position.set(0, -4, 0);
  layer([bat], -gap * 2.1, sku === 'atlas' ? 'Battery · 3.87 V 1000 mAh Li-ion polymer (est.)' : 'Battery · 3.87 V 850 mAh Li-ion polymer (est.)', 'stacked-cell, swelling allowance 8 %');
  // main PCB with shields + LRA + speaker
  const pcb = new THREE.Group();
  const board = box(44, 40, 0.8, 6, M.pcb(), 'main_pcb'); pcb.add(board);
  const can1 = box(14, 12, 1.4, 0.6, M.shield(), 'shield_soc'); can1.position.set(-8, 6, 0.8);
  const can2 = box(12, 9, 1.2, 0.6, M.shield(), 'shield_modem'); can2.position.set(9, 7, 0.8);
  const can3 = box(10, 7, 1.0, 0.6, M.shield(), 'shield_gnss_pmic'); can3.position.set(8, -6, 0.8);
  const spk = box(15, 11, 3.0, 1.2, M.plasticBlack(), 'speaker_1511'); spk.position.set(-10, -11, 0.8);
  const lra = named(new THREE.Mesh(new THREE.CylinderGeometry(4, 4, 2.6, 48), M.steelPolish()), 'haptic_lra', 'internal'); lra.rotation.x = Math.PI / 2; lra.position.set(12, -14, 2.1);
  pcb.add(can1, can2, can3, spk, lra);
  if (sku === 'atlas') { const cam = box(6.5, 6.5, 4.2, 0.8, M.plasticBlack(), 'camera_module'); cam.position.set(0, 18.5, 0.8); pcb.add(cam); }
  layer([pcb], -gap * 0.9, 'Main logic board · 10-layer HDI, SiP + LTE Cat-4 modem', sku === 'atlas' ? 'Glance camera module · 1511 speaker · Ø8 LRA' : '1511 speaker box (ePTFE vent) · Ø8 LRA haptic');
  // frame with buttons
  const fr = layer([...find('frame_unibody'), ...find('diamond_cut_chamfer'), ...find('antenna_split'), ...parts.children.filter((c) => c.userData.role === 'port')], gap * 0.2,
    sku === 'atlas' ? 'Unibody · Grade 5 titanium, CNC 5-axis' : 'Unibody · 6013-T6 aluminium, CNC 5-axis', '4 nano-moulded antenna splits · USB-C (IPx7 receptacle)');
  const crown = find('crown')[0], key = find('talk_key')[0];
  parts.remove(crown); parts.remove(key); fr.add(crown, key);
  crown.position.x += gap * 1.0; key.position.x += gap * 1.0;
  // midframe + display + glass
  const mid = box(46, 46, 0.9, 8, M.plasticDark(), 'midframe_pc_gf'); mid.position.z = 0;
  layer([mid], gap * 2.0, 'Midframe · PC-GF30 + Mg stiffener', 'display seal: 0.25 mm PSA gasket');
  const disp = new THREE.Group();
  const panel = box(31.5, 31.5, 0.9, 6, M.plasticBlack(), 'display_module'); disp.add(panel);
  const flex = box(10, 9, 0.12, 1, M.flex(), 'display_flex'); flex.position.set(0, -20, 0.2); disp.add(flex);
  layer([disp], gap * 2.75, '1.6" AMOLED · 466 × 466 · 412 ppi · LTPO 1–60 Hz', 'peak 1,500 nits (outdoor), AOD');
  const glassObjs = parts.children.filter((c) => ['cover_glass', 'cover_sapphire', 'display_466', 'camera_trim', 'camera_lens', 'privacy_led'].includes(c.name) || (c.geometry && c.geometry.type === 'CircleGeometry' && c.position.z > S.frame_h));
  const gl = layer(glassObjs, gap * 3.55, sku === 'atlas' ? 'Cover · sapphire 0.8 mm, AR + oleophobic' : 'Cover · Gorilla Glass Victus 2, 0.7 mm 2.5D', 'black ink mask, ALS window');
  for (const o of glassObjs) o.position.z -= S.frame_h; // keep glass close to its layer origin
  g.add(parts);
  g.userData = { ...dev.userData, exploded: true };
  // wrap with back-bulge offset
  const outer = new THREE.Group(); outer.add(g); outer.userData = g.userData; outer.name = dev.name + ' (exploded)';
  return outer;
}

export function buildPebbleExploded(PR, finish, opts = {}) {
  const dev = buildPebble(PR, finish, opts);
  const parts = dev.children[0]; const gap = opts.gap ?? 8;
  const g = new THREE.Group();
  const take = (pred) => parts.children.filter(pred);
  const layer = (objs, z, lab, sub) => { const grp = new THREE.Group(); for (const o of objs) { parts.remove(o); grp.add(o); } grp.position.z = z; label(grp, lab, sub); g.add(grp); return grp; };
  layer(take((c) => c.name === 'housing_back' || c.name === 'tether_hole'), -gap * 3.0, 'Back housing · PC-GF10, 2K soft-touch PU', 'LORE Mount insert (316L) · N52 ring magnet · 2× Au pogo');
  const bat = box(30, 26, 5.2, 4, M.pouch(), 'battery'); layer([bat], -gap * 1.8, 'Battery · 3.85 V 600 mAh Li-ion polymer (est.)', '');
  const pcb = new THREE.Group(); const board = box(32, 30, 0.8, 8, M.pcb(), 'main_pcb'); pcb.add(board);
  const can = box(12, 11, 1.3, 0.6, M.shield(), 'shield_soc'); can.position.set(-4, 3, 0.8); pcb.add(can);
  const spk = box(15, 11, 3, 1.2, M.plasticBlack(), 'speaker'); spk.position.set(5, -8, 0.8); pcb.add(spk);
  const ant = box(10, 10, 1.6, 0.4, M.ceramicWhite(), 'gnss_patch'); ant.position.set(8, 8, 0.8); pcb.add(ant);
  layer([pcb], -gap * 0.6, 'Logic board · nRF54H20-class BLE SoC + NPU co-processor', 'L1+L5 GNSS · 9-axis IMU · 1511 speaker');
  layer(take((c) => c.name === 'housing_top_shell' || c.userData.role === 'port'), gap * 0.7, 'Top housing · PC-GF10, 2K soft-touch PU', 'ePTFE mic + speaker membranes (IP67)');
  layer(take((c) => c.name === 'led_ring_lightguide'), gap * 3.2, 'Light guide · frosted PMMA, 12× RGB LED', 'Talk-button travel 0.35 mm, metal dome 2.4 N');
  layer(take((c) => c.name === 'talk_button_cap'), gap * 4.3, 'Talk cap · floating, full-face press', '');
  g.add(parts);
  const outer = new THREE.Group(); outer.add(g); outer.position.z = 0; outer.userData = { ...dev.userData, exploded: true }; outer.name = dev.name + ' (exploded)';
  return outer;
}

// ------------------------------------------------------------------ accessories
function tubeAlong(points, w, t, m, name, closed = false, seg = 300) {
  const curve = new THREE.CatmullRomCurve3(points, closed, 'catmullrom', 0.5);
  const sh = roundedRectShape(t, w, Math.min(t, w) * 0.45);
  const geo = new THREE.ExtrudeGeometry(sh, { steps: seg, bevelEnabled: false, extrudePath: curve });
  return named(new THREE.Mesh(geo, m), name, 'accessory');
}
function roundTube(points, r, m, name, closed = false, seg = 300) {
  const curve = new THREE.CatmullRomCurve3(points, closed, 'catmullrom', 0.5);
  return named(new THREE.Mesh(new THREE.TubeGeometry(curve, seg, r, 24, closed), m), name, 'accessory');
}
// LORE Mount male puck (shared by every accessory), facing +Z
export function mountPuck(PR, m, { d = 23.6, t = 2.4 } = {}) {
  const grp = new THREE.Group();
  const ol = circle(d / 2, 128);
  grp.add(named(new THREE.Mesh(sweep(ol, slabProfile({ H: t, rt: 0.6, rb: 0.3, cap: 6, fil: 6 })), m), 'mount_puck', 'accessory'));
  for (let k = 0; k < 3; k++) {
    const lug = box(4, 1.4, 0.8, 0.3, m, 'mount_lug'); const a = k * Math.PI * 2 / 3;
    lug.position.set(Math.cos(a) * (d / 2 - 0.6), Math.sin(a) * (d / 2 - 0.6), t - 0.4); lug.rotation.z = a + Math.PI / 2; grp.add(lug);
  }
  for (const dx of [-2.5, 2.5]) { const pin = named(new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 0.6, 24), M.gold()), 'pogo_pin', 'accessory'); pin.rotation.x = Math.PI / 2; pin.position.set(dx, 0, t + 0.15); grp.add(pin); }
  return grp;
}
export function buildClip(PR) {
  const g = new THREE.Group(); g.name = 'LORE Clip';
  const steel = M.steel();
  g.add(mountPuck(PR, steel));
  // spring tongue: 17-7PH stainless, 1.0 mm, U-bend at top, runs down the back of the puck
  const pts = [new THREE.Vector3(0, 8, -0.2), new THREE.Vector3(0, 15, -0.6), new THREE.Vector3(0, 18.5, -3.0), new THREE.Vector3(0, 15.5, -5.8),
    new THREE.Vector3(0, 4, -5.6), new THREE.Vector3(0, -12, -4.4), new THREE.Vector3(0, -22, -3.0), new THREE.Vector3(0, -25, -3.6)];
  const tongue = tubeAlong(pts, 16, 1.1, M.steelPolish(), 'clip_spring');
  g.add(tongue);
  const pad = box(16, 6, 1.2, 2, M.silicone(0x1d1f23), 'clip_grip_pad'); pad.position.set(0, -20, -3.4); pad.rotation.x = Math.PI; g.add(pad);
  return g;
}
export function buildLanyard(PR, { length = 420, color = 0x7A4A2C } = {}) {
  const g = new THREE.Group(); g.name = 'LORE Leather Lanyard';
  const yoke = new THREE.Group();
  yoke.add(mountPuck(PR, M.steel()));
  const tab = box(10, 18, 2.4, 3, M.leather(color), 'lanyard_yoke_leather'); tab.position.set(0, 14, -1.2); yoke.add(tab);
  g.add(yoke);
  const ring = named(new THREE.Mesh(new THREE.TorusGeometry(4.2, 0.9, 24, 64), M.brass()), 'brass_ring', 'accessory'); ring.position.set(0, 26, 0); ring.rotation.y = Math.PI / 2; g.add(ring);
  for (const sx of [-1, 1]) {
    const pts = [new THREE.Vector3(sx * 1.5, 26, 0), new THREE.Vector3(sx * 2.2, 40, -0.5), new THREE.Vector3(sx * 2.6, 56, -1), new THREE.Vector3(sx * 12, 140, -4), new THREE.Vector3(sx * 34, 280, -10), new THREE.Vector3(sx * 58, length, -16)];
    g.add(tubeAlong(pts, 2.2, 9, M.leather(color), 'lanyard_strap'));
  }
  const slider = box(12, 8, 5, 2, M.brass(), 'brass_slider'); slider.position.set(0, 52, 0); g.add(slider);
  return g;
}
export function buildWristStrap(PR, { color = 0x7A4A2C } = {}) {
  const g = new THREE.Group(); g.name = 'LORE Wrist Strap';
  g.add(mountPuck(PR, M.steel()));
  const pts = [];
  for (let k = 0; k <= 30; k++) { const a = (k / 30) * Math.PI * 2; pts.push(new THREE.Vector3(Math.sin(a) * 38, 30 + 70 - Math.cos(a) * 70 * 0.5 - 35, Math.sin(a * 2) * 3 - 4)); }
  const strap = tubeAlong(pts.slice(0, 30), 8, 2.0, M.leather(color), 'wrist_loop', true);
  g.add(strap);
  const tab = box(10, 14, 2.6, 3, M.leather(color), 'wrist_tab'); tab.position.set(0, 12, -1.2); g.add(tab);
  const keeper = box(13, 7, 5, 2, M.brass(), 'brass_keeper'); keeper.position.set(0, 24, -1); g.add(keeper);
  return g;
}
export function buildDock(PR, { finish = 'sq-ink' } = {}) {
  const g = new THREE.Group(); g.name = 'LORE Dock';
  const F = FINISHES[finish];
  const base = new THREE.Mesh(sweep(squircleRect(72, 60, 22, 3.2), slabProfile({ H: 12, rt: 3, rb: 1.2, cap: 10 })), mat(F.frame));
  base.rotation.x = -Math.PI / 2; g.add(named(base, 'dock_base_al', 'accessory'));
  const foot = new THREE.Mesh(sweep(squircleRect(66, 54, 20, 3.2), slabProfile({ H: 0.8, rt: 0.3, rb: 0.3, cap: 3, fil: 3 })), M.silicone(0x111214));
  foot.rotation.x = -Math.PI / 2; foot.position.y = -0.8; g.add(named(foot, 'dock_silicone_foot', 'accessory'));
  const cradle = new THREE.Group();
  const back = new THREE.Mesh(sweep(squircleRect(50, 46, 14, 3.4), slabProfile({ H: 9, rt: 3, rb: 3, cap: 10 })), mat(F.frame));
  cradle.add(named(back, 'dock_cradle', 'accessory'));
  const puck = mountPuck(PR, M.steel(), { t: 1.2 }); puck.position.z = 9; cradle.add(puck);
  cradle.rotation.x = -Math.PI / 2 + THREE.MathUtils.degToRad(68); cradle.position.set(0, 10, -8);
  g.add(cradle);
  const led = new THREE.Mesh(new THREE.CircleGeometry(0.6, 24), M.ledOn(0xF2A27A, 1.2)); led.position.set(0, 6, 30.05); g.add(led);
  g.userData.cradle = cradle;
  return g;
}
export function buildRuggedCase(PR, { color = 0x5E6B4E } = {}) {
  const S = squareParams(PR, 'square');
  const g = new THREE.Group(); g.name = 'LORE Rugged Case';
  const ol = squircleRect(S.plan_w, S.plan_h, S.corner_r, S.corner_n);
  const T = S.thickness_total, w = 2.0, lip = 1.6;
  // closed C-section swept around the device outline; corners thicker via per-vertex offset
  const prof = [];
  const back = -1.4;
  for (let k = 0; k <= 12; k++) { const s = k / 12; prof.push({ o: -3, s: 0.0001 + s * 0.999, z: back }); }
  for (let k = 1; k <= 8; k++) { const f = (k / 8) * Math.PI / 2; prof.push({ o: -3 + (w + 3) * Math.sin(f), z: back + 3 - 3 * Math.cos(f) }); }
  for (let k = 1; k <= 8; k++) { const f = Math.PI / 2 + (k / 8) * Math.PI / 2; prof.push({ o: w - 2.2 + 2.2 * Math.sin(f), z: T + 0.6 - 2.2 - 2.2 * Math.cos(f) }); }
  prof.push({ o: -lip, z: T + 0.6 }, { o: -lip - 0.4, z: T + 0.2 }, { o: -lip - 0.4, z: T - 0.4 });
  const geo = sweep(ol, prof);
  // corner bumpers: push outward where |x| and |y| both large
  const pp = geo.attributes.position;
  for (let i = 0; i < pp.count; i++) {
    const x = pp.getX(i), y = pp.getY(i), r = Math.hypot(x, y); if (r < 24) continue;
    const c = Math.pow(Math.abs(Math.sin(2 * Math.atan2(y, x))), 6) * 1.6 * Math.min(1, (r - 24) / 6);
    pp.setX(i, x * (1 + c / r)); pp.setY(i, y * (1 + c / r));
  }
  geo.computeVertexNormals();
  const tm = M.tpu(color); tm.side = THREE.DoubleSide;
  g.add(named(new THREE.Mesh(geo, tm), 'case_tpu', 'accessory'));
  // ribs on sides (grip) and a lanyard eyelet at the NW corner
  const ey = named(new THREE.Mesh(new THREE.TorusGeometry(2.6, 1.1, 20, 48), M.tpu(color)), 'case_eyelet', 'accessory');
  ey.position.set(-26.5, 26.5, 3); ey.rotation.set(Math.PI / 2, 0, Math.PI / 4); g.add(ey);
  return g;
}
export function buildBuds(PR, { color = 0x1D1F23, accent = 0xC59E62 } = {}) {
  const g = new THREE.Group(); g.name = 'LORE Buds';
  // titanium memory-alloy neckband (Ø3.2 silicone over Ø1.2 Ti wire)
  const band = [];
  for (let k = 0; k <= 30; k++) { const t = k / 30, a = Math.PI * (t - 0.5) * 1.12; band.push(new THREE.Vector3(Math.sin(a) * 62, -Math.cos(a) * 58 + 40 + 6 * Math.sin(t * Math.PI), -10 * Math.sin(t * Math.PI))); }
  g.add(roundTube(band, 1.7, M.silicone(color), 'neckband'));
  for (const sx of [-1, 1]) {
    const end = band[sx < 0 ? 0 : band.length - 1];
    // ear hook + electronics housing + transducer pad
    const hook = [end.clone(), end.clone().add(new THREE.Vector3(sx * 4, 10, 2)), end.clone().add(new THREE.Vector3(sx * 2, 26, 4)), end.clone().add(new THREE.Vector3(-sx * 8, 34, 6)), end.clone().add(new THREE.Vector3(-sx * 18, 28, 7))];
    g.add(roundTube(hook, 2.6, M.silicone(color), 'ear_hook', false, 80));
    const pod = new THREE.Mesh(sweep(squircleRect(14, 22, 6, 2.6), slabProfile({ H: 6.5, rt: 2.4, rb: 2.0, cap: 10 })), M.silicone(color));
    const tip = hook[4]; pod.position.copy(tip).add(new THREE.Vector3(-sx * 2, -10, 0)); pod.rotation.y = sx * 0.35;
    g.add(named(pod, 'transducer_pod', 'accessory'));
    const ringA = named(new THREE.Mesh(new THREE.TorusGeometry(4.4, 0.35, 16, 64), M.brass()), 'pod_accent', 'accessory');
    ringA.position.copy(pod.position).add(new THREE.Vector3(0, 2, 6.6)); ringA.rotation.y = sx * 0.35; ringA.material.color.set(accent); g.add(ringA);
    const batt = new THREE.Mesh(sweep(squircleRect(11, 26, 5.5, 2.4), slabProfile({ H: 8, rt: 3.5, rb: 3.5, cap: 10 })), M.silicone(color));
    batt.position.copy(end).add(new THREE.Vector3(sx * 0.5, -6, -4)); batt.rotation.y = sx * Math.PI / 2; g.add(named(batt, 'battery_pod', 'accessory'));
  }
  return g;
}
export function buildPowerPuck(PR, { finish = 'sq-ink' } = {}) {
  const F = FINISHES[finish];
  const g = new THREE.Group(); g.name = 'LORE Power Puck';
  const ol = squircleRect(64, 64, 22, 3.0);
  const body = new THREE.Mesh(sweep(ol, slabProfile({ H: 16, rt: 4, rb: 4, cap: 14 })), mat(F.frame));
  g.add(named(body, 'puck_body_al', 'accessory'));
  const top = new THREE.Mesh(sweep(offsetOutline(ol, -4.5), [{ o: 0, s: 1, z: 16.0 }, ...Array.from({ length: 9 }, (_, k) => ({ o: 0, s: 1 - (k + 1) / 9, z: 16.05 }))]), M.silicone(0x16171a));
  g.add(named(top, 'puck_top_pad', 'accessory'));
  const puck = mountPuck(PR, M.steel(), { t: 0.8 }); puck.position.z = 16; g.add(puck);
  for (let k = 0; k < 4; k++) { const l = new THREE.Mesh(new THREE.CircleGeometry(0.45, 20), k < 3 ? M.ledOn(0xF2E6D8, 1.5) : M.hole()); onSide(ol, idxNearX(ol, -4.5 + k * 3, -1), 10, l); g.add(l); }
  const usb = slot(9.2, 3.4, M.hole()); onSide(ol, idxNearY(ol, 0, 1), 8, usb); g.add(usb);
  g.userData.top = 16.8;
  return g;
}

// ------------------------------------------------------------------ props for scale & context
export function buildCreditCard() { // ISO/IEC 7810 ID-1: 85.60 × 53.98 × 0.76 mm, r 3.18
  const m = M.card(); const g = new THREE.Group(); g.name = 'ID-1 card (85.60 × 53.98 mm)';
  g.add(named(new THREE.Mesh(sweep(squircleRect(85.6, 53.98, 3.18, 2), slabProfile({ H: 0.76, rt: 0.3, rb: 0.3, cap: 3, fil: 3 })), m), 'card', 'prop'));
  const chip = box(11, 9, 0.05, 1.4, M.gold(), 'chip'); chip.position.set(-28, 4, 0.76); g.add(chip);
  return g;
}
export function buildEuroCoin() { // €1: Ø23.25 mm, 2.33 mm
  const g = new THREE.Group(); g.name = '€1 coin (Ø23.25 mm)';
  const o = new THREE.Mesh(new THREE.CylinderGeometry(23.25 / 2, 23.25 / 2, 2.33, 96), M.coinOuter()); o.rotation.x = Math.PI / 2; o.position.z = 2.33 / 2;
  const i = new THREE.Mesh(new THREE.CylinderGeometry(8, 8, 2.36, 96), M.coinInner()); i.rotation.x = Math.PI / 2; i.position.z = 2.33 / 2;
  g.add(named(o, 'coin_ring', 'prop'), named(i, 'coin_core', 'prop'));
  return g;
}
// Abstract "artist mannequin" hand, 50th-percentile adult (hand length ~ 189 mm, breadth ~ 86 mm), palm up.
export function buildHand(color = 0xD8CDBF) {
  const m = M.clay(color); const g = new THREE.Group(); g.name = 'mannequin hand (P50, 189 mm)';
  const palm = new THREE.Mesh(sweep(superellipse(84, 100, 2.6), slabProfile({ H: 26, rt: 11, rb: 10, top: (s) => -3 * (1 - s * s), cap: 20 })), m);
  g.add(named(palm, 'palm', 'prop'));
  const fingers = [[-30, 72, 8.0, 0.10], [-10, 84, 8.8, 0.03], [10, 80, 8.6, -0.04], [29, 64, 7.8, -0.13]];
  for (const [x, len, r, rot] of fingers) {
    const f = new THREE.Mesh(new THREE.CapsuleGeometry(r, len - 2 * r, 12, 32), m);
    f.position.set(x + Math.sin(-rot) * len / 2, 50 + len / 2 - 6, 9.5); f.rotation.z = rot;
    g.add(named(f, 'finger', 'prop'));
  }
  const thumb = new THREE.Mesh(new THREE.CapsuleGeometry(10.5, 48, 12, 32), m);
  thumb.position.set(-52, 2, 11); thumb.rotation.z = 0.85; g.add(named(thumb, 'thumb', 'prop'));
  const wrist = new THREE.Mesh(new THREE.CapsuleGeometry(22, 40, 12, 48), m);
  wrist.position.set(0, -72, 12); wrist.scale.set(1.25, 1, 0.55); g.add(named(wrist, 'wrist', 'prop'));
  return g;
}
