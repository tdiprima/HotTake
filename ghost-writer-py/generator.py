"""
Generates SEO-optimized articles using OpenAI's API.
"""
import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_article(topic):
    prompt = f"""
    Write a 1500-word SEO-optimized article about "{topic}".
    Include:
    - catchy introduction
    - 10 clear headings with explanations
    - engaging examples
    - conclude with a call to action
    Use a conversational tone like Medium or Dev.to.
    Format using Markdown: use ## for headings (do not include a # title at the top).
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def optimize_for_seo(article, topic):
    prompt = f"""
    Analyze this article about '{topic}' and provide:
    - A list of 5 high-traffic keywords.
    - A rewritten introduction that includes these keywords naturally.
    Output in JSON format: {{"keywords": ["kw1", "kw2", "kw3", "kw4", "kw5"], "introduction": "text of the rewritten introduction"}}
    Article:
    {article}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    optimized_data = json.loads(response.choices[0].message.content)
    return optimized_data["keywords"], optimized_data["introduction"]
