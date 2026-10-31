"""Interest scoring for POIs.

final = 0.7 * editorial + 0.3 * computed  (editorial = curator's 0..1 judgement, if present)
computed = category prior + evidence bonuses (wikipedia/wikidata, fact richness, height/visibility,
hidden-gem bonus). Popularity signals (Wikipedia pageviews) are added when online.
"""
from __future__ import annotations

import math
from typing import Optional

CATEGORY_PRIOR = {
    "monument": 0.55, "ruin": 0.5, "church": 0.4, "fountain": 0.45, "square": 0.45, "museum": 0.4,
    "statue": 0.35, "palace": 0.35, "bridge": 0.35, "street": 0.3, "park": 0.3, "neighbourhood": 0.35,
    "viewpoint": 0.4, "hidden_gem": 0.5,
}


def computed_interest(category: str, n_facts: int, has_wikipedia: bool, has_wikidata: bool,
                      tags: list[str], height_m: Optional[float] = None, monthly_pageviews: Optional[int] = None) -> float:
    s = CATEGORY_PRIOR.get(category, 0.35)
    s += 0.08 if has_wikipedia else 0.0
    s += 0.04 if has_wikidata else 0.0
    s += 0.04 * min(n_facts, 4)
    if "hidden-gem" in tags:
        s += 0.06
    if "landmark" in tags:
        s += 0.08
    if height_m:
        s += min(0.06, height_m / 1000)
    if monthly_pageviews:
        s += min(0.15, 0.03 * math.log10(max(1, monthly_pageviews)))
    return round(min(1.0, s), 3)


def final_interest(editorial: Optional[float], computed: float) -> float:
    if editorial is None:
        return round(computed, 3)
    return round(min(1.0, 0.7 * editorial + 0.3 * computed), 3)


DEFAULT_VISIBLE_RANGE = {
    "monument": 150, "ruin": 120, "church": 80, "fountain": 60, "square": 100, "museum": 70, "statue": 30,
    "palace": 80, "bridge": 100, "street": 60, "park": 90, "neighbourhood": 120, "viewpoint": 80, "hidden_gem": 30,
}
