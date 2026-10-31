import { describe, expect, it } from "vitest";
import { angleDiff } from "../src/geo.ts";
import { ComplementaryHeading, HeadingKalman } from "../src/heading-fusion.ts";

// Deterministic PRNG + gaussian for reproducible noise.
function rng(seed: number) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
}
function gauss(r: () => number) {
  return Math.sqrt(-2 * Math.log(r() + 1e-12)) * Math.cos(2 * Math.PI * r());
}

describe("HeadingKalman", () => {
  it("converges to true heading from noisy compass + gps + steps", () => {
    const r = rng(1);
    const k = new HeadingKalman();
    const truth = 75;
    for (let t = 0; t < 60_000; t += 200) {
      k.compass({ t, headingDeg: truth + 8 + gauss(r) * 8, fieldUT: 46 }); // +8 deg hard-iron bias
      if (t % 1000 === 0) k.gps({ t, courseDeg: truth + gauss(r) * 6, speedMps: 1.4, accuracyM: 4 });
      if (t % 600 === 0) k.step({ t, directionDeg: truth + gauss(r) * 12, quality: 0.8 });
    }
    const e = k.estimate(60_000);
    expect(Math.abs(angleDiff(e.headingDeg, truth))).toBeLessThan(6); // vs 8 deg raw compass bias
    expect(e.compassBiasDeg).toBeGreaterThan(4); // learned the compass offset
    expect(e.confidence).toBe("high");
  });

  it("handles wrap-around at north", () => {
    const r = rng(2);
    const k = new HeadingKalman();
    for (let t = 0; t < 20_000; t += 200) k.compass({ t, headingDeg: (360 + 2 + gauss(r) * 5) % 360, fieldUT: 46 });
    const e = k.estimate();
    expect(Math.abs(angleDiff(e.headingDeg, 2))).toBeLessThan(4);
  });

  it("rejects magnetically disturbed compass samples", () => {
    const k = new HeadingKalman();
    for (let t = 0; t < 5000; t += 200) k.gps({ t, courseDeg: 180, speedMps: 1.5, accuracyM: 3 });
    // walking past a tram line: field magnitude 80 uT and compass says 120 deg
    let accepted = 0;
    for (let t = 5000; t < 8000; t += 200) if (k.compass({ t, headingDeg: 120, fieldUT: 80 })) accepted++;
    expect(accepted).toBe(0);
    const e = k.estimate();
    expect(Math.abs(angleDiff(e.headingDeg, 180))).toBeLessThan(5);
    expect(e.rejected.compass).toBeGreaterThan(10);
  });

  it("ignores GPS course when standing still", () => {
    const k = new HeadingKalman();
    expect(k.gps({ t: 0, courseDeg: 90, speedMps: 0.2 })).toBe(false);
    expect(k.gps({ t: 0, courseDeg: null, speedMps: 2 })).toBe(false);
  });

  it("gates outliers but follows a real turn via gyro", () => {
    const k = new HeadingKalman();
    for (let t = 0; t <= 5000; t += 100) k.compass({ t, headingDeg: 0, fieldUT: 46 });
    // single wild sample -> rejected
    expect(k.compass({ t: 5100, headingDeg: 150, fieldUT: 46 })).toBe(false);
    // user turns right 90 deg over 2 s, gyro reports it, compass follows
    for (let t = 5200; t <= 7200; t += 100) {
      k.gyro({ t, yawRateDps: 45 });
      k.compass({ t, headingDeg: ((t - 5200) / 2000) * 90, fieldUT: 46 });
    }
    for (let t = 7300; t <= 9000; t += 100) {
      k.gyro({ t, yawRateDps: 0 });
      k.compass({ t, headingDeg: 90, fieldUT: 46 });
    }
    expect(Math.abs(angleDiff(k.estimate().headingDeg, 90))).toBeLessThan(6);
  });

  it("confidence is low before any measurement", () => {
    expect(new HeadingKalman().estimate().confidence).toBe("low");
  });
});

describe("ComplementaryHeading", () => {
  it("integrates gyro and pulls toward the absolute reference", () => {
    const c = new ComplementaryHeading(0.1);
    c.update(0, 10);
    let h = 0;
    for (let t = 100; t <= 10_000; t += 100) h = c.update(t, 40, 0);
    expect(Math.abs(angleDiff(h, 40))).toBeLessThan(1);
    expect(c.update(10_100, null, 90)).toBeCloseTo(h + 9, 0);
  });
});
