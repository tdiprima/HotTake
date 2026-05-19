# HotTake 🔥 💅

**What's buzzing in tech right now?** HotTake finds out, writes about it, and drops polished Markdown on your desk.

HotTake pulls trending topics from Hacker News and Dev.to, generates opinionated, SEO-optimized articles using a local LLM (via Ollama), and presents them to you as Markdown files.

## How It Works

1. **Scans for trends** — Pulls the highest-scoring stories from Hacker News and Dev.to.
2. **Generates a take** — Sends each topic to a local Ollama model to produce a punchy, conversational article.
3. **Optimizes for SEO** — Extracts high-traffic keywords and rewrites the introduction to rank.
4. **Publishes** — Saves each article as a clean Markdown file, ready for your blog or CMS.

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with a model pulled (default: `gemma4:latest`)

### Install

```bash
uv sync
```

### Run

```bash
cd hottake
python main.py
```

Articles land in the current directory as `.md` files.

### Configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama API endpoint |
| `OLLAMA_MODEL` | `gemma4:latest` | Model to use for generation |
| `ENABLE_SHEETS_LOGGING` | `false` | Log article metadata to Google Sheets |

## Project Structure

```
hottake/
  main.py        # Orchestration — fetch, generate, publish
  trends.py      # Topic discovery from Hacker News and Dev.to
  generator.py   # Article generation and SEO optimization via Ollama
  publisher.py   # Markdown file output
  log.py         # Optional Google Sheets logging
```

## License

[MIT](LICENSE)
