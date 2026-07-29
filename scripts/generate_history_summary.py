"""
Generate data/history_summary.json by reading all snapshots in data/history/.
Produces a consolidated time-series file consumed by the price history chart.

Run after snapshot.py. Idempotent - regenerated from scratch on every run.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
HISTORY_DIR = ROOT / "data" / "history"
SUMMARY_FILE = ROOT / "data" / "history_summary.json"


def main() -> None:
    snapshots = sorted(HISTORY_DIR.glob("*.json"))
    if not snapshots:
        print("No snapshots found.")
        return

    dates = [p.stem for p in snapshots]
    models: dict[str, dict] = {}

    for i, path in enumerate(snapshots):
        data = json.loads(path.read_text(encoding="utf-8"))
        for m in data["models"]:
            mid = m["model_id"]
            if mid not in models:
                models[mid] = {
                    "provider": m["provider"],
                    "model_name": m.get("model_name", mid),
                    "input": [None] * len(dates),
                    "output": [None] * len(dates),
                }
            models[mid]["input"][i] = m.get("input_per_1m_usd")
            models[mid]["output"][i] = m.get("output_per_1m_usd")

    summary = {
        "last_updated": datetime.now(tz=timezone.utc).date().isoformat(),
        "dates": dates,
        "models": models,
    }

    SUMMARY_FILE.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"History summary written: {len(models)} models across {len(dates)} date(s).")


if __name__ == "__main__":
    main()
