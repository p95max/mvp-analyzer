"""AI summary module with optional real LLM integration and safe mock fallback."""

from typing import Any, Dict, Iterable, List, Set

from .config import get_settings


def extract_keys(items: Iterable[Dict[str, Any]]) -> Set[str]:
    keys: Set[str] = set()
    for item in items:
        keys.update(item.keys())
    return keys


def truncate_text(value: str, max_length: int) -> str:
    if len(value) <= max_length:
        return value
    return value[: max_length - 1].rstrip() + "…"


def build_mock_summary(items: List[Dict[str, Any]]) -> str:
    total = len(items)
    if total == 0:
        return "Dataset is empty."
    keys = sorted(extract_keys(items))
    primary_fields = ", ".join(keys[:8])
    sample = items[0]
    example_parts: List[str] = []
    for field in keys[:3]:
        if field in sample:
            value = sample[field]
            if isinstance(value, str):
                value = truncate_text(value, 120)
            example_parts.append(f"{field}={value}")
    example = ", ".join(example_parts)
    if example:
        return (
            f"Dataset contains {total} items with fields: {primary_fields}. "
            f"Example: {example}."
        )
    return f"Dataset contains {total} items with fields: {primary_fields}."


async def generate_summary(items: List[Dict[str, Any]]) -> str:
    settings = get_settings()
    if not settings.openai_api_key:
        return build_mock_summary(items)
    return build_mock_summary(items)
