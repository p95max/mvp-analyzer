"""Pydantic schemas for request and response models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AnalyzeOptions(BaseModel):
    max_sample_items: Optional[int] = Field(default=None, ge=1, le=100)


class AnalyzeRequest(BaseModel):
    query: str = Field(min_length=1, description="Dataset resource name, for example 'posts'.")
    options: AnalyzeOptions = Field(default_factory=AnalyzeOptions)


class AnalyzeResponse(BaseModel):
    status: str = Field(description="High level status of the operation.")
    source_items: int = Field(description="Number of items received from the external source.")
    items_count: int = Field(description="Alias for source_items for convenience.")
    summary: str = Field(description="Short AI-based summary of dataset content.")
    sample: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Sample of normalized items from the dataset.",
    )
