"""API router exposing the /analyze endpoint."""

from typing import List
from fastapi import APIRouter, Depends
from .ai import generate_summary
from .cache import TTLCache
from .client import ExternalAPIClient
from .config import Settings, get_settings
from .normalizer import normalize_dataset
from .schemas import AnalyzeRequest, AnalyzeResponse


router = APIRouter()


def get_cache(settings: Settings = Depends(get_settings)) -> TTLCache:
    return TTLCache(ttl_seconds=settings.cache_ttl_seconds)


def get_client() -> ExternalAPIClient:
    return ExternalAPIClient(base_url=str(get_settings().external_api_base_url))


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    payload: AnalyzeRequest,
    settings: Settings = Depends(get_settings),
) -> AnalyzeResponse:
    cache = get_cache(settings=settings)
    cache_key = payload.query
    cached = cache.get(cache_key)
    client: ExternalAPIClient = get_client()
    try:
        if cached is not None:
            normalized_items: List[dict] = cached
        else:
            raw_items = await client.fetch_dataset(payload.query)
            normalized_items = normalize_dataset(raw_items)
            cache.set(cache_key, normalized_items)
    finally:
        await client.close()

    max_sample_items = payload.options.max_sample_items or settings.ai_max_sample_items
    sample = normalized_items[:max_sample_items]
    summary = await generate_summary(normalized_items)
    count = len(normalized_items)

    return AnalyzeResponse(
        status="ok",
        source_items=count,
        items_count=count,
        summary=summary,
        sample=sample,
    )
