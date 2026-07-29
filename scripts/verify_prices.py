"""
Verify data/prices.json for internal consistency and anomalies.

Checks performed:
  - Required fields are present and non-null
  - No duplicate model_ids
  - All prices are positive
  - Output price >= input price (warns if output < 50% of input)
  - Batch prices do not exceed standard prices
  - Cache read price does not exceed input price
  - Tier is a known value
  - Context window is positive
  - If 30+ daily snapshots exist: flag any price that moved > JUMP_THRESHOLD
    compared to the snapshot from 30 days ago

Exits 0 if all checks pass (warnings are non-fatal).
Exits 1 if any error is found.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRICES_FILE = ROOT / "data" / "prices.json"
HISTORY_DIR = ROOT / "data" / "history"

REQUIRED_FIELDS = [
    "provider",
    "model_id",
    "model_name",
    "input_per_1m_usd",
    "output_per_1m_usd",
]
VALID_TIERS = {"efficient", "performance", "flagship", "specialized"}
JUMP_THRESHOLD = 0.50  # warn if price moved >=50% vs 30 days ago


def check_model(
    m: dict,
    history_30d: dict[str, dict] | None,
) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a single model."""
    errors: list[str] = []
    warnings: list[str] = []
    mid = m.get("model_id", "<unknown>")

    is_embedding = m.get("is_embedding", False)

    # Required fields (embedding models have no output tokens - skip output check)
    for field in REQUIRED_FIELDS:
        if field == "output_per_1m_usd" and is_embedding:
            continue
        if m.get(field) is None:
            errors.append(f"{mid}: missing required field '{field}'")

    # All prices positive
    price_fields = [
        "input_per_1m_usd",
        "output_per_1m_usd",
        "batch_input_per_1m_usd",
        "batch_output_per_1m_usd",
        "cache_read_per_1m_usd",
        "cache_write_per_1m_usd",
    ]
    for field in price_fields:
        v = m.get(field)
        if v is not None and v <= 0:
            errors.append(f"{mid}: {field} must be > 0, got {v}")

    inp = m.get("input_per_1m_usd")
    out = m.get("output_per_1m_usd")

    # Output sanity: warn if output < 50% of input (very unusual)
    if inp is not None and out is not None and out < inp * 0.5:
        warnings.append(
            f"{mid}: output ({out}) is less than 50% of input ({inp}) - verify"
        )

    # Batch prices should not exceed standard prices
    bi = m.get("batch_input_per_1m_usd")
    bo = m.get("batch_output_per_1m_usd")
    if bi is not None and inp is not None and bi > inp * 1.01:
        warnings.append(f"{mid}: batch_input ({bi}) > input ({inp}) - verify")
    if bo is not None and out is not None and bo > out * 1.01:
        warnings.append(f"{mid}: batch_output ({bo}) > output ({out}) - verify")

    # Cache read should not exceed input
    cr = m.get("cache_read_per_1m_usd")
    if cr is not None and inp is not None and cr > inp * 1.01:
        warnings.append(f"{mid}: cache_read ({cr}) > input ({inp}) - verify")

    # Valid tier
    tier = m.get("tier")
    if tier is not None and tier not in VALID_TIERS:
        errors.append(f"{mid}: unknown tier '{tier}' (valid: {', '.join(sorted(VALID_TIERS))})")

    # Context window positive
    ctx = m.get("context_window_k")
    if ctx is not None and ctx <= 0:
        errors.append(f"{mid}: context_window_k must be > 0, got {ctx}")

    # 30-day price jump check
    if history_30d is not None:
        old = history_30d.get(mid)
        if old is not None:
            for field, label in [
                ("input_per_1m_usd", "input"),
                ("output_per_1m_usd", "output"),
            ]:
                old_v = old.get(field)
                new_v = m.get(field)
                if old_v and new_v and old_v > 0:
                    pct = abs(new_v - old_v) / old_v
                    if pct >= JUMP_THRESHOLD:
                        direction = "up" if new_v > old_v else "down"
                        warnings.append(
                            f"{mid}: {label} moved {direction} {pct * 100:.0f}% "
                            f"over 30 days (${old_v} -> ${new_v}) - verify"
                        )

    return errors, warnings


def load_history_30d() -> dict[str, dict] | None:
    """Return a model_id->model dict from ~30 snapshots ago, or None."""
    snapshots = sorted(HISTORY_DIR.glob("*.json"))
    if len(snapshots) < 30:
        return None
    data = json.loads(snapshots[-30].read_text(encoding="utf-8"))
    return {m["model_id"]: m for m in data["models"]}


def main() -> None:
    data = json.loads(PRICES_FILE.read_text(encoding="utf-8"))
    models: list[dict] = data["models"]

    all_errors: list[str] = []
    all_warnings: list[str] = []

    # Duplicate model_ids
    seen: set[str] = set()
    for m in models:
        mid = m.get("model_id", "")
        if mid in seen:
            all_errors.append(f"Duplicate model_id: '{mid}'")
        seen.add(mid)

    history_30d = load_history_30d()
    has_history = history_30d is not None
    snapshots = sorted(HISTORY_DIR.glob("*.json"))

    for m in models:
        errs, warns = check_model(m, history_30d)
        all_errors.extend(errs)
        all_warnings.extend(warns)

    # Print results
    date = datetime.now(tz=timezone.utc).date().isoformat()
    print(f"verify_prices.py - {date}")
    print(f"Models: {len(models)}  |  Snapshots: {len(snapshots)}"
          f"  |  30-day jump check: {'enabled' if has_history else 'disabled (<30 snapshots)'}")
    print()

    for w in all_warnings:
        print(f"  WARNING  {w}")
    for e in all_errors:
        print(f"  ERROR    {e}")

    if not all_errors and not all_warnings:
        print("  All checks passed.")

    print()
    print(f"Result: {len(all_errors)} error(s), {len(all_warnings)} warning(s).")

    if all_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
