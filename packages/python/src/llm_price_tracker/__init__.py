"""
llm-price-tracker: daily-updated LLM pricing data.

Wraps the llm-price-tracker JSON API served via jsDelivr CDN.
No dependencies - uses the Python standard library only (urllib.request).

Usage::

    from llm_price_tracker import fetch_prices, get_model, get_provider

    data = fetch_prices()
    for m in data["models"]:
        print(m["provider"], m["model_name"], m["input_per_1m_usd"])

    sonnet = get_model("claude-sonnet-5")
    anthropic = get_provider("anthropic")
"""

from __future__ import annotations

import json
import urllib.request
from typing import Any

__all__ = ["fetch_prices", "get_model", "get_provider", "BASE_URL"]

BASE_URL = "https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main"


def _get(url: str) -> Any:
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())


def fetch_prices() -> dict[str, Any]:
    """Fetch the full prices dataset (all providers and models).

    Returns a dict with keys:

    - ``last_updated`` (str): ISO date of the last daily update.
    - ``models`` (list[dict]): all models across all providers.

    Each model dict contains: ``provider``, ``model_id``, ``model_name``,
    ``input_per_1m_usd``, ``output_per_1m_usd``, ``context_window_k``,
    ``supports_vision``, ``supports_function_calling``, ``is_reasoning``,
    ``tier``, ``notes``, and optional batch/cache price fields.
    """
    return _get(f"{BASE_URL}/data/prices.json")


def get_model(model_id: str) -> dict[str, Any] | None:
    """Return a single model by its API identifier, or ``None`` if not found.

    Args:
        model_id: The model's API identifier, e.g. ``"claude-sonnet-5"``,
            ``"gpt-4.1"``, or ``"amazon.nova-pro-v1"``.
    """
    data = fetch_prices()
    for m in data["models"]:
        if m["model_id"] == model_id:
            return m
    return None


def get_provider(provider_slug: str) -> dict[str, Any]:
    """Fetch all models for a single provider.

    Args:
        provider_slug: Lowercase hyphenated provider name, e.g. ``"anthropic"``,
            ``"openai"``, ``"google"``, ``"mistral"``, ``"cohere"``,
            ``"together-ai"``, ``"fireworks-ai"``, ``"ai21-labs"``,
            ``"xai"``, ``"perplexity"``, ``"amazon-bedrock"``.

    Returns the same shape as :func:`fetch_prices`.

    Raises:
        urllib.error.HTTPError: If the provider slug is not recognised.
    """
    return _get(f"{BASE_URL}/data/providers/{provider_slug}.json")
