"""
Flask web application that orchestrates automated article generation workflow.
"""
from flask import Flask

from generator import generate_article, optimize_for_seo
from log import log_article
from publisher import publish_as_markdown
from trends import get_trending_topics

app = Flask(__name__)


@app.route("/run")
def run_automation():
    topics = get_trending_topics()
    for topic in topics:
        article = generate_article(topic)
        keywords, new_intro = optimize_for_seo(article, topic)

        # Replace the original introduction with the optimized one
        # Find the index of the first ## heading
        lines = article.split("\n")
        intro_end = next(
            (i for i, line in enumerate(lines) if line.strip().startswith("##")),
            len(lines),
        )
        optimized_article = new_intro.strip() + "\n\n" + "\n".join(lines[intro_end:])

        publish_as_markdown(topic, optimized_article)
        # log_article(topic, keywords)  # Commented out - Google Sheets logging disabled

    return "✅ Articles generated and published as Markdown files!"


if __name__ == "__main__":
    app.run(port=5000)
