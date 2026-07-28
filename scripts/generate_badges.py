"""
Generate shields.io endpoint JSON files for each model's input and output price.

Files are written to data/badges/{model_id}-input.json and
data/badges/{model_id}-output.json and served via jsDelivr CDN so that
any README can embed a live-updating price badge.
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRICES_FILE = ROOT / "data" / "prices.json"
BADGES_DIR = ROOT / "data" / "badges"

TIER_COLORS: dict[str, str] = {
    "efficient": "brightgreen",
    "performance": "blue",
    "flagship": "orange",
    "specialized": "blueviolet",
}

FIELDS: list[tuple[str, str]] = [
    ("input_per_1m_usd", "input"),
    ("output_per_1m_usd", "output"),
]


def slug(model_id: str) -> str:
    """Return a filesystem-safe version of a model_id (replaces / with -)."""
    return model_id.replace("/", "-")


def fmt_price(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"${value:.2f}/1M"


def main() -> None:
    BADGES_DIR.mkdir(parents=True, exist_ok=True)

    data: dict = json.loads(PRICES_FILE.read_text(encoding="utf-8"))

    # Build the set of expected filenames so we can remove stale files.
    expected: set[str] = set()
    for model in data["models"]:
        file_id = slug(model["model_id"])
        for _, suffix in FIELDS:
            expected.add(f"{file_id}-{suffix}.json")

    removed = 0
    for existing in BADGES_DIR.glob("*.json"):
        if existing.name != ".gitkeep" and existing.name not in expected:
            existing.unlink()
            removed += 1

    count = 0
    for model in data["models"]:
        model_id: str = model["model_id"]
        file_id = slug(model_id)
        color = TIER_COLORS.get(model.get("tier", ""), "blue")

        for field, suffix in FIELDS:
            badge = {
                "schemaVersion": 1,
                "label": f"{model['model_name']} {suffix}",
                "message": fmt_price(model.get(field)),
                "color": color,
            }
            out = BADGES_DIR / f"{file_id}-{suffix}.json"
            out.write_text(
                json.dumps(badge, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            count += 1

    if removed:
        print(f"Removed {removed} stale badge file(s).")
    print(f"Generated {count} badge files for {len(data['models'])} models.")


if __name__ == "__main__":
    main()
