// Renders the LORE companion app screens from ux/app-screens/screens.html:
//   png/<id>.png (390x844 @2x), contact-sheet.png (labelled grid), phone-mockup.png (3 screens in phone frames)
// Run from design/:  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node ux/scripts/render-app-screens.mjs [filter]
import { run } from '../../tools/render.mjs';
const page = 'ux/app-screens/screens.html';
const ids = ['01-welcome', '02-pair', '03-interests-persona', '04-city-pack-store', '05-rome-pack-detail', '06-live-walk-map',
  '07-day-recap', '08-safety', '09-lore-pass', '10-device-settings', '11-story-detail', '12-dinner-booking'];
const wait = 'window.__done===true';
const jobs = ids.map((s) => ({ url: `${page}?s=${s}`, out: `ux/app-screens/png/${s}.png`, width: 390, height: 844, scale: 2, selector: '#cap', waitFor: wait }));
jobs.push({ url: page, out: 'ux/app-screens/contact-sheet.png', width: 2800, height: 2300, selector: '#sheet', waitFor: wait });
jobs.push({ url: `${page}?view=mockup`, out: 'ux/app-screens/phone-mockup.png', width: 1900, height: 1200, scale: 2, selector: '#sheet', waitFor: wait });
const f = process.argv[2];
await run(f ? jobs.filter((j) => j.out.includes(f)) : jobs, { gl: false });
