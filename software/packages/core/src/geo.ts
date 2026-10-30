/**
 * Geodesy helpers for Map Vision.
 *
 * All angles are degrees, clockwise from true north, in [0, 360) unless noted.
 * Distances are metres. Spherical Earth model (R = 6 371 008.8 m) is accurate to
 * ~0.3 % which is far below GNSS error at walking scale.
 */
import type { Direction, LatLng } from "./types.ts";

export const EARTH_RADIUS_M = 6_371_008.8;
const D2R = Math.PI / 180;
const R2D = 180 / Math.PI;

export function toRad(deg: number): number {
  return deg * D2R;
}
export function toDeg(rad: number): number {
  return rad * R2D;
}

/** Normalise any angle into [0, 360). */
export function normalizeDeg(deg: number): number {
  const d = deg % 360;
  return d < 0 ? d + 360 : d;
}

/** Signed smallest difference b - a in (-180, 180]. Positive = b is clockwise of a. */
export function angleDiff(a: number, b: number): number {
  let d = normalizeDeg(b) - normalizeDeg(a);
  if (d > 180) d -= 360;
  if (d <= -180) d += 360;
  return d;
}

/** Great-circle distance (haversine). */
export function haversine(a: LatLng, b: LatLng): number {
  const dLat = toRad(b.lat - a.lat);
  const dLng = toRad(b.lng - a.lng);
  const s =
    Math.sin(dLat / 2) ** 2 + Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 2 * EARTH_RADIUS_M * Math.asin(Math.min(1, Math.sqrt(s)));
}

/** Initial great-circle bearing from a to b. */
export function bearing(a: LatLng, b: LatLng): number {
  const phi1 = toRad(a.lat);
  const phi2 = toRad(b.lat);
  const dL = toRad(b.lng - a.lng);
  const y = Math.sin(dL) * Math.cos(phi2);
  const x = Math.cos(phi1) * Math.sin(phi2) - Math.sin(phi1) * Math.cos(phi2) * Math.cos(dL);
  return normalizeDeg(toDeg(Math.atan2(y, x)));
}

/** Point reached travelling `distanceM` from `origin` on `bearingDeg`. */
export function destinationPoint(origin: LatLng, bearingDeg: number, distanceM: number): LatLng {
  const delta = distanceM / EARTH_RADIUS_M;
  const theta = toRad(bearingDeg);
  const phi1 = toRad(origin.lat);
  const l1 = toRad(origin.lng);
  const phi2 = Math.asin(Math.sin(phi1) * Math.cos(delta) + Math.cos(phi1) * Math.sin(delta) * Math.cos(theta));
  const l2 =
    l1 + Math.atan2(Math.sin(theta) * Math.sin(delta) * Math.cos(phi1), Math.cos(delta) - Math.sin(phi1) * Math.sin(phi2));
  return { lat: toDeg(phi2), lng: ((toDeg(l2) + 540) % 360) - 180 };
}

/** Local equirectangular projection (east, north metres) around `origin`. Good to <0.1 % within a few km. */
export function toLocalXY(origin: LatLng, p: LatLng): { x: number; y: number } {
  const x = toRad(p.lng - origin.lng) * Math.cos(toRad((origin.lat + p.lat) / 2)) * EARTH_RADIUS_M;
  const y = toRad(p.lat - origin.lat) * EARTH_RADIUS_M;
  return { x, y };
}

/** Relative bearing of a target from the user's heading, in (-180, 180]. Negative = left. */
export function relativeBearing(headingDeg: number, bearingToTargetDeg: number): number {
  return angleDiff(headingDeg, bearingToTargetDeg);
}

export interface DirectionClassification {
  direction: Direction;
  /** Signed relative bearing (deg); negative = left. */
  relative: number;
  /** Clock position 1..12 (12 = straight ahead). */
  clock: number;
  /** True if the user should tilt their head up to see the feature. */
  lookUp: boolean;
  /** Elevation angle to the top of the feature (deg), if height known. */
  elevationDeg?: number;
}

export interface ClassifyOptions {
  /** Half-width of the "ahead" cone (deg). Default 30. */
  aheadHalfAngle?: number;
  /** Half-width of the "behind" cone (deg). Default 30 (i.e. |rel| >= 150). */
  behindHalfAngle?: number;
  /** Height of the feature (m) - used for look-up. */
  heightM?: number;
  /** Distance to the feature (m) - used for look-up. */
  distanceM?: number;
  /** Elevation angle above which we say "look up". Default 25 deg. */
  lookUpThresholdDeg?: number;
  /** Force look-up (fact card is about something high, e.g. a frieze or bricked window). */
  forceLookUp?: boolean;
  /** Eye height (m). Default 1.6. */
  eyeHeightM?: number;
}

/**
 * Classify a relative bearing into ahead / left / right / behind and decide "look up".
 */
export function classifyDirection(relative: number, opts: ClassifyOptions = {}): DirectionClassification {
  const ahead = opts.aheadHalfAngle ?? 30;
  const behind = opts.behindHalfAngle ?? 30;
  const rel = angleDiff(0, relative);
  const abs = Math.abs(rel);
  let direction: Direction;
  if (abs <= ahead) direction = "ahead";
  else if (abs >= 180 - behind) direction = "behind";
  else direction = rel < 0 ? "left" : "right";

  let clock = Math.round(normalizeDeg(rel) / 30) % 12;
  if (clock === 0) clock = 12;

  let elevationDeg: number | undefined;
  let lookUp = !!opts.forceLookUp;
  if (opts.heightM !== undefined && opts.distanceM !== undefined) {
    const eye = opts.eyeHeightM ?? 1.6;
    elevationDeg = toDeg(Math.atan2(Math.max(0, opts.heightM - eye), Math.max(1, opts.distanceM)));
    if (elevationDeg >= (opts.lookUpThresholdDeg ?? 25)) lookUp = true;
  }
  return { direction, relative: rel, clock, lookUp, elevationDeg };
}

/** Convenience: classify target `poi` relative to user at `pos` facing `heading`. */
export function directionTo(
  pos: LatLng,
  headingDeg: number,
  target: LatLng,
  opts: Omit<ClassifyOptions, "distanceM"> = {},
): DirectionClassification & { distanceM: number; bearingDeg: number } {
  const distanceM = haversine(pos, target);
  const bearingDeg = bearing(pos, target);
  const c = classifyDirection(relativeBearing(headingDeg, bearingDeg), { ...opts, distanceM });
  return { ...c, distanceM, bearingDeg };
}

/**
 * Which side of the street is `point` on, for someone walking along segment start->end?
 * Uses the 2D cross product in a local tangent plane. Returns "left" | "right" | "on"
 * (within `toleranceM` of the centreline) and the perpendicular offset.
 */
export function sideOfStreet(
  start: LatLng,
  end: LatLng,
  point: LatLng,
  toleranceM = 1.0,
): { side: "left" | "right" | "on"; offsetM: number; alongFraction: number } {
  const b = toLocalXY(start, end);
  const p = toLocalXY(start, point);
  const len = Math.hypot(b.x, b.y);
  if (len < 1e-6) return { side: "on", offsetM: Math.hypot(p.x, p.y), alongFraction: 0 };
  const cross = b.x * p.y - b.y * p.x; // >0 => point is counter-clockwise => left of travel
  const offset = cross / len;
  const along = (b.x * p.x + b.y * p.y) / (len * len);
  if (Math.abs(offset) <= toleranceM) return { side: "on", offsetM: Math.abs(offset), alongFraction: along };
  return { side: offset > 0 ? "left" : "right", offsetM: Math.abs(offset), alongFraction: along };
}

/** Distance from point to segment (m), plus the clamped projection fraction. */
export function distanceToSegment(start: LatLng, end: LatLng, point: LatLng): { distanceM: number; t: number } {
  const b = toLocalXY(start, end);
  const p = toLocalXY(start, point);
  const len2 = b.x * b.x + b.y * b.y;
  const t = len2 === 0 ? 0 : Math.max(0, Math.min(1, (p.x * b.x + p.y * b.y) / len2));
  return { distanceM: Math.hypot(p.x - t * b.x, p.y - t * b.y), t };
}

/** Linear interpolation along a polyline by distance. Returns the position and segment heading. */
export function interpolateAlong(path: LatLng[], distanceM: number): { pos: LatLng; heading: number; segment: number; done: boolean } {
  if (path.length < 2) throw new Error("path needs >= 2 points");
  let remaining = Math.max(0, distanceM);
  for (let i = 0; i < path.length - 1; i++) {
    const segLen = haversine(path[i], path[i + 1]);
    const hdg = bearing(path[i], path[i + 1]);
    if (remaining <= segLen) {
      const f = segLen === 0 ? 0 : remaining / segLen;
      return {
        pos: { lat: path[i].lat + (path[i + 1].lat - path[i].lat) * f, lng: path[i].lng + (path[i + 1].lng - path[i].lng) * f },
        heading: hdg,
        segment: i,
        done: false,
      };
    }
    remaining -= segLen;
  }
  const n = path.length;
  return { pos: path[n - 1], heading: bearing(path[n - 2], path[n - 1]), segment: n - 2, done: true };
}

export function pathLength(path: LatLng[]): number {
  let d = 0;
  for (let i = 0; i < path.length - 1; i++) d += haversine(path[i], path[i + 1]);
  return d;
}

/** Human phrase for a classification, e.g. "on your right", "just ahead", "behind you". */
export function directionPhrase(c: Pick<DirectionClassification, "direction">, distanceM?: number): string {
  const near = distanceM !== undefined && distanceM < 40;
  switch (c.direction) {
    case "ahead":
      return near ? "right in front of you" : "just ahead";
    case "left":
      return "on your left";
    case "right":
      return "on your right";
    case "behind":
      return "behind you";
  }
}
