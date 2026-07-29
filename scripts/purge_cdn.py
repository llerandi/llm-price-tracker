"""
Purge jsDelivr CDN cache for all tracked files after a daily update.

Runs after `git push` in the GitHub Actions workflow so the CDN serves
fresh data within seconds instead of waiting for the default TTL.

Uses urllib (stdlib) and ThreadPoolExecutor for parallel requests.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRICES_FILE = ROOT / "data" / "prices.json"

CDN_BASE = "https://purge.jsdelivr.net/gh/llerandi/llm-price-tracker@main"

# Files that are always regenerated each run
STATIC_PATHS = [
    "data/prices.json",
    "data/latest.json",
    "data/feed.xml",
    "data/changelog.md",
    "data/history_summary.json",
]

BADGE_SUFFIXES = ("input", "output", "context")


def slug(model_id: str) -> str:
    return model_id.replace("/", "-")


def build_paths(data: dict) -> list[str]:
    paths = list(STATIC_PATHS)

    # Badge files - one per model per suffix
    for m in data["models"]:
        file_id = slug(m["model_id"])
        for suffix in BADGE_SUFFIXES:
            paths.append(f"data/badges/{file_id}-{suffix}.json")

    # Per-provider files
    providers = {m["provider"].lower().replace(" ", "-") for m in data["models"]}
    for provider in providers:
        paths.append(f"data/providers/{provider}.json")

    return paths


def purge_one(path: str) -> tuple[str, bool, str]:
    url = f"{CDN_BASE}/{path}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as r:
            return path, True, str(r.status)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return path, False, str(exc)


def main() -> None:
    data = json.loads(PRICES_FILE.read_text(encoding="utf-8"))
    paths = build_paths(data)

    print(f"Purging {len(paths)} paths from jsDelivr CDN...")

    ok = 0
    failed: list[str] = []

    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(purge_one, p): p for p in paths}
        for future in as_completed(futures):
            path, success, detail = future.result()
            if success:
                ok += 1
            else:
                failed.append(path)
                print(f"  warn: {path} - {detail}")

    print(f"Done. {ok}/{len(paths)} purged successfully.")
    if failed:
        print(f"  {len(failed)} failed (CDN will expire normally).")


if __name__ == "__main__":
    main()
