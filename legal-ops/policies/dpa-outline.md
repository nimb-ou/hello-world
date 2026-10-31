# Data Processing Addendum: Outline (B2B "LORE for Business")

> **OUTLINE ONLY. NOT LEGAL ADVICE.** A privacy lawyer must turn this into a full DPA. It is for B2B fleet customers (hostels, tour operators, schools) who issue LORE devices to their guests or staff. Model the full text on GDPR Art. 28(3), the **EU SCCs 2021/914** (Modules 2/3) plus the **UK IDTA/Addendum**, CCPA "service provider" contract terms (Cal. Civ. Code §1798.100(d), regs §7051), and DPDP Act s.8(2) (a Data Processor engaged only under a valid contract).

## Role allocation (decide per use case)
| Scenario | Customer | LORE |
|---|---|---|
| Hostel lends devices to guests; guests use them anonymously (no LORE account) and the hostel sees device location for theft recovery | **Controller** (fleet dashboard data) | **Processor** for fleet data; **independent controller** for safety/telecom data needed to run the service |
| Tour operator runs group tours with guide dashboard "where's my group" | Controller | Processor |
| Guests sign in with their own LORE account | Independent controller (bookings) | **Independent controller** (account data). No DPA needed for that data; data-sharing terms instead |

## DPA sections
1. **Definitions**: GDPR/UK GDPR/CCPA/DPDP terms mapped.
2. **Subject matter, duration, nature and purpose** (Annex I): fleet management, device location for loss/theft, usage analytics, guide-group features.
3. **Categories of data subjects**: guests, tour participants, customer staff. **Data categories**: device ID, location (precise, real-time, opt-in for group features), check-out/in times, optional name/room number. **No special-category data.**
4. **Processor obligations (Art. 28(3))**: documented instructions only; confidentiality of personnel; Art. 32 security (**Annex II TOMs**: encryption, access control, logging, pen-testing, BCP); sub-processor rules (general authorisation + public list + **30-day objection right**); assistance with DSRs, DPIAs, breach notification; deletion/return at end of contract (within **30 days**); audit rights (SOC 2 report first, on-site audit max 1×/year with 30 days' notice, at customer cost unless a breach is found).
5. **Breach notification**: processor → controller **without undue delay and within 48 hours** of awareness, with Art. 33(3) information.
6. **International transfers**: SCCs Module 2 (C→P) / Module 3 (P→P with sub-processors); UK Addendum; Swiss amendments; DPF reliance where certified; TIA summary available.
7. **CCPA service-provider terms**: no selling/sharing; no use outside the business purpose; no combining with other data except as allowed; certification of understanding; notify if unable to comply.
8. **DPDP**: processing only on Data Fiduciary instructions; reasonable security safeguards; breach intimation to the Data Fiduciary.
9. **Guest transparency**: the customer must give guests a notice (LORE provides a template sticker/QR card: "This device shares its location with [Hostel] while checked out…").
10. **Location-tracking safeguards**: group/fleet location visible **only while the device is checked out/the tour is active**; history retained **≤7 days** by default; staff access logged.
11. **Liability**: subject to the MSA cap; data-protection super-cap (e.g., 2× annual fees, or $[x]).
12. **Annexes**: I (processing description), II (TOMs), III (sub-processor list), IV (SCCs as incorporated).
