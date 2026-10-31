"""Tiny HTTP layer (stdlib only) so the builder runs on any CI box and can be mocked in tests."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Optional

USER_AGENT = "LORE-CityPack-Builder/0.1 (https://lore.travel; software@lore.travel)"

# Signature: (url, data_or_None, headers) -> bytes. Tests inject a fake.
Fetcher = Callable[[str, Optional[bytes], dict], bytes]


class NetworkUnavailable(RuntimeError):
    """Raised when a remote source cannot be reached (offline, blocked, or rate-limited)."""


def urllib_fetch(url: str, data: Optional[bytes] = None, headers: Optional[dict] = None, timeout: float = 30.0) -> bytes:
    req = urllib.request.Request(url, data=data, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - fixed https hosts
            return resp.read()
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
        raise NetworkUnavailable(f"{url}: {exc}") from exc


def get_json(fetch: Fetcher, url: str, data: Optional[bytes] = None, headers: Optional[dict] = None,
             retries: int = 2, backoff_s: float = 1.5) -> Any:
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            raw = fetch(url, data, headers or {})
            return json.loads(raw.decode("utf-8"))
        except NetworkUnavailable as exc:
            last = exc
            if attempt < retries:
                time.sleep(backoff_s * (attempt + 1))
        except json.JSONDecodeError as exc:
            raise NetworkUnavailable(f"{url}: non-JSON response ({exc})") from exc
    raise NetworkUnavailable(str(last))


def quote_title(title: str) -> str:
    return urllib.parse.quote(title.replace(" ", "_"), safe="")
