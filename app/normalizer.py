"""Dataset normalization utilities."""

import re
from typing import Any, Dict, List


def to_snake_case(value: str) -> str:
    value = re.sub(r"[\s\-]+", "_", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"[^a-zA-Z0-9_]", "_", value)
    value = value.strip("_")
    return value.lower()


def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in item.items():
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        new_key = to_snake_case(key)
        if isinstance(value, dict):
            normalized[new_key] = normalize_item(value)
        elif isinstance(value, list):
            normalized[new_key] = normalize_list(value)
        else:
            normalized[new_key] = value
    return normalized


def normalize_list(items: List[Any]) -> List[Any]:
    result: List[Any] = []
    for value in items:
        if isinstance(value, dict):
            result.append(normalize_item(value))
        elif isinstance(value, list):
            result.append(normalize_list(value))
        else:
            result.append(value)
    return result


def normalize_dataset(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_item(item) for item in items]
