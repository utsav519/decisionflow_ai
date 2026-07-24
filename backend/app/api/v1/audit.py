"""
Audit API router — read-only access to audit trail.

Spec reference: API contract §8
"""

from __future__ import annotations

import math

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_correlation_id
from app.core.exceptions import AuditNotFoundError
from app.db.session import get_db
from app.repositories.audit_repository import AuditRepository

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("")
def list_audit_logs(
    response: Response,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    action: str | None = Query(None),
    entity_type: str | None = Query(None),
    entity_id: str | None = Query(None),
    performed_by: str | None = Query(None),
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    """List audit log entries with pagination and filters."""
    repo = AuditRepository(db)
    logs, total = repo.list_audit_logs(
        page=page,
        page_size=page_size,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        performed_by=performed_by,
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": [_audit_to_dict(log) for log in logs],
        "meta": {
            "page": page,
            "page_size": page_size,
            "total_items": total,
            "total_pages": max(1, math.ceil(total / page_size)),
        },
        "correlation_id": correlation_id,
    }


@router.get("/{audit_id}")
def get_audit_log(
    audit_id: str,
    response: Response,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    """Get a single audit log entry by ID."""
    repo = AuditRepository(db)
    log = repo.get_by_id(audit_id)
    if not log:
        raise AuditNotFoundError(audit_id)

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": _audit_to_dict(log),
        "correlation_id": correlation_id,
    }


def _audit_to_dict(log) -> dict:
    """Convert an AuditLog ORM to a response dict."""
    return {
        "id": log.id,
        "action": log.action,
        "entity_type": log.entity_type,
        "entity_id": log.entity_id,
        "entity_version": log.entity_version,
        "performed_by": log.performed_by,
        "summary": log.summary,
        "request_snapshot": log.request_snapshot_json,
        "result_snapshot": log.result_snapshot_json,
        "metadata": log.metadata_json,
        "correlation_id": log.correlation_id,
        "created_at": log.created_at.isoformat() if log.created_at else None,
    }
