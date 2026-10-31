"""Command line: python -m lore_citypack {build,verify,stats}."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from .builder import build_from_files
from .http import urllib_fetch
from .seed import load_seed
from .wikipedia import try_fetch_summary, verify_fact_against_summary


def cmd_build(a: argparse.Namespace) -> int:
    j, s, pack = build_from_files(a.seed, a.out, online=a.online, include_unreviewed=a.include_unreviewed)
    print(f"built {pack['city']} pack ({pack['build']['mode']}): {pack['stats']['pois']} POIs, "
          f"{pack['stats']['facts']} facts, {pack['stats']['sources']} sources")
    for n in pack["build"]["notes"]:
        print(f"  - {n}")
    print(f"  -> {j}\n  -> {s}")
    return 0


def cmd_verify(a: argparse.Namespace) -> int:
    """Check every curated fact against its Wikipedia article lead (requires network)."""
    seed = load_seed(a.seed)
    report, reached = [], 0
    for p in seed["pois"]:
        url = p.get("wikipedia")
        summ = try_fetch_summary(urllib_fetch, url) if url else None
        if summ is None:
            report.append({"poi": p["slug"], "status": "unreachable-or-missing", "url": url})
            continue
        reached += 1
        for i, f in enumerate(p["facts"], 1):
            report.append({"poi": p["slug"], "fact": i, "support": verify_fact_against_summary(f["text"], summ), "url": url})
    Path(a.report).write_text(json.dumps(report, indent=1))
    print(f"verified against {reached}/{len(seed['pois'])} reachable articles -> {a.report}")
    if reached == 0:
        print("no articles reachable (offline / blocked network); facts remain review_status=curated")
    return 0


def cmd_stats(a: argparse.Namespace) -> int:
    seed = load_seed(a.seed)
    cats: dict[str, int] = {}
    for p in seed["pois"]:
        cats[p["category"]] = cats.get(p["category"], 0) + 1
    print(json.dumps({"pois": len(seed["pois"]), "facts": sum(len(p["facts"]) for p in seed["pois"]), "categories": cats}, indent=1))
    return 0


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(prog="lore_citypack")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="build a city pack")
    b.add_argument("--city", default="rome")
    b.add_argument("--seed", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--online", action="store_true", help="enrich from Overpass + Wikipedia (falls back to seed)")
    b.add_argument("--include-unreviewed", action="store_true", help="ship auto-extracted facts (NOT for customers)")
    b.set_defaults(fn=cmd_build)
    v = sub.add_parser("verify", help="score curated facts against Wikipedia (network)")
    v.add_argument("--seed", required=True)
    v.add_argument("--report", default="output/verify-report.json")
    v.set_defaults(fn=cmd_verify)
    s = sub.add_parser("stats")
    s.add_argument("--seed", required=True)
    s.set_defaults(fn=cmd_stats)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
