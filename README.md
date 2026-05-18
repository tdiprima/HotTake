# Ghost Writer 🖋️ 👻

An automated content pipeline that generates SEO-optimized articles from trending topics using OpenAI and publishes them as Markdown.

## Writing Content Is a Grind

Keeping a blog alive means researching trends, writing drafts, optimizing for search engines, and publishing consistently. Each article demands the same cycle: find a topic, structure an outline, write 1500 words, sprinkle in keywords, and format for the web. Miss a day and your momentum dies.

## Let the Pipeline Handle It

Ghost Writer automates the full loop. It pulls trending topics from Google Trends, generates long-form articles via OpenAI's API, rewrites introductions with targeted SEO keywords, and saves publish-ready Markdown files. Optionally, it logs article metadata to Google Sheets for tracking output over time.

The system runs on-demand from the command line or unattended on a daily schedule.

## What You Get

Given the trending topic "Artificial Intelligence in Healthcare", Ghost Writer produces:

```markdown
# Artificial Intelligence in Healthcare

AI is transforming diagnostics, drug discovery, and patient care at an
unprecedented pace. Healthcare professionals leveraging machine learning
models can now detect conditions earlier and personalize treatment plans...

## How AI Is Revolutionizing Diagnostics
...

## The Role of Machine Learning in Drug Discovery
...
```

Each article includes a rewritten SEO introduction, 10 structured sections, and a call to action — ready to publish.

## Usage

### Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Install

```bash
git clone https://github.com/tdiprima/ghost-writer-py.git
cd ghost-writer-py
pip install .
```

### Configure

```bash
export OPENAI_API_KEY="your-api-key"
```

For Google Sheets logging (optional):

```bash
export ENABLE_SHEETS_LOGGING="true"
```

Then place your Google service account credentials at `creds.json` (see `creds.json.example`) and share a spreadsheet named "Blog Stats" with the service account email.

### Run

```bash
cd ghost-writer-py
python main.py
```

**Scheduled mode (daily at 09:00):**

```bash
python schedule.py
```

### Project Structure

```
ghost-writer-py/
├── main.py         # Entry point, orchestrates the pipeline
├── generator.py    # Article generation and SEO optimization via OpenAI
├── trends.py       # Fetches trending topics from Google Trends
├── publisher.py    # Writes articles to Markdown files
├── log.py          # Optional Google Sheets logging
└── schedule.py     # Daily scheduler entry point
```

## License

[MIT](LICENSE)

<br>
