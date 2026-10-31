// LORE product-render studio: PBR scene, cyclorama sweep, area-light soft shadows via
// multi-frame accumulation (jittered key light + sub-pixel camera jitter), float averaging.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

export function makeStudio({ width, height, bg = 0xE7E1D7, env = 0.85, exposure = 1.0, sweep = true }) {
  const canvas = document.createElement('canvas');
  canvas.width = width; canvas.height = height;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, alpha: false });
  renderer.setPixelRatio(1); renderer.setSize(width, height, false);
  renderer.toneMapping = THREE.NeutralToneMapping; renderer.toneMappingExposure = exposure;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(bg);
  const pm = new THREE.PMREMGenerator(renderer);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = env;
  let floor = null;
  if (sweep) {
    // cyclorama: flat floor curving up into a back wall (radius 400 mm)
    const geo = new THREE.PlaneGeometry(4000, 3000, 2, 160);
    const p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const v = p.getY(i) + 900; // v: distance along sweep from front edge
      const R = 400, flat = 1200;
      let y = 0, z = 0;
      if (v < flat) { z = flat - v; y = 0; }
      else if (v < flat + Math.PI * R / 2) { const a = (v - flat) / R; z = -Math.sin(a) * R; y = R - Math.cos(a) * R; }
      else { z = -R; y = R + (v - flat - Math.PI * R / 2); }
      p.setXYZ(i, p.getX(i), y, z - 300);
    }
    geo.computeVertexNormals();
    floor = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: bg, roughness: 0.95, metalness: 0 }));
    floor.receiveShadow = true; scene.add(floor);
  }
  const key = new THREE.DirectionalLight(0xfff4e8, 2.2);
  key.castShadow = true; key.shadow.mapSize.set(4096, 4096);
  const sc = key.shadow.camera; sc.left = -260; sc.right = 260; sc.top = 260; sc.bottom = -260; sc.near = 10; sc.far = 3000;
  key.shadow.bias = -0.0002; key.shadow.normalBias = 0.15;
  scene.add(key, key.target);
  const fill = new THREE.DirectionalLight(0xe8f0ff, 0.35); scene.add(fill);
  const rim = new THREE.DirectionalLight(0xffffff, 0.0); scene.add(rim);
  const sky = new THREE.DirectionalLight(0xffffff, 0.6); sky.castShadow = true; sky.shadow.mapSize.set(2048, 2048);
  Object.assign(sky.shadow.camera, { left: -260, right: 260, top: 260, bottom: -260, near: 10, far: 3000 }); sky.shadow.bias = -0.0003; sky.shadow.normalBias = 0.2;
  scene.add(sky, sky.target);
  return { canvas, renderer, scene, key, fill, rim, sky, floor,
    keyDir: new THREE.Vector3(-0.55, 1.0, 0.65).normalize(), keySpread: 0.12, target: new THREE.Vector3() };
}

export function placeOnFloor(obj, y = 0) {
  obj.updateMatrixWorld(true);
  const b = new THREE.Box3().setFromObject(obj);
  obj.position.y += y - b.min.y; obj.updateMatrixWorld(true);
  return obj;
}

// Accumulate N jittered frames into a float buffer, then write to an output 2D canvas.
export async function accumulate(st, camera, { frames = 24, out, onFrame } = {}) {
  const { renderer, scene, key, sky, canvas } = st;
  const W = canvas.width, H = canvas.height, gl = renderer.getContext();
  const sum = new Float32Array(W * H * 4), px = new Uint8Array(W * H * 4);
  let seed = 3; const rnd = () => ((seed = (seed * 48271) % 2147483647) / 2147483647);
  const t = st.target;
  for (let f = 0; f < frames; f++) {
    // key: small area light (soft penumbra); sky: wide dome sampling (contact occlusion)
    const kd = st.keyDir.clone().add(new THREE.Vector3((rnd() - 0.5), (rnd() - 0.5), (rnd() - 0.5)).multiplyScalar(st.keySpread * 2)).normalize();
    key.position.copy(t).addScaledVector(kd, 900); key.target.position.copy(t);
    const th = rnd() * Math.PI * 2, ph = Math.acos(1 - rnd() * 0.75);
    const sd = new THREE.Vector3(Math.sin(ph) * Math.cos(th), Math.cos(ph), Math.sin(ph) * Math.sin(th));
    sky.position.copy(t).addScaledVector(sd, 900); sky.target.position.copy(t);
    if (camera.setViewOffset) camera.setViewOffset(W, H, rnd() - 0.5, rnd() - 0.5, W, H);
    renderer.render(scene, camera);
    gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    for (let i = 0; i < px.length; i++) sum[i] += px[i];
    if (onFrame) onFrame(f);
    await new Promise((r) => setTimeout(r, 0));
  }
  if (camera.clearViewOffset) camera.clearViewOffset();
  const ctx = out.getContext('2d'); const img = ctx.createImageData(W, H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const s = ((H - 1 - y) * W + x) * 4, d = (y * W + x) * 4;
    img.data[d] = sum[s] / frames; img.data[d + 1] = sum[s + 1] / frames; img.data[d + 2] = sum[s + 2] / frames; img.data[d + 3] = 255;
  }
  ctx.putImageData(img, 0, 0);
}

// Project a world point into pixel coords of the output image.
export function project(camera, v, W, H) {
  const p = v.clone().project(camera);
  return { x: (p.x * 0.5 + 0.5) * W, y: (-p.y * 0.5 + 0.5) * H };
}
