// Copies the built City Pack into the prototype's public/ folder so the PWA can load it offline.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
for (const city of ["rome", "mumbai"]) {
  const src = join(root, `city-pack/output/${city}.pack.json`);
  const dst = join(root, `apps/prototype/public/packs/${city}.pack.json`);
  mkdirSync(dirname(dst), { recursive: true });
  copyFileSync(src, dst);
  console.log(`copied ${src} -> ${dst}`);
}
