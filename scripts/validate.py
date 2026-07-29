"""Validate the structure and content of data/prices.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRICES_FILE = ROOT / "data" / "prices.json"

REQUIRED_FIELDS: dict[str, type | tuple[type, ...]] = {
    "provider": str,
    "model_id": str,
    "model_name": str,
    "input_per_1m_usd": (int, float, type(None)),
    "output_per_1m_usd": (int, float, type(None)),
    "context_window_k": (int, type(None)),
    "supports_vision": bool,
    "supports_function_calling": bool,
    "is_reasoning": bool,
    "tier": str,
}

OPTIONAL_FIELDS: dict[str, type | tuple[type, ...]] = {
    "batch_input_per_1m_usd": (int, float, type(None)),
    "batch_output_per_1m_usd": (int, float, type(None)),
    "cache_read_per_1m_usd": (int, float, type(None)),
    "cache_write_per_1m_usd": (int, float, type(None)),
    "is_embedding": bool,
}

VALID_TIERS = {"efficient", "performance", "flagship", "specialized"}


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    if "schema_version" not in data:
        errors.append("Missing top-level 'schema_version' key.")

    if "models" not in data:
        errors.append("Missing top-level 'models' key.")
        return errors

    if not isinstance(data["models"], list):
        errors.append("'models' must be a list.")
        return errors

    seen_ids: set[str] = set()

    for i, model in enumerate(data["models"]):
        prefix = f"models[{i}] ({model.get('model_id', '?')})"

        for field, expected_type in REQUIRED_FIELDS.items():
            if field not in model:
                errors.append(f"{prefix}: missing required field '{field}'.")
                continue
            if not isinstance(model[field], expected_type):
                errors.append(
                    f"{prefix}: '{field}' should be {expected_type}, "
                    f"got {type(model[field]).__name__}."
                )

        for field, expected_type in OPTIONAL_FIELDS.items():
            if field in model and not isinstance(model[field], expected_type):
                errors.append(
                    f"{prefix}: '{field}' should be {expected_type}, "
                    f"got {type(model[field]).__name__}."
                )

        all_price_fields = (
            "input_per_1m_usd", "output_per_1m_usd",
            "batch_input_per_1m_usd", "batch_output_per_1m_usd",
            "cache_read_per_1m_usd", "cache_write_per_1m_usd",
        )
        for price_field in all_price_fields:
            value = model.get(price_field)
            if value is not None and value < 0:
                errors.append(f"{prefix}: '{price_field}' must be >= 0.")

        tier = model.get("tier")
        if tier and tier not in VALID_TIERS:
            errors.append(
                f"{prefix}: invalid tier '{tier}'. "
                f"Valid values: {sorted(VALID_TIERS)}."
            )

        model_id = model.get("model_id")
        if model_id:
            if model_id in seen_ids:
                errors.append(f"{prefix}: duplicate model_id '{model_id}'.")
            seen_ids.add(model_id)

    return errors


def main() -> None:
    if not PRICES_FILE.exists():
        print(f"ERROR: {PRICES_FILE} not found.")
        sys.exit(1)

    data = json.loads(PRICES_FILE.read_text())
    errors = validate(data)

    if errors:
        print(f"Validation failed with {len(errors)} error(s):\n")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print(f"OK - {len(data['models'])} models validated successfully.")


if __name__ == "__main__":
    main()
