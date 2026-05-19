"""
Retrieves trending topics from Google Trends for article generation.

Sources (tried in order):
1. Google Trends API v1alpha (requires service account with alpha access)
2. Google Trends RSS feed (public, no auth required)
3. Sample topics (offline fallback)

API alpha access: https://developers.google.com/search/apis/trends#apply
"""

import logging
import os
from xml.etree import ElementTree

import requests
from google.auth.transport.requests import Request as AuthRequest
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

TRENDS_API_BASE = "https://searchtrends.googleapis.com/v1alpha"
TRENDS_API_SCOPE = "https://www.googleapis.com/auth/trends.readonly"
TRENDS_CREDS_PATH = os.getenv("GOOGLE_TRENDS_CREDENTIALS", "")

RSS_URL = "https://trends.google.com/trending/rss?geo=US"

REQUEST_TIMEOUT_SECONDS = 15
POLL_TIMEOUT_SECONDS = 30
POLL_INTERVAL_SECONDS = 2
MAX_TOPICS = 5


def get_trending_topics():
    """
    Retrieve trending topics, trying each source in order:
    1. Google Trends API v1alpha
    2. Google Trends RSS feed
    3. Hardcoded sample topics (fallback)
    """
    topics = _fetch_from_api()
    if topics:
        return topics[:MAX_TOPICS]

    topics = _fetch_from_rss()
    if topics:
        return topics[:MAX_TOPICS]

    logger.warning("All trend sources failed. Using sample topics.")
    return _sample_topics()


def _get_api_credentials():
    """Load service account credentials scoped for the Trends API."""
    if not TRENDS_CREDS_PATH:
        return None

    if not os.path.isfile(TRENDS_CREDS_PATH):
        logger.warning("Trends credentials file not found: %s", TRENDS_CREDS_PATH)
        return None

    creds = Credentials.from_service_account_file(
        TRENDS_CREDS_PATH, scopes=[TRENDS_API_SCOPE]
    )
    creds.refresh(AuthRequest())
    return creds


def _fetch_from_api():
    """
    Fetch trending topics via the Google Trends API v1alpha.

    Uses an async operation pattern:
    1. POST a query spec to create an operation
    2. Poll the operation until results are ready
    """
    creds = _get_api_credentials()
    if creds is None:
        return []

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }

    # Step 1: Submit the trending query
    spec = {
        "spec": {
            "geo": {
                "type": "GEO_TYPE_COUNTRY_OR_REGION",
                "code": "US",
            },
            "timeResolution": "DAY",
        }
    }

    try:
        response = requests.post(
            f"{TRENDS_API_BASE}/trendingSearches:query",
            json=spec,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        result = response.json()

        # If the response contains an operation name, poll for results
        if "name" in result:
            return _poll_operation(result["name"], headers)

        return _extract_topics(result)

    except requests.RequestException as exc:
        logger.error("Trends API request failed: %s", exc)
        return []
    except (KeyError, ValueError) as exc:
        logger.error("Trends API response parse failed: %s", exc)
        return []


def _poll_operation(operation_name, headers):
    """Poll an async operation until it completes or times out."""
    import time

    url = f"{TRENDS_API_BASE}/operations/{operation_name}"
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS

    while time.monotonic() < deadline:
        try:
            response = requests.get(
                url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            result = response.json()

            if result.get("done"):
                return _extract_topics(result.get("response", {}))

            time.sleep(POLL_INTERVAL_SECONDS)

        except requests.RequestException as exc:
            logger.error("Trends API poll failed: %s", exc)
            return []

    logger.warning("Trends API operation timed out after %ds.", POLL_TIMEOUT_SECONDS)
    return []


def _extract_topics(data):
    """Pull topic titles from the API response."""
    topics = []

    # The v1alpha response structure may vary; try known paths
    for item in data.get("trendingSearches", data.get("items", [])):
        title = item.get("title", item.get("query", ""))
        if isinstance(title, dict):
            title = title.get("query", "")
        title = str(title).strip()
        if title:
            topics.append(title)

    if topics:
        logger.info("Fetched %d trending topics from Trends API.", len(topics))
    return topics


def _fetch_from_rss():
    """Fetch daily trending searches from the Google Trends RSS feed."""
    try:
        response = requests.get(RSS_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()

        root = ElementTree.fromstring(response.content)
        titles = [item.find("title").text.strip()
                  for item in root.iter("item")
                  if item.find("title") is not None
                  and item.find("title").text]

        if titles:
            logger.info("Fetched %d trending topics from RSS feed.", len(titles))
            return titles

        logger.warning("RSS feed returned no items.")
        return []

    except requests.RequestException as exc:
        logger.error("RSS feed request failed: %s", exc)
        return []
    except ElementTree.ParseError as exc:
        logger.error("RSS feed XML parse failed: %s", exc)
        return []


def _sample_topics():
    """Hardcoded topics for offline development and testing."""
    return [
        "Artificial Intelligence in Healthcare",
        "Climate Change Solutions",
        "Remote Work Trends",
        "Sustainable Energy",
        "Digital Privacy",
    ]
