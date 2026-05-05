"""
Scrapes Google Trends to retrieve trending topics for article generation.
"""

import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_trending_topics():
    """
    Attempts to retrieve trending topics from Google Trends.
    Falls back to sample topics if web scraping fails (due to JS rendering).

    To use real trending topics, install pytrends: pip install pytrends
    """
    try:
        # Try using pytrends if available
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="en-US", tz=360)
        trending_searches = pytrends.trending_searches(pn="united_states")
        topics = trending_searches[0].tolist()[:5]
        if topics:
            return topics
    except ImportError:
        logger.info("PyTrends not installed. Attempting web scraping...")
    except Exception as e:
        logger.error("PyTrends error: %s", e)

    # Fallback: Try web scraping (likely won't work due to JS rendering)
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily?geo=US"
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        topics = [t.text.strip() for t in soup.select(".details-wrapper .title")]
        if topics:
            return topics[:5]
    except Exception as e:
        logger.error("Web scraping error: %s", e)

    logger.info("Using sample topics for testing...")
    return [
        "Artificial Intelligence in Healthcare",
        "Climate Change Solutions",
        "Remote Work Trends",
        "Sustainable Energy",
        "Digital Privacy",
    ]
