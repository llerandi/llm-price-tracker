# LLM Price Tracker

[![CI](https://img.shields.io/github/actions/workflow/status/llerandi/llm-price-tracker/ci.yaml?label=CI&logo=github)](https://github.com/llerandi/llm-price-tracker/actions/workflows/ci.yaml)
[![License](https://img.shields.io/github/license/llerandi/llm-price-tracker)](LICENSE)
[![Stars](https://img.shields.io/github/stars/llerandi/llm-price-tracker?style=social)](https://github.com/llerandi/llm-price-tracker/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/llerandi/llm-price-tracker)](https://github.com/llerandi/llm-price-tracker/commits/main)
[![Updated daily](https://img.shields.io/badge/last--updated-2026--07--29-brightgreen)](https://github.com/llerandi/llm-price-tracker/actions/workflows/update.yaml)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue?logo=python)](https://www.python.org/)
[![Live site](https://img.shields.io/badge/live%20site-GitHub%20Pages-0969da)](https://llerandi.github.io/llm-price-tracker/)

A daily-updated reference of LLM model pricing across all major providers. One source of truth for input/output token costs, context windows, and capabilities - structured as JSON so you can consume it programmatically.

**Live site:** [llerandi.github.io/llm-price-tracker](https://llerandi.github.io/llm-price-tracker/) - sortable, filterable table updated daily.

> [!TIP]
> Looking for rate limits (RPM, TPM, RPD) instead? See the sister project: [LLM Rate Limits Tracker](https://github.com/llerandi/llm-rate-limits-tracker)

---

## Pricing Table

Prices in USD per 1 million tokens. Sorted by provider, then by input price.

<!-- PRICING_TABLE_START -->
| Provider | Model | Input ($/1M) | Output ($/1M) | Context | Capabilities |
|----------|-------|:------------:|:-------------:|:-------:|:------------:|
| AI21 Labs | Jamba 1.7 Large | $2.00 | $8.00 | 256K | tools |
| Amazon Bedrock | Nova Micro | $0.04 | $0.14 | 128K | tools |
| Anthropic | Claude Haiku 4.5 | $1.00 | $5.00 | 200K | vision, tools |
| Cohere | Command R7B | $0.04 | $0.15 | 128K | tools |
| DeepSeek | DeepSeek V4 | $0.07 | $0.28 | 64K | tools |
| Fireworks AI | DeepSeek V4 Flash | $0.14 | $0.28 | 128K | tools |
| Google | Gemini 2.5 Flash Lite | $0.10 | $0.40 | 1M | vision, tools |
| Groq | Llama 4 Scout | $0.05 | $0.08 | 128K | vision, tools |
| Mistral | Devstral Small 2 | $0.10 | $0.30 | 128K | tools |
| OpenAI | GPT-5 Nano | $0.05 | $0.40 | 32K | tools |
| Perplexity | Sonar | $1.00 | $1.00 | 128K | - |
| Qwen | Qwen3 Turbo | $0.08 | $0.25 | 128K | tools |
| Together AI | Llama 4 Scout | $0.18 | $0.59 | 128K | vision, tools |
| xAI | Grok Build 0.1 | $1.00 | $2.00 | 256K | tools |
_Showing the cheapest model per provider (14 providers shown, 50 models total). [**View all models with filters and comparison →**](https://llerandi.github.io/llm-price-tracker/)_
<!-- PRICING_TABLE_END -->

---

## Batch and Cache Pricing

Some providers offer discounted rates for asynchronous (batch) processing and prompt caching. Prices in USD per 1 million tokens.

- **Batch**: requests are queued and processed asynchronously (typically within 24 hours) at ~50% off standard rates.
- **Cache read**: tokens served from the prompt cache at a fraction of the standard input cost.
- **Cache write**: tokens written to the cache, billed once at a slight premium over the standard input cost (Anthropic and GPT-5.6 models).

<!-- BATCH_CACHE_TABLE_START -->
_Batch and cache pricing is available for select models. [**See full pricing table →**](https://llerandi.github.io/llm-price-tracker/)_
<!-- BATCH_CACHE_TABLE_END -->

> **Official batch and caching docs:**
> [Anthropic batch](https://docs.anthropic.com/en/docs/build-with-claude/message-batches) -
> [Anthropic caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) -
> [OpenAI batch](https://platform.openai.com/docs/guides/batch) -
> [OpenAI caching](https://platform.openai.com/docs/guides/prompt-caching)

---

> **Notes on specific models:**
> - Gemini 2.5 Pro: input $2.50/1M and output $15.00/1M above 200K tokens.
> - GPT-5.6 Sol, Terra, and Luna: requests above 272K tokens charged at 2x input and 1.5x output.
> - Perplexity Sonar models: token prices above exclude a per-request fee of $5-14/1K requests (varies by search context size).
>
> **Official pricing pages:**
> [AI21 Labs](https://docs.ai21.com/docs/usage-cost) -
> [Amazon Bedrock](https://aws.amazon.com/bedrock/pricing/) -
> [Anthropic](https://www.anthropic.com/pricing) -
> [Cohere](https://cohere.com/pricing) -
> [Fireworks AI](https://fireworks.ai/pricing) -
> [Google](https://ai.google.dev/pricing) -
> [Mistral](https://mistral.ai/technology/#pricing) -
> [OpenAI](https://platform.openai.com/pricing) -
> [Perplexity](https://docs.perplexity.ai/docs/getting-started/pricing) -
> [Together AI](https://www.together.ai/pricing) -
> [xAI](https://x.ai/api)

---

## Embeddable Badges

Add a live price badge to any README. Badges update daily and are served via jsDelivr CDN.

**URL pattern:**

```
https://img.shields.io/endpoint?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fllerandi%2Fllm-price-tracker%40main%2Fdata%2Fbadges%2F{model-id}-{input|output|context}.json
```

Model IDs with slashes (e.g. Fireworks AI, Together AI) have the `/` replaced with `-` in the filename. Browse all IDs in [`data/prices.json`](data/prices.json) or check [`data/badges/`](data/badges/).

**Example - Claude Sonnet 5 input price:**

[![Claude Sonnet 5 input](https://img.shields.io/endpoint?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fllerandi%2Fllm-price-tracker%40main%2Fdata%2Fbadges%2Fclaude-sonnet-5-input.json)](https://llerandi.github.io/llm-price-tracker/)

```markdown
[![Claude Sonnet 5 input](https://img.shields.io/endpoint?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fllerandi%2Fllm-price-tracker%40main%2Fdata%2Fbadges%2Fclaude-sonnet-5-input.json)](https://llerandi.github.io/llm-price-tracker/)
```

Use the [live site](https://llerandi.github.io/llm-price-tracker/) to browse all models and copy badge embed code directly.

---

## API Reference

All endpoints are static JSON files served via jsDelivr CDN with full CORS support (`Access-Control-Allow-Origin: *`). No API key required. Updated and CDN-purged daily at 06:00 UTC.

**Base URL:** `https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main`

| Endpoint | Description |
|----------|-------------|
| `/data/prices.json` | All models from all providers |
| `/data/latest.json` | Permanent alias for `prices.json` - stable URL that always points to the current data |
| `/data/providers/{provider}.json` | Models for a single provider (e.g. `anthropic`, `openai`, `google`, `mistral`, `cohere`, `together-ai`, `fireworks-ai`, `ai21-labs`, `xai`, `perplexity`, `amazon-bedrock`, `deepseek`, `groq`, `qwen`) |
| `/data/history/YYYY-MM-DD.json` | Price snapshot for a given date |
| `/data/history_summary.json` | Consolidated time-series of input/output prices for all models (used by the price history chart) |
| `/data/feed.xml` | Atom 1.0 feed of daily price changes - subscribe in any RSS reader |
| `/data/changelog.md` | All price changes and model additions/removals, newest first |
| `/data/badges/{model-id}-input.json` | shields.io endpoint badge for input price |
| `/data/badges/{model-id}-output.json` | shields.io endpoint badge for output price |
| `/data/badges/{model-id}-context.json` | shields.io endpoint badge for context window |

Model IDs that contain `/` (Fireworks AI, Together AI) use `-` in badge filenames.

### Schema stability

The JSON schema is stable. New fields may be added in future but existing fields will not be renamed or removed without a deprecation period. `input_per_1m_usd`, `output_per_1m_usd`, `context_window_k`, and all boolean capability fields are guaranteed to remain in the schema. Optional fields (`batch_*`, `cache_*`, `notes`) are present only when data is available; treat their absence or `null` as equivalent.

### Endpoints

**Get all models (curl):**

```bash
curl https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main/data/prices.json
```

**Get models for a single provider (curl):**

```bash
curl https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main/data/providers/anthropic.json
```

**Filter by price (Python, no dependencies):**

```python
import urllib.request, json

url = "https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main/data/prices.json"
with urllib.request.urlopen(url) as r:
    data = json.load(r)

cheap = [m for m in data["models"] if (m["input_per_1m_usd"] or 999) < 1.0]
for m in cheap:
    print(f"{m['provider']} {m['model_name']}: ${m['input_per_1m_usd']}/1M in")
```

**Filter by capability (JavaScript):**

```js
const res = await fetch(
  "https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main/data/prices.json"
);
const { models } = await res.json();

// Models with vision support under $5/1M input
const visionModels = models.filter(
  m => m.supports_vision && (m.input_per_1m_usd ?? Infinity) < 5
);
```

**Get a specific provider (JavaScript):**

```js
const res = await fetch(
  "https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main/data/providers/anthropic.json"
);
const { models } = await res.json();
```

### JSON Schema

Each entry in `models` contains:

| Field | Type | Description |
|-------|------|-------------|
| `provider` | string | Provider display name (e.g. `"OpenAI"`) |
| `model_id` | string | API identifier used when calling the provider |
| `model_name` | string | Human-readable model name |
| `input_per_1m_usd` | number or null | Input cost per 1M tokens in USD |
| `output_per_1m_usd` | number or null | Output cost per 1M tokens in USD |
| `context_window_k` | integer or null | Context window size in thousands of tokens |
| `supports_vision` | boolean | Accepts image inputs |
| `supports_function_calling` | boolean | Supports tool/function call syntax |
| `is_reasoning` | boolean | Chain-of-thought / extended thinking model |
| `tier` | string | `"efficient"`, `"performance"`, `"flagship"`, or `"specialized"` |
| `notes` | string or null | Pricing caveats or special conditions |
| `batch_input_per_1m_usd` | number or null | Asynchronous batch input price (optional) |
| `batch_output_per_1m_usd` | number or null | Asynchronous batch output price (optional) |
| `cache_read_per_1m_usd` | number or null | Prompt cache read price (optional) |
| `cache_write_per_1m_usd` | number or null | Prompt cache write price (optional) |

**Top-level fields in `prices.json`:**

| Field | Type | Description |
|-------|------|-------------|
| `last_updated` | string | ISO 8601 date of the last update (`"YYYY-MM-DD"`) |
| `models` | array | Array of model objects (see above) |

---

## Client Libraries

Installable wrappers around the jsDelivr JSON API. Both are zero-dependency and read-only.

### JavaScript / TypeScript (Node >= 18 and browsers)

```bash
npm install llm-price-tracker
```

```js
const { fetchPrices, getModel, getProvider } = require("llm-price-tracker");

// All models
const { models } = await fetchPrices();

// Single model
const sonnet = await getModel("claude-sonnet-5");
console.log(sonnet.input_per_1m_usd); // 2.00

// All models for a provider
const { models: anthropicModels } = await getProvider("anthropic");
```

Source: [`packages/npm/`](packages/npm/)

### Python (>= 3.9, no dependencies)

```bash
pip install llm-price-tracker
```

```python
from llm_price_tracker import fetch_prices, get_model, get_provider

# All models
data = fetch_prices()

# Single model
sonnet = get_model("claude-sonnet-5")
print(sonnet["input_per_1m_usd"])  # 2.0

# All models for a provider
anthropic = get_provider("anthropic")
```

Source: [`packages/python/`](packages/python/)

---

## Contributing

Prices change frequently. If you spot an outdated entry or a missing model, contributions are welcome.

1. Fork the repository and create a branch.
2. Edit `data/prices.json` with the correct values.
3. Run `python scripts/validate.py` to check the schema.
4. Run `python scripts/verify_prices.py` to check consistency (prices positive, batch <= standard, no duplicates).
5. Run `python scripts/update_prices.py` to regenerate the README table.
6. Open a pull request with a link to the official pricing page as evidence.

To add a new provider, add a new entry in `data/prices.json` following the existing schema.

---

## How It Works

A GitHub Actions workflow (`update.yaml`) runs daily at 06:00 UTC. It runs `scripts/update_prices.py`, which:

1. Sorts all entries by provider and input price.
2. Updates the `last_updated` timestamp in `prices.json`.
3. Regenerates the pricing table in this README using HTML comment markers as boundaries.
4. Writes a compact daily snapshot to `data/history/YYYY-MM-DD.json` with just the pricing fields.
5. Commits and pushes if there are changes.

A second workflow (`ci.yaml`) runs on every push and pull request to lint the scripts and validate the JSON schema.

---

## Troubleshooting

**The live site or badges show stale data.**

The daily workflow automatically purges the jsDelivr CDN cache after each push, so data is normally fresh within seconds. If you are still seeing stale data, hard-refresh the live site (`Ctrl+Shift+R` on Windows/Linux, `Cmd+Shift+R` on Mac). To force a manual purge for a specific file, open this URL in your browser:

```
https://purge.jsdelivr.net/gh/llerandi/llm-price-tracker@main/data/prices.json
```

---

## Roadmap

### Phase 1 - Foundation

- [x] JSON schema definition
- [x] Initial pricing data: Anthropic, Google, Mistral, OpenAI
- [x] Auto-generated README pricing table from JSON
- [x] CI pipeline (lint + JSON validation)
- [x] Daily automated update workflow

### Phase 2 - Expand

- [x] Add providers: Cohere, Together AI, Fireworks AI, AI21 Labs
- [x] Add batch pricing and prompt caching columns
- [x] Track price history with daily snapshots

### Phase 3 - Tooling

- [x] GitHub Pages site with sortable and filterable table
- [x] Embeddable price badge for other repositories
- [x] REST-like endpoint via jsDelivr CDN with CORS support

### Phase 4 - Insights

- [x] Price history chart on the live site (visualize changes over time per model)
- [x] Auto-generated changelog: markdown summary of price changes by date
- [x] Cost calculator on the live site (tokens x price = estimated cost)
- [x] Add providers: xAI (Grok), Perplexity, AWS Bedrock

### Phase 5 - Community

- [x] Automated price verification: script that cross-checks prices against official pages
- [x] Support for multiple currencies (EUR, GBP) on the live site
- [x] npm / PyPI package wrapping the jsDelivr JSON endpoint

### Phase 6 - Automation and Discovery

- [x] Automated GitHub Issue when a price changes by more than 10% (subscribe via Watch -> Issues)
- [x] RSS/Atom feed of price changes, generated daily and served as static XML via jsDelivr CDN
- [x] Add providers: DeepSeek, Groq, Qwen (Alibaba Cloud)
- [x] Filters on the live site by tier, capabilities, and max price
- [x] Model comparison view: select two models for a side-by-side diff

### Phase 7 - Polish and Reach

- [x] Dark mode with manual toggle (light by default, persisted in localStorage)
- [x] data/latest.json permanent alias for the current prices
- [x] Weekly price summary posted to GitHub Discussions every Monday
- [x] SEO: sitemap.xml, Open Graph meta tags, JSON-LD structured data
- [x] Embeddable context window badge (alongside existing price badges)
- [x] Export current filtered table as CSV
- [x] Shareable URLs: query params preserve active filters and comparison
- [x] Changelog section on the live site
- [x] Cost calculator presets (10-page PDF, code review, 1K support chats, article summary)
- [x] Embedding model pricing (OpenAI, Google, Cohere, Voyage AI)
- [x] More currencies: JPY, CAD, AUD (with fallback rates if API fails)
- [x] Provider stats: aggregate summary per provider on the live site

### Phase 8 - CDN Reliability and API

- [x] Auto-purge jsDelivr CDN cache after every daily update (prices, badges, feed, providers)
- [x] API documentation: stable schema contract, curl and JS/Python examples, versioning policy

---

## License

[MIT](LICENSE)
