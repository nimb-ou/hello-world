// LORE social cover designs. Each export returns {id, w, h, title, body(html)}.
// Brand: COMPANY.md palette + brand/palette/lore-colors.css; logos copied from brand/logo/svg into gtm/assets/brand.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const assets = path.resolve(here, '../../../assets');
const svg = (f) => fs.readFileSync(path.join(assets, 'brand', f), 'utf8').replace(/<\?xml[^>]*>/, '');
export const WORD = { ink: svg('lore-wordmark-ink.svg'), bone: svg('lore-wordmark-bone.svg'), terra: svg('lore-wordmark-terracotta.svg') };
export const SYM = { terra: svg('lore-symbol-terracotta.svg'), bone: svg('lore-symbol-bone.svg'), ink: svg('lore-symbol-ink.svg') };

export const css = `
@font-face{font-family:Fraunces;src:url(${assets}/fonts/fraunces-latin-full-normal.woff2) format('woff2');font-weight:100 900;font-style:normal}
@font-face{font-family:Fraunces;src:url(${assets}/fonts/fraunces-latin-full-italic.woff2) format('woff2');font-weight:100 900;font-style:italic}
@font-face{font-family:Inter;src:url(${assets}/fonts/inter-latin-wght-normal.woff2) format('woff2');font-weight:100 900}
@font-face{font-family:'JetBrains Mono';src:url(${assets}/fonts/jetbrains-mono-latin-wght-normal.woff2) format('woff2');font-weight:100 800}
:root{--ink:#14161A;--bone:#F3EEE6;--terra:#C4623A;--brass:#B8935A;--olive:#5E6B4E;--fog:#9AA0A6;--night:#0D1B2A;--signal:#D2392B;--surface:#EAE3D7;--link:#A84E2A}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:var(--w);height:var(--h);overflow:hidden}
body{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.c{position:relative;width:var(--w);height:var(--h);overflow:hidden;padding:84px 84px}
.grain:after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.10;mix-blend-mode:multiply;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .9 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.dark.grain:after{mix-blend-mode:screen;opacity:.07;filter:invert(1)}
.bone{background:var(--bone);color:var(--ink)}.ink{background:var(--ink);color:var(--bone)}.night{background:var(--night);color:var(--bone)}
.olive{background:var(--olive);color:var(--bone)}.terra{background:var(--terra);color:var(--bone)}
.kicker{font-family:'JetBrains Mono',monospace;font-size:24px;letter-spacing:.14em;text-transform:uppercase;display:flex;gap:18px;align-items:center}
.kicker .dot{width:12px;height:12px;border-radius:50%;background:var(--terra)}
.serif{font-family:Fraunces,serif;font-optical-sizing:auto;font-variation-settings:"SOFT" 50,"WONK" 0}
h1{font-family:Fraunces,serif;font-weight:400;letter-spacing:-.02em;line-height:1.02}
h1 em{font-style:italic;color:var(--terra)}
.mono{font-family:'JetBrains Mono',monospace}
.foot{position:absolute;left:84px;right:84px;bottom:72px;display:flex;justify-content:space-between;align-items:flex-end}
.foot .wm svg{height:40px;width:auto;display:block}
.foot .meta{font-family:'JetBrains Mono',monospace;font-size:20px;letter-spacing:.08em;opacity:.75;text-align:right;line-height:1.5}
.rule{height:2px;background:currentColor;opacity:.18}
.pill{display:inline-block;border:2px solid currentColor;border-radius:999px;padding:14px 30px;font-weight:600;font-size:28px;letter-spacing:.01em}
.pill.fill{background:var(--terra);border-color:var(--terra);color:var(--bone)}
.c > div[style*='width:'] > svg, .c > div[style*='width:']>svg{width:100%;height:auto;display:block}
.src{font-family:'JetBrains Mono',monospace;font-size:20px;opacity:.7;letter-spacing:.04em}
`;

const foot = (tone, meta) => `<div class="foot"><div class="wm">${tone === 'dark' ? WORD.bone : WORD.ink}</div><div class="meta">${meta}</div></div>`;

export const designs = [
// ---------- FEED 1080x1350 ----------
{ id: 'feed-01-keyhole', w: 1080, h: 1350, title: 'Secrets of Rome #01: The Aventine Keyhole', body: `
<div class="c ink dark grain">
 <div class="kicker"><span class="dot"></span>Secrets of Rome · Nº 01</div>
 <svg viewBox="0 0 600 600" style="position:absolute;left:240px;top:190px;width:600px;height:600px">
  <defs><clipPath id="kh"><path d="M267.4 310.9A78 78 0 1 1 332.6 310.9L369 462L231 462Z"/></clipPath>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9B48F"/><stop offset=".55" stop-color="#F3EEE6"/><stop offset="1" stop-color="#B8935A"/></linearGradient></defs>
  <circle cx="300" cy="300" r="290" fill="#C4623A"/>
  <g clip-path="url(#kh)"><rect width="600" height="600" fill="url(#sky)"/>
   <path d="M150 470 L150 330 Q200 300 230 330 L230 470Z M450 470 L450 330 Q400 300 370 330 L370 470Z" fill="#5E6B4E"/>
   <path d="M262 330 Q262 268 300 258 Q338 268 338 330Z" fill="#14161A"/><rect x="296" y="236" width="8" height="24" fill="#14161A"/><rect x="258" y="328" width="84" height="40" fill="#14161A"/>
   <path d="M150 470 L300 380 L450 470Z" fill="#3c4532"/></g>
 </svg>
 <h1 style="position:absolute;left:84px;right:84px;top:850px;font-size:76px">There's a keyhole in Rome where people say you can see <em>three states</em> at once.</h1>
 <div class="src" style="position:absolute;left:84px;top:1130px">PIAZZA DEI CAVALIERI DI MALTA · AVENTINO</div>
 ${foot('dark', 'Swipe →<br>@lore.travel')}
</div>` },

{ id: 'feed-02-colosseum', w: 1080, h: 1350, title: 'Secrets of Rome #02: Why the holes?', body: `
<div class="c bone grain">
 <div class="kicker"><span class="dot"></span>Secrets of Rome · Nº 02</div>
 <h1 style="font-size:104px;margin-top:70px">Why is the Colosseum <em>full of holes?</em></h1>
 <svg viewBox="0 0 912 470" style="position:absolute;left:84px;top:640px;width:912px">
  ${[0,1,2,3,4,5].map(i=>`<g transform="translate(${i*152},0)"><path d="M8 470 V190 A68 68 0 0 1 144 190 V470" fill="none" stroke="#14161A" stroke-width="3"/>
  <rect x="0" y="0" width="152" height="470" fill="none" stroke="#14161A" stroke-width="3"/>
  ${[60,110,330,410].map((y,k)=>`<circle cx="${(k%2?118:34)}" cy="${y}" r="${7+(k%3)*2}" fill="#C4623A"/>`).join('')}</g>`).join('')}
  <line x1="0" y1="120" x2="912" y2="120" stroke="#14161A" stroke-width="3"/>
 </svg>
 <p style="position:absolute;left:84px;top:1150px;font-size:30px;line-height:1.35;max-width:760px">Hint: it isn't bullets, and it isn't the weather.</p>
 ${foot('light', 'Answer in caption<br>@lore.travel')}
</div>` },

{ id: 'feed-03-lookup-pantheon', w: 1080, h: 1350, title: 'Look up: Pantheon', body: `
<div class="c night dark grain">
 <svg viewBox="-500 -500 1000 1000" style="position:absolute;left:-60px;top:80px;width:1200px;height:1200px">
  ${[460,400,340,280,220].map((r,i)=>`<circle r="${r}" fill="none" stroke="#B8935A" stroke-opacity="${.55-i*.07}" stroke-width="2"/>`).join('')}
  ${Array.from({length:28},(_,i)=>{const a=i*Math.PI*2/28;return `<line x1="${Math.cos(a)*120}" y1="${Math.sin(a)*120}" x2="${Math.cos(a)*460}" y2="${Math.sin(a)*460}" stroke="#B8935A" stroke-opacity=".35" stroke-width="2"/>`}).join('')}
  <circle r="120" fill="#F3EEE6"/><circle r="120" fill="none" stroke="#C4623A" stroke-width="6"/>
 </svg>
 <div style="position:absolute;left:84px;top:84px" class="kicker"><span class="dot"></span>Look up · Pantheon</div>
 <h1 style="position:absolute;left:84px;bottom:240px;font-size:150px">Look <em>up.</em></h1>
 <p style="position:absolute;left:84px;bottom:180px;font-size:30px;opacity:.85">The only window in the Pantheon is a hole in the sky.</p>
 ${foot('dark', '41.899° N · 12.477° E')}
</div>` },

{ id: 'feed-04-solo-first-night', w: 1080, h: 1350, title: 'Solo safe: First-night routine', body: `
<div class="c olive dark grain">
 <div class="kicker"><span class="dot" style="background:var(--bone)"></span>Solo safe · First Night</div>
 <h1 style="font-size:92px;margin-top:60px">My first-night routine in <em style="color:var(--bone);text-decoration:underline;text-decoration-color:var(--terra);text-underline-offset:12px">any</em> new city.</h1>
 <div style="margin-top:80px;display:grid;gap:34px">
 ${[['01','Walk it in daylight','From my stay to the nearest main square.'],['02','Address offline','Saved in the local language, ready for any taxi.'],['03','One person knows','Live location shared until I’m in for the night.']].map(([n,t,d])=>`
  <div style="display:grid;grid-template-columns:120px 1fr;gap:20px;align-items:start;border-top:2px solid rgba(243,238,230,.25);padding-top:30px">
   <div class="mono" style="font-size:44px;color:var(--bone);opacity:.7">${n}</div>
   <div><div class="serif" style="font-size:52px;line-height:1.05">${t}</div><div style="font-size:28px;opacity:.85;margin-top:10px">${d}</div></div></div>`).join('')}
 </div>
 ${foot('dark', 'Save for your next trip<br>@lore.travel')}
</div>` },

{ id: 'feed-05-fact-card', w: 1080, h: 1350, title: 'Build in public: Our AI can’t invent history', body: `
<div class="c bone grain">
 <div class="kicker"><span class="dot"></span>Building LORE · In public</div>
 <h1 style="font-size:84px;margin-top:56px">Our AI is <em>not allowed</em> to make up history.</h1>
 <div style="margin-top:64px;background:#fff;border:2px solid var(--ink);border-radius:28px;padding:44px 48px;box-shadow:18px 18px 0 var(--terra)" class="mono">
  <div style="display:flex;justify-content:space-between;font-size:22px;opacity:.6;letter-spacing:.1em"><span>FACT CARD</span><span>ROME · #0412 · SAMPLE</span></div>
  <div class="serif" style="font-size:40px;line-height:1.2;margin:26px 0 30px;font-family:Fraunces">“The Stadium of Domitian lies beneath Piazza Navona.”</div>
  ${[['PLACE','Piazza Navona, Rione Parione'],['DATE','c. AD 86'],['SOURCE','Primary/official source (Story team to fill)'],['CHECKED BY','2 reviewers'],['STATUS','✓ VERIFIED']].map(([k,v])=>`<div style="display:grid;grid-template-columns:230px 1fr;font-size:24px;padding:12px 0;border-top:1px dashed #9AA0A6"><span style="opacity:.55">${k}</span><span>${v}</span></div>`).join('')}
 </div>
 ${foot('light', 'Every story. Checked & sourced.')}
</div>` },

{ id: 'feed-06-is-it-true', w: 1080, h: 1350, title: 'Is it true? The Four Rivers myth', body: `
<div class="c terra dark grain">
 <div class="kicker"><span class="dot" style="background:var(--ink)"></span>Is it true? · Piazza Navona</div>
 <h1 style="font-size:96px;margin-top:60px">Bernini’s statue is hiding its eyes from Borromini’s church.</h1>
 <div style="position:absolute;right:70px;top:640px;transform:rotate(-9deg);border:8px solid var(--bone);border-radius:18px;padding:12px 36px" class="mono"><span style="font-size:110px;font-weight:800;letter-spacing:.06em">MYTH</span></div>
 <div style="position:absolute;left:84px;right:84px;top:930px">
  <div style="position:relative;height:4px;background:var(--bone);opacity:.6"></div>
  <div style="display:flex;justify-content:space-between;margin-top:22px" class="mono">
   <div><div style="font-size:52px">1651</div><div style="font-size:22px;opacity:.85">Fountain finished</div></div>
   <div style="text-align:right"><div style="font-size:52px">later</div><div style="font-size:22px;opacity:.85">Church façade completed</div></div></div>
 </div>
 ${foot('dark', 'Great story. Wrong dates.')}
</div>` },

{ id: 'feed-07-navona-stadium', w: 1080, h: 1350, title: 'Secrets of Rome #03: Piazza Navona was a stadium', body: `
<div class="c ink dark grain">
 <div class="kicker"><span class="dot"></span>Secrets of Rome · Nº 03</div>
 <svg viewBox="0 0 400 900" style="position:absolute;right:90px;top:170px;height:1000px">
  <path d="M60 860 V180 A140 140 0 0 1 340 180 V860 Z" fill="none" stroke="#B8935A" stroke-width="6"/>
  <path d="M110 820 V200 A90 90 0 0 1 290 200 V820 Z" fill="#C4623A" fill-opacity=".9"/>
  <circle cx="200" cy="520" r="34" fill="#F3EEE6"/><circle cx="200" cy="300" r="18" fill="#F3EEE6"/><circle cx="200" cy="740" r="18" fill="#F3EEE6"/>
  <text x="200" y="890" fill="#9AA0A6" font-family="JetBrains Mono" font-size="20" text-anchor="middle">N ↑  ~276 m</text>
 </svg>
 <h1 style="position:absolute;left:84px;top:260px;width:560px;font-size:92px">This square is shaped like a running track.</h1>
 <p class="serif" style="position:absolute;left:84px;top:820px;width:540px;font-size:44px;font-style:italic;color:var(--terra)">Because it was one.</p>
 <div class="src" style="position:absolute;left:84px;top:960px;width:540px;line-height:1.6">STADIUM OF DOMITIAN · 1ST CENTURY AD<br>PIAZZA NAVONA, ROMA</div>
 ${foot('dark', '@lore.travel')}
</div>` },

{ id: 'feed-08-which-lore', w: 1080, h: 1350, title: 'Which LORE would you carry?', body: `
<div class="c bone grain">
 <div class="kicker"><span class="dot"></span>Building LORE · Vote</div>
 <h1 style="font-size:96px;margin-top:56px">Which one would you <em>carry?</em></h1>
 <div style="position:absolute;left:84px;right:84px;top:600px;display:grid;grid-template-columns:repeat(3,1fr);gap:28px;align-items:end">
  <div style="text-align:center"><div style="width:210px;height:210px;margin:0 auto;border-radius:44%;background:radial-gradient(circle at 35% 30%,#D98863,#C4623A 55%,#9c4a2a);box-shadow:0 30px 40px rgba(20,22,26,.25);position:relative"><div style="position:absolute;inset:64px;border-radius:50%;border:6px solid rgba(243,238,230,.85);box-shadow:0 0 22px rgba(243,238,230,.6)"></div></div>
   <div class="serif" style="font-size:46px;margin-top:40px">1 · Pebble</div><div class="mono" style="font-size:22px;opacity:.65;margin-top:8px">clip-on · no screen</div></div>
  <div style="text-align:center"><div style="width:240px;height:240px;margin:0 auto;border-radius:56px;background:linear-gradient(145deg,#2a2d33,#14161A);box-shadow:0 30px 40px rgba(20,22,26,.3);display:grid;place-items:center"><div style="width:170px;height:170px;border-radius:40px;background:#000;display:grid;place-items:center;color:#F3EEE6;font-family:Fraunces;font-size:26px;text-align:center;line-height:1.1">Look up<br><span style="font-family:'JetBrains Mono';font-size:14px;color:#C4623A">ON YOUR RIGHT</span></div></div>
   <div class="serif" style="font-size:46px;margin-top:40px">2 · Square</div><div class="mono" style="font-size:22px;opacity:.65;margin-top:8px">screen · global eSIM</div></div>
  <div style="text-align:center"><div style="width:240px;height:240px;margin:0 auto;border-radius:56px;background:linear-gradient(145deg,#d9d9d6,#9AA0A6 60%,#7b8086);box-shadow:0 30px 40px rgba(20,22,26,.3);display:grid;place-items:center;position:relative"><div style="width:170px;height:170px;border-radius:40px;background:#0D1B2A"></div><div style="position:absolute;right:-12px;top:96px;width:16px;height:48px;border-radius:6px;background:#B8935A"></div></div>
   <div class="serif" style="font-size:46px;margin-top:40px">3 · Atlas</div><div class="mono" style="font-size:22px;opacity:.65;margin-top:8px">titanium · satellite SOS</div></div>
 </div>
 <div class="src" style="position:absolute;left:84px;top:1110px">ILLUSTRATION, NOT A PRODUCT RENDER · TARGET PRICES $149 / $299 / $599</div>
 ${foot('light', 'Comment 1, 2 or 3')}
</div>` },

// ---------- STORY / TIKTOK 1080x1920 ----------
{ id: 'story-01-every-street', w: 1080, h: 1920, title: 'Brand: Every street has a story', body: `
<div class="c ink dark grain" style="padding:250px 90px 350px">
 <div style="width:150px">${SYM.terra}</div>
 <h1 style="font-size:150px;margin-top:120px">Every street has a <em>story.</em></h1>
 <p style="font-size:38px;line-height:1.35;margin-top:60px;opacity:.88;max-width:820px">LORE is a pocket-sized travel companion that tells you the stories of the city around you, through your own earphones.</p>
 <div style="margin-top:80px"><span class="pill fill">Join the waitlist · lore.travel</span></div>
 <div style="position:absolute;left:90px;bottom:300px;width:300px">${WORD.bone}</div>
</div>` },

{ id: 'story-02-112', w: 1080, h: 1920, title: 'Solo safe: Save 112', body: `
<div class="c night dark grain" style="padding:250px 90px 350px">
 <div class="kicker"><span class="dot" style="background:var(--signal)"></span>Solo safe · Screenshot this</div>
 <div class="mono" style="font-size:420px;font-weight:700;line-height:1;margin-top:120px;letter-spacing:-.04em;color:var(--bone)">112</div>
 <h1 style="font-size:88px;margin-top:40px">The EU-wide emergency number.</h1>
 <p style="font-size:38px;line-height:1.4;margin-top:40px;opacity:.85">Free from any phone, anywhere in the EU. Save it before you land.</p>
 <div class="src" style="position:absolute;left:90px;bottom:380px">SOURCE: EUROPEAN COMMISSION · 112 EMERGENCY NUMBER</div>
 <div style="position:absolute;left:90px;bottom:300px;width:220px">${WORD.bone}</div>
</div>` },

{ id: 'story-03-pasquino', w: 1080, h: 1920, title: 'TikTok cover: Pasquino, the talking statue', body: `
<div class="c bone grain" style="padding:250px 90px 350px">
 <div class="kicker"><span class="dot"></span>Secrets of Rome · Nº 07</div>
 <svg viewBox="0 0 600 700" style="position:absolute;right:-60px;top:1000px;width:620px">
  <rect x="160" y="560" width="300" height="140" fill="#D2CEC7"/><rect x="140" y="540" width="340" height="30" fill="#B0ADA9"/>
  <path d="M220 540 C200 420 230 330 300 300 C380 270 430 330 420 420 C415 480 400 520 380 540 Z" fill="#B0ADA9"/>
  <circle cx="330" cy="250" r="70" fill="#B0ADA9"/>
  ${[[60,140,-8],[40,260,6],[90,380,-4],[430,120,9]].map(([x,y,r])=>`<g transform="translate(${x},${y}) rotate(${r})"><rect width="150" height="96" fill="#fff" stroke="#14161A" stroke-width="2"/><line x1="16" y1="26" x2="134" y2="26" stroke="#14161A" stroke-width="3"/><line x1="16" y1="46" x2="120" y2="46" stroke="#14161A" stroke-width="3"/><line x1="16" y1="66" x2="128" y2="66" stroke="#C4623A" stroke-width="3"/></g>`).join('')}
 </svg>
 <h1 style="font-size:116px;margin-top:80px;max-width:860px">Rome has a statue that’s been posting <em>anonymous insults</em> since the 1500s.</h1>
 <div style="position:absolute;left:90px;bottom:300px;width:220px">${WORD.ink}</div>
</div>` },

{ id: 'story-04-lookup-challenge', w: 1080, h: 1920, title: '#LookUpChallenge', body: `
<div class="c terra dark grain" style="padding:250px 90px 350px">
 <div class="kicker"><span class="dot" style="background:var(--ink)"></span>New challenge</div>
 <div style="position:absolute;right:90px;top:520px;width:300px;height:300px;border:6px solid var(--bone);border-radius:50%;display:grid;place-items:center"><div class="serif" style="font-size:160px;line-height:1">↑</div></div>
 <h1 style="font-size:170px;margin-top:640px">#LookUp<br>Challenge</h1>
 <p style="font-size:40px;line-height:1.4;margin-top:50px;max-width:860px">In any city: stop, look up for 10 seconds, film what you missed. Tag <b>@lore.travel</b> and we’ll tell you its story, if we can verify it.</p>
 <div style="position:absolute;left:90px;bottom:300px;width:220px">${WORD.bone}</div>
</div>` },

{ id: 'story-05-kickstarter', w: 1080, h: 1920, title: 'Kickstarter launch date (Stage 2)', body: `
<div class="c bone grain" style="padding:250px 90px 350px">
 <div class="kicker"><span class="dot"></span>Launching on Kickstarter</div>
 <div class="mono" style="margin-top:110px;font-size:150px;line-height:1;font-weight:600;letter-spacing:-.03em">25·05<br><span style="color:var(--link)">2027</span></div>
 <h1 style="font-size:100px;margin-top:80px">Waitlist gets first access and up to <em>34% off.</em></h1>
 <div style="margin-top:70px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px" class="mono">
  ${[['$99','PEBBLE'],['$199','SQUARE'],['$399','ATLAS']].map(([p,n])=>`<div style="border:2px solid var(--ink);border-radius:20px;padding:24px;text-align:center"><div style="font-size:52px">${p}</div><div style="font-size:20px;opacity:.6;margin-top:8px">${n} · FROM</div></div>`).join('')}
 </div>
 <div style="margin-top:60px"><span class="pill fill">Reserve your spot · lore.travel</span></div>
 <div class="src" style="position:absolute;left:90px;bottom:380px">PLANNED DATE & PRICES · SUBJECT TO CHANGE</div>
 <div style="position:absolute;left:90px;bottom:300px;width:220px">${WORD.ink}</div>
</div>` },

{ id: 'story-06-map-vision', w: 1080, h: 1920, title: 'Map Vision explainer', body: `
<div class="c night dark grain" style="padding:250px 90px 350px">
 <div class="kicker"><span class="dot"></span>How LORE sees · Map Vision</div>
 <h1 style="font-size:104px;margin-top:70px">No camera. It still knows what’s on your <em>left.</em></h1>
 <svg viewBox="0 0 900 760" style="position:absolute;left:130px;top:760px;width:820px">
  <rect x="0" y="0" width="300" height="760" fill="#13263A" stroke="#B8935A" stroke-width="2"/><rect x="600" y="0" width="300" height="760" fill="#13263A" stroke="#B8935A" stroke-width="2"/>
  <rect x="40" y="60" width="220" height="200" fill="none" stroke="#B8935A" stroke-opacity=".5" stroke-dasharray="6 6"/><rect x="640" y="300" width="220" height="260" fill="none" stroke="#B8935A" stroke-opacity=".5" stroke-dasharray="6 6"/>
  ${[1,2,3].map(r=>`<circle cx="450" cy="520" r="${r*60}" fill="none" stroke="#C4623A" stroke-opacity="${.6-r*.15}" stroke-width="3"/>`).join('')}
  <circle cx="450" cy="520" r="22" fill="#C4623A"/><path d="M450 420 L475 480 L425 480Z" fill="#F3EEE6"/>
  <text x="150" y="420" fill="#F3EEE6" font-family="JetBrains Mono" font-size="34" text-anchor="middle">← LEFT</text>
  <text x="750" y="250" fill="#F3EEE6" font-family="JetBrains Mono" font-size="34" text-anchor="middle">RIGHT →</text>
  <text x="450" y="80" fill="#F3EEE6" font-family="JetBrains Mono" font-size="34" text-anchor="middle">↑ AHEAD</text>
  <text x="750" y="660" fill="#C4623A" font-family="JetBrains Mono" font-size="30" text-anchor="middle">LOOK UP ⤒</text>
 </svg>
 <div class="mono" style="position:absolute;left:90px;bottom:380px;font-size:24px;opacity:.75;line-height:1.6">L1+L5 GNSS · 9-AXIS IMU · COMPASS · STEPS · BUILDING FOOTPRINTS</div>
 <div style="position:absolute;right:90px;bottom:300px;width:220px">${WORD.bone}</div>
</div>` },
];
