import sqlite3
from pathlib import Path

import pytest

from lore_citypack.builder import build_from_files
from lore_citypack.seed import haversine_m, load_seed, validate_seed

SEED = Path(__file__).resolve().parents[1] / "data" / "mumbai_seed.json"
REQUIRED = [
    "gateway-of-india", "taj-mahal-palace", "csmvs-museum", "jehangir-art-gallery", "kala-ghoda", "david-sassoon-library",
    "knesset-eliyahoo", "rajabai-clock-tower", "university-of-mumbai-fort", "bombay-high-court", "oval-maidan",
    "oval-art-deco-row", "flora-fountain-hutatma-chowk", "horniman-circle", "asiatic-society-town-hall",
    "st-thomas-cathedral", "reserve-bank-of-india", "bombay-stock-exchange", "csmt", "bmc-headquarters", "regal-cinema",
    "leopold-cafe", "colaba-causeway", "wellington-fountain", "afghan-church", "eros-cinema", "marine-drive",
]


@pytest.fixture(scope="module")
def seed():
    return load_seed(SEED)


def test_valid_and_large_enough(seed):
    assert validate_seed(seed) == []
    assert len(seed["pois"]) >= 60
    assert all(2 <= len(p["facts"]) <= 4 for p in seed["pois"])


def test_required_heritage_pois(seed):
    slugs = {p["slug"] for p in seed["pois"]}
    assert [s for s in REQUIRED if s not in slugs] == []


def test_unesco_sources_cited(seed):
    urls = {s["url"] for p in seed["pois"] for f in p["facts"] for s in f.get("sources", [])}
    assert "https://whc.unesco.org/en/list/1480" in urls  # Victorian Gothic and Art Deco Ensembles (2018)
    assert "https://whc.unesco.org/en/list/945" in urls   # CSMT (2004)


def test_spot_coordinates(seed):
    by = {p["slug"]: p for p in seed["pois"]}
    known = {"gateway-of-india": (18.9220, 72.8347), "csmt": (18.9400, 72.8355), "rajabai-clock-tower": (18.9297, 72.8293)}
    for slug, (lat, lng) in known.items():
        assert haversine_m(by[slug]["lat"], by[slug]["lng"], lat, lng) < 150


def test_build_mumbai_pack(tmp_path):
    j, s, pack = build_from_files(SEED, tmp_path)
    assert j.name == "mumbai.pack.json" and pack["city"] == "mumbai"
    con = sqlite3.connect(s)
    assert con.execute("SELECT COUNT(*) FROM pois").fetchone()[0] == pack["stats"]["pois"]
    assert con.execute("SELECT COUNT(*) FROM facts WHERE poi_id LIKE 'mumbai-%'").fetchone()[0] == pack["stats"]["facts"]
    con.close()
