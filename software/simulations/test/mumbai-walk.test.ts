import { describe, expect, it } from "vitest";
import { MUMBAI_DEMO_ROUTE, StoryEngine } from "../../packages/core/src/index.ts";
import { loadPack, runWalk } from "../walk-sim.ts";

describe("Mumbai pack + walk simulation (simulated sensors)", () => {
  const pack = loadPack("mumbai");

  it("pack has >= 60 POIs with 2-4 sourced facts each", () => {
    expect(pack.city).toBe("mumbai");
    expect(pack.pois.length).toBeGreaterThanOrEqual(60);
    for (const p of pack.pois) {
      expect(p.facts.length).toBeGreaterThanOrEqual(2);
      expect(p.facts.length).toBeLessThanOrEqual(4);
      for (const f of p.facts) expect(f.sources[0].url).toMatch(/^https:\/\//);
    }
  });

  it("standing at the Gateway facing it narrates the Gateway", () => {
    const e = new StoryEngine(pack.pois);
    const d = e.update({ t: 1e6, position: { lat: 18.9226, lng: 72.8338 }, heading: 135, headingConfidence: "high", speedMps: 0, accuracyM: 5 });
    expect(d.kind === "narrate" && d.poi.id).toBe("mumbai-gateway-of-india");
  });

  for (const seed of [1, 42, 99]) {
    it(`seed ${seed}: quiet compliance, no repeats, key heritage stops narrated`, () => {
      const { metrics, transcript } = runWalk(pack, { seed, route: MUMBAI_DEMO_ROUTE });
      expect(metrics.quiet.narrationStartsDuringQuiet).toBe(0);
      expect(metrics.factRepeatRate).toBe(0);
      expect(metrics.poiRepeatRate).toBe(0);
      expect(metrics.narrationsPerKm).toBeGreaterThan(4);
      expect(metrics.narrationsPerKm).toBeLessThan(16);
      expect(metrics.directionAccuracy).toBeGreaterThanOrEqual(0.85);
      expect(transcript.map((e) => e.poiId)).toEqual(
        expect.arrayContaining(["mumbai-gateway-of-india", "mumbai-kala-ghoda", "mumbai-flora-fountain-hutatma-chowk", "mumbai-horniman-circle", "mumbai-csmt"]),
      );
    });
  }
});
