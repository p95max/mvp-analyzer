"""HTTP client for the external data source."""

from typing import Any, Dict, List
import httpx
from fastapi import HTTPException, status
from .config import get_settings


class ExternalAPIClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=10.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def fetch_dataset(self, resource: str) -> List[Dict[str, Any]]:
        path = f"/{resource.lstrip('/')}"
        try:
            response = await self._client.get(path)
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External API request failed: {exc}",
            ) from exc

        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown dataset resource: {resource}",
            )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External API returned error: {exc.response.status_code}",
            ) from exc

        data = response.json()
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unexpected payload format from external API",
        )


def create_external_api_client() -> ExternalAPIClient:
    settings = get_settings()
    return ExternalAPIClient(base_url=str(settings.external_api_base_url))
