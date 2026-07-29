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

---

## Pricing Table

Prices in USD per 1 million tokens. Sorted by provider, then by input price.

<!-- PRICING_TABLE_START -->
| Provider | Model | Input ($/1M) | Output ($/1M) | Context | Capabilities |
|----------|-------|:------------:|:-------------:|:-------:|:------------:|
| AI21 Labs | Jamba 1.7 Large | $2.00 | $8.00 | 256K | tools |
| Amazon Bedrock | Nova Micro | $0.04 | $0.14 | 128K | tools |
| Amazon Bedrock | Nova Lite | $0.06 | $0.24 | 300K | vision, tools |
| Amazon Bedrock | Nova Pro | $0.80 | $3.20 | 300K | vision, tools |
| Amazon Bedrock | Nova Premier | $2.00 | $8.00 | 1M | vision, tools |
| Anthropic | Claude Haiku 4.5 | $1.00 | $5.00 | 200K | vision, tools |
| Anthropic | Claude Sonnet 5 | $2.00 | $10.00 | 200K | vision, tools |
| Anthropic | Claude Opus 5 | $5.00 | $25.00 | 200K | vision, tools |
| Anthropic | Claude Fable 5 | $10.00 | $50.00 | 200K | vision, tools |
| Cohere | Command R7B | $0.04 | $0.15 | 128K | tools |
| Cohere | Command R | $0.15 | $0.60 | 128K | tools |
| Cohere | Command R+ | $2.50 | $10.00 | 128K | tools |
| Fireworks AI | DeepSeek V4 Flash | $0.14 | $0.28 | 128K | tools |
| Google | Gemini 2.5 Flash Lite | $0.10 | $0.40 | 1M | vision, tools |
| Google | Gemini 2.5 Flash | $0.30 | $2.50 | 1M | vision, tools, reasoning |
| Google | Gemini 3.5 Flash-Lite | $0.30 | $2.50 | 1M | vision, tools |
| Google | Gemini 2.5 Pro | $1.25 | $10.00 | 2M | vision, tools |
| Google | Gemini 3.5 Flash | $1.50 | $9.00 | 1M | vision, tools, reasoning |
| Google | Gemini 3.6 Flash | $1.50 | $7.50 | 1M | vision, tools, reasoning |
| Mistral | Devstral Small 2 | $0.10 | $0.30 | 128K | tools |
| Mistral | Mistral Small 4 | $0.15 | $0.60 | 128K | tools |
| Mistral | Codestral | $0.30 | $0.90 | 256K | tools |
| Mistral | Devstral Medium 2 | $0.40 | $2.00 | 128K | tools |
| Mistral | Mistral Large 3 | $0.50 | $1.50 | 128K | tools |
| Mistral | Mistral Medium 3.5 | $1.50 | $7.50 | 128K | tools |
| OpenAI | GPT-5 Nano | $0.05 | $0.40 | 32K | tools |
| OpenAI | GPT-4.1 Nano | $0.10 | $0.40 | 1M | vision, tools |
| OpenAI | GPT-4.1 Mini | $0.40 | $1.60 | 1M | vision, tools |
| OpenAI | GPT-5.6 Luna | $1.00 | $6.00 | 272K | vision, tools |
| OpenAI | o4-mini | $1.10 | $4.40 | 200K | tools, reasoning |
| OpenAI | o3 | $2.00 | $8.00 | 200K | tools, reasoning |
| OpenAI | GPT-4.1 | $2.00 | $8.00 | 1M | vision, tools |
| OpenAI | GPT-5.6 Terra | $2.50 | $15.00 | 272K | vision, tools |
| OpenAI | GPT-5.6 Sol | $5.00 | $30.00 | 272K | vision, tools |
| OpenAI | GPT-5.5 | $5.00 | $30.00 | 272K | vision, tools |
| Perplexity | Sonar | $1.00 | $1.00 | 128K | - |
| Perplexity | Sonar Reasoning Pro | $2.00 | $8.00 | 128K | reasoning |
| Perplexity | Sonar Pro | $3.00 | $15.00 | 200K | - |
| Together AI | Llama 4 Scout | $0.18 | $0.59 | 128K | vision, tools |
| Together AI | DeepSeek V3.1 | $0.60 | $1.70 | 128K | tools |
| xAI | Grok Build 0.1 | $1.00 | $2.00 | 256K | tools |
| xAI | Grok 4.3 | $1.25 | $2.50 | 1M | vision, tools, reasoning |
<!-- PRICING_TABLE_END -->

---

## Batch and Cache Pricing

Some providers offer discounted rates for asynchronous (batch) processing and prompt caching. Prices in USD per 1 million tokens.

- **Batch**: requests are queued and processed asynchronously (typically within 24 hours) at ~50% off standard rates.
- **Cache read**: tokens served from the prompt cache at a fraction of the standard input cost.
- **Cache write**: tokens written to the cache, billed once at a slight premium over the standard input cost (Anthropic and GPT-5.6 models).

<!-- BATCH_CACHE_TABLE_START -->
| Provider | Model | Batch Input ($/1M) | Batch Output ($/1M) | Cache Read ($/1M) | Cache Write ($/1M) |
|----------|-------|:------------------:|:-------------------:|:-----------------:|:------------------:|
| Amazon Bedrock | Nova Micro | $0.02 | $0.07 | N/A | N/A |
| Amazon Bedrock | Nova Lite | $0.03 | $0.12 | N/A | N/A |
| Amazon Bedrock | Nova Pro | $0.40 | $1.60 | N/A | N/A |
| Amazon Bedrock | Nova Premier | $1.00 | $4.00 | N/A | N/A |
| Anthropic | Claude Haiku 4.5 | $0.50 | $2.50 | $0.10 | $1.25 |
| Anthropic | Claude Sonnet 5 | $1.00 | $5.00 | $0.20 | $2.50 |
| Anthropic | Claude Opus 5 | $2.50 | $12.50 | $0.50 | $6.25 |
| Anthropic | Claude Fable 5 | $5.00 | $25.00 | $1.00 | $12.50 |
| Fireworks AI | DeepSeek V4 Flash | $0.07 | $0.14 | $0.07 | N/A |
| Google | Gemini 2.5 Flash Lite | $0.05 | $0.20 | $0.01 | N/A |
| Google | Gemini 2.5 Flash | $0.15 | $1.25 | $0.03 | N/A |
| Google | Gemini 3.5 Flash-Lite | $0.15 | $1.25 | N/A | N/A |
| Google | Gemini 2.5 Pro | $0.62 | $5.00 | $0.12 | N/A |
| Google | Gemini 3.5 Flash | $0.75 | $4.50 | N/A | N/A |
| Google | Gemini 3.6 Flash | $0.75 | $3.75 | N/A | N/A |
| OpenAI | GPT-5 Nano | $0.03 | $0.20 | $0.01 | N/A |
| OpenAI | GPT-4.1 Nano | $0.05 | $0.20 | $0.03 | N/A |
| OpenAI | GPT-4.1 Mini | $0.20 | $0.80 | $0.10 | N/A |
| OpenAI | GPT-5.6 Luna | $0.50 | $3.00 | $0.50 | $1.25 |
| OpenAI | o4-mini | $0.55 | $2.20 | $0.55 | N/A |
| OpenAI | o3 | $1.00 | $4.00 | $1.00 | N/A |
| OpenAI | GPT-4.1 | $1.00 | $4.00 | $0.50 | N/A |
| OpenAI | GPT-5.6 Terra | $1.25 | $7.50 | $1.25 | $3.13 |
| OpenAI | GPT-5.6 Sol | $2.50 | $15.00 | $0.50 | $6.25 |
| OpenAI | GPT-5.5 | $2.50 | $15.00 | $0.50 | N/A |
| xAI | Grok 4.3 | N/A | N/A | $0.20 | N/A |
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
https://img.shields.io/endpoint?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fllerandi%2Fllm-price-tracker%40main%2Fdata%2Fbadges%2F{model-id}-{input|output}.json
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

All endpoints are static JSON files served via jsDelivr CDN with full CORS support (`Access-Control-Allow-Origin: *`). No API key required. Updated daily.

**Base URL:** `https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main`

| Endpoint | Description |
|----------|-------------|
| `/data/prices.json` | All models from all providers |
| `/data/providers/{provider}.json` | Models for a single provider (e.g. `anthropic`, `openai`, `google`, `mistral`, `cohere`, `together-ai`, `fireworks-ai`, `ai21-labs`, `xai`, `perplexity`, `amazon-bedrock`) |
| `/data/history/YYYY-MM-DD.json` | Price snapshot for a given date |
| `/data/history_summary.json` | Consolidated time-series of input/output prices for all models (used by the price history chart) |
| `/data/changelog.md` | All price changes and model additions/removals, newest first |
| `/data/badges/{model-id}-input.json` | shields.io endpoint badge for input price |
| `/data/badges/{model-id}-output.json` | shields.io endpoint badge for output price |

Model IDs that contain `/` (Fireworks AI, Together AI) use `-` in filenames.

**Example - fetch all models and filter by price (Python):**

```python
import urllib.request
import json

BASE = "https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main"

with urllib.request.urlopen(f"{BASE}/data/prices.json") as r:
    data = json.load(r)

cheap = [m for m in data["models"] if (m["input_per_1m_usd"] or 999) < 1.0]
for m in cheap:
    print(f"{m['provider']} {m['model_name']}: ${m['input_per_1m_usd']}/1M input")
```

**Example - fetch a single provider (JavaScript):**

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
| `provider` | string | Provider name (e.g. `"OpenAI"`) |
| `model_id` | string | API identifier for the model |
| `model_name` | string | Human-readable name |
| `input_per_1m_usd` | number or null | Input cost per 1M tokens in USD |
| `output_per_1m_usd` | number or null | Output cost per 1M tokens in USD |
| `context_window_k` | integer or null | Context window in thousands of tokens |
| `supports_vision` | boolean | Whether the model accepts image inputs |
| `supports_function_calling` | boolean | Whether the model supports tool/function calls |
| `is_reasoning` | boolean | Whether the model is a reasoning (chain-of-thought) model |
| `tier` | string | `efficient`, `performance`, `flagship`, or `specialized` |
| `notes` | string | Any pricing caveats or special conditions |
| `batch_input_per_1m_usd` | number or null | Batch input cost per 1M tokens (optional) |
| `batch_output_per_1m_usd` | number or null | Batch output cost per 1M tokens (optional) |
| `cache_read_per_1m_usd` | number or null | Prompt cache read cost per 1M tokens (optional) |
| `cache_write_per_1m_usd` | number or null | Prompt cache write cost per 1M tokens (optional) |

---

## Contributing

Prices change frequently. If you spot an outdated entry or a missing model, contributions are welcome.

1. Fork the repository and create a branch.
2. Edit `data/prices.json` with the correct values.
3. Run `python scripts/validate.py` to check your changes pass validation.
4. Run `python scripts/update_prices.py` to regenerate the README table.
5. Open a pull request with a link to the official pricing page as evidence.

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

**The live site or badges show stale data after a push to main.**

jsDelivr CDN caches files for a period after each push. To force a refresh:

1. Purge the CDN cache by opening this URL in your browser:
   ```
   https://purge.jsdelivr.net/gh/llerandi/llm-price-tracker@main/data/prices.json
   ```
2. Hard-refresh the live site (`Ctrl+Shift+R` on Windows/Linux, `Cmd+Shift+R` on Mac).

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
- [x] GitHub Issues alert when a price changes by more than 10%
- [x] Embeddable price badge for other repositories
- [x] REST-like endpoint via jsDelivr CDN with CORS support

### Phase 4 - Insights

- [x] Price history chart on the live site (visualize changes over time per model)
- [x] Auto-generated changelog: markdown summary of price changes by date
- [x] Cost calculator on the live site (tokens x price = estimated cost)
- [x] Add providers: xAI (Grok), Perplexity, AWS Bedrock

### Phase 5 - Community

- [ ] Automated price verification: script that cross-checks prices against official pages
- [ ] Support for multiple currencies (EUR, GBP) on the live site
- [ ] npm / PyPI package wrapping the jsDelivr JSON endpoint

---

## License

[MIT](LICENSE)
