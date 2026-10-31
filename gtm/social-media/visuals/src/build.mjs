// Render LORE social covers to PNG + a contact sheet.
// Run from repo root:
//   PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node gtm/social-media/visuals/src/build.mjs
// Requires: (cd gtm/tools && npm install)  -> playwright + @fontsource-variable fonts
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { designs, css } from './designs.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.resolve(here, '../../../tools/package.json'));
const { chromium } = require('playwright');
const htmlDir = path.resolve(here, 'html');
const pngDir = path.resolve(here, '../png');
fs.mkdirSync(htmlDir, { recursive: true });
fs.mkdirSync(pngDir, { recursive: true });

const page = (d) => `<!doctype html><html><head><meta charset="utf-8"><title>${d.title}</title>
<style>:root{--w:${d.w}px;--h:${d.h}px}${css}</style></head><body>${d.body}</body></html>`;

const browser = await chromium.launch();
const ctx = await browser.newContext({ deviceScaleFactor: 1 });
const p = await ctx.newPage();
const out = [];
for (const d of designs) {
  const f = path.join(htmlDir, `${d.id}.html`);
  fs.writeFileSync(f, page(d));
  await p.setViewportSize({ width: d.w, height: d.h });
  await p.goto('file://' + f);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(150);
  const png = path.join(pngDir, `${d.id}-${d.w}x${d.h}.png`);
  await p.screenshot({ path: png, clip: { x: 0, y: 0, width: d.w, height: d.h } });
  out.push({ ...d, png });
  console.log('rendered', path.basename(png));
}

// contact sheet
const feed = out.filter(o => o.h === 1350), story = out.filter(o => o.h === 1920);
const tile = (o, w) => `<figure><img src="file://${o.png}" style="width:${w}px"><figcaption>${o.id} · ${o.w}×${o.h}<br><span>${o.title}</span></figcaption></figure>`;
const sheet = `<!doctype html><html><head><meta charset="utf-8"><style>${css}
 html,body{width:2400px;height:auto;overflow:visible;background:#EAE3D7}
 .wrap{padding:80px}
 h2{font-family:Fraunces;font-weight:400;font-size:64px;color:#14161A}
 .sub{font-family:'JetBrains Mono';font-size:20px;letter-spacing:.1em;color:#5C5F66;margin:10px 0 50px}
 .grid{display:flex;flex-wrap:wrap;gap:36px;margin-bottom:70px}
 figure{background:#F3EEE6;padding:16px;border-radius:14px;box-shadow:0 2px 0 #C6C7C6}
 img{display:block;border-radius:6px}
 figcaption{font-family:'JetBrains Mono';font-size:15px;color:#14161A;margin-top:12px;line-height:1.45}
 figcaption span{font-family:Inter;color:#5C5F66}
</style></head><body><div class="wrap">
<h2>LORE: social covers v1</h2><div class="sub">FEED 4:5 · 1080×1350 · ${feed.length} DESIGNS — STORIES/TIKTOK 9:16 · 1080×1920 · ${story.length} DESIGNS · GENERATED ${new Date().toISOString().slice(0,10)}</div>
<div class="grid">${feed.map(o => tile(o, 520)).join('')}</div>
<div class="grid">${story.map(o => tile(o, 340)).join('')}</div>
</div></body></html>`;
const sf = path.join(htmlDir, 'contact-sheet.html');
fs.writeFileSync(sf, sheet);
await p.setViewportSize({ width: 2400, height: 1200 });
await p.goto('file://' + sf);
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(300);
await p.screenshot({ path: path.resolve(here, '../contact-sheet.png'), fullPage: true });
console.log('rendered contact-sheet.png');
await browser.close();
