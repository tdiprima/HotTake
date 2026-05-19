"""
Fetches trending technology topics from Hacker News and Dev.to
for article generation.
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

logger = logging.getLogger(__name__)

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
DEVTO_ARTICLES_URL = "https://dev.to/api/articles"

REQUEST_TIMEOUT = 10
TOPIC_COUNT = 5
HN_CANDIDATE_COUNT = 30


def _fetch_hn_item(item_id):
    """Fetch a single Hacker News item by ID."""
    response = requests.get(
        HN_ITEM_URL.format(item_id=item_id), timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def _get_hn_topics():
    """
    Fetch top stories from Hacker News, sorted by score.
    Returns the highest-scored titles as topic strings.
    """
    response = requests.get(HN_TOP_STORIES_URL, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    story_ids = response.json()[:HN_CANDIDATE_COUNT]

    stories = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_fetch_hn_item, sid): sid for sid in story_ids}
        for future in as_completed(futures):
            try:
                story = future.result()
                if story and story.get("title"):
                    stories.append(story)
            except Exception as exc:
                logger.debug("Failed to fetch HN item %s: %s", futures[future], exc)

    stories.sort(key=lambda s: s.get("score", 0), reverse=True)
    return [story["title"] for story in stories[:TOPIC_COUNT]]


def _get_devto_topics():
    """Fetch trending technology articles from Dev.to."""
    response = requests.get(
        DEVTO_ARTICLES_URL,
        params={"per_page": TOPIC_COUNT, "tag": "technology", "top": 1},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    articles = response.json()
    return [article["title"] for article in articles if article.get("title")]


def get_trending_topics():
    """
    Retrieve trending technology topics.

    Tries Hacker News first (tech-focused, free, no auth),
    then Dev.to, then falls back to default topics.
    """
    sources = [
        ("Hacker News", _get_hn_topics),
        ("Dev.to", _get_devto_topics),
    ]

    for name, fetch_fn in sources:
        try:
            topics = fetch_fn()
            if topics:
                logger.info("Fetched %d topics from %s", len(topics), name)
                return topics[:TOPIC_COUNT]
        except Exception as exc:
            logger.warning("Failed to fetch from %s: %s", name, exc)

    logger.info("All sources failed. Using default topics.")
    return [
        "Artificial Intelligence in Healthcare",
        "Climate Change Solutions",
        "Remote Work Trends",
        "Sustainable Energy",
        "Digital Privacy",
    ]
