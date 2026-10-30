// LORE design render harness.
// Serves /design over HTTP and drives headless Chromium (Playwright) to capture pages to PNG.
// Usage (from design/):  node tools/render.mjs <jobs.json | inline-json>
// A job: { "url": "industrial/render.html?shot=hero-square", "out": "industrial/renders/x.png",
//          "width": 2400, "height": 1600, "scale": 1, "waitFor": "window.__done === true", "timeout": 600000 }
// A job with "eval" instead of "out" runs page.evaluate and writes its (base64) result to "save".
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.glb': 'model/gltf-binary', '.stl': 'model/stl' };

export function serve(port = 0) {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
      let f = path.join(ROOT, p);
      if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
      // allow brand assets one level up (read-only), e.g. /../brand/...
      if (p.startsWith('/_brand/')) f = path.join(ROOT, '..', 'brand', p.slice(8));
      fs.readFile(f, (err, buf) => {
        if (err) { res.writeHead(404); return res.end('404 ' + p); }
        res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
        res.end(buf);
      });
    });
    srv.listen(port, '127.0.0.1', () => resolve(srv));
  });
}

export async function run(jobs, { gl = true } = {}) {
  const srv = await serve();
  const base = `http://127.0.0.1:${srv.address().port}/`;
  const browser = await chromium.launch({
    executablePath: CHROME,
    args: gl ? ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
      '--enable-webgl', '--disable-gpu-sandbox'] : [],
  });
  try {
    for (const j of jobs) {
      const t0 = Date.now();
      const ctx = await browser.newContext({ viewport: { width: j.width || 1200, height: j.height || 800 },
        deviceScaleFactor: j.scale || 1 });
      const page = await ctx.newPage();
      page.on('console', (m) => { if (m.type() === 'error' || process.env.VERBOSE) console.log('  [page]', m.text()); });
      page.on('pageerror', (e) => console.log('  [pageerror]', e.message));
      await page.goto(base + j.url, { waitUntil: 'load', timeout: 120000 });
      await page.evaluate(() => document.fonts && document.fonts.ready);
      if (j.waitFor) await page.waitForFunction(j.waitFor, null, { timeout: j.timeout || 900000, polling: 500 });
      else await page.waitForTimeout(j.delay || 400);
      if (j.eval) {
        const data = await page.evaluate(j.eval);
        for (const [name, b64] of Object.entries(data)) {
          const out = path.join(ROOT, j.saveDir, name);
          fs.mkdirSync(path.dirname(out), { recursive: true });
          fs.writeFileSync(out, Buffer.from(b64, 'base64'));
          console.log('  wrote', path.relative(ROOT, out), (fs.statSync(out).size / 1024).toFixed(0) + ' KB');
        }
      }
      if (j.out) {
        const out = path.join(ROOT, j.out);
        fs.mkdirSync(path.dirname(out), { recursive: true });
        const sel = j.selector ? await page.$(j.selector) : null;
        if (sel) await sel.screenshot({ path: out, omitBackground: !!j.transparent });
        else await page.screenshot({ path: out, omitBackground: !!j.transparent });
        console.log(`  ${j.out}  (${((Date.now() - t0) / 1000).toFixed(1)}s)`);
      }
      await ctx.close();
    }
  } finally {
    await browser.close();
    srv.close();
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const arg = process.argv[2];
  const jobs = JSON.parse(fs.existsSync(arg) ? fs.readFileSync(arg, 'utf8') : arg);
  const filter = process.argv[3];
  await run(filter ? jobs.filter((j) => (j.out || j.url).includes(filter)) : jobs, { gl: !process.env.NOGL });
}
