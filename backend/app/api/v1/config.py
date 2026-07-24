"""
Config API router — operator and field catalogue endpoints.

Spec reference: API contract §9-10
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_correlation_id
from app.core.domain_catalogue import DomainCatalogue
from app.engine.operators import get_supported_operators

router = APIRouter(prefix="/config", tags=["Config"])


@router.get("/fields")
def list_fields(
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    """Return all registered domain fields."""
    return {
        "success": True,
        "data": DomainCatalogue.get_all_fields(),
        "correlation_id": correlation_id,
    }


@router.get("/operators")
def list_operators(
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    """Return all supported operators."""
    return {
        "success": True,
        "data": get_supported_operators(),
        "correlation_id": correlation_id,
    }
