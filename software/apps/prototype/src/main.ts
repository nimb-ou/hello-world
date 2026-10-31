/**
 * LORE prototype PWA. Runs fully offline in a phone browser:
 * Geolocation + DeviceOrientation -> HeadingKalman -> StoryEngine -> narration -> speechSynthesis.
 * SIMULATION MODE replays the Pantheon -> Trevi route so it can be demoed from anywhere.
 *
 * URL params: ?sim=1 (start simulation), &speed=10, &mute=1, &backend=http://localhost:8787, &persona=storyteller
 */
import {
  DEMO_ROUTES, HeadingKalman, PERSONAS, StoryEngine, bearing, directionTo, haversine, interpolateAlong, pathLength,
  templateNarration, angleDiff, type CityPack, type Decision, type EngineContext, type InterestProfile, type NarrationScript,
  type NarrateDecision, type Persona,
} from "../../../packages/core/src/index.ts";

const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;
const params = new URLSearchParams(location.search);
const muted = params.get("mute") === "1";
const backend = params.get("backend") ?? "http://localhost:8787";
const CITIES: Record<string, string> = { rome: "Rome", mumbai: "Mumbai" };
const city = params.get("city") && CITIES[params.get("city")!] ? params.get("city")! : "rome";

const INTERESTS: { id: string; label: string; tags?: string[]; categories?: string[] }[] = [
  { id: "ancient", label: "Ancient Rome", tags: ["ancient-rome", "julius-caesar", "augustus"] },
  { id: "art", label: "Art & Baroque", tags: ["baroque", "bernini", "borromini", "caravaggio", "art", "renaissance", "michelangelo", "raphael"] },
  { id: "film", label: "Film & opera", tags: ["film", "fellini", "opera"] },
  { id: "hidden", label: "Hidden gems", tags: ["hidden-gem", "talking-statues", "satire"] },
  { id: "legends", label: "Legends", tags: ["legend"] },
  { id: "churches", label: "Churches", categories: ["church"] },
  { id: "views", label: "Views", tags: ["viewpoint", "sunset"] },
];

const state = {
  pack: null as CityPack | null,
  engine: null as StoryEngine | null,
  kf: new HeadingKalman(),
  persona: (params.get("persona") as Persona) || "local-friend",
  interests: new Set<string>(["ancient", "art", "hidden"]),
  mode: "idle" as "idle" | "live" | "sim",
  quiet: false,
  pos: null as { lat: number; lng: number } | null,
  accuracy: 99,
  speed: 0,
  heading: null as number | null,
  headingConf: "low" as "high" | "medium" | "low",
  simT: 0,
  simAlong: 0,
  simTimer: 0 as unknown as ReturnType<typeof setInterval>,
  liveTimer: 0 as unknown as ReturnType<typeof setInterval>,
  speaking: null as { script: NarrationScript; startT: number } | null,
  crossing: false,
};

function now(): number {
  return state.mode === "sim" ? state.simT : Date.now();
}

function profile(): InterestProfile {
  const tags: Record<string, number> = {};
  const categories: Record<string, number> = {};
  for (const i of INTERESTS) {
    if (!state.interests.has(i.id)) continue;
    i.tags?.forEach((t) => (tags[t] = 1.6));
    i.categories?.forEach((c) => (categories[c] = 1.5));
  }
  return { tags, categories };
}

async function loadPack(): Promise<CityPack> {
  const res = await fetch(`./packs/${city}.pack.json`);
  if (!res.ok) throw new Error(`pack load failed: ${res.status}`);
  return res.json();
}

// ---------- speech ----------
function speak(script: NarrationScript, onEnd: () => void) {
  const simSpeed = Number(($("simSpeed") as HTMLSelectElement).value);
  const synth = "speechSynthesis" in window ? window.speechSynthesis : null;
  const realTTS = !muted && synth && !(state.mode === "sim" && simSpeed > 1);
  if (realTTS) {
    synth!.cancel();
    const u = new SpeechSynthesisUtterance(script.speechText);
    u.lang = "en-GB";
    u.rate = PERSONAS[script.persona].wpm / 165;
    u.onend = onEnd;
    u.onerror = onEnd;
    synth!.speak(u);
  } else {
    // Timer-based fallback (headless, muted, or sped-up simulation): advance in engine time.
    const endAt = now() + script.estimatedSec * 1000;
    const check = setInterval(() => {
      if (now() >= endAt || !state.speaking) {
        clearInterval(check);
        onEnd();
      }
    }, 100);
  }
}

function stopSpeech() {
  if ("speechSynthesis" in window) window.speechSynthesis.cancel();
  state.speaking = null;
}

async function narrate(d: NarrateDecision) {
  const input = { poi: d.poi, facts: d.facts, tier: d.tier, persona: state.persona, direction: d.direction, directionReliable: d.directionReliable, live: d.live, followUp: d.reason === "proximity" ? undefined : d.reason } as const;
  let script = templateNarration(input);
  if (($("cloud") as HTMLInputElement).checked) {
    try {
      const r = await fetch(`${backend}/narrate`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ poi_id: d.poi.id, fact_ids: d.facts.map((f) => f.id), persona: state.persona, tier: d.tier, direction: d.directionReliable ? d.direction.direction : null, distance_m: d.direction.distanceM, follow_up: input.followUp }),
        signal: AbortSignal.timeout(6000),
      });
      if (r.ok) script = (await r.json()).script as NarrationScript;
    } catch {
      /* offline: keep template */
    }
  }
  state.speaking = { script, startT: now() };
  renderNow(d, script);
  speak(script, () => {
    state.engine?.onSpeechEnd(now());
    state.speaking = null;
  });
}

// ---------- engine tick ----------
function context(): EngineContext | null {
  if (!state.pos) return null;
  return { t: now(), position: state.pos, accuracyM: state.accuracy, heading: state.heading, headingConfidence: state.headingConf, speedMps: state.speed, crossingRoad: state.crossing };
}

function handle(d: Decision) {
  if (d.kind === "narrate") void narrate(d);
  else $("state").textContent = d.reason + (d.deferred ? " (queued)" : "");
}

function tick() {
  const ctx = context();
  if (!ctx || !state.engine) return;
  renderSensors();
  renderRadar();
  renderProgress();
  if (state.quiet) {
    $("state").textContent = "quiet";
    return;
  }
  handle(state.engine.update(ctx));
}

// ---------- live sensors ----------
function startLive() {
  stopSim();
  state.mode = "live";
  $("modeChip").textContent = "LIVE";
  $("modeChip").classList.remove("sim");
  if (!("geolocation" in navigator)) {
    $("narration").textContent = "Geolocation is not available in this browser. Try the simulated walk.";
    return;
  }
  navigator.geolocation.watchPosition(
    (p) => {
      state.pos = { lat: p.coords.latitude, lng: p.coords.longitude };
      state.accuracy = p.coords.accuracy;
      state.speed = p.coords.speed ?? 0;
      state.kf.gps({ t: Date.now(), courseDeg: p.coords.heading ?? null, speedMps: state.speed, accuracyM: p.coords.accuracy });
    },
    (e) => ($("narration").textContent = `Location error: ${e.message}`),
    { enableHighAccuracy: true, maximumAge: 1000 },
  );
  const onOrient = (e: DeviceOrientationEvent & { webkitCompassHeading?: number; webkitCompassAccuracy?: number }) => {
    const h = e.webkitCompassHeading ?? (e.absolute && e.alpha !== null ? (360 - e.alpha) % 360 : null);
    if (h === null) return;
    state.kf.compass({ t: Date.now(), headingDeg: h, accuracyDeg: e.webkitCompassAccuracy });
    const est = state.kf.estimate();
    state.heading = est.headingDeg;
    state.headingConf = est.confidence;
  };
  const D = DeviceOrientationEvent as unknown as { requestPermission?: () => Promise<string> };
  const attach = () => {
    window.addEventListener("deviceorientationabsolute", onOrient as EventListener);
    window.addEventListener("deviceorientation", onOrient as EventListener);
  };
  if (typeof D.requestPermission === "function") D.requestPermission().then((r) => r === "granted" && attach()).catch(() => {});
  else attach();
  clearInterval(state.liveTimer);
  state.liveTimer = setInterval(tick, 1000);
}

// ---------- simulation ----------
const route = DEMO_ROUTES[city];
const routeLen = pathLength(route.path);
let simRand = 7;
const rnd = () => ((simRand = (simRand * 1664525 + 1013904223) >>> 0) / 2 ** 32);

function startSim() {
  clearInterval(state.liveTimer);
  stopSpeech();
  state.mode = "sim";
  state.simT = 1_000_000;
  state.simAlong = 0;
  state.kf = new HeadingKalman();
  state.engine = new StoryEngine(state.pack!.pois);
  state.engine.setProfile(profile());
  $("modeChip").textContent = "SIMULATION";
  $("modeChip").classList.add("sim");
  $("btnSim").textContent = "Restart simulated walk";
  const stops = route.stops.map((s) => ({ ...s, left: s.seconds }));
  const step = () => {
    state.simT += 1000;
    const stop = stops.find((s) => state.simAlong >= s.atM && s.left > 0);
    const v = stop ? 0 : 1.3;
    if (stop) stop.left--;
    state.simAlong = Math.min(routeLen, state.simAlong + v);
    const at = interpolateAlong(route.path, state.simAlong);
    state.pos = at.pos;
    state.accuracy = 4;
    state.speed = v;
    const t = state.simT;
    state.kf.compass({ t, headingDeg: at.heading + (rnd() - 0.5) * 14, fieldUT: 46 });
    state.kf.gps({ t, courseDeg: v > 0 ? at.heading + (rnd() - 0.5) * 10 : null, speedMps: v, accuracyM: 4 });
    const est = state.kf.estimate(t);
    state.heading = est.headingDeg;
    state.headingConf = est.confidence;
    state.crossing = route.crossings.some((c) => haversine(at.pos, c.at) < c.radiusM);
    tick();
    if (at.done) {
      stopSim();
      $("simLabel").textContent = `Arrived: ${[...route.path].reverse().find((p) => p.label)?.label}. Simulation complete.`;
    }
  };
  clearInterval(state.simTimer);
  const speed = Number(($("simSpeed") as HTMLSelectElement).value);
  state.simTimer = setInterval(step, 1000 / speed);
  step();
}

function stopSim() {
  clearInterval(state.simTimer);
}

// ---------- rendering ----------
function dirLabel(d: NarrateDecision): string {
  if (!d.directionReliable) return "Nearby";
  const arrows = { ahead: "↑ Ahead", left: "← Left", right: "Right →", behind: "↓ Behind" } as const;
  return arrows[d.direction.direction] + (d.direction.lookUp ? " · look up" : "");
}

function renderNow(d: NarrateDecision, s: NarrationScript) {
  $("poiName").textContent = d.poi.name;
  const badge = $("dirBadge");
  badge.textContent = dirLabel(d);
  badge.classList.toggle("lookup", d.direction.lookUp);
  $("distance").textContent = `${Math.round(d.direction.distanceM)} m · ${d.tier === "short" ? "20 s" : d.tier === "medium" ? "40 s" : "deep dive"}${s.mode === "llm" ? " · cloud" : ""}`;
  $("narration").textContent = s.speechText;
  $("sources").innerHTML = "";
  s.sources.forEach((src) => {
    const a = document.createElement("a");
    a.href = src.url;
    a.target = "_blank";
    a.rel = "noopener";
    a.textContent = src.title.replace(/^Wikipedia \(en\): /, "Source: ");
    $("sources").appendChild(a);
  });
  $("state").textContent = "speaking";
}

function renderSensors() {
  $("heading").textContent = state.heading === null ? "-" : `${Math.round(state.heading)}° ${state.headingConf}`;
  $("gps").textContent = state.pos ? `±${Math.round(state.accuracy)} m ${state.speed.toFixed(1)} m/s` : "-";
  if (state.crossing) $("state").textContent = "crossing road";
}

function renderRadar() {
  const svg = $("radar") as unknown as SVGSVGElement;
  if (!state.pos || !state.pack) return;
  const R = 200; // metres at the edge
  const h = state.heading ?? 0;
  let out = `<circle r="96" fill="none" stroke="currentColor" stroke-opacity=".12"/><circle r="48" fill="none" stroke="currentColor" stroke-opacity=".12"/>`;
  out += `<path d="M0 0 L-34 -90 A96 96 0 0 1 34 -90 Z" fill="#B8935A" fill-opacity=".14"/>`;
  const told = new Set(state.engine?.exportState().spokenFactIds ?? []);
  for (const p of state.pack.pois) {
    const d = haversine(state.pos, p);
    if (d > R) continue;
    const rel = angleDiff(h, bearing(state.pos, p)) * (Math.PI / 180);
    const r = (d / R) * 92;
    const x = Math.sin(rel) * r;
    const y = -Math.cos(rel) * r;
    const fresh = p.facts.some((f) => !told.has(f.id));
    const isNow = state.speaking && state.engine?.lastPoi?.id === p.id;
    out += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${isNow ? 6 : 3.5}" fill="${isNow ? "#C4623A" : fresh ? "#B8935A" : "#9AA0A6"}"><title>${p.name}</title></circle>`;
  }
  out += `<path d="M0 -8 L6 6 L0 3 L-6 6 Z" fill="currentColor"/>`;
  out += `<text y="-100" text-anchor="middle" font-size="9" fill="currentColor" opacity=".5" dy="9">facing</text>`;
  svg.innerHTML = out;
}

function renderProgress() {
  if (state.mode !== "sim") return;
  const pct = (state.simAlong / routeLen) * 100;
  $("simBar").style.width = `${pct.toFixed(1)}%`;
  const at = interpolateAlong(route.path, state.simAlong);
  const label = [...route.path.slice(0, at.segment + 1)].reverse().find((p) => p.label)?.label ?? "";
  $("simLabel").textContent = `${Math.round(state.simAlong)} / ${Math.round(routeLen)} m · near ${label}`;
}

function renderAround() {
  const ctx = context();
  const box = $("around");
  if (!ctx || !state.engine) {
    box.hidden = false;
    box.innerHTML = `<div class="item"><b>No location yet</b><span>Start a walk first</span></div>`;
    return;
  }
  const list = state.engine.whatsAroundMe(ctx, 5);
  box.hidden = false;
  box.innerHTML = list
    .map((c) => {
      const dd = directionTo(ctx.position, ctx.heading ?? 0, c.poi);
      const dir = ctx.headingConfidence === "low" ? "nearby" : dd.direction;
      return `<div class="item"><b>${c.poi.name}</b><span>${dir} · ${Math.round(c.distanceM)} m</span></div>`;
    })
    .join("");
  const names = list.slice(0, 3).map((c) => `${c.poi.name}, ${ctx.headingConfidence === "low" ? "nearby" : directionTo(ctx.position, ctx.heading ?? 0, c.poi).direction}`);
  if (names.length && !muted && "speechSynthesis" in window && state.mode !== "sim") {
    window.speechSynthesis.speak(new SpeechSynthesisUtterance(`Around you: ${names.join("; ")}.`));
  }
}

function renderControls() {
  const ib = $("interests");
  ib.innerHTML = "";
  for (const i of INTERESTS) {
    const b = document.createElement("button");
    b.textContent = i.label;
    b.setAttribute("aria-pressed", String(state.interests.has(i.id)));
    b.onclick = () => {
      state.interests.has(i.id) ? state.interests.delete(i.id) : state.interests.add(i.id);
      state.engine?.setProfile(profile());
      renderControls();
    };
    ib.appendChild(b);
  }
  const pb = $("personas");
  pb.innerHTML = "";
  for (const [id, p] of Object.entries(PERSONAS)) {
    const b = document.createElement("button");
    b.textContent = p.label;
    b.title = p.description;
    b.setAttribute("aria-pressed", String(state.persona === id));
    b.onclick = () => {
      state.persona = id as Persona;
      renderControls();
    };
    pb.appendChild(b);
  }
}

// ---------- boot ----------
async function boot() {
  const sel = $("citySel") as HTMLSelectElement;
  sel.value = city;
  sel.onchange = () => {
    const q = new URLSearchParams(location.search);
    q.set("city", sel.value);
    location.search = q.toString();
  };
  document.title = `LORE ${CITIES[city]}`;
  renderControls();
  try {
    state.pack = await loadPack();
  } catch (e) {
    $("narration").textContent = String(e);
    return;
  }
  state.engine = new StoryEngine(state.pack.pois);
  state.engine.setProfile(profile());
  $("simLabel").textContent = `${route.name} · ${(routeLen / 1000).toFixed(1)} km · ${state.pack.pois.length} places in pack`;

  $("btnSim").onclick = startSim;
  $("btnLive").onclick = startLive;
  $("btnMore").onclick = () => {
    const ctx = context();
    if (!ctx || !state.engine) return;
    stopSpeech();
    state.quiet = false;
    $("btnQuiet").setAttribute("aria-pressed", "false");
    handle(state.engine.tellMeMore(ctx));
  };
  $("btnAround").onclick = renderAround;
  $("btnQuiet").onclick = () => {
    state.quiet = !state.quiet;
    $("btnQuiet").setAttribute("aria-pressed", String(state.quiet));
    if (state.quiet) {
      stopSpeech();
      state.engine?.quiet(now());
    } else state.engine?.resume(now());
  };
  if ("serviceWorker" in navigator && location.protocol !== "file:" && !params.has("nosw")) navigator.serviceWorker.register("./sw.js").catch(() => {});
  if (params.get("sim") === "1") {
    const sp = params.get("speed");
    if (sp) ($("simSpeed") as HTMLSelectElement).value = sp;
    startSim();
  }
}

(window as unknown as { __lore: typeof state }).__lore = state; // test hook (screenshots / e2e)
void boot();
