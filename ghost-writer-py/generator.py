"""
Generates SEO-optimized articles using OpenAI's API.
"""

import json
import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_article(topic):
    prompt = f"""
    Write a 600-word SEO-optimized article about "{topic}".
    Include:
    - catchy introduction
    - clear headings with explanations
    - engaging examples
    - conclude with a call to action
    Use a conversational tone like Medium or Dev.to.
    Make it sound interesting.
    Write like a human.

    Format using Markdown: use ## for headings (do not include a # title at the top).
    """

    response = client.chat.completions.create(
        model="gpt-5.5", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def optimize_for_seo(article, topic):
    prompt = f"""
    Analyze this article about '{topic}' and provide:
    - A list of 5 high-traffic keywords.
    - A rewritten introduction that includes these keywords naturally.
    Output ONLY valid JSON, no markdown code blocks or other text: {{"keywords": ["kw1", "kw2", "kw3", "kw4", "kw5"], "introduction": "text of the rewritten introduction"}}
    Article:
    {article}
    """
    response = client.chat.completions.create(
        model="gpt-5.2", messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown code blocks if present
    if content.startswith("```json"):
        content = content[7:]  # Remove ```json
    elif content.startswith("```"):
        content = content[3:]  # Remove ```

    if content.endswith("```"):
        content = content[:-3]  # Remove trailing ```

    content = content.strip()

    try:
        optimized_data = json.loads(content)
        return optimized_data["keywords"], optimized_data["introduction"]
    except json.JSONDecodeError as e:
        logger.error("Error parsing JSON response: %s", e)
        logger.error("Raw content: %s...", content[:200])
        return ["SEO", "article", topic, "content", "guide"], (
            article.split("\n\n")[0] if article else ""
        )
