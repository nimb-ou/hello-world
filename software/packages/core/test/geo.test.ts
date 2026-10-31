import { describe, expect, it } from "vitest";
import {
  angleDiff, bearing, classifyDirection, destinationPoint, directionTo, distanceToSegment, haversine,
  interpolateAlong, normalizeDeg, pathLength, relativeBearing, sideOfStreet,
} from "../src/geo.ts";

const PANTHEON = { lat: 41.8986, lng: 12.4769 };
const TREVI = { lat: 41.9009, lng: 12.4833 };
const COLOSSEUM = { lat: 41.8902, lng: 12.4922 };

describe("haversine", () => {
  it("is zero for identical points", () => expect(haversine(PANTHEON, PANTHEON)).toBe(0));
  it("Pantheon -> Trevi is ~580 m", () => {
    const d = haversine(PANTHEON, TREVI);
    expect(d).toBeGreaterThan(560);
    expect(d).toBeLessThan(600);
  });
  it("1 degree of latitude is ~111.2 km", () => {
    expect(haversine({ lat: 41, lng: 12 }, { lat: 42, lng: 12 })).toBeCloseTo(111_195, -2);
  });
  it("is symmetric", () => expect(haversine(PANTHEON, COLOSSEUM)).toBeCloseTo(haversine(COLOSSEUM, PANTHEON), 6));
});

describe("bearing", () => {
  it("cardinal directions", () => {
    const o = { lat: 41.9, lng: 12.48 };
    expect(bearing(o, { lat: 41.91, lng: 12.48 })).toBeCloseTo(0, 3);
    expect(bearing(o, { lat: 41.9, lng: 12.49 })).toBeCloseTo(90, 1);
    expect(bearing(o, { lat: 41.89, lng: 12.48 })).toBeCloseTo(180, 3);
    expect(bearing(o, { lat: 41.9, lng: 12.47 })).toBeCloseTo(270, 1);
  });
  it("Pantheon -> Trevi is roughly ENE", () => {
    const b = bearing(PANTHEON, TREVI);
    expect(b).toBeGreaterThan(55);
    expect(b).toBeLessThan(75);
  });
  it("destinationPoint round-trips with bearing/haversine", () => {
    const p = destinationPoint(PANTHEON, 123, 250);
    expect(haversine(PANTHEON, p)).toBeCloseTo(250, 3);
    expect(bearing(PANTHEON, p)).toBeCloseTo(123, 2);
  });
});

describe("angles", () => {
  it("normalizes", () => {
    expect(normalizeDeg(-10)).toBe(350);
    expect(normalizeDeg(725)).toBe(5);
  });
  it("angleDiff wraps across north", () => {
    expect(angleDiff(350, 10)).toBe(20);
    expect(angleDiff(10, 350)).toBe(-20);
    expect(angleDiff(0, 180)).toBe(180);
  });
  it("relativeBearing negative = left", () => {
    expect(relativeBearing(90, 0)).toBe(-90);
    expect(relativeBearing(90, 180)).toBe(90);
  });
});

describe("classifyDirection", () => {
  it("ahead / left / right / behind cones", () => {
    expect(classifyDirection(0).direction).toBe("ahead");
    expect(classifyDirection(29).direction).toBe("ahead");
    expect(classifyDirection(-31).direction).toBe("left");
    expect(classifyDirection(95).direction).toBe("right");
    expect(classifyDirection(150).direction).toBe("behind");
    expect(classifyDirection(-170).direction).toBe("behind");
  });
  it("clock positions", () => {
    expect(classifyDirection(0).clock).toBe(12);
    expect(classifyDirection(90).clock).toBe(3);
    expect(classifyDirection(-90).clock).toBe(9);
    expect(classifyDirection(180).clock).toBe(6);
  });
  it("look up when the elevation angle to the top is steep", () => {
    // 43 m dome at 40 m -> ~46 deg -> look up
    expect(classifyDirection(0, { heightM: 43, distanceM: 40 }).lookUp).toBe(true);
    // same dome at 200 m -> ~12 deg -> no
    expect(classifyDirection(0, { heightM: 43, distanceM: 200 }).lookUp).toBe(false);
    expect(classifyDirection(0, { forceLookUp: true }).lookUp).toBe(true);
  });
  it("directionTo: facing north with Trevi to the NE-E -> right", () => {
    const c = directionTo(PANTHEON, 0, TREVI);
    expect(c.direction).toBe("right");
    const c2 = directionTo(PANTHEON, 64, TREVI);
    expect(c2.direction).toBe("ahead");
    const c3 = directionTo(PANTHEON, 244, TREVI);
    expect(c3.direction).toBe("behind");
  });
});

describe("sideOfStreet", () => {
  // Walking north up a street; a point east of it is on the right.
  const a = { lat: 41.9, lng: 12.48 };
  const b = { lat: 41.901, lng: 12.48 };
  it("east of a northbound street is right, west is left", () => {
    expect(sideOfStreet(a, b, { lat: 41.9005, lng: 12.4802 }).side).toBe("right");
    expect(sideOfStreet(a, b, { lat: 41.9005, lng: 12.4798 }).side).toBe("left");
  });
  it("reverses when walking the other way", () => {
    expect(sideOfStreet(b, a, { lat: 41.9005, lng: 12.4802 }).side).toBe("left");
  });
  it("reports offset and 'on' near the centreline", () => {
    const r = sideOfStreet(a, b, { lat: 41.9005, lng: 12.48 + 0.00012 });
    expect(r.offsetM).toBeCloseTo(9.9, 0);
    expect(sideOfStreet(a, b, { lat: 41.9005, lng: 12.480001 }).side).toBe("on");
  });
  it("distanceToSegment clamps to endpoints", () => {
    const r = distanceToSegment(a, b, { lat: 41.899, lng: 12.48 });
    expect(r.t).toBe(0);
    expect(r.distanceM).toBeCloseTo(111.2, 0);
  });
});

describe("paths", () => {
  const path = [PANTHEON, TREVI, COLOSSEUM];
  it("pathLength sums segments", () => expect(pathLength(path)).toBeCloseTo(haversine(PANTHEON, TREVI) + haversine(TREVI, COLOSSEUM), 6));
  it("interpolateAlong walks the path", () => {
    const mid = interpolateAlong(path, haversine(PANTHEON, TREVI) / 2);
    expect(mid.segment).toBe(0);
    expect(haversine(mid.pos, PANTHEON)).toBeCloseTo(haversine(PANTHEON, TREVI) / 2, 0);
    expect(interpolateAlong(path, 1e9).done).toBe(true);
  });
});
