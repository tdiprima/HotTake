"""
Generates SEO-optimized articles using a local Ollama model.
"""

import json
import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:latest")

client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


def generate_article(topic):
    # Include:
    # - catchy introduction
    # - clear headings with explanations
    # - engaging examples
    # - conclude with a call to action
    # Use a conversational tone like Medium or Dev.to.
    # Make it sound interesting.
    # Write like a human.

    prompt = f"""
    Write a 600-word SEO-optimized article (and especially an SEO-optimized title) about "{topic}".

    Style and voice:
    - Conversational, direct, slightly cynical. Sound like a smart person
      explaining something informally, not a corporate blog.
    - Call out BS and corporate spin directly. Mock sanitized language
      by quoting it then countering with what it actually means.
    - Short punchy paragraphs. One to three sentences max per paragraph.
    - Use sentence fragments deliberately for emphasis. "Not because of
      passwords. Because of context."
    - Stack short phrases on separate lines instead of bullet lists.
      Like this: "Search history. Watch history. Download logs. Timestamps."
    - Subheadings should be opinionated or editorial, not generic SEO labels.
      Example: "The 'we weren't hacked' defense" not "Understanding Data Breaches".
    - Use second person ("you") mixed with broader observations.
    - Ground every point with a concrete example or real consequence.
      No vague claims without showing why it matters.
    - Build tension with short fragments, then deliver the punchline.
    - End with a bigger-picture takeaway, not a generic call to action.

    Format using Markdown: use ## for headings.
    """
    #  (do not include a # title at the top)

    response = client.chat.completions.create(
        model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}]
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
        model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}]
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
