// Renders LORE Square/Atlas device screens from ux/device-screens/screens.html:
//   png/<id>.png (466x466 each), contact-sheet.png (labelled grid), on-device-mockup.png (4 screens in the drawn device)
// Run from design/:  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node ux/scripts/render-device-screens.mjs [filter]
import { run } from '../../tools/render.mjs';
const page = 'ux/device-screens/screens.html';
const ids = ['01-home-compass', '02-now-narrating', '03-nearby', '04-navigation', '05-listening', '06-answer', '07-dinner',
  '08-sos-countdown', '09-sos-live', '10-walk-me-home', '11-city-pack-download', '12-battery-low-power',
  '13-settings-narrator-persona', '14-offline-mode', '15-nightstand'];
const wait = 'window.__done===true';
const jobs = ids.map((s) => ({ url: `${page}?s=${s}`, out: `ux/device-screens/png/${s}.png`, width: 466, height: 466, selector: '#cap', waitFor: wait }));
jobs.push({ url: page, out: 'ux/device-screens/contact-sheet.png', width: 2800, height: 2200, selector: '#sheet', waitFor: wait });
jobs.push({ url: `${page}?view=mockup`, out: 'ux/device-screens/on-device-mockup.png', width: 1760, height: 1000, scale: 2, selector: '#sheet', waitFor: wait });
const f = process.argv[2];
await run(f ? jobs.filter((j) => j.out.includes(f)) : jobs, { gl: false });
