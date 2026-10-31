/**
 * LORE backend (Node, zero-framework HTTP). Endpoints:
 *   GET  /health
 *   GET  /nearby?lat&lng&radius=300&limit=20
 *   POST /narrate            {poi_id, fact_ids?, persona?, tier?, direction?, distance_m?, follow_up?}
 *   GET  /search?q=...       (web search adapter; mock by default)
 *   GET  /hotels?lat&lng&checkin&nights&max_price_eur   (affiliate adapter; mock, SIMULATED data)
 *   POST /safety/walk-home   {user_id, eta_minutes, contacts[]}
 *   GET  /safety/walk-home/:id | POST .../:id/checkin | .../:id/extend {minutes} | .../:id/cancel | .../:id/location {ciphertext}
 *   GET  /s/:token           share-link view (ciphertext only)
 * Run: npm run backend   (PORT=8787; ANTHROPIC_API_KEY optional -> mock mode)
 */
import { createServer, type IncomingMessage, type Server, type ServerResponse } from "node:http";
import Anthropic from "@anthropic-ai/sdk";
import { ClaudeWebSearchAdapter, MockSearchAdapter, type WebSearchAdapter } from "./adapters/search.ts";
import { MockHotelAdapter, type HotelAffiliateAdapter } from "./adapters/hotels.ts";
import { NarrateService } from "./narrate.ts";
import { loadPack, PackIndex } from "./pack.ts";
import { MockNotifier, SafetyService } from "./safety.ts";

export interface AppDeps {
  index: PackIndex;
  narrate: NarrateService;
  search: WebSearchAdapter;
  hotels: HotelAffiliateAdapter;
  safety: SafetyService;
}

export function defaultDeps(): AppDeps {
  const index = new PackIndex(loadPack());
  const key = process.env.ANTHROPIC_API_KEY;
  return {
    index,
    narrate: NarrateService.fromEnv(index.byId),
    search: key && process.env.LORE_SEARCH === "claude" ? new ClaudeWebSearchAdapter(new Anthropic({ apiKey: key })) : new MockSearchAdapter(),
    hotels: new MockHotelAdapter(),
    safety: new SafetyService(new MockNotifier()),
  };
}

class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

function send(res: ServerResponse, status: number, body: unknown) {
  res.writeHead(status, { "content-type": "application/json", "access-control-allow-origin": "*", "access-control-allow-headers": "content-type", "access-control-allow-methods": "GET,POST,OPTIONS" });
  res.end(JSON.stringify(body));
}

async function readJson(req: IncomingMessage): Promise<any> {
  let raw = "";
  for await (const chunk of req) {
    raw += chunk;
    if (raw.length > 64_000) throw new HttpError(413, "body too large");
  }
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    throw new HttpError(400, "invalid JSON");
  }
}

function num(v: string | null, name: string): number {
  const n = Number(v);
  if (v === null || !Number.isFinite(n)) throw new HttpError(400, `${name} is required and must be a number`);
  return n;
}

export function createApp(deps: AppDeps = defaultDeps()): Server {
  return createServer(async (req, res) => {
    try {
      const url = new URL(req.url ?? "/", "http://localhost");
      const path = url.pathname;
      const q = url.searchParams;
      if (req.method === "OPTIONS") return send(res, 204, {});
      if (req.method === "GET" && path === "/health") return send(res, 200, { ok: true, city: deps.index.pack.city, pois: deps.index.pack.pois.length, narrate_mode: deps.narrate.mode, search: deps.search.name, hotels: deps.hotels.name });
      if (req.method === "GET" && path === "/nearby") {
        const items = deps.index.nearby(num(q.get("lat"), "lat"), num(q.get("lng"), "lng"), Number(q.get("radius") ?? 300), Number(q.get("limit") ?? 20));
        return send(res, 200, { items: items.map(({ poi, distance_m }) => ({ id: poi.id, name: poi.name, lat: poi.lat, lng: poi.lng, category: poi.category, interest: poi.interest, distance_m, facts: poi.facts.length })) });
      }
      if (req.method === "POST" && path === "/narrate") {
        const body = await readJson(req);
        if (typeof body.poi_id !== "string") throw new HttpError(400, "poi_id required");
        try {
          return send(res, 200, await deps.narrate.narrate(body));
        } catch (e) {
          if (e instanceof RangeError) throw new HttpError(400, e.message);
          throw e;
        }
      }
      if (req.method === "GET" && path === "/search") {
        const query = q.get("q");
        if (!query) throw new HttpError(400, "q required");
        return send(res, 200, { adapter: deps.search.name, live_info_only: true, results: await deps.search.search(query, { limit: Number(q.get("limit") ?? 5) }) });
      }
      if (req.method === "GET" && path === "/hotels") {
        const offers = await deps.hotels.search({ lat: num(q.get("lat"), "lat"), lng: num(q.get("lng"), "lng"), checkin: q.get("checkin") ?? undefined, nights: Number(q.get("nights") ?? 1), max_price_eur: q.get("max_price_eur") ? Number(q.get("max_price_eur")) : undefined });
        return send(res, 200, { adapter: deps.hotels.name, offers });
      }
      if (path === "/safety/walk-home" && req.method === "POST") {
        const b = await readJson(req);
        try {
          const { timer, share_url_base } = deps.safety.start(String(b.user_id ?? "anon"), Number(b.eta_minutes), Array.isArray(b.contacts) ? b.contacts.map(String) : []);
          return send(res, 201, { id: timer.id, status: timer.status, due_at: timer.due_at, share_url_base, note: "Append #k=<key> on device; the server never receives the key." });
        } catch (e) {
          throw new HttpError(400, (e as Error).message);
        }
      }
      const m = path.match(/^\/safety\/walk-home\/([\w-]+)(?:\/(checkin|extend|cancel|location))?$/);
      if (m) {
        const [, id, action] = m;
        await deps.safety.sweep();
        try {
          if (!action && req.method === "GET") {
            const t = deps.safety.get(id);
            if (!t) throw new HttpError(404, "not found");
            return send(res, 200, { id: t.id, status: t.status, due_at: t.due_at, escalated_at: t.escalated_at ?? null, locations: t.locations.length });
          }
          if (req.method === "POST" && action === "checkin") return send(res, 200, { status: deps.safety.checkIn(id).status });
          if (req.method === "POST" && action === "cancel") return send(res, 200, { status: deps.safety.cancel(id).status });
          if (req.method === "POST" && action === "extend") return send(res, 200, { due_at: deps.safety.extend(id, Number((await readJson(req)).minutes ?? 10)).due_at });
          if (req.method === "POST" && action === "location") {
            deps.safety.pushLocation(id, String((await readJson(req)).ciphertext ?? ""));
            return send(res, 202, { stored: true });
          }
        } catch (e) {
          if (e instanceof HttpError) throw e;
          const msg = (e as Error).message;
          throw new HttpError(msg === "not found" ? 404 : 400, msg);
        }
      }
      const s = path.match(/^\/s\/([\w-]+)$/);
      if (s && req.method === "GET") {
        await deps.safety.sweep();
        const v = deps.safety.shareView(s[1]);
        if (!v) throw new HttpError(404, "not found");
        return send(res, 200, v);
      }
      throw new HttpError(404, "not found");
    } catch (e) {
      if (e instanceof HttpError) return send(res, e.status, { error: e.message });
      console.error(e);
      return send(res, 500, { error: "internal error" });
    }
  });
}

const isMain = process.argv[1]?.endsWith("server.ts");
if (isMain) {
  const port = Number(process.env.PORT ?? 8787);
  const deps = defaultDeps();
  createApp(deps).listen(port, () => console.log(`LORE backend on :${port} (narrate: ${deps.narrate.mode})`));
  setInterval(() => void deps.safety.sweep(), 15_000).unref();
}
