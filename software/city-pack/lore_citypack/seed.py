"""Load and validate curated seed data."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

VALID_CATEGORIES = {
    "monument", "church", "fountain", "square", "museum", "ruin", "street", "bridge", "statue",
    "palace", "park", "neighbourhood", "viewpoint", "hidden_gem",
}
VALID_KINDS = {"history", "architecture", "art", "legend", "culture", "film", "people", "practical"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class SeedError(ValueError):
    pass


def haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 6_371_008.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


def load_seed(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate_seed(data)
    if errors:
        raise SeedError("seed validation failed:\n  " + "\n  ".join(errors))
    return data


def validate_seed(data: dict) -> list[str]:
    errs: list[str] = []
    south, west, north, east = data["bbox"]
    slugs: set[str] = set()
    pois = data.get("pois", [])
    for p in pois:
        sid = p.get("slug", "?")
        if not SLUG_RE.match(sid):
            errs.append(f"{sid}: bad slug")
        if sid in slugs:
            errs.append(f"{sid}: duplicate slug")
        slugs.add(sid)
        if not (south <= p["lat"] <= north and west <= p["lng"] <= east):
            errs.append(f"{sid}: coordinates outside city bbox")
        if p.get("category") not in VALID_CATEGORIES:
            errs.append(f"{sid}: invalid category {p.get('category')}")
        ei = p.get("editorial_interest", 0.5)
        if not 0 <= ei <= 1:
            errs.append(f"{sid}: editorial_interest out of range")
        facts = p.get("facts", [])
        if not 2 <= len(facts) <= 4:
            errs.append(f"{sid}: needs 2-4 facts, has {len(facts)}")
        poi_src = p.get("wikipedia")
        for i, f in enumerate(facts):
            words = len(f["text"].split())
            if not 6 <= words <= 70:
                errs.append(f"{sid}#{i}: fact length {words} words (6-70 allowed)")
            if f.get("kind") not in VALID_KINDS:
                errs.append(f"{sid}#{i}: invalid kind")
            if f.get("depth") not in (1, 2, 3):
                errs.append(f"{sid}#{i}: depth must be 1-3")
            if f.get("kind") == "legend" and not f.get("is_legend"):
                errs.append(f"{sid}#{i}: legend facts must set is_legend")
            srcs = f.get("sources") or ([{"url": poi_src}] if poi_src else [])
            if not srcs:
                errs.append(f"{sid}#{i}: no source")
            for s in srcs:
                if not str(s.get("url", "")).startswith("https://"):
                    errs.append(f"{sid}#{i}: source must be https URL")
        if not any(f.get("depth") == 1 for f in facts):
            errs.append(f"{sid}: needs at least one depth-1 (headline) fact")
    # near-duplicate coordinates usually mean a copy/paste error
    for i, a in enumerate(pois):
        for b in pois[i + 1:]:
            if haversine_m(a["lat"], a["lng"], b["lat"], b["lng"]) < 5:
                errs.append(f"{a['slug']} and {b['slug']} are < 5 m apart (copy/paste?)")
    return errs
