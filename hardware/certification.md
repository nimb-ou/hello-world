# Certification Plan: Pebble, Square, Atlas

All costs are **estimates to be verified** with lab quotes (TÜV SÜD, Bureau Veritas/7Layers, SGS, DEKRA, CETECOM, UL). Costs are in USD and include pre-scans and one re-test round. Using pre-certified radio modules (Quectel EG25-G, BG95-S5) reduces, but does **not** remove, end-product testing. New antennas, SAR, OTA and carrier testing always apply to the finished device.

## 1. Scope per SKU

| Regime | Pebble (Wi-Fi/BT) | Square (+LTE) | Atlas (+LTE, NTN, camera) | Notes |
|---|---|---|---|---|
| **FCC** (US): Part 15B/15C/15E; Parts 22/24/27 (+90 for B14 if enabled); RF exposure | $30k | $55k | $70k | Atlas adds MSS/NTN (Part 25 terminal authorisation via the Skylo-certified module); verify the scope with a TCB |
| **SAR** (FCC/ISED/CE), body-worn 0–5 mm | $8k (may be exempt at low power, verify) | $25k | $30k | Clip, strap and pocket positions. Plan a proximity sensor if the margin is thin |
| **ISED** (Canada) RSS-247/130/132/133/139/102 | $6k | $10k | $12k | Mostly leverages FCC data |
| **CE / RED** (EU): EN 300 328, 301 893, 301 908-1/-13, 303 413 (GNSS), 301 489-x EMC, EN 62368-1, EN 50566/62209 SAR, **EN 18031-1/-2/-3 cybersecurity (RED Art. 3.3 d/e/f, mandatory from 1 Aug 2025)** | $30k | $50k | $60k | Notified Body is optional with harmonised standards. Budget a cyber consultant |
| **UKCA** | $4k | $5k | $5k | Re-uses CE reports; also PSTI Act (UK product security) |
| **Japan**: MIC/TELEC (radio, giteki) + JATE (LTE terminal) | $12k | $30k | $40k | NTN on Atlas: MIC status of Skylo in Japan **unknown → disable NTN in JP SKU at launch** |
| **India**: WPC ETA (radio) + BIS CRS (IS 13252 IT equipment, IS 16046 battery) + TEC MTCTE (cellular) | $10k | $30k | $35k | Needs a local Authorised Indian Representative; 3–5 months |
| Korea KC / Australia RCM (optional, wave 2) | $10k | $20k | $20k | |
| **PTCRB** (North America carriers) | – | $45k | $55k | Module-based integrated device: RF OTA (CTIA TRP/TIS) is the large item. Module-only figures of $16–20k ([M2M guide](https://m2msupport.net/m2msupport/?p=1333)) exclude OTA |
| **GCF** (EU/ROW operators) | – | $50k | $55k | Field trials depend on operator; partly overlaps with PTCRB OTA |
| **Carrier acceptance** (AT&T, T-Mobile; Verizon deferred) | – | $70k | $80k | Depends on the eSIM partner. A global MVNO profile may need only the host operator's approval |
| **GSMA eSIM** (eSA certificate held by the eUICC vendor; device RSP/LPA conformance SGP.23) | – | $15k | $15k | LPA implemented on AP; test via the connectivity partner |
| **Skylo NTN device certification** | – | – | $40k | The module is certified; the end device is certified by Skylo (E) |
| **Bluetooth SIG** qualification: Adopter $12,000 from 1 Mar 2026 ([SIG fee schedule](https://www.bluetooth.com/fee-schedule/)); one QDID can cover the family if radio/stack are identical | $12k | $12k (shared) | $12k (shared) | Join as a Contributing Adopter ($8k first qualification) if eligible |
| Wi-Fi Alliance (optional) | $5k | $5k | $5k | Marketing only |
| **Battery**: UN38.3 transport, IEC 62133-2, IEC 62368-1 Annex M; cell-level UL 1642 via cell vendor | $12k | $14k | $14k | UN38.3 is required **before air freight of the first EVT units** |
| **RoHS** (EU 2011/65 + 2015/863), **REACH** SVHC, **WEEE** registration (per EU state), **battery regulation EU 2023/1542** (labelling, removability rules for portable batteries from 2027: verify the device exemption), Prop 65, packaging (PPWR) | $12k | $12k | $15k | Ti/DLC/ceramic material declarations for Atlas |
| IP67 (IEC 60529), drop/tumble, salt-fog, UV (internal reliability, not regulatory) | $10k | $12k | $15k | Done at the DVT reliability lab |
| Consultant / agents / filing fees / contingency (~20 %) | $15k | $70k | $75k | |
| **Total (E)** | **≈ $165k** | **≈ $485k** | **≈ $640k** | These NRE values are used in `bom/build_bom.py` |

The Pebble Lite ECR is about $140k (no Wi-Fi radio; otherwise similar).

## 2. Timeline (aligned to COMPANY.md: Q1 2027 EVT, Q2 2027 Kickstarter, Q4 2027 ship)

| When | Activity |
|---|---|
| Nov–Dec 2026 | Engage lab and TCB; regulatory strategy memo; select eSIM connectivity partner; BT SIG membership; EN 18031 cyber gap analysis |
| Q1 2027 (EVT) | Pre-scans (EMC, radiated spurious emissions, LTE desense, GNSS desense); antenna OTA iteration in a CTIA chamber; early SAR scan; UN38.3 on EVT cells |
| Q2 2027 (DVT) | Formal FCC/ISED/CE/UKCA tests on DVT units (≈ 6–8 weeks); SAR; PTCRB/GCF OTA + protocol; BT SIG listing; IEC 62133-2 |
| Q3 2027 | FCC grant (US Kickstarter shipping gate); CE DoC; MIC/JATE; carrier acceptance (AT&T/T-Mobile 8–12 weeks); India BIS/WPC/TEC in parallel (long pole, 3–5 months); Skylo device cert (Atlas) |
| Q4 2027 (PVT/MP) | Production conformity; labels and e-label on device; first shipments US/EU/UK. JP and IN may follow 1–2 months later |

**Critical path**: carrier acceptance and India. **Recommendation:** launch Square/Atlas cellular in US/EU/UK first. The device still works in 150+ countries through the roaming eSIM profile, but the *regulatory* sale markets start with US, EU, UK and CA.

## 3. Design-for-compliance rules (enforced at schematic and layout review)

- Shield cans on the SoC/DRAM, LTE, Wi-Fi, GNSS and PMIC. Common-mode chokes on USB.
- Ferrite and RC on every flex leaving the main board.
- Spread-spectrum clocking on DSI/UFS where supported.
- Software-controllable TX power back-off tables (SAR) in the modem NV and the combo-chip calibration.
- Unique per-device credentials, secure boot, signed OTA, no default passwords, and a vulnerability disclosure policy (EN 18031 / UK PSTI / US Cyber Trust Mark optional).
- E-label support on the display (Square/Atlas); the Pebble needs a laser-etched label.
