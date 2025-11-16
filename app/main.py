"""FastAPI application factory and startup configuration."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from app.config import get_settings
from app.api import router as api_router
from fastapi.responses import RedirectResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level.upper())
    yield


app = FastAPI(
    title="MVP Analyzer",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="")

@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
