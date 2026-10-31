import datetime as dt
import json
import sqlite3
from pathlib import Path

from lore_citypack.builder import build_from_files, build_pack, match_osm_to_seed, source_title
from lore_citypack.http import NetworkUnavailable
from lore_citypack.osm import OsmPlace, build_overpass_query, classify_category, parse_overpass
from lore_citypack.seed import load_seed
from lore_citypack.wikipedia import candidate_facts_from_summary, summary_endpoint, verify_fact_against_summary, WikiSummary

SEED = Path(__file__).resolve().parents[1] / "data" / "rome_seed.json"
NOW = dt.datetime(2026, 10, 30, tzinfo=dt.timezone.utc)


def offline_fetch(url, data, headers):
    raise NetworkUnavailable("blocked")


def test_offline_build_falls_back_to_seed():
    seed = load_seed(SEED)
    pack = build_pack(seed, online=True, fetch=offline_fetch, now=NOW)
    assert pack["build"]["mode"] == "seed"
    assert any("overpass unavailable" in n for n in pack["build"]["notes"])
    assert pack["stats"]["pois"] == len(seed["pois"])


def test_pack_shape_and_ids():
    pack = build_pack(load_seed(SEED), now=NOW)
    ids = [p["id"] for p in pack["pois"]]
    assert len(ids) == len(set(ids))
    fact_ids = [f["id"] for p in pack["pois"] for f in p["facts"]]
    assert len(fact_ids) == len(set(fact_ids))
    for p in pack["pois"]:
        assert 0 < p["interest"] <= 1
        assert p["footprint"] is None
        for f in p["facts"]:
            assert f["poi_id"] == p["id"]
            assert f["review_status"] == "curated"
            assert f["sources"] and f["sources"][0]["title"]
    assert pack["routing"]["status"] == "not-included-in-v1"


def test_interest_ranks_landmarks_above_minor_sites():
    pack = build_pack(load_seed(SEED), now=NOW)
    by = {p["id"]: p for p in pack["pois"]}
    assert by["rome-colosseum"]["interest"] > by["rome-abate-luigi"]["interest"]
    assert by["rome-pantheon"]["interest"] > by["rome-palazzo-madama"]["interest"]


def test_build_from_files_writes_json_and_sqlite(tmp_path):
    j, s, pack = build_from_files(SEED, tmp_path, now=NOW)
    data = json.loads(j.read_text())
    assert data["stats"]["pois"] >= 60
    con = sqlite3.connect(s)
    n_pois = con.execute("SELECT COUNT(*) FROM pois").fetchone()[0]
    n_facts = con.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
    n_src = con.execute("SELECT COUNT(*) FROM fact_sources").fetchone()[0]
    assert n_pois == data["stats"]["pois"]
    assert n_facts == data["stats"]["facts"]
    assert n_src >= n_facts
    # spatial query works (rtree if compiled in, else lat/lng index)
    rows = con.execute(
        "SELECT name FROM pois WHERE lat BETWEEN 41.8980 AND 41.8992 AND lng BETWEEN 12.4760 AND 12.4780").fetchall()
    assert ("Pantheon",) in rows
    assert con.execute("SELECT value FROM meta WHERE key='city'").fetchone()[0] == "rome"
    con.close()


def test_overpass_query_and_parse():
    q = build_overpass_query((41.87, 12.44, 41.92, 12.51))
    assert "[out:json]" in q and "(41.87,12.44,41.92,12.51)" in q and "out center tags;" in q
    payload = {"elements": [
        {"type": "node", "id": 1, "lat": 41.9, "lon": 12.48, "tags": {"name": "Fontana X", "amenity": "fountain"}},
        {"type": "way", "id": 2, "center": {"lat": 41.8986, "lon": 12.4769},
         "tags": {"name": "Pantheon", "wikipedia": "en:Pantheon, Rome", "wikidata": "Q99309", "historic": "monument", "height": "43 m"}},
        {"type": "node", "id": 3, "lat": 1, "lon": 1, "tags": {}},
    ]}
    places = parse_overpass(payload)
    assert [p.osm_id for p in places] == ["node/1", "way/2"]
    assert places[1].wikipedia == "https://en.wikipedia.org/wiki/Pantheon%2C_Rome"
    assert places[1].height_m == 43.0
    assert classify_category(places[0].tags) == "fountain"


def test_match_osm_by_name_and_distance():
    seed = load_seed(SEED)
    places = [OsmPlace("node/9", "Fontana di Trevi (Trevi Fountain)", 41.90095, 12.48331, {}),
              OsmPlace("node/10", "Some Cafe", 41.9, 12.48, {})]
    matched, unmatched = match_osm_to_seed(seed["pois"], places)
    assert matched["trevi-fountain"].osm_id == "node/9"
    assert [p.osm_id for p in unmatched] == ["node/10"]


def test_online_enrichment_with_mocked_network():
    seed = load_seed(SEED)
    overpass = {"elements": [
        {"type": "way", "id": 42, "center": {"lat": 41.8986, "lon": 12.4769},
         "tags": {"name": "Pantheon", "wikipedia": "en:Pantheon, Rome", "wikidata": "Q99309"}},
        {"type": "node", "id": 77, "lat": 41.8990, "lon": 12.4800,
         "tags": {"name": "Obscure Chapel", "wikipedia": "en:Obscure Chapel", "historic": "monument"}},
    ]}

    def fake_fetch(url, data, headers):
        if "interpreter" in url:
            return json.dumps(overpass).encode()
        if "Obscure_Chapel" in url:
            return json.dumps({"title": "Obscure Chapel", "extract": "Obscure Chapel is a small chapel in Rome built in 1700. It is decorated with frescoes by an unknown painter of the period."}).encode()
        if "summary" in url:
            return json.dumps({"title": "Pantheon, Rome", "extract": "The Pantheon is a former Roman temple, rebuilt by Hadrian. It was consecrated in 609 as a church.", "wikibase_item": "Q99309"}).encode()
        raise NetworkUnavailable(url)

    pack = build_pack(seed, online=True, fetch=fake_fetch, now=NOW)
    assert pack["build"]["mode"] == "seed+online"
    by = {p["id"]: p for p in pack["pois"]}
    assert by["rome-pantheon"]["osm"] == "way/42"
    assert "rome-pantheon-3" in pack["fact_support"]
    assert pack["fact_support"]["rome-pantheon-3"] > 0.3  # "609" + "consecrated" + "church" supported
    # unreviewed auto facts are held back by default...
    assert "rome-obscure-chapel" not in by
    assert any("held for review" in n for n in pack["build"]["notes"])
    # ...and included (flagged) only on explicit request
    pack2 = build_pack(seed, online=True, fetch=fake_fetch, include_unreviewed=True, now=NOW)
    oc = {p["id"]: p for p in pack2["pois"]}["rome-obscure-chapel"]
    assert all(f["review_status"] == "needs_review" for f in oc["facts"])


def test_wikipedia_helpers():
    assert summary_endpoint("https://en.wikipedia.org/wiki/Pantheon,_Rome") == \
        "https://en.wikipedia.org/api/rest_v1/page/summary/Pantheon%2C_Rome"
    s = WikiSummary(url="u", title="T", extract="First sentence has enough words to count here. Second one also has quite enough words in it.")
    assert len(candidate_facts_from_summary(s)) == 2
    assert verify_fact_against_summary("Completed in 1762 by Salvi", WikiSummary("u", "Trevi", "Completed in 1762, designed by Nicola Salvi")) == 1.0
    assert source_title("https://en.wikipedia.org/wiki/Trajan%27s_Column") == "Wikipedia (en): Trajan's Column"
