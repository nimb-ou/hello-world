import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import type { CityPack } from "../src/types.ts";

export function loadRomePack(): CityPack {
  const p = fileURLToPath(new URL("../../../city-pack/output/rome.pack.json", import.meta.url));
  return JSON.parse(readFileSync(p, "utf8")) as CityPack;
}
