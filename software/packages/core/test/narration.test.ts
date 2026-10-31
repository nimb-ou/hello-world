import { describe, expect, it } from "vitest";
import { buildNarrationPrompt, finalizeLLMNarration, stripCitations, templateNarration, validateNarration, type NarrationInput } from "../src/narration.ts";
import { loadRomePack } from "./helpers.ts";

const pack = loadRomePack();
const trevi = pack.pois.find((p) => p.id === "rome-trevi-fountain")!;
const base: NarrationInput = {
  poi: trevi,
  facts: trevi.facts.slice(0, 2),
  tier: "short",
  persona: "local-friend",
  direction: { direction: "right", lookUp: false, distanceM: 60 },
  directionReliable: true,
};

describe("templateNarration", () => {
  it("only contains fact text plus persona scaffolding, with citations", () => {
    const s = templateNarration(base);
    expect(s.mode).toBe("template");
    expect(s.text).toContain("on your right");
    for (const f of base.facts) {
      expect(s.text).toContain(`[f:${f.id}]`);
      expect(s.speechText).toContain(f.text.slice(1, 30));
    }
    expect(s.speechText).not.toMatch(/\[f:/);
    expect(s.sources[0].url).toMatch(/^https:\/\//);
    expect(s.estimatedSec).toBeGreaterThan(5);
  });

  it("passes its own hallucination guard for every persona and POI", () => {
    for (const persona of ["local-friend", "historian", "storyteller", "minimalist"] as const) {
      for (const poi of pack.pois) {
        const input: NarrationInput = { ...base, poi, facts: poi.facts, tier: "deep", persona };
        const s = templateNarration(input);
        const v = validateNarration(s.text, input);
        expect(v.problems, `${persona} ${poi.id}`).toEqual([]);
      }
    }
  });

  it("hedges legends and says 'look up'", () => {
    const legend = trevi.facts.find((f) => f.is_legend)!;
    const s = templateNarration({ ...base, facts: [legend] });
    expect(s.speechText).toMatch(/Tradition says/);
    const pantheon = pack.pois.find((p) => p.id === "rome-pantheon")!;
    const lu = pantheon.facts.find((f) => f.look_up)!;
    expect(templateNarration({ ...base, poi: pantheon, facts: [lu] }).speechText).toContain("Look up.");
    expect(templateNarration({ ...base, poi: pantheon, facts: [lu], directionReliable: false }).speechText).not.toContain("Look up.");
  });

  it("says 'nearby' instead of left/right when heading is unreliable", () => {
    const s = templateNarration({ ...base, directionReliable: false });
    expect(s.speechText).toContain("nearby");
    expect(s.speechText).not.toContain("your right");
  });

  it("appends live info", () => {
    const s = templateNarration({ ...base, live: [{ poi_id: trevi.id, text: "Crowds are light right now.", source: "mock", expires_at: 1 }] });
    expect(s.speechText).toContain("Right now: Crowds are light right now.");
  });
});

describe("LLM prompt + guard", () => {
  it("prompt contains only the allowed facts and the rules", () => {
    const p = buildNarrationPrompt(base);
    expect(p.allowedFactIds).toEqual(base.facts.map((f) => f.id));
    expect(p.system).toMatch(/ONLY the facts/);
    expect(p.user).toContain(base.facts[0].text);
    expect(p.user).not.toContain(trevi.facts[3].text);
    expect(p.user).toContain("<where>on your right</where>");
  });

  it("accepts faithful output", () => {
    const [f1, f2] = base.facts;
    const text = `On your right is the Trevi Fountain. Nicola Salvi designed it, and Giuseppe Pannini completed it in 1762. [f:${f1.id}] Its water arrives on the Aqua Virgo, built by Marcus Agrippa in 19 BC. [f:${f2.id}]`;
    const r = finalizeLLMNarration(text, base);
    expect(r.validation.problems).toEqual([]);
    expect(r.script.mode).toBe("llm");
    expect(stripCitations(r.script.text)).not.toContain("[f:");
  });

  it("rejects invented numbers, names and unknown citations, falling back to template", () => {
    const [f1] = base.facts;
    const bad = `The Trevi Fountain was finished in 1735 by Michelangelo. [f:${f1.id}] [f:rome-fake-9]`;
    const v = validateNarration(bad, base);
    expect(v.ok).toBe(false);
    expect(v.problems.join(" ")).toMatch(/1735/);
    expect(v.problems.join(" ")).toMatch(/Michelangelo/);
    expect(v.problems.join(" ")).toMatch(/rome-fake-9/);
    const r = finalizeLLMNarration(bad, base);
    expect(r.script.mode).toBe("template");
  });

  it("rejects uncited output", () => {
    expect(validateNarration("A lovely fountain.", base).problems).toContain("no fact citations");
  });
});
