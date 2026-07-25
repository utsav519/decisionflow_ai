"""
Audit log repository — append-only data access for audit_logs table.

Spec reference: §30 Audit & Traceability
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.ids import new_audit_id
from app.models.audit import AuditLog


class AuditRepository:
    """Append-only operations on the audit_logs table."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: dict[str, Any]) -> AuditLog:
        """Insert a new audit record."""
        record = AuditLog(
            id=new_audit_id(),
            action=data["action"],
            entity_type=data["entity_type"],
            entity_id=data["entity_id"],
            entity_version=data.get("entity_version"),
            performed_by=data.get("performed_by"),
            summary=data["summary"],
            request_snapshot_json=data.get("request_snapshot"),
            result_snapshot_json=data.get("result_snapshot"),
            metadata_json=data.get("metadata"),
            correlation_id=data["correlation_id"],
        )
        self.db.add(record)
        self.db.flush()
        return record

    def get_by_id(self, audit_id: str) -> AuditLog | None:
        """Fetch a single audit record by ID."""
        return self.db.query(AuditLog).filter(AuditLog.id == audit_id).first()

    def list_audit_logs(
        self,
        page: int = 1,
        page_size: int = 20,
        action: str | None = None,
        entity_type: str | None = None,
        entity_id: str | None = None,
        performed_by: str | None = None,
    ) -> tuple[list[AuditLog], int]:
        """Return a paginated, filtered list of audit records."""
        query = self.db.query(AuditLog)

        if action:
            query = query.filter(AuditLog.action == action)
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        if entity_id:
            query = query.filter(AuditLog.entity_id == entity_id)
        if performed_by:
            query = query.filter(AuditLog.performed_by == performed_by)

        total = query.count()
        logs = (
            query.order_by(AuditLog.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return logs, total
