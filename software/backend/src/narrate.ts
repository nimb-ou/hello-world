/**
 * /narrate: cloud narration with Claude tool calling, guarded to verified fact cards.
 *
 * Flow: client sends poi_id + the fact_ids the on-device Story Engine selected. Claude may call
 *   get_fact_cards (returns ONLY those facts) and get_live_info (live data, labelled), then writes
 *   the narration with [f:ID] citations. The output passes core's validateNarration() guard or we
 *   fall back to the deterministic template. No ANTHROPIC_API_KEY -> mock mode (template only).
 */
import Anthropic from "@anthropic-ai/sdk";
import {
  buildNarrationPrompt, finalizeLLMNarration, templateNarration, type Direction, type FactCard, type LiveInfo,
  type NarrationInput, type NarrationScript, type Persona, type Poi, type StoryTier,
} from "../../packages/core/src/index.ts";

export const DEFAULT_MODEL = process.env.LORE_MODEL ?? "claude-sonnet-5-5";

export interface NarrateRequest {
  poi_id: string;
  fact_ids?: string[];
  persona?: Persona;
  tier?: StoryTier;
  direction?: Direction | null;
  distance_m?: number;
  follow_up?: "tell-me-more" | "related";
}
export interface NarrateResponse {
  script: NarrationScript;
  mode: "mock" | "llm" | "llm-fallback-template";
  model?: string;
  guard?: { ok: boolean; problems: string[] };
  tool_calls: string[];
}

/** Minimal surface of the SDK we use, so tests can inject a fake. */
export interface MessagesClient {
  beta: { messages: { create(params: Anthropic.Beta.MessageCreateParamsNonStreaming): Promise<Anthropic.Beta.BetaMessage> } };
}

export type LiveInfoProvider = (poi: Poi) => Promise<LiveInfo[]>;
export const mockLiveInfo: LiveInfoProvider = async () => [];

const TOOLS: Anthropic.Beta.BetaTool[] = [
  {
    name: "get_fact_cards",
    description: "Return the verified fact cards you are allowed to use for this place. Call this before writing. Facts outside this list must never be stated.",
    input_schema: { type: "object", properties: { poi_id: { type: "string" } }, required: ["poi_id"], additionalProperties: false },
    strict: true,
  },
  {
    name: "get_live_info",
    description: "Return current live information (opening hours, closures, events) for the place, each with a source. Optional.",
    input_schema: { type: "object", properties: { poi_id: { type: "string" } }, required: ["poi_id"], additionalProperties: false },
    strict: true,
  },
];

export class NarrateService {
  constructor(
    private pois: Map<string, Poi>,
    private client: MessagesClient | null,
    private liveInfo: LiveInfoProvider = mockLiveInfo,
    private model = DEFAULT_MODEL,
  ) {}

  static fromEnv(pois: Map<string, Poi>, liveInfo?: LiveInfoProvider): NarrateService {
    const key = process.env.ANTHROPIC_API_KEY;
    return new NarrateService(pois, key ? (new Anthropic({ apiKey: key }) as unknown as MessagesClient) : null, liveInfo);
  }

  get mode(): "mock" | "llm" {
    return this.client ? "llm" : "mock";
  }

  buildInput(req: NarrateRequest): NarrationInput {
    const poi = this.pois.get(req.poi_id);
    if (!poi) throw new RangeError(`unknown poi_id ${req.poi_id}`);
    let facts: FactCard[];
    if (req.fact_ids?.length) {
      facts = poi.facts.filter((f) => req.fact_ids!.includes(f.id));
      if (facts.length !== req.fact_ids.length) throw new RangeError("fact_ids must belong to poi_id");
    } else facts = poi.facts.filter((f) => f.depth === 1);
    return {
      poi,
      facts,
      tier: req.tier ?? "short",
      persona: req.persona ?? "local-friend",
      direction: req.direction ? { direction: req.direction, lookUp: facts.some((f) => f.look_up), distanceM: req.distance_m } : undefined,
      directionReliable: !!req.direction,
      followUp: req.follow_up,
    };
  }

  async narrate(req: NarrateRequest): Promise<NarrateResponse> {
    const input = this.buildInput(req);
    if (!this.client) return { script: templateNarration(input), mode: "mock", tool_calls: [] };

    const prompt = buildNarrationPrompt(input);
    const toolCalls: string[] = [];
    const messages: Anthropic.Beta.BetaMessageParam[] = [
      { role: "user", content: `${prompt.user}\n\nFirst call get_fact_cards for poi_id "${input.poi.id}" (and optionally get_live_info), then write the narration.` },
    ];
    let live: LiveInfo[] = [];
    let text = "";
    for (let i = 0; i < 4; i++) {
      const res = await this.client.beta.messages.create({
        model: this.model,
        max_tokens: 2000,
        system: prompt.system,
        tools: TOOLS,
        tool_choice: { type: "auto" },
        output_config: { effort: "low" },
        betas: ["server-side-fallback-2026-07-01"],
        fallbacks: "default",
        messages,
      } as Anthropic.Beta.MessageCreateParamsNonStreaming);
      if (res.stop_reason === "refusal") break;
      messages.push({ role: "assistant", content: res.content as Anthropic.Beta.BetaContentBlockParam[] });
      const uses = res.content.filter((b): b is Anthropic.Beta.BetaToolUseBlock => b.type === "tool_use");
      if (res.stop_reason !== "tool_use" || uses.length === 0) {
        text = res.content.map((b) => (b.type === "text" ? b.text : "")).join("").trim();
        break;
      }
      const results: Anthropic.Beta.BetaToolResultBlockParam[] = [];
      for (const u of uses) {
        toolCalls.push(u.name);
        const askedId = (u.input as { poi_id?: string }).poi_id;
        if (askedId !== input.poi.id) {
          results.push({ type: "tool_result", tool_use_id: u.id, is_error: true, content: `Only poi_id ${input.poi.id} is available.` });
        } else if (u.name === "get_fact_cards") {
          const facts = input.facts.map((f) => ({ id: f.id, text: f.text, legend: !!f.is_legend, look_up: !!f.look_up }));
          results.push({ type: "tool_result", tool_use_id: u.id, content: JSON.stringify(facts) });
        } else if (u.name === "get_live_info") {
          live = await this.liveInfo(input.poi);
          results.push({ type: "tool_result", tool_use_id: u.id, content: JSON.stringify(live.map((l) => ({ text: l.text, source: l.source }))) });
        } else {
          results.push({ type: "tool_result", tool_use_id: u.id, is_error: true, content: "unknown tool" });
        }
      }
      messages.push({ role: "user", content: results });
    }
    const finalInput = { ...input, live };
    if (!text) return { script: templateNarration(finalInput), mode: "llm-fallback-template", model: this.model, guard: { ok: false, problems: ["no text from model"] }, tool_calls: toolCalls };
    const { script, validation } = finalizeLLMNarration(text, finalInput);
    return {
      script,
      mode: script.mode === "llm" ? "llm" : "llm-fallback-template",
      model: this.model,
      guard: { ok: validation.ok, problems: validation.problems },
      tool_calls: toolCalls,
    };
  }
}
