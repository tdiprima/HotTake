"""
Scrapes Google Trends to retrieve trending topics for article generation.
"""
import requests
from bs4 import BeautifulSoup


def get_trending_topics():
    url = "https://trends.google.com/trends/trendingsearches/daily?geo=US"  # Corrected URL for daily trends
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # Adjusted selector based on typical Google Trends HTML structure (may need updates if HTML changes)
    topics = [t.text.strip() for t in soup.select(".details-wrapper .title")]
    return topics[:5]  # Top 5 trending searches
