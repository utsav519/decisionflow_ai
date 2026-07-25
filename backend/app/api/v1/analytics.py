"""
Analytics API router — dashboard metrics.

Spec reference: API contract §7
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_correlation_id
from app.db.session import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
def get_dashboard(
    response: Response,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    """Return aggregated analytics for the dashboard."""
    service = AnalyticsService(db)
    dashboard = service.get_dashboard()

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": dashboard,
        "correlation_id": correlation_id,
    }


@router.get("/summary")
def get_summary(
    response: Response,
    domain: str | None = None,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    service = AnalyticsService(db)
    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": service.get_summary(domain),
        "correlation_id": correlation_id,
    }


@router.get("/decision-distribution")
def get_decision_distribution(
    response: Response,
    domain: str | None = None,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    service = AnalyticsService(db)
    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": service.get_decision_distribution(domain),
        "correlation_id": correlation_id,
    }


@router.get("/decision-trend")
def get_decision_trend(
    response: Response,
    domain: str | None = None,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    service = AnalyticsService(db)
    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": service.get_decision_trend(domain),
        "correlation_id": correlation_id,
    }


@router.get("/top-policies")
def get_top_policies(
    response: Response,
    domain: str | None = None,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    service = AnalyticsService(db)
    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": service.get_top_policies(domain),
        "correlation_id": correlation_id,
    }
