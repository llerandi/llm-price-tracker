"""
Generate data/feed.xml (Atom 1.0) from daily history snapshots.

Each Atom entry covers one day where at least one price changed, a model was
added, or a model was removed.  The feed is capped at MAX_ENTRIES so it stays
a manageable size even as the history grows.

Run after snapshot.py so today's snapshot is already present.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
HISTORY_DIR = ROOT / "data" / "history"
FEED_FILE = ROOT / "data" / "feed.xml"

SITE_URL = "https://llerandi.github.io/llm-price-tracker/"
FEED_URL = "https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main/data/feed.xml"
REPO_URL = "https://github.com/llerandi/llm-price-tracker"
MAX_ENTRIES = 30

PRICE_FIELDS: list[tuple[str, str]] = [
    ("input_per_1m_usd", "Input"),
    ("output_per_1m_usd", "Output"),
    ("batch_input_per_1m_usd", "Batch Input"),
    ("batch_output_per_1m_usd", "Batch Output"),
    ("cache_read_per_1m_usd", "Cache Read"),
    ("cache_write_per_1m_usd", "Cache Write"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_snapshot(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {m["model_id"]: m for m in data["models"]}


def pct_change(old: float | None, new: float | None) -> float | None:
    if old is None or new is None or old == 0:
        return None
    return (new - old) / old


def xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


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
            if pct is not None and abs(pct) >= 0.001:
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


def build_summary(
    price_changes: list[dict], new_models: list[dict], removed_models: list[dict]
) -> str:
    parts = []
    if price_changes:
        parts.append(f"{len(price_changes)} price change(s)")
    if new_models:
        parts.append(f"{len(new_models)} new model(s)")
    if removed_models:
        parts.append(f"{len(removed_models)} removal(s)")
    return ", ".join(parts)


def build_content(
    date: str,
    price_changes: list[dict],
    new_models: list[dict],
    removed_models: list[dict],
) -> str:
    """Build an HTML fragment for the Atom entry content (wrapped in CDATA)."""
    parts: list[str] = [f"<h2>Price update - {date}</h2>"]

    if price_changes:
        parts.append("<h3>Price changes</h3>")
        parts.append(
            "<table>"
            "<tr><th>Provider</th><th>Model</th><th>Field</th>"
            "<th>Old ($/1M)</th><th>New ($/1M)</th><th>Change</th></tr>"
        )
        for c in price_changes:
            sign = "+" if c["pct"] > 0 else ""
            parts.append(
                f"<tr>"
                f"<td>{xml_escape(c['provider'])}</td>"
                f"<td>{xml_escape(c['model_name'])}</td>"
                f"<td>{c['field']}</td>"
                f"<td>${c['old']:.4f}</td>"
                f"<td>${c['new']:.4f}</td>"
                f"<td>{sign}{c['pct'] * 100:.1f}%</td>"
                f"</tr>"
            )
        parts.append("</table>")

    if new_models:
        parts.append("<h3>New models</h3><ul>")
        for m in new_models:
            name = xml_escape(m.get("model_name", m.get("model_id", "")))
            provider = xml_escape(m.get("provider", ""))
            inp = m.get("input_per_1m_usd")
            out = m.get("output_per_1m_usd")
            pricing = (
                f" — ${inp:.4f}/1M in / ${out:.4f}/1M out"
                if inp is not None and out is not None
                else ""
            )
            parts.append(f"<li><strong>{provider}</strong> {name}{pricing}</li>")
        parts.append("</ul>")

    if removed_models:
        parts.append("<h3>Removed models</h3><ul>")
        for m in removed_models:
            name = xml_escape(m.get("model_name", m.get("model_id", "")))
            provider = xml_escape(m.get("provider", ""))
            parts.append(f"<li><strong>{provider}</strong> {name}</li>")
        parts.append("</ul>")

    parts.append(
        f'<p><a href="{SITE_URL}">Live site</a> &nbsp;|&nbsp; '
        f'<a href="{REPO_URL}/blob/main/data/prices.json">Raw JSON</a></p>'
    )

    return "".join(parts)


# ---------------------------------------------------------------------------
# Feed assembly
# ---------------------------------------------------------------------------


def main() -> None:
    snapshots = sorted(HISTORY_DIR.glob("*.json"))
    now_iso = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    entries: list[dict] = []
    for i in range(len(snapshots) - 1, 0, -1):
        if len(entries) >= MAX_ENTRIES:
            break
        date_curr = snapshots[i].stem
        prev = load_snapshot(snapshots[i - 1])
        curr = load_snapshot(snapshots[i])
        price_changes, new_models, removed_models = compare(prev, curr)
        if price_changes or new_models or removed_models:
            entries.append(
                {
                    "date": date_curr,
                    "price_changes": price_changes,
                    "new_models": new_models,
                    "removed_models": removed_models,
                }
            )

    feed_updated = f"{entries[0]['date']}T06:00:00Z" if entries else now_iso

    lines: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        "  <title>LLM Price Tracker</title>",
        f'  <link href="{SITE_URL}"/>',
        f'  <link rel="self" type="application/atom+xml" href="{FEED_URL}"/>',
        f"  <updated>{feed_updated}</updated>",
        f"  <id>{REPO_URL}</id>",
        "  <author><name>LLM Price Tracker</name></author>",
    ]

    for e in entries:
        date = e["date"]
        summary = build_summary(e["price_changes"], e["new_models"], e["removed_models"])
        content = build_content(
            date, e["price_changes"], e["new_models"], e["removed_models"]
        )
        entry_id = f"{REPO_URL}/blob/main/data/history/{date}.json"

        lines += [
            "  <entry>",
            f"    <title>{xml_escape(f'Price update - {date}: {summary}')}</title>",
            f'    <link href="{SITE_URL}"/>',
            f"    <id>{entry_id}</id>",
            f"    <updated>{date}T06:00:00Z</updated>",
            f"    <summary>{xml_escape(summary)}</summary>",
            f"    <content type=\"html\"><![CDATA[{content}]]></content>",
            "  </entry>",
        ]

    if not entries:
        lines += [
            "  <entry>",
            "    <title>LLM Price Tracker - no changes recorded yet</title>",
            f'    <link href="{SITE_URL}"/>',
            f"    <id>{REPO_URL}/init</id>",
            f"    <updated>{now_iso}</updated>",
            "    <summary>Daily LLM pricing data is now tracked. Price changes will appear here as they are detected.</summary>",
            "  </entry>",
        ]

    lines.append("</feed>")

    FEED_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Feed written: {len(entries)} entry/entries.")


if __name__ == "__main__":
    main()
