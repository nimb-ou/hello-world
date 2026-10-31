"""OpenStreetMap / Overpass API source.

Fetches candidate POIs (historic sites, attractions, museums, viewpoints, notable places of
worship, fountains, artworks) with their wikipedia/wikidata tags inside the city bbox.
"""
from __future__ import annotations

import urllib.parse
from dataclasses import dataclass, field
from typing import Optional

from .http import Fetcher, get_json

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]


def build_overpass_query(bbox: tuple[float, float, float, float], timeout_s: int = 120) -> str:
    """bbox = (south, west, north, east)."""
    s, w, n, e = bbox
    b = f"({s},{w},{n},{e})"
    selectors = [
        'nwr["historic"]["name"]',
        'nwr["tourism"~"^(attraction|museum|viewpoint|artwork)$"]["name"]',
        'nwr["amenity"="place_of_worship"]["wikipedia"]',
        'nwr["amenity"="fountain"]["name"]',
        'nwr["man_made"="obelisk"]',
        'nwr["building"]["wikidata"]["name"]',
    ]
    body = "\n".join(f"  {sel}{b};" for sel in selectors)
    return f"[out:json][timeout:{timeout_s}];\n(\n{body}\n);\nout center tags;"


@dataclass
class OsmPlace:
    osm_id: str
    name: str
    lat: float
    lng: float
    tags: dict = field(default_factory=dict)

    @property
    def wikipedia(self) -> Optional[str]:
        """Return a canonical https Wikipedia URL from an OSM `wikipedia=lang:Title` tag."""
        raw = self.tags.get("wikipedia")
        if not raw or ":" not in raw:
            return None
        lang, title = raw.split(":", 1)
        return f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'), safe='')}"

    @property
    def wikidata(self) -> Optional[str]:
        return self.tags.get("wikidata")

    @property
    def height_m(self) -> Optional[float]:
        try:
            return float(str(self.tags.get("height", "")).replace("m", "").strip())
        except ValueError:
            return None


def parse_overpass(payload: dict) -> list[OsmPlace]:
    out: list[OsmPlace] = []
    for el in payload.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name:en") or tags.get("name")
        if not name:
            continue
        if "lat" in el and "lon" in el:
            lat, lng = el["lat"], el["lon"]
        elif "center" in el:
            lat, lng = el["center"]["lat"], el["center"]["lon"]
        else:
            continue
        out.append(OsmPlace(osm_id=f"{el['type']}/{el['id']}", name=name, lat=float(lat), lng=float(lng), tags=tags))
    return out


def fetch_osm_places(fetch: Fetcher, bbox: tuple[float, float, float, float]) -> list[OsmPlace]:
    query = build_overpass_query(bbox)
    data = urllib.parse.urlencode({"data": query}).encode()
    last_exc: Exception | None = None
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            payload = get_json(fetch, endpoint, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}, retries=1)
            return parse_overpass(payload)
        except Exception as exc:  # try the next mirror
            last_exc = exc
    raise last_exc or RuntimeError("no overpass endpoint")


def classify_category(tags: dict) -> str:
    if tags.get("amenity") == "place_of_worship":
        return "church"
    if tags.get("amenity") == "fountain":
        return "fountain"
    if tags.get("tourism") == "museum":
        return "museum"
    if tags.get("tourism") == "viewpoint":
        return "viewpoint"
    if tags.get("man_made") == "obelisk":
        return "monument"
    h = tags.get("historic", "")
    if h in ("ruins", "archaeological_site"):
        return "ruin"
    if h in ("monument", "memorial"):
        return "monument"
    if tags.get("tourism") == "artwork" or h == "statue":
        return "statue"
    if h in ("castle", "palace", "manor"):
        return "palace"
    return "monument"
