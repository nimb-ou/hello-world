import { describe, expect, it } from "vitest";
import { loadPack, runWalk, toMarkdown } from "../walk-sim.ts";

describe("Rome walk simulation (simulated sensors)", () => {
  const pack = loadPack();
  for (const seed of [1, 42, 99]) {
    it(`seed ${seed}: quiet-moment compliance, no repeats, sensible density`, () => {
      const { metrics, transcript } = runWalk(pack, { seed });
      expect(metrics.quiet.narrationStartsDuringQuiet).toBe(0);
      expect(metrics.factRepeatRate).toBe(0);
      expect(metrics.poiRepeatRate).toBe(0);
      expect(metrics.narrationsPerKm).toBeGreaterThan(4);
      expect(metrics.narrationsPerKm).toBeLessThan(16);
      expect(metrics.directionAccuracy).toBeGreaterThanOrEqual(0.85);
      expect(transcript.map((e) => e.poiId)).toEqual(expect.arrayContaining(["rome-pantheon", "rome-piazza-navona", "rome-campo-de-fiori", "rome-largo-di-torre-argentina", "rome-trevi-fountain"]));
    });
  }
  it("renders markdown labelled as simulated", () => {
    const res = runWalk(pack, { seed: 3 });
    expect(toMarkdown(res, 3)).toMatch(/SIMULATED DATA/);
  });
});
