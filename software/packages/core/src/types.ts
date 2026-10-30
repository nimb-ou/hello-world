/**
 * Shared types for the LORE core engine.
 * The City Pack JSON produced by `city-pack/` conforms to `CityPack`.
 */

export interface LatLng {
  lat: number;
  lng: number;
}

export type FactKind =
  | "history"
  | "architecture"
  | "art"
  | "legend"
  | "culture"
  | "film"
  | "people"
  | "practical";

export interface FactSource {
  url: string;
  title: string;
}

/** A single verified, sourced statement. Narration may ONLY use these. */
export interface FactCard {
  id: string;
  poi_id: string;
  text: string;
  kind: FactKind;
  /** 1 = headline fact (used in 20 s tier), 2 = supporting, 3 = deep-dive material. */
  depth: 1 | 2 | 3;
  /** True if the fact refers to something you must look up to see. */
  look_up?: boolean;
  /** True if the statement is a legend/tradition, narrated with hedging ("legend says"). */
  is_legend?: boolean;
  sources: FactSource[];
  review_status: "curated" | "verified" | "needs_review";
}

export type PoiCategory =
  | "monument"
  | "church"
  | "fountain"
  | "square"
  | "museum"
  | "ruin"
  | "street"
  | "bridge"
  | "statue"
  | "palace"
  | "park"
  | "neighbourhood"
  | "viewpoint"
  | "hidden_gem";

export interface Poi {
  id: string;
  name: string;
  lat: number;
  lng: number;
  category: PoiCategory;
  tags: string[];
  /** 0..1 editorial/computed interest score. */
  interest: number;
  /** Distance in metres from which the POI is plausibly visible/recognisable. */
  visible_range_m: number;
  /** Approximate height in metres (used for "look up" classification). */
  height_m?: number;
  wikipedia?: string;
  wikidata?: string;
  osm?: string;
  /** Building footprint polygon (GeoJSON ring) - placeholder until OSM footprints are imported. */
  footprint?: [number, number][] | null;
  facts: FactCard[];
}

export interface CityPack {
  schema_version: string;
  city: string;
  name: string;
  bbox: [number, number, number, number]; // [south, west, north, east]
  generated_at: string;
  build: { mode: "online" | "seed" | "seed+online"; notes: string[] };
  pois: Poi[];
}

export type Direction = "ahead" | "left" | "right" | "behind";

export type Persona = "local-friend" | "historian" | "storyteller" | "minimalist";

export type StoryTier = "short" | "medium" | "deep";

export interface LiveInfo {
  poi_id: string;
  text: string;
  source: string;
  /** epoch ms */
  expires_at: number;
}
