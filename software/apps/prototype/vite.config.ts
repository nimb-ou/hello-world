import { defineConfig } from "vite";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL(".", import.meta.url));

export default defineConfig({
  root,
  base: "./",
  server: { fs: { allow: [fileURLToPath(new URL("../..", import.meta.url))] }, host: true },
  preview: { host: true },
  build: { outDir: "dist", emptyOutDir: true, target: "es2020" },
});
