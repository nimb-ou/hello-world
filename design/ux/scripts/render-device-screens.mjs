// Renders every device screen in ux/device-screens/screens.html to 466x466 PNG + a contact sheet.
// Run from design/:  node ux/scripts/render-device-screens.mjs
import { run } from '../../tools/render.mjs';
const ids = ['01-home-compass','02-now-narrating','03-nearby','04-navigation','05-listening','06-answer','07-dinner','08-sos-countdown','09-sos-live','10-walk-me-home','11-battery','12-nightstand','13-city-pack','14-settings','15-offline'];
const jobs = ids.map((s) => ({ url: `ux/device-screens/screens.html?s=${s}`, out: `ux/device-screens/png/${s}.png`, width: 466, height: 466, selector: '#cap', waitFor: 'window.__done===true' }));
jobs.push({ url: 'ux/device-screens/screens.html', out: 'ux/device-screens/contact-sheet.png', width: 2632, height: 1900, scale: 1, waitFor: 'window.__done===true' });
await run(jobs, { gl: false });
