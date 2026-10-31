# DPIA: Location, Motion and Audio Processing in LORE (DRAFT v0.1)

> **DRAFT. NOT LEGAL ADVICE.** Data Protection Impact Assessment under GDPR Art. 35 / UK GDPR Art. 35, also used as the basis for the CPRA risk assessment (CPPA regs, effective 1 Jan 2026) and the DPDP "periodic DPIA" if LORE is ever notified as a Significant Data Fiduciary. The DPO and privacy counsel must review it. Update it at each major release (EVT, Kickstarter, launch, Atlas camera).

| Field | Value |
|---|---|
| Controller | LORE Labs, Inc. |
| Assessors | COO (Privacy Lead), Head of Software, Hardware lead; DPO (from Q2 2027) |
| Version / date | v0.1 / [date] |
| Next review | Before the EVT beta (Q1 2027) |

## 1. Why a DPIA is required
Triggers: **systematic monitoring** (continuous location); **location data** listed in EDPB WP248 criteria; **innovative technology** (AI narration, sensor fusion); **large scale** (target 5k → 100k+ users); possibly **vulnerable users** (solo travellers, people with visual impairments in the accessibility version). Two or more WP248 criteria means a DPIA is mandatory. The Italian Garante's list of processing requiring a DPIA includes geolocation-based processing [verify].

## 2. Description of processing
| Flow | Data | Where processed | Retention |
|---|---|---|---|
| F1 Map Vision narration | GNSS (L1+L5), IMU, compass, steps, map geometry | **On-device only** | 24h rolling buffer |
| F2 "Tell me more"/Q&A | press-to-talk audio → text; coarse location (geohash-7) + place ID | On-device ASR where possible; cloud LLM (EU region, zero-retention terms) | Audio: none; transcripts 30 days |
| F3 Live info (opening hours, transit) | place IDs, coarse location | Cloud → third-party APIs (no user ID passed) | Logs 24h |
| F4 Trip History (opt-in) | full track + stories | Encrypted cloud | User-controlled |
| F5 Safety: SOS / live share / walk-me-home | precise location, contacts, timers | Cloud relay + SMS provider; optional emergency monitoring partner | Session + 7 days; SOS log 13 months |
| F6 Quiet-moment VAD | speech-present boolean | On-device RAM | seconds |
| F7 Glance camera (Atlas) | images | On-device vision; optional cloud with face blur | Not stored |
| F8 Telemetry | crash, GNSS quality, battery | Cloud, pseudonymous ID | 13 months |
| F9 Connectivity | IMSI, cell ID, data usage | Connectivity partner | Per telecom law |

## 3. Necessity and proportionality
- **Purpose limitation:** location only for narration, navigation and safety. **Never** for advertising, profiling for third parties, or sale.
- **Minimisation:** on-device by default; coarse location to the cloud; no ad IDs; trip history off by default.
- **Lawful basis:** contract (F1, F2, F3, F5); consent (F4, cloud location under ePrivacy Art. 5(3), voice improvement, analytics); vital interests (F5 in an emergency); legitimate interests with an LIA (F6, F8).
- **Transparency:** first-run explainer, privacy label, LED indicator for mic and live share.
- **Rights:** in-app export/delete; consent toggles.
- **Processors:** DPAs; EU hosting; SCCs/DPF.

## 4. Risk assessment
Scale: Likelihood (L) 1–5, Severity (S) 1–5, Risk = L×S. Residual risk is after mitigations.

| # | Risk to individuals | L | S | Inherent | Mitigations | Residual |
|---|---|---|---|---|---|---|
| R1 | **Stalking / covert tracking** (device hidden on a victim; abuser uses live share) | 3 | 5 | 15 | Live share needs on-device confirmation; persistent LED + periodic audible "your location is being shared" reminders; unwanted-tracker detection (DULT) [verify]; session auto-expiry (max 24h); abuse reporting; law-enforcement process | 6 |
| R2 | **Breach of location history** reveals home, routines, religion (visits to places of worship), health (clinics), sexuality | 2 | 5 | 10 | History opt-in; E2E encryption option; encryption at rest; access control; sensitive-place suppression (don't store dwell at clinics, places of worship, etc. in history unless the user saves them) | 4 |
| R3 | **Function creep** (later use for ads/analytics/sale) | 2 | 4 | 8 | Policy commitment; board-level privacy principle; DPIA re-review gate; CCPA "no sale" | 2 |
| R4 | **Government access** to location data | 2 | 4 | 8 | Minimal retention (nothing to hand over); transparency report; challenge overbroad requests; EU hosting | 4 |
| R5 | **Bystander privacy** (mic, camera) | 3 | 3 | 9 | Press-to-talk only; VAD keeps no audio; Glance on-device face blur; no face recognition; capture indicator | 3 |
| R6 | **Inaccurate AI narration** causes harm (e.g., wrong safety info, defamatory statement about a business) | 3 | 3 | 9 | Fact-grounding with sources; verifier; no safety advice from LLM free text; error reporting; editorial review for top places | 4 |
| R7 | **SOS failure** leads to harm | 2 | 5 | 10 | Not marketed as an emergency service; clear disclaimers; redundancy (LTE → SMS → phone app → satellite on Atlas); battery reserve for SOS; regular self-test | 6 (product-safety risk; see safety disclaimers) |
| R8 | **Children** using the device | 2 | 4 | 8 | 18+ accounts; parental mode only via parent account; no profiling | 3 |
| R9 | **Connectivity partner misuse** of network location | 2 | 4 | 8 | DPA / controller-to-controller terms; audit; minimal data | 4 |
| R10 | **International transfer** exposure | 2 | 3 | 6 | EU hosting; SCCs/DPF; TIA | 3 |
| R11 | **Re-identification from "anonymous" telemetry** | 2 | 3 | 6 | No precise location in telemetry; k-anonymity aggregation (k ≥ 20); rotate IDs | 2 |

**Conclusion (draft):** with mitigations, residual risks are **acceptable**. No residual risk is "high", so **no prior consultation with the SA (Art. 36) is required**, subject to DPO sign-off. R1 and R7 need ongoing monitoring metrics.

## 5. Action plan
| Action | Owner | Due |
|---|---|---|
| Implement sensitive-place suppression in Trip History | Software | Beta |
| Anti-stalking features (LED, reminders, auto-expiry) | Software/Hardware | EVT |
| Legitimate-interests assessments for F6, F8 | Privacy Lead | Dec 2026 |
| Processor DPAs and TIAs signed | COO | Before beta |
| DPO review and sign-off | DPO | Q2 2027 |
| CPRA-format risk assessment summary (for later CPPA submission) | Privacy Lead | 2028 |

## 6. Sign-off
Privacy Lead: ________ DPO: ________ CEO: ________ Date: ______
