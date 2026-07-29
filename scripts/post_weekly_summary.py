"""
Post a weekly LLM price summary to GitHub Discussions.

Reads the current prices.json and the 7-day-old snapshot (if available),
builds a markdown summary, and creates a Discussion post via the GitHub
GraphQL API using the GH_TOKEN environment variable.

Requires the repo to have Discussions enabled and a "Weekly Summary"
category to exist (created automatically via GraphQL if absent).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRICES_FILE = ROOT / "data" / "prices.json"
HISTORY_DIR = ROOT / "data" / "history"

SITE_URL = "https://llerandi.github.io/llm-price-tracker/"
REPO_URL = "https://github.com/llerandi/llm-price-tracker"

PRICE_FIELDS: list[tuple[str, str]] = [
    ("input_per_1m_usd", "Input"),
    ("output_per_1m_usd", "Output"),
]


def load_snapshot(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {m["model_id"]: m for m in data["models"]}


def pct_change(old: float | None, new: float | None) -> float | None:
    if old is None or new is None or old == 0:
        return None
    return (new - old) / old


def build_body(data: dict, prev: dict[str, dict] | None, today: str) -> str:
    models = data["models"]
    n_models = len(models)
    n_providers = len({m["provider"] for m in models})

    # Cheapest and most expensive models
    by_input = sorted(
        [m for m in models if m.get("input_per_1m_usd") is not None],
        key=lambda m: m["input_per_1m_usd"],
    )
    cheapest = by_input[:3]
    priciest = by_input[-3:][::-1]

    lines = [
        f"## Weekly LLM Price Summary - {today}",
        "",
        f"Tracking **{n_models} models** across **{n_providers} providers**.",
        f"Data: [{SITE_URL}]({SITE_URL}) | "
        f"[Raw JSON]({REPO_URL}/blob/main/data/prices.json)",
        "",
    ]

    # Price changes this week
    if prev:
        changes: list[dict] = []
        for m in models:
            mid = m["model_id"]
            prev_m = prev.get(mid)
            if prev_m is None:
                continue
            for field, label in PRICE_FIELDS:
                pct = pct_change(prev_m.get(field), m.get(field))
                if pct is not None and abs(pct) >= 0.001:
                    changes.append(
                        {
                            "provider": m["provider"],
                            "model_name": m.get("model_name", mid),
                            "field": label,
                            "old": prev_m[field],
                            "new": m[field],
                            "pct": pct,
                        }
                    )

        new_models = [
            m for m in models if m["model_id"] not in prev
        ]

        if changes or new_models:
            lines += ["### Changes this week", ""]
            if changes:
                lines += [
                    "| Provider | Model | Field | Old | New | Change |",
                    "|----------|-------|-------|-----|-----|--------|",
                ]
                for c in sorted(changes, key=lambda x: abs(x["pct"]), reverse=True):
                    sign = "+" if c["pct"] > 0 else ""
                    lines.append(
                        f"| {c['provider']} | {c['model_name']} | {c['field']} "
                        f"| ${c['old']:.4f} | ${c['new']:.4f} | {sign}{c['pct'] * 100:.1f}% |"
                    )
                lines.append("")
            if new_models:
                lines += ["**New models added:**", ""]
                for m in new_models:
                    inp = m.get("input_per_1m_usd")
                    out = m.get("output_per_1m_usd")
                    pricing = (
                        f" - ${inp}/1M in / ${out}/1M out"
                        if inp is not None and out is not None
                        else ""
                    )
                    lines.append(f"- **{m['provider']}** {m.get('model_name', m['model_id'])}{pricing}")
                lines.append("")
        else:
            lines += ["### Changes this week", "", "_No price changes detected this week._", ""]
    else:
        lines += ["_Not enough history to show weekly changes yet._", ""]

    lines += [
        "### Cheapest models (input price)",
        "",
        "| Provider | Model | Input $/1M | Output $/1M |",
        "|----------|-------|:----------:|:-----------:|",
    ]
    for m in cheapest:
        lines.append(
            f"| {m['provider']} | {m.get('model_name', m['model_id'])} "
            f"| ${m['input_per_1m_usd']:.4f} | ${m.get('output_per_1m_usd', 0):.4f} |"
        )
    lines += [
        "",
        "### Most expensive models (input price)",
        "",
        "| Provider | Model | Input $/1M | Output $/1M |",
        "|----------|-------|:----------:|:-----------:|",
    ]
    for m in priciest:
        lines.append(
            f"| {m['provider']} | {m.get('model_name', m['model_id'])} "
            f"| ${m['input_per_1m_usd']:.4f} | ${m.get('output_per_1m_usd', 0):.4f} |"
        )
    lines += [
        "",
        "---",
        f"_Posted automatically every Monday. "
        f"[Subscribe to updates]({REPO_URL}/discussions) or "
        f"[watch the repo]({REPO_URL}) for price change alerts._",
    ]

    return "\n".join(lines)


def get_discussion_category_id(repo: str) -> str:
    """Return the GraphQL node ID for the 'Weekly Summary' Discussions category."""
    owner, name = repo.split("/")
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        discussionCategories(first: 20) {
          nodes { id name }
        }
      }
    }
    """
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}",
         "-f", f"owner={owner}", "-f", f"name={name}"],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(result.stdout)
    categories = data["data"]["repository"]["discussionCategories"]["nodes"]
    for cat in categories:
        if cat["name"].lower() in ("weekly summary", "announcements", "general"):
            return cat["id"]
    # Fallback: first available category
    if categories:
        return categories[0]["id"]
    print("No Discussions categories found. Enable Discussions on the repo first.", file=sys.stderr)
    sys.exit(1)


def get_repo_id(repo: str) -> str:
    owner, name = repo.split("/")
    query = 'query($owner: String!, $name: String!) { repository(owner: $owner, name: $name) { id } }'
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}",
         "-f", f"owner={owner}", "-f", f"name={name}"],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)["data"]["repository"]["id"]


def create_discussion(repo_id: str, category_id: str, title: str, body: str) -> None:
    mutation = """
    mutation($repoId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
      createDiscussion(input: {
        repositoryId: $repoId,
        categoryId: $categoryId,
        title: $title,
        body: $body
      }) {
        discussion { url }
      }
    }
    """
    result = subprocess.run(
        ["gh", "api", "graphql",
         "-f", f"query={mutation}",
         "-f", f"repoId={repo_id}",
         "-f", f"categoryId={category_id}",
         "-f", f"title={title}",
         "-f", f"body={body}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Failed to create discussion: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(result.stdout)
    url = data["data"]["createDiscussion"]["discussion"]["url"]
    print(f"Discussion created: {url}")


def main() -> None:
    repo = os.environ.get("REPO", "llerandi/llm-price-tracker")
    today = datetime.now(tz=timezone.utc).date().isoformat()

    data = json.loads(PRICES_FILE.read_text(encoding="utf-8"))

    # Load snapshot from ~7 days ago
    snapshots = sorted(HISTORY_DIR.glob("*.json"))
    prev: dict[str, dict] | None = None
    if len(snapshots) >= 7:
        prev = load_snapshot(snapshots[-7])
    elif len(snapshots) >= 2:
        prev = load_snapshot(snapshots[0])

    title = f"Weekly LLM Price Summary - {today}"
    body = build_body(data, prev, today)

    repo_id = get_repo_id(repo)
    category_id = get_discussion_category_id(repo)
    create_discussion(repo_id, category_id, title, body)


if __name__ == "__main__":
    main()
