# Privacy and Security Programme

> **DRAFT. NOT LEGAL ADVICE.** A qualified privacy lawyer (EU/UK GDPR, US state privacy, India DPDP) must review this programme and every policy in `policies/` before publication. Items marked **[S]** were checked by web search on 30 Oct 2026. Items marked **[V]** come from working knowledge and were not re-checked in this pass. Verify them.

Owner: COO (acting **Privacy Lead**; formal DPO decision in §3). Security lead: Head of Software (until a dedicated security engineer is hired, see `hr-hiring.md`).

**LORE's privacy promise (product principle):** *"LORE knows where you are so it can tell you the story. It doesn't sell where you've been."*
1. **Location stays on the device by default.** Map Vision runs on-device. Offline City Packs mean most narration needs no server round-trip.
2. **No sale or "sharing" of personal data** (CCPA sense). No third-party ad SDKs on device or app.
3. **Trip history is opt-in**, encrypted and deletable in one tap.
4. **Microphone is press-to-talk only.** The always-on "quiet-moment" voice-activity detector runs on-device, keeps **no audio**, and stores only a boolean signal for a few seconds.
5. **Safety data (SOS, live share, walk-me-home) is shared only with people the user chooses**, only while the feature is active.

---

## 1. Personal-data inventory (Record of Processing, Art. 30 GDPR, v0.1)

| # | Data category | Examples | Source | Purpose | Legal basis (GDPR / UK GDPR) | Storage location | Retention (proposal) | Sensitivity |
|---|---|---|---|---|---|---|---|---|
| 1 | Account data | name, email, password hash, language, country | user | provide account, LORE Pass | Contract (6(1)(b)) | Cloud (EU region primary) | life of account + 30 days | Normal |
| 2 | Device identifiers | serial, IMEI, eUICC EID, ICCID, BT MAC | device | activation, eSIM, warranty, theft-lock | Contract; legal obligation (telecom KYC where applicable) | Cloud + connectivity partner | life of device + 6 yrs (warranty/tax) | Normal |
| 3 | **Precise real-time location** (GNSS, heading, step data) | lat/long, heading, speed | device sensors | narration, Map Vision, navigation | **Contract** for core narration *on-device*; **consent** (ePrivacy Art. 5(3)/9 + GDPR 6(1)(a)) where location leaves the device (cloud AI query, live share) | **On device by default**; cloud only per request, transient | Device: rolling 24h buffer, unless trip history is on. Cloud requests: **not stored** beyond 24h in logs (pseudonymised) | **High** (CPRA "sensitive PI"; DPDP; "special risk" per EDPB) |
| 4 | Trip history (opt-in) | routes, places visited, stories heard | device | "My trips" diary, recommendations | Consent | Encrypted cloud (E2E option) | until the user deletes it; auto-delete option at 90 days | High |
| 5 | Safety data | emergency contacts, SOS events, live location share sessions, check-in timers | user/device | safety features | Contract; **vital interests (6(1)(d))** for an actual SOS | Cloud (EU) + partner relay | SOS event logs 13 months (dispute/safety review); live share deleted at session end + 7 days | High |
| 6 | Voice queries | press-to-talk audio → transcript | user | answer questions | Contract; **no voice training without separate opt-in consent** | On-device ASR preferred; cloud ASR transient | Audio: not stored (deleted after transcription). Transcripts 30 days for debugging unless opt-in | High (voice can be biometric if used for identification; **we don't**) |
| 7 | Quiet-moment VAD signal | speech present yes/no | mic | pause narration | Legitimate interests (safety/UX); ePrivacy "strictly necessary" for the service requested | On-device RAM only | seconds | Low (no content) |
| 8 | Camera "Glance" (Atlas) | images of facades | user-initiated | identify building | Contract (user-initiated) | On-device vision; cloud only with consent | Not stored by default | High (bystanders' faces possible → blur on-device) |
| 9 | Payment data | card tokens, billing address | user | purchases, LORE Pass | Contract; legal obligation (tax) | **Stripe / Shopify Payments** (PCI DSS); we hold tokens only | 10 yrs for invoices (tax law, e.g., DE/IT) | Normal (PCI) |
| 10 | Support data | tickets, chat, call recordings | user | support, RMA | Contract; legitimate interests | Zendesk/Intercom | 3 yrs after closure | Normal |
| 11 | Telemetry / diagnostics | crash logs, battery stats, GNSS fix quality | device | reliability, safety | Legitimate interests (with opt-out); **consent** where ePrivacy Art. 5(3) needs it (non-essential) | Cloud | 13 months, then aggregated | Low–Medium |
| 12 | Marketing data | newsletter, Kickstarter backer list, referral | user | marketing | Consent (EU/UK); opt-out (US CAN-SPAM) | Klaviyo/HubSpot | until unsubscribed + suppression list | Normal |
| 13 | Website / app analytics | page views | cookies/SDK | analytics | Consent (cookie banner) except strictly necessary | PostHog EU / Plausible (cookieless preferred) | 13 months | Low |
| 14 | Content-contributor data (guides/storytellers) | name, payout details, tax forms | contributor | licensing, payments | Contract; legal obligation | Notion/Drive + payout provider | 7–10 yrs (tax) | Normal |
| 15 | Employee / candidate data | HR records | staff | employment | Contract; legal obligation | Deel/Remote, Google Workspace | per local law | High (HR) |

**Data minimisation decisions (proposed):**
- No ad IDs (IDFA/AAID), no third-party ad SDKs, no data brokers.
- Cloud AI requests send **coarse location (geohash level 7, ~150 m) + place IDs** instead of exact lat/long where possible.
- Pseudonymous device ID for telemetry, rotated quarterly.
- City Packs downloaded by city, so the server learns only "which city", not "where in the city".

---

## 2. Regulatory map

| Law | Applies? | Key obligations for LORE | Status / dates |
|---|---|---|---|
| **EU GDPR** (Reg. 2016/679) | Yes: we target EU users (Rome launch city!) | Lawful basis, transparency (Arts 13/14), DSRs (access, deletion, portability, objection), DPIA for **systematic location tracking** (Art. 35), Art. 28 DPAs, Art. 30 records, breach notice **72h** to the SA, **Art. 27 EU representative** (no EU establishment, regular processing, so required), international transfers (Chapter V) | In force |
| **ePrivacy Directive** 2002/58/EC (+ national laws, e.g., Italy's Codice Privacy) | Yes | **Consent for storing/accessing info on the device** (Art. 5(3)) unless strictly necessary; location data (Art. 9) where we act as or with an ECS provider | In force; ePrivacy Regulation withdrawn by the Commission (2025) [V] |
| **UK GDPR + DPA 2018 + PECR**, as amended by the **Data (Use and Access) Act 2025** | Yes (London is on the city list; UK sales) | Similar to GDPR; **UK representative (Art. 27 UK GDPR)**; DUAA changes: new recognised legitimate interests, relaxed cookie consent for some analytics, **complaints-handling duty** (in force 19 Jun 2026), PECR fines up to £17.5M/4% [S] | Main DUAA provisions commenced **5 Feb 2026** [S] |
| **EU Data Act** (Reg. 2023/2854) | Yes (connected product) | User access to product data; pre-contract info; access-by-design for products placed on the market from 12 Sep 2026 [V] | Applies from 12 Sep 2025 [V] |
| **EU AI Act** | Yes (limited-risk AI system: conversational AI + synthetic audio) | Art. 50 transparency from **2 Aug 2026** [S] | See `policies/eu-ai-act-assessment.md` |
| **US CCPA/CPRA** (California) | **Not yet** (below thresholds: >$26.625M revenue, or 100k+ CA consumers/households, or ≥50% revenue from selling/sharing) [S]. **Likely by 2028** if we sell >100k units or reach revenue | Notice at collection, right to know/delete/correct, **limit use of sensitive PI (precise geolocation)**, opt-out of sale/sharing (we don't sell), GPC signal honouring, contracts with service providers; **risk assessments** and **cybersecurity audits** under the CPPA regulations effective **1 Jan 2026** (phased, first submissions by 1 Apr 2028) [S] | Build to CPRA standard now; cheaper than retrofitting |
| Other US state laws (VA, CO, CT, UT, TX, OR, MT, IA, DE, NH, NJ, TN, MN, MD, IN, KY, RI, NE…) [V] | Thresholds are typically 100k residents (some 35k–50k; **Texas & Nebraska: no numeric threshold, apply to non-small businesses**) [V] | **Precise geolocation = sensitive data → opt-in consent** (VA, CO, CT, TX, OR…); **Maryland MODPA (eff. Oct 2025): strict necessity for sensitive data, ban on sale of sensitive data** [V] | Consent flow for location satisfies all |
| **Washington My Health My Data Act** / Nevada SB 370 | Possibly, if we collect "consumer health data" (e.g., step counts inferred into fitness/health?) [V] | Avoid health inferences; step data used only for navigation, not health | Design choice |
| **US COPPA** (16 CFR 312, amended rule effective Jun 2025, compliance by Apr 2026) [V] | Only if directed to children or with actual knowledge of <13 users | See `policies/childrens-data-stance.md` | — |
| **India DPDP Act 2023 + DPDP Rules 2025** | Yes, if offered to people in India (Indian users, Indian travellers abroad buying from us) | Notice + consent (itemised, plain language, available in English/22 languages on request), **Consent Manager** interoperability, security safeguards, **breach notice to the Board and each affected Data Principal**, **verifiable parental consent for under-18s**, data retention limits, grievance redressal (respond within 90 days per Rules) [V], Significant Data Fiduciary duties if notified | Rules notified **13/14 Nov 2025**; Consent Manager provisions after **12 months (~Nov 2026)**; core obligations after **18 months (~13 May 2027)** [S] |
| **Japan APPI** | Yes (Kyoto on city list; JP sales in 2028) | Purpose specification, consent for third-party provision and **cross-border transfer** (with info on the destination country's regime), security control measures, breach reporting to the PPC [V] | In force |
| **Turkey KVKK, Brazil LGPD, etc.** | As we expand (Istanbul is on the city list) | Turkey: VERBIS registration threshold; cross-border transfer rules revised 2024 [V] | Later |

---

## 3. Governance roles

| Role | Decision |
|---|---|
| **Controller** | LORE Labs, Inc. (US) for all user data. EU/Indian subsidiaries later become joint/independent controllers for their staff data |
| **DPO (Art. 37 GDPR)** | Required where core activities consist of **regular and systematic monitoring of data subjects on a large scale**. Real-time location tracking for narration arguably qualifies once scale is "large" (EDPB WP243). **Decision: appoint an external DPO-as-a-service at Kickstarter launch (Q2 2027)** (est. €400–€1,500/month). Until then the COO is Privacy Lead |
| **EU Art. 27 representative** | Appoint before EU users are onboarded (beta in Rome, Q1 2027). Providers: e.g., VeraSafe, DataRep, Prighter, EDPO (est. **€500–€2,500/yr** each for EU and UK) [V] |
| **UK representative** | Same provider; UK ICO **data protection fee** (Tier 1: £52/yr; Tier 2 £78) [V], required for a controller processing UK personal data even if non-UK? (Applies to UK-established controllers; check with counsel) |
| **India Grievance Officer** | Named contact for DPDP grievances; publish in the privacy policy |
| **Processors (sub-processors)** | Cloud (AWS/GCP EU regions), LLM API providers (zero-retention/enterprise terms), Stripe, Shopify, Zendesk/Intercom, Twilio (SMS for safety alerts), connectivity partner (processor or independent controller per contract), Sentry/Datadog, Klaviyo, Google Workspace. Maintain a **public sub-processor list** with 30-day change notice |

---

## 4. International transfers
- US-hosted processing of EU/UK data: rely on the **EU–US Data Privacy Framework** by **self-certifying LORE Labs, Inc. to the DPF** (and UK Extension; Swiss-US DPF) via the Department of Commerce (annual fee tier by revenue; ~$250–$3,250 [V]) **and/or** use **2021 SCCs (Module 1/2/3)** + a Transfer Impact Assessment. The DPF survived its first legal challenge (General Court, *Latombe*, Sep 2025) [V]. Keep SCCs as a fallback.
- **Default architecture:** primary user-data storage in an **EU region (Frankfurt or Ireland)**. US region for US users. India: DPDP lets the government blacklist countries (negative list). No restrictions notified yet [V].
- LLM API calls: choose EU data residency where available; contractually **no training on our data**, ≤30-day (preferably zero) retention.

---

## 5. Security programme

### 5.1 Framework and milestones
| When | Milestone |
|---|---|
| Q4 2026 | Security baseline: SSO (Google Workspace) + hardware security keys for admins, MDM (Kandji/Jamf/Fleet) on laptops, GitHub branch protection + secret scanning, 1Password Business, cloud IAM least privilege, backups, logging |
| Q1 2027 | **Threat model** for device + app + cloud (STRIDE); **EN 18031 / ETSI EN 303 645 gap analysis**; secure-boot + signed OTA design; pen-test of the companion app + API (est. $10k–$25k) |
| Q2 2027 | Vulnerability Disclosure Policy at `lore.travel/security` + `security.txt` (RFC 9116) + **published support period** (PSTI); bug bounty (private, via HackerOne/Intigriti/YesWeHack) |
| Q3 2027 | Device hardware pen-test (JTAG/UART, flash extraction, BLE pairing, eSIM profile handling) (est. $20k–$50k); SBOM per release; **PSIRT** process for **CRA reporting** (24h early warning, 72h notification, 14-day final report to ENISA's Single Reporting Platform; obligations from 11 Sep 2026) [S] |
| 2028 | **SOC 2 Type I → Type II** (needed for B2B fleet customers) via Vanta/Drata/Secureframe (est. $15k–$40k/yr incl. auditor); consider ISO/IEC 27001 + 27701 for EU B2B |

### 5.2 Device security requirements (summary for Hardware/Software)
1. **Secure boot** chain with hardware root of trust; signed firmware; **anti-rollback**.
2. **No universal default passwords** (PSTI / EN 18031 / ETSI 303 645 provision 5.1). BLE pairing via LE Secure Connections (numeric comparison or app-based OOB).
3. **Encrypted storage** of trip history, contacts and tokens (AES-256, keys in secure element / TrustZone).
4. **Signed OTA updates**, delta updates over eSIM with a resume; **security updates for ≥5 years after the end of sale** (proposed support period); automatic security updates by default (CRA Annex I).
5. **Theft-lock / activation lock** (device bound to account; remote wipe).
6. Debug ports **disabled/fused** in production.
7. **Privacy LEDs**: LED ring shows mic active (press-to-talk) and live-share active.
8. Minimal attack surface: no open network services on device; Wi-Fi only client mode.
9. Crypto: TLS 1.3, certificate pinning for our API, modern ciphers; FIPS not needed.
10. Log hygiene: no precise location in crash logs.

### 5.3 Incident and breach response
| Step | Time | Who |
|---|---|---|
| Detect & triage (sev 1–4) | immediately | On-call engineer |
| Incident commander assigned; legal hold | <2h | COO |
| Assess personal-data breach risk | <24h | Privacy Lead + DPO |
| **GDPR/UK GDPR: notify the lead SA / ICO** (via the Art. 27 representative's member state SA, since we have no main establishment, so **every SA concerned** may be competent; no one-stop-shop) | **≤72h** from awareness | Privacy Lead |
| Notify affected users if high risk | without undue delay | COO + Comms |
| **CRA: early warning of actively exploited vulnerability / severe incident** | **≤24h**, notification ≤72h, final report ≤14 days | Security lead |
| **India DPDP: intimate the Data Protection Board + each affected Data Principal** | without delay; detailed report to the Board **within 72h** (per Rules) [V] | Privacy Lead |
| US state breach laws (all 50 states; e.g., CA ≤ "most expedient time"; some 30–60 days) | per state | Counsel |
| Japan APPI: preliminary report to PPC (~3–5 days) and final (30/60 days) [V] | | Counsel |
| Post-mortem + remediation | ≤10 business days | Eng |

Cyber insurance must cover breach response costs; see `admin-ops.md`.

---

## 6. Data-subject rights operations
- **Self-service in the app:** download my data (JSON + GPX for trips), delete trip history, delete account (with a 30-day recovery window), toggle consents (location to cloud, trip history, voice improvement, analytics, marketing).
- **Web form + email** privacy@lore.travel; identity verification proportional to risk.
- **Response time:** GDPR 1 month (+2 months for complex cases); CCPA 45 days (+45); DPDP per Rules (grievance redressal within a set period, 90 days per draft) [V]; APPI without delay.
- **Honour Global Privacy Control (GPC)** on the website (required in CA, CO, CT, etc.) [V].
- DSR log kept for 24 months (CCPA record-keeping).

---

## 7. Policies index (drafts in `policies/`)

| File | Status | Publish where |
|---|---|---|
| `policies/privacy-policy.md` | Draft v0.1 | lore.travel/privacy, app stores, in-app |
| `policies/terms-of-service.md` | Draft v0.1 | lore.travel/terms; app onboarding |
| `policies/subscription-terms.md` | Draft v0.1 | Checkout; LORE Pass page |
| `policies/warranty-returns-policy.md` | Draft v0.1 | lore.travel/warranty; in-box leaflet |
| `policies/acceptable-use-policy.md` | Draft v0.1 | lore.travel/aup |
| `policies/dpa-outline.md` | Outline | B2B fleet customers (hostels, tour operators) |
| `policies/dpia-location-data.md` | Draft v0.1 | Internal (shared with the DPO/SA on request) |
| `policies/childrens-data-stance.md` | Draft v0.1 | Internal + summarised in the privacy policy |
| `policies/eu-ai-act-assessment.md` | Draft v0.1 | Internal |
| `policies/safety-disclaimers.md` | Draft v0.1 | In-box, app, website, Kickstarter |

---

## 8. Privacy and security budget (est.)

| Item | 2027 | 2028 |
|---|---|---|
| EU + UK Art. 27 representative | €1.5k–€4k | same |
| External DPO (from Q2 2027) | €4k–€12k | €6k–€18k |
| Privacy counsel review of policies + DPIA | $8k–$20k | $5k–$10k |
| Pen-tests (app/API + device) | $30k–$75k | $30k–$60k |
| Bug bounty pool | $5k–$15k | $15k–$40k |
| Consent/cookie tool (Cookiebot/Usercentrics/OneTrust lite) | $500–$3k | same |
| Compliance automation (Vanta/Drata) + SOC 2 audit | — | $20k–$45k |
| DPF self-certification fee | ~$250–$1k [V] | same |
| **Total** | **~$55k–$135k** | **~$80k–$180k** |

---

## Sources
- India DPDP Rules 2025 phasing: https://yourstory.com/2025/11/digital-personal-data-protection-dpdp-rules-2025-rollout-over-18-months ; https://www.mondaq.com/india/data-protection/1706890/a-closer-look-at-the-dpdp-rules-2025 ; https://www.exterro.com/resources/india-notifies-final-dpdpa-rules-phased-enforcement-begins
- CCPA thresholds and 2026 regulations: https://www.schellman.com/blog/privacy/ccpa-now-requires-annual-cybersecurity-audits ; https://www.eisneramper.com/insights/risk-compliance/new-requirements-in-2026-and-beyond-0726/ ; https://www.forvismazars.us/forsights/2026/05/cpra-cybersecurity-audits-overview-of-requirements
- UK DUAA 2025 commencement: https://www.kennedyslaw.com/en/thought-leadership/article/2026/the-data-use-and-access-act-2025-commencement-dates-and-planned-guidance-for-2026 ; https://mondaq.com/uk/privacy-protection/1748226/key-data-protection-changes-under-the-data-use-and-access-act-2025-comes-into-force-on-february-5-2026
- EU CRA reporting: https://www.skadden.com/insights/publications/2026/09/get-ready-reporting-faqs-and-checklist ; https://ncsc.gov.ie/cra/
- EU AI Act Article 50: https://www.cooley.com/news/insight/2026/2026-08-03-eu-ai-act-transparency-obligations-take-effect-2-august-2026
- UK PSTI: https://www.twobirds.com/en/insights/2024/uk/new-uk-product-security-rules-for-connected-products-go-live-in-april
