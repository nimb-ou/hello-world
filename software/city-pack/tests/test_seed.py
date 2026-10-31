import copy
import json
from pathlib import Path

import pytest

from lore_citypack.seed import SeedError, haversine_m, load_seed, validate_seed

SEED = Path(__file__).resolve().parents[1] / "data" / "rome_seed.json"

REQUIRED = [
    "colosseum", "pantheon", "trevi-fountain", "piazza-navona", "campo-de-fiori", "largo-di-torre-argentina",
    "bocca-della-verita", "ponte-sant-angelo", "keyhole-knights-of-malta", "pasquino", "elephant-and-obelisk",
    "via-margutta", "arco-degli-acetari", "quartiere-coppede",
]


@pytest.fixture(scope="module")
def seed():
    return load_seed(SEED)


def test_seed_is_valid(seed):
    assert validate_seed(seed) == []


def test_at_least_60_pois_with_2_to_4_facts(seed):
    assert len(seed["pois"]) >= 60
    for p in seed["pois"]:
        assert 2 <= len(p["facts"]) <= 4, p["slug"]


def test_required_landmarks_and_hidden_gems_present(seed):
    slugs = {p["slug"] for p in seed["pois"]}
    missing = [s for s in REQUIRED if s not in slugs]
    assert not missing


def test_every_fact_has_https_source(seed):
    for p in seed["pois"]:
        for f in p["facts"]:
            srcs = f.get("sources") or [{"url": p.get("wikipedia")}]
            assert all(s["url"] and s["url"].startswith("https://") for s in srcs), p["slug"]


def test_known_coordinates_are_accurate(seed):
    """Spot-check against independently known coordinates (tolerance 120 m)."""
    by = {p["slug"]: p for p in seed["pois"]}
    known = {"colosseum": (41.8902, 12.4922), "pantheon": (41.8986, 12.4769), "trevi-fountain": (41.9009, 12.4833),
             "st-peters-basilica": (41.9022, 12.4539)}
    for slug, (lat, lng) in known.items():
        assert haversine_m(by[slug]["lat"], by[slug]["lng"], lat, lng) < 120


def test_legend_facts_flagged(seed):
    for p in seed["pois"]:
        for f in p["facts"]:
            if f["kind"] == "legend":
                assert f.get("is_legend") is True


def test_validator_catches_errors():
    data = json.loads(SEED.read_text())
    bad = copy.deepcopy(data)
    bad["pois"][0]["lat"] = 10.0
    bad["pois"][1]["facts"] = bad["pois"][1]["facts"][:1]
    bad["pois"][2]["facts"][0]["sources"] = [{"url": "http://insecure.example"}]
    bad["pois"][3]["slug"] = bad["pois"][4]["slug"]
    errs = validate_seed(bad)
    joined = "\n".join(errs)
    assert "outside city bbox" in joined
    assert "needs 2-4 facts" in joined
    assert "https" in joined
    assert "duplicate slug" in joined


def test_load_seed_raises_on_invalid(tmp_path):
    data = json.loads(SEED.read_text())
    data["pois"][0]["category"] = "spaceport"
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(data))
    with pytest.raises(SeedError):
        load_seed(p)
