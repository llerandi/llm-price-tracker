"""
Generate data/changelog.md by comparing all consecutive daily snapshots
in data/history/ and recording price changes, new models, and removals.

Run after snapshot.py so the current day's snapshot is already written.
The output file is regenerated from scratch on every run (idempotent).
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
HISTORY_DIR = ROOT / "data" / "history"
CHANGELOG_FILE = ROOT / "data" / "changelog.md"

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


def compare(
    prev: dict[str, dict], curr: dict[str, dict]
) -> tuple[list[dict], list[dict], list[dict]]:
    """Return (price_changes, new_models, removed_models)."""
    price_changes: list[dict] = []
    new_models: list[dict] = []
    removed_models: list[dict] = []

    for model_id, curr_m in curr.items():
        prev_m = prev.get(model_id)
        if prev_m is None:
            new_models.append(curr_m)
            continue
        for field, label in PRICE_FIELDS:
            pct = pct_change(prev_m.get(field), curr_m.get(field))
            if pct is not None and abs(pct) >= 0.001:  # any change, not just >10%
                price_changes.append(
                    {
                        "provider": curr_m["provider"],
                        "model_name": curr_m.get("model_name", model_id),
                        "field": label,
                        "old": prev_m[field],
                        "new": curr_m[field],
                        "pct": pct,
                    }
                )

    for model_id, prev_m in prev.items():
        if model_id not in curr:
            removed_models.append(prev_m)

    return price_changes, new_models, removed_models


def fmt(v: float | None) -> str:
    return f"${v:.4f}".rstrip("0").rstrip(".") + "/1M" if v is not None else "N/A"


def render_entry(
    date_prev: str,
    date_curr: str,
    price_changes: list[dict],
    new_models: list[dict],
    removed_models: list[dict],
) -> str:
    lines = [f"## {date_curr}", ""]

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
                f"| {fmt(c['old'])} | {fmt(c['new'])} | {sign}{c['pct'] * 100:.1f}% |"
            )
        lines.append("")

    if new_models:
        lines += ["### New models", ""]
        for m in new_models:
            inp = fmt(m.get("input_per_1m_usd"))
            out = fmt(m.get("output_per_1m_usd"))
            name = m.get("model_name", m.get("model_id", ""))
            lines.append(f"- **{m['provider']}** {name} — {inp} in / {out} out")
        lines.append("")

    if removed_models:
        lines += ["### Removed models", ""]
        for m in removed_models:
            name = m.get("model_name", m.get("model_id", ""))
            lines.append(f"- **{m['provider']}** {name}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    snapshots = sorted(HISTORY_DIR.glob("*.json"))
    if len(snapshots) < 2:
        header = (
            "# Price Changelog\n\n"
            "All price changes, new models, and removals detected by the daily update workflow.\n"
            "Sorted by date (newest first). "
            "Source: [`data/history/`](data/history/)\n\n"
            "---\n\n"
            "_No changes recorded yet._\n"
        )
        CHANGELOG_FILE.write_text(header, encoding="utf-8")
        print("Not enough snapshots to compare (need at least 2). Empty changelog written.")
        return

    entries: list[str] = []
    for i in range(len(snapshots) - 1, 0, -1):  # newest first
        date_curr = snapshots[i].stem
        date_prev = snapshots[i - 1].stem
        prev = load_snapshot(snapshots[i - 1])
        curr = load_snapshot(snapshots[i])
        price_changes, new_models, removed_models = compare(prev, curr)
        if price_changes or new_models or removed_models:
            entries.append(render_entry(date_prev, date_curr, price_changes, new_models, removed_models))

    header = (
        "# Price Changelog\n\n"
        "All price changes, new models, and removals detected by the daily update workflow.\n"
        "Sorted by date (newest first). "
        "Source: [`data/history/`](data/history/)\n\n"
        "---\n\n"
    )

    if entries:
        content = header + "\n---\n\n".join(entries)
    else:
        content = header + "_No changes recorded yet._\n"

    CHANGELOG_FILE.write_text(content, encoding="utf-8")
    print(f"Changelog written: {len(entries)} entries from {len(snapshots)} snapshots.")


if __name__ == "__main__":
    main()
