// Render SVG or HTML files to PNG with headless Chromium.
// Usage: node render.js <in.svg|in.html> <out.png> [width] [height] [--scale=2] [--opaque]
// Or:    node render.js --batch jobs.json   (array of {in, out, width, height, scale, opaque})
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const EXE = process.env.CHROME ||
  ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome'].find(p => fs.existsSync(p));

function svgSize(file) {
  const s = fs.readFileSync(file, 'utf8');
  const vb = s.match(/viewBox="([\d.\-\s]+)"/);
  const w = s.match(/<svg[^>]*\swidth="([\d.]+)/);
  const h = s.match(/<svg[^>]*\sheight="([\d.]+)/);
  if (w && h) return [parseFloat(w[1]), parseFloat(h[1])];
  if (vb) { const p = vb[1].trim().split(/\s+/).map(Number); return [p[2], p[3]]; }
  return [1024, 1024];
}

async function renderOne(browser, job) {
  const inAbs = path.resolve(job.in);
  const isSvg = inAbs.endsWith('.svg');
  let [w, h] = isSvg ? svgSize(inAbs) : [1440, 900];
  if (job.width) { const r = job.width / w; w = job.width; h = job.height || Math.round(h * r); }
  const scale = job.scale || 1;
  const ctx = await browser.newContext({ viewport: { width: Math.round(w), height: Math.round(h) }, deviceScaleFactor: scale });
  const page = await ctx.newPage();
  if (isSvg) {
    const svg = fs.readFileSync(inAbs, 'utf8');
    await page.setContent(`<!doctype html><html><head><style>html,body{margin:0;padding:0;background:transparent}svg{display:block;width:${w}px;height:${h}px}</style></head><body>${svg.replace(/<\?xml[^>]*\?>/, '')}</body></html>`, { waitUntil: 'load' });
  } else {
    await page.goto('file://' + inAbs, { waitUntil: 'networkidle' });
  }
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.waitForTimeout(150);
  const opts = { path: path.resolve(job.out), omitBackground: !job.opaque };
  if (!isSvg && job.fullPage !== false) opts.fullPage = true;
  await page.screenshot(opts);
  await ctx.close();
  console.log('rendered', job.out);
}

(async () => {
  const args = process.argv.slice(2);
  let jobs;
  if (args[0] === '--batch') jobs = JSON.parse(fs.readFileSync(args[1], 'utf8'));
  else {
    const flags = Object.fromEntries(args.filter(a => a.startsWith('--')).map(a => { const [k, v] = a.slice(2).split('='); return [k, v === undefined ? true : Number(v)]; }));
    const pos = args.filter(a => !a.startsWith('--'));
    jobs = [{ in: pos[0], out: pos[1], width: pos[2] && +pos[2], height: pos[3] && +pos[3], scale: flags.scale, opaque: flags.opaque }];
  }
  const browser = await chromium.launch({ executablePath: EXE });
  for (const j of jobs) await renderOne(browser, j);
  await browser.close();
})();
