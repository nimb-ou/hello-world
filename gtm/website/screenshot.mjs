// Render desktop + mobile screenshots of the landing page.
// Run: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node gtm/website/screenshot.mjs
import path from 'node:path';
import fs from 'node:fs';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const { chromium } = createRequire(path.resolve(here, '../tools/package.json'))('playwright');
const out = path.join(here, 'screenshots'); fs.mkdirSync(out, { recursive: true });
const url = 'file://' + path.join(here, 'index.html');
const b = await chromium.launch();
async function shot(name, opts, fn) {
  const ctx = await b.newContext(opts); const p = await ctx.newPage();
  await p.goto(url); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('in')));
  await p.waitForTimeout(800);
  if (fn) await fn(p); else await p.screenshot({ path: path.join(out, name), fullPage: true });
  console.log('saved', name); await ctx.close();
}
await shot('desktop-full-1440.png', { viewport: { width: 1440, height: 900 } });
await shot('desktop-hero-1440x900.png', { viewport: { width: 1440, height: 900 } }, p => p.screenshot({ path: path.join(out, 'desktop-hero-1440x900.png') }));
await shot('mobile-full-390.png', { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
await shot('mobile-hero-390x844.png', { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }, p => p.screenshot({ path: path.join(out, 'mobile-hero-390x844.png') }));
// validation states
await shot('desktop-form-error.png', { viewport: { width: 1440, height: 900 } }, async p => {
  await p.fill('#email', 'nimit@'); await p.click('button[type=submit]');
  const el = await p.$('#waitlist'); await el.screenshot({ path: path.join(out, 'desktop-form-error.png') });
});
await shot('desktop-form-success.png', { viewport: { width: 1440, height: 900 } }, async p => {
  await p.fill('#email', 'traveller@example.com'); await p.check('#consent'); await p.click('button[type=submit]');
  const el = await p.$('#waitlist'); await el.screenshot({ path: path.join(out, 'desktop-form-success.png') });
});
await b.close();
