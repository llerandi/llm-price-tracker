# llm-price-tracker

[![CI](https://img.shields.io/github/actions/workflow/status/edullerandi/llm-price-tracker/ci.yaml?label=CI&logo=github)](https://github.com/edullerandi/llm-price-tracker/actions/workflows/ci.yaml)
[![License](https://img.shields.io/github/license/edullerandi/llm-price-tracker)](LICENSE)
[![Stars](https://img.shields.io/github/stars/edullerandi/llm-price-tracker?style=social)](https://github.com/edullerandi/llm-price-tracker/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/edullerandi/llm-price-tracker)](https://github.com/edullerandi/llm-price-tracker/commits/main)
[![Updated daily](https://img.shields.io/badge/last--updated-2026--07--28-brightgreen)](https://github.com/edullerandi/llm-price-tracker/actions/workflows/update.yaml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python)](https://www.python.org/)

A daily-updated reference of LLM model pricing across all major providers. One source of truth for input/output token costs, context windows, and capabilities - structured as JSON so you can consume it programmatically.

---

## Pricing Table

Prices in USD per 1 million tokens. Sorted by provider, then by input price.

<!-- PRICING_TABLE_START -->
| Provider | Model | Input ($/1M) | Output ($/1M) | Context | Capabilities |
|----------|-------|:------------:|:-------------:|:-------:|:------------:|
| Anthropic | Claude Haiku 4.5 | $1.00 | $5.00 | 200K | vision, tools |
| Anthropic | Claude Sonnet 5 | $2.00 | $10.00 | 200K | vision, tools |
| Anthropic | Claude Opus 5 | $5.00 | $25.00 | 200K | vision, tools |
| Anthropic | Claude Fable 5 | $10.00 | $50.00 | 200K | vision, tools |
| Google | Gemini 2.5 Flash Lite | $0.10 | $0.40 | 1M | vision, tools |
| Google | Gemini 2.5 Flash | $0.15 | $1.25 | 1M | vision, tools |
| Google | Gemini 2.5 Pro | $1.00 | $10.00 | 2M | vision, tools |
| Mistral | Devstral Small 2 | $0.10 | $0.30 | 128K | tools |
| Mistral | Mistral Small 4 | $0.15 | $0.60 | 128K | tools |
| Mistral | Codestral | $0.30 | $0.90 | 256K | tools |
| Mistral | Devstral Medium 2 | $0.40 | $2.00 | 128K | tools |
| Mistral | Mistral Large 3 | $0.50 | $1.50 | 128K | tools |
| Mistral | Mistral Medium 3.5 | $1.50 | $7.50 | 128K | tools |
| OpenAI | GPT-4o mini | $0.15 | $0.60 | 128K | vision, tools |
| OpenAI | GPT-5.6 Luna | $1.00 | $6.00 | 272K | vision, tools |
| OpenAI | o4-mini | $1.10 | $4.40 | 200K | tools, reasoning |
| OpenAI | o3 | $2.00 | $8.00 | 200K | tools, reasoning |
| OpenAI | GPT-4o | $2.50 | $10.00 | 128K | vision, tools |
| OpenAI | GPT-5.6 Terra | $2.50 | $15.00 | 272K | vision, tools |
| OpenAI | GPT-5.6 Sol | $5.00 | $30.00 | 272K | vision, tools |
<!-- PRICING_TABLE_END -->

> **Notes on specific models:**
> - Gemini 2.5 Pro: input $2.50/1M and output $15.00/1M above 200K tokens.
> - GPT-5.6 Sol and Terra: requests above 272K tokens charged at 2x input and 1.5x output.
>
> **Official pricing pages:**
> [Anthropic](https://www.anthropic.com/pricing) -
> [Google](https://ai.google.dev/pricing) -
> [Mistral](https://mistral.ai/technology/#pricing) -
> [OpenAI](https://platform.openai.com/pricing)

---

## Use the Data Programmatically

The `data/prices.json` file is the single source of truth. You can fetch it directly via jsDelivr CDN for zero-latency access:

```
https://cdn.jsdelivr.net/gh/edullerandi/llm-price-tracker@main/data/prices.json
```

Example - fetch and filter in Python:

```python
import urllib.request
import json

url = "https://cdn.jsdelivr.net/gh/edullerandi/llm-price-tracker@main/data/prices.json"
with urllib.request.urlopen(url) as r:
    data = json.load(r)

# Find all models under $1/1M input
cheap = [m for m in data["models"] if (m["input_per_1m_usd"] or 999) < 1.0]
for m in cheap:
    print(f"{m['provider']} {m['model_name']}: ${m['input_per_1m_usd']}/1M input")
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
4. Commits and pushes if there are changes.

A second workflow (`ci.yaml`) runs on every push and pull request to lint the scripts and validate the JSON schema.

---

## Roadmap

### Phase 1 - Foundation

- [x] JSON schema definition
- [x] Initial pricing data: Anthropic, Google, Mistral, OpenAI
- [x] Auto-generated README pricing table from JSON
- [x] CI pipeline (lint + JSON validation)
- [x] Daily automated update workflow

### Phase 2 - Expand

- [ ] Add providers: Cohere, Together AI, Fireworks AI, AI21 Labs
- [ ] Add batch pricing and prompt caching columns
- [ ] Track price history with daily snapshots

### Phase 3 - Tooling

- [ ] GitHub Pages site with sortable and filterable table
- [ ] GitHub Issues alert when a price changes by more than 10%
- [ ] Embeddable price badge for other repositories
- [ ] REST-like endpoint via jsDelivr CDN with CORS support

---

## License

[MIT](LICENSE)
