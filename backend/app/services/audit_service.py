"""
Audit service — creates audit records for policy lifecycle events.

Spec reference: §30 Audit & Traceability
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.repositories.audit_repository import AuditRepository

logger = logging.getLogger(__name__)


class AuditService:
    """Creates audit trail entries for all significant events."""

    def __init__(self, db: Session) -> None:
        self.repo = AuditRepository(db)

    def log_policy_created(
        self,
        policy_id: str,
        version: int,
        request_data: dict[str, Any],
        result_data: dict[str, Any],
        performed_by: str,
        correlation_id: str,
    ) -> None:
        self.repo.create({
            "action": "POLICY_CREATED",
            "entity_type": "POLICY",
            "entity_id": policy_id,
            "entity_version": version,
            "performed_by": performed_by,
            "summary": f"Policy '{result_data.get('name', policy_id)}' created as DRAFT.",
            "request_snapshot": request_data,
            "result_snapshot": result_data,
            "correlation_id": correlation_id,
        })

    def log_policy_updated(
        self,
        policy_id: str,
        version: int,
        request_data: dict[str, Any],
        result_data: dict[str, Any],
        performed_by: str,
        correlation_id: str,
    ) -> None:
        self.repo.create({
            "action": "POLICY_UPDATED",
            "entity_type": "POLICY",
            "entity_id": policy_id,
            "entity_version": version,
            "performed_by": performed_by,
            "summary": f"Policy '{result_data.get('name', policy_id)}' updated.",
            "request_snapshot": request_data,
            "result_snapshot": result_data,
            "correlation_id": correlation_id,
        })

    def log_policy_activated(
        self,
        policy_id: str,
        version: int,
        performed_by: str,
        correlation_id: str,
        approval_comment: str | None = None,
    ) -> None:
        self.repo.create({
            "action": "POLICY_ACTIVATED",
            "entity_type": "POLICY",
            "entity_id": policy_id,
            "entity_version": version,
            "performed_by": performed_by,
            "summary": f"Policy '{policy_id}' activated (v{version}).",
            "request_snapshot": {"approval_comment": approval_comment},
            "correlation_id": correlation_id,
        })

    def log_policy_disabled(
        self,
        policy_id: str,
        version: int,
        performed_by: str,
        correlation_id: str,
        reason: str | None = None,
    ) -> None:
        self.repo.create({
            "action": "POLICY_DISABLED",
            "entity_type": "POLICY",
            "entity_id": policy_id,
            "entity_version": version,
            "performed_by": performed_by,
            "summary": f"Policy '{policy_id}' disabled.",
            "request_snapshot": {"reason": reason},
            "correlation_id": correlation_id,
        })

    def log_policy_deleted(
        self,
        policy_id: str,
        version: int,
        performed_by: str,
        correlation_id: str,
    ) -> None:
        self.repo.create({
            "action": "POLICY_DELETED",
            "entity_type": "POLICY",
            "entity_id": policy_id,
            "entity_version": version,
            "performed_by": performed_by,
            "summary": f"Policy '{policy_id}' deleted/archived.",
            "correlation_id": correlation_id,
        })
