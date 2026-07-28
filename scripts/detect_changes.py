"""
Compare the two most recent snapshots in data/history/ and report
price changes greater than THRESHOLD (default 10%).

Writes 'changed=true' or 'changed=false' to stdout for use as a
GitHub Actions output variable. If changes are found, also writes a
markdown summary to the path in the SUMMARY_FILE environment variable
(default: /tmp/price_changes.md).
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
HISTORY_DIR = ROOT / "data" / "history"
THRESHOLD = 0.10

PRICE_FIELDS: list[tuple[str, str]] = [
    ("input_per_1m_usd", "Input"),
    ("output_per_1m_usd", "Output"),
    ("batch_input_per_1m_usd", "Batch Input"),
    ("batch_output_per_1m_usd", "Batch Output"),
    ("cache_read_per_1m_usd", "Cache Read"),
    ("cache_write_per_1m_usd", "Cache Write"),
]


def load_snapshot(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {m["model_id"]: m for m in data["models"]}


def pct_change(old: float | None, new: float | None) -> float | None:
    if old is None or new is None or old == 0:
        return None
    return (new - old) / old


def build_summary(
    date_prev: str,
    date_curr: str,
    price_changes: list[dict],
    new_models: list[dict],
    removed_models: list[dict],
) -> str:
    lines = [
        f"## Price changes detected: {date_prev} to {date_curr}",
        "",
        (
            f"The following prices changed by more than {int(THRESHOLD * 100)}% "
            "since the previous daily snapshot."
        ),
        "",
    ]

    if price_changes:
        lines += [
            "### Price changes",
            "",
            "| Provider | Model | Field | Old | New | Change |",
            "|----------|-------|-------|-----|-----|--------|",
        ]
        for c in price_changes:
            sign = "+" if c["pct"] > 0 else ""
            lines.append(
                f"| {c['provider']} | {c['model_name']} | {c['field']} "
                f"| ${c['old']:.2f} | ${c['new']:.2f} | {sign}{c['pct'] * 100:.1f}% |"
            )
        lines.append("")

    if new_models:
        lines += ["### New models", ""]
        for c in new_models:
            lines.append(f"- {c['provider']}: `{c['model_id']}`")
        lines.append("")

    if removed_models:
        lines += ["### Removed models", ""]
        for c in removed_models:
            lines.append(f"- {c['provider']}: `{c['model_id']}`")
        lines.append("")

    lines += [
        "---",
        "_Opened automatically by the daily update workflow._",
        "_Source: [data/prices.json](https://github.com/llerandi/llm-price-tracker/blob/main/data/prices.json)_",
    ]

    return "\n".join(lines)


def main() -> None:
    snapshots = sorted(HISTORY_DIR.glob("*.json"))
    if len(snapshots) < 2:
        print("changed=false")
        return

    date_prev = snapshots[-2].stem
    date_curr = snapshots[-1].stem
    prev = load_snapshot(snapshots[-2])
    curr = load_snapshot(snapshots[-1])

    price_changes: list[dict] = []
    new_models: list[dict] = []
    removed_models: list[dict] = []

    for model_id, curr_model in curr.items():
        prev_model = prev.get(model_id)
        if prev_model is None:
            new_models.append({"provider": curr_model["provider"], "model_id": model_id})
            continue
        for field, label in PRICE_FIELDS:
            pct = pct_change(prev_model.get(field), curr_model.get(field))
            if pct is not None and abs(pct) >= THRESHOLD:
                price_changes.append(
                    {
                        "provider": curr_model["provider"],
                        "model_name": curr_model.get("model_name", model_id),
                        "field": label,
                        "old": prev_model[field],
                        "new": curr_model[field],
                        "pct": pct,
                    }
                )

    for model_id, prev_model in prev.items():
        if model_id not in curr:
            removed_models.append(
                {"provider": prev_model["provider"], "model_id": model_id}
            )

    if not price_changes and not new_models and not removed_models:
        print("changed=false")
        return

    summary = build_summary(date_prev, date_curr, price_changes, new_models, removed_models)
    summary_file = Path(os.environ.get("SUMMARY_FILE", "/tmp/price_changes.md"))
    summary_file.write_text(summary, encoding="utf-8")

    print("changed=true")


if __name__ == "__main__":
    main()
