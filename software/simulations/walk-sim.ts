/**
 * Headless walk simulation: runs Map Vision (heading fusion) + Story Engine + Narration along the
 * Rome demo route with SIMULATED sensors, and writes a transcript + metrics.
 *
 *   npm run sim                      # default seed, persona local-friend
 *   npx tsx simulations/walk-sim.ts --seed 7 --persona storyteller
 *
 * All sensor data here is simulated (labelled as such in the output).
 */
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  HeadingKalman, ROME_DEMO_ROUTE, StoryEngine, destinationPoint, directionTo, haversine, interpolateAlong, pathLength,
  templateNarration, type CityPack, type DemoRoute, type Persona,
} from "../packages/core/src/index.ts";

const here = dirname(fileURLToPath(import.meta.url));

export interface SimOptions {
  seed?: number;
  persona?: Persona;
  walkSpeedMps?: number;
  route?: DemoRoute;
  /** Distances (m along route) where the simulated user presses "tell me more". */
  tellMeMoreAtM?: number[];
}

export interface TranscriptEntry {
  t: number;
  alongM: number;
  poi: string;
  poiId: string;
  reason: string;
  tier: string;
  direction: string;
  trueDirection: string;
  distanceM: number;
  lookUp: boolean;
  speech: string;
  factIds: string[];
  sources: string[];
  durationSec: number;
}

export interface SimMetrics {
  simulated: true;
  routeKm: number;
  durationMin: number;
  narrations: number;
  narrationsPerKm: number;
  factsSpoken: number;
  factRepeatRate: number;
  poiRepeatRate: number;
  speakingShare: number;
  quiet: { quietSeconds: number; narrationStartsDuringQuiet: number; compliance: number; ongoingSpeechOverlapSec: number };
  directionAccuracy: number;
  headingErrorDeg: { mean: number; p95: number };
  silenceReasons: Record<string, number>;
}

function rng(seed: number) {
  let s = seed >>> 0 || 1;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
}

export function loadPack(): CityPack {
  return JSON.parse(readFileSync(join(here, "../city-pack/output/rome.pack.json"), "utf8"));
}

export function runWalk(pack: CityPack, opts: SimOptions = {}) {
  const route = opts.route ?? ROME_DEMO_ROUTE;
  const persona = opts.persona ?? "local-friend";
  const speed = opts.walkSpeedMps ?? 1.3;
  const r = rng(opts.seed ?? 42);
  const g = () => Math.sqrt(-2 * Math.log(r() + 1e-12)) * Math.cos(2 * Math.PI * r());
  const total = pathLength(route.path);
  const engine = new StoryEngine(pack.pois);
  const kf = new HeadingKalman();
  const tellAt = [...(opts.tellMeMoreAtM ?? [335, 1185])];
  const stops = route.stops.map((s) => ({ ...s, remaining: s.seconds, done: false }));
  const transcript: TranscriptEntry[] = [];
  const silence: Record<string, number> = {};
  const headingErrs: number[] = [];
  let along = 0;
  let t = 0;
  let speakingUntil = 0;
  let speakingSec = 0;
  let quietSeconds = 0;
  let startsDuringQuiet = 0;
  let overlap = 0;
  let dirChecks = 0;
  let dirCorrect = 0;
  const COMPASS_BIAS = 7; // simulated hard-iron offset (deg)

  while (along < total) {
    t += 1000;
    // --- motion model (simulated) ---
    const stop = stops.find((s) => !s.done && along >= s.atM);
    let v = speed * (0.9 + 0.2 * r());
    if (stop) {
      v = 0;
      if (--stop.remaining <= 0) stop.done = true;
    }
    along += v;
    const truth = interpolateAlong(route.path, along);
    const trueHeading = truth.heading;
    // --- simulated sensors ---
    const gpsPos = destinationPoint(truth.pos, r() * 360, Math.abs(g()) * 4);
    const nearCorso = haversine(truth.pos, { lat: 41.9003, lng: 12.4808 }) < 40; // trams/buses: magnetic disturbance
    for (let k = 0; k < 5; k++) {
      const tt = t - 1000 + k * 200;
      kf.gyro({ t: tt, yawRateDps: g() * 2 });
      kf.compass({ t: tt, headingDeg: trueHeading + COMPASS_BIAS + g() * 9 + (nearCorso ? 60 : 0), fieldUT: nearCorso ? 71 : 46 + g() * 2 });
    }
    kf.gps({ t, courseDeg: v > 0.5 ? trueHeading + g() * 8 : null, speedMps: v, accuracyM: 4 });
    if (v > 0.5) kf.step({ t, directionDeg: trueHeading + g() * 14, quality: 0.75 });
    const est = kf.estimate(t);
    headingErrs.push(Math.abs(((est.headingDeg - trueHeading + 540) % 360) - 180));

    const crossing = route.crossings.some((c) => haversine(truth.pos, c.at) < c.radiusM);
    const talking = route.talkingWindowsM.some(([a, b]) => along >= a && along <= b);
    const quietNow = crossing || talking;
    if (quietNow) quietSeconds++;
    if (quietNow && t < speakingUntil) overlap++;
    if (t < speakingUntil) speakingSec++;

    const ctx = { t, position: gpsPos, accuracyM: 4, heading: est.headingDeg, headingConfidence: est.confidence, speedMps: v, crossingRoad: crossing, userTalking: talking };
    let d;
    if (tellAt.length && along >= tellAt[0]) {
      tellAt.shift();
      d = engine.tellMeMore(ctx);
    } else d = engine.update(ctx);

    if (d.kind === "silent") {
      silence[d.reason] = (silence[d.reason] ?? 0) + 1;
      continue;
    }
    if (quietNow) startsDuringQuiet++;
    const script = templateNarration({ poi: d.poi, facts: d.facts, tier: d.tier, persona, direction: d.direction, directionReliable: d.directionReliable, live: d.live, followUp: d.reason === "proximity" ? undefined : d.reason });
    const trueDir = directionTo(truth.pos, trueHeading, d.poi);
    dirChecks++;
    if (trueDir.direction === d.direction.direction || d.direction.distanceM < 25) dirCorrect++;
    speakingUntil = t + script.estimatedSec * 1000;
    engine.onSpeechEnd(speakingUntil);
    transcript.push({
      t, alongM: Math.round(along), poi: d.poi.name, poiId: d.poi.id, reason: d.reason, tier: d.tier,
      direction: d.directionReliable ? d.direction.direction : "nearby", trueDirection: trueDir.direction,
      distanceM: Math.round(d.direction.distanceM), lookUp: d.direction.lookUp, speech: script.speechText,
      factIds: script.factIds, sources: script.sources.map((s) => s.url), durationSec: script.estimatedSec,
    });
  }

  const allFacts = transcript.flatMap((e) => e.factIds);
  const pois = transcript.filter((e) => e.reason === "proximity").map((e) => e.poiId);
  const sorted = [...headingErrs].sort((a, b) => a - b);
  const metrics: SimMetrics = {
    simulated: true,
    routeKm: +(total / 1000).toFixed(2),
    durationMin: +(t / 60000).toFixed(1),
    narrations: transcript.length,
    narrationsPerKm: +(transcript.length / (total / 1000)).toFixed(1),
    factsSpoken: allFacts.length,
    factRepeatRate: allFacts.length ? +(1 - new Set(allFacts).size / allFacts.length).toFixed(3) : 0,
    poiRepeatRate: pois.length ? +(1 - new Set(pois).size / pois.length).toFixed(3) : 0,
    speakingShare: +(speakingSec / (t / 1000)).toFixed(2),
    quiet: {
      quietSeconds,
      narrationStartsDuringQuiet: startsDuringQuiet,
      compliance: transcript.length ? +(1 - startsDuringQuiet / transcript.length).toFixed(3) : 1,
      ongoingSpeechOverlapSec: overlap,
    },
    directionAccuracy: dirChecks ? +(dirCorrect / dirChecks).toFixed(3) : 1,
    headingErrorDeg: { mean: +(headingErrs.reduce((a, b) => a + b, 0) / headingErrs.length).toFixed(1), p95: +sorted[Math.floor(sorted.length * 0.95)].toFixed(1) },
    silenceReasons: silence,
  };
  return { transcript, metrics, route, persona };
}

function fmt(ms: number) {
  const s = Math.round(ms / 1000);
  return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
}

export function toMarkdown(res: ReturnType<typeof runWalk>, seed: number): string {
  const m = res.metrics;
  const lines = [
    `# LORE walk simulation: ${res.route.name}`,
    "",
    "> **SIMULATED DATA.** GNSS, compass, gyro and step signals are synthetic (seeded noise, a 7 deg compass bias, magnetic disturbance near Via del Corso). Narration uses the offline deterministic template path from verified City Pack fact cards. Regenerate with `npm run sim`.",
    "",
    `Persona: **${res.persona}**, seed ${seed}. Route ${m.routeKm} km, ${m.durationMin} min including stops.`,
    "",
    "## Metrics",
    "",
    "| Metric | Value |",
    "|---|---|",
    `| Narrations | ${m.narrations} (${m.narrationsPerKm} per km) |`,
    `| Facts spoken | ${m.factsSpoken} |`,
    `| Fact repeat rate | ${(m.factRepeatRate * 100).toFixed(1)} % |`,
    `| POI repeat rate (proximity triggers) | ${(m.poiRepeatRate * 100).toFixed(1)} % |`,
    `| Share of time speaking | ${(m.speakingShare * 100).toFixed(0)} % |`,
    `| Quiet-moment compliance (no story starts while crossing/talking) | ${(m.quiet.compliance * 100).toFixed(1)} % (${m.quiet.narrationStartsDuringQuiet} violations, ${m.quiet.quietSeconds} s of quiet moments) |`,
    `| Ongoing speech overlapping a quiet moment (device ducks audio) | ${m.quiet.ongoingSpeechOverlapSec} s |`,
    `| Left/right/ahead/behind accuracy vs ground truth | ${(m.directionAccuracy * 100).toFixed(0)} % |`,
    `| Fused heading error | mean ${m.headingErrorDeg.mean} deg, p95 ${m.headingErrorDeg.p95} deg |`,
    `| Silent ticks by reason | ${Object.entries(m.silenceReasons).map(([k, v]) => `${k}: ${v}`).join(", ")} |`,
    "",
    "## Transcript",
    "",
  ];
  for (const e of res.transcript) {
    lines.push(`### ${fmt(e.t)} | ${e.alongM} m | ${e.poi}`);
    lines.push("");
    lines.push(`*${e.reason}, ${e.tier} tier, ~${e.durationSec} s. Said: **${e.direction}**${e.lookUp ? " + look up" : ""} (ground truth: ${e.trueDirection}), ${e.distanceM} m away.*`);
    lines.push("");
    lines.push(`> ${e.speech}`);
    lines.push("");
    lines.push(`Facts: ${e.factIds.join(", ")}. Sources: ${e.sources.join(", ")}`);
    lines.push("");
  }
  return lines.join("\n");
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (isMain) {
  const args = process.argv.slice(2);
  const arg = (k: string) => {
    const i = args.indexOf(k);
    return i >= 0 ? args[i + 1] : undefined;
  };
  const seed = Number(arg("--seed") ?? 42);
  const persona = (arg("--persona") ?? "local-friend") as Persona;
  const res = runWalk(loadPack(), { seed, persona });
  const out = join(here, "output");
  mkdirSync(out, { recursive: true });
  writeFileSync(join(out, "rome-walk-transcript.md"), toMarkdown(res, seed));
  writeFileSync(join(out, "rome-walk-metrics.json"), JSON.stringify(res.metrics, null, 2));
  console.log(JSON.stringify(res.metrics, null, 2));
  console.log(`transcript -> ${join(out, "rome-walk-transcript.md")}`);
}
