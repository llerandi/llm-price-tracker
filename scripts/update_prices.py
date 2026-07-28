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


def build_table(models: list[dict]) -> str:
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
        for m in models
    ]
    return header + "\n".join(rows)


def update_readme(table_md: str, last_updated: str) -> None:
    content = README_FILE.read_text(encoding="utf-8")

    # Replace pricing table
    pattern = re.compile(
        rf"{re.escape(TABLE_START)}.*?{re.escape(TABLE_END)}", re.DOTALL
    )
    table_block = f"{TABLE_START}\n{table_md}\n{TABLE_END}"
    content = pattern.sub(table_block, content, count=1)

    # Replace last-updated badge URL (shields.io dynamic date badge)
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

    # Regenerate README table
    table = build_table(data["models"])
    update_readme(table, today)

    print(f"Done. {len(data['models'])} models. Last updated: {today}")


if __name__ == "__main__":
    main()
