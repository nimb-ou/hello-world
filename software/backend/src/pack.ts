import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { haversine, type CityPack, type Poi } from "../../packages/core/src/index.ts";

export function loadPack(path?: string): CityPack {
  const p = path ?? process.env.LORE_PACK ?? fileURLToPath(new URL("../../city-pack/output/rome.pack.json", import.meta.url));
  return JSON.parse(readFileSync(p, "utf8")) as CityPack;
}

export class PackIndex {
  readonly byId = new Map<string, Poi>();
  constructor(readonly pack: CityPack) {
    for (const p of pack.pois) this.byId.set(p.id, p);
  }
  nearby(lat: number, lng: number, radiusM = 300, limit = 20) {
    return this.pack.pois
      .map((p) => ({ poi: p, distance_m: Math.round(haversine({ lat, lng }, p)) }))
      .filter((x) => x.distance_m <= radiusM)
      .sort((a, b) => a.distance_m - b.distance_m)
      .slice(0, limit);
  }
}
