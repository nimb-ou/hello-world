// LORE CMF -> three.js PBR materials. Colour values are render targets matched to the CMF table
// in industrial/id-spec.md (section 7). Physical masters (Pantone/NCS + gloss units) are in that doc.
import * as THREE from 'three';

const P = (o) => new THREE.MeshPhysicalMaterial(o);

// Micro-texture for bead-blast / soft-touch: tiling noise used as a bump map.
let _noise = null;
export function noiseTexture() {
  if (_noise) return _noise;
  const c = document.createElement('canvas'); c.width = c.height = 512;
  const g = c.getContext('2d'); const d = g.createImageData(512, 512);
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < d.data.length; i += 4) { const v = 110 + rnd() * 40; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
  g.putImageData(d, 0, 0);
  _noise = new THREE.CanvasTexture(c); _noise.wrapS = _noise.wrapT = THREE.RepeatWrapping; _noise.repeat.set(6, 6);
  return _noise;
}

function blasted(o, bump = 0.4) { return P({ ...o, bumpMap: noiseTexture(), bumpScale: bump }); }

export const FINISHES = {
  // ---------------- Pebble: PC + 10% glass fibre, 2K PU soft-touch paint (Bone/Ink/Terracotta)
  bone: { label: 'Bone', sku: 'pebble',
    body: () => blasted({ color: 0xE6DED1, roughness: 0.68, metalness: 0, sheen: 0.35, sheenRoughness: 0.8, sheenColor: 0xffffff, clearcoat: 0.0 }, 0.25),
    dish: () => blasted({ color: 0xE9E2D6, roughness: 0.55, metalness: 0, sheen: 0.3, sheenRoughness: 0.7 }, 0.2),
    back: '#DCD3C5', backText: 'rgba(120,108,92,0.9)' },
  ink: { label: 'Ink', sku: 'pebble',
    body: () => blasted({ color: 0x1D1F23, roughness: 0.62, metalness: 0, sheen: 0.5, sheenRoughness: 0.75, sheenColor: 0x8a8f99 }, 0.25),
    dish: () => blasted({ color: 0x202226, roughness: 0.5, metalness: 0, sheen: 0.4, sheenRoughness: 0.6, sheenColor: 0x8a8f99 }, 0.2),
    back: '#1A1C20', backText: 'rgba(150,154,160,0.85)' },
  terracotta: { label: 'Terracotta', sku: 'pebble',
    body: () => blasted({ color: 0xB4573A, roughness: 0.66, metalness: 0, sheen: 0.4, sheenRoughness: 0.8, sheenColor: 0xffd9c4 }, 0.25),
    dish: () => blasted({ color: 0xBA5C3D, roughness: 0.52, metalness: 0, sheen: 0.35, sheenRoughness: 0.7, sheenColor: 0xffd9c4 }, 0.2),
    back: '#A9502F', backText: 'rgba(240,215,195,0.8)' },

  // ---------------- Square: 6013-T6 aluminium, bead-blast + Type II anodise; diamond-cut chamfer
  'sq-ink': { label: 'Ink', sku: 'square',
    frame: () => blasted({ color: 0x3B3C40, metalness: 1, roughness: 0.42 }, 0.35),
    chamfer: () => P({ color: 0x80858E, metalness: 1, roughness: 0.1 }),
    back: '#1C1E22', backRough: 0.5, backText: 'rgba(140,145,152,0.9)',
    split: 0x15171a, key: () => blasted({ color: 0xC4623A, metalness: 1, roughness: 0.38 }, 0.3),
    crown: () => blasted({ color: 0x3B3C40, metalness: 1, roughness: 0.32 }, 0.2) },
  'sq-sand': { label: 'Sand', sku: 'square',
    frame: () => blasted({ color: 0xCDBDA3, metalness: 1, roughness: 0.42 }, 0.35),
    chamfer: () => P({ color: 0xF0E4D0, metalness: 1, roughness: 0.1 }),
    back: '#D6CAB6', backRough: 0.5, backText: 'rgba(120,105,85,0.9)',
    split: 0xb9ab95, key: () => blasted({ color: 0xC4623A, metalness: 1, roughness: 0.38 }, 0.3),
    crown: () => blasted({ color: 0xCDBDA3, metalness: 1, roughness: 0.32 }, 0.2) },

  // ---------------- Atlas: Grade 5 titanium; bead-blast natural or black DLC; zirconia back; ZrN brass-tone crown
  'at-ti': { label: 'Bead-blasted Titanium', sku: 'atlas',
    frame: () => blasted({ color: 0xA29D94, metalness: 1, roughness: 0.46 }, 0.45),
    chamfer: () => P({ color: 0xD4CFC6, metalness: 1, roughness: 0.07 }),
    back: '#8E8982', backRough: 0.3, backText: 'rgba(60,57,52,0.85)', backClear: 0.8,
    split: 0x6e6a64, key: () => blasted({ color: 0xA29D94, metalness: 1, roughness: 0.4 }, 0.35),
    crown: () => blasted({ color: 0xC59E62, metalness: 1, roughness: 0.28 }, 0.15) },
  'at-dlc': { label: 'Black DLC Titanium', sku: 'atlas',
    frame: () => blasted({ color: 0x2A2A2D, metalness: 1, roughness: 0.34 }, 0.35),
    chamfer: () => P({ color: 0x5C5C61, metalness: 1, roughness: 0.07 }),
    back: '#141416', backRough: 0.22, backText: 'rgba(130,130,135,0.85)', backClear: 1.0,
    split: 0x111113, key: () => blasted({ color: 0x2A2A2D, metalness: 1, roughness: 0.3 }, 0.3),
    crown: () => blasted({ color: 0xC59E62, metalness: 1, roughness: 0.28 }, 0.15) },
};

export const M = {
  glass: () => P({ color: 0x050607, roughness: 0.04, metalness: 0, ior: 1.52, specularIntensity: 0.55, envMapIntensity: 0.6 }),
  sapphire: () => P({ color: 0x040506, roughness: 0.03, metalness: 0, ior: 1.77, specularIntensity: 0.45, envMapIntensity: 0.6,
    iridescence: 0.25, iridescenceIOR: 1.3, iridescenceThicknessRange: [180, 320] }),
  hole: () => new THREE.MeshStandardMaterial({ color: 0x1a1816, roughness: 0.9 }),
  usbTongue: () => new THREE.MeshStandardMaterial({ color: 0x1a1a1a, roughness: 0.5 }),
  ledOff: () => P({ color: 0xEDE6DA, roughness: 0.35, transmission: 0, sheen: 0.2, emissive: 0x000000 }),
  ledOn: (hex = 0xF2A27A, i = 2.2) => P({ color: 0xF5E9DD, roughness: 0.3, emissive: hex, emissiveIntensity: i }),
  steel: () => blasted({ color: 0xB9B9B6, metalness: 1, roughness: 0.38 }, 0.3),
  steelPolish: () => P({ color: 0xD8D8D6, metalness: 1, roughness: 0.08 }),
  gold: () => P({ color: 0xE3B866, metalness: 1, roughness: 0.25 }),
  brass: () => P({ color: 0xC59E62, metalness: 1, roughness: 0.3 }),
  lens: () => P({ color: 0x020305, roughness: 0.02, metalness: 0.2, clearcoat: 1, iridescence: 1, iridescenceIOR: 1.6, iridescenceThicknessRange: [250, 420] }),
  pcb: () => P({ color: 0x1E2A22, roughness: 0.45, clearcoat: 0.6, clearcoatRoughness: 0.3 }),
  shield: () => P({ color: 0xBFC1C3, metalness: 1, roughness: 0.3 }),
  pouch: () => P({ color: 0xC9CBCD, metalness: 0.8, roughness: 0.42 }),
  flex: () => P({ color: 0xC2772E, roughness: 0.4, clearcoat: 0.8, transmission: 0 }),
  plasticDark: () => new THREE.MeshStandardMaterial({ color: 0x2b2d31, roughness: 0.6 }),
  plasticBlack: () => new THREE.MeshStandardMaterial({ color: 0x0e0f11, roughness: 0.55 }),
  ceramicWhite: () => P({ color: 0xEEECE8, roughness: 0.3, clearcoat: 0.3 }),
  leather: (hex = 0x7A4A2C) => blasted({ color: hex, roughness: 0.62, sheen: 0.6, sheenRoughness: 0.5, sheenColor: 0xffe0c0 }, 0.9),
  leatherEdge: (hex = 0x3a2416) => P({ color: hex, roughness: 0.4, clearcoat: 0.5 }),
  tpu: (hex = 0x5E6B4E) => blasted({ color: hex, roughness: 0.55, sheen: 0.3, sheenRoughness: 0.6 }, 0.3),
  silicone: (hex = 0x1D1F23) => blasted({ color: hex, roughness: 0.5, sheen: 0.5, sheenRoughness: 0.5, sheenColor: 0x999999 }, 0.15),
  webbing: (hex = 0x2F3229) => P({ color: hex, roughness: 0.9, sheen: 0.7, sheenRoughness: 0.4, sheenColor: 0x9a9a8a }),
  clay: (hex = 0xD9CFC1) => P({ color: hex, roughness: 0.78, sheen: 0.2, sheenRoughness: 0.9 }),
  card: () => P({ color: 0x0D1B2A, roughness: 0.35, clearcoat: 0.6, clearcoatRoughness: 0.2 }),
  coinOuter: () => P({ color: 0xD8B866, metalness: 1, roughness: 0.35 }),
  coinInner: () => P({ color: 0xC9C9C6, metalness: 1, roughness: 0.35 }),
  wood: () => P({ color: 0x8A6A4C, roughness: 0.55, clearcoat: 0.2 }),
  stone: (hex = 0xCFC8BC) => blasted({ color: hex, roughness: 0.85 }, 1.2),
};
