"""
Policy API router — full CRUD + lifecycle endpoints.

Spec reference: API contract §12-18
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_correlation_id, get_current_user
from app.db.session import get_db
from app.schemas.policy import PolicyCreate, PolicyStateTransition, PolicyUpdate
from app.services.policy_service import PolicyService

router = APIRouter(prefix="/policies", tags=["Policies"])


# ─── CREATE ──────────────────────────────────────────────


@router.post("", status_code=201)
def create_policy(
    body: PolicyCreate,
    response: Response,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
    user_id: str = Depends(get_current_user),
) -> dict:
    """Create a new policy (always starts as DRAFT)."""
    service = PolicyService(db)
    data = body.model_dump(mode="python")

    # Flatten conditions to a serialisable dict
    data["conditions"] = _conditions_to_dict(data["conditions"])
    if data.get("ai_metadata"):
        data["ai_metadata"] = body.ai_metadata.model_dump() if body.ai_metadata else None

    result = service.create_policy(
        data=data,
        performed_by=user_id,
        correlation_id=correlation_id,
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": result["policy"],
        "meta": {
            "validation_status": result["validation_status"],
            "validation_warnings": result["validation_warnings"],
        },
        "correlation_id": correlation_id,
    }


# ─── LIST ────────────────────────────────────────────────


@router.get("")
def list_policies(
    response: Response,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = Query(None),
    decision: str | None = Query(None),
    source: str | None = Query(None),
    domain: str | None = Query(None),
    search: str | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    """List policies with pagination and filters."""
    service = PolicyService(db)
    result = service.list_policies(
        page=page,
        page_size=page_size,
        status=status,
        decision=decision,
        source=source,
        domain=domain,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": result["policies"],
        "meta": result["pagination"],
        "correlation_id": correlation_id,
    }


# ─── GET BY ID ───────────────────────────────────────────


@router.get("/{policy_id}")
def get_policy(
    policy_id: str,
    response: Response,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    """Get a single policy by ID."""
    service = PolicyService(db)
    policy = service.get_policy(policy_id)

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": policy,
        "correlation_id": correlation_id,
    }


# ─── UPDATE ──────────────────────────────────────────────


@router.put("/{policy_id}")
def update_policy(
    policy_id: str,
    body: PolicyUpdate,
    response: Response,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
    user_id: str = Depends(get_current_user),
) -> dict:
    """Update a DRAFT policy."""
    service = PolicyService(db)
    data = body.model_dump(exclude_unset=True)

    if "conditions" in data and data["conditions"] is not None:
        data["conditions"] = _conditions_to_dict(data["conditions"])

    result = service.update_policy(
        policy_id=policy_id,
        data=data,
        performed_by=user_id,
        correlation_id=correlation_id,
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": result["policy"],
        "meta": {
            "validation_status": result["validation_status"],
            "validation_warnings": result["validation_warnings"],
        },
        "correlation_id": correlation_id,
    }


# ─── DELETE ──────────────────────────────────────────────


@router.delete("/{policy_id}")
def delete_policy(
    policy_id: str,
    response: Response,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
    user_id: str = Depends(get_current_user),
) -> dict:
    """Delete/archive a policy."""
    service = PolicyService(db)
    result = service.delete_policy(
        policy_id=policy_id,
        performed_by=user_id,
        correlation_id=correlation_id,
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": result["policy"],
        "meta": {"message": result["message"]},
        "correlation_id": correlation_id,
    }


# ─── ACTIVATE ────────────────────────────────────────────


@router.post("/{policy_id}/activate")
def activate_policy(
    policy_id: str,
    response: Response,
    body: PolicyStateTransition | None = None,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
    user_id: str = Depends(get_current_user),
) -> dict:
    """Activate a policy (DRAFT → ACTIVE)."""
    service = PolicyService(db)
    approval_comment = body.approval_comment if body else None

    result = service.activate_policy(
        policy_id=policy_id,
        performed_by=user_id,
        correlation_id=correlation_id,
        approval_comment=approval_comment,
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": result["policy"],
        "meta": {
            "validation_status": result["validation_status"],
            "validation_warnings": result["validation_warnings"],
        },
        "correlation_id": correlation_id,
    }


# ─── DISABLE ─────────────────────────────────────────────


@router.post("/{policy_id}/disable")
def disable_policy(
    policy_id: str,
    response: Response,
    body: PolicyStateTransition | None = None,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
    user_id: str = Depends(get_current_user),
) -> dict:
    """Disable a policy (ACTIVE → DISABLED)."""
    service = PolicyService(db)
    reason = body.reason if body else None

    result = service.disable_policy(
        policy_id=policy_id,
        performed_by=user_id,
        correlation_id=correlation_id,
        reason=reason,
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": result["policy"],
        "correlation_id": correlation_id,
    }


# ─── HELPERS ─────────────────────────────────────────────


def _conditions_to_dict(conditions) -> dict:
    """Convert a Pydantic ConditionGroup to a plain dict for JSON storage."""
    if hasattr(conditions, "model_dump"):
        return conditions.model_dump(mode="python")
    return conditions
