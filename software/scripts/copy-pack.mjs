// Copies the built City Pack into the prototype's public/ folder so the PWA can load it offline.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = join(root, "city-pack/output/rome.pack.json");
const dst = join(root, "apps/prototype/public/packs/rome.pack.json");
mkdirSync(dirname(dst), { recursive: true });
copyFileSync(src, dst);
console.log(`copied ${src} -> ${dst}`);
