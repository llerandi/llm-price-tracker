"""
Sort prices.json, update last_updated, and regenerate the README pricing table.

Run manually or via the GitHub Actions daily workflow.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRICES_FILE = ROOT / "data" / "prices.json"
README_FILE = ROOT / "README.md"

TABLE_START = "<!-- PRICING_TABLE_START -->"
TABLE_END = "<!-- PRICING_TABLE_END -->"

BATCH_TABLE_START = "<!-- BATCH_CACHE_TABLE_START -->"
BATCH_TABLE_END = "<!-- BATCH_CACHE_TABLE_END -->"

SITE_URL = "https://llerandi.github.io/llm-price-tracker/"


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------


def fmt_price(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"${value:.2f}"


def fmt_context(k: int | None) -> str:
    if k is None:
        return "N/A"
    if k >= 1000:
        return f"{k // 1000}M"
    return f"{k}K"


def fmt_capabilities(model: dict) -> str:
    caps = []
    if model.get("supports_vision"):
        caps.append("vision")
    if model.get("supports_function_calling"):
        caps.append("tools")
    if model.get("is_reasoning"):
        caps.append("reasoning")
    return ", ".join(caps) if caps else "-"


# ---------------------------------------------------------------------------
# Table builder
# ---------------------------------------------------------------------------


def pick_preview_models(models: list[dict]) -> list[dict]:
    """Return the cheapest model per provider for the README preview table.

    Models must already be sorted by (provider, input_per_1m_usd) ascending.
    """
    seen: set[str] = set()
    preview: list[dict] = []
    for m in models:
        if m["provider"] not in seen:
            seen.add(m["provider"])
            preview.append(m)
    return preview


def build_table(preview: list[dict], total: int) -> str:
    """Build a short preview table showing one model per provider."""
    header = (
        "| Provider | Model | Input ($/1M) | Output ($/1M) | Context | Capabilities |\n"
        "|----------|-------|:------------:|:-------------:|:-------:|:------------:|\n"
    )
    rows = [
        f"| {m['provider']} "
        f"| {m['model_name']} "
        f"| {fmt_price(m.get('input_per_1m_usd'))} "
        f"| {fmt_price(m.get('output_per_1m_usd'))} "
        f"| {fmt_context(m.get('context_window_k'))} "
        f"| {fmt_capabilities(m)} |"
        for m in preview
    ]
    n_providers = len(preview)
    cta = (
        f"\n_Showing the cheapest model per provider ({n_providers} providers shown, "
        f"{total} models total). "
        f"[**View all models with filters and comparison →**]({SITE_URL})_"
    )
    return header + "\n".join(rows) + cta


def build_batch_cache_note() -> str:
    return (
        f"_Batch and cache pricing is available for select models. "
        f"[**See full pricing table →**]({SITE_URL})_"
    )


def update_readme(table_md: str, batch_cache_md: str, last_updated: str) -> None:
    content = README_FILE.read_text(encoding="utf-8")

    # Replace main pricing table
    pattern = re.compile(
        rf"{re.escape(TABLE_START)}.*?{re.escape(TABLE_END)}", re.DOTALL
    )
    content = pattern.sub(f"{TABLE_START}\n{table_md}\n{TABLE_END}", content, count=1)

    # Replace batch/cache table
    bc_pattern = re.compile(
        rf"{re.escape(BATCH_TABLE_START)}.*?{re.escape(BATCH_TABLE_END)}", re.DOTALL
    )
    content = bc_pattern.sub(
        f"{BATCH_TABLE_START}\n{batch_cache_md}\n{BATCH_TABLE_END}", content, count=1
    )

    # Replace last-updated badge URL
    content = re.sub(
        r"(last--updated-)[0-9]{4}--[0-9]{2}--[0-9]{2}",
        f"last--updated-{last_updated.replace('-', '--')}",
        content,
    )

    README_FILE.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    data: dict = json.loads(PRICES_FILE.read_text(encoding="utf-8"))

    # Sort: provider alphabetically, then by input price ascending
    data["models"].sort(
        key=lambda m: (m["provider"], m.get("input_per_1m_usd") or 0)
    )

    today = datetime.now(tz=timezone.utc).date().isoformat()
    data["last_updated"] = today

    # Write sorted + updated prices
    PRICES_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Regenerate README tables (preview: one model per provider)
    preview = pick_preview_models(data["models"])
    table = build_table(preview, total=len(data["models"]))
    batch_cache_note = build_batch_cache_note()
    update_readme(table, batch_cache_note, today)

    print(f"Done. {len(data['models'])} models. Last updated: {today}")


if __name__ == "__main__":
    main()
