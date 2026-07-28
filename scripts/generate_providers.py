"""
Generate per-provider JSON files in data/providers/{slug}.json.

These are served via jsDelivr CDN as REST-like endpoints so consumers
can fetch pricing for a single provider without downloading the full list.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRICES_FILE = ROOT / "data" / "prices.json"
PROVIDERS_DIR = ROOT / "data" / "providers"


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main() -> None:
    PROVIDERS_DIR.mkdir(parents=True, exist_ok=True)

    data: dict = json.loads(PRICES_FILE.read_text(encoding="utf-8"))
    last_updated: str = data["last_updated"]

    by_provider: dict[str, list[dict]] = {}
    for model in data["models"]:
        by_provider.setdefault(model["provider"], []).append(model)

    for provider, models in by_provider.items():
        out = PROVIDERS_DIR / f"{slugify(provider)}.json"
        out.write_text(
            json.dumps(
                {
                    "provider": provider,
                    "last_updated": last_updated,
                    "model_count": len(models),
                    "models": models,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

    print(f"Generated {len(by_provider)} provider files.")


if __name__ == "__main__":
    main()
