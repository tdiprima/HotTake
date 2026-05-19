"""
Publishes generated articles as Markdown files.
"""

import re


def publish_as_markdown(title, content):
    # Sanitize filename (replace spaces and special chars)
    safe_title = re.sub(r"[^a-zA-Z0-9_-]", "", title.replace(" ", "_")).lower()
    filename = f"{safe_title}.md"

    with open(filename, "w") as f:
        f.write(f"# {title}\n\n")
        f.write(content)

    return filename
