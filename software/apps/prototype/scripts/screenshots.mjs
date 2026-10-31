// Builds nothing; expects `npm run app:build` first. Serves dist/ with vite preview, drives the
// PWA in SIMULATION MODE with headless Chromium, and saves phone-size screenshots.
//   PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers npm run app:screenshots
import { spawn } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

process.env.PLAYWRIGHT_BROWSERS_PATH ??= "/opt/pw-browsers";
const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../../..");
const outDir = join(here, "../screenshots");
mkdirSync(outDir, { recursive: true });
const PORT = 4173;

const server = spawn("npx", ["vite", "preview", "--config", "apps/prototype/vite.config.ts", "--port", String(PORT), "--strictPort"], { cwd: root, stdio: "pipe", detached: true });
await new Promise((res, rej) => {
  const to = setTimeout(() => rej(new Error("preview did not start")), 20000);
  server.stdout.on("data", (d) => String(d).includes(String(PORT)) && (clearTimeout(to), res()));
});

const browser = await chromium.launch();
try {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, colorScheme: "light", isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  await page.goto(`http://localhost:${PORT}/?sim=1&speed=30&mute=1&nosw=1`);
  const shot = async (name, full = false) => {
    await page.screenshot({ path: join(outDir, name), fullPage: full });
    console.log("saved", name);
  };
  const waitAlong = (m) => page.waitForFunction((m) => window.__lore && window.__lore.simAlong >= m, m, { timeout: 120000 });
  const waitPoi = (txt) => page.waitForFunction((t) => document.getElementById("poiName").textContent.includes(t), txt, { timeout: 120000 });

  await waitPoi("Pantheon");
  await page.waitForTimeout(400);
  await shot("01-sim-pantheon.png");
  await waitPoi("Navona");
  await shot("02-sim-piazza-navona.png");
  await waitPoi("Campo");
  await shot("03-sim-campo-de-fiori.png");
  await waitAlong(1150);
  await page.click("#btnAround");
  await page.waitForTimeout(300);
  await shot("04-sim-whats-around-me-largo-argentina.png", true);
  await page.click("#btnMore");
  await page.waitForTimeout(300);
  await shot("05-sim-tell-me-more.png");
  await waitPoi("Trevi");
  await shot("06-sim-trevi-fountain.png");
  await shot("07-sim-full-page.png", true);
  const dark = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, colorScheme: "dark", isMobile: true });
  const p2 = await dark.newPage();
  await p2.goto(`http://localhost:${PORT}/?sim=1&speed=30&mute=1&nosw=1&persona=storyteller`);
  await p2.waitForFunction(() => document.getElementById("poiName").textContent.includes("Navona"), null, { timeout: 120000 });
  await p2.screenshot({ path: join(outDir, "08-sim-dark-storyteller.png") });
  console.log("saved 08-sim-dark-storyteller.png");
} finally {
  await browser.close();
  try { process.kill(-server.pid, "SIGTERM"); } catch { server.kill(); }
}
process.exit(0);
