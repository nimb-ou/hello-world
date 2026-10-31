"""Write a City Pack to SQLite (the on-device storage format; see docs/device-software.md)."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

SCHEMA = """
PRAGMA journal_mode = DELETE;
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE pois (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  lat REAL NOT NULL,
  lng REAL NOT NULL,
  category TEXT NOT NULL,
  interest REAL NOT NULL,
  visible_range_m REAL NOT NULL,
  height_m REAL,
  wikipedia TEXT,
  wikidata TEXT,
  osm TEXT
);
CREATE TABLE poi_tags (poi_id TEXT NOT NULL REFERENCES pois(id), tag TEXT NOT NULL, PRIMARY KEY (poi_id, tag));
CREATE TABLE facts (
  id TEXT PRIMARY KEY,
  poi_id TEXT NOT NULL REFERENCES pois(id),
  ord INTEGER NOT NULL,
  text TEXT NOT NULL,
  kind TEXT NOT NULL,
  depth INTEGER NOT NULL,
  look_up INTEGER NOT NULL DEFAULT 0,
  is_legend INTEGER NOT NULL DEFAULT 0,
  review_status TEXT NOT NULL
);
CREATE TABLE fact_sources (fact_id TEXT NOT NULL REFERENCES facts(id), url TEXT NOT NULL, title TEXT NOT NULL);
-- Placeholder: building footprints (GeoJSON rings) from OSM building=* ways; populated by the
-- footprint stage (not yet implemented) and used by Map Vision for side-of-street + "look up".
CREATE TABLE footprints (poi_id TEXT REFERENCES pois(id), osm_way TEXT, ring_geojson TEXT NOT NULL, height_m REAL);
CREATE INDEX idx_facts_poi ON facts(poi_id);
CREATE INDEX idx_pois_latlng ON pois(lat, lng);
"""


def write_sqlite(pack: dict, path: str | Path) -> Path:
    path = Path(path)
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    try:
        con.executescript(SCHEMA)
        rtree = True
        try:
            con.execute("CREATE VIRTUAL TABLE poi_rtree USING rtree(rid, min_lat, max_lat, min_lng, max_lng)")
        except sqlite3.OperationalError:
            rtree = False
        meta = {
            "schema_version": pack["schema_version"],
            "city": pack["city"],
            "name": pack["name"],
            "bbox": json.dumps(pack["bbox"]),
            "generated_at": pack["generated_at"],
            "build": json.dumps(pack["build"]),
            "routing": json.dumps(pack.get("routing", {})),
            "rtree": "1" if rtree else "0",
        }
        con.executemany("INSERT INTO meta VALUES (?, ?)", meta.items())
        for rid, p in enumerate(pack["pois"], start=1):
            con.execute(
                "INSERT INTO pois VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["lat"], p["lng"], p["category"], p["interest"], p["visible_range_m"],
                 p.get("height_m"), p.get("wikipedia"), p.get("wikidata"), p.get("osm")),
            )
            if rtree:
                con.execute("INSERT INTO poi_rtree VALUES (?,?,?,?,?)", (rid, p["lat"], p["lat"], p["lng"], p["lng"]))
            con.executemany("INSERT INTO poi_tags VALUES (?, ?)", [(p["id"], t) for t in p["tags"]])
            for i, f in enumerate(p["facts"]):
                con.execute(
                    "INSERT INTO facts VALUES (?,?,?,?,?,?,?,?,?)",
                    (f["id"], p["id"], i, f["text"], f["kind"], f["depth"], int(bool(f.get("look_up"))),
                     int(bool(f.get("is_legend"))), f["review_status"]),
                )
                con.executemany("INSERT INTO fact_sources VALUES (?,?,?)", [(f["id"], s["url"], s["title"]) for s in f["sources"]])
        con.commit()
        con.execute("VACUUM")
    finally:
        con.close()
    return path
