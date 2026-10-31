/**
 * Narration: turns selected fact cards into a spoken script.
 *
 * Two paths, same contract:
 *  1. LLM path (on-device 3B model or cloud Claude): `buildNarrationPrompt()` produces a prompt
 *     that only allows the supplied fact cards, requires [f:ID] citations, and
 *     `validateNarration()` rejects any output that cites unknown facts, introduces numbers
 *     not present in the facts, or names proper nouns that are not in the facts.
 *  2. Deterministic template path (offline / guard failure): `templateNarration()` builds the
 *     script directly from fact text. It cannot hallucinate because it only concatenates facts.
 */
import { directionPhrase, type DirectionClassification } from "./geo.ts";
import type { FactCard, FactSource, LiveInfo, Persona, Poi, StoryTier } from "./types.ts";
import { wordCount } from "./story-engine.ts";

export interface NarrationInput {
  poi: Poi;
  facts: FactCard[];
  tier: StoryTier;
  persona: Persona;
  direction?: Pick<DirectionClassification, "direction" | "lookUp"> & { distanceM?: number };
  directionReliable?: boolean;
  live?: LiveInfo[];
  /** "tell me more" / related follow-up. */
  followUp?: "tell-me-more" | "related";
}

export interface NarrationScript {
  /** Text with [f:ID] citations (for logs / transparency UI). */
  text: string;
  /** Clean text for TTS. */
  speechText: string;
  factIds: string[];
  sources: FactSource[];
  estimatedSec: number;
  mode: "template" | "llm";
  persona: Persona;
  tier: StoryTier;
}

export const PERSONAS: Record<Persona, { label: string; description: string; wpm: number }> = {
  "local-friend": { label: "Local friend", description: "Warm, witty, a friend who grew up here.", wpm: 155 },
  historian: { label: "Historian", description: "Precise, calm, dates and names first.", wpm: 145 },
  storyteller: { label: "Storyteller", description: "Cinematic, unhurried, sets the scene.", wpm: 140 },
  minimalist: { label: "Minimalist", description: "Just the facts. Shortest possible.", wpm: 160 },
};

const LEGEND_RE = /\b(legend|tradition|traditionally|said to|story goes|reputed|popular belief|myth|according to|story says|popular story)\b/i;

function cap(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Deterministic pick so the same POI always gets the same opener variant (stable tests/logs). */
function pick<T>(arr: T[], key: string): T {
  let h = 0;
  for (let i = 0; i < key.length; i++) h = (h * 31 + key.charCodeAt(i)) >>> 0;
  return arr[h % arr.length];
}

function where(input: NarrationInput): string {
  if (!input.direction || input.directionReliable === false) return "nearby";
  return directionPhrase(input.direction, input.direction.distanceM);
}

const ARTICLE_RE = /^(Pantheon|Colosseum|Fountain|Basilica|Church|Temple|Theatre|Arch|Column|Mausoleum|Baths|Pyramid|Keyhole|Orange|Great|Capuchin|Victor|Obelisk|Portico|Non-Catholic|Spanish|Roman|Palatine|Circus|Elephant|Turtle|Triton|Tiber|Pincio|Quattro Fontane|Ara Pacis|Domus|Bocca)\b/;

/** "Fountain of the Four Rivers" -> "the Fountain of the Four Rivers"; Italian proper names unchanged. */
export function withArticle(name: string): string {
  return ARTICLE_RE.test(name) ? `the ${name}` : name;
}

function opener(input: NarrationInput): string {
  const name = withArticle(input.poi.name);
  const w = where(input);
  const W = cap(w);
  if (input.followUp === "tell-me-more") {
    return {
      "local-friend": `Okay, more on ${name}.`,
      historian: `Further notes on ${name}.`,
      storyteller: `There's more to ${name}.`,
      minimalist: `${name}, continued.`,
    }[input.persona];
  }
  if (input.followUp === "related") {
    return {
      "local-friend": `Since you liked that, here's a related one: ${name}, ${w}.`,
      historian: `A related site: ${name}, ${w}.`,
      storyteller: `And that thread leads us to ${name}, ${w}.`,
      minimalist: `Related: ${name}, ${w}.`,
    }[input.persona];
  }
  const variants: Record<Persona, string[]> = {
    "local-friend": [`${W}, that's ${name}.`, `See ${name} ${w}?`, `Quick one: ${name} is ${w}.`],
    historian: [`${W}: ${name}.`, `${name}, ${w}.`],
    storyteller: [`Slow down for a moment. ${W} is ${name}.`, `${W}, ${name} is waiting for you.`],
    minimalist: [`${name}, ${w}.`],
  };
  return pick(variants[input.persona], input.poi.id + input.persona);
}

function legendHedge(p: Persona): string {
  return { "local-friend": "Locals will tell you this:", historian: "According to tradition:", storyteller: "Legend has it:", minimalist: "Legend:" }[p];
}

function connector(p: Persona, i: number): string {
  if (i === 0) return "";
  const c: Record<Persona, string[]> = {
    "local-friend": ["And here's the fun part:", "Also,", "One more thing:"],
    historian: ["Additionally,", "Note also:", "Further,"],
    storyteller: ["Now picture this:", "And then,", "Here's the twist:"],
    minimalist: [""],
  };
  const arr = c[p];
  return arr[(i - 1) % arr.length];
}

function joinConnector(conn: string, sentence: string): string {
  if (!conn) return sentence;
  if (conn.endsWith(",")) return `${conn} ${sentence.charAt(0).toLowerCase()}${sentence.slice(1)}`;
  return `${conn} ${sentence}`;
}

export function stripCitations(text: string): string {
  return text.replace(/\s*\[f:[^\]]+\]/g, "").replace(/\s{2,}/g, " ").trim();
}

export function estimateSeconds(text: string, wpm = 150): number {
  return Math.max(1, Math.round((wordCount(stripCitations(text)) / wpm) * 60));
}

function collectSources(facts: FactCard[]): FactSource[] {
  const seen = new Map<string, FactSource>();
  for (const f of facts) for (const s of f.sources) if (!seen.has(s.url)) seen.set(s.url, s);
  return [...seen.values()];
}

/** Deterministic, hallucination-free narration from fact cards. */
export function templateNarration(input: NarrationInput): NarrationScript {
  const parts: string[] = [opener(input)];
  const facts = input.persona === "minimalist" && input.tier === "short" ? input.facts.slice(0, 1) : input.facts;
  facts.forEach((f, i) => {
    let sentence = f.text.trim();
    if (f.is_legend && !LEGEND_RE.test(sentence)) sentence = `${legendHedge(input.persona)} ${sentence}`;
    if (f.look_up && input.directionReliable !== false)
      sentence = `${input.direction?.direction === "behind" ? "Turn around and look up." : "Look up."} ${sentence}`;
    else sentence = joinConnector(connector(input.persona, i), sentence);
    parts.push(`${sentence} [f:${f.id}]`);
  });
  for (const l of input.live ?? []) parts.push(`Right now: ${l.text}`);
  if (input.tier !== "deep" && input.persona !== "minimalist" && input.poi.facts.length > facts.length) {
    parts.push({ "local-friend": "Say 'tell me more' if you want the rest.", historian: "Ask for more detail if you wish.", storyteller: "There's more, if you want it.", minimalist: "" }[input.persona]);
  }
  const text = parts.filter(Boolean).join(" ");
  return {
    text,
    speechText: stripCitations(text),
    factIds: facts.map((f) => f.id),
    sources: collectSources(facts),
    estimatedSec: estimateSeconds(text, PERSONAS[input.persona].wpm),
    mode: "template",
    persona: input.persona,
    tier: input.tier,
  };
}

export interface NarrationPrompt {
  system: string;
  user: string;
  allowedFactIds: string[];
  maxWords: number;
}

const TIER_WORDS: Record<StoryTier, number> = { short: 55, medium: 105, deep: 260 };

/**
 * Prompt for the LLM path. Works for the on-device model (llama.cpp chat template) and for Claude.
 * The model may rephrase and connect facts, never add new claims.
 */
export function buildNarrationPrompt(input: NarrationInput): NarrationPrompt {
  const maxWords = TIER_WORDS[input.tier];
  const persona = PERSONAS[input.persona];
  const system = [
    "You are LORE, a pocket travel companion speaking into the listener's earphones while they walk.",
    `Persona: ${persona.label} - ${persona.description}`,
    "HARD RULES:",
    "1. Use ONLY the facts in <facts>. Do not add any date, number, name, place, quote or claim that is not in them.",
    "2. After every sentence that uses a fact, append its citation tag exactly as given, e.g. [f:rome-pantheon-1].",
    "3. Facts marked legend=true must be told as legend or tradition, never as established history.",
    "4. Use the direction phrase given in <where> exactly once; do not invent other directions.",
    "5. If a fact has look_up=true and <where> is not 'nearby', tell the listener to look up.",
    `6. At most ${maxWords} words. Spoken style: short sentences, no lists, no markdown, no emoji.`,
    "7. If the facts are insufficient, say less. Never guess.",
  ].join("\n");
  const facts = input.facts
    .map((f) => `<fact id="${f.id}" legend="${!!f.is_legend}" look_up="${!!f.look_up}">${f.text}</fact>`)
    .join("\n");
  const live = (input.live ?? []).map((l) => `<live source="${l.source}">${l.text}</live>`).join("\n");
  const user = [
    `<place>${input.poi.name}</place>`,
    `<where>${where(input)}</where>`,
    `<tier>${input.tier}${input.followUp ? ` (${input.followUp})` : ""}</tier>`,
    `<facts>\n${facts}\n</facts>`,
    live ? `<live_info>\n${live}\n</live_info>\nLive info may be mentioned without a citation, prefixed with "Right now".` : "",
    "Write the narration now.",
  ]
    .filter(Boolean)
    .join("\n");
  return { system, user, allowedFactIds: input.facts.map((f) => f.id), maxWords };
}

export interface ValidationResult {
  ok: boolean;
  problems: string[];
  citedFactIds: string[];
}

/** Words that may appear capitalised mid-sentence without being in the facts. */
const PROPER_NOUN_ALLOW = new Set([
  "I", "LORE", "According", "Turn", "Tradition", "Rome", "Roman", "Romans", "Look", "Right", "Okay", "Legend", "Locals", "And", "But", "So", "Now", "Here",
  "Also", "Note", "Further", "Additionally", "There", "This", "That", "The", "It", "Its", "Say", "Ask", "Quick", "See",
  "Slow", "One", "Since", "A", "An", "If", "You", "Your", "Just", "On", "In", "Behind", "Ahead", "Today", "Tonight",
]);

function numbersIn(s: string): string[] {
  return (s.match(/\d[\d,.]*/g) ?? []).map((n) => n.replace(/[.,]$/, "").replace(/,/g, ""));
}

/**
 * Anti-hallucination guard for LLM output. Conservative by design: a false rejection costs us a
 * template narration; a false acceptance costs user trust.
 */
export function validateNarration(text: string, input: Pick<NarrationInput, "facts" | "poi" | "live" | "tier">): ValidationResult {
  const problems: string[] = [];
  const allowed = new Set(input.facts.map((f) => f.id));
  const cited = [...text.matchAll(/\[f:([^\]]+)\]/g)].map((m) => m[1]);
  if (cited.length === 0) problems.push("no fact citations");
  for (const id of cited) if (!allowed.has(id)) problems.push(`cites unknown fact ${id}`);

  const corpus = [input.poi.name, ...input.facts.map((f) => f.text), ...(input.live ?? []).map((l) => l.text)].join(" ");
  const corpusNums = new Set(numbersIn(corpus));
  for (const n of numbersIn(stripCitations(text))) if (!corpusNums.has(n)) problems.push(`number not in facts: ${n}`);

  const corpusWords = new Set(corpus.split(/[^\p{L}\p{N}'’-]+/u).filter(Boolean));
  const clean = stripCitations(text);
  for (const sentence of clean.split(/(?<=[.!?])\s+/)) {
    const words = sentence.split(/\s+/).map((w) => w.replace(/^[^\p{L}]+|[^\p{L}'’-]+$/gu, "")).filter(Boolean);
    words.forEach((w, i) => {
      if (i === 0) return;
      if (!/^\p{Lu}/u.test(w)) return;
      if (PROPER_NOUN_ALLOW.has(w) || corpusWords.has(w)) return;
      const base = w.replace(/['’]s$/, "");
      if (corpusWords.has(base)) return;
      problems.push(`proper noun not in facts: ${w}`);
    });
  }
  const limit = Math.round(TIER_WORDS[input.tier] * 1.4);
  if (wordCount(clean) > limit) problems.push(`too long: ${wordCount(clean)} words > ${limit}`);
  return { ok: problems.length === 0, problems, citedFactIds: [...new Set(cited)] };
}

/** Wrap validated LLM text into a script; falls back to the template on any guard failure. */
export function finalizeLLMNarration(llmText: string, input: NarrationInput): { script: NarrationScript; validation: ValidationResult } {
  const validation = validateNarration(llmText, input);
  if (!validation.ok) return { script: templateNarration(input), validation };
  const used = input.facts.filter((f) => validation.citedFactIds.includes(f.id));
  return {
    script: {
      text: llmText.trim(),
      speechText: stripCitations(llmText),
      factIds: used.map((f) => f.id),
      sources: collectSources(used),
      estimatedSec: estimateSeconds(llmText, PERSONAS[input.persona].wpm),
      mode: "llm",
      persona: input.persona,
      tier: input.tier,
    },
    validation,
  };
}
