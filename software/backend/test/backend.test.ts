import { afterAll, beforeAll, describe, expect, it } from "vitest";
import type { AddressInfo } from "node:net";
import type { Server } from "node:http";
import { createApp, type AppDeps } from "../src/server.ts";
import { loadPack, PackIndex } from "../src/pack.ts";
import { NarrateService, type MessagesClient } from "../src/narrate.ts";
import { MockSearchAdapter } from "../src/adapters/search.ts";
import { MockHotelAdapter } from "../src/adapters/hotels.ts";
import { MockNotifier, SafetyService } from "../src/safety.ts";

const index = new PackIndex(loadPack());
let clockMs = 1_700_000_000_000;
const notifier = new MockNotifier();
const deps: AppDeps = {
  index,
  narrate: new NarrateService(index.byId, null),
  search: new MockSearchAdapter(),
  hotels: new MockHotelAdapter(),
  safety: new SafetyService(notifier, () => clockMs),
};
let server: Server;
let base = "";
beforeAll(async () => {
  server = createApp(deps);
  await new Promise<void>((r) => server.listen(0, r));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
afterAll(() => new Promise<void>((r) => server.close(() => r())));
const post = (p: string, body: unknown) => fetch(base + p, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });

describe("backend (mock mode)", () => {
  it("health", async () => {
    const j = await (await fetch(`${base}/health`)).json();
    expect(j).toMatchObject({ ok: true, city: "rome", narrate_mode: "mock" });
  });

  it("nearby sorts by distance", async () => {
    const j = await (await fetch(`${base}/nearby?lat=41.8986&lng=12.4769&radius=200`)).json();
    expect(j.items[0].id).toBe("rome-pantheon");
    expect(j.items.every((x: any, i: number, a: any[]) => i === 0 || a[i - 1].distance_m <= x.distance_m)).toBe(true);
    expect((await fetch(`${base}/nearby?lat=abc&lng=1`)).status).toBe(400);
  });

  it("narrate (mock) returns a guarded template script", async () => {
    const r = await post("/narrate", { poi_id: "rome-trevi-fountain", fact_ids: ["rome-trevi-fountain-1"], persona: "historian", direction: "left" });
    const j = await r.json();
    expect(j.mode).toBe("mock");
    expect(j.script.factIds).toEqual(["rome-trevi-fountain-1"]);
    expect(j.script.speechText.toLowerCase()).toContain("on your left");
    expect((await post("/narrate", { poi_id: "nope" })).status).toBe(400);
    expect((await post("/narrate", { poi_id: "rome-trevi-fountain", fact_ids: ["rome-pantheon-1"] })).status).toBe(400);
  });

  it("search and hotels adapters (mock, labelled)", async () => {
    const s = await (await fetch(`${base}/search?q=Pantheon%20opening%20hours`)).json();
    expect(s.adapter).toBe("mock");
    expect(s.results[0].title).toMatch(/MOCK/);
    const h = await (await fetch(`${base}/hotels?lat=41.9&lng=12.48&max_price_eur=200`)).json();
    expect(h.offers.length).toBe(3);
    expect(h.offers.every((o: any) => o.simulated && o.price_per_night_eur <= 200)).toBe(true);
  });

  it("walk-me-home: start, E2E location, overdue escalation once, check-in", async () => {
    const r = await post("/safety/walk-home", { user_id: "u1", eta_minutes: 20, contacts: ["+39000000"] });
    expect(r.status).toBe(201);
    const t = await r.json();
    const token = t.share_url_base.split("/").pop();
    expect((await post(`/safety/walk-home/${t.id}/location`, { ciphertext: '{"lat":41.9}' })).status).toBe(400);
    expect((await post(`/safety/walk-home/${t.id}/location`, { ciphertext: "A".repeat(48) })).status).toBe(202);
    let v = await (await fetch(`${base}/s/${token}`)).json();
    expect(v).toMatchObject({ status: "active", count: 1 });
    clockMs += 21 * 60_000;
    v = await (await fetch(`${base}/safety/walk-home/${t.id}`)).json();
    expect(v.status).toBe("overdue");
    await fetch(`${base}/safety/walk-home/${t.id}`);
    expect(notifier.sent.length).toBe(1);
    expect((await (await post(`/safety/walk-home/${t.id}/checkin`, {})).json()).status).toBe("checked_in");
    expect((await post("/safety/walk-home", { eta_minutes: 0, contacts: [] })).status).toBe(400);
    expect((await fetch(`${base}/safety/walk-home/missing`)).status).toBe(404);
  });
});

describe("NarrateService with a fake Claude client (tool loop + guard)", () => {
  function fakeClient(finalText: string): MessagesClient & { calls: any[] } {
    const calls: any[] = [];
    return {
      calls,
      beta: {
        messages: {
          async create(params: any) {
            calls.push(params);
            if (calls.length === 1)
              return { content: [{ type: "tool_use", id: "tu1", name: "get_fact_cards", input: { poi_id: "rome-trevi-fountain" } }], stop_reason: "tool_use" } as any;
            return { content: [{ type: "text", text: finalText }], stop_reason: "end_turn" } as any;
          },
        },
      },
    };
  }

  it("accepts faithful, cited output and sends the right request shape", async () => {
    const c = fakeClient("On your left is the Trevi Fountain. Nicola Salvi designed it and Giuseppe Pannini completed it in 1762. [f:rome-trevi-fountain-1]");
    const svc = new NarrateService(index.byId, c);
    const r = await svc.narrate({ poi_id: "rome-trevi-fountain", fact_ids: ["rome-trevi-fountain-1"], direction: "left" });
    expect(r.mode).toBe("llm");
    expect(r.tool_calls).toEqual(["get_fact_cards"]);
    expect(c.calls[0].model).toBe("claude-sonnet-5-5");
    expect(c.calls[0].fallbacks).toBe("default");
    const toolResult = c.calls[1].messages[2].content[0];
    expect(JSON.parse(toolResult.content)).toHaveLength(1);
  });

  it("rejects hallucinated output and falls back to the template", async () => {
    const svc = new NarrateService(index.byId, fakeClient("Built in 1699 by Michelangelo. [f:rome-trevi-fountain-1]"));
    const r = await svc.narrate({ poi_id: "rome-trevi-fountain", fact_ids: ["rome-trevi-fountain-1"] });
    expect(r.mode).toBe("llm-fallback-template");
    expect(r.guard?.ok).toBe(false);
    expect(r.script.mode).toBe("template");
  });
});
