"""
Orchestrates automated article generation workflow.
Run: python main.py
"""

import logging
import os

from generator import generate_article, optimize_for_seo
from log import log_article
from publisher import publish_as_markdown
from trends import get_trending_topics

logger = logging.getLogger(__name__)

ENABLE_SHEETS = os.getenv("ENABLE_SHEETS_LOGGING", "false").lower() == "true"


def run():
    """Fetch trending topics, generate and publish articles."""
    topics = get_trending_topics()
    logger.info("Found %d topics: %s", len(topics), topics)

    if not topics:
        logger.warning("No trending topics found. Check internet connection.")
        return

    for topic in topics:
        logger.info("Generating article for topic: %s", topic)
        article = generate_article(topic)
        keywords, new_intro = optimize_for_seo(article, topic)

        lines = article.split("\n")
        intro_end = next(
            (i for i, line in enumerate(lines) if line.strip().startswith("##")),
            len(lines),
        )
        optimized_article = new_intro.strip() + "\n\n" + "\n".join(lines[intro_end:])

        filename = publish_as_markdown(topic, optimized_article)
        logger.info("Published %s", filename)

        if ENABLE_SHEETS:
            log_article(topic, keywords)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    run()
