/**
 * Web search adapter interface. Production candidates: Claude's server-side web_search tool (below),
 * Brave Search API, or Exa. All results are LIVE INFO, never fact cards: they are shown/spoken with
 * a "right now" prefix and a source, and never enter the verified City Pack without editorial review.
 */
import Anthropic from "@anthropic-ai/sdk";

export interface SearchResult {
  title: string;
  url: string;
  snippet: string;
  source: string;
}
export interface WebSearchAdapter {
  readonly name: string;
  search(query: string, opts?: { near?: { lat: number; lng: number }; limit?: number }): Promise<SearchResult[]>;
}

export class MockSearchAdapter implements WebSearchAdapter {
  readonly name = "mock";
  async search(query: string, opts: { limit?: number } = {}): Promise<SearchResult[]> {
    const q = query.toLowerCase();
    const base: SearchResult[] = [
      { title: `[MOCK] Opening hours: ${query}`, url: "https://example.com/mock/opening-hours", snippet: "Simulated result. Real adapter returns live opening hours.", source: "mock" },
      { title: `[MOCK] Events near ${query}`, url: "https://example.com/mock/events", snippet: "Simulated result. No real event data.", source: "mock" },
    ];
    if (q.includes("weather")) base.unshift({ title: "[MOCK] Rome weather", url: "https://example.com/mock/weather", snippet: "Simulated: 21 C, clear.", source: "mock" });
    return base.slice(0, opts.limit ?? 5);
  }
}

/** Uses Claude's server-side web search tool; requires ANTHROPIC_API_KEY. */
export class ClaudeWebSearchAdapter implements WebSearchAdapter {
  readonly name = "claude-web-search";
  constructor(private client: Anthropic, private model = process.env.LORE_MODEL ?? "claude-sonnet-5-5") {}
  async search(query: string, opts: { limit?: number } = {}): Promise<SearchResult[]> {
    const res = await this.client.messages.create({
      model: this.model,
      max_tokens: 2048,
      output_config: { effort: "low" },
      tools: [{ type: "web_search_20260209", name: "web_search", max_uses: 2 }],
      messages: [{ role: "user", content: `Search the web for: ${query}. Reply with one short line per useful result.` }],
    } as Anthropic.MessageCreateParamsNonStreaming);
    const out: SearchResult[] = [];
    for (const block of res.content) {
      if (block.type === "web_search_tool_result" && Array.isArray(block.content)) {
        for (const r of block.content) if (r.type === "web_search_result") out.push({ title: r.title, url: r.url, snippet: r.page_age ?? "", source: "web_search" });
      }
    }
    return out.slice(0, opts.limit ?? 5);
  }
}
