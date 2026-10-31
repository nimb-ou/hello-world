import { describe, expect, it } from "vitest";
import { bearing } from "../src/geo.ts";
import { StoryEngine, type EngineContext } from "../src/story-engine.ts";
import { loadRomePack } from "./helpers.ts";

const pack = loadRomePack();
const PANTHEON_SQ = { lat: 41.89895, lng: 12.47685 };
const pantheon = pack.pois.find((p) => p.id === "rome-pantheon")!;

function ctx(over: Partial<EngineContext> = {}): EngineContext {
  return { t: 1_000_000, position: PANTHEON_SQ, heading: bearing(PANTHEON_SQ, pantheon), headingConfidence: "high", speedMps: 1.2, accuracyM: 5, ...over };
}

describe("StoryEngine", () => {
  it("narrates the Pantheon when standing in front of it, facing it", () => {
    const e = new StoryEngine(pack.pois);
    const d = e.update(ctx());
    expect(d.kind).toBe("narrate");
    if (d.kind !== "narrate") return;
    expect(d.poi.id).toBe("rome-pantheon");
    expect(d.direction.direction).toBe("ahead");
    expect(d.facts.length).toBeGreaterThan(0);
    expect(d.facts[0].depth).toBe(1);
    expect(d.estimatedSec).toBeLessThan(50);
  });

  it("never repeats a fact", () => {
    const e = new StoryEngine(pack.pois, { minGapMs: 0, poiCooldownMs: 0 });
    const seen = new Set<string>();
    let t = 0;
    for (let i = 0; i < 40; i++) {
      t += 120_000;
      const d = e.update(ctx({ t }));
      if (d.kind === "narrate") {
        for (const f of d.facts) {
          expect(seen.has(f.id)).toBe(false);
          seen.add(f.id);
        }
        e.onSpeechEnd(t + d.estimatedSec * 1000);
      }
    }
    expect(seen.size).toBe(pantheon.facts.length); // only the Pantheon is in range here; every fact told exactly once
  });

  it("stays quiet while crossing, talking, moving fast, or manually quieted", () => {
    const e = new StoryEngine(pack.pois);
    expect(e.update(ctx({ crossingRoad: true }))).toMatchObject({ kind: "silent", reason: "crossing-road" });
    expect(e.update(ctx({ t: 1_002_000 }))).toMatchObject({ kind: "silent", reason: "crossing-road" }); // post-crossing window
    expect(e.update(ctx({ t: 1_010_000, userTalking: true }))).toMatchObject({ reason: "user-talking" });
    expect(e.update(ctx({ t: 1_020_000, speedMps: 6 }))).toMatchObject({ reason: "moving-fast" });
    e.quiet(1_030_000, 60_000);
    expect(e.update(ctx({ t: 1_040_000 }))).toMatchObject({ reason: "manual-quiet" });
    expect(e.update(ctx({ t: 1_100_000 })).kind).toBe("narrate");
  });

  it("enforces a gap between stories and says 'speaking' while talking", () => {
    const e = new StoryEngine(pack.pois);
    const d = e.update(ctx());
    expect(d.kind).toBe("narrate");
    expect(e.update(ctx({ t: 1_001_000 }))).toMatchObject({ reason: "speaking" });
    if (d.kind === "narrate") e.onSpeechEnd(1_000_000 + d.estimatedSec * 1000);
    expect(e.update(ctx({ t: 1_000_000 + d.kind.length * 0 + (d as any).estimatedSec * 1000 + 5_000 }))).toMatchObject({ reason: "cooldown" });
  });

  it("does not trust proximity with poor GPS", () => {
    const e = new StoryEngine(pack.pois);
    expect(e.update(ctx({ accuracyM: 80 }))).toMatchObject({ reason: "poor-gps" });
  });

  it("interest profile changes what gets picked", () => {
    const at = { lat: 41.8988, lng: 12.4731 }; // Four Rivers fountain / Navona
    const base = new StoryEngine(pack.pois);
    const noFountains = new StoryEngine(pack.pois);
    noFountains.setProfile({ categories: { fountain: 0, square: 0 } });
    const a = base.update(ctx({ position: at, heading: 0 }));
    const b = noFountains.update(ctx({ position: at, heading: 0 }));
    expect(a.kind).toBe("narrate");
    expect(b.kind).toBe("narrate");
    if (a.kind === "narrate" && b.kind === "narrate") {
      expect(["fountain", "square"]).toContain(a.poi.category);
      expect(["fountain", "square"]).not.toContain(b.poi.category);
    }
  });

  it("prefers things ahead over things behind", () => {
    const e = new StoryEngine(pack.pois);
    const cands = e.candidates(ctx({ heading: bearing(PANTHEON_SQ, pantheon) }));
    const ahead = new StoryEngine(pack.pois).candidates(ctx({ heading: (bearing(PANTHEON_SQ, pantheon) + 180) % 360 }));
    const s1 = cands.find((c) => c.poi.id === "rome-pantheon")!.score;
    const s2 = ahead.find((c) => c.poi.id === "rome-pantheon")!.score;
    expect(s1).toBeGreaterThan(s2);
  });

  it("tier: 40 s when standing, 20 s when walking past a minor site", () => {
    const e = new StoryEngine(pack.pois);
    const d = e.update(ctx({ speedMps: 0 }));
    expect(d.kind === "narrate" && d.tier).toBe("medium");
    const pasq = pack.pois.find((p) => p.id === "rome-pasquino")!;
    const e2 = new StoryEngine(pack.pois);
    const d2 = e2.update(ctx({ position: pasq, heading: 0, speedMps: 1.4 }));
    expect(d2.kind === "narrate" && d2.tier).toBe("short");
  });

  it("'tell me more' goes deep on the same POI, then chains to a related one", () => {
    const e = new StoryEngine(pack.pois, { wordBudget: { short: 30, medium: 30, deep: 260 } });
    const d1 = e.update(ctx());
    expect(d1.kind).toBe("narrate");
    const d2 = e.tellMeMore(ctx({ t: 1_005_000 }));
    expect(d2).toMatchObject({ kind: "narrate", reason: "tell-me-more", tier: "deep" });
    if (d2.kind === "narrate") expect(d2.poi.id).toBe("rome-pantheon");
    const d3 = e.tellMeMore(ctx({ t: 1_010_000 }));
    expect(d3.kind).toBe("narrate");
    if (d3.kind === "narrate") {
      expect(d3.reason).toBe("related");
      expect(d3.poi.id).not.toBe("rome-pantheon");
    }
  });

  it("'tell me more' during a crossing is deferred and delivered after", () => {
    const e = new StoryEngine(pack.pois, { wordBudget: { short: 30, medium: 30, deep: 260 } });
    e.update(ctx());
    const d = e.tellMeMore(ctx({ t: 1_002_000, crossingRoad: true }));
    expect(d).toMatchObject({ kind: "silent", reason: "crossing-road", deferred: true });
    expect(e.update(ctx({ t: 1_003_000 }))).toMatchObject({ kind: "silent", deferred: true });
    const later = e.update(ctx({ t: 1_010_000 }));
    expect(later).toMatchObject({ kind: "narrate", reason: "tell-me-more" });
  });

  it("whatsAroundMe lists nearby POIs with directions", () => {
    const e = new StoryEngine(pack.pois);
    const list = e.whatsAroundMe(ctx(), 5);
    expect(list.length).toBe(5);
    expect(list.map((c) => c.poi.id)).toContain("rome-pantheon");
    for (const c of list) expect(["ahead", "left", "right", "behind"]).toContain(c.direction.direction);
  });

  it("merges fresh live info and ignores expired", () => {
    const e = new StoryEngine(pack.pois);
    e.setLiveInfo([
      { poi_id: "rome-pantheon", text: "Open until 19:00 today.", source: "mock-hours", expires_at: 2_000_000 },
      { poi_id: "rome-pantheon", text: "Old news.", source: "mock", expires_at: 10 },
    ]);
    const d = e.update(ctx());
    expect(d.kind === "narrate" && d.live.map((l) => l.text)).toEqual(["Open until 19:00 today."]);
  });

  it("low heading confidence marks direction unreliable", () => {
    const e = new StoryEngine(pack.pois);
    const d = e.update(ctx({ headingConfidence: "low" }));
    expect(d.kind === "narrate" && d.directionReliable).toBe(false);
  });

  it("state export/import preserves novelty across sessions", () => {
    const e = new StoryEngine(pack.pois);
    e.update(ctx());
    const e2 = new StoryEngine(pack.pois);
    e2.importState(e.exportState());
    expect(e2.spokenCount).toBe(e.spokenCount);
  });
});
