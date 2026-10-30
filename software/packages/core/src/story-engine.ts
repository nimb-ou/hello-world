/**
 * Story Engine: decides WHAT to narrate, WHEN, and HOW LONG.
 *
 * Inputs per tick: fused position + heading (with confidence), speed, and safety context
 * (crossing a road, user talking). Output: a Decision - either "narrate this POI with
 * these fact cards at this tier" or "stay silent because <reason>".
 *
 * Design rules (from COMPANY.md):
 *  - Only verified fact cards are ever selected (narration.ts turns them into words).
 *  - Never repeat a fact card to the same user (novelty is tracked per fact, persisted).
 *  - Stay quiet while crossing roads, moving fast, or while the user is talking.
 *  - 20 s / 40 s stories by default; "tell me more" goes deeper (deep tier) and chains.
 */
import { directionTo, haversine, type DirectionClassification } from "./geo.ts";
import type { FactCard, LatLng, LiveInfo, Poi, PoiCategory, StoryTier } from "./types.ts";

export interface EngineContext {
  /** epoch ms (or simulation ms) */
  t: number;
  position: LatLng;
  /** GNSS horizontal accuracy (m). */
  accuracyM?: number;
  /** Fused body heading; null if unknown. */
  heading: number | null;
  headingConfidence?: "high" | "medium" | "low";
  speedMps: number;
  /** From Navigation/Safety service: user is on/near a crossing. */
  crossingRoad?: boolean;
  /** From voice activity detection: user (or someone with them) is talking. */
  userTalking?: boolean;
}

export interface InterestProfile {
  /** Multipliers per category; 1 = neutral, 0 = never, 2 = loves it. */
  categories?: Partial<Record<PoiCategory, number>>;
  /** Multipliers per tag (e.g. "baroque", "film", "ancient-rome", "food"). */
  tags?: Record<string, number>;
}

export interface EngineConfig {
  /** Hard upper bound on candidate distance (m). */
  maxRadiusM: number;
  /** Minimum silence between the end of one story and the start of the next (ms). */
  minGapMs: number;
  /** Don't come back to the same POI within this time (ms) unless asked. */
  poiCooldownMs: number;
  /** Candidates scoring below this are ignored. */
  minScore: number;
  /** Above this speed the user is jogging / on a scooter / in a vehicle -> quiet. */
  maxNarrationSpeedMps: number;
  /** Extra quiet window after a crossing ends (ms). */
  postCrossingQuietMs: number;
  /** Extra quiet window after the user stops talking (ms). */
  postTalkQuietMs: number;
  /** If GNSS accuracy is worse than this we don't trust proximity triggers. */
  maxAccuracyM: number;
  /** Speech rate for duration estimates. */
  wordsPerMinute: number;
  /** Word budgets per tier (20 s / 40 s / deep dive at 150 wpm). */
  wordBudget: Record<StoryTier, number>;
}

export const DEFAULT_ENGINE_CONFIG: EngineConfig = {
  maxRadiusM: 160,
  minGapMs: 20_000,
  poiCooldownMs: 15 * 60_000,
  minScore: 0.12,
  maxNarrationSpeedMps: 2.3,
  postCrossingQuietMs: 4_000,
  postTalkQuietMs: 3_000,
  maxAccuracyM: 35,
  wordsPerMinute: 150,
  wordBudget: { short: 55, medium: 105, deep: 260 },
};

export type QuietReason =
  | "manual-quiet"
  | "speaking"
  | "crossing-road"
  | "user-talking"
  | "moving-fast"
  | "cooldown"
  | "poor-gps"
  | "nothing-nearby";

export interface NarrateDecision {
  kind: "narrate";
  reason: "proximity" | "tell-me-more" | "related";
  poi: Poi;
  facts: FactCard[];
  tier: StoryTier;
  direction: DirectionClassification & { distanceM: number; bearingDeg: number };
  /** False when heading confidence is low: narration must not say left/right. */
  directionReliable: boolean;
  score: number;
  live: LiveInfo[];
  estimatedSec: number;
  t: number;
}

export interface SilentDecision {
  kind: "silent";
  reason: QuietReason;
  /** A user request (tell me more) is waiting for the quiet moment to end. */
  deferred?: boolean;
  t: number;
}

export type Decision = NarrateDecision | SilentDecision;

export interface Candidate {
  poi: Poi;
  score: number;
  distanceM: number;
  direction: DirectionClassification & { distanceM: number; bearingDeg: number };
  unspoken: FactCard[];
}

export interface EngineState {
  spokenFactIds: string[];
  poiLastNarrated: Record<string, number>;
  history: { t: number; poiId: string; factIds: string[]; tier: StoryTier; reason: NarrateDecision["reason"] }[];
}

const DIRECTION_WEIGHT = { ahead: 1.0, left: 0.9, right: 0.9, behind: 0.35 } as const;

export function wordCount(s: string): number {
  return s.trim().split(/\s+/).filter(Boolean).length;
}

export class StoryEngine {
  readonly config: EngineConfig;
  private pois: Poi[];
  private profile: InterestProfile = {};
  private spoken = new Set<string>();
  private poiLast = new Map<string, number>();
  private history: EngineState["history"] = [];
  private live = new Map<string, LiveInfo[]>();
  private speakingUntil = 0;
  private lastEndAt = -Infinity;
  private manualQuietUntil = 0;
  private lastCrossingAt = -Infinity;
  private lastTalkAt = -Infinity;
  private pendingMore = false;
  private lastNarrated: Poi | null = null;

  constructor(pois: Poi[], config: Partial<EngineConfig> = {}) {
    this.pois = pois;
    this.config = { ...DEFAULT_ENGINE_CONFIG, ...config, wordBudget: { ...DEFAULT_ENGINE_CONFIG.wordBudget, ...config.wordBudget } };
  }

  setProfile(profile: InterestProfile): void {
    this.profile = profile;
  }

  /** Merge live info (opening hours, events, closures). Expired items are ignored at read time. */
  setLiveInfo(items: LiveInfo[]): void {
    for (const it of items) {
      const arr = this.live.get(it.poi_id) ?? [];
      arr.push(it);
      this.live.set(it.poi_id, arr);
    }
  }

  liveFor(poiId: string, t: number): LiveInfo[] {
    return (this.live.get(poiId) ?? []).filter((l) => l.expires_at > t);
  }

  /** User pressed "Quiet": silence for `durationMs` (default 10 min) and stop current speech. */
  quiet(t: number, durationMs = 10 * 60_000): void {
    this.manualQuietUntil = t + durationMs;
    this.speakingUntil = Math.min(this.speakingUntil, t);
    this.pendingMore = false;
  }

  resume(t: number): void {
    this.manualQuietUntil = t;
  }

  /** Called by the audio layer when TTS actually finishes (or is interrupted). */
  onSpeechEnd(t: number): void {
    this.speakingUntil = Math.min(this.speakingUntil, t);
    this.lastEndAt = t;
  }

  isSpeaking(t: number): boolean {
    return t < this.speakingUntil;
  }

  exportState(): EngineState {
    return {
      spokenFactIds: [...this.spoken],
      poiLastNarrated: Object.fromEntries(this.poiLast),
      history: [...this.history],
    };
  }

  importState(s: EngineState): void {
    this.spoken = new Set(s.spokenFactIds);
    this.poiLast = new Map(Object.entries(s.poiLastNarrated));
    this.history = [...s.history];
  }

  get spokenCount(): number {
    return this.spoken.size;
  }

  private profileWeight(poi: Poi): number {
    const cat = this.profile.categories?.[poi.category] ?? 1;
    const tagWeights = poi.tags.map((t) => this.profile.tags?.[t]).filter((w): w is number => w !== undefined);
    const tag = tagWeights.length ? Math.max(...tagWeights) : 1;
    // A zero on either means "never"; otherwise geometric blend.
    if (cat === 0 || (tagWeights.length && tagWeights.every((w) => w === 0))) return 0;
    return Math.sqrt(cat * tag);
  }

  /** Quiet-moment check. Returns a reason to stay silent, or null if we may speak. */
  quietReason(ctx: EngineContext, ignoreGap = false): QuietReason | null {
    if (ctx.crossingRoad) this.lastCrossingAt = ctx.t;
    if (ctx.userTalking) this.lastTalkAt = ctx.t;
    if (ctx.t < this.manualQuietUntil) return "manual-quiet";
    if (ctx.t < this.speakingUntil) return "speaking";
    if (ctx.crossingRoad || ctx.t - this.lastCrossingAt < this.config.postCrossingQuietMs) return "crossing-road";
    if (ctx.userTalking || ctx.t - this.lastTalkAt < this.config.postTalkQuietMs) return "user-talking";
    if (ctx.speedMps > this.config.maxNarrationSpeedMps) return "moving-fast";
    if (!ignoreGap && ctx.t - this.lastEndAt < this.config.minGapMs) return "cooldown";
    return null;
  }

  /** Score every POI in range. Exposed for "what's around me" and for debugging/telemetry. */
  candidates(ctx: EngineContext, opts: { includeTold?: boolean; radiusM?: number } = {}): Candidate[] {
    const out: Candidate[] = [];
    const headingOk = ctx.heading !== null && ctx.headingConfidence !== "low";
    const recentCats = this.history.slice(-2).map((h) => this.pois.find((p) => p.id === h.poiId)?.category);
    for (const poi of this.pois) {
      const range = opts.radiusM ?? Math.min(poi.visible_range_m, this.config.maxRadiusM);
      const d = haversine(ctx.position, poi);
      if (d > range) continue;
      const unspoken = poi.facts.filter((f) => !this.spoken.has(f.id));
      if (!opts.includeTold) {
        if (unspoken.length === 0) continue;
        const last = this.poiLast.get(poi.id);
        if (last !== undefined && ctx.t - last < this.config.poiCooldownMs) continue;
      }
      const dir = directionTo(ctx.position, ctx.heading ?? 0, poi, { heightM: poi.height_m });
      const distanceFactor = 1 - 0.75 * Math.pow(d / range, 1.3);
      const headingFactor = !headingOk ? 0.8 : d < 25 ? 1 : DIRECTION_WEIGHT[dir.direction];
      const novelty = poi.facts.length === 0 ? 0 : unspoken.length === poi.facts.length ? 1 : 0.55 * (unspoken.length / poi.facts.length);
      const diversity = recentCats.filter((c) => c === poi.category).length >= 2 ? 0.75 : 1;
      const liveBoost = this.liveFor(poi.id, ctx.t).length ? 1.1 : 1;
      const score =
        poi.interest * this.profileWeight(poi) * distanceFactor * headingFactor * (opts.includeTold ? 1 : novelty) * diversity * liveBoost;
      out.push({ poi, score, distanceM: d, direction: dir, unspoken });
    }
    return out.sort((a, b) => b.score - a.score);
  }

  /** Choose tier from dwell time: standing still / slow -> 40 s, walking past -> 20 s. */
  chooseTier(ctx: EngineContext, c: Candidate): StoryTier {
    if (ctx.speedMps < 0.5) return "medium";
    // Seconds until we've walked out of comfortable range of the POI (rough, assumes passing by).
    const secondsInRange = (Math.min(c.poi.visible_range_m, this.config.maxRadiusM) + Math.max(0, 60 - c.distanceM)) / Math.max(ctx.speedMps, 0.3);
    if (c.poi.interest >= 0.85 && secondsInRange > 90) return "medium";
    return "short";
  }

  /** Greedy fact selection within the word budget: headline facts first, legends never lead. */
  selectFacts(unspoken: FactCard[], tier: StoryTier): FactCard[] {
    const budget = this.config.wordBudget[tier];
    const ordered = [...unspoken].sort((a, b) => a.depth - b.depth || Number(!!a.is_legend) - Number(!!b.is_legend));
    const chosen: FactCard[] = [];
    let words = 0;
    for (const f of ordered) {
      const w = wordCount(f.text);
      if (chosen.length === 0 || words + w <= budget) {
        chosen.push(f);
        words += w;
      }
      if (words >= budget) break;
    }
    return chosen;
  }

  private commit(ctx: EngineContext, c: Candidate, tier: StoryTier, reason: NarrateDecision["reason"]): NarrateDecision {
    const facts = this.selectFacts(c.unspoken, tier);
    const forceLookUp = facts.some((f) => f.look_up);
    const direction = directionTo(ctx.position, ctx.heading ?? 0, c.poi, { heightM: c.poi.height_m, forceLookUp });
    const words = facts.reduce((n, f) => n + wordCount(f.text), 0) + 12; // + opener / direction phrase
    const estimatedSec = Math.round((words / this.config.wordsPerMinute) * 60);
    for (const f of facts) this.spoken.add(f.id);
    this.poiLast.set(c.poi.id, ctx.t);
    this.speakingUntil = ctx.t + estimatedSec * 1000;
    this.lastEndAt = this.speakingUntil; // provisional; refined by onSpeechEnd()
    this.lastNarrated = c.poi;
    this.history.push({ t: ctx.t, poiId: c.poi.id, factIds: facts.map((f) => f.id), tier, reason });
    return {
      kind: "narrate",
      reason,
      poi: c.poi,
      facts,
      tier,
      direction,
      directionReliable: ctx.heading !== null && ctx.headingConfidence !== "low",
      score: c.score,
      live: this.liveFor(c.poi.id, ctx.t),
      estimatedSec,
      t: ctx.t,
    };
  }

  /** Main tick. Call ~1 Hz with fused context. */
  update(ctx: EngineContext): Decision {
    const quiet = this.quietReason(ctx, this.pendingMore);
    if (quiet) return { kind: "silent", reason: quiet, deferred: this.pendingMore || undefined, t: ctx.t };
    if (this.pendingMore) {
      this.pendingMore = false;
      const d = this.tellMeMore(ctx);
      if (d.kind === "narrate") return d;
    }
    if (ctx.accuracyM !== undefined && ctx.accuracyM > this.config.maxAccuracyM) return { kind: "silent", reason: "poor-gps", t: ctx.t };
    const best = this.candidates(ctx)[0];
    if (!best || best.score < this.config.minScore) return { kind: "silent", reason: "nothing-nearby", t: ctx.t };
    return this.commit(ctx, best, this.chooseTier(ctx, best), "proximity");
  }

  /**
   * "Tell me more": deep tier on the last POI; if exhausted, chain to the closest related POI
   * (shared tag) in range. Safety quiet moments still apply - the request is deferred.
   */
  tellMeMore(ctx: EngineContext): Decision {
    const quiet = this.quietReason(ctx, true);
    if (quiet && quiet !== "speaking" && quiet !== "manual-quiet") {
      this.pendingMore = true;
      return { kind: "silent", reason: quiet, deferred: true, t: ctx.t };
    }
    // An explicit request overrides current speech and manual quiet.
    this.speakingUntil = Math.min(this.speakingUntil, ctx.t);
    this.manualQuietUntil = Math.min(this.manualQuietUntil, ctx.t);
    const last = this.lastNarrated;
    if (last) {
      const unspoken = last.facts.filter((f) => !this.spoken.has(f.id));
      const d = haversine(ctx.position, last);
      if (unspoken.length && d < 400) {
        const dir = directionTo(ctx.position, ctx.heading ?? 0, last, { heightM: last.height_m });
        return this.commit(ctx, { poi: last, score: 1, distanceM: d, direction: dir, unspoken }, "deep", "tell-me-more");
      }
      const tags = new Set(last.tags);
      const related = this.candidates(ctx, { radiusM: 400 })
        .filter((c) => c.poi.id !== last.id)
        .map((c) => ({ c, shared: c.poi.tags.filter((t) => tags.has(t)).length }))
        .filter((x) => x.shared > 0)
        .sort((a, b) => b.shared - a.shared || b.c.score - a.c.score)[0];
      if (related) return this.commit(ctx, related.c, "medium", "related");
    }
    const best = this.candidates(ctx, { radiusM: 250 })[0];
    if (best) return this.commit(ctx, best, "medium", "related");
    return { kind: "silent", reason: "nothing-nearby", t: ctx.t };
  }

  /** "What's around me": top-N POIs with direction, regardless of novelty/cooldowns. */
  whatsAroundMe(ctx: EngineContext, n = 5, radiusM = 300): Candidate[] {
    return this.candidates(ctx, { includeTold: true, radiusM }).slice(0, n);
  }

  get lastPoi(): Poi | null {
    return this.lastNarrated;
  }
}
