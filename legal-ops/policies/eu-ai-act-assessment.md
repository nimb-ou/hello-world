# EU AI Act (Regulation (EU) 2024/1689): LORE Obligations Assessment (DRAFT v0.1)

> **DRAFT. NOT LEGAL ADVICE.** Counsel must review this preliminary classification. Items marked [S] were checked by web search on 30 Oct 2026. Items marked [verify] were not.

## 1. Timeline (as currently understood)
| Date | Obligation | Source |
|---|---|---|
| 2 Feb 2025 | Prohibited practices (Art. 5) + AI literacy (Art. 4) apply | [S] |
| 2 Aug 2025 | GPAI model provider obligations (Arts 53–55) apply | [S] |
| **2 Aug 2026** | **Art. 50 transparency obligations apply.** Commission Art. 50 Guidelines adopted 20 Jul 2026; Code of Practice on transparency of AI-generated content finalised 10 Jun 2026 | [S] |
| 2 Dec 2027 | High-risk Annex III obligations (moved from Aug 2026 by the **Digital Omnibus**; political agreement 7 May 2026; reportedly in force since late Jul 2026, so confirm in the OJ) | [S] |
| 2 Aug 2028 | High-risk Annex I (product-embedded) obligations | [S] |

## 2. LORE's AI systems and roles
| System | Role under the Act | Risk class (preliminary) | Reasoning |
|---|---|---|---|
| Story engine (LLM narration, on-device + cloud) | **Provider** of an AI system placed on the EU market under our own name; **deployer** for our own use | **Limited risk (Art. 50)** | Interacts directly with people (50(1)) and generates synthetic audio/text (50(2)) |
| Voice Q&A assistant | Provider | Limited risk (50(1)) | Conversational AI |
| Synthetic TTS voice | Provider | 50(2): machine-readable marking of synthetic audio (where technically feasible); 50(4) deepfake rules if we imitate a real person's voice (**don't**, unless licensed and disclosed) | |
| Map Vision sensor fusion (non-ML or ML) | Provider | Minimal risk | Not in Annex III; not a safety component of an Annex I product (consumer electronics aren't under Annex I machinery/toy/medical, etc. [verify: the radio-equipment link]) |
| Quiet-moment detection (VAD, gait) | Provider | Minimal risk | Not emotion recognition: detects **speech presence**, not emotions. **Don't add emotion inference** (Art. 50(3) duties; and emotion recognition in some contexts is prohibited, though not in consumer leisure use) |
| Atlas Glance (building recognition) | Provider | Minimal risk. **Must not do remote biometric identification** (Annex III(1)) or untargeted facial scraping (Art. 5(1)(e), prohibited) | On-device face blur |
| Safety features (SOS) | Provider | Minimal; **not** "AI system used to dispatch emergency first-response services" (Annex III(5)(d)), because we only alert user-chosen contacts. **If** a future feature uses AI to triage/prioritise emergency calls for emergency services, it becomes **high-risk** | Design guardrail |
| Accessibility version for blind/low-vision walkers (later) | Provider | Re-assess: possible medical-device questions (MDR) if marketed as assistive tech for a disability; likely still minimal under the AI Act | Re-assess before launch |
| Fine-tuned open models (Llama/Gemma/Qwen) distributed on-device | Possibly **GPAI "downstream modifier"**. Becomes a GPAI provider only if the modification is substantial (Commission GPAI guidelines: indicative threshold of more than one-third of the original model's training compute) [verify] | Our LoRA fine-tunes are far below that, so we're **not** a GPAI provider; we rely on the upstream provider's documentation | |

## 3. Obligations we must meet

### 3.1 Art. 50(1): tell people they're interacting with AI
- First-run onboarding: "*LORE's voice is an AI. It's built to stick to checked facts, but it can make mistakes.*"
- Periodic gentle reminder? Not required if obvious from context, but we'll include **"AI narrator" labelling** in the app and on the packaging, and the device's voice introduces itself ("I'm LORE, your AI guide") on first use and after a factory reset.
- Accessible to blind users (spoken disclosure, not only on-screen).

### 3.2 Art. 50(2): mark synthetic content
- Synthetic audio and text outputs: **machine-readable marking** where technically feasible (e.g., audio watermarking via TTS provider, C2PA metadata for any exported audio/images, text metadata in shared story cards).
- Consider signing the **Code of Practice on transparency of AI-generated content** (voluntary; ~190 signatories by Aug 2026 [S]) as the compliance route, or document an alternative.
- Exception: AI performing an "assistive function for standard editing" doesn't apply to us, since we generate content.

### 3.3 Art. 4: AI literacy
- Staff training on AI risks for everyone working on/with the AI systems (record attendance). Content: hallucination, bias in historical narratives (colonial framing, contested history), privacy, safety gating.

### 3.4 Art. 5: prohibited practices to avoid
- No manipulative or deceptive techniques that distort behaviour (e.g., using narration to push affiliate bookings in a way that undermines informed decisions). **Affiliate recommendations must be labelled "Partner"** and must not be inserted into "factual" stories without disclosure (also UCPD).
- No exploitation of vulnerabilities (age, disability).
- No untargeted facial-image scraping; no biometric categorisation.

### 3.5 Voluntary good practice (supports product-liability defence under the new PLD)
- Model cards and an eval suite: factual accuracy rate (target ≥98% verified claims), hallucination rate, toxicity, bias review of narratives in each City Pack.
- Human editorial review of the top-200 stories per city.
- Incident logging for harmful outputs; fixes through City Pack updates.

## 4. Interaction with other laws
- **GDPR** (DPIA covers AI processing). **DSA** (if UGC is public). **Product Liability Directive 2024/2853** (software and AI are "products"; defects include failure to provide security updates). **Unfair Commercial Practices Directive** (affiliate disclosures). **Copyright/DSM Directive Art. 4** (TDM opt-outs respected for fine-tuning data).
- UK: no AI Act; the ICO AI guidance and the CMA apply. US: FTC Act §5 (deceptive AI claims). Don't claim "never wrong" or "100% accurate".

## 5. Owner and review
Owner: COO + Head of Software. Review: each model change or new AI feature, and at least every 6 months.
