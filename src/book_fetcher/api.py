"""Fetch books from OpenLibrary API with retry support."""

import sys
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENT = "BookFetcher/1.0 (your.email@example.com)"


def _create_session() -> requests.Session:
    """Create a requests session with retry logic and proper User-Agent."""
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def fetch_books(limit: int, subject: str, min_year: int) -> list[dict[str, Any]]:
    """Fetch books from OpenLibrary API that match criteria."""
    base_url = "https://openlibrary.org"
    url = (
        f"{base_url}/search.json"
        f"?q=subject:{subject}"
        f"&limit={limit}"
        f"&first_publish_year>={min_year}"
    )
    session = _create_session()
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        docs: list[dict[str, Any]] = data.get("docs", [])
        return docs
    except requests.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
        sys.exit(1)
