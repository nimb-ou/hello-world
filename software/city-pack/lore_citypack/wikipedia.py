"""Wikipedia REST API source (page summaries) used to enrich and verify fact cards."""
from __future__ import annotations

import re
import urllib.parse
from dataclasses import dataclass
from typing import Optional

from .http import Fetcher, NetworkUnavailable, get_json, quote_title


@dataclass
class WikiSummary:
    url: str
    title: str
    extract: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    wikidata: Optional[str] = None


def parse_wiki_url(url: str) -> tuple[str, str]:
    """'https://en.wikipedia.org/wiki/Pantheon,_Rome' -> ('en', 'Pantheon,_Rome') (title unquoted)."""
    m = re.match(r"^https://([a-z\-]+)\.wikipedia\.org/wiki/(.+)$", url)
    if not m:
        raise ValueError(f"not a Wikipedia article URL: {url}")
    return m.group(1), urllib.parse.unquote(m.group(2))


def summary_endpoint(url: str) -> str:
    lang, title = parse_wiki_url(url)
    return f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote_title(title)}"


def fetch_summary(fetch: Fetcher, url: str) -> WikiSummary:
    payload = get_json(fetch, summary_endpoint(url), headers={"Accept": "application/json"}, retries=1)
    if payload.get("type") == "https://mediawiki.org/wiki/HyperSwitch/errors/not_found":
        raise LookupError(f"article not found: {url}")
    coords = payload.get("coordinates") or {}
    return WikiSummary(
        url=url,
        title=payload.get("title", ""),
        extract=payload.get("extract", ""),
        lat=coords.get("lat"),
        lng=coords.get("lon"),
        wikidata=payload.get("wikibase_item"),
    )


_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def candidate_facts_from_summary(summary: WikiSummary, max_facts: int = 2) -> list[str]:
    """Split the lead extract into sentence-level CANDIDATE facts (marked needs_review downstream)."""
    sentences = [s.strip() for s in _SENT.split(summary.extract or "") if 8 <= len(s.split()) <= 60]
    return sentences[:max_facts]


_STOP = {"the", "and", "was", "for", "his", "her", "its", "with", "that", "this", "from", "are", "were", "into", "has", "had",
         "you", "your", "one", "who", "which", "also", "but", "not", "they", "their", "there", "here", "built", "about"}


def keywords(text: str) -> set[str]:
    words = re.findall(r"[A-Za-zÀ-ÿ]{4,}|\d{2,4}", text)
    return {w.lower() for w in words if w.lower() not in _STOP}


def verify_fact_against_summary(fact_text: str, summary: WikiSummary) -> float:
    """Crude support score in [0,1]: share of the fact's numbers and rare keywords found in the article lead.
    Used to triage human review (low score != false; the lead is only a summary)."""
    fact_kw = keywords(fact_text)
    if not fact_kw:
        return 0.0
    src_kw = keywords(summary.extract + " " + summary.title)
    nums = {k for k in fact_kw if k.isdigit()}
    num_ok = len(nums & src_kw) / len(nums) if nums else 1.0
    word_ok = len((fact_kw - nums) & src_kw) / max(1, len(fact_kw - nums))
    return round(0.5 * num_ok + 0.5 * word_ok, 3)


def try_fetch_summary(fetch: Fetcher, url: str) -> Optional[WikiSummary]:
    try:
        return fetch_summary(fetch, url)
    except (NetworkUnavailable, LookupError, ValueError):
        return None
