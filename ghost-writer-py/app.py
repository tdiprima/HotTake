"""
Flask web application that orchestrates automated article generation workflow.
"""

import logging
import os

from flask import Flask
from generator import generate_article, optimize_for_seo
from log import log_article
from publisher import publish_as_markdown
from trends import get_trending_topics

logger = logging.getLogger(__name__)

ENABLE_SHEETS = os.getenv("ENABLE_SHEETS_LOGGING", "false").lower() == "true"

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <h1>Ghost Writer - Automated Article Generator</h1>
    <p>Click the button below to generate articles based on trending topics.</p>
    <form action="/run" method="get">
        <button type="submit" style="padding: 10px 20px; font-size: 16px;">Generate Articles</button>
    </form>
    <p>This could take up to 5 minutes. Go get a coffee. ☕️</p>
    """


@app.route("/run")
def run_automation():
    topics = get_trending_topics()
    logger.info("Found %d topics: %s", len(topics), topics)

    if not topics:
        return "⚠️ No trending topics found. Please check your internet connection or try again later."

    generated_files = []
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
        generated_files.append(filename)
        logger.info("Published %s", filename)

        if ENABLE_SHEETS:
            log_article(topic, keywords)

    return (
        "✅ Articles generated and published as Markdown files!<br><br>Generated files:<br>"
        + "<br>".join(generated_files)
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    app.run(port=5000)
