"""Basic API tests for the /analyze endpoint."""

import pytest
import sys
from pathlib import Path
from httpx import ASGITransport, AsyncClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.main import app


@pytest.mark.asyncio
async def test_analyze_posts_dataset():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/analyze",
            json={"query": "posts", "options": {}},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["source_items"] == 100
    assert payload["items_count"] == 100
    assert isinstance(payload["summary"], str)
    assert len(payload["sample"]) > 0


@pytest.mark.asyncio
async def test_analyze_unknown_dataset():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/analyze",
            json={"query": "unknown-dataset", "options": {}},
        )

    assert response.status_code == 400
    body = response.json()
    assert "Unknown dataset resource" in body["detail"]
