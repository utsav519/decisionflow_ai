"""
Shared Pydantic schemas for the application.

Includes pagination metadata, API response envelopes, and error details.
Uses Pydantic V2 BaseModels.

Spec reference: §14 Common Schemas
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Detailed information about a specific validation issue."""
    path: str = Field(..., description="The path to the invalid field (e.g., 'body.policy.name')")
    issue: str = Field(..., description="A clear description of why validation failed")
    received: Any | None = Field(None, description="The value that was received")
    allowed_values: list[Any] | None = Field(None, description="List of acceptable values")
    suggestion: str | None = Field(None, description="Suggested fix")

    model_config = ConfigDict(extra="ignore")


class ErrorBody(BaseModel):
    """Structured error payload matching the API contract."""
    code: str = Field(..., description="Application-specific error code")
    message: str = Field(..., description="Human-readable error message")
    details: list[ErrorDetail] = Field(default_factory=list, description="Validation or specific issue details")


class PaginationMeta(BaseModel):
    """Pagination metadata included in list responses."""
    page: int = Field(..., description="Current page number (1-indexed)")
    page_size: int = Field(..., description="Number of items per page")
    total_items: int = Field(..., description="Total number of items matching filters")
    total_pages: int = Field(..., description="Total number of available pages")


class StandardResponse(BaseModel, Generic[T]):
    """Standard success response envelope."""
    success: bool = Field(True, description="Always true for 2xx responses")
    data: T | None = Field(None, description="The primary response payload")
    meta: dict[str, Any] | None = Field(None, description="Additional metadata, like pagination")
    correlation_id: str = Field(..., description="Unique ID for request tracing")


class StandardErrorResponse(BaseModel):
    """Standard error response envelope."""
    success: bool = Field(False, description="Always false for 4xx/5xx responses")
    error: ErrorBody = Field(..., description="Detailed error information")
    correlation_id: str = Field(..., description="Unique ID for request tracing")
