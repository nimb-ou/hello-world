"""Build a City Pack from curated seed data, optionally enriched with OSM + Wikipedia.

Pipeline:
  1. load + validate curated seed (always available, ships in-repo)
  2. [online] Overpass: fetch candidate places in bbox; match to seed POIs (wikipedia tag or
     name + <80 m); attach osm ids / wikidata / heights; keep unmatched notable places as new POIs
  3. [online] Wikipedia REST: summaries for new POIs -> CANDIDATE facts (review_status=needs_review,
     excluded from the shipped pack unless --include-unreviewed); summaries for seed POIs -> a
     support score per curated fact (triage for editors)
  4. score interest, assign stable ids, emit JSON + SQLite
If any network stage fails the builder logs it and continues with the seed (mode="seed").
"""
from __future__ import annotations

import datetime as _dt
import json
import logging
import re
import urllib.parse
from pathlib import Path
from typing import Optional

from . import PACK_SCHEMA_VERSION
from .http import Fetcher, NetworkUnavailable, urllib_fetch
from .osm import OsmPlace, classify_category, fetch_osm_places
from .scoring import DEFAULT_VISIBLE_RANGE, computed_interest, final_interest
from .seed import haversine_m, load_seed
from .wikipedia import candidate_facts_from_summary, try_fetch_summary, verify_fact_against_summary

log = logging.getLogger("lore_citypack")

ROUTING_NOTE = {
    "status": "not-included-in-v1",
    "plan": "Pedestrian routing graph generated from OSM highway=* (footway, pedestrian, living_street, steps, "
            "residential, crossing nodes) with Valhalla tile builder; shipped as a separate routing tile set "
            "(~25-40 MB for central Rome) so packs can update stories without re-downloading routing.",
    "crossings": "Crossing nodes (highway=crossing) feed the Safety service's 'quiet while crossing' signal.",
}


def source_title(url: str) -> str:
    m = re.match(r"^https://([a-z\-]+)\.wikipedia\.org/wiki/(.+)$", url)
    if m:
        return f"Wikipedia ({m.group(1)}): {urllib.parse.unquote(m.group(2)).replace('_', ' ')}"
    return urllib.parse.urlparse(url).netloc


def _norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9à-ÿ ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def match_osm_to_seed(seed_pois: list[dict], places: list[OsmPlace], max_m: float = 80) -> tuple[dict[str, OsmPlace], list[OsmPlace]]:
    """Return ({seed_slug: osm_place}, unmatched_places)."""
    matched: dict[str, OsmPlace] = {}
    used: set[str] = set()
    by_wiki = {p.get("wikipedia"): p["slug"] for p in seed_pois if p.get("wikipedia")}
    for pl in places:
        slug = by_wiki.get(pl.wikipedia) if pl.wikipedia else None
        if slug and slug not in matched:
            matched[slug] = pl
            used.add(pl.osm_id)
    for p in seed_pois:
        if p["slug"] in matched:
            continue
        best: Optional[tuple[float, OsmPlace]] = None
        for pl in places:
            if pl.osm_id in used:
                continue
            d = haversine_m(p["lat"], p["lng"], pl.lat, pl.lng)
            if d > max_m:
                continue
            a, b = _norm(p["name"]), _norm(pl.name)
            if a in b or b in a or len(set(a.split()) & set(b.split())) >= 2:
                if best is None or d < best[0]:
                    best = (d, pl)
        if best:
            matched[p["slug"]] = best[1]
            used.add(best[1].osm_id)
    unmatched = [pl for pl in places if pl.osm_id not in used]
    return matched, unmatched


def _slugify(name: str) -> str:
    s = _norm(name)
    s = s.translate(str.maketrans("àáâäèéêëìíîïòóôöùúûü", "aaaaeeeeiiiioooouuuu"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60] or "poi"


def build_pack(seed: dict, *, online: bool = False, fetch: Fetcher = urllib_fetch,
               include_unreviewed: bool = False, max_new_pois: int = 150,
               now: Optional[_dt.datetime] = None) -> dict:
    city = seed["city"]
    bbox = tuple(seed["bbox"])
    notes: list[str] = []
    mode = "seed"
    osm_matches: dict[str, OsmPlace] = {}
    new_places: list[OsmPlace] = []
    fact_support: dict[str, float] = {}

    if online:
        try:
            places = fetch_osm_places(fetch, bbox)  # type: ignore[arg-type]
            osm_matches, unmatched = match_osm_to_seed(seed["pois"], places)
            new_places = [p for p in unmatched if p.wikipedia][:max_new_pois]
            notes.append(f"overpass: {len(places)} places, {len(osm_matches)} matched to seed, {len(new_places)} new with wikipedia")
            mode = "seed+online"
        except (NetworkUnavailable, Exception) as exc:  # noqa: BLE001 - any failure -> seed fallback
            notes.append(f"overpass unavailable, using curated seed only: {exc.__class__.__name__}: {str(exc)[:160]}")
            log.warning("overpass failed: %s", exc)

    pois: list[dict] = []
    for p in seed["pois"]:
        slug = p["slug"]
        poi_id = f"{city}-{slug}"
        osm = osm_matches.get(slug)
        wiki = p.get("wikipedia") or (osm.wikipedia if osm else None)
        wikidata = p.get("wikidata") or (osm.wikidata if osm else None)
        height = p.get("height_m") or (osm.height_m if osm else None)
        summary = try_fetch_summary(fetch, wiki) if (online and mode != "seed" and wiki) else None
        facts = []
        for i, f in enumerate(p["facts"], start=1):
            srcs = f.get("sources") or [{"url": wiki}]
            fid = f"{poi_id}-{i}"
            card = {
                "id": fid,
                "poi_id": poi_id,
                "text": f["text"],
                "kind": f["kind"],
                "depth": f["depth"],
                "sources": [{"url": s["url"], "title": s.get("title") or source_title(s["url"])} for s in srcs],
                "review_status": "curated",
            }
            if f.get("look_up"):
                card["look_up"] = True
            if f.get("is_legend"):
                card["is_legend"] = True
            if summary:
                fact_support[fid] = verify_fact_against_summary(f["text"], summary)
            facts.append(card)
        comp = computed_interest(p["category"], len(facts), bool(wiki), bool(wikidata), p.get("tags", []), height)
        poi = {
            "id": poi_id,
            "name": p["name"],
            "lat": round(p["lat"], 6),
            "lng": round(p["lng"], 6),
            "category": p["category"],
            "tags": sorted(set(p.get("tags", []))),
            "interest": final_interest(p.get("editorial_interest"), comp),
            "visible_range_m": p.get("visible_range_m") or DEFAULT_VISIBLE_RANGE[p["category"]],
            "footprint": None,
            "facts": facts,
        }
        if height:
            poi["height_m"] = height
        if wiki:
            poi["wikipedia"] = wiki
        if wikidata:
            poi["wikidata"] = wikidata
        if osm:
            poi["osm"] = osm.osm_id
        pois.append(poi)

    # New POIs discovered online: only shipped if they have reviewed facts (or --include-unreviewed).
    seen_slugs = {p["slug"] for p in seed["pois"]}
    for pl in new_places:
        summary = try_fetch_summary(fetch, pl.wikipedia)  # type: ignore[arg-type]
        if not summary:
            continue
        cands = candidate_facts_from_summary(summary)
        if len(cands) < 2 and not include_unreviewed:
            continue
        slug = _slugify(pl.name)
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        poi_id = f"{city}-{slug}"
        facts = [{
            "id": f"{poi_id}-{i}", "poi_id": poi_id, "text": t, "kind": "history", "depth": 1 if i == 1 else 2,
            "sources": [{"url": pl.wikipedia, "title": source_title(pl.wikipedia)}], "review_status": "needs_review",
        } for i, t in enumerate(cands, start=1)]
        if not include_unreviewed:
            notes.append(f"held for review: {pl.name} ({len(facts)} candidate facts)")
            continue
        cat = classify_category(pl.tags)
        pois.append({
            "id": poi_id, "name": pl.name, "lat": round(pl.lat, 6), "lng": round(pl.lng, 6), "category": cat,
            "tags": ["osm-discovered"], "interest": computed_interest(cat, len(facts), True, bool(pl.wikidata), [], pl.height_m),
            "visible_range_m": DEFAULT_VISIBLE_RANGE[cat], "footprint": None, "facts": facts,
            "wikipedia": pl.wikipedia, "osm": pl.osm_id, **({"wikidata": pl.wikidata} if pl.wikidata else {}),
        })

    if fact_support:
        weak = sorted((v, k) for k, v in fact_support.items() if v < 0.25)
        notes.append(f"wikipedia support scores computed for {len(fact_support)} facts; {len(weak)} flagged for editor review")
    notes.append("footprints: placeholder (null) - OSM building footprint stage not yet implemented")

    generated = (now or _dt.datetime.now(_dt.timezone.utc)).replace(microsecond=0).isoformat()
    return {
        "schema_version": PACK_SCHEMA_VERSION,
        "city": city,
        "name": seed["name"],
        "bbox": list(bbox),
        "generated_at": generated,
        "build": {"mode": mode, "notes": notes, "curation_note": seed.get("curation_note", "")},
        "routing": ROUTING_NOTE,
        "stats": {
            "pois": len(pois),
            "facts": sum(len(p["facts"]) for p in pois),
            "sources": len({s["url"] for p in pois for f in p["facts"] for s in f["sources"]}),
        },
        "fact_support": fact_support,
        "pois": sorted(pois, key=lambda p: p["id"]),
    }


def write_json(pack: dict, path: str | Path) -> Path:
    path = Path(path)
    path.write_text(json.dumps(pack, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return path


def build_from_files(seed_path: str | Path, out_dir: str | Path, **kw) -> tuple[Path, Path, dict]:
    from .sqlite_writer import write_sqlite

    seed = load_seed(seed_path)
    pack = build_pack(seed, **kw)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    j = write_json(pack, out / f"{seed['city']}.pack.json")
    s = write_sqlite(pack, out / f"{seed['city']}.pack.sqlite")
    return j, s, pack
