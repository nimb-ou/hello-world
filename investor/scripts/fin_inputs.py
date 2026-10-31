"""Finance-derived inputs for the deck that are not in finance/model_summary.json.

Use of funds ($1.75M, D14) = pre-seed operating spend Nov-26..Jun-27 (before the Kickstarter payout),
grouped from finance/budget-12-months.md ($000, base scenario); the remainder is the
cash buffer the model shows at the Jun-27 low point. Update when finance changes.
"""
USE_OF_FUNDS = [
    ("Founding engineering team", 500_000, "R&D salaries + burden ($464k), dev tools & ML compute ($36k)"),
    ("Kickstarter, brand & community", 322_000, "Campaign marketing $230k, growth lead, brand/PR"),
    ("Hardware: ID, ODM NRE, 50 EVT", 210_000, "ID/ME/CMF agency $95k, ODM NRE $80k, EVT build $35k"),
    ("G&A, legal, IP, insurance", 168_000, "Founder salary, formation, trademarks, provisionals, SaaS"),
    ("City Pack content (Rome, London)", 40_000, "Editorial fact-checking and storytellers"),
    ("Cash buffer through Kickstarter", 510_000, "Low point ~$528k in Jun-27 with the D14 top-up (was $278k)"),
]
RUNWAY_NOTE = ("Runway: Nov 2026 to the Kickstarter payout (Jun/Jul 2027) and the $6M seed (Aug 2027). "
               "The $250k top-up (D14) lifts the Jun-27 cash low from ~$278k to ~$0.5M.")
UE_LINES = [
    ("DTC hardware GM (H2-2028 cost): ", "Pebble 42% · Square 23% · Atlas 37%. At launch, before the D11 cost-down, Square is only 7%."),
    ("Lifetime contribution per device: ", "$42 / $57 / $211 incl. LORE Pass, accessories and affiliate, after $60 paid CAC."),
    ("LORE Pass GM ≈69% ", "(2028) → ≈75% (2031); cloud + data ≈ $2.02 per paid user-month."),
    ("Biggest swing: ", "if the Square cost-down fails, FY31 EBITDA is −$8.3M not +$0.8M. DVT gate Sep-2027: >$205 ex-NRE → price $329. Square is DTC-only until landed ≤$200 (D15)."),
]
