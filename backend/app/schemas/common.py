from typing import Any, Literal

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    path: str | None = None
    issue: str
    received: Any | None = None
    allowed_values: list[Any] | None = None
    suggestion: str | None = None


class APIError(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    success: Literal[False] = False
    error: APIError
    correlation_id: str


class SuccessResponse(BaseModel):
    success: Literal[True] = True
    data: Any
    meta: dict[str, Any] = Field(default_factory=dict)
    correlation_id: str
