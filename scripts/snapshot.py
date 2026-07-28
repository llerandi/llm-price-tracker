"""
Write a compact daily price snapshot to data/history/YYYY-MM-DD.json.

Only stores pricing fields - the minimal set needed to reconstruct price
history and detect changes over time.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRICES_FILE = ROOT / "data" / "prices.json"
HISTORY_DIR = ROOT / "data" / "history"

PRICE_FIELDS = (
    "input_per_1m_usd",
    "output_per_1m_usd",
    "batch_input_per_1m_usd",
    "batch_output_per_1m_usd",
    "cache_read_per_1m_usd",
    "cache_write_per_1m_usd",
)


def main() -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    data: dict = json.loads(PRICES_FILE.read_text(encoding="utf-8"))
    today = datetime.now(tz=timezone.utc).date().isoformat()

    snapshot = {
        "date": today,
        "models": [
            {
                "provider": m["provider"],
                "model_id": m["model_id"],
                **{f: m.get(f) for f in PRICE_FIELDS},
            }
            for m in data["models"]
        ],
    }

    out = HISTORY_DIR / f"{today}.json"
    out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Snapshot written: {out.name} ({len(snapshot['models'])} models)")


if __name__ == "__main__":
    main()
